import socket
import struct
import sys
import threading

from spherov2.adapter.bleak_adapter import BleakAdaptor
from spherov2.adapter.tcp_helper import recvall
from spherov2.helper import to_bytes, to_int


def process_socket(conn: socket.socket, addr):
    print('Incoming connection from %s:%d' % addr)
    with conn:
        def callback(char, data):
            char = char.encode('ascii')
            conn.sendall('\x01' + to_bytes(len(char), 2) + char + to_bytes(len(data), 1) + data)

        while True:
            cmd = recvall(conn, 1)
            adapter: BleakAdaptor = None
            if cmd == b'\x00':
                timeout = struct.unpack('f', recvall(conn, 4))[0]
                toys = BleakAdaptor.scan_toys(timeout=timeout)
                conn.sendall(to_bytes(len(toys), 2))
                for toy in toys:
                    name = toy.name.encode('utf_8')
                    address = toy.address.encode('ascii')
                    conn.sendall(to_bytes(len(name), 2) + name + to_bytes(len(address), 2) + address)
            elif cmd == b'\x01':
                size = to_int(recvall(conn, 2))
                mac_address = recvall(conn, size).decode('ascii')
                adapter = BleakAdaptor(mac_address)
            elif cmd == b'\x02':
                size = to_int(recvall(conn, 2))
                uuid = recvall(conn, size).decode('ascii')
                adapter.set_callback(uuid, callback)
            elif cmd == b'\x03':
                size = to_int(recvall(conn, 2))
                uuid = recvall(conn, size).decode('ascii')
                size = to_int(recvall(conn, 2))
                data = recvall(conn, size)
                adapter.write(uuid, data)
            else:
                break


if __name__ == '__main__':
    address = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50004
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((address, port))
        s.listen()
        print('Server listening on %s:%d...' % (address, port))
        while True:
            threading.Thread(target=process_socket, args=s.accept()).start()
