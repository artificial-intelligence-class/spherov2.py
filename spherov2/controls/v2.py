import threading
from collections import OrderedDict, defaultdict
from enum import IntEnum, Enum, auto, IntFlag
from typing import Dict, List, Callable, NamedTuple, Tuple

from spherov2.commands.drive import DriveFlags
from spherov2.commands.drive import RawMotorModes as DriveRawMotorModes
from spherov2.commands.io import IO
from spherov2.controls import RawMotorModes, PacketDecodingException, CommandExecuteError
from spherov2.helper import to_bytes, to_int, packet_chk
from spherov2.listeners.sensor import StreamingServiceData


class Packet(NamedTuple):
    """Packet protocol v2, from https://sdk.sphero.com/docs/api_spec/general_api
    [SOP, FLAGS, TID (optional), SID (optional), DID, CID, SEQ, ERR (at response), DATA..., CHK, EOP]"""

    flags: 'Packet.Flags'
    did: int
    cid: int
    seq: int
    tid: int
    sid: int
    data: bytearray
    err: 'Packet.Error' = None

    class Flags(IntFlag):
        is_response = 0b1
        requests_response = 0b10
        requests_only_error_response = 0b100
        is_activity = 0b1000
        has_target_id = 0b10000
        has_source_id = 0b100000
        unused = 0b1000000
        extended_flags = 0b10000000

    class Encoding(IntEnum):
        escape = 0xAB
        start = 0x8D
        end = 0xD8
        escaped_escape = 0x23
        escaped_start = 0x05
        escaped_end = 0x50

    class Error(IntEnum):
        success = 0x00
        bad_device_id = 0x01
        bad_command_id = 0x02
        not_yet_implemented = 0x03
        command_is_restricted = 0x04
        bad_data_length = 0x05
        command_failed = 0x06
        bad_parameter_value = 0x07
        busy = 0x08
        bad_target_id = 0x09
        target_unavailable = 0x0a

    @staticmethod
    def parse_response(data) -> 'Packet':
        sop, *data, eop = data
        if sop != Packet.Encoding.start:
            raise PacketDecodingException('Unexpected start of packet')
        if eop != Packet.Encoding.end:
            raise PacketDecodingException('Unexpected end of packet')
        *data, chk = Packet.__unescape_data(data)
        if packet_chk(data) != chk:
            raise PacketDecodingException('Bad response checksum')

        flags = data.pop(0)

        tid = None
        if flags & Packet.Flags.has_target_id:
            tid = data.pop(0)

        sid = None
        if flags & Packet.Flags.has_source_id:
            sid = data.pop(0)

        did, cid, seq, *data = data

        err = Packet.Error.success
        if flags & Packet.Flags.is_response:
            err = Packet.Error(data.pop(0))

        return Packet(flags, did, cid, seq, tid, sid, bytearray(data), err)

    @staticmethod
    def __unescape_data(response_data) -> List[int]:
        raw_data = []

        iter_response_data = iter(response_data)
        for b in iter_response_data:
            if b == Packet.Encoding.escape:
                b = next(iter_response_data, None)
                if b == Packet.Encoding.escaped_escape:
                    b = Packet.Encoding.escape
                elif b == Packet.Encoding.escaped_start:
                    b = Packet.Encoding.start
                elif b == Packet.Encoding.escaped_end:
                    b = Packet.Encoding.end
                else:
                    raise PacketDecodingException('Unexpected escaping byte')

            raw_data.append(b)

        return raw_data

    @property
    def id(self) -> Tuple:
        return self.did, self.cid, self.seq

    def build(self) -> bytearray:
        packet = bytearray([self.flags])

        if self.flags & Packet.Flags.has_target_id:
            packet.append(self.tid)

        if self.flags & Packet.Flags.has_source_id:
            packet.append(self.sid)

        packet.extend(self.id)

        if self.flags & Packet.Flags.is_response:
            packet.append(self.err)

        packet.extend(self.data)
        packet.append(packet_chk(packet))

        escaped_packet = bytearray([Packet.Encoding.start])
        for c in packet:
            if c == Packet.Encoding.escape:
                escaped_packet.extend((Packet.Encoding.escape, Packet.Encoding.escaped_escape))
            elif c == Packet.Encoding.start:
                escaped_packet.extend((Packet.Encoding.escape, Packet.Encoding.escaped_start))
            elif c == Packet.Encoding.end:
                escaped_packet.extend((Packet.Encoding.escape, Packet.Encoding.escaped_end))
            else:
                escaped_packet.append(c)
        escaped_packet.append(Packet.Encoding.end)

        return escaped_packet

    def check_error(self):
        if self.err != Packet.Error.success:
            raise CommandExecuteError(self.err)

    class Manager:
        def __init__(self):
            self.__seq = 0

        def new_packet(self, did, cid, tid=None, data=None):
            flags = Packet.Flags.requests_response | Packet.Flags.is_activity
            sid = None
            if tid is not None:
                flags |= Packet.Flags.has_source_id | Packet.Flags.has_target_id
                sid = 0x1
            packet = Packet(flags, did, cid, self.__seq, tid, sid, bytearray(data or []))
            self.__seq = (self.__seq + 1) % 0xff
            return packet

    class Collector:
        def __init__(self, callback):
            self.__callback = callback
            self.__data = []

        def add(self, data):
            for b in data:
                self.__data.append(b)
                if b == Packet.Encoding.end:
                    pkt = self.__data
                    self.__data = []
                    if len(pkt) < 6:
                        raise PacketDecodingException(f'Very small packet {[hex(x) for x in pkt]}')
                    self.__callback(Packet.parse_response(pkt))


