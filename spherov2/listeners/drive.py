from typing import NamedTuple

from spherov2.commands.drive import MotorIndexes


class MotorStall(NamedTuple):
    motor_index: MotorIndexes
    is_triggered: bool
