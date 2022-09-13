import asyncio
import threading

import bleak


class BleakAdapter:
    @staticmethod
    def scan_toys(timeout: float = 5.0):
        return asyncio.run(bleak.BleakScanner.discover(timeout))

    def __init__(self, address):
        self.__event_loop = asyncio.new_event_loop()
        self.__device = bleak.BleakClient(address, timeout=5.0)
        self.__lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__event_loop.run_forever)
        self.__thread.start()
        try:
            self.__execute(self.__device.connect())
        except:
            self.close(False)
            raise

    def __execute(self, coroutine):
        with self.__lock:
            return asyncio.run_coroutine_threadsafe(coroutine, self.__event_loop).result()

    def close(self, disconnect=True):
        if disconnect:
            self.__execute(self.__device.disconnect())
        with self.__lock:
            self.__event_loop.call_soon_threadsafe(self.__event_loop.stop)
            self.__thread.join()
        self.__event_loop.close()

    def set_callback(self, uuid, cb):
        self.__execute(self.__device.start_notify(uuid, cb))

    def write(self, uuid, data):
        self.__execute(self.__device.write_gatt_char(uuid, data, True))