class AnimationControl:
    def __init__(self, toy):
        self.__toy = toy


class DriveControl:
    def __init__(self, toy):
        self.__toy = toy
        self.__is_boosting = False

    def roll_start(self, heading, speed):
        flag = DriveFlags.FORWARD
        if speed < 0:
            flag = DriveFlags.BACKWARD
            heading = (heading + 180) % 360
        if self.__is_boosting:
            flag |= DriveFlags.TURBO
        speed = min(255, abs(speed))
        self.__toy.drive_with_heading(speed, heading, flag)

    def roll_stop(self, heading):
        self.roll_start(heading, 0)

    set_heading = roll_stop

    def set_stabilization(self, stabilize):
        self.__toy.set_stabilization(stabilize)

    def set_raw_motors(self, left_mode, left_speed, right_mode, right_speed):
        if left_mode == RawMotorModes.FORWARD:
            left_drive_mode = DriveRawMotorModes.FORWARD
        elif left_mode == RawMotorModes.REVERSE:
            left_drive_mode = DriveRawMotorModes.REVERSE
        else:
            left_drive_mode = DriveRawMotorModes.OFF

        if right_mode == RawMotorModes.FORWARD:
            right_drive_mode = DriveRawMotorModes.FORWARD
        elif right_mode == RawMotorModes.REVERSE:
            right_drive_mode = DriveRawMotorModes.REVERSE
        else:
            right_drive_mode = DriveRawMotorModes.OFF

        self.__toy.set_raw_motors(left_drive_mode, left_speed, right_drive_mode, right_speed)

    def reset_heading(self):
        self.__toy.reset_yaw()


class FirmwareUpdateControl:
    def __init__(self, toy):
        self.__toy = toy


class LedControl:
    def __init__(self, toy):
        self.__toy = toy

    def set_leds(self, mapping: Dict[IntEnum, int]):
        mask = 0
        led_values = []
        for e in self.__toy.LEDs:
            if e in mapping:
                mask |= 1 << e
                led_values.append(mapping[e])
        if mask:
            if self.__toy.implements(IO.set_all_leds_with_32_bit_mask):
                self.__toy.set_all_leds_with_32_bit_mask(mask, led_values)
            elif self.__toy.implements(IO.set_all_leds_with_16_bit_mask):
                self.__toy.set_all_leds_with_16_bit_mask(mask, led_values)
            elif hasattr(self.__toy, 'set_all_leds_with_8_bit_mask'):
                self.__toy.set_all_leds_with_8_bit_mask(mask, led_values)


