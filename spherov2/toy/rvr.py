import struct
from enum import IntEnum
from functools import lru_cache
from typing import Callable, List

from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.connection import Connection
from spherov2.commands.drive import Drive, RawMotorModes, MotorIndexes
from spherov2.commands.factory_test import FactoryTest
from spherov2.commands.firmware import Firmware, ApplicationIds, ResetStrategies
from spherov2.commands.io import IO, SpecdrumsColorPaletteIndicies
from spherov2.commands.power import Power, BatteryVoltageStates, BatteryVoltageReadingTypes, AmplifierIds, EfuseIds
from spherov2.commands.sensor import Sensor, SensitivityBasedCollisionDetectionMethods, SensitivityLevels, \
    ThermalProtectionStatus
from spherov2.commands.system_info import SystemInfo, BootReasons, SosMessages
from spherov2.commands.system_mode import SystemMode
from spherov2.controls.v2 import DriveControl, LedControl, StreamingControl, Processors
from spherov2.helper import nibble_to_byte, to_int
from spherov2.listeners.api_and_shell import ApiProtocolVersion
from spherov2.listeners.drive import MotorStall
from spherov2.listeners.power import BatteryVoltageStateThresholds
from spherov2.listeners.sensor import BotToBotInfraredReadings, RgbcSensorValues, ColorDetection, StreamingServiceData, \
    MotorCurrent, MotorTemperature, MotorThermalProtectionStatus
from spherov2.listeners.system_info import Version, LastErrorInfo, ConfigBlock, ManufacturingDate, EventLogStatus
from spherov2.toy.core import Toy
from spherov2.types import ToyType


