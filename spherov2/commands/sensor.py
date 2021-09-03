import struct
from enum import IntEnum, IntFlag

from spherov2.commands import Commands
from spherov2.helper import to_bytes, to_int
from spherov2.listeners.sensor import SensorStreamingMask, CollisionDetected, BotToBotInfraredReadings, \
    RgbcSensorValues, ColorDetection, StreamingServiceData, MotorCurrent, MotorTemperature, \
    MotorThermalProtectionStatus, ThermalProtectionStatus


class CliffDetectionSensorLocations(IntFlag):
    FRONT_LEFT = 0x1  # 0b1
    FRONT_RIGHT = 0x2  # 0b10
    BACK_LEFT = 0x4  # 0b100
    BACK_RIGHT = 0x8  # 0b1000


class CollisionDetectedAxis(IntFlag):
    X_AXIS = 0x1  # 0b1
    Y_AXIS = 0x2  # 0b10


class GyroMaxFlags(IntFlag):
    MAX_PLUS_X = 0x1  # 0b1
    MAX_MINUS_X = 0x2  # 0b10
    MAX_PLUS_Y = 0x4  # 0b100
    MAX_MINUS_Y = 0x8  # 0b1000
    MAX_PLUS_Z = 0x10  # 0b10000
    MAX_MINUS_Z = 0x20  # 0b100000


class InfraredSensorLocations(IntFlag):
    FRONT_LEFT = 0xff  # 0b11111111
    FRONT_RIGHT = 0xff00  # 0b1111111100000000
    BACK_LEFT = 0xff000000  # 0b11111111000000000000000000000000 #How it's displayed in decompiled: -0x1000000
    BACK_RIGHT = 0xff0000  # 0b111111110000000000000000


class LocatorFlags(IntFlag):
    AUTO_CALIBRATE = 0x1  # 0b1


class CollisionDetectionMethods(IntEnum):
    NO_COLLISION_DETECTION = 0
    ACCELEROMETER_BASED_DETECTION = 1
    ACCELEROMETER_BASED_WITH_EXTRA_FILTERING = 2
    HYBRID_ACCELEROMETER_AND_CONTROL_SYSTEM_DETECTION = 3


class MotorIndexes(IntEnum):
    LEFT_MOTOR_INDEX = 0
    RIGHT_MOTOR_INDEX = 1


class SensitivityBasedCollisionDetectionMethods(IntEnum):
    ACCELEROMETER_BASED_DETECTION = 0


class SensitivityLevels(IntEnum):
    SUPER_HIGH = 0
    VERY_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    VERY_LOW = 5


class SteamingDataSizes(IntEnum):
    EIGHT_BIT = 0
    SIXTEEN_BIT = 1
    THIRTY_TWO_BIT = 2


class ThermalProtectionStatus(IntEnum):
    OK = 0
    WARN = 1
    CRITICAL = 2


