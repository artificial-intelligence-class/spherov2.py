import socket
import struct
import sys
import threading

from spherov2.adapter.bleak_adapter import BleakAdaptor
from spherov2.adapter.tcp_helper import recvall, RequestOp, ResponseOp
from spherov2.helper import to_bytes, to_int


def process_socket(conn: socket.socket, addr):
    print('Incoming connection from %s:%d' % addr)
    with conn:
        def callback(char, d):
            char = char.encode('ascii')
            conn.sendall(ResponseOp.ON_DATA + to_bytes(len(char), 2) + char + to_bytes(len(d), 1) + d)

        adapter: BleakAdaptor = None
        try:
            while True:
                cmd = recvall(conn, 1)
                if cmd == RequestOp.SCAN:
                    timeout = struct.unpack('f', recvall(conn, 4))[0]
                    try:
                        toys = BleakAdaptor.scan_toys(timeout=timeout)
                    except BaseException as e:
                        err = str(e)[:0xffff].encode('utf_8')
                        conn.sendall(ResponseOp.ERROR + to_bytes(len(err), 2) + err)
                        continue
                    conn.sendall(ResponseOp.OK + to_bytes(len(toys), 2))
                    for toy in toys:
                        name = toy.name.encode('utf_8')
                        addr = toy.address.encode('ascii')
                        conn.sendall(to_bytes(len(name), 2) + name + to_bytes(len(addr), 2) + addr)
                elif cmd == RequestOp.END:
                    break
                else:
                    seq_size = recvall(conn, 3)
                    seq, size = seq_size[0], to_int(seq_size[1:])
                    data = recvall(conn, size).decode('ascii')
                    try:
                        if cmd == RequestOp.INIT:
                            adapter = BleakAdaptor(data)
                        elif cmd == RequestOp.SET_CALLBACK:
                            adapter.set_callback(data, callback)
                        elif cmd == RequestOp.WRITE:
                            size = to_int(recvall(conn, 2))
                            payload = recvall(conn, size)
                            adapter.write(data, payload)
                        conn.sendall(ResponseOp.OK + bytes([seq]))
                    except EOFError:
                        raise
                    except BaseException as e:
                        err = str(e)[:0xffff].encode('utf_8')
                        conn.sendall(ResponseOp.ERROR + to_bytes(len(err), 2) + err + bytes([seq]))
        finally:
            if adapter:
                adapter.close()


if __name__ == '__main__':
    address = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50004
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((address, port))
        s.listen()
        print('Server listening on %s:%d...' % (address, port))
        while True:
            threading.Thread(target=process_socket, args=s.accept()).start()
