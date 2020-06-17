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
