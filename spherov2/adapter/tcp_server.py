import asyncio
import struct
import sys
from typing import Optional

import bleak

from spherov2.adapter.tcp_consts import RequestOp, ResponseOp
from spherov2.helper import to_bytes, to_int
from spherov2.toy.consts import ServicesUUID


async def process_connection(reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter):
    peer = writer.get_extra_info('peername')

    def callback(char, d):
        if writer.is_closing():
            return
        writer.write(ResponseOp.ON_DATA + char.encode('ascii') + b'\0' + to_bytes(len(d), 1) + d)
        asyncio.ensure_future(writer.drain())

    print('Incoming connection from %s:%d' % peer)
    adapter: Optional[bleak.BleakClient] = None

    try:
        while True:
            cmd = await reader.readexactly(1)
            if cmd == RequestOp.SCAN:
                timeout = struct.unpack('f', await reader.readexactly(4))[0]
                try:
                    toys = await bleak.discover(timeout, filters={'UUIDs': [e.value for e in ServicesUUID]})
                except BaseException as e:
                    writer.write(ResponseOp.ERROR + str(e).encode('utf_8') + b'\0')
                    await writer.drain()
                    continue
                writer.write(ResponseOp.OK + to_bytes(len(toys), 2))
                await writer.drain()
                for toy in toys:
                    name = toy.name.encode('utf_8')
                    addr = toy.address.encode('ascii')
                    writer.write(name + b'\0' + addr + b'\0')
                    await writer.drain()
            elif cmd == RequestOp.END:
                break
            else:
                seq = (await reader.readexactly(1))[0]
                data = (await reader.readuntil(b'\0'))[:-1].decode('ascii')
                try:
                    if cmd == RequestOp.INIT:
                        adapter = bleak.BleakClient(data)
                        await adapter.connect()
                    elif cmd == RequestOp.SET_CALLBACK:
                        await adapter.start_notify(data, callback)
                    elif cmd == RequestOp.WRITE:
                        size = to_int(await reader.readexactly(2))
                        payload = bytearray(await reader.readexactly(size))
                        await adapter.write_gatt_char(data, payload, True)
                except EOFError:
                    raise
                except BaseException as e:
                    writer.write(ResponseOp.ERROR + str(e).encode('utf_8') + b'\0' + bytes([seq]))
                    await writer.drain()
                    continue
                writer.write(ResponseOp.OK + bytes([seq]))
                await writer.drain()
    finally:
        writer.close()
        if adapter and await adapter.is_connected():
            await adapter.disconnect()
        await writer.wait_closed()
        print('Disconnected from %s:%d' % peer)


if __name__ == '__main__':
    address = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50004
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(asyncio.start_server(process_connection, host=address, port=port))
    print('Server listening on %s:%d...' % (address, port))
    loop.run_until_complete(server.wait_closed())
