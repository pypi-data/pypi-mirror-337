from enum import IntEnum
from typing import Any

from serde import serde
from pypostcard.types import f32, u8
from openhydroponics.msg import EndpointClass, EndpointInputClass

class Endpoint:

    def __init__(self, node, endpoint_id):
        self._node = node
        self._endpoint_id = endpoint_id

    async def interview(self):
        pass

    @property
    def node(self):
        return self._node

    async def set_config(self, config):
        pass


class InputEndpoint(Endpoint):
    ENDPOINT_CLASS = EndpointClass.Input

    def __init__(self, node, endpoint_id):
        super().__init__(node, endpoint_id)
        self._value = None
        self._scale = None

    def handle_sensor_reading(self, msg):
        self._value = msg.value
        self._scale = msg.scale

    @property
    def value(self):
        return self._value

    @property
    def scale(self):
        return self._scale


class TemperatureEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.Temperature


class HumidityEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.Humidity


class ECConfigType(IntEnum):
    LOW = 0
    HIGH = 1
    GAIN = 2


@serde
class ECConfigCalibration:
    value: f32


@serde
class ECConfigGain:
    value: u8


class ECEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.EC

    async def set_config(self, config):
        if "high" in config and "low" in config:
            print("Do not set high and low at the same time, calibration will be wrong")
            return
        if "high" in config:
            await self.node.set_config(
                ECConfigType.HIGH, ECConfigCalibration(value=f32(config["high"]))
            )
        if "low" in config:
            await self.node.set_config(
                ECConfigType.LOW, ECConfigCalibration(value=f32(config["low"]))
            )
        if "gain" in config:
            await self.node.set_config(
                ECConfigType.GAIN, ECConfigGain(value=u8(config["gain"]))
            )


def get_endpoint_input_class(endpoint_input_class: EndpointInputClass) -> Any:
    if endpoint_input_class == EndpointInputClass.Temperature:
        return TemperatureEndpoint
    if endpoint_input_class == EndpointInputClass.Humidity:
        return HumidityEndpoint
    if endpoint_input_class == EndpointInputClass.EC:
        return ECEndpoint
    return None


def get_endpoint_class(endpoint_class: EndpointClass, endpoint_sub_class) -> Any:
    if endpoint_class == EndpointClass.Input:
        return get_endpoint_input_class(endpoint_sub_class)
    return None
