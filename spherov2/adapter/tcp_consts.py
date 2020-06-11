from enum import Enum


class RequestOp(bytes, Enum):
    SCAN = b'\x00'
    INIT = b'\x01'
    SET_CALLBACK = b'\x02'
    WRITE = b'\x03'
    END = b'\xff'


class ResponseOp(bytes, Enum):
    OK = b'\x00'
    ON_DATA = b'\x01'
    ERROR = b'\xff'
