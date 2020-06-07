import struct
from enum import IntEnum
from functools import lru_cache

from spherov2.command.animatronic import Animatronic, R2LegActions
from spherov2.command.api_and_shell import APIAndShell
from spherov2.command.driving import Driving, DriveFlags, StabilizationIndexes, RawMotorModes
from spherov2.command.firmware import Firmware, PendingUpdateFlags
from spherov2.command.io import IO
from spherov2.command.power import Power, BatteryStates
from spherov2.command.sensor import Sensor, CollisionDetectionMethods
from spherov2.command.system_info import SystemInfo
from spherov2.controls.v2 import DriveControl, LedControl
from spherov2.toy.core import Toy, ToySensor
from spherov2.helper import to_int
from spherov2.toy.types import ToyType


class R2D2(Toy):
    toy_type = ToyType('R2-D2', 'D2-', 'D2', .12)

    class LEDs(IntEnum):
        FRONT_RED = 0
        FRONT_GREEN = 1
        FRONT_BLUE = 2
        LOGIC_DISPLAYS = 3
        BACK_RED = 4
        BACK_GREEN = 5
        BACK_BLUE = 6
        HOLO_PROJECTOR = 7

    class Animations(IntEnum):
        CHARGER_1 = 0
        CHARGER_2 = 1
        CHARGER_3 = 2
        CHARGER_4 = 3
        CHARGER_5 = 4
        CHARGER_6 = 5
        CHARGER_7 = 6
        EMOTE_ALARM = 7
        EMOTE_ANGRY = 8
        EMOTE_ATTENTION = 9
        EMOTE_FRUSTRATED = 10
        EMOTE_DRIVE = 11
        EMOTE_EXCITED = 12
        EMOTE_SEARCH = 13
        EMOTE_SHORT_CIRCUIT = 14
        EMOTE_LAUGH = 15
        EMOTE_NO = 16
        EMOTE_RETREAT = 17
        EMOTE_FIERY = 18
        EMOTE_UNDERSTOOD = 19
        EMOTE_YES = 21
        EMOTE_SCAN = 22
        EMOTE_SURPRISED = 24
        IDLE_1 = 25
        IDLE_2 = 26
        IDLE_3 = 27
        WWM_ANGRY = 31
        WWM_ANXIOUS = 32
        WWM_BOW = 33
        WWM_CONCERN = 34
        WWM_CURIOUS = 35
        WWM_DOUBLE_TAKE = 36
        WWM_EXCITED = 37
        WWM_FIERY = 38
        WMM_FRUSTRATED = 39
        WWM_HAPPY = 40
        WWM_JITTERY = 41
        WWM_LAUGH = 42
        WWM_LONG_SHAKE = 43
        WWM_NO = 44
        WWM_OMINOUS = 45
        WWM_RELIEVED = 46
        WWM_SAD = 47
        WWM_SCARED = 48
        WWM_SHAKE = 49
        WWM_SURPRISED = 50
        WWM_TAUNTING = 51
        WWM_WHISPER = 52
        WWM_YELLING = 53
        WWM_YOOHOO = 54
        MOTOR = 55

    sensors = {
        'quaternion': {
            'x': ToySensor(0x2000000, -1., 1.),
            'y': ToySensor(0x1000000, -1., 1.),
            'z': ToySensor(0x800000, -1., 1.),
            'w': ToySensor(0x400000, -1., 1.)
        },
        'attitude': {
            'pitch': ToySensor(0x40000, -179., 180.),
            'roll': ToySensor(0x20000, -179., 180.),
            'yaw': ToySensor(0x10000, -179., 180.)
        },
        'accelerometer': {
            'x': ToySensor(0x8000, -8.19, 8.19),
            'y': ToySensor(0x4000, -8.19, 8.19),
            'z': ToySensor(0x2000, -8.19, 8.19)
        },
        'accel_one': {'accel_one': ToySensor(0x200, 0., 8000.)},
        'locator': {
            'x': ToySensor(0x40, -32768., 32767., '@var * 100.0'),
            'y': ToySensor(0x20, -32768., 32767., '@var * 100.0'),
        },
        'velocity': {
            'x': ToySensor(0x10, -32768., 32767., '@var * 100.0'),
            'y': ToySensor(0x8, -32768., 32767., '@var * 100.0'),
        },
        'speed': {'speed': ToySensor(0x4, 0., 32767.)},
        'core_time': {'core_time': ToySensor(0x2, 0., 0.)}
    }

    extended_sensors = {
        'r2_head_angle': {'r2_head_angle': ToySensor(0x4000000, -162., 182.)},
        'gyroscope': {
            'x': ToySensor(0x2000000, -20000., 20000.),
            'y': ToySensor(0x1000000, -20000., 20000.),
            'z': ToySensor(0x800000, -20000., 20000.)
        }
    }

    def ping(self, data):
        return self._execute(APIAndShell.ping(data)).data

    def drive_with_heading(self, speed, heading, drive_flags=DriveFlags.FORWARD):
        self._execute(Driving.drive_with_heading(speed, heading, drive_flags))

    def set_raw_motors(self, left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed):
        self._execute(Driving.set_raw_motors(left_mode, left_speed, right_mode, right_speed))

    def reset_yaw(self):
        self._execute(Driving.reset_yaw())

    def set_stabilization(self, stabilization_index: StabilizationIndexes):
        self._execute(Driving.set_stabilization(stabilization_index))

    def set_audio_volume(self, volume):
        self._execute(IO.set_audio_volume(volume))

    def set_all_leds_with_16_bit_mask(self, mask, values):
        self._execute(IO.set_all_leds_with_16_bit_mask(mask, values))

    def start_idle_led_animation(self):
        self._execute(IO.start_idle_led_animation())

    def play_animation(self, animation: Animations, wait=False):
        self._execute(Animatronic.play_animation(animation))
        if wait:
            self._wait_packet(Animatronic.play_animation_complete_notify)

    def set_head_position(self, head_position: float):
        self._execute(Animatronic.set_head_position(head_position))

    def perform_leg_action(self, leg_action: R2LegActions):
        self._execute(Animatronic.perform_leg_action(leg_action))

    def set_leg_position(self, leg_position: float):
        self._execute(Animatronic.set_leg_position(leg_position))

    def get_leg_position(self):
        return struct.unpack('>f', bytearray(self._execute(Animatronic.get_leg_position()).data))[0]

    def stop_animation(self):
        self._execute(Animatronic.stop_animation())

    def wake(self):
        self._execute(Power.wake())

    def sleep(self):
        self._execute(Power.sleep())

    def enable_battery_voltage_state_change_notify(self, callback):  # TODO
        self._execute(Power.enable_battery_voltage_state_change_notify())

    def get_battery_voltage(self):
        return to_int(self._execute(Power.get_battery_voltage()).data) / 100

    def get_battery_state(self):
        return BatteryStates(self._execute(Power.get_battery_state()).data[0])

    def get_main_app_version(self):
        data = self._execute(SystemInfo.get_main_app_version()).data
        return to_int(data[:2]), to_int(data[2:4]), to_int(data[4:])

    def get_secondary_main_app_version(self):
        self._execute(SystemInfo.get_secondary_main_app_version())
        data = self._wait_packet(SystemInfo.secondary_main_app_version_notify).data
        return to_int(data[:2]), to_int(data[2:4]), to_int(data[4:])

    def get_three_character_sku(self):
        return bytearray(self._execute(SystemInfo.get_three_character_sku()).data)

    def get_stats_id(self):
        return self._execute(SystemInfo.get_stats_id()).data

    def get_mac_address(self):
        return bytearray(self._execute(SystemInfo.get_mac_address()).data)

    def get_pending_update_flags(self):
        return PendingUpdateFlags(to_int(self._execute(Firmware.get_pending_update_flags()).data))

    def enable_gyro_max_notify(self, callback):  # TODO
        self._execute(Sensor.enable_gyro_max_notify())

    def set_locator_flags(self, locator_flags: bool):
        self._execute(Sensor.set_locator_flags(locator_flags))

    def set_sensor_streaming_mask(self, interval, count, sensor_masks):
        self._execute(Sensor.set_sensor_streaming_mask(interval, count, sensor_masks))

    def set_extended_sensor_streaming_mask(self, sensor_masks):
        self._execute(Sensor.set_extended_sensor_streaming_mask(sensor_masks))

    def reset_locator_x_and_y(self):
        self._execute(Sensor.reset_locator_x_and_y())

    def configure_collision_detection(self, collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time):
        self._execute(Sensor.configure_collision_detection(
            collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time
        ))

    @property
    @lru_cache
    def drive_control(self) -> DriveControl:
        return DriveControl(self)

    @property
    @lru_cache
    def multi_led_control(self) -> LedControl:
        return LedControl(self)
