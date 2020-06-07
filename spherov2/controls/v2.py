from enum import IntEnum
from typing import Dict

from spherov2.command.driving import DriveFlags
from spherov2.controls.enums import RawMotorModes
from spherov2.command.driving import RawMotorModes as DriveRawMotorModes
from spherov2.toy.core import Toy


class DriveControl:
    def __init__(self, toy: Toy):
        self.__toy = toy
        self.__is_boosting = False

    def roll_start(self, heading, speed):
        flag = DriveFlags.FORWARD
        if speed < 0:
            flag = DriveFlags.BACKWARD
            heading += 180
        if self.__is_boosting:
            flag |= DriveFlags.TURBO
        speed = min(255, abs(speed))
        heading %= 360
        self.__toy.drive_with_heading(speed, heading, flag)

    def roll_stop(self, heading):
        self.roll_start(heading, 0)

    def set_stabilization(self, stabilize):
        self.__toy.set_stabilization(stabilize)

    def set_raw_motors(self, left_mode, left_speed, right_mode, right_speed):
        if left_mode == RawMotorModes.FORWARD:
            left_drive_mode = DriveRawMotorModes.FORWARD
        elif left_mode == RawMotorModes.REVERSE:
            left_drive_mode = DriveRawMotorModes.REVERSE
        else:
            left_drive_mode = DriveRawMotorModes.OFF

        if right_mode == RawMotorModes.FORWARD:
            right_drive_mode = DriveRawMotorModes.FORWARD
        elif right_mode == RawMotorModes.REVERSE:
            right_drive_mode = DriveRawMotorModes.REVERSE
        else:
            right_drive_mode = DriveRawMotorModes.OFF

        self.__toy.set_raw_motors(left_drive_mode, left_speed, right_drive_mode, right_speed)

    def reset_header(self):
        self.__toy.reset_yaw()


class LedControl:
    def __init__(self, toy: Toy):
        self.__toy = toy

    def set_leds(self, mapping: Dict[IntEnum, int]):
        mask = 0
        led_values = []
        for e in self.__toy.LEDs:
            if e in mapping:
                mask |= 1 << e
                led_values.append(mapping[e])
        if mask:
            if hasattr(self.__toy, 'set_all_leds_with_32_bit_mask'):
                self.__toy.set_all_leds_with_32_bit_mask(mask, led_values)
            elif hasattr(self.__toy, 'set_all_leds_with_16_bit_mask'):
                self.__toy.set_all_leds_with_16_bit_mask(mask, led_values)
            elif hasattr(self.__toy, 'set_all_leds_with_8_bit_mask'):
                self.__toy.set_all_leds_with_8_bit_mask(mask, led_values)
