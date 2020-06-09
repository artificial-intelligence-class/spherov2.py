from typing import NamedTuple, Union


class ToyType(NamedTuple):
    display_name: str
    prefix: Union[str, None]
    filter_prefix: str
    cmd_safe_interval: float


class Color(NamedTuple):
    r: int = None
    g: int = None
    b: int = None


class AppVersion(NamedTuple):
    major: int
    minor: int
    revision: int


class CollisionArgs(NamedTuple):
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
