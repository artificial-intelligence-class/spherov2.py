import struct

from spherov2.listeners.core import PowerStates
from spherov2.listeners.sensor import CollisionDetected


class Async:
    battery_state_changed_notify = (0xfe, 1), lambda listener, p: listener(PowerStates(p.data[0]))
    sensor_streaming_data_notify = (
        (0xfe, 3), lambda listener, p: listener(list(struct.unpack('>%dH' % (len(p.data) // 2), p.data))))
    will_sleep_notify = (0xfe, 5), lambda listener, _: listener()

    @staticmethod
    def __process(listener, packet):
        print(packet.data)
        unpacked = struct.unpack('>3HB3HBL', packet.data)
        listener(CollisionDetected(acceleration_x=unpacked[0] / 4096, acceleration_y=unpacked[1] / 4096,
                                   acceleration_z=unpacked[2] / 4096, x_axis=bool(unpacked[3] & 1),
                                   y_axis=bool(unpacked[3] & 2), power_x=unpacked[4], power_y=unpacked[5],
                                   power_z=unpacked[6], speed=unpacked[7], time=unpacked[8] / 1000))

    collision_detected_notify = (0xfe, 7), __process.__func__
    gyro_max_notify = (0xfe, 12), lambda listener, p: listener(p.data[0])
    did_sleep_notify = (0xfe, 20), lambda listener, _: listener()
