import asyncio
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from typing import Callable, Coroutine

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
        self.__waiting = defaultdict(list)
        self.__listeners = defaultdict(set)
        self.__packet_queue = asyncio.Queue()

    async def __aenter__(self):
        if self.__adapter is not None:
            raise RuntimeError('Toy already in context manager')
        self.__adapter = self.__adapter_cls(self.address)
        await self.__adapter.connect()
        asyncio.ensure_future(self.__process_packet())
        try:
            await self.__adapter.start_notify(CharacteristicUUID.api_v2.value, self.__api_read)
            await self.__adapter.write(CharacteristicUUID.anti_dos.value, b'usetheforce...band')
        except:
            await self.__aexit__(None, None, None)
            raise
        return self

    async def __aexit__(self, typ, val, tb):
        self.__packet_queue.put_nowait(None)
        await self.__packet_queue.join()
        await self.__adapter.disconnect()
        self.__adapter = None
        self.__packet_queue = asyncio.Queue()

    async def __process_packet(self):
        while self.__adapter is not None:
            try:
                payload = await self.__packet_queue.get()
            except:
                continue
            self.__packet_queue.task_done()
            if payload is None:
                break
            # print('request ' + ' '.join([hex(c) for c in payload]))
            await self.__adapter.write(CharacteristicUUID.api_v2.value, payload)
            await asyncio.sleep(self.toy_type.cmd_safe_interval)

    async def _execute(self, packet: Packet) -> Packet:
        if self.__adapter is None:
            raise RuntimeError('Use toys in context manager')
        self.__packet_queue.put_nowait(packet.build())
        return await self._wait_packet(packet.id)

    async def _wait_packet(self, key, timeout=10.0) -> Packet:
        future = asyncio.futures.Future()
        self.__waiting[key].append(future)
        packet = await asyncio.wait_for(future, timeout)
        if packet.error != Packet.Error.success:
            raise CommandExecuteError(packet.error)
        return packet

    def _add_listener(self, key, notifier: Callable[[Packet], Coroutine]):
        if not asyncio.iscoroutinefunction(notifier):
            raise ValueError(f'Notifier {notifier} is not a coroutine function')
        self.__listeners[key].add(notifier)

    def _remove_listener(self, key, notifier: Callable[[Packet], Coroutine]):
        self.__listeners[key].remove(notifier)

    def __api_read(self, char, data):
        self.__decoder.add(data)

    async def __new_packet(self, packet: Packet):
        # print('response ' + ' '.join([hex(c) for c in packet.build()]))
        key = packet.id
        queue = self.__waiting[key]
        while len(queue):
            queue.pop().set_result(packet)
        for f in self.__listeners[key]:
            asyncio.ensure_future(f(packet))