class Sensor(Commands):
    _did = 24

    @staticmethod
    def set_sensor_streaming_mask(toy, interval, count, sensor_masks, proc=None):
        toy._execute(Sensor._encode(toy, 0, proc, [*to_bytes(interval, 2), count, *to_bytes(sensor_masks, 4)]))

    @staticmethod
    def get_sensor_streaming_mask(toy, proc=None):
        return SensorStreamingMask(*struct.unpack('>HBI', toy._execute(Sensor._encode(toy, 1, proc)).data))

    sensor_streaming_data_notify = (
        (24, 2, 0xff), lambda listener, p: listener(list(struct.unpack('>%df' % (len(p.data) // 4), p.data))))

    @staticmethod
    def set_extended_sensor_streaming_mask(toy, sensor_masks, proc=None):
        toy._execute(Sensor._encode(toy, 12, proc, to_bytes(sensor_masks, 4)))

    @staticmethod
    def get_extended_sensor_streaming_mask(toy, proc=None):
        return to_int(toy._execute(Sensor._encode(toy, 13, proc)).data)

    @staticmethod
    def enable_gyro_max_notify(toy, enable, proc=None):
        toy._execute(Sensor._encode(toy, 15, proc, [int(enable)]))

    gyro_max_notify = (24, 16, 0xff), lambda listener, p: listener(p.data[0])

    @staticmethod
    def configure_collision_detection(toy, collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time, proc=None):
        toy._execute(Sensor._encode(
            toy, 17, proc, [collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time]))

    @staticmethod
    def __collision_detected_notify_helper(listener, packet):
        unpacked = struct.unpack('>3hB3hBL', packet.data)
        listener(CollisionDetected(acceleration_x=unpacked[0] / 4096, acceleration_y=unpacked[1] / 4096,
                                   acceleration_z=unpacked[2] / 4096, x_axis=bool(unpacked[3] & 1),
                                   y_axis=bool(unpacked[3] & 2), power_x=unpacked[4], power_y=unpacked[5],
                                   power_z=unpacked[6], speed=unpacked[7], time=unpacked[8] / 1000))

    collision_detected_notify = (24, 18, 0xff), __collision_detected_notify_helper.__func__

    @staticmethod
    def reset_locator_x_and_y(toy, proc=None):
        toy._execute(Sensor._encode(toy, 19, proc))

    @staticmethod
    def enable_collision_detected_notify(toy, enable: bool, proc=None):  # Untested
        toy._execute(Sensor._encode(toy, 20, proc, [int(enable)]))

    @staticmethod
    def set_locator_flags(toy, locator_flags: bool, proc=None):
        toy._execute(Sensor._encode(toy, 23, proc, [int(locator_flags)]))

    @staticmethod
    def set_accelerometer_activity_threshold(toy, threshold: float, proc=None):
        toy._execute(Sensor._encode(toy, 24, proc, struct.pack('>f', threshold)))

    @staticmethod
    def enable_accelerometer_activity_notify(toy, enable: bool, proc=None):
        toy._execute(Sensor._encode(toy, 25, proc, [int(enable)]))

    accelerometer_activity_notify = (24, 26, 0xff), lambda listener, _: listener()

    @staticmethod
    def set_gyro_activity_threshold(toy, threshold: float, proc=None):
        toy._execute(Sensor._encode(toy, 27, proc, struct.pack('>f', threshold)))

    @staticmethod
    def enable_gyro_activity_notify(toy, enable: bool, proc=None):
        toy._execute(Sensor._encode(toy, 28, proc, [int(enable)]))

    gyro_activity_notify = (24, 29, 0xff), lambda listener, _: listener()

    @staticmethod
    def get_bot_to_bot_infrared_readings(toy, proc=None):
        data = to_int(toy._execute(Sensor._encode(toy, 34, proc)).data)
        return BotToBotInfraredReadings(data & 1, data & 2, data & 4, data & 8)

    @staticmethod
    def get_rgbc_sensor_values(toy, proc=None):
        return RgbcSensorValues(*struct.unpack('>4H', toy._execute(Sensor._encode(toy, 35, proc)).data))

    @staticmethod
    def magnetometer_calibrate_to_north(toy, proc=None):
        toy._execute(Sensor.magnetometer_calibrate_to_north(Sensor._encode(toy, 37, proc)))

    magnetometer_north_yaw_notify = (24, 38, 0xff), lambda listener, p: listener(to_int(p.data))

    @staticmethod
    def start_robot_to_robot_infrared_broadcasting(toy, far_code, near_code, proc=None):
        toy._execute(Sensor._encode(toy, 39, proc, [far_code, near_code]))

    @staticmethod
    def start_robot_to_robot_infrared_following(toy, far_code, near_code, proc=None):
        toy._execute(Sensor._encode(toy, 40, proc, [far_code, near_code]))

    @staticmethod
    def stop_robot_to_robot_infrared_broadcasting(toy, proc=None):
        toy._execute(Sensor._encode(toy, 41, proc))

    @staticmethod
    def send_robot_to_robot_infrared_message(toy, s, s2, s3, s4, s5, proc=None):  # Untested / Unknown param names
        toy._execute(Sensor._encode(toy, 42, proc, [s, s2, s3, s4, s5]))

    @staticmethod
    def listen_for_robot_to_robot_infrared_message(toy, s, j, proc=None):  # Untested / Unknown param names
        toy._execute(Sensor._encode(toy, 43, proc, [s, j]))

    robot_to_robot_infrared_message_received_notify = (24, 44, 0xff), lambda listener, p: listener(p.data[0])

    @staticmethod
    def get_ambient_light_sensor_value(toy, proc=None):
        return struct.unpack('>f', toy._execute(Sensor._encode(toy, 48, proc)).data)[0]

    @staticmethod
    def stop_robot_to_robot_infrared_following(toy, proc=None):
        toy._execute(Sensor._encode(toy, 50, proc))

    @staticmethod
    def start_robot_to_robot_infrared_evading(toy, far_code, near_code, proc=None):
        toy._execute(Sensor._encode(toy, 51, proc, [far_code, near_code]))

    @staticmethod
    def stop_robot_to_robot_infrared_evading(toy, proc=None):
        toy._execute(Sensor._encode(toy, 52, proc))

    @staticmethod
    def enable_color_detection_notify(toy, enable, interval, minimum_confidence_threshold, proc=None):
        toy._execute(
            Sensor._encode(toy, 53, proc, [int(enable), *to_bytes(interval, 2), minimum_confidence_threshold]))

    color_detection_notify = (24, 54, 0xff), lambda listener, p: listener(ColorDetection(*p.data))

    @staticmethod
    def get_current_detected_color_reading(toy, proc=None):
        toy._execute(Sensor._encode(toy, 55, proc))

    @staticmethod
    def enable_color_detection(toy, enable, proc=None):
        toy._execute(Sensor._encode(toy, 56, proc, [int(enable)]))

    @staticmethod
    def configure_streaming_service(toy, token, configuration, proc=None):
        toy._execute(Sensor._encode(toy, 57, proc, [token, *configuration]))

    @staticmethod
    def start_streaming_service(toy, period, proc=None):
        toy._execute(Sensor._encode(toy, 58, proc, to_bytes(period, 2)))

    @staticmethod
    def stop_streaming_service(toy, proc=None):
        toy._execute(Sensor._encode(toy, 59, proc))

    @staticmethod
    def clear_streaming_service(toy, proc=None):
        toy._execute(Sensor._encode(toy, 60, proc))

    streaming_service_data_notify = (
        (24, 61, 0xff), lambda listener, p: listener(p.sid, StreamingServiceData(p.data[0], p.data[1:])))

    @staticmethod
    def enable_robot_infrared_message_notify(toy, enable, proc=None):
        toy._execute(Sensor._encode(toy, 62, proc, [int(enable)]))

    @staticmethod
    def send_infrared_message(toy, infrared_code, front_strength, left_strength, right_strength, rear_strength,
                              proc=None):
        toy._execute(Sensor._encode(
            toy, 63, proc, [infrared_code, front_strength, left_strength, right_strength, rear_strength]))

    motor_current_notify = (
        (24, 64, 0xff), lambda listener, p: listener(MotorCurrent(*struct.unpack('>2fQ', p.data))))

    @staticmethod
    def enable_motor_current_notify(toy, enable, proc=None):
        toy._execute(Sensor._encode(toy, 65, proc, data=[int(enable)]))

    @staticmethod
    def get_motor_temperature(toy, motor_index, proc=None):
        return MotorTemperature(
            *struct.unpack('>2f', toy._execute(Sensor._encode(toy, 66, proc, data=[motor_index])).data))

    @staticmethod
    def configure_sensitivity_based_collision_detection(
            toy, method: SensitivityBasedCollisionDetectionMethods, level: SensitivityLevels, i,  # unknown name
            proc=None):
        toy._execute(Sensor._encode(toy, 71, proc, data=[method, level, *to_bytes(i, 2)]))

    @staticmethod
    def enable_sensitivity_based_collision_detection_notify(toy, enable, proc=None):
        toy._execute(Sensor._encode(toy, 72, proc, data=[int(enable)]))

    sensitivity_based_collision_detected_notify = (24, 73, 0xff), lambda listener, p: listener(to_int(p.data))

    @staticmethod
    def get_motor_thermal_protection_status(toy, proc=None):
        data = struct.unpack('>fBfB', toy._execute(Sensor._encode(toy, 75, proc)).data)
        return MotorThermalProtectionStatus(
            data[0], ThermalProtectionStatus(data[1]), data[2], ThermalProtectionStatus(data[3]))

    @staticmethod
    def enable_motor_thermal_protection_status_notify(toy, enable, proc=None):
        toy._execute(Sensor._encode(toy, 76, proc, [int(enable)]))

    @staticmethod
    def __motor_thermal_protection_status_notify_helper(listener, packet):
        data = struct.unpack('>fBfB', packet.data)
        listener(MotorThermalProtectionStatus(
            data[0], ThermalProtectionStatus(data[1]), data[2], ThermalProtectionStatus(data[3])))

    motor_thermal_protection_status_notify = (24, 77, 0xff), __motor_thermal_protection_status_notify_helper.__func__
