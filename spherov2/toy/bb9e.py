from collections import OrderedDict
from enum import IntEnum
from functools import partialmethod, lru_cache

from spherov2.commands.animatronic import Animatronic
from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.connection import Connection
from spherov2.commands.drive import Drive
from spherov2.commands.factory_test import FactoryTest
from spherov2.commands.firmware import Firmware
from spherov2.commands.io import IO
from spherov2.commands.power import Power
from spherov2.commands.sensor import Sensor
from spherov2.commands.system_info import SystemInfo
from spherov2.controls.v2 import DriveControl, LedControl, SensorControl, FirmwareUpdateControl, StatsControl
from spherov2.toy import ToyV2, ToySensor, Toy
from spherov2.types import ToyType


class BB9E(ToyV2):
    toy_type = ToyType('BB-9E', 'GB-', 'GB', .12)
    _handshake = [('00020005-574f-4f20-5370-6865726f2121', bytearray(b'usetheforce...band'))]

    class LEDs(IntEnum):
        BODY_RED = 0
        BODY_GREEN = 1
        BODY_BLUE = 2
        AIMING = 3
        HEAD = 4

    class Animations(IntEnum):
        EMOTE_ALARM = 0
        EMOTE_NO = 1
        EMOTE_SCAN_SWEEP = 2
        EMOTE_SCARED = 3
        EMOTE_YES = 4
        EMOTE_AFFIRMATIVE = 5
        EMOTE_AGITATED = 6
        EMOTE_ANGRY = 7
        EMOTE_CONTENT = 8
        EMOTE_EXCITED = 9
        EMOTE_FIERY = 10
        EMOTE_GREETINGS = 11
        EMOTE_NERVOUS = 12
        EMOTE_SLEEP = 14
        EMOTE_SURPRISED = 15
        EMOTE_UNDERSTOOD = 16
        HIT = 17
        WWM_ANGRY = 18
        WWM_ANXIOUS = 19
        WWM_BOW = 20
        WWM_CURIOUS = 22
        WWM_DOUBLE_TAKE = 23
        WWM_EXCITED = 24
        WWM_FIERY = 25
        WWM_HAPPY = 26
        WWM_JITTERY = 27
        WWM_LAUGH = 28
        WWM_LONG_SHAKE = 29
        WWM_NO = 30
        WWM_OMINOUS = 31
        WWM_RELIEVED = 32
        WWM_SAD = 33
        WWM_SCARED = 34
        WWM_SHAKE = 35
        WWM_SURPRISED = 36
        WWM_TAUNTING = 37
        WWM_WHISPER = 38
        WWM_YELLING = 39
        WWM_YOOHOO = 40
        WWM_FRUSTRATED = 41
        IDLE_1 = 42
        IDLE_2 = 43
        IDLE_3 = 44
        EYE_1 = 45
        EYE_2 = 46
        EYE_3 = 47
        EYE_4 = 48

    sensors = OrderedDict(
        quaternion=OrderedDict(
            x=ToySensor(0x2000000, -1., 1.),
            y=ToySensor(0x1000000, -1., 1.),
            z=ToySensor(0x800000, -1., 1.),
            w=ToySensor(0x400000, -1., 1.)
        ),
        attitude=OrderedDict(
            pitch=ToySensor(0x40000, -179., 180.),
            roll=ToySensor(0x20000, -179., 180.),
            yaw=ToySensor(0x10000, -179., 180.)
        ),
        accelerometer=OrderedDict(
            x=ToySensor(0x8000, -8.19, 8.19),
            y=ToySensor(0x4000, -8.19, 8.19),
            z=ToySensor(0x2000, -8.19, 8.19)
        ),
        accel_one=OrderedDict(accel_one=ToySensor(0x200, 0., 8000.)),
        locator=OrderedDict(
            x=ToySensor(0x40, -32768., 32767., lambda x: x * 100.),
            y=ToySensor(0x20, -32768., 32767., lambda x: x * 100.),
        ),
        velocity=OrderedDict(
            x=ToySensor(0x10, -32768., 32767., lambda x: x * 100.),
            y=ToySensor(0x8, -32768., 32767., lambda x: x * 100.),
        ),
        speed=OrderedDict(speed=ToySensor(0x4, 0., 32767.)),
        core_time=OrderedDict(core_time=ToySensor(0x2, 0., 0.))
    )

    extended_sensors = OrderedDict(
        gyroscope=OrderedDict(
            x=ToySensor(0x2000000, -20000., 20000.),
            y=ToySensor(0x1000000, -20000., 20000.),
            z=ToySensor(0x800000, -20000., 20000.)
        )
    )

    # Animatronic
    play_animation = Animatronic.play_animation
    stop_animation = Animatronic.stop_animation
    enable_idle_animations = Animatronic.enable_idle_animations
    enable_trophy_mode = Animatronic.enable_trophy_mode
    get_trophy_mode_enabled = Animatronic.get_trophy_mode_enabled

    # APIAndShell
    ping = ApiAndShell.ping
    get_api_protocol_version = ApiAndShell.get_api_protocol_version
    send_command_to_shell = ApiAndShell.send_command_to_shell
    add_send_string_to_console_listener = partialmethod(Toy._add_listener, ApiAndShell.send_string_to_console)
    remove_send_string_to_console_listener = partialmethod(Toy._remove_listener, ApiAndShell.send_string_to_console)

    # Connection
    set_bluetooth_name = Connection.set_bluetooth_name
    get_bluetooth_name = Connection.get_bluetooth_name

    # Drive
    set_raw_motors = Drive.set_raw_motors
    reset_yaw = Drive.reset_yaw
    drive_with_heading = Drive.drive_with_heading
    set_stabilization = Drive.set_stabilization

    # FactoryTest
    get_factory_mode_challenge = FactoryTest.get_factory_mode_challenge
    enter_factory_mode = FactoryTest.enter_factory_mode
    exit_factory_mode = FactoryTest.exit_factory_mode
    get_chassis_id = FactoryTest.get_chassis_id

    # Firmware
    get_pending_update_flags = Firmware.get_pending_update_flags

    # IO
    play_audio_file = IO.play_audio_file
    set_all_leds_with_16_bit_mask = IO.set_all_leds_with_16_bit_mask
    start_idle_led_animation = IO.start_idle_led_animation

    # Sensor
    set_sensor_streaming_mask = Sensor.set_sensor_streaming_mask
    get_sensor_streaming_mask = Sensor.get_sensor_streaming_mask
    add_sensor_streaming_data_notify_listener = partialmethod(Toy._add_listener, Sensor.sensor_streaming_data_notify)
    remove_sensor_streaming_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Sensor.sensor_streaming_data_notify)
    set_extended_sensor_streaming_mask = Sensor.set_extended_sensor_streaming_mask
    get_extended_sensor_streaming_mask = Sensor.get_extended_sensor_streaming_mask
    enable_gyro_max_notify = Sensor.enable_gyro_max_notify
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_max_notify)
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener, Sensor.gyro_max_notify)
    configure_collision_detection = Sensor.configure_collision_detection
    add_collision_detected_notify_listener = partialmethod(Toy._add_listener, Sensor.collision_detected_notify)
    remove_collision_detected_notify_listener = partialmethod(Toy._remove_listener, Sensor.collision_detected_notify)
    reset_locator_x_and_y = Sensor.reset_locator_x_and_y
    set_locator_flags = Sensor.set_locator_flags
    set_accelerometer_activity_threshold = Sensor.set_accelerometer_activity_threshold
    enable_accelerometer_activity_notify = Sensor.enable_accelerometer_activity_notify
    add_accelerometer_activity_notify_listener = partialmethod(Toy._add_listener, Sensor.accelerometer_activity_notify)
    remove_accelerometer_activity_notify_listener = partialmethod(Toy._remove_listener,
                                                                  Sensor.accelerometer_activity_notify)
    set_gyro_activity_threshold = Sensor.set_gyro_activity_threshold
    enable_gyro_activity_notify = Sensor.enable_gyro_activity_notify
    add_gyro_activity_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_activity_notify)
    remove_gyro_activity_notify_listener = partialmethod(Toy._remove_listener, Sensor.gyro_activity_notify)

    # Power
    enter_deep_sleep = Power.enter_deep_sleep
    sleep = Power.sleep
    get_battery_voltage = Power.get_battery_voltage
    get_battery_state = Power.get_battery_state
    enable_battery_state_changed_notify = Power.enable_battery_state_changed_notify
    add_battery_state_changed_notify_listener = partialmethod(Toy._add_listener, Power.battery_state_changed_notify)
    remove_battery_state_changed_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Power.battery_state_changed_notify)
    wake = Power.wake
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener, Power.will_sleep_notify)
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener, Power.will_sleep_notify)
    add_did_sleep_notify_listener = partialmethod(Toy._add_listener, Power.did_sleep_notify)
    remove_did_sleep_notify_listener = partialmethod(Toy._remove_listener, Power.did_sleep_notify)
    enable_battery_voltage_state_change_notify = Power.enable_battery_voltage_state_change_notify
    add_battery_voltage_state_change_notify_listener = partialmethod(Toy._add_listener,
                                                                     Power.battery_voltage_state_change_notify)
    remove_battery_voltage_state_change_notify_listener = partialmethod(Toy._remove_listener,
                                                                        Power.battery_voltage_state_change_notify)

    # SystemInfo
    get_main_app_version = SystemInfo.get_main_app_version
    get_bootloader_version = SystemInfo.get_bootloader_version
    get_board_revision = SystemInfo.get_board_revision
    get_mac_address = SystemInfo.get_mac_address
    get_stats_id = SystemInfo.get_stats_id
    get_secondary_main_app_version = SystemInfo.get_secondary_main_app_version
    add_secondary_main_app_version_notify_listener = partialmethod(Toy._add_listener,
                                                                   SystemInfo.secondary_main_app_version_notify)
    remove_secondary_main_app_version_notify_listener = partialmethod(Toy._remove_listener,
                                                                      SystemInfo.secondary_main_app_version_notify)
    get_processor_name = SystemInfo.get_processor_name
    get_secondary_mcu_bootloader_version = SystemInfo.get_secondary_mcu_bootloader_version
    add_get_secondary_mcu_bootloader_version_notify_listener = partialmethod(Toy._add_listener,
                                                                             SystemInfo.secondary_mcu_bootloader_version_notify)
    remove_get_secondary_mcu_bootloader_version_notify_listener = partialmethod(Toy._remove_listener,
                                                                                SystemInfo.secondary_mcu_bootloader_version_notify)
    get_three_character_sku = SystemInfo.get_three_character_sku

    # Controls
    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    @property
    @lru_cache(None)
    def firmware_update_control(self):
        return FirmwareUpdateControl(self)

    @property
    @lru_cache(None)
    def multi_led_control(self):
        return LedControl(self)

    @property
    @lru_cache(None)
    def sensor_control(self):
        return SensorControl(self)

    @property
    @lru_cache(None)
    def stats_control(self):
        return StatsControl(self)
