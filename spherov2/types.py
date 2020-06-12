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
