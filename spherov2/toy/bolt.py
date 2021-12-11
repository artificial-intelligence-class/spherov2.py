from collections import OrderedDict
from enum import IntEnum
from functools import partialmethod, lru_cache

from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.connection import Connection
from spherov2.commands.drive import Drive
from spherov2.commands.firmware import Firmware
from spherov2.commands.io import IO
from spherov2.commands.power import Power
from spherov2.commands.sensor import Sensor
from spherov2.commands.system_info import SystemInfo
from spherov2.controls.v2 import AnimationControl, DriveControl, LedControl, SensorControl, StatsControl, Processors
from spherov2.toy import ToyV2, Toy, ToySensor
from spherov2.types import ToyType


class BOLT(ToyV2):
    toy_type = ToyType('Sphero BOLT', 'SB-', 'SB', .075)
    _handshake = [('00020005-574f-4f20-5370-6865726f2121', bytearray(b'usetheforce...band'))] #TODO: find correct info here

    class LEDs(IntEnum):
        FRONT_RED = 0
        FRONT_GREEN = 1
        FRONT_BLUE = 2
        BACK_RED = 3
        BACK_GREEN = 4
        BACK_BLUE = 5

    # Sensors Available:
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
        ),
        ambient_light=OrderedDict(
            ambient_light=ToySensor(0x40000, 120000., 120000.))
    )

    # Bolt Supported calls
    # API and Shell:
    get_api_protocol_version = ApiAndShell.get_api_protocol_version  # GetApiProtocolVersionCommand
    get_supported_cids = ApiAndShell.get_supported_cids  # GetSupportedCidsCommand
    get_supported_dids = ApiAndShell.get_supported_dids  # GetSupportedDidsCommand
    ping = ApiAndShell.ping  # PingCommand
    send_command_to_shell = ApiAndShell.send_command_to_shell  # SendCommandToShellCommand
    add_send_string_to_console_listener = partialmethod(Toy._add_listener,
                                                        ApiAndShell.send_string_to_console)  # SendStringToConsoleCommand
    remove_send_string_to_console_listener = partialmethod(Toy._remove_listener,
                                                           ApiAndShell.send_string_to_console)  # SendStringToConsoleCommand

    # Connection
    get_bluetooth_advertising_name = Connection.get_bluetooth_advertising_name  # GetBluetoothAdvertisingNameCommand
    get_bluetooth_name = Connection.get_bluetooth_name  # GetBluetoothNameCommand
    set_bluetooth_name = Connection.set_bluetooth_name  # SetBluetoothNameCommand

    #Drive - Driving done on the Secondary Processor
    drive_with_heading = partialmethod(Drive.drive_with_heading,
                                                      proc=Processors.SECONDARY) #DriveWithHeadingCommand
    reset_yaw = partialmethod(Drive.reset_yaw,
                                                      proc=Processors.SECONDARY) #ResetYawCommand
    set_pitch_torque_modification_value = partialmethod(Drive.set_pitch_torque_modification_value,
                                                      proc=Processors.SECONDARY) #SetPitchTorqueModificationValueCommand
    set_raw_motors = partialmethod(Drive.set_raw_motors,
                                                      proc=Processors.SECONDARY) #SetRawMotorsCommand
    set_stabilization = partialmethod(Drive.set_stabilization,
                                                      proc=Processors.SECONDARY) #SetStabilizationCommand

    # Firmware
    get_pending_update_flags = Firmware.get_pending_update_flags  # GetPendingUpdateFlagsCommand

    # IO - most LED/Matrix stuff is done on Secondary Processor, if issues check that
    assign_compressed_frame_player_frames_to_animation = partialmethod(
        IO.assign_compressed_frame_player_frames_to_animation,
        proc=Processors.SECONDARY)  # AssignCompressedFramePlayerFramesToAnimationCommand
    add_compressed_frame_player_animation_complete_notify_listener = partialmethod(
        Toy._add_listener,
        IO.compressed_frame_player_animation_complete_notify)  # CompressedFramePlayerAnimationCompleteNotifyCommand
    remove_compressed_frame_player_animation_complete_notify_listener = partialmethod(
        Toy._remove_listener,
        IO.compressed_frame_player_animation_complete_notify)  # CompressedFramePlayerAnimationCompleteNotifyCommand
    delete_all_compressed_frame_player_animations_and_frames = partialmethod(
        IO.delete_all_compressed_frame_player_animations_and_frames,
        proc=Processors.SECONDARY)  # DeleteAllCompressedFramePlayerAnimationsAndFramesCommand
    draw_compressed_frame_player_fill = partialmethod(IO.draw_compressed_frame_player_fill,
                                                      proc=Processors.SECONDARY)  # DrawCompressedFramePlayerFillCommand
    draw_compressed_frame_player_line = partialmethod(IO.draw_compressed_frame_player_line,
                                                      proc=Processors.SECONDARY)  # DrawCompressedFramePlayerLineCommand
    get_compressed_frame_player_list_of_frames = partialmethod(IO.get_compressed_frame_player_list_of_frames,
                                                               proc=Processors.SECONDARY)  # GetCompressedFramePlayerListOfFramesCommand
    override_compressed_frame_player_animation_global_settings = partialmethod(
        IO.override_compressed_frame_player_animation_global_settings,
        proc=Processors.SECONDARY)  # OverrideCompressedFramePlayerAnimationGlobalSettingsCommand
    pause_compressed_frame_player_animation = partialmethod(IO.pause_compressed_frame_player_animation,
                                                            proc=Processors.SECONDARY)  # PauseCompressedFramePlayerAnimationCommand
    play_compressed_frame_player_animation = partialmethod(IO.play_compressed_frame_player_animation,
                                                           proc=Processors.SECONDARY)  # PlayCompressedFramePlayerAnimationCommand
    play_compressed_frame_player_animation_with_loop_option = partialmethod(
        IO.play_compressed_frame_player_animation_with_loop_option,
        proc=Processors.SECONDARY)  # PlayCompressedFramePlayerAnimationWithLoopOptionCommand
    play_compressed_frame_player_frame = partialmethod(IO.play_compressed_frame_player_frame,
                                                       proc=Processors.SECONDARY)  # PlayCompressedFramePlayerFrameCommand
    reset_compressed_frame_player_animation = partialmethod(IO.reset_compressed_frame_player_animation,
                                                            proc=Processors.SECONDARY)  # ResetCompressedFramePlayerAnimationCommand
    resume_compressed_frame_player_animation = partialmethod(IO.resume_compressed_frame_player_animation,
                                                             proc=Processors.SECONDARY)  # ResumeCompressedFramePlayerAnimationCommand
    save_compressed_frame_player64_bit_frame = partialmethod(IO.save_compressed_frame_player64_bit_frame,
                                                             proc=Processors.SECONDARY)  # SaveCompressedFramePlayer64BitFrameCommand
    save_compressed_frame_player_animation = partialmethod(IO.save_compressed_frame_player_animation,
                                                           proc=Processors.SECONDARY)  # SaveCompressedFramePlayerAnimationCommand
    save_compressed_frame_player_animation_without_frames = partialmethod(
        IO.save_compressed_frame_player_animation_without_frames,
        proc=Processors.SECONDARY)  # SaveCompressedFramePlayerAnimationWithoutFramesCommand
    set_all_leds_with_8_bit_mask = partialmethod(IO.set_all_leds_with_8_bit_mask,
                                                 proc=Processors.PRIMARY)  # SetAllLedsWith8BitMaskCommand
    set_compressed_frame_player = partialmethod(IO.set_compressed_frame_player,
                                                proc=Processors.SECONDARY)  # SetCompressedFramePlayerCommand
    set_compressed_frame_player_frame_rotation = partialmethod(IO.set_compressed_frame_player_frame_rotation,
                                                               proc=Processors.SECONDARY)  # SetCompressedFramePlayerFrameRotationCommand
    set_compressed_frame_player_one_color = partialmethod(IO.set_compressed_frame_player_one_color,
                                                          proc=Processors.SECONDARY)  # SetCompressedFramePlayerOneColorCommand
    set_compressed_frame_player_pixel = partialmethod(IO.set_compressed_frame_player_pixel,
                                                      proc=Processors.SECONDARY)  # SetCompressedFramePlayerPixelCommand
    set_compressed_frame_player_single_character = partialmethod(IO.set_compressed_frame_player_single_character,
                                                                 proc=Processors.SECONDARY)  # SetCompressedFramePlayerSingleCharacterCommand
    set_compressed_frame_player_text_scrolling = partialmethod(IO.set_compressed_frame_player_text_scrolling,
                                                               proc=Processors.SECONDARY)  # SetCompressedFramePlayerTextScrollingCommand
    add_compressed_frame_player_animation_complete_notify = partialmethod(
        Toy._add_listener,
        IO.set_compressed_frame_player_text_scrolling_notify)  # SetCompressedFramePlayerTextScrollingNotifyCommand
    remove_compressed_frame_player_animation_complete_notify_listener = partialmethod(
        Toy._remove_listener,
        IO.set_compressed_frame_player_text_scrolling_notify)  # SetCompressedFramePlayerTextScrollingNotifyCommand
    set_led = partialmethod(IO.set_led, proc=Processors.SECONDARY)  # SetLedCommand

    # Testing
    release_led_requests = partialmethod(IO.release_led_requests, proc=Processors.PRIMARY)

    # Power
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                   Power.charger_state_changed_notify)  # ChargerStateChangedNotifyCommand
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                      Power.charger_state_changed_notify)  # ChargerStateChangedNotifyCommand
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                   Power.did_sleep_notify)  # DidSleepNotifyCommand
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                      Power.did_sleep_notify)  # DidSleepNotifyCommand
    enable_battery_voltage_state_change_notify = Power.enable_battery_voltage_state_change_notify  # EnableBatteryVoltageStateChangeNotifyCommand
    enable_charger_state_changed_notify = Power.enable_charger_state_changed_notify  # EnableChargerStateChangedNotifyCommand
    enter_deep_sleep = Power.enter_deep_sleep  # EnterDeepSleepCommand
    get_battery_voltage = Power.get_battery_voltage  # GetBatteryVoltageCommand
    get_battery_voltage_state = Power.get_battery_voltage_state  # GetBatteryVoltageStateCommand
    get_charger_state = Power.get_charger_state  # GetChargerStateCommand
    sleep = Power.sleep  # SleepCommand
    wake = Power.wake  # WakeCommand
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                   Power.will_sleep_notify)  # WillSleepNotifyCommand
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                      Power.will_sleep_notify)  # WillSleepNotifyCommand

    # Sensor
    add_collision_detected_notify_listener = partialmethod(Toy._add_listener,
                                                           Sensor.collision_detected_notify)  # CollisionDetectedNotifyCommand
    remove_collision_detected_notify_listener = partialmethod(Toy._remove_listener,
                                                              Sensor.collision_detected_notify)  # CollisionDetectedNotifyCommand
    configure_collision_detection = Sensor.configure_collision_detection  # ConfigureCollisionDetectionCommand
    enable_gyro_max_notify = partialmethod(Sensor.enable_gyro_max_notify, proc=Processors.SECONDARY)  # EnableGyroMaxNotifyCommand
    get_ambient_light_sensor_value = partialmethod(Sensor.get_ambient_light_sensor_value, proc=Processors.SECONDARY)
    get_bot_to_bot_infrared_readings = Sensor.get_bot_to_bot_infrared_readings  # GetBotToBotInfraredReadingsCommand
    get_sensor_streaming_mask = partialmethod(Sensor.get_sensor_streaming_mask, proc=Processors.SECONDARY)  # GetSensorStreamingMaskCommand
    set_sensor_streaming_mask = partialmethod(Sensor.set_sensor_streaming_mask, proc=Processors.SECONDARY)  # SetSensorStreamingMaskCommand
    get_extended_sensor_streaming_mask = partialmethod(Sensor.get_extended_sensor_streaming_mask, proc=Processors.SECONDARY)  # GetExtendedSensorStreamingMaskCommand
    set_extended_sensor_streaming_mask = partialmethod(Sensor.set_extended_sensor_streaming_mask, proc=Processors.SECONDARY)  # SetExtendedSensorStreamingMaskCommand
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_max_notify)  # GyroMaxNotifyCommand
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener,
                                                    Sensor.gyro_max_notify)  # GyroMaxNotifyCommand
    listen_for_robot_to_robot_infrared_message = Sensor.listen_for_robot_to_robot_infrared_message  # ListenForRobotToRobotInfraredMessageCommand
    magnetometer_calibrate_to_north = Sensor.magnetometer_calibrate_to_north  # MagnetometerCalibrateToNorthCommand
    add_magnetometer_north_yaw_notify_listener = partialmethod(Toy._add_listener,
                                                               Sensor.magnetometer_north_yaw_notify)  # MagnetometerNorthYawNotifyCommand
    remove_magnetometer_north_yaw_notify_listener = partialmethod(Toy._remove_listener,
                                                                  Sensor.magnetometer_north_yaw_notify)  # MagnetometerNorthYawNotifyCommand
    reset_locator_x_and_y = partialmethod(Sensor.reset_locator_x_and_y, proc=Processors.SECONDARY)  # ResetLocationXAndYCommand
    add_robot_to_robot_infrared_message_received_notify_listener = partialmethod(Toy._add_listener,
                                                                                 Sensor.robot_to_robot_infrared_message_received_notify)  ##RobotToRobotInfraredMessageReceivedNotifyCommand
    remove_robot_to_robot_infrared_message_received_notify_listener = partialmethod(Toy._remove_listener,
                                                                                    Sensor.robot_to_robot_infrared_message_received_notify)  # RobotToRobotInfraredMessageReceivedNotifyCommand
    send_robot_to_robot_infrared_message = Sensor.send_robot_to_robot_infrared_message  # SendRobotToRobotInfraredMessageCommand
    add_sensor_streaming_data_notify_listener = partialmethod(Toy._add_listener,
                                                              Sensor.sensor_streaming_data_notify)  # SensorStreamingDataNotifyCommand
    remove_sensor_streaming_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Sensor.sensor_streaming_data_notify)  # SensorStreamingDataNotifyCommand
    set_locator_flags = Sensor.set_locator_flags  # SetLocatorFlagsCommand
    start_robot_to_robot_infrared_broadcasting = Sensor.start_robot_to_robot_infrared_broadcasting  # StartRobotToRobotInfraredBroadcastingCommand
    start_robot_to_robot_infrared_evading = Sensor.start_robot_to_robot_infrared_evading  # StartRobotToRobotInfraredEvadingCommand
    start_robot_to_robot_infrared_following = Sensor.start_robot_to_robot_infrared_following  # StartRobotToRobotInfraredFollowingCommand
    stop_robot_to_robot_infrared_broadcasting = Sensor.stop_robot_to_robot_infrared_broadcasting  # StopRobotToRobotInfraredBroadcastingCommand
    stop_robot_to_robot_infrared_evading = Sensor.stop_robot_to_robot_infrared_evading  # StopRobotToRobotInfraredEvadingCommand
    stop_robot_to_robot_infrared_following = Sensor.stop_robot_to_robot_infrared_following  # StopRobotToRobotInfraredFollowingCommand

    # System Info
    erase_config_block = SystemInfo.erase_config_block  # EraseConfigBlockCommand
    get_board_revision = SystemInfo.get_board_revision  # GetBoardRevisionCommand
    get_boot_reason = SystemInfo.get_boot_reason  # GetBootReasonCommand
    get_bootloader_version = SystemInfo.get_bootloader_version  # GetBootloaderVersionCommand
    get_secondary_mcu_bootloader_version = SystemInfo.get_secondary_mcu_bootloader_version
    get_config_block = SystemInfo.get_config_block  # GetConfigBlockCommand
    get_last_error_info = SystemInfo.get_last_error_info  # GetLastErrorInfoCommand
    get_mac_address = SystemInfo.get_mac_address  # GetMacAddressCommand
    get_main_app_version = SystemInfo.get_main_app_version  # GetMainAppVersionCommand
    get_secondary_main_app_version = SystemInfo.get_secondary_main_app_version
    get_manufacturing_date = SystemInfo.get_manufacturing_date  # GetManufacturingDateCommand
    get_processor_name = SystemInfo.get_processor_name  # GetProcessorNameCommand
    get_sku = SystemInfo.get_sku  # GetSkuCommand
    get_stats_id = SystemInfo.get_stats_id  # GetStatsIdCommand
    get_swd_locking_status = SystemInfo.get_swd_locking_status  # GetSwdLockingStatusCommand
    set_config_block = SystemInfo.set_config_block  # SetConfigBlockCommand
    write_config_block = SystemInfo.write_config_block  # WriteConfigBlockCommand

    # Controls - V2
    @property
    @lru_cache(None)
    def animation_control(self):
        return AnimationControl(self)

    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    @property
    @lru_cache(None)
    def multi_led_control(self):
        return LedControl(self)

    @property
    def sensor_control(self):
        if self._sensor_controller is None: #Make a new SensorControl if necessary (NOT A UTIL CLASS)
            self._sensor_controller = SensorControl(self)
        return self._sensor_controller

    @property
    @lru_cache(None)
    def stats_control(self):
        return StatsControl(self)
