import threading
from enum import IntEnum
from typing import Dict, List, Callable

from spherov2.commands.drive import DriveFlags
from spherov2.commands.drive import RawMotorModes as DriveRawMotorModes
from spherov2.controls.enums import RawMotorModes
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


class SensorControl:
    def __init__(self, toy: Toy):
        self.__toy = toy
        toy.add_sensor_streaming_data_notify_listener(self.__process_sensor_stream_data)

        self.__count = 0
        self.__interval = 250
        self.__enabled = {}
        self.__enabled_extended = {}
        self.__listeners = set()

    def __process_sensor_stream_data(self, sensor_data: List[float]):
        data = {}

        def __new_data():
            n = {}
            for name, component in components.items():
                d = sensor_data.pop(0)
                if component.modifier:
                    d = component.modifier(d)
                n[name] = d
            data[sensor] = n

        for sensor, components in self.__toy.sensors.items():
            if sensor in self.__enabled:
                __new_data()
        for sensor, components in self.__toy.extended_sensors.items():
            if sensor in self.__enabled_extended:
                __new_data()

        for f in self.__listeners:
            threading.Thread(target=f, args=(data,)).start()

    def add_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.add(listener)

    def remove_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.remove(listener)

    def set_count(self, count: int):
        if count > 0:
            self.__count = count
            self.update()

    def set_interval(self, interval: int):
        if interval >= 0:
            self.__interval = interval
            self.update()

    def update(self):
        sensors_mask = extended_sensors_mask = 0
        for sensor in self.__enabled.values():
            for component in sensor.values():
                sensors_mask |= component.bit
        for sensor in self.__enabled_extended.values():
            for component in sensor.values():
                extended_sensors_mask |= component.bit
        self.__toy.set_sensor_streaming_mask(0, self.__count, sensors_mask)
        self.__toy.set_extended_sensor_streaming_mask(extended_sensors_mask)
        self.__toy.set_sensor_streaming_mask(self.__interval, self.__count, sensors_mask)

    def enable(self, *sensors):
        for sensor in sensors:
            if sensor in self.__toy.sensors:
                self.__enabled[sensor] = self.__toy.sensors[sensor]
            elif sensor in self.__toy.extended_sensors:
                self.__enabled_extended[sensor] = self.__toy.extended_sensors[sensor]
        self.update()

    def disable(self, *sensors):
        for sensor in sensors:
            self.__enabled.pop(sensor, None)
            self.__enabled_extended.pop(sensor, None)
        self.update()

    def disable_all(self):
        self.__enabled.clear()
        self.__enabled_extended.clear()
        self.update()
