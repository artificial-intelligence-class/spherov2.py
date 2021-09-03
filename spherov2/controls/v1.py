import threading
from enum import IntEnum
from typing import NamedTuple, Callable, Dict, List

from spherov2.commands.sphero import ReverseFlags, RollModes
from spherov2.controls import PacketDecodingException, CommandExecuteError
from spherov2.helper import packet_chk, to_bytes


class Packet:
    """Packet protocol v1.2, from https://docs.gosphero.com/api/Sphero_API_1.20.pdf"""

    SOP = 0xff
    ASYNC = 0xfe

    class Error(IntEnum):
        command_succeeded = 0x00
        non_specific_error = 0x01
        checksum_failure = 0x02
        command_fragment = 0x03
        unknown_command_id = 0x04
        unsupported_command = 0x05
        bad_message_format = 0x06
        parameter_value_invalid = 0x07
        failed_to_execute = 0x08
        unknown_device_id = 0x09
        voltage_too_low = 0x31
        illegal_page_number = 0x32
        flash_fail = 0x33
        main_application_corrupt = 0x34
        message_timeout = 0x35

    class Request(NamedTuple):
        """[SOP1, SOP2, DID, CID, SEQ, DLEN, <data>, CHK]"""

        did: int
        cid: int
        seq: int
        data: bytearray

        @property
        def id(self):
            return Packet.SOP, self.seq

        @property
        def dlen(self):
            return len(self.data) + 1

        def build(self) -> bytearray:
            payload = bytearray([Packet.SOP, Packet.SOP, self.did, self.cid, self.seq, self.dlen, *self.data])
            payload.append(packet_chk(payload[2:]))
            return payload

    class Response(NamedTuple):
        """[SOP1, SOP2, MRSP, SEQ, DLEN, <data>, CHK]"""

        mrsp: 'Packet.Error'
        seq: int
        data: bytearray

        @property
        def id(self):
            return Packet.SOP, self.seq

        @property
        def dlen(self):
            return len(self.data) + 1

        def build(self) -> bytearray:
            payload = bytearray([Packet.SOP, Packet.SOP, self.mrsp, self.seq, self.dlen, *self.data])
            payload.append(packet_chk(payload[2:]))
            return payload

        def check_error(self):
            if self.mrsp != Packet.Error.command_succeeded:
                raise CommandExecuteError(self.mrsp)

    class Async(NamedTuple):
        """[SOP1, SOP2, ID CODE, DLEN-MSB, DLEN-LSB, <data>, CHK]"""

        id_code: int
        data: bytearray

        @property
        def id(self):
            return Packet.ASYNC, self.id_code

        @property
        def dlen(self):
            return to_bytes(len(self.data) + 1, 2)

        def build(self) -> bytearray:
            payload = bytearray([Packet.SOP, Packet.ASYNC, self.id_code, *self.dlen, *self.data])
            payload.append(packet_chk(payload[2:]))
            return payload

    @staticmethod
    def parse_response(data) -> Response:
        chk = data.pop()
        if chk != packet_chk(data):
            raise PacketDecodingException('Bad response checksum')
        mrsp, seq, _, *data = data
        return Packet.Response(Packet.Error(mrsp), seq, bytearray(data))

    @staticmethod
    def parse_async(data) -> Async:
        chk = data.pop()
        if chk != packet_chk(data):
            raise PacketDecodingException('Bad response checksum')
        id_code, _, _, *data = data
        return Packet.Async(id_code, bytearray(data))

    class Manager:
        def __init__(self):
            self.__seq = 0

        def new_packet(self, did, cid, _, data=None):
            packet = Packet.Request(did, cid, self.__seq, bytearray(data or []))
            self.__seq = (self.__seq + 1) % 0x100
            return packet

    class Collector:
        def __init__(self, callback):
            self.__callback = callback
            self.__data = bytearray()

        def add(self, data):
            if not self.__data:
                while data and data[0] != Packet.SOP:
                    data.pop(0)
            self.__data.extend(data)
            while len(self.__data) > 4:
                sop1, sop2, *payload = self.__data
                if sop1 != Packet.SOP:
                    self.__data.clear()
                    raise PacketDecodingException('Unexpected start of packet')
                if sop2 == Packet.SOP:
                    _, _, dlen, *remain = payload
                    if dlen > len(remain):
                        break
                    self.__callback(Packet.parse_response(payload[:dlen + 3]))
                    self.__data = remain[dlen:]
                elif sop2 == Packet.ASYNC:
                    _, dlen_msb, dlen_lsb, *remain = payload
                    dlen = (dlen_msb << 8) | dlen_lsb
                    if dlen > len(remain):
                        break
                    self.__callback(Packet.parse_async(payload[:dlen + 3]))
                    self.__data = remain[dlen:]
                else:
                    raise PacketDecodingException('Unexpected start of packet 2')