class RVR(Toy):
    toy_type = ToyType('Sphero RVR', 'RV-', 'RV', .075)

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

    def ping(self, data: bytes, target: Processors):
        self._execute(ApiAndShell.ping(data, nibble_to_byte(1, target)))

    def get_api_protocol_version(self, target: Processors):
        data = self._execute(ApiAndShell.get_api_protocol_version(nibble_to_byte(1, target))).data
        return ApiProtocolVersion(major_version=data[0], minor_version=data[1])

    def send_command_to_shell(self, command: bytes, target: Processors):
        self._execute(ApiAndShell.send_command_to_shell(command, nibble_to_byte(1, target)))

    def add_send_string_to_console_listener(self, listener: Callable[[bytes], None]):
        self._add_listener(ApiAndShell.send_string_to_console, lambda p: listener(bytes(p.data).rstrip(b'\0')))

    def get_supported_dids(self, target: Processors) -> List[int]:
        return list(self._execute(ApiAndShell.get_supported_dids(nibble_to_byte(1, target))).data)

    def get_supported_cids(self, target: Processors) -> List[int]:
        return list(self._execute(ApiAndShell.get_supported_cids(nibble_to_byte(1, target))).data)

    def get_main_app_version(self, target: Processors):
        return Version(*struct.unpack('>3H', bytearray(
            self._execute(SystemInfo.get_main_app_version(nibble_to_byte(1, target))).data)))

    def get_bootloader_version(self, target: Processors):
        return Version(*struct.unpack('>3H', bytearray(
            self._execute(SystemInfo.get_bootloader_version(nibble_to_byte(1, target))).data)))

    def get_board_revision(self):
        return self._execute(SystemInfo.get_board_revision(nibble_to_byte(1, 1))).data[0]

    def get_mac_address(self):
        return bytearray(self._execute(SystemInfo.get_mac_address(nibble_to_byte(1, 1))).data)

    def get_stats_id(self):
        return self._execute(SystemInfo.get_stats_id(nibble_to_byte(1, 1))).data

    def get_processor_name(self, target: Processors) -> bytes:
        return bytes(self._execute(SystemInfo.get_processor_name(nibble_to_byte(1, target))).data).rstrip(b'\0')

    def get_boot_reason(self):
        return BootReasons(self._execute(SystemInfo.get_boot_reason(nibble_to_byte(1, 1))).data[0])

    def get_last_error_info(self):
        return LastErrorInfo(*struct.unpack('>32sH12s', bytearray(
            self._execute(SystemInfo.get_last_error_info(nibble_to_byte(1, 1))).data)))

    def write_config_block(self):
        self._execute(SystemInfo.write_config_block(nibble_to_byte(1, 1)))

    def get_config_block(self):
        data = bytes(self._execute(SystemInfo.get_config_block(nibble_to_byte(1, 1))).data)
        return ConfigBlock(*struct.unpack('>2I', data[:8]), data[8:])

    def set_config_block(self, metadata_version, config_block_version, application_data: bytes):
        self._execute(SystemInfo.set_config_block(
            metadata_version, config_block_version, application_data, nibble_to_byte(1, 1)))

    def erase_config_block(self, j):  # unknown name
        self._execute(SystemInfo.erase_config_block(j, nibble_to_byte(1, 1)))

    def get_swd_locking_status(self, target: Processors):
        return bool(self._execute(SystemInfo.get_swd_locking_status(nibble_to_byte(1, target))).data[0])

    def get_manufacturing_date(self):
        return ManufacturingDate(*struct.unpack('>HBB', bytearray(
            self._execute(SystemInfo.get_manufacturing_date(nibble_to_byte(1, 1))).data)))

    def get_sku(self):
        return bytes(self._execute(SystemInfo.get_sku(nibble_to_byte(1, 1))).data).rstrip(b'\0')

    def get_core_up_time_in_milliseconds(self):
        return to_int(self._execute(SystemInfo.get_core_up_time_in_milliseconds(nibble_to_byte(1, 1))).data)

    def get_event_log_status(self, target: Processors):
        return EventLogStatus(*struct.unpack('>3I', bytearray(
            self._execute(SystemInfo.get_event_log_status(nibble_to_byte(1, target))).data)))

    def get_event_log_data(self, j, j2, target: Processors):  # unknown name
        return bytes(self._execute(SystemInfo.get_event_log_data(j, j2, nibble_to_byte(1, target))).data)

    def clear_event_log(self, target: Processors):
        self._execute(SystemInfo.clear_event_log(nibble_to_byte(1, target)))

    def enable_sos_message_notify(self, enable: bool):
        self._execute(SystemInfo.enable_sos_message_notify(enable, nibble_to_byte(1, 1)))

    def add_sos_message_notify_listener(self, listener: Callable[[SosMessages], None]):
        self._add_listener(SystemInfo.sos_message_notify, lambda p: listener(SosMessages(p.data[0])))

    def get_sos_message(self):
        self._execute(SystemInfo.get_sos_message(nibble_to_byte(1, 1)))

    def clear_sos_message(self):
        self._execute(SystemInfo.clear_sos_message(nibble_to_byte(1, 1)))

    def get_out_of_box_state(self):
        return bool(self._execute(SystemMode.get_out_of_box_state(nibble_to_byte(1, 1))).data[0])

    def enable_out_of_box_state(self, enable: bool):
        self._execute(SystemMode.enable_out_of_box_state(enable, nibble_to_byte(1, 1)))

    def enter_deep_sleep(self, s):
        self._execute(Power.enter_deep_sleep(s, nibble_to_byte(1, 1)))

    def sleep(self):
        self._execute(Power.sleep(nibble_to_byte(1, 1)))

    def force_battery_refresh(self):
        self._execute(Power.force_battery_refresh(nibble_to_byte(1, 1)))

    def wake(self):
        self._execute(Power.wake(nibble_to_byte(1, 1)))

    def get_battery_percentage(self):
        return self._execute(Power.get_battery_percentage(nibble_to_byte(1, 1))).data[0]

    def get_battery_voltage_state(self):
        return BatteryVoltageStates(self._execute(Power.get_battery_voltage_state(nibble_to_byte(1, 1))).data[0])

    def add_will_sleep_notify_listener(self, listener: Callable[[], None]):
        self._add_listener(Power.will_sleep_notify, lambda _: listener())

    def add_did_sleep_notify_listener(self, listener: Callable[[], None]):
        self._add_listener(Power.did_sleep_notify, lambda _: listener())

    def enable_battery_voltage_state_change_notify(self, enable: bool):
        self._execute(Power.enable_battery_voltage_state_change_notify(enable, nibble_to_byte(1, 1)))

    def add_battery_voltage_state_change_notify_listener(self, listener: Callable[[BatteryVoltageStates], None]):
        self._add_listener(Power.battery_voltage_state_change_notify,
                           lambda p: listener(BatteryVoltageStates(p.data[0])))

    def get_battery_voltage_in_volts(self, reading_type: BatteryVoltageReadingTypes):
        return struct.unpack('>f', bytearray(
            self._execute(Power.get_battery_voltage_in_volts(reading_type, nibble_to_byte(1, 1))).data))[0]

    def get_battery_voltage_state_thresholds(self):
        return BatteryVoltageStateThresholds(*struct.unpack('>3f', bytearray(
            self._execute(Power.get_battery_voltage_state_thresholds(nibble_to_byte(1, 1))).data)))

    def get_current_sense_amplifier_current(self, amplifier_id: AmplifierIds):
        return struct.unpack('>f', bytearray(
            self._execute(Power.get_current_sense_amplifier_current(amplifier_id, nibble_to_byte(1, 1))).data))[0]

    def get_efuse_fault_status(self, efuse_id: EfuseIds):
        return self._execute(Power.get_efuse_fault_status(efuse_id, nibble_to_byte(1, 1))).data[0]

    def add_efuse_fault_occurred_notify_listener(self, listener: Callable[[EfuseIds], None]):
        self._add_listener(Power.efuse_fault_occurred_notify, lambda p: listener(EfuseIds(p.data[0])))

    def enable_efuse(self, efuse_id: EfuseIds):
        self._execute(Power.enable_efuse(efuse_id, nibble_to_byte(1, 1)))

    def set_raw_motors(self, left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed):
        self._execute(Drive.set_raw_motors(left_mode, left_speed, right_mode, right_speed, nibble_to_byte(1, 2)))

    def reset_yaw(self):
        self._execute(Drive.reset_yaw(nibble_to_byte(1, 2)))

    def drive_with_heading(self, speed, heading, drive_flags):
        self._execute(Drive.drive_with_heading(speed, heading, drive_flags, nibble_to_byte(1, 2)))

    def set_control_system_type(self, s, s2):  # unknown name
        self._execute(Drive.set_control_system_type(s, s2, nibble_to_byte(1, 2)))

    def set_component_parameters(self, s, s2, f_arr: List[float]):  # unknown name
        self._execute(Drive.set_component_parameters(s, s2, f_arr, nibble_to_byte(1, 2)))

    def get_component_parameters(self, s, s2):  # unknown name
        data = bytearray(self._execute(Drive.get_component_parameters(s, s2, nibble_to_byte(1, 2))).data)
        return struct.unpack('>%df' % (len(data) // 4), data)

    def set_custom_control_system_timeout(self, timeout: int):
        self._execute(Drive.set_custom_control_system_timeout(timeout, nibble_to_byte(1, 2)))

    def enable_motor_stall_notify(self, enable: bool):
        self._execute(Drive.enable_motor_stall_notify(enable, nibble_to_byte(1, 2)))

    def add_motor_stall_notify_listener(self, listener: Callable[[MotorStall], None]):
        self._add_listener(Drive.motor_stall_notify, lambda p: listener(MotorStall(*p.data)))

    def enable_motor_fault_notify(self, enable: bool):
        self._execute(Drive.enable_motor_fault_notify(enable, nibble_to_byte(1, 2)))

    def add_motor_fault_notify_listener(self, listener: Callable[[bool], None]):
        self._add_listener(Drive.motor_fault_notify, lambda p: listener(bool(p.data[0])))

    def get_motor_fault_state(self):
        return bool(self._execute(Drive.get_motor_fault_state(nibble_to_byte(1, 2))).data[0])

    def enable_gyro_max_notify(self, enable: bool):
        self._execute(Sensor.enable_gyro_max_notify(enable, nibble_to_byte(1, 2)))

    def add_gyro_max_notify_listener(self, listener: Callable[[int], None]):
        self._add_listener(Sensor.gyro_max_notify, lambda p: listener(p.data[0]))

    def reset_locator_x_and_y(self):
        self._execute(Sensor.reset_locator_x_and_y(nibble_to_byte(1, 2)))

    def set_locator_flags(self, locator_flags: bool):
        self._execute(Sensor.set_locator_flags(locator_flags, nibble_to_byte(1, 2)))

    def get_bot_to_bot_infrared_readings(self):
        data = to_int(self._execute(Sensor.get_bot_to_bot_infrared_readings(nibble_to_byte(1, 2))).data)
        return BotToBotInfraredReadings(data & 1, data & 2, data & 4, data & 8)

    def get_rgbc_sensor_values(self):
        return RgbcSensorValues(*struct.unpack('>4H', bytearray(
            self._execute(Sensor.get_rgbc_sensor_values(nibble_to_byte(1, 1))).data)))

    def magnetometer_calibrate_to_north(self):
        self._execute(Sensor.magnetometer_calibrate_to_north(nibble_to_byte(1, 2)))

    def add_magnetometer_north_yaw_notify_listener(self, listener: Callable[[int], None]):
        self._add_listener(Sensor.magnetometer_north_yaw_notify, lambda p: listener(to_int(p.data)))

    def start_robot_to_robot_infrared_broadcasting(self, far_code, near_code):
        self._execute(Sensor.start_robot_to_robot_infrared_broadcasting(far_code, near_code, nibble_to_byte(1, 2)))

    def start_robot_to_robot_infrared_following(self, far_code, near_code):
        self._execute(Sensor.start_robot_to_robot_infrared_following(far_code, near_code, nibble_to_byte(1, 2)))

    def stop_robot_to_robot_infrared_broadcasting(self):
        self._execute(Sensor.stop_robot_to_robot_infrared_broadcasting(nibble_to_byte(1, 2)))

    def add_robot_to_robot_infrared_message_received_notify_listener(self, listener: Callable[[int], None]):
        self._add_listener(Sensor.robot_to_robot_infrared_message_received_notify, lambda p: listener(p.data[0]))

    def get_ambient_light_sensor_value(self):
        return struct.unpack('>f', bytearray(
            self._execute(Sensor.get_ambient_light_sensor_value(nibble_to_byte(1, 1))).data))[0]

    def stop_robot_to_robot_infrared_following(self):
        self._execute(Sensor.stop_robot_to_robot_infrared_following(nibble_to_byte(1, 2)))

    def start_robot_to_robot_infrared_evading(self, far_code, near_code):
        self._execute(Sensor.start_robot_to_robot_infrared_evading(far_code, near_code, nibble_to_byte(1, 2)))

    def stop_robot_to_robot_infrared_evading(self):
        self._execute(Sensor.stop_robot_to_robot_infrared_evading(nibble_to_byte(1, 2)))

    def enable_color_detection_notify(self, enable: bool, interval, minimum_confidence_threshold):
        self._execute(
            Sensor.enable_color_detection_notify(enable, interval, minimum_confidence_threshold, nibble_to_byte(1, 1)))

    def add_color_detection_notify_listener(self, listener: Callable[[ColorDetection], None]):
        self._add_listener(Sensor.color_detection_notify, lambda p: listener(ColorDetection(*p.data)))

    def get_current_detected_color_reading(self):
        self._execute(Sensor.get_current_detected_color_reading())

    def enable_color_detection(self, enable: bool):
        self._execute(Sensor.enable_color_detection(enable))

    def configure_streaming_service(self, token, configuration: List[int], target: Processors):
        self._execute(Sensor.configure_streaming_service(token, configuration, nibble_to_byte(1, target)))

    def start_streaming_service(self, period, target: Processors):
        self._execute(Sensor.start_streaming_service(period, nibble_to_byte(1, target)))

    def stop_streaming_service(self, target: Processors):
        self._execute(Sensor.stop_streaming_service(nibble_to_byte(1, target)))

    def clear_streaming_service(self, target: Processors):
        self._execute(Sensor.clear_streaming_service(nibble_to_byte(1, target)))

    def add_streaming_service_data_notify_listener(self, listener: Callable[[int, StreamingServiceData], None]):
        self._add_listener(Sensor.streaming_service_data_notify,
                           lambda p: listener(p.source_id, StreamingServiceData(p.data[0], bytearray(p.data[1:]))))

    def enable_robot_infrared_message_notify(self, enable: bool):
        self._execute(Sensor.enable_robot_infrared_message_notify(enable, nibble_to_byte(1, 2)))

    def send_infrared_message(self, infrared_code, front_strength, left_strength, right_strength, rear_strength):
        self._execute(Sensor.send_infrared_message(
            infrared_code, front_strength, left_strength, right_strength, rear_strength, nibble_to_byte(1, 2)))

    def add_motor_current_notify_listener(self, listener: Callable[[MotorCurrent], None]):
        self._add_listener(Sensor.motor_current_notify,
                           lambda p: listener(MotorCurrent(*struct.unpack('>2fQ', bytearray(p.data)))))

    def enable_motor_current_notify(self, enable: bool):
        self._execute(Sensor.enable_motor_current_notify(enable, nibble_to_byte(1, 2)))

    def get_motor_temperature(self, motor_index: MotorIndexes):
        return MotorTemperature(*struct.unpack('>2f', bytearray(
            self._execute(Sensor.get_motor_temperature(motor_index, nibble_to_byte(1, 2))).data)))

    def configure_sensitivity_based_collision_detection(
            self, method: SensitivityBasedCollisionDetectionMethods, level: SensitivityLevels, i):  # unknown names
        self._execute(Sensor.configure_sensitivity_based_collision_detection(method, level, i, nibble_to_byte(1, 2)))

    def enable_sensitivity_based_collision_detection_notify(self, enable: bool):
        self._execute(Sensor.enable_sensitivity_based_collision_detection_notify(enable, nibble_to_byte(1, 2)))

    def add_sensitivity_based_collision_detected_notify_listener(self, listener: Callable[[int], None]):
        self._add_listener(Sensor.sensitivity_based_collision_detected_notify, lambda p: listener(to_int(p.data)))

    def get_motor_thermal_protection_status(self):
        data = struct.unpack('>fBfB', bytearray(self._execute(Sensor.get_motor_thermal_protection_status()).data))
        return MotorThermalProtectionStatus(
            data[0], ThermalProtectionStatus(data[1]), data[2], ThermalProtectionStatus(data[3]))

    def enable_motor_thermal_protection_status_notify(self, enable: bool):
        self._execute(Sensor.enable_motor_thermal_protection_status_notify(enable, nibble_to_byte(1, 2)))

    def add_motor_thermal_protection_status_notify_listener(
            self, listener: Callable[[MotorThermalProtectionStatus], None]):
        def __process(packet):
            data = struct.unpack('>fBfB', bytearray(packet.data))
            listener(MotorThermalProtectionStatus(
                data[0], ThermalProtectionStatus(data[1]), data[2], ThermalProtectionStatus(data[3])))

        self._add_listener(Sensor.motor_thermal_protection_status_notify, __process)

    def set_bluetooth_name(self, name: bytes):
        self._execute(Connection.set_bluetooth_name(name, nibble_to_byte(1, 1)))

    def get_bluetooth_name(self):
        return bytes(self._execute(Connection.get_bluetooth_name(nibble_to_byte(1, 1))).data).rstrip(b'\0')

    def get_bluetooth_advertising_name(self):
        return bytes(self._execute(Connection.get_bluetooth_advertising_name(nibble_to_byte(1, 1))).data).rstrip(b'\0')

    def set_all_leds_with_32_bit_mask(self, mask, values):
        self._execute(IO.set_all_leds_with_32_bit_mask(mask, values, nibble_to_byte(1, 1)))

    def set_compressed_frame_player_one_color(self, s, s2, s3):  # unknown names
        self._execute(IO.set_compressed_frame_player_one_color(s, s2, s3, nibble_to_byte(1, 1)))

    def save_compressed_frame_player_animation(
            self, s, s2, z: bool, s3, s_arr: List[int], i, i_arr: List[int]):  # unknown names
        self._execute(IO.save_compressed_frame_player_animation(s, s2, z, s3, s_arr, i, i_arr, nibble_to_byte(1, 1)))

    def play_compressed_frame_player_animation(self, s):  # unknown names
        self._execute(IO.play_compressed_frame_player_animation(s, nibble_to_byte(1, 1)))

    def play_compressed_frame_player_frame(self, i):  # unknown names
        self._execute(IO.play_compressed_frame_player_frame(i, nibble_to_byte(1, 1)))

    def get_compressed_frame_player_list_of_frames(self):
        data = self._execute(IO.get_compressed_frame_player_list_of_frames(nibble_to_byte(1, 1))).data
        return struct.unpack('>%dH' % (len(data) // 2), bytearray(data))

    def delete_all_compressed_frame_player_animations_and_frames(self):
        self._execute(IO.delete_all_compressed_frame_player_animations_and_frames(nibble_to_byte(1, 1)))

    def pause_compressed_frame_player_animation(self):
        self._execute(IO.pause_compressed_frame_player_animation(nibble_to_byte(1, 1)))

    def resume_compressed_frame_player_animation(self):
        self._execute(IO.resume_compressed_frame_player_animation(nibble_to_byte(1, 1)))

    def reset_compressed_frame_player_animation(self):
        self._execute(IO.reset_compressed_frame_player_animation(nibble_to_byte(1, 1)))

    def add_compressed_frame_player_animation_complete_notify_listener(self, listener: Callable[[int], None]):
        self._add_listener(IO.compressed_frame_player_animation_complete_notify, lambda p: listener(p.data[0]))

    def assign_compressed_frame_player_frames_to_animation(self, s, i, i_arr: List[int]):  # unknown names
        self._execute(IO.assign_compressed_frame_player_frames_to_animation(s, i, i_arr, nibble_to_byte(1, 1)))

    def save_compressed_frame_player_animation_without_frames(
            self, s, s2, z: bool, s3, s_arr: List[int], i):  # unknown names
        self._execute(
            IO.save_compressed_frame_player_animation_without_frames(s, s2, z, s3, s_arr, i, nibble_to_byte(1, 1)))

    def play_compressed_frame_player_animation_with_loop_option(self, s, z: bool):  # unknown names
        self._execute(IO.play_compressed_frame_player_animation_with_loop_option(s, z, nibble_to_byte(1, 1)))

    def get_active_color_palette(self):
        return self._execute(IO.get_active_color_palette(nibble_to_byte(1, 1))).data

    def set_active_color_palette(self, rgb_index_bytes: List[int]):
        self._execute(IO.set_active_color_palette(rgb_index_bytes, nibble_to_byte(1, 1)))

    def get_color_identification_report(self, red, green, blue, confidence_threshold):
        return self._execute(
            IO.get_color_identification_report(red, green, blue, confidence_threshold, nibble_to_byte(1, 1))).data

    def load_color_palette(self, palette_index: SpecdrumsColorPaletteIndicies):
        self._execute(IO.load_color_palette(palette_index, nibble_to_byte(1, 1)))

    def save_color_palette(self, palette_index: SpecdrumsColorPaletteIndicies):
        self._execute(IO.save_color_palette(palette_index, nibble_to_byte(1, 1)))

    def get_compressed_frame_player_frame_info_type(self):
        self._execute(IO.get_compressed_frame_player_frame_info_type(nibble_to_byte(1, 1)))

    def save_compressed_frame_player16_bit_frame(self, i, i2, i3, i4, i5):  # unknown names
        return to_int(
            self._execute(IO.save_compressed_frame_player16_bit_frame(i, i2, i3, i4, i5, nibble_to_byte(1, 1))).data)

    def release_led_requests(self):
        self._execute(IO.release_led_requests(nibble_to_byte(1, 1)))

    def get_current_application_id(self, target: Processors):
        return ApplicationIds(self._execute(Firmware.get_current_application_id(nibble_to_byte(1, target))).data[0])

    def get_all_updatable_processors(self):
        self._execute(Firmware.get_all_updatable_processors(nibble_to_byte(1, 1)))

    def get_version_for_updatable_processors(self):
        self._execute(Firmware.get_version_for_updatable_processors(nibble_to_byte(1, 1)))

    def set_pending_update_for_processors(self, data: bytes):  # unknown names
        return ResetStrategies(self._execute(Firmware.set_pending_update_for_processors(data, nibble_to_byte(1, 1))))

    def get_pending_update_for_processors(self):
        return self._execute(Firmware.get_pending_update_for_processors(nibble_to_byte(1, 1))).data

    def reset_with_parameters(self, strategy: ResetStrategies):
        self._execute(Firmware.reset_with_parameters(strategy, nibble_to_byte(1, 1)))

    def clear_pending_update_processors(self, data: bytes):  # unknown names
        self._execute(Firmware.clear_pending_update_processors(data, nibble_to_byte(1, 1)))

    def get_factory_mode_challenge(self, target: Processors):
        return to_int(self._execute(FactoryTest.get_factory_mode_challenge(nibble_to_byte(1, target))).data)

    def enter_factory_mode(self, challenge: int, target: Processors):
        self._execute(FactoryTest.enter_factory_mode(challenge, nibble_to_byte(1, target)))

    def exit_factory_mode(self, target: Processors):
        self._execute(FactoryTest.exit_factory_mode(nibble_to_byte(1, target)))

    def get_chassis_id(self, target: Processors):
        return to_int(self._execute(FactoryTest.get_chassis_id(nibble_to_byte(1, target))).data)

    def enable_extended_life_test(self, enable: bool):
        self._execute(FactoryTest.enable_extended_life_test(enable, nibble_to_byte(1, 1)))

    def get_factory_mode_status(self, target: Processors):
        return bool(self._execute(FactoryTest.get_factory_mode_status(nibble_to_byte(1, target))).data[0])

    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    @property
    @lru_cache(None)
    def multi_led_control(self):
        return LedControl(self)

    led_control = multi_led_control

    @property
    @lru_cache(None)
    def sensor_control(self):
        return StreamingControl(self)
