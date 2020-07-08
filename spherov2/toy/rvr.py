from enum import IntEnum
from functools import lru_cache, partialmethod

from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.connection import Connection
from spherov2.commands.drive import Drive
from spherov2.commands.factory_test import FactoryTest
from spherov2.commands.firmware import Firmware
from spherov2.commands.io import IO
from spherov2.commands.power import Power
from spherov2.commands.sensor import Sensor
from spherov2.commands.system_info import SystemInfo
from spherov2.commands.system_mode import SystemMode
from spherov2.controls.v2 import DriveControl, LedControl, StreamingControl, Processors
from spherov2.toy import Toy, ToyV2
from spherov2.types import ToyType


class RVR(ToyV2):
    toy_type = ToyType('Sphero RVR', 'RV-', 'RV', .075)
    _require_target = True

    class LEDs(IntEnum):
        RIGHT_HEADLIGHT_RED = 0
        RIGHT_HEADLIGHT_GREEN = 1
        RIGHT_HEADLIGHT_BLUE = 2
        LEFT_HEADLIGHT_RED = 3
        LEFT_HEADLIGHT_GREEN = 4
        LEFT_HEADLIGHT_BLUE = 5
        LEFT_STATUS_INDICATION_RED = 6
        LEFT_STATUS_INDICATION_GREEN = 7
        LEFT_STATUS_INDICATION_BLUE = 8
        RIGHT_STATUS_INDICATION_RED = 9
        RIGHT_STATUS_INDICATION_GREEN = 10
        RIGHT_STATUS_INDICATION_BLUE = 11
        BATTERY_DOOR_REAR_RED = 12
        BATTERY_DOOR_REAR_GREEN = 13
        BATTERY_DOOR_REAR_BLUE = 14
        BATTERY_DOOR_FRONT_RED = 15
        BATTERY_DOOR_FRONT_GREEN = 16
        BATTERY_DOOR_FRONT_BLUE = 17
        POWER_BUTTON_FRONT_RED = 18
        POWER_BUTTON_FRONT_GREEN = 19
        POWER_BUTTON_FRONT_BLUE = 20
        POWER_BUTTON_REAR_RED = 21
        POWER_BUTTON_REAR_GREEN = 22
        POWER_BUTTON_REAR_BLUE = 23
        LEFT_BRAKELIGHT_RED = 24
        LEFT_BRAKELIGHT_GREEN = 25
        LEFT_BRAKELIGHT_BLUE = 26
        RIGHT_BRAKELIGHT_RED = 27
        RIGHT_BRAKELIGHT_GREEN = 28
        RIGHT_BRAKELIGHT_BLUE = 29
        UNDERCARRIAGE_WHITE = 30

    ping = ApiAndShell.ping
    get_api_protocol_version = ApiAndShell.get_api_protocol_version
    send_command_to_shell = ApiAndShell.send_command_to_shell
    add_send_string_to_console_listener = partialmethod(Toy._add_listener, ApiAndShell.send_string_to_console)
    remove_send_string_to_console_listener = partialmethod(Toy._remove_listener, ApiAndShell.send_string_to_console)
    get_supported_dids = ApiAndShell.get_supported_dids
    get_supported_cids = ApiAndShell.get_supported_cids

    get_main_app_version = SystemInfo.get_main_app_version
    get_bootloader_version = SystemInfo.get_bootloader_version
    get_board_revision = partialmethod(SystemInfo.get_board_revision, proc=Processors.PRIMARY)
    get_mac_address = partialmethod(SystemInfo.get_mac_address, proc=Processors.PRIMARY)
    get_stats_id = partialmethod(SystemInfo.get_stats_id, proc=Processors.PRIMARY)
    get_processor_name = SystemInfo.get_processor_name
    get_boot_reason = partialmethod(SystemInfo.get_boot_reason, proc=Processors.PRIMARY)
    get_last_error_info = partialmethod(SystemInfo.get_last_error_info, proc=Processors.PRIMARY)
    write_config_block = partialmethod(SystemInfo.write_config_block, proc=Processors.PRIMARY)
    get_config_block = partialmethod(SystemInfo.get_config_block, proc=Processors.PRIMARY)
    set_config_block = partialmethod(SystemInfo.set_config_block, proc=Processors.PRIMARY)
    erase_config_block = partialmethod(SystemInfo.erase_config_block, proc=Processors.PRIMARY)
    get_swd_locking_status = SystemInfo.get_swd_locking_status
    get_manufacturing_date = partialmethod(SystemInfo.get_manufacturing_date, proc=Processors.PRIMARY)
    get_sku = partialmethod(SystemInfo.get_sku, proc=Processors.PRIMARY)
    get_core_up_time_in_milliseconds = partialmethod(SystemInfo.get_core_up_time_in_milliseconds,
                                                     proc=Processors.PRIMARY)
    get_event_log_status = SystemInfo.get_event_log_status
    get_event_log_data = SystemInfo.get_event_log_data
    clear_event_log = SystemInfo.clear_event_log
    enable_sos_message_notify = partialmethod(SystemInfo.enable_sos_message_notify, proc=Processors.PRIMARY)
    add_sos_message_notify_listener = partialmethod(Toy._add_listener, SystemInfo.sos_message_notify)
    remove_sos_message_notify_listener = partialmethod(Toy._remove_listener, SystemInfo.sos_message_notify)
    get_sos_message = partialmethod(SystemInfo.get_sos_message, proc=Processors.PRIMARY)
    clear_sos_message = partialmethod(SystemInfo.clear_sos_message, proc=Processors.PRIMARY)

    get_out_of_box_state = partialmethod(SystemMode.get_out_of_box_state, proc=Processors.PRIMARY)
    enable_out_of_box_state = partialmethod(SystemMode.enable_out_of_box_state, proc=Processors.PRIMARY)

    enter_deep_sleep = partialmethod(Power.enter_deep_sleep, proc=Processors.PRIMARY)
    sleep = partialmethod(Power.sleep, proc=Processors.PRIMARY)
    force_battery_refresh = partialmethod(Power.force_battery_refresh, proc=Processors.PRIMARY)
    wake = partialmethod(Power.wake, proc=Processors.PRIMARY)
    get_battery_percentage = partialmethod(Power.get_battery_percentage, proc=Processors.PRIMARY)
    get_battery_voltage_state = partialmethod(Power.get_battery_voltage_state, proc=Processors.PRIMARY)
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener, Power.will_sleep_notify)
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener, Power.will_sleep_notify)
    add_did_sleep_notify_listener = partialmethod(Toy._add_listener, Power.did_sleep_notify)
    remove_did_sleep_notify_listener = partialmethod(Toy._remove_listener, Power.did_sleep_notify)
    enable_battery_voltage_state_change_notify = partialmethod(Power.enable_battery_voltage_state_change_notify,
                                                               proc=Processors.PRIMARY)
    add_battery_voltage_state_change_notify_listener = partialmethod(Toy._add_listener,
                                                                     Power.battery_voltage_state_change_notify)
    remove_battery_voltage_state_change_notify_listener = partialmethod(Toy._remove_listener,
                                                                        Power.battery_voltage_state_change_notify)
    get_battery_voltage_in_volts = partialmethod(Power.get_battery_voltage_in_volts, proc=Processors.PRIMARY)
    get_battery_voltage_state_thresholds = partialmethod(Power.get_battery_voltage_state_thresholds,
                                                         proc=Processors.PRIMARY)
    get_current_sense_amplifier_current = partialmethod(Power.get_current_sense_amplifier_current,
                                                        proc=Processors.PRIMARY)
    get_efuse_fault_status = partialmethod(Power.get_efuse_fault_status, proc=Processors.PRIMARY)
    add_efuse_fault_occurred_notify_listener = partialmethod(Toy._add_listener, Power.efuse_fault_occurred_notify)
    remove_efuse_fault_occurred_notify_listener = partialmethod(Toy._remove_listener, Power.efuse_fault_occurred_notify)
    enable_efuse = partialmethod(Power.enable_efuse, proc=Processors.PRIMARY)

    set_raw_motors = partialmethod(Drive.set_raw_motors, proc=Processors.SECONDARY)
    reset_yaw = partialmethod(Drive.reset_yaw, proc=Processors.SECONDARY)
    drive_with_heading = partialmethod(Drive.drive_with_heading, proc=Processors.SECONDARY)
    set_control_system_type = partialmethod(Drive.set_control_system_type, proc=Processors.SECONDARY)
    set_component_parameters = partialmethod(Drive.set_component_parameters, proc=Processors.SECONDARY)
    get_component_parameters = partialmethod(Drive.get_component_parameters, proc=Processors.SECONDARY)
    set_custom_control_system_timeout = partialmethod(Drive.set_custom_control_system_timeout,
                                                      proc=Processors.SECONDARY)
    enable_motor_stall_notify = partialmethod(Drive.enable_motor_stall_notify, proc=Processors.SECONDARY)
    add_motor_stall_notify_listener = partialmethod(Toy._add_listener, Drive.motor_stall_notify)
    remove_motor_stall_notify_listener = partialmethod(Toy._remove_listener, Drive.motor_stall_notify)
    enable_motor_fault_notify = partialmethod(Drive.enable_motor_fault_notify, proc=Processors.SECONDARY)
    add_motor_fault_notify_listener = partialmethod(Toy._add_listener, Drive.motor_fault_notify)
    remove_motor_fault_notify_listener = partialmethod(Toy._remove_listener, Drive.motor_fault_notify)
    get_motor_fault_state = partialmethod(Drive.get_motor_fault_state, proc=Processors.SECONDARY)

    enable_gyro_max_notify = partialmethod(Sensor.enable_gyro_max_notify, proc=Processors.SECONDARY)
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_max_notify)
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener, Sensor.gyro_max_notify)
    reset_locator_x_and_y = partialmethod(Sensor.reset_locator_x_and_y, proc=Processors.SECONDARY)
    set_locator_flags = partialmethod(Sensor.set_locator_flags, proc=Processors.SECONDARY)
    get_bot_to_bot_infrared_readings = partialmethod(Sensor.get_bot_to_bot_infrared_readings, proc=Processors.SECONDARY)
    get_rgbc_sensor_values = partialmethod(Sensor.get_rgbc_sensor_values, proc=Processors.PRIMARY)
    magnetometer_calibrate_to_north = partialmethod(Sensor.magnetometer_calibrate_to_north, proc=Processors.SECONDARY)
    add_magnetometer_north_yaw_notify_listener = partialmethod(Toy._add_listener, Sensor.magnetometer_north_yaw_notify)
    remove_magnetometer_north_yaw_notify_listener = partialmethod(Toy._remove_listener,
                                                                  Sensor.magnetometer_north_yaw_notify)
    start_robot_to_robot_infrared_broadcasting = partialmethod(Sensor.start_robot_to_robot_infrared_broadcasting,
                                                               proc=Processors.SECONDARY)
    start_robot_to_robot_infrared_following = partialmethod(Sensor.start_robot_to_robot_infrared_following,
                                                            proc=Processors.SECONDARY)
    stop_robot_to_robot_infrared_broadcasting = partialmethod(Sensor.stop_robot_to_robot_infrared_broadcasting,
                                                              proc=Processors.SECONDARY)
    add_robot_to_robot_infrared_message_received_notify_listener = partialmethod(
        Toy._add_listener, Sensor.robot_to_robot_infrared_message_received_notify)
    remove_robot_to_robot_infrared_message_received_notify_listener = partialmethod(
        Toy._remove_listener, Sensor.robot_to_robot_infrared_message_received_notify)
    get_ambient_light_sensor_value = partialmethod(Sensor.get_ambient_light_sensor_value, proc=Processors.PRIMARY)
    stop_robot_to_robot_infrared_following = partialmethod(Sensor.stop_robot_to_robot_infrared_following,
                                                           proc=Processors.SECONDARY)
    start_robot_to_robot_infrared_evading = partialmethod(Sensor.start_robot_to_robot_infrared_evading,
                                                          proc=Processors.SECONDARY)
    stop_robot_to_robot_infrared_evading = partialmethod(Sensor.stop_robot_to_robot_infrared_evading,
                                                         proc=Processors.SECONDARY)
    enable_color_detection_notify = partialmethod(Sensor.enable_color_detection_notify, proc=Processors.PRIMARY)
    add_color_detection_notify_listener = partialmethod(Toy._add_listener, Sensor.color_detection_notify)
    remove_color_detection_notify_listener = partialmethod(Toy._remove_listener, Sensor.color_detection_notify)
    get_current_detected_color_reading = partialmethod(Sensor.get_current_detected_color_reading,
                                                       proc=Processors.PRIMARY)
    enable_color_detection = partialmethod(Sensor.enable_color_detection, proc=Processors.PRIMARY)
    configure_streaming_service = Sensor.configure_streaming_service
    start_streaming_service = Sensor.start_streaming_service
    stop_streaming_service = Sensor.stop_streaming_service
    clear_streaming_service = Sensor.clear_streaming_service
    add_streaming_service_data_notify_listener = partialmethod(Toy._add_listener, Sensor.streaming_service_data_notify)
    remove_streaming_service_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                  Sensor.streaming_service_data_notify)
    enable_robot_infrared_message_notify = partialmethod(Sensor.enable_robot_infrared_message_notify,
                                                         proc=Processors.SECONDARY)
    send_infrared_message = partialmethod(Sensor.send_infrared_message, proc=Processors.SECONDARY)
    add_motor_current_notify_listener = partialmethod(Toy._add_listener, Sensor.motor_current_notify)
    remove_motor_current_notify_listener = partialmethod(Toy._remove_listener, Sensor.motor_current_notify)
    enable_motor_current_notify = partialmethod(Sensor.enable_motor_current_notify, proc=Processors.SECONDARY)
    get_motor_temperature = partialmethod(Sensor.get_motor_temperature, proc=Processors.SECONDARY)
    configure_sensitivity_based_collision_detection = partialmethod(
        Sensor.configure_sensitivity_based_collision_detection, proc=Processors.SECONDARY)
    enable_sensitivity_based_collision_detection_notify = partialmethod(
        Sensor.enable_sensitivity_based_collision_detection_notify, proc=Processors.SECONDARY)
    add_sensitivity_based_collision_detected_notify_listener = partialmethod(
        Toy._add_listener, Sensor.sensitivity_based_collision_detected_notify)
    remove_sensitivity_based_collision_detected_notify_listener = partialmethod(
        Toy._remove_listener, Sensor.sensitivity_based_collision_detected_notify)
    get_motor_thermal_protection_status = partialmethod(Sensor.get_motor_thermal_protection_status,
                                                        proc=Processors.SECONDARY)
    enable_motor_thermal_protection_status_notify = partialmethod(Sensor.enable_motor_thermal_protection_status_notify,
                                                                  proc=Processors.SECONDARY)
    add_motor_thermal_protection_status_notify_listener = partialmethod(Toy._add_listener,
                                                                        Sensor.motor_thermal_protection_status_notify)
    remove_motor_thermal_protection_status_notify_listener = partialmethod(
        Toy._remove_listener, Sensor.motor_thermal_protection_status_notify)

    set_bluetooth_name = partialmethod(Connection.set_bluetooth_name, proc=Processors.PRIMARY)
    get_bluetooth_name = partialmethod(Connection.get_bluetooth_name, proc=Processors.PRIMARY)
    get_bluetooth_advertising_name = partialmethod(Connection.get_bluetooth_advertising_name, proc=Processors.PRIMARY)

    set_all_leds_with_32_bit_mask = partialmethod(IO.set_all_leds_with_32_bit_mask, proc=Processors.PRIMARY)
    set_compressed_frame_player_one_color = partialmethod(IO.set_compressed_frame_player_one_color,
                                                          proc=Processors.PRIMARY)
    save_compressed_frame_player_animation = partialmethod(IO.save_compressed_frame_player_animation,
                                                           proc=Processors.PRIMARY)
    play_compressed_frame_player_animation = partialmethod(IO.play_compressed_frame_player_animation,
                                                           proc=Processors.PRIMARY)
    play_compressed_frame_player_frame = partialmethod(IO.play_compressed_frame_player_frame,
                                                       proc=Processors.PRIMARY)
    get_compressed_frame_player_list_of_frames = partialmethod(IO.get_compressed_frame_player_list_of_frames,
                                                               proc=Processors.PRIMARY)
    delete_all_compressed_frame_player_animations_and_frames = partialmethod(
        IO.delete_all_compressed_frame_player_animations_and_frames, proc=Processors.PRIMARY)
    pause_compressed_frame_player_animation = partialmethod(IO.pause_compressed_frame_player_animation,
                                                            proc=Processors.PRIMARY)
    resume_compressed_frame_player_animation = partialmethod(IO.resume_compressed_frame_player_animation,
                                                             proc=Processors.PRIMARY)
    reset_compressed_frame_player_animation = partialmethod(IO.reset_compressed_frame_player_animation,
                                                            proc=Processors.PRIMARY)
    add_compressed_frame_player_animation_complete_notify_listener = partialmethod(
        Toy._add_listener, IO.compressed_frame_player_animation_complete_notify)
    remove_compressed_frame_player_animation_complete_notify_listener = partialmethod(
        Toy._remove_listener, IO.compressed_frame_player_animation_complete_notify)
    assign_compressed_frame_player_frames_to_animation = partialmethod(
        IO.assign_compressed_frame_player_frames_to_animation, proc=Processors.PRIMARY)
    save_compressed_frame_player_animation_without_frames = partialmethod(
        IO.save_compressed_frame_player_animation_without_frames, proc=Processors.PRIMARY)
    play_compressed_frame_player_animation_with_loop_option = partialmethod(
        IO.play_compressed_frame_player_animation_with_loop_option, proc=Processors.PRIMARY)
    get_active_color_palette = partialmethod(IO.get_active_color_palette, proc=Processors.PRIMARY)
    set_active_color_palette = partialmethod(IO.set_active_color_palette, proc=Processors.PRIMARY)
    get_color_identification_report = partialmethod(IO.get_color_identification_report, proc=Processors.PRIMARY)
    load_color_palette = partialmethod(IO.load_color_palette, proc=Processors.PRIMARY)
    save_color_palette = partialmethod(IO.save_color_palette, proc=Processors.PRIMARY)
    get_compressed_frame_player_frame_info_type = partialmethod(IO.get_compressed_frame_player_frame_info_type,
                                                                proc=Processors.PRIMARY)
    save_compressed_frame_player16_bit_frame = partialmethod(IO.save_compressed_frame_player16_bit_frame,
                                                             proc=Processors.PRIMARY)
    release_led_requests = partialmethod(IO.release_led_requests, proc=Processors.PRIMARY)

    get_current_application_id = Firmware.get_current_application_id
    get_all_updatable_processors = partialmethod(Firmware.get_all_updatable_processors, proc=Processors.PRIMARY)
    get_version_for_updatable_processors = partialmethod(Firmware.get_version_for_updatable_processors,
                                                         proc=Processors.PRIMARY)
    set_pending_update_for_processors = partialmethod(Firmware.set_pending_update_for_processors,
                                                      proc=Processors.PRIMARY)
    get_pending_update_for_processors = partialmethod(Firmware.get_pending_update_for_processors,
                                                      proc=Processors.PRIMARY)
    reset_with_parameters = partialmethod(Firmware.reset_with_parameters, proc=Processors.PRIMARY)
    clear_pending_update_processors = partialmethod(Firmware.clear_pending_update_processors, proc=Processors.PRIMARY)
    get_factory_mode_challenge = FactoryTest.get_factory_mode_challenge
    enter_factory_mode = FactoryTest.enter_factory_mode
    exit_factory_mode = FactoryTest.exit_factory_mode
    get_chassis_id = FactoryTest.get_chassis_id
    enable_extended_life_test = partialmethod(FactoryTest.enable_extended_life_test, proc=Processors.PRIMARY)
    get_factory_mode_status = FactoryTest.get_factory_mode_status

    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    @property
    @lru_cache(None)
    def multi_led_control(self):
        return LedControl(self)

    @property
    @lru_cache(None)
    def sensor_control(self):
        return StreamingControl(self)