class SensorControl:
    def __init__(self, toy):
        toy.add_sensor_streaming_data_notify_listener(self.__process_sensor_stream_data)

        self.__toy = toy
        self.__count = 0
        self.__interval = 250
        self.__enabled = {}
        self.__enabled_extended = {}
        self.__listeners = set()

    def __process_sensor_stream_data(self, sensor_data: List[float]):
        data = {}

        def __new_data():
            n = {}
            for name, component in components.items():
                d = sensor_data.pop(0)
                if component.modifier:
                    d = component.modifier(d)
                n[name] = d
            data[sensor] = n

        for sensor, components in self.__toy.sensors.items():
            if sensor in self.__enabled:
                __new_data()
        for sensor, components in self.__toy.extended_sensors.items():
            if sensor in self.__enabled_extended:
                __new_data()

        for f in self.__listeners:
            threading.Thread(target=f, args=(data,)).start()

    def add_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.add(listener)

    def remove_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.remove(listener)

    def set_count(self, count: int):
        if count >= 0 and count != self.__count:
            self.__count = count
            self.__update()

    def set_interval(self, interval: int):
        if interval >= 0 and interval != self.__interval:
            self.__interval = interval
            self.__update()

    def __update(self):
        sensors_mask = extended_sensors_mask = 0
        for sensor in self.__enabled.values():
            for component in sensor.values():
                sensors_mask |= component.bit
        for sensor in self.__enabled_extended.values():
            for component in sensor.values():
                extended_sensors_mask |= component.bit
        self.__toy.set_sensor_streaming_mask(0, self.__count, sensors_mask)
        self.__toy.set_extended_sensor_streaming_mask(extended_sensors_mask)
        self.__toy.set_sensor_streaming_mask(self.__interval, self.__count, sensors_mask)

    def enable(self, *sensors):
        for sensor in sensors:
            if sensor in self.__toy.sensors:
                self.__enabled[sensor] = self.__toy.sensors[sensor]
            elif sensor in self.__toy.extended_sensors:
                self.__enabled_extended[sensor] = self.__toy.extended_sensors[sensor]
        self.__update()

    def disable(self, *sensors):
        for sensor in sensors:
            self.__enabled.pop(sensor, None)
            self.__enabled_extended.pop(sensor, None)
        self.__update()

    def disable_all(self):
        self.__enabled.clear()
        self.__enabled_extended.clear()
        self.__update()


class StatsControl:
    def __init__(self, toy):
        self.__toy = toy


class Processors(IntEnum):
    UNKNOWN = 0
    PRIMARY = 1
    SECONDARY = 2


class StreamingServiceAttribute(NamedTuple):
    min_value: int
    max_value: int
    modifier: Callable[[float], float] = None


class StreamingDataSizes(IntEnum):
    EightBit = 0
    SixteenBit = 1
    ThirtyTwoBit = 2


class StreamingService(NamedTuple):
    attributes: OrderedDict
    slot: int
    processor: Processors = Processors.SECONDARY
    data_size: StreamingDataSizes = StreamingDataSizes.ThirtyTwoBit


class StreamingServiceState(Enum):
    Unknown = auto()
    Stop = auto()
    Start = auto()
    Restart = auto()


