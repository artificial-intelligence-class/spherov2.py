import threading
import time
from dataclasses import dataclass
from functools import cached_property
from queue import SimpleQueue

from spherov2.adapter.bleak import BleakAdaptor
from spherov2.packet import Packet, Collector
from spherov2.toy.consts import CharacteristicUUID
from spherov2.toy.types import ToyType


class CommandTimeoutException(Exception):
    ...


class CommandExecuteError(Exception):
    ...


class Toy:
    toy_type = ToyType('Robot', None, 'Sphero', .06)

    def __init__(self, mac_address, adapter_cls=BleakAdaptor):
        self.mac_address = mac_address

        self.__adapter = None
        self.__adapter_cls = adapter_cls
        self.__decoder = Collector(self.__new_packet)
        self.__packets = {}
        self.__cv = threading.Condition()

        self.__thread = threading.Thread(target=self.__process_packet)
        self.__packet_queue = SimpleQueue()

    def __enter__(self):
        if self.__adapter is not None:
            raise RuntimeError('Toy already in context manager')
        self.__adapter = self.__adapter_cls(self.mac_address)
        self.__adapter.set_callback(CharacteristicUUID.api_v2.value, self.__api_read)
        self.__adapter.write(CharacteristicUUID.anti_dos.value, b'usetheforce...band')
        self.__thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__adapter.close()
        self.__adapter = None
        self.__packet_queue.put(None)
        self.__thread.join()
        self.__packet_queue = SimpleQueue()

    def __process_packet(self):
        while self.__adapter is not None:
            payload = self.__packet_queue.get()
            if payload is None:
                break
            print('request ' + ' '.join([hex(c) for c in payload]))
            self.__adapter.write(CharacteristicUUID.api_v2.value, payload)
            time.sleep(self.toy_type.cmd_safe_interval)

    def _execute(self, packet: Packet) -> Packet:
        if self.__adapter is None:
            raise RuntimeError('Use toys in context manager')
        self.__packet_queue.put(packet.build())
        return self._wait_packet(packet.id)

    def _wait_packet(self, key, timeout=10.0):
        with self.__cv:
            if self.__cv.wait_for(lambda: key in self.__packets, timeout):
                packet = self.__packets[key]
                if packet.error != Packet.Error.success:
                    raise CommandExecuteError(packet.error)
                return packet
        raise CommandTimeoutException

    def __api_read(self, char, data):
        self.__decoder.add(data)

    def __new_packet(self, packet: Packet):
        print('response ' + ' '.join([hex(c) for c in packet.build()]))
        with self.__cv:
            self.__packets[packet.id] = packet
            self.__cv.notify_all()

    @cached_property
    def drive_control(self):
        raise NotImplementedError


@dataclass
class ToySensor:
    bit: int
    min_value: float
    max_value: float
    modifier: str = None
