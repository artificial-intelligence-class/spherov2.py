from enum import IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class CollisionDetectionMethods(IntEnum):
    OFF = 0
    DEFAULT = 1


class RollModes(IntEnum):
    STOP = 0
    GO = 1
    CALIBRATE = 2


class ReverseFlags(IntEnum):
    OFF = 0
    ON = 1


class RawMotorModes(IntEnum):
    OFF = 0
    FORWARD = 1
    REVERSE = 2
    BRAKE = 3
    IGNORE = 4


class Sphero:
    __encode = partial(Packet, device_id=2)

    @staticmethod
    def set_heading(heading: int, target_id=None):
        return Sphero.__encode(command_id=1, data=to_bytes(heading, 2), target_id=target_id)

    @staticmethod
    def set_stabilization(stabilize: bool, target_id=None):
        return Sphero.__encode(command_id=2, data=[int(stabilize)], target_id=target_id)

    @staticmethod
    def set_data_streaming(interval, num_samples_per_packet, mask, count, extended_mask, target_id=None):
        return Sphero.__encode(command_id=17,
                               data=[*to_bytes(interval, 2), *to_bytes(num_samples_per_packet, 2),
                                     *to_bytes(mask, 4), count & 0xff, *to_bytes(extended_mask, 4)],
                               target_id=target_id)

    @staticmethod
    def configure_collision_detection(collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time, target_id=None):
        return Sphero.__encode(command_id=18,
                               data=[collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time],
                               target_id=target_id)

    @staticmethod
    def configure_locator(flags, x, y, yaw_tare, target_id=None):
        return Sphero.__encode(command_id=19, data=[flags, *to_bytes(x, 2), *to_bytes(y, 2), *to_bytes(yaw_tare, 2)],
                               target_id=target_id)

    @staticmethod
    def set_main_led(r, g, b, target_id=None):
        return Sphero.__encode(command_id=32, data=[r, g, b], target_id=target_id)

    @staticmethod
    def set_back_led_brightness(brightness, target_id=None):
        return Sphero.__encode(command_id=33, data=[brightness], target_id=target_id)

    @staticmethod
    def roll(speed, heading, roll_mode: RollModes, reverse_flag: ReverseFlags, target_id=None):
        return Sphero.__encode(command_id=48, data=[speed, *to_bytes(heading, 2), roll_mode, reverse_flag],
                               target_id=target_id)

    @staticmethod
    def set_raw_motors(left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed, target_id=None):
        return Sphero.__encode(command_id=51, data=[left_mode, left_speed, right_mode, right_speed],
                               target_id=target_id)
