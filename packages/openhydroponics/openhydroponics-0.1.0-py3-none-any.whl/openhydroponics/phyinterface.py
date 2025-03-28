import asyncio
import logging
import traceback
from typing import AsyncIterator, Callable, Awaitable, List, Optional
import can
import serial.tools.list_ports

from openhydroponics.msg_pipe import MsgPipe

LOG = logging.getLogger(__name__)


class Listener(can.Listener):
    def __init__(self, phy_iface):
        self._phy_iface = phy_iface

    def on_message_received(self, msg):
        self._phy_iface.on_message_received(msg)


class CanPhyIface:
    MsgCallback = Callable[[bytes], Awaitable[None]]

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._lock = asyncio.Lock()
        self._listeners: List[CanPhyIface.MsgCallback] = []
        self._msg_pipe = MsgPipe()

        interface = "socketcan"
        channel = "can0"

        if channel is None:
            return

        self._bus = can.Bus(
            interface=interface,
            channel=channel,
            bitrate=1000000,
            receive_own_messages=False,
            fd=True,
        )
        self._listener = Listener(self)
        can.Notifier(self._bus, [self._listener])

    def add_listener(self, callback: MsgCallback) -> None:
        """Add a listener callback that will be called on for every message received"""
        self._listeners.append(callback)

    async def _call_listeners(self, msg: can.Message) -> None:
        async with self._lock:
            # Only handle one msg at a time. This is called by another thread and may be called again before we
            # handle the previous msg
            calls = []
            for listener in self._listeners:
                calls.append(listener(msg))
            try:
                await asyncio.gather(*calls)
            except Exception as exception:  # pylint: disable=broad-except
                print(exception)
                traceback.print_exception(exception)

            await self._msg_pipe.send(msg)

    def on_message_received(self, msg: can.Message) -> None:
        asyncio.run_coroutine_threadsafe(self._call_listeners(msg), self._loop)

    def send_message(self, arb: int, msg: bytes, is_remote=False) -> None:
        """Send a message over the CAN bus"""
        msg = CanPhyIface.pad_data(msg)
        if is_remote:
            self._bus.send(
                can.Message(arbitration_id=arb, is_fd=False, is_remote_frame=True)
            )
        else:
            self._bus.send(can.Message(arbitration_id=arb, data=msg, is_fd=True))

    async def wait_for(self, arb: int, timeout: Optional[float] = 2.0) -> can.Message:
        """Listen on incoming can frames and wait for a specific arbitration id"""
        async for msg in self.wait_for_many(arb, timeout):
            return msg

    async def wait_for_many(
        self, arb: int, timeout: Optional[float] = 2.0
    ) -> AsyncIterator[can.Message]:
        """Listen on incoming can frames and wait for multiple frames with a specific arbitration id"""

        async for msg in self._msg_pipe.wait_for_messages(timeout):
            if msg.arbitration_id == arb:
                yield msg
        raise asyncio.exceptions.TimeoutError()

    @staticmethod
    def get_slcan_channel():
        SUPPORTED_SLCAN_VIDS = [
            0xAD50,  # CANABLE
            0x16D0,  # CANABLE 2.0
            0x1E3,  # KORLAN_USB2CAN
        ]
        for port in serial.tools.list_ports.comports():
            if port.vid in SUPPORTED_SLCAN_VIDS:
                return port.device
        LOG.error("No supported slcan device found")
        return None

    @staticmethod
    def pad_data(data: bytes) -> bytes:
        """Pad data to valid CAN FD frame length"""
        if len(data) <= 8:
            return data
        for fdlen in (12, 16, 20, 24, 32, 48, 64):
            if fdlen >= len(data):
                return data.ljust(fdlen, b"\x00")
        raise ValueError("Data too long for CAN FD frame")
