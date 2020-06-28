import struct
from enum import IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class CollisionDetectionMethods(IntEnum):
    NO_COLLISION_DETECTION = 0
    ACCELEROMETER_BASED_DETECTION = 1
    ACCELEROMETER_BASED_WITH_EXTRA_FILTERING = 2
    HYBRID_ACCELEROMETER_AND_CONTROL_SYSTEM_DETECTION = 3


class ThermalProtectionStatus(IntEnum):
    OK = 0
    WARN = 1
    CRITICAL = 2


class SensitivityBasedCollisionDetectionMethods(IntEnum):
    ACCELEROMETER_BASED_DETECTION = 0


class SensitivityLevels(IntEnum):
    SUPER_HIGH = 0
    VERY_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    VERY_LOW = 5


class Sensor:
    __encode = partial(Packet, device_id=24)

    @staticmethod
    def set_sensor_streaming_mask(interval, count, sensor_masks, target_id=None):
        return Sensor.__encode(
            command_id=0,
            data=[*to_bytes(interval, 2), count, *to_bytes(sensor_masks, 4)],
            target_id=target_id
        )

    @staticmethod
    def get_sensor_streaming_mask(target_id=None):
        return Sensor.__encode(command_id=1, target_id=target_id)

    sensor_streaming_data_notify = (24, 2, 0xff)

    @staticmethod
    def set_extended_sensor_streaming_mask(sensor_masks, target_id=None):
        return Sensor.__encode(command_id=12, data=to_bytes(sensor_masks, 4), target_id=target_id)

    @staticmethod
    def get_extended_sensor_streaming_mask(target_id=None):
        return Sensor.__encode(command_id=13, target_id=target_id)

    @staticmethod
    def enable_gyro_max_notify(enable, target_id=None):
        return Sensor.__encode(command_id=15, data=[int(enable)], target_id=target_id)

    gyro_max_notify = (24, 16, 0xff)

    @staticmethod
    def configure_collision_detection(collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time, target_id=None):
        return Sensor.__encode(command_id=17,
                               data=[collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time],
                               target_id=target_id)

    collision_detected_notify = (24, 18, 0xff)

    @staticmethod
    def reset_locator_x_and_y(target_id=None):
        return Sensor.__encode(command_id=19, target_id=target_id)

    @staticmethod
    def set_locator_flags(locator_flags: bool, target_id=None):
        return Sensor.__encode(command_id=23, data=[int(locator_flags)], target_id=target_id)

    @staticmethod
    def set_accelerometer_activity_threshold(threshold: float, target_id=None):
        return Sensor.__encode(command_id=24, data=struct.pack('>f', threshold), target_id=target_id)

    @staticmethod
    def enable_accelerometer_activity_notify(enable: bool, target_id=None):
        return Sensor.__encode(command_id=25, data=[int(enable)], target_id=target_id)

    accelerometer_activity_notify = (24, 26, 0xff)

    @staticmethod
    def set_gyro_activity_threshold(threshold: float, target_id=None):
        return Sensor.__encode(command_id=27, data=struct.pack('>f', threshold), target_id=target_id)

    @staticmethod
    def enable_gyro_activity_notify(enable: bool, target_id=None):
        return Sensor.__encode(command_id=28, data=[int(enable)], target_id=target_id)

    gyro_activity_notify = (24, 29, 0xff)

    @staticmethod
    def get_bot_to_bot_infrared_readings(target_id=None):
        return Sensor.__encode(command_id=34, target_id=target_id)

    @staticmethod
    def get_rgbc_sensor_values(target_id=None):
        return Sensor.__encode(command_id=35, target_id=target_id)

    @staticmethod
    def magnetometer_calibrate_to_north(target_id=None):
        return Sensor.__encode(command_id=37, target_id=target_id)

    magnetometer_north_yaw_notify = (24, 38, 0xff)

    @staticmethod
    def start_robot_to_robot_infrared_broadcasting(far_code, near_code, target_id=None):
        return Sensor.__encode(command_id=39, data=[far_code, near_code], target_id=target_id)

    @staticmethod
    def start_robot_to_robot_infrared_following(far_code, near_code, target_id=None):
        return Sensor.__encode(command_id=40, data=[far_code, near_code], target_id=target_id)

    @staticmethod
    def stop_robot_to_robot_infrared_broadcasting(target_id=None):
        return Sensor.__encode(command_id=41, target_id=target_id)

    robot_to_robot_infrared_message_received_notify = (24, 44, 0xff)

    @staticmethod
    def get_ambient_light_sensor_value(target_id=None):
        return Sensor.__encode(command_id=48, target_id=target_id)

    @staticmethod
    def stop_robot_to_robot_infrared_following(target_id=None):
        return Sensor.__encode(command_id=50, target_id=target_id)

    @staticmethod
    def start_robot_to_robot_infrared_evading(far_code, near_code, target_id=None):
        return Sensor.__encode(command_id=51, data=[far_code, near_code], target_id=target_id)

    @staticmethod
    def stop_robot_to_robot_infrared_evading(target_id=None):
        return Sensor.__encode(command_id=52, target_id=target_id)

    @staticmethod
    def enable_color_detection_notify(enable, interval, minimum_confidence_threshold, target_id=None):
        return Sensor.__encode(command_id=53, data=[int(enable), *to_bytes(interval, 2), minimum_confidence_threshold],
                               target_id=target_id)

    color_detection_notify = (24, 54, 0xff)

    @staticmethod
    def get_current_detected_color_reading(target_id=None):
        return Sensor.__encode(command_id=55, target_id=target_id)

    @staticmethod
    def enable_color_detection(enable, target_id=None):
        return Sensor.__encode(command_id=56, data=[int(enable)], target_id=target_id)

    @staticmethod
    def configure_streaming_service(token, configuration, target_id=None):
        return Sensor.__encode(command_id=57, data=[token, *configuration], target_id=target_id)

    @staticmethod
    def start_streaming_service(period, target_id=None):
        return Sensor.__encode(command_id=58, data=to_bytes(period, 2), target_id=target_id)

    @staticmethod
    def stop_streaming_service(target_id=None):
        return Sensor.__encode(command_id=59, target_id=target_id)

    @staticmethod
    def clear_streaming_service(target_id=None):
        return Sensor.__encode(command_id=60, target_id=target_id)

    streaming_service_data_notify = (24, 61, 0xff)

    @staticmethod
    def enable_robot_infrared_message_notify(enable, target_id=None):
        return Sensor.__encode(command_id=62, data=[int(enable)], target_id=target_id)

    @staticmethod
    def send_infrared_message(infrared_code, front_strength, left_strength, right_strength, rear_strength,
                              target_id=None):
        return Sensor.__encode(
            command_id=63,
            data=[infrared_code, front_strength, left_strength, right_strength, rear_strength],
            target_id=target_id)

    motor_current_notify = (24, 64, 0xff)

    @staticmethod
    def enable_motor_current_notify(enable, target_id=None):
        return Sensor.__encode(command_id=65, data=[int(enable)], target_id=target_id)

    @staticmethod
    def get_motor_temperature(motor_index, target_id=None):
        return Sensor.__encode(command_id=66, data=[motor_index], target_id=target_id)

    @staticmethod
    def configure_sensitivity_based_collision_detection(method, level, i, target_id=None):
        return Sensor.__encode(command_id=71, data=[method, level, *to_bytes(i, 2)], target_id=target_id)

    @staticmethod
    def enable_sensitivity_based_collision_detection_notify(enable, target_id=None):
        return Sensor.__encode(command_id=72, data=[int(enable)], target_id=target_id)

    sensitivity_based_collision_detected_notify = (24, 73, 0xff)

    @staticmethod
    def get_motor_thermal_protection_status(target_id=None):
        return Sensor.__encode(command_id=75, target_id=target_id)

    @staticmethod
    def enable_motor_thermal_protection_status_notify(enable, target_id=None):
        return Sensor.__encode(command_id=76, data=[int(enable)], target_id=target_id)

    motor_thermal_protection_status_notify = (24, 77, 0xff)
