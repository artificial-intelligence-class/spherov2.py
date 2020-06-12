import asyncio
import struct
from typing import NamedTuple

from spherov2.adapter.tcp_consts import RequestOp, ResponseOp
from spherov2.helper import to_int, to_bytes


class MockDevice(NamedTuple):
    name: str
    address: str


def get_tcp_adapter(host: str = 'localhost', port: int = 50004):
    class TCPAdapter:
        @staticmethod
        async def scan_toys(timeout=5.0):
            reader, writer = await asyncio.open_connection(host, port)
            try:
                writer.write(RequestOp.SCAN + struct.pack('f', timeout))
                await writer.drain()
                code = await reader.readexactly(1)
                if code == ResponseOp.ERROR:
                    data = (await reader.readuntil(b'\0'))[:-1]
                    raise Exception(data.decode('utf_8'))
                elif code != ResponseOp.OK:
                    raise SystemError(f'Unexpected response op code {code}')
                num_devices = to_int(await reader.readexactly(2))
                devices = []
                for _ in range(num_devices):
                    name = (await reader.readuntil(b'\0'))[:-1].decode('utf_8')
                    address = (await reader.readuntil(b'\0'))[:-1].decode('ascii')
                    devices.append(MockDevice(name, address))
                return devices
            finally:
                writer.write(RequestOp.END)
                await writer.drain()
                writer.close()
                await writer.wait_closed()

        def __init__(self, address):
            self.__address = address
            self.__reader = None
            self.__writer = None
            self.__sequence = 0
            self.__sequence_wait = {}
            self.__callbacks = {}

        async def connect(self):
            self.__reader, self.__writer = await asyncio.open_connection(host, port)
            asyncio.ensure_future(self.__recv())
            try:
                await self.__send(RequestOp.INIT, self.__address.encode('ascii') + b'\0')
            except:
                await self.disconnect()
                raise

        async def __recv(self):
            while True:
                try:
                    code = await self.__reader.readexactly(1)
                except EOFError:
                    break
                if code == ResponseOp.OK:
                    self.__sequence_wait.pop((await self.__reader.readexactly(1))[0]).set_result(None)
                    continue
                data = (await self.__reader.readuntil(b'\0'))[:-1]
                if code == ResponseOp.ON_DATA:
                    uuid = data.decode('ascii').lower()
                    size = (await self.__reader.readexactly(1))[0]
                    data = await self.__reader.readexactly(size)
                    for f in self.__callbacks.get(uuid, []):
                        f(uuid, data)
                elif code == ResponseOp.ERROR:
                    err = Exception(data.decode('utf_8'))
                    self.__sequence_wait.pop((await self.__reader.readexactly(1))[0]).set_exception(err)

        async def __send(self, cmd, payload):
            if self.__writer.is_closing():
                raise ConnectionError('Connection is closing')
            seq = self.__sequence
            self.__sequence = (self.__sequence + 1) % 0x100
            f = self.__sequence_wait[seq] = asyncio.futures.Future()
            self.__writer.write(cmd + bytes([seq]) + payload)
            await self.__writer.drain()
            await f

        async def disconnect(self):
            self.__writer.write(RequestOp.END)
            await self.__writer.drain()
            self.__writer.close()
            await self.__writer.wait_closed()

        async def start_notify(self, uuid, cb):
            if uuid in self.__callbacks:
                self.__callbacks[uuid].add(cb)
            else:
                self.__callbacks[uuid] = {cb}
                await self.__send(RequestOp.SET_CALLBACK, uuid.encode('ascii') + b'\0')

        async def write(self, uuid, data):
            await self.__send(RequestOp.WRITE, uuid.encode('ascii') + b'\0' + to_bytes(len(data), 2) + bytes(data))

    return TCPAdapter
