from enum import IntEnum
from typing import NamedTuple


class CollisionDetected(NamedTuple):
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    x_axis: bool
    y_axis: bool
    power_x: int
    power_y: int
    power_z: int
    speed: int
    time: float


class SensorStreamingMask(NamedTuple):
    interval: int
    packet_count: int
    data_mask: int


class BotToBotInfraredReadings(NamedTuple):
    back_left: bool
    back_right: bool
    front_left: bool
    front_right: bool


class RgbcSensorValues(NamedTuple):
    red: int
    green: int
    blue: int
    clear: int


class ColorDetection(NamedTuple):
    red: int
    green: int
    blue: int
    confidence: int
    color_classification_id: int


class StreamingServiceData(NamedTuple):
    token: int
    sensor_data: bytearray


class MotorCurrent(NamedTuple):
    left_motor_current: float
    right_motor_current: float
    up_time: int


class MotorTemperature(NamedTuple):
    case_temperature: float
    winding_coil_temperature: float


class ThermalProtectionStatus(IntEnum):
    OK = 0
    WARN = 1
    CRITICAL = 2


class MotorThermalProtectionStatus(NamedTuple):
    left_motor_temperature: float
    left_motor_status: ThermalProtectionStatus
    right_motor_temperature: float
    right_motor_status: ThermalProtectionStatus
