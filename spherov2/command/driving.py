from enum import IntFlag, IntEnum
from functools import partial

from spherov2.packet import Packet


class DriveFlags(IntFlag):
    forward = 0b0
    backward = 0b1
    turbo = 0b10


class StabilizationIndexes(IntEnum):
    NO_CONTROL_SYSTEM = 0
    FULL_CONTROL_SYSTEM = 1
    PITCH_CONTROL_SYSTEM = 2
    ROLL_CONTROL_SYSTEM = 3
    YAW_CONTROL_SYSTEM = 4
    SPEED_AND_YAW_CONTROL_SYSTEM = 5


class Driving:
    __encode = partial(Packet, device_id=22)

    @staticmethod
    def reset_yaw(target_id=None):
        return Driving.__encode(command_id=6, target_id=target_id)

    @staticmethod
    def drive_with_heading(speed, heading, drive_flags: DriveFlags, target_id=None):
        return Driving.__encode(command_id=7, data=[speed, *heading, drive_flags], target_id=target_id)

    @staticmethod
    def set_stabilization(stabilization_index: StabilizationIndexes, target_id=None):
        return Driving.__encode(command_id=12, data=[stabilization_index], target_id=target_id)
