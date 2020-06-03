import asyncio
import threading
import bleak

from spherov2.toy.types import ServicesUUID


class BleakAdaptor:
    @staticmethod
    def scan_toys(timeout: float = 5.0):
        return asyncio.run(bleak.discover(timeout, filters={'UUIDs': [e.value for e in ServicesUUID]}))

    def __init__(self, mac_address):
        self.__event_loop = asyncio.new_event_loop()
        self.__device = bleak.BleakClient(mac_address, self.__event_loop)
        self.__thread = threading.Thread(target=self.__event_loop.run_forever)
        self.__thread.start()
        asyncio.run_coroutine_threadsafe(self.__device.connect(), self.__event_loop).result()

    def close(self):
        asyncio.run_coroutine_threadsafe(self.__device.disconnect(), self.__event_loop).result()
        self.__event_loop.call_soon_threadsafe(self.__event_loop.stop)
        self.__thread.join()
        self.__event_loop.close()

    def set_callback(self, uuid, cb):
        return asyncio.run_coroutine_threadsafe(self.__device.start_notify(uuid, cb), self.__event_loop).result()

    def write(self, uuid, data):
        return asyncio.run_coroutine_threadsafe(self.__device.write_gatt_char(uuid, bytearray(data), True),
                                                self.__event_loop).result()
