from dataclasses import dataclass
from enum import IntEnum
from typing import Any

from serde import serde
from pypostcard.types import Enum, List, f32, u8, u16, u32
from pypostcard.serde import from_postcard, take_from_postcard, to_postcard


@dataclass
class ArbitrationId:
    prio: bool
    dst: int
    master: bool
    src: int
    multiframe: bool
    msg_type: int
    msg_id: int

    def encode(self):
        id = (
            (self.prio << 28)
            | (self.dst << 21)
            | (self.master << 20)
            | (self.src << 13)
            | (self.multiframe << 12)
            | (self.msg_type << 10)
            | self.msg_id
        )
        return id

    @staticmethod
    def decode(id: int):
        return ArbitrationId(
            prio=bool((id >> 28) & 0x1),
            dst=(id >> 21) & 0b1111111,
            master=bool((id >> 20) & 1),
            src=(id >> 13) & 0b1111111,
            multiframe=bool((id >> 12) & 1),
            msg_type=(id >> 10) & 0b11,
            msg_id=id & 0b1111111111,
        )


class MsgType(IntEnum):
    Request = 0
    Response = 1
    Value = 2


class MsgId(IntEnum):
    Heartbeat = 1
    HeartbeatWithIdRequest = 2
    IdSet = 3
    NodeInfo = 4
    EndpointInfo = 5
    SensorReading = 6
    ActuatorOutput = 7
    EndpointConfig = 8


class EndpointClass(IntEnum):
    NotSupported = 0
    Input = 1
    Output = 2


class EndpointInputClass(IntEnum):
    NotSupported = 0
    Temperature = 1
    Humidity = 2
    EC = 3


class Msg:
    messages = {}

    def __init__(self, msg_id: MsgId, msg_type: MsgType) -> None:
        self._msg_id = msg_id
        self._msg_type = msg_type

    def __call__(self, cls):
        cls.MSG_ID = self._msg_id
        cls.MSG_TYPE = self._msg_type
        Msg.messages[(self._msg_id, self._msg_type)] = cls
        return serde(cls)

    @staticmethod
    def encode(msg: Any) -> bytes:
        header = Header(msg_id=u16(msg.MSG_ID))
        data = to_postcard(header)
        return data + to_postcard(msg)

    @staticmethod
    def decode(arb: ArbitrationId, data: bytes):
        header, bytes_decoded = take_from_postcard(Header, data)
        msg_id = header.msg_id
        msg_type = arb.msg_type
        msg_cls = Msg.messages.get((msg_id, msg_type), None)
        if not msg_cls:
            print(f"Unknown message id: {msg_id} {msg_type}")
            return None
        return from_postcard(msg_cls, data[bytes_decoded:])

    @staticmethod
    def get_msg_cls(msg_id: MsgId, msg_type: MsgType):
        return Msg.messages.get((msg_id, msg_type), None)


@serde
class Header:
    msg_id: u16


@Msg(MsgId.Heartbeat, MsgType.Value)
class Heartbeat:
    counter: u32


@Msg(MsgId.HeartbeatWithIdRequest, MsgType.Request)
class HeartbeatWithIdRequest:
    counter: u32
    uuid: List[u8, 16]


@Msg(MsgId.IdSet, MsgType.Request)
class IdSet:
    uuid: List[u8, 16]


@Msg(MsgId.NodeInfo, MsgType.Value)
class NodeInfo:
    uuid: List[u8, 16]
    number_of_endpoints: u8


@Msg(MsgId.EndpointInfo, MsgType.Request)
class EndpointInfoRequest:
    endpoint_id: u8


@Msg(MsgId.EndpointInfo, MsgType.Response)
class EndpointInfoResponse:
    id: u8
    endpoint_class: Enum[u8, EndpointClass]
    endpoint_sub_class: u8


@Msg(MsgId.SensorReading, MsgType.Value)
class SensorReading:
    endpoint_id: u8
    value: f32
    scale: u8


@Msg(MsgId.ActuatorOutput, MsgType.Value)
class ActuatorOutput:
    endpoint_id: u8
    value: f32


@Msg(MsgId.EndpointConfig, MsgType.Request)
class EndpointConfigRequest:
    endpoint_id: u8
    config_no: u8
    config: List[u8, 32]
