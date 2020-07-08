from enum import IntEnum

from spherov2.toy import Toy
from spherov2.types import ToyType


class BOLT(Toy):
    toy_type = ToyType('Sphero BOLT', 'SB-', 'SB', .075)

    class LEDs(IntEnum):
        FRONT_RED = 0
        FRONT_GREEN = 1
        FRONT_BLUE = 2
        BACK_RED = 3
        BACK_GREEN = 4
        BACK_BLUE = 5
