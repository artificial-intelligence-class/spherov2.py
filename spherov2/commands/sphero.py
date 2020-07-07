from enum import IntEnum

from spherov2.commands import Commands
from spherov2.helper import to_bytes


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


class Sphero(Commands):
    _did = 2

    @staticmethod
    def set_heading(toy, heading: int, tid=None):
        toy._execute(Sphero._encode(toy, 1, tid, to_bytes(heading, 2)))

    @staticmethod
    def set_stabilization(toy, stabilize: bool, tid=None):
        toy._execute(Sphero._encode(toy, 2, tid, [int(stabilize)]))

    @staticmethod
    def set_data_streaming(toy, interval, num_samples_per_packet, mask, count, extended_mask, tid=None):
        toy._execute(Sphero._encode(
            toy, 17, tid,
            [*to_bytes(interval, 2), *to_bytes(num_samples_per_packet, 2), *to_bytes(mask, 4), count & 0xff,
             *to_bytes(extended_mask, 4)]))

    @staticmethod
    def configure_collision_detection(toy, collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time, tid=None):
        toy._execute(Sphero._encode(
            toy, 18, tid, [collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time]))

    @staticmethod
    def configure_locator(toy, flags, x, y, yaw_tare, tid=None):
        toy._execute(Sphero._encode(toy, 19, tid, [flags, *to_bytes(x, 2), *to_bytes(y, 2), *to_bytes(yaw_tare, 2)]))

    @staticmethod
    def set_main_led(toy, r, g, b, tid=None):
        toy._execute(Sphero._encode(toy, 32, tid, [r, g, b]))

    @staticmethod
    def set_back_led_brightness(toy, brightness, tid=None):
        toy._execute(Sphero._encode(toy, 33, tid, data=[brightness]))

    @staticmethod
    def roll(toy, speed, heading, roll_mode: RollModes, reverse_flag: ReverseFlags, tid=None):
        toy._execute(Sphero._encode(toy, 48, tid, [speed, *to_bytes(heading, 2), roll_mode, reverse_flag]))

    @staticmethod
    def set_raw_motors(toy, left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed, tid=None):
        toy._execute(Sphero._encode(toy, 51, tid, [left_mode, left_speed, right_mode, right_speed]))
