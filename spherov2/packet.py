from enum import IntFlag, IntEnum
from typing import List, Tuple


class PacketDecodingException(Exception):
    ...


class Packet:
    """
    Packet structure, from https://sdk.sphero.com/docs/api_spec/general_api
    ---------------------------------
    - start      [1 byte]
    - flags      [1 byte]
    - target_id  [1 byte] (optional)
    - source_id  [1 byte] (optional)
    - device_id  [1 byte]
    - command_id [1 byte]
    - sequence   [1 byte]
    - error      [1 byte] (at response)
    - data       [n byte] (zero or more)
    - checksum   [1 byte]
    - end        [1 byte]
    ---------------------------------
    """

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

    __sequence = -1

    def __init__(self, device_id, command_id,
                 target_id=None, source_id=None, data=None, flags=None, error=None, sequence=None):
        self.flags = flags
        if flags is None:
            self.flags = Packet.Flags.requests_response | Packet.Flags.is_activity
            if target_id is not None:
                self.flags |= Packet.Flags.has_source_id | Packet.Flags.has_target_id
                source_id = 0x1

        self.target_id = target_id
        self.source_id = source_id
        self.device_id = device_id
        self.command_id = command_id
        self.sequence = self.generate_sequence() if sequence is None else sequence
        self.data = data or []
        self.error = error

    @classmethod
    def generate_sequence(cls):
        cls.__sequence = (cls.__sequence + 1) % 0xff
        return cls.__sequence

    @property
    def id(self) -> Tuple:
        return self.device_id, self.command_id, self.sequence

    @staticmethod
    def __unescape_response_data(response_data) -> List[int]:
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

    @staticmethod
    def from_response(response_data) -> 'Packet':
        response_data = Packet.__unescape_response_data(response_data)
        start, flags, *data, checksum, end = response_data
        if start != Packet.Encoding.start:
            raise PacketDecodingException('Unexpected start of packet')
        if end != Packet.Encoding.end:
            raise PacketDecodingException('Unexpected end of packet')

        target_id = None
        if flags & Packet.Flags.has_target_id:
            target_id = data.pop(0)

        source_id = None
        if flags & Packet.Flags.has_source_id:
            source_id = data.pop(0)

        device_id, command_id, sequence, *data = data

        error = Packet.Error.success
        if flags & Packet.Flags.is_response:
            error = Packet.Error(data.pop(0))

        packet = Packet(
            flags=flags,
            target_id=target_id,
            source_id=source_id,
            device_id=device_id,
            command_id=command_id,
            sequence=sequence,
            error=error,
            data=data,
        )

        calc_checksum = packet.checksum
        if calc_checksum != checksum:
            raise PacketDecodingException(
                f'Bad response checksum. (Expected: {checksum:#04x}, obtained: {calc_checksum:#04x})')

        return packet

    @property
    def packet_payload(self) -> List[int]:
        ret = [self.flags]

        if self.flags & Packet.Flags.has_target_id:
            ret.append(self.target_id)

        if self.flags & Packet.Flags.has_source_id:
            ret.append(self.source_id)

        ret.extend((self.device_id, self.command_id, self.sequence))

        if self.flags & Packet.Flags.is_response:
            ret.append(self.error)

        ret.extend(self.data)
        return ret

    @property
    def checksum(self) -> int:
        return 0xff - (sum(self.packet_payload) & 0xff)

    def build(self) -> List[int]:
        full_packet = [
            *self.packet_payload,
            self.checksum,
        ]

        escaped_full_packet = []
        for i in full_packet:
            if i == Packet.Encoding.escape:
                escaped_full_packet.extend((Packet.Encoding.escape, Packet.Encoding.escaped_escape))
            elif i == Packet.Encoding.start:
                escaped_full_packet.extend((Packet.Encoding.escape, Packet.Encoding.escaped_start))
            elif i == Packet.Encoding.end:
                escaped_full_packet.extend((Packet.Encoding.escape, Packet.Encoding.escaped_end))
            else:
                escaped_full_packet.append(i)

        return [Packet.Encoding.start, *escaped_full_packet, Packet.Encoding.end]


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
                self.__callback(Packet.from_response(pkt))
