from typing import NamedTuple

from spherov2.controls.enums import PacketDecodingException
from spherov2.helper import packet_chk, to_bytes


class Packet:
    """Packet protocol v1.2, from https://docs.gosphero.com/api/Sphero_API_1.20.pdf"""

    SOP = 0xff
    ASYNC = 0xfe

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

        mrsp: int
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
        return Packet.Response(mrsp, seq, bytearray(data))

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
