import struct
import asyncio
from typing import NamedTuple

from spherov2.adapter.tcp_consts import RequestOp, ResponseOp
from spherov2.helper import to_int, to_bytes


class MockDevice(NamedTuple):
    name: str
    address: str


def recvall(s, size):
    data = bytes()
    while len(data) < size:
        n = s.recv(size - len(data))
        if not n:
            raise EOFError
        data += n
    return data


def get_tcp_adapter(host: str, port: int = 50004):
    """Gets an anonymous ``TCPAdapter`` with the given address and port."""

    class TCPAdapter:
        @staticmethod
        async def scan_toys(timeout=5.0):
            reader, writer = await asyncio.open_connection(host, port)
            try:
                writer.write(RequestOp.SCAN + struct.pack('!f', timeout))
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

        @staticmethod
        async def scan_toy(name: str, timeout: float = 5.0):
            name = name.encode('utf_8')
            reader, writer = await asyncio.open_connection(host, port)
            try:
                writer.write(RequestOp.FIND + to_bytes(len(name), 2) +
                          name + struct.pack('!f', timeout))
                await writer.drain()
                code = await reader.readexactly(1)
                if code == ResponseOp.ERROR:
                    data = (await reader.readuntil(b'\0'))[:-1]
                    raise Exception(data.decode('utf_8'))
                elif code != ResponseOp.OK:
                    raise SystemError(f'Unexpected response op code {code}')
                name = (await reader.readuntil(b'\0'))[:-1].decode('utf_8')
                address = (await reader.readuntil(b'\0'))[:-1].decode('ascii')
                return MockDevice(name, address)
            finally:
                writer.write(RequestOp.END)
                await writer.drain()
                writer.close()
                await writer.wait_closed()

        def __init__(self, address):
            address = address.encode('ascii')

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
                except:
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
            if not self.__thread.is_alive():
                raise ConnectionError('Connection is lost')
            seq = self.__sequence
            self.__sequence = (self.__sequence + 1) % 0x100
            f = self.__sequence_wait[seq] = asyncio.futures.Future()
            self.__writer.write(cmd + bytes([seq]) + payload)
            await self.__writer.drain()
            await f

        async def close(self):
            # self.__socket.sendall(RequestOp.END)
            # self.__socket.close()
            # self.__thread.join()
            self.__writer.write(RequestOp.END)
            await self.__writer.drain()
            self.__writer.close()
            await self.__writer.wait_closed()

        async def set_callback(self, uuid, cb):
            if uuid in self.__callbacks:
                self.__callbacks[uuid].add(cb)
            else:
                self.__callbacks[uuid] = {cb}
                buf = uuid.encode('ascii')
                await self.__send(RequestOp.SET_CALLBACK,
                            to_bytes(len(buf), 2) + buf)

        async def write(self, uuid, data):
            uuid = uuid.encode('ascii')
            await self.__send(RequestOp.WRITE, to_bytes(len(uuid), 2) +
                        uuid + to_bytes(len(data), 2) + data)

    return TCPAdapter
