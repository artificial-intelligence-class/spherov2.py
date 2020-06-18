from enum import IntFlag, IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class DriveFlags(IntFlag):
    FORWARD = 0b0
    BACKWARD = 0b1
    TURBO = 0b10


class StabilizationIndexes(IntEnum):
    NO_CONTROL_SYSTEM = 0
    FULL_CONTROL_SYSTEM = 1
    PITCH_CONTROL_SYSTEM = 2
    ROLL_CONTROL_SYSTEM = 3
    YAW_CONTROL_SYSTEM = 4
    SPEED_AND_YAW_CONTROL_SYSTEM = 5


class RawMotorModes(IntEnum):
    OFF = 0
    FORWARD = 1
    REVERSE = 2


class GenericRawMotorIndexes(IntEnum):
    LEFT_DRIVE = 0
    RIGHT_DRIVE = 1
    HEAD = 2
    LEG = 3


class GenericRawMotorModes(IntEnum):
    MOTOR_OFF = 0
    FORWARD = 1
    REVERSE = 2


class Drive:
    __encode = partial(Packet, device_id=22)

    @staticmethod
    def set_raw_motors(left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed, target_id=None):
        return Drive.__encode(command_id=1, data=[left_mode, left_speed, right_mode, right_speed],
                              target_id=target_id)

    @staticmethod
    def reset_yaw(target_id=None):
        return Drive.__encode(command_id=6, target_id=target_id)

    @staticmethod
    def drive_with_heading(speed, heading, drive_flags: DriveFlags, target_id=None):
        return Drive.__encode(command_id=7, data=[speed, *to_bytes(heading, 2), drive_flags], target_id=target_id)

    @staticmethod
    def generic_raw_motor(index: GenericRawMotorIndexes, mode: GenericRawMotorModes, speed, target_id=None):
        return Drive.__encode(command_id=11, data=[index, mode, *speed], target_id=target_id)

    @staticmethod
    def set_stabilization(stabilization_index: StabilizationIndexes, target_id=None):
        return Drive.__encode(command_id=12, data=[stabilization_index], target_id=target_id)
