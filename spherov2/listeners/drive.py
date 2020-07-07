from enum import IntEnum
from typing import NamedTuple


class MotorIndexes(IntEnum):
    LEFT_MOTOR_INDEX = 0
    RIGHT_MOTOR_INDEX = 1


class MotorStall(NamedTuple):
    motor_index: MotorIndexes
    is_triggered: bool
