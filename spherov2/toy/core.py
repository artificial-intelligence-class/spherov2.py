import threading
from dataclasses import dataclass

from spherov2.adapter.bleak import BleakAdaptor
from spherov2.packet import Packet, Collector
from spherov2.toy.types import CharacteristicUUID


class CommandTimeoutException(Exception):
    ...


class CommandExecuteError(Exception):
    ...


class Toy:
    def __init__(self, mac_address, adapter_cls=BleakAdaptor):
        self.mac_address = mac_address

        self.__adapter = None
        self.__adapter_cls = adapter_cls
        self.__decoder = Collector(self.__new_packet)
        self.__packets = {}
        self.__cv = threading.Condition()

    def __enter__(self):
        self.__adapter = self.__adapter_cls(self.mac_address)
        self.__adapter.set_callback(CharacteristicUUID.api_v2.value, self.__api_read)
        self.__adapter.write(CharacteristicUUID.anti_dos.value, b'usetheforce...band')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__adapter.close()
        self.__adapter = None

    def _execute(self, packet: Packet) -> Packet:
        if self.__adapter is None:
            raise RuntimeError('Use toys in context manager')
        print('request ' + ' '.join([hex(c) for c in packet.build()]))
        self.__adapter.write(CharacteristicUUID.api_v2.value, packet.build())
        return self._wait_packet(packet.id)

    def _wait_packet(self, key, timeout=10.0):
        with self.__cv:
            if self.__cv.wait_for(lambda: key in self.__packets, timeout):
                return self.__packets[key]
        raise CommandTimeoutException

    def __api_read(self, char, data):
        self.__decoder.add(data)

    def __new_packet(self, packet: Packet):
        if packet.error != Packet.Error.success:
            raise CommandExecuteError('command execute error: ' + str(packet.error))
        print('response ' + ' '.join([hex(c) for c in packet.build()]))
        with self.__cv:
            self.__packets[packet.id] = packet
            self.__cv.notify_all()


@dataclass
class ToySensor:
    bit: int
    min_value: float
    max_value: float
    modifier: str = None
