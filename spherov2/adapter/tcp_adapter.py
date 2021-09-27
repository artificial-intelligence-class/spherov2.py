import socket
import struct
import threading
from concurrent import futures
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
        def scan_toys(timeout=5.0):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            try:
                s.sendall(RequestOp.SCAN + struct.pack('!f', timeout))
                code = recvall(s, 1)
                if code == ResponseOp.ERROR:
                    size = to_int(recvall(s, 2))
                    data = recvall(s, size)
                    raise Exception(data.decode('utf_8'))
                elif code != ResponseOp.OK:
                    raise SystemError(f'Unexpected response op code {code}')
                num_devices = to_int(recvall(s, 2))
                devices = []
                for _ in range(num_devices):
                    name_size = to_int(recvall(s, 2))
                    name = recvall(s, name_size).decode('utf_8')
                    address_size = to_int(recvall(s, 2))
                    addr = recvall(s, address_size).decode('ascii')
                    devices.append(MockDevice(name, addr))
                return devices
            finally:
                s.sendall(RequestOp.END)
                s.close()

        def __init__(self, address):
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((host, port))
            address = address.encode('ascii')

            self.__sequence = 0
            self.__sequence_wait = {}

            self.__callbacks = {}
            self.__thread = threading.Thread(target=self.__recv)
            self.__thread.start()
            try:
                self.__send(RequestOp.INIT, to_bytes(len(address), 2) + address)
            except:
                self.close()
                raise

        def __recv(self):
            while True:
                try:
                    code = recvall(self.__socket, 1)
                except:
                    break
                if code == ResponseOp.OK:
                    self.__sequence_wait.pop(recvall(self.__socket, 1)[0]).set_result(None)
                    continue
                size = to_int(recvall(self.__socket, 2))
                data = recvall(self.__socket, size)
                if code == ResponseOp.ON_DATA:
                    uuid = data.decode('ascii').lower()
                    size = recvall(self.__socket, 1)[0]
                    data = recvall(self.__socket, size)
                    for f in self.__callbacks.get(uuid, []):
                        f(uuid, data)
                elif code == ResponseOp.ERROR:
                    err = Exception(data.decode('utf_8'))
                    self.__sequence_wait.pop(recvall(self.__socket, 1)[0]).set_exception(err)

        def __send(self, cmd, payload):
            if not self.__thread.is_alive():
                raise ConnectionError('Connection is lost')
            seq = self.__sequence
            self.__sequence = (self.__sequence + 1) % 0x100
            f = self.__sequence_wait[seq] = futures.Future()
            self.__socket.sendall(cmd + bytes([seq]) + payload)
            f.result()

        def close(self):
            self.__socket.sendall(RequestOp.END)
            self.__socket.close()
            self.__thread.join()

        def set_callback(self, uuid, cb):
            if uuid in self.__callbacks:
                self.__callbacks[uuid].add(cb)
            else:
                self.__callbacks[uuid] = {cb}
                buf = uuid.encode('ascii')
                self.__send(RequestOp.SET_CALLBACK, to_bytes(len(buf), 2) + buf)

        def write(self, uuid, data):
            uuid = uuid.encode('ascii')
            self.__send(RequestOp.WRITE, to_bytes(len(uuid), 2) + uuid + to_bytes(len(data), 2) + data)

    return TCPAdapter
