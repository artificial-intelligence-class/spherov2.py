import asyncio
import struct
import sys
from typing import Optional

import bleak

from spherov2.adapter.tcp_consts import RequestOp, ResponseOp
from spherov2.helper import to_bytes, to_int


async def process_connection(reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter):
    peer = writer.get_extra_info('peername')

    def callback(char, d):
        if writer.is_closing():
            return
        char = char.encode('ascii')
        writer.write(ResponseOp.ON_DATA + to_bytes(len(char), 2) + char + to_bytes(len(d), 1) + d)
        asyncio.ensure_future(writer.drain())

    print('Incoming connection from %s:%d' % peer)
    adapter: Optional[bleak.BleakClient] = None

    try:
        while True:
            cmd = await reader.readexactly(1)
            if cmd == RequestOp.SCAN:
                timeout = struct.unpack('!f', await reader.readexactly(4))[0]
                try:
                    toys = await bleak.discover(timeout)
                except BaseException as e:
                    err = str(e)[:0xffff].encode('utf_8')
                    writer.write(ResponseOp.ERROR + to_bytes(len(err), 2) + err)
                    await writer.drain()
                    continue
                writer.write(ResponseOp.OK + to_bytes(len(toys), 2))
                await writer.drain()
                for toy in toys:
                    name = toy.name.encode('utf_8')
                    addr = toy.address.encode('ascii')
                    writer.write(to_bytes(len(name), 2) + name + to_bytes(len(addr), 2) + addr)
                    await writer.drain()
            elif cmd == RequestOp.END:
                break
            else:
                seq_size = await reader.readexactly(3)
                seq, size = seq_size[0], to_int(seq_size[1:])
                data = (await reader.readexactly(size)).decode('ascii')
                try:
                    if cmd == RequestOp.INIT:
                        adapter = bleak.BleakClient(data, timeout=5.0)
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
                    err = str(e)[:0xffff].encode('utf_8')
                    writer.write(ResponseOp.ERROR + to_bytes(len(err), 2) + err + bytes([seq]))
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
