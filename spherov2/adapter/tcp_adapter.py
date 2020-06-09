import socket
import struct
import threading
from typing import NamedTuple

from spherov2.adapter.tcp_helper import recvall
from spherov2.helper import to_int, to_bytes


class MockDevice(NamedTuple):
    name: str
    address: str


def get_tcp_adapter(address: str, port: int = 50004):
    class TCPAdapter:  # TODO
        @staticmethod
        def scan_toys(timeout=5.0):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, port))
            s.sendall(b'\x00' + struct.pack('f', timeout))
            num_devices = to_int(recvall(s, 2))
            devices = []
            for _ in range(num_devices):
                name_size = to_int(recvall(s, 2))
                name = recvall(s, name_size).decode('utf_8')
                address_size = to_int(recvall(s, 2))
                addr = recvall(s, address_size).decode('ascii')
                devices.append(MockDevice(name, addr))
            s.sendall(b'\xff')
            s.close()
            return devices

        def __init__(self, mac_address):
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((address, port))
            mac_address = mac_address.encode('ascii')
            self.__socket.sendall(b'\x01' + to_bytes(len(mac_address), 2) + mac_address)

            self.__callbacks = {}
            self.__thread = threading.Thread(target=self.__recv)
            self.__thread.start()

        def __recv(self):
            while True:
                code = self.__socket.recv(1)
                if code == b'\x00':
                    continue
                size = self.__socket.recv(2)
                data = recvall(self.__socket, size)
                if code == b'\x01':
                    uuid = data.decode('ascii')
                    size = self.__socket.recv(1)
                    data = recvall(self.__socket, size)
                    if uuid in self.__callbacks:
                        for f in self.__callbacks[uuid]:
                            threading.Thread(target=f, args=(uuid, data)).start()
                elif code == b'\x02':
                    raise Exception(data.decode('utf_8'))

        def close(self):
            self.__socket.sendall(b'\xff')
            self.__socket.close()
            self.__thread.join()

        def set_callback(self, uuid, cb):
            if uuid in self.__callbacks:
                self.__callbacks[uuid].add(cb)
            else:
                self.__callbacks[uuid] = set([cb])
                buf = uuid.encode('ascii')
                self.__socket.sendall(b'\x02' + to_bytes(len(buf), 2) + buf)

        def write(self, uuid, data):
            uuid = uuid.encode('ascii')
            self.__socket.sendall(b'\x03' + to_bytes(len(uuid), 2) + uuid + to_bytes(len(data), 2) + bytes(data))

    return TCPAdapter
