import threading
import time
from collections import OrderedDict, defaultdict
from concurrent import futures
from functools import partial
from queue import SimpleQueue
from typing import NamedTuple, Callable

from spherov2.controls.v1 import Packet as PacketV1
from spherov2.controls.v2 import Packet as PacketV2
from spherov2.types import ToyType


class ToySensor(NamedTuple):
    bit: int
    min_value: float
    max_value: float
    modifier: Callable[[float], float] = None


class Toy:
    toy_type = ToyType('Robot', None, 'Sphero', .06)
    sensors = OrderedDict()
    extended_sensors = OrderedDict()

    _send_uuid = '22bb746f-2ba1-7554-2d6f-726568705327'
    _response_uuid = '22bb746f-2ba6-7554-2d6f-726568705327'
    _handshake = [('22bb746f-2bbd-7554-2d6f-726568705327', bytearray(b'011i3')),
                  ('22bb746f-2bb2-7554-2d6f-726568705327', bytearray([7]))]
    _packet = PacketV1
    _require_target = False

    def __init__(self, toy, adapter_cls):
        self.address = toy.address
        self.name = toy.name

        self.__adapter = None
        self.__adapter_cls = adapter_cls
        self._packet_manager = self._packet.Manager()
        self.__decoder = self._packet.Collector(self.__new_packet)
        self.__waiting = defaultdict(SimpleQueue)
        self.__listeners = defaultdict(dict)
        self._sensor_controller = None

        self.__thread = None
        self.__packet_queue = SimpleQueue()

    def __enter__(self):
        if self.__adapter is not None:
            raise RuntimeError('Toy already in context manager')
        self.__adapter = self.__adapter_cls(self.address)
        self.__thread = threading.Thread(target=self.__process_packet)
        try:
            for uuid, data in self._handshake:
                self.__adapter.write(uuid, data)
            self.__adapter.set_callback(self._response_uuid, self.__api_read)
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
            while payload:
                self.__adapter.write(self._send_uuid, payload[:20])
                payload = payload[20:]
            time.sleep(self.toy_type.cmd_safe_interval)

    def _execute(self, packet):
        if self.__adapter is None:
            raise RuntimeError('Use toys in context manager')
        self.__packet_queue.put(packet.build())
        return self._wait_packet(packet.id)

    def _wait_packet(self, key, timeout=10.0, check_error=False):
        future = futures.Future()
        self.__waiting[key].put(future)
        packet = future.result(timeout)
        if check_error:
            packet.check_error()
        return packet

    def _add_listener(self, key, listener: Callable):
        self.__listeners[key[0]][listener] = partial(key[1], listener)

    def _remove_listener(self, key, listener: Callable):
        self.__listeners[key[0]].pop(listener)

    def __api_read(self, char, data):
        self.__decoder.add(data)

    def __new_packet(self, packet):
        # print('response ' + ' '.join([hex(c) for c in packet.build()]))
        key = packet.id
        queue = self.__waiting[key]
        while not queue.empty():
            queue.get().set_result(packet)
        for f in self.__listeners[key].values():
            threading.Thread(target=f, args=(packet,)).start()

    @classmethod
    def implements(cls, method, with_target=False):
        m = getattr(cls, method.__name__, None)
        if m is method:
            return with_target == cls._require_target
        if hasattr(m, '_partialmethod'):
            f = m._partialmethod
            return f.func is method and (
                    ('proc' in f.keywords and not with_target) or with_target == cls._require_target)
        return False


class ToyV2(Toy):
    _packet = PacketV2
    _handshake = []

    _response_uuid = _send_uuid = '00010002-574f-4f20-5370-6865726f2121' #Original
    #_response_uuid = '22bb746f-2ba6-7554-2d6f-726568705327'
    #_send_uuid =     '22bb746f-2ba1-7554-2d6f-726568705327'
    #_send_uuid =     '00010002-574f-4f20-5370-6865726f2121'
    #_response_uuid = '00020002-574f-4f20-5370-6865726f2121'

    # _response_uuid = _send_uuid = '00010001-574f-4f20-5370-6865726f2121' #Available responses
    # _response_uuid = _send_uuid = '00010002-574f-4f20-5370-6865726f2121'
    # _response_uuid = _send_uuid = '00010003-574f-4f20-5370-6865726f2121'
    # _response_uuid = _send_uuid = '00020001-574f-4f20-5370-6865726f2121'
    # _response_uuid = _send_uuid = '00020002-574f-4f20-5370-6865726f2121'
    # _response_uuid = _send_uuid = '00020004-574f-4f20-5370-6865726f2121'
    # _response_uuid = _send_uuid = '00020005-574f-4f20-5370-6865726f2121'
    # _response_uuid = _send_uuid = '22bb746f-2bbd-7554-2d6f-726568705327'
    # _response_uuid = _send_uuid = '22bb746f-2bb2-7554-2d6f-726568705327'
    # _response_uuid = _send_uuid = '22bb746f-2bbf-7554-2d6f-726568705327'
    # _response_uuid = _send_uuid = '22bb746f-2ba0-7554-2d6f-726568705327'
    # _response_uuid = _send_uuid = '22bb746f-2ba1-7554-2d6f-726568705327'
    # _response_uuid = _send_uuid = '22bb746f-2ba6-7554-2d6f-726568705327'
    # _response_uuid = _send_uuid = '22bb746f-2bb0-7554-2d6f-726568705327'

#Some values found in apk - should revisit what values may be per robot
#Adaptor.BLEService = "22bb746f2bb075542d6f726568705327";
#Adaptor.WakeCharacteristic = "22bb746f2bbf75542d6f726568705327";
#Adaptor.TXPowerCharacteristic = "22bb746f2bb275542d6f726568705327";
#Adaptor.AntiDosCharacteristic = "22bb746f2bbd75542d6f726568705327";
#Adaptor.RobotControlService = "22bb746f2ba075542d6f726568705327";
#Adaptor.CommandsCharacteristic = "22bb746f2ba175542d6f726568705327";
#Adaptor.ResponseCharacteristic = "22bb746f2ba675542d6f726568705327";