class DriveControl:
    def __init__(self, toy):
        self.__toy = toy
        self.__is_aiming = False

    def roll_start(self, heading, speed):
        flag = ReverseFlags.OFF
        if speed < 0:
            flag = ReverseFlags.ON
            heading = (heading + 180) % 360
        speed = min(255, abs(speed))
        self.__toy.roll(speed, heading, RollModes.GO, flag)

    def roll_stop(self, heading):
        self.__toy.roll(0, heading, RollModes.STOP, ReverseFlags.OFF)

    def set_heading(self, heading):
        self.__toy.roll(0, heading, RollModes.CALIBRATE, ReverseFlags.OFF)

    def set_stabilization(self, stabilize):
        self.__toy.set_stabilization(stabilize)

    def set_raw_motors(self, left_mode, left_speed, right_mode, right_speed):
        self.__toy.set_raw_motors(left_mode, left_speed, right_mode, right_speed)


class FirmwareUpdateControl:
    def __init__(self, toy):
        self.__toy = toy


class LedControl:
    def __init__(self, toy):
        self.__toy = toy


class SensorControl:
    def __init__(self, toy):
        toy.add_sensor_streaming_data_notify_listener(self.__sensor_streaming_data)

        self.__toy = toy
        self.__count = 0
        self.__interval = 250
        self.__enabled = {}
        self.__enabled_extended = {}
        self.__listeners = set()

    def add_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.add(listener)

    def remove_sensor_data_listener(self, listener: Callable[[Dict[str, Dict[str, float]]], None]):
        self.__listeners.remove(listener)

    def __sensor_streaming_data(self, sensor_data: List[int]):
        data = {}

        def __new_data():
            n = {}
            for name, component in components.items():
                d = sensor_data.pop(0)
                if component.modifier:
                    d = component.modifier(d)
                n[name] = d
            if self.__toy.name.startswith('2B') and sensor in ['locator', 'velocity']:
                n['x'], n['y'] = -n['y'], n['x']
            data[sensor] = n

        for sensor, components in self.__toy.sensors.items():
            if sensor in self.__enabled:
                __new_data()
        for sensor, components in self.__toy.extended_sensors.items():
            if sensor in self.__enabled_extended:
                __new_data()

        for f in self.__listeners:
            threading.Thread(target=f, args=(data,)).start()

    def set_count(self, count: int):
        if count >= 0 and count != self.__count:
            self.__count = count
            self.__update()

    def set_interval(self, interval: int):
        if interval >= 0 and interval != self.__interval:
            self.__interval = interval * 4 // 10
            if self.__interval == 0 and interval > 0:
                self.__interval = 1
            self.__update()

    def __update(self):
        sensors_mask = extended_sensors_mask = 0
        for sensor in self.__enabled.values():
            for component in sensor.values():
                sensors_mask |= component.bit
        for sensor in self.__enabled_extended.values():
            for component in sensor.values():
                extended_sensors_mask |= component.bit
        self.__toy.set_data_streaming(self.__interval, 1, sensors_mask, self.__count, extended_sensors_mask)

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
