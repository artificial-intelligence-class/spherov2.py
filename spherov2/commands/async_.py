import struct
from enum import IntEnum, IntFlag

from spherov2.listeners.async_ import CollisionDetected
from spherov2.listeners.core import PowerStates


class CollisionAxis(IntFlag):
    X_AXIS = 0x1  # 0b1
    Y_AXIS = 0x2  # 0b10


class GyroMaxExceedsFlags(IntFlag):
    X_POSITIVE = 0x1  # 0b1
    X_NEGATIVE = 0x2  # 0b10
    Y_POSITIVE = 0x4  # 0b100
    Y_NEGATIVE = 0x8  # 0b1000
    Z_POSITIVE = 0x10  # 0b10000
    Z_NEGATIVE = 0x20  # 0b100000


class PowerStates(IntEnum):
    UNKNOWN = 0
    CHARGING = 1
    OK = 2
    LOW = 3
    CRITICAL = 4


class Async:
    battery_state_changed_notify = (0xfe, 1), lambda listener, p: listener(PowerStates(p.data[0]))
    sensor_streaming_data_notify = (
        (0xfe, 3), lambda listener, p: listener(list(struct.unpack('>%dh' % (len(p.data) // 2), p.data))))
    will_sleep_notify = (0xfe, 5), lambda listener, _: listener()

    @staticmethod
    def __process(listener, packet):
        unpacked = struct.unpack('>3hB2hBL', packet.data)
        listener(CollisionDetected(acceleration_x=unpacked[0] / 4096, acceleration_y=unpacked[1] / 4096,
                                   acceleration_z=unpacked[2] / 4096, x_axis=bool(unpacked[3] & 1),
                                   y_axis=bool(unpacked[3] & 2), power_x=unpacked[4], power_y=unpacked[5],
                                   speed=unpacked[6], time=unpacked[7] / 1000))

    collision_detected_notify = (0xfe, 7), __process.__func__
    gyro_max_notify = (0xfe, 12), lambda listener, p: listener(p.data[0])
    did_sleep_notify = (0xfe, 20), lambda listener, _: listener()
