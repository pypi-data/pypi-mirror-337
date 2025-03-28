import asyncio
import time
from typing import Any, Tuple, TypeVar
from typing import Union
from uuid import UUID
import can
from plum import dispatch
from pypostcard.types import List, u8
from pypostcard.serde import to_postcard

from .phyinterface import CanPhyIface
from openhydroponics import msg as Msg
from .msg import ArbitrationId
from . import endpoint as Endpoint

NodeType = TypeVar("Node")

class NodeManager:
    def __init__(self, phy_iface: CanPhyIface = None):
        self._node_id = 1
        self._nodes = {}
        self._last_node_id = 1

        self._phy_iface = phy_iface or CanPhyIface()
        self._phy_iface.add_listener(self.on_message_received)

    def get_node(self, uuid: Union[str, UUID]) -> Union[NodeType, None]:
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        for node in self._nodes.values():
            if node.uuid == uuid:
                return node
        return None

    async def request_node(
        self, uuid: Union[str, UUID], timeout_s: float = 2.0
    ) -> Union[NodeType, None]:
        timeout = time.time() + timeout_s
        while time.time() < timeout:
            node = self.get_node(uuid)
            if node:
                return node
            await asyncio.sleep(0.1)
        return None

    def __iter__(self):
        return iter(self._nodes.values())

    @property
    def node_id(self) -> int:
        return self._node_id

    async def on_message_received(self, msg: can.Message):
        arb = ArbitrationId.decode(msg.arbitration_id)
        msg = Msg.Msg.decode(arb, msg.data)
        if msg:
            self._handle_msg(arb, msg)
        else:
            print("Failed to decode message")

    @dispatch
    def _handle_msg(self, arb: ArbitrationId, msg: Msg.Heartbeat):
        node = self._nodes.get(arb.src)
        if node:
            # All good
            return
        node = Node(
            arb.src, UUID("00000000-00000000-00000000-00000000"), self, self._phy_iface
        )
        node.send_rtr(Msg.NodeInfo)

    @dispatch
    def _handle_msg(self, arb: ArbitrationId, msg: Msg.HeartbeatWithIdRequest):
        uuid = UUID(bytes=bytes(msg.uuid))
        if arb.src != 0:
            return
        node = None
        for node_id, n in self._nodes.items():
            if n.uuid == uuid:
                print(f"Node {uuid} already exists")
                node = n
                break
        if not node:
            node_id = self._last_node_id + 1
            print(f"New node {uuid} found. Giving node id {node_id} to it")
            self._last_node_id = node_id
            node = Node(node_id, uuid, self, self._phy_iface)
            self._nodes[node_id] = node
        msg = Msg.IdSet(uuid=msg.uuid)
        node.send_msg(msg)

    @dispatch
    def _handle_msg(self, arb: ArbitrationId, msg: Msg.NodeInfo):
        uuid = UUID(bytes=bytes(msg.uuid))
        node = self._nodes.get(arb.src)
        if not node:
            print(f"Node {uuid} found.")
            node = Node(arb.src, uuid, self, self._phy_iface)
            node._number_of_endpoints = msg.number_of_endpoints
            self._nodes[arb.src] = node
            asyncio.create_task(node.interview())
            return

    @dispatch
    def _handle_msg(self, arb: ArbitrationId, msg: Msg.SensorReading):
        node = self._nodes.get(arb.src)
        if not node:
            print(f"Unknown node {arb.src}")
            return
        node.handle_sensor_reading(msg)

    @dispatch
    def _handle_msg(self, arb: ArbitrationId, msg: Any):
        print("Handle unkwown msg", msg)


class Node:
    def __init__(
        self, node_id: int, uuid: UUID, manager: NodeManager, phy_iface: CanPhyIface
    ):
        self._node_id = node_id
        self._endpoints = {}
        self._uuid = uuid
        self._manager = manager
        self._phy_iface = phy_iface
        self._last_heartbeat = time.time()
        self._number_of_endpoints = -1

    async def interview(self):
        if self._number_of_endpoints == -1:
            self.send_rtr(Msg.NodeInfo)
            resp = await self.wait_for(Msg.NodeInfo)
            if not resp:
                return
            self._number_of_endpoints = resp.number_of_endpoints
        for endpoint in range(self._number_of_endpoints):
            endpoint_info = await self.send_and_wait(
                Msg.EndpointInfoRequest(endpoint_id=u8(endpoint))
            )
            if not endpoint_info:
                continue
            EndpointClass = Endpoint.get_endpoint_class(
                endpoint_info.endpoint_class, endpoint_info.endpoint_sub_class
            )
            if not EndpointClass:
                print(
                    "Unknown endpoint class",
                    endpoint_info.endpoint_class,
                    endpoint_info.endpoint_sub_class,
                )
                continue
            self._endpoints[endpoint] = EndpointClass(self, endpoint)
            await self._endpoints[endpoint].interview()

    def get_endpoint(self, endpoint_id: int) -> Union[Endpoint.Endpoint, None]:
        return self._endpoints.get(endpoint_id)

    def get_endpoint_value(self, endpoint_id: int) -> Tuple[float, int]:
        endpoint = self._endpoints.get(endpoint_id)
        if not endpoint:
            return (None, None)
        return endpoint.value, endpoint.scale

    def handle_sensor_reading(self, msg: Msg.SensorReading):
        endpoint = self._endpoints.get(msg.endpoint_id)
        if not endpoint:
            print("Unknown endpoint", msg.endpoint_id)
            return
        endpoint.handle_sensor_reading(msg)

    @property
    def node_id(self) -> int:
        return self._node_id

    async def send_and_wait(self, request: Any):
        assert request.MSG_TYPE == Msg.MsgType.Request
        response = Msg.Msg.get_msg_cls(request.MSG_ID, Msg.MsgType.Response)
        assert response
        self.send_msg(request)
        return await self.wait_for(response)

    def send_msg(self, msg: Any):
        arb = ArbitrationId(
            prio=False,
            dst=self._node_id,
            master=True,  # We are the master
            src=self._manager.node_id,
            multiframe=False,
            msg_type=0,
            msg_id=msg.MSG_ID,
        )
        data = Msg.Msg.encode(msg)
        self._phy_iface.send_message(arb.encode(), data)

    def send_rtr(self, msg: Any):
        arb = ArbitrationId(
            prio=False,
            dst=self._node_id,
            master=True,  # We are the master
            src=self._manager.node_id,
            multiframe=False,
            msg_type=0,
            msg_id=msg.MSG_ID,
        )
        self._phy_iface.send_message(arb.encode(), b"", is_remote=True)

    async def set_config(self, config_no: int, config):
        cfg = to_postcard(config)
        cfg.extend([0] * (32 - len(cfg)))
        msg = Msg.EndpointConfigRequest(
            endpoint_id=u8(self.node_id),
            config_no=u8(config_no),
            config=List(list(cfg)),
        )
        self.send_msg(msg)

    async def wait_for(self, msg: Any):
        arb = ArbitrationId(
            prio=False,
            dst=self._manager.node_id,
            master=False,
            src=self._node_id,
            multiframe=False,
            msg_type=msg.MSG_TYPE,
            msg_id=msg.MSG_ID,
        )
        try:
            frame = await self._phy_iface.wait_for(arb.encode())
            return Msg.Msg.decode(arb, frame.data)
        except asyncio.TimeoutError:
            print("Timeout waiting for frame", msg)
        return None

    @property
    def uuid(self) -> UUID:
        return self._uuid
