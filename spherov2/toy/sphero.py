import struct
from collections import OrderedDict
from typing import Callable, List

from spherov2.commands.async_ import Async
from spherov2.commands.core import Core, PowerStates, IntervalOptions
from spherov2.commands.sphero import Sphero as SpheroCmd, CollisionDetectionMethods, RollModes, ReverseFlags, \
    RawMotorModes
from spherov2.listeners.core import Versions, BluetoothInfo, PowerState
from spherov2.listeners.sensor import CollisionDetected
from spherov2.toy.core import Toy, ToySensor
from spherov2.types import ToyType


class Sphero(Toy):
    toy_type = ToyType('SPRK/2.0', None, 'Sphero', .06)

    sensors = OrderedDict(
        attitude=OrderedDict(
            pitch=ToySensor(0x40000, -179., 180.),
            roll=ToySensor(0x20000, -179., 180.),
            yaw=ToySensor(0x10000, -179., 180.)
        ),
        accelerometer=OrderedDict(
            x=ToySensor(0x8000, -32768., 32767., lambda x: x / 4096),
            y=ToySensor(0x4000, -32768., 32767., lambda x: x / 4096),
            z=ToySensor(0x2000, -32768., 32767., lambda x: x / 4096)
        ),
        gyroscope=OrderedDict(
            x=ToySensor(0x1000, -20000., 20000., lambda x: x * .1),
            y=ToySensor(0x800, -20000., 20000., lambda x: x * .1),
            z=ToySensor(0x400, -20000., 20000., lambda x: x * .1)
        ),
        back_emf=OrderedDict(
            left=ToySensor(0x40, -32768., 32767.),
            right=ToySensor(0x20, -32768., 32767.),
        )
    )

    extended_sensors = OrderedDict(
        quaternion=OrderedDict(
            x=ToySensor(0x80000000, -10000., 10000., lambda x: x / 10000),
            y=ToySensor(0x40000000, -10000., 10000., lambda x: x / 10000),
            z=ToySensor(0x20000000, -10000., 10000., lambda x: x / 10000),
            w=ToySensor(0x10000000, -10000., 10000., lambda x: x / 10000)
        ),
        locator=OrderedDict(
            x=ToySensor(0x8000000, -32768., 32767.),
            y=ToySensor(0x4000000, -32768., 32767.),
        ),
        accel_one=OrderedDict(accel_one=ToySensor(0x2000000, 0., 8000.)),
        velocity=OrderedDict(
            x=ToySensor(0x1000000, -32768., 32767., lambda x: x * .1),
            y=ToySensor(0x800000, -32768., 32767., lambda x: x * .1),
        ),
        speed=OrderedDict(speed=ToySensor(0x400000, 0., 32767.)),
    )

    def ping(self):
        self._execute(Core.ping())

    def get_versions(self) -> Versions:
        unpacked = struct.unpack('>8B', bytearray(self._execute(Core.get_versions()).data))
        return Versions(
            record_version=unpacked[0], model_number=unpacked[1], hardware_version_code=unpacked[2],
            main_app_version_major=unpacked[3], main_app_version_minor=unpacked[4],
            bootloader_version='%d.%d' % (unpacked[5] >> 4, unpacked[5] & 0xf),
            orb_basic_version='%d.%d' % (unpacked[6] >> 4, unpacked[6] & 0xf),
            overlay_version='%d.%d' % (unpacked[7] >> 4, unpacked[7] & 0xf),
        )

    def set_bluetooth_name(self, name: str):
        self._execute(Core.set_bluetooth_name(name))

    def get_bluetooth_info(self) -> BluetoothInfo:
        data = self._execute(Core.get_bluetooth_info()).data
        name = ''
        i = 0
        while i < len(data) and data[i] != 0:
            name += chr(data[i])
            i += 1
        while i < len(data) and data[i] == 0:
            i += 1
        address = ''
        while i < len(data) and data[i] != 0:
            address += chr(data[i])
            i += 1
        return BluetoothInfo(name=name, address=address)

    def get_power_state(self) -> PowerState:
        unpacked = struct.unpack('>2B3H', bytearray(self._execute(Core.get_power_state()).data))
        return PowerState(record_version=unpacked[0], state=PowerStates(unpacked[1]), voltage=unpacked[2] / 100,
                          number_of_charges=unpacked[3], time_since_last_charge=unpacked[4])

    def enable_battery_state_changed_notify(self, enable: bool):
        self._execute(Core.enable_battery_state_changed_notify(enable))

    def sleep(self, interval_option: IntervalOptions, unk: int, unk2: int):  # FIXME: unknown arg name
        self._execute(Core.sleep(interval_option, unk, unk2))

    def set_inactivity_timeout(self, timeout: int):
        self._execute(Core.set_inactivity_timeout(timeout))

    # TODO: getChargerState, jumpToBootloader, beginReflash, hereIsPage, jumpToMain

    def set_heading(self, heading: int):
        self._execute(SpheroCmd.set_heading(heading))

    def set_stabilization(self, stabilize: bool):
        self._execute(SpheroCmd.set_stabilization(stabilize))

    # TODO: setRotationRate, getChassisId, selfLevel

    def set_data_streaming(self, interval, num_samples_per_packet, mask, count, extended_mask):
        self._execute(SpheroCmd.set_data_streaming(interval, num_samples_per_packet, mask, count, extended_mask))

    def configure_collision_detection(self, collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time):
        self._execute(SpheroCmd.configure_collision_detection(
            collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time
        ))

    def configure_locator(self, flags, x, y, yaw_tare):  # name from web
        self._execute(SpheroCmd.configure_locator(flags, x, y, yaw_tare))

    # TODO: getTemperature

    def set_main_led(self, r, g, b):
        self._execute(SpheroCmd.set_main_led(r, g, b))

    def set_back_led_brightness(self, brightness):
        self._execute(SpheroCmd.set_back_led_brightness(brightness))

    def roll(self, speed, heading, roll_mode: RollModes, reverse_flag: ReverseFlags):
        self._execute(SpheroCmd.roll(speed, heading, roll_mode, reverse_flag))

    # TODO: boost

    def set_raw_motors(self, left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed):
        self._execute(SpheroCmd.set_raw_motors(left_mode, left_speed, right_mode, right_speed))

    # TODO: setMotionTimeout, setPersistentOptions, getPersistentOptions, setTemporaryOptions, getTemporaryOptions

    def add_battery_state_changed_notify_listener(self, listener: Callable[[PowerStates], None]):
        self._add_listener(Async.battery_state_changed_notify, lambda p: listener(PowerStates(p.data[0])))

    def remove_battery_state_changed_notify_listener(self, listener):
        self._remove_listener(Async.battery_state_changed_notify, listener)

    def add_sensor_streaming_data_notify_listener(self, listener: Callable[[List[int]], None]):
        self._add_listener(Async.sensor_streaming_data_notify,
                           lambda p: listener(list(struct.unpack('>%dH' % (len(p.data) // 2), bytearray(p.data)))))

    def remove_sensor_streaming_data_notify_listener(self, listener):
        self._remove_listener(Async.sensor_streaming_data_notify, listener)

    def add_will_sleep_notify_listener(self, listener: Callable[[], None]):
        self._add_listener(Async.will_sleep_notify, lambda _: listener())

    def remove_will_sleep_notify_listener(self, listener):
        self._remove_listener(Async.will_sleep_notify, listener)

    def add_collision_detected_notify_listener(self, listener: Callable[[CollisionDetected], None]):
        def __process(packet):
            unpacked = struct.unpack('>3HB3HBL', bytearray(packet.data))
            listener(CollisionDetected(acceleration_x=unpacked[0] / 4096, acceleration_y=unpacked[1] / 4096,
                                       acceleration_z=unpacked[2] / 4096, x_axis=bool(unpacked[3] & 1),
                                       y_axis=bool(unpacked[3] & 2), power_x=unpacked[4], power_y=unpacked[5],
                                       power_z=unpacked[6], speed=unpacked[7], time=unpacked[8] / 1000))

        self._add_listener(Async.collision_detected_notify, __process)

    def remove_collision_detected_notify_listener(self, listener):
        self._remove_listener(Async.collision_detected_notify, listener)

    def add_gyro_max_notify_listener(self, listener: Callable[[int], None]):
        self._add_listener(Async.gyro_max_notify, lambda p: listener(p.data[0]))

    def remove_gyro_max_notify_listener(self, listener):
        self._remove_listener(Async.gyro_max_notify, listener)

    def add_did_sleep_notify_listener(self, listener: Callable[[], None]):
        self._add_listener(Async.gyro_max_notify, lambda p: listener())

    def remove_did_sleep_notify_listener(self, listener):
        self._remove_listener(Async.gyro_max_notify, listener)
