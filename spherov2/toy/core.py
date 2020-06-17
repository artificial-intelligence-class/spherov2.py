import threading
import time
from collections import defaultdict, OrderedDict
from concurrent import futures
from dataclasses import dataclass
from queue import SimpleQueue
from typing import Callable

from spherov2.packet import Packet, Collector
from spherov2.toy.consts import CharacteristicUUID
from spherov2.types import ToyType


class CommandExecuteError(Exception):
    ...


@dataclass
class ToySensor:
    bit: int
    min_value: float
    max_value: float
    modifier: Callable[[float], float] = None


class Toy:
    toy_type = ToyType('Robot', None, 'Sphero', .06)
    sensors = OrderedDict()
    extended_sensors = OrderedDict()

    def __init__(self, toy, adapter_cls):
        self.address = toy.address
        self.name = toy.name

        self.__adapter = None
        self.__adapter_cls = adapter_cls
        self.__decoder = Collector(self.__new_packet)
        self.__waiting = defaultdict(SimpleQueue)
        self.__listeners = defaultdict(set)

        self.__thread = None
        self.__packet_queue = SimpleQueue()

    def __enter__(self):
        if self.__adapter is not None:
            raise RuntimeError('Toy already in context manager')
        self.__adapter = self.__adapter_cls(self.address)
        self.__thread = threading.Thread(target=self.__process_packet)
        try:
            self.__adapter.set_callback(CharacteristicUUID.api_v2.value, self.__api_read)
            self.__adapter.write(CharacteristicUUID.anti_dos.value, b'usetheforce...band')
            self.__thread.start()
        except:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__adapter.close()
        self.__adapter = None
        if self.__thread.is_alive():
            self.__packet_queue.put(None)
            self.__thread.join()
        self.__packet_queue = SimpleQueue()

    def __process_packet(self):
        while self.__adapter is not None:
            payload = self.__packet_queue.get()
            if payload is None:
                break
            # print('request ' + ' '.join([hex(c) for c in payload]))
            self.__adapter.write(CharacteristicUUID.api_v2.value, payload)
            time.sleep(self.toy_type.cmd_safe_interval)

    def _execute(self, packet: Packet) -> Packet:
        if self.__adapter is None:
            raise RuntimeError('Use toys in context manager')
        self.__packet_queue.put(packet.build())
        return self._wait_packet(packet.id)

    def _wait_packet(self, key, timeout=10.0):
        future = futures.Future()
        self.__waiting[key].put(future)
        packet = future.result(timeout)
        if packet.error != Packet.Error.success:
            raise CommandExecuteError(packet.error)
        return packet

    def _add_listener(self, key, notifier: Callable[[Packet], None]):
        self.__listeners[key].add(notifier)

    def _remove_listener(self, key, notifier: Callable):
        self.__listeners[key].remove(notifier)

    def __api_read(self, char, data):
        self.__decoder.add(data)

    def __new_packet(self, packet: Packet):
        # print('response ' + ' '.join([hex(c) for c in packet.build()]))
        key = packet.id
        queue = self.__waiting[key]
        while not queue.empty():
            queue.get().set_result(packet)
        for f in self.__listeners[key]:
            threading.Thread(target=f, args=(packet,)).start()
