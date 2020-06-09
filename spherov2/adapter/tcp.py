import socket
from typing import NamedTuple

from spherov2.helper import to_int


class MockDevice(NamedTuple):
    name: str
    address: str


def get_tcp_adapter(address: str, port: int = 50004):
    class TCPAdapter:  # TODO
        @staticmethod
        def scan_toys():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, port))
            s.sendall(b'\x00')
            num_devices = to_int(s.recv(2))
            devices = []
            for _ in range(num_devices):
                name_size = to_int(s.recv(2))
                name = s.recv(name_size).decode('utf_8')
                addr = s.recv(2 * 6 + 5).decode('ascii')
                devices.append(MockDevice(name, addr))
            return devices

        def __init__(self, mac_address):
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((address, port))
            self.__socket.sendall(bytes('\x01') + mac_address.encode('ascii'))

        def close(self):
            ...

        def set_callback(self, uuid, cb):
            ...

        def write(self, uuid, data):
            ...

    return TCPAdapter
