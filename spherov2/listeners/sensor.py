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
