from enum import IntEnum

from spherov2.toy.core import Toy
from spherov2.types import ToyType


class BB9E(Toy):
    toy_type = ToyType('BB-9E', 'GB-', 'GB', .12)

    class LEDs(IntEnum):
        BODY_RED = 0
        BODY_GREEN = 1
        BODY_BLUE = 2
        AIMING = 3
        HEAD = 4