class StreamingControl:
    __streaming_services = {
        'quaternion': StreamingService(OrderedDict(
            w=StreamingServiceAttribute(-1, 1),
            x=StreamingServiceAttribute(-1, 1),
            y=StreamingServiceAttribute(-1, 1),
            z=StreamingServiceAttribute(-1, 1)
        ), 1),
        'imu': StreamingService(OrderedDict(
            pitch=StreamingServiceAttribute(-180, 180),
            roll=StreamingServiceAttribute(-90, 90),
            yaw=StreamingServiceAttribute(-180, 180)
        ), 1),
        'accelerometer': StreamingService(OrderedDict(
            x=StreamingServiceAttribute(-16, 16),
            y=StreamingServiceAttribute(-16, 16),
            z=StreamingServiceAttribute(-16, 16)
        ), 1),
        'color_detection': StreamingService(OrderedDict(
            r=StreamingServiceAttribute(0, 255),
            g=StreamingServiceAttribute(0, 255),
            b=StreamingServiceAttribute(0, 255),
            index=StreamingServiceAttribute(0, 255),
            confidence=StreamingServiceAttribute(0, 1)
        ), 1, Processors.PRIMARY, StreamingDataSizes.EightBit),
        'gyroscope': StreamingService(OrderedDict(
            x=StreamingServiceAttribute(-2000, 2000),
            y=StreamingServiceAttribute(-2000, 2000),
            z=StreamingServiceAttribute(-2000, 2000)
        ), 1),
        'core_time_lower': StreamingService(OrderedDict(time_lower=StreamingServiceAttribute(0, 1 << 63)), 3),
        'locator': StreamingService(OrderedDict(
            x=StreamingServiceAttribute(-16000, 16000, lambda x: x * 100.),
            y=StreamingServiceAttribute(-16000, 16000, lambda x: x * 100.),
        ), 2),
        'velocity': StreamingService(OrderedDict(
            x=StreamingServiceAttribute(-5, 5, lambda x: x * 100.),
            y=StreamingServiceAttribute(-5, 5, lambda x: x * 100.),
        ), 2),
        'speed': StreamingService(OrderedDict(speed=StreamingServiceAttribute(0, 5, lambda x: x * 100.)), 2),
        'core_time_upper': StreamingService(OrderedDict(time_upper=StreamingServiceAttribute(0, 1 << 63)), 3),
        'ambient_light': StreamingService(
            OrderedDict(light=StreamingServiceAttribute(0, 120000)), 2, Processors.PRIMARY
        ),
    }

    def __init__(self, toy):
        toy.add_streaming_service_data_notify_listener(self.__streaming_service_data)
        self.__toy = toy
        self.__slots = {
            Processors.PRIMARY: defaultdict(list),
            Processors.SECONDARY: defaultdict(list)
        }
        self.__enabled = set()
        self.__listeners = set()
        self.__interval = 500

    def add_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.add(listener)

    def remove_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.remove(listener)

    def enable(self, *sensors):
        changed = False
        for sensor in sensors:
            if sensor not in self.__enabled and sensor in self.__streaming_services:
                self.__enabled.add(sensor)
                changed = True
        if changed:
            self.__configure(StreamingServiceState.Start)

    def disable(self, *sensors):
        changed = False
        for sensor in sensors:
            if sensor in self.__enabled:
                self.__enabled.remove(sensor)
                changed = True
        if changed:
            self.__configure(StreamingServiceState.Start if self.__enabled else StreamingServiceState.Stop)

    def disable_all(self):
        if not self.__enabled:
            return
        self.__enabled.clear()
        self.__configure(StreamingServiceState.Stop)

    def set_count(self, count: int):
        pass

    def set_interval(self, interval: int):
        if interval < 0:
            raise ValueError('Interval attempted to be set with negative value')
        self.__interval = interval
        if self.__enabled:
            self.__configure(StreamingServiceState.Restart)

    def __configure(self, state: StreamingServiceState):
        for target in [Processors.PRIMARY, Processors.SECONDARY]:
            self.__toy.stop_streaming_service(target)
            if state == StreamingServiceState.Stop:
                self.__toy.clear_streaming_service(target)
            elif state == StreamingServiceState.Start:
                self.__toy.clear_streaming_service(target)
                slots = self.__slots[target]
                slots.clear()
                for index, (s, sensor) in enumerate(self.__streaming_services.items()):
                    if s in self.__enabled and sensor.processor == target:
                        slots[sensor.slot].append((index, s, sensor))
                if slots:
                    for slot, services in slots.items():
                        data = []
                        for index, _, sensor in services:
                            data.extend(to_bytes(index, 2))
                            data.append(sensor.data_size)
                        self.__toy.configure_streaming_service(slot, data, target)
                    self.__toy.start_streaming_service(self.__interval, target)
            elif state == StreamingServiceState.Restart:
                self.__toy.start_streaming_service(self.__interval, target)

    def __streaming_service_data(self, source_id, data: StreamingServiceData):
        node = data.token & 0xf
        processor = source_id & 0xf
        sensor_data = data.sensor_data
        services = self.__slots[processor][node]
        data = {}
        for _, sensor_name, sensor in services:
            n = {}
            for name, component in sensor.attributes.items():
                data_size = 1 << sensor.data_size
                value, sensor_data = to_int(sensor_data[:data_size]), sensor_data[data_size:]
                value = value / ((1 << data_size * 8) - 1) * (
                        component.max_value - component.min_value) + component.min_value
                if component.modifier is not None:
                    value = component.modifier(value)
                n[name] = value
            if sensor_name == 'color_detection' and node != 0:
                continue
            data[sensor_name] = n
        for f in self.__listeners:
            threading.Thread(target=f, args=(data,)).start()
