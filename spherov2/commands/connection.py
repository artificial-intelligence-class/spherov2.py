from enum import IntEnum

from spherov2.commands import Commands


class BleCentralStates(IntEnum):
    NOT_YET_INITIALIZED = 0
    DISCONNECTED = 1
    SCANNING = 2
    CONNECTING = 3
    RECONNECTING = 4
    CONNECTED = 5
    DISCONNECTING = 6
    CONFIGURING = 7


class BleCentralStates(IntEnum):
    NOT_YET_INITIALIZED = 0
    DISCONNECTED = 1
    SCANNING = 2
    CONNECTING = 3
    RECONNECTING = 4
    CONNECTED = 5
    DISCONNECTING = 6
    CONFIGURING = 7


class BleCentralStates(IntEnum):
    NOT_YET_INITIALIZED = 0
    DISCONNECTED = 1
    SCANNING = 2
    CONNECTING = 3
    RECONNECTING = 4
    CONNECTED = 5
    DISCONNECTING = 6
    CONFIGURING = 7


class Connection(Commands):
    _did = 25

    @staticmethod
    def set_bluetooth_name(toy, name: bytes, proc=None):
        toy._execute(Connection._encode(toy, 3, proc, [*name, 0]))

    @staticmethod
    def get_bluetooth_name(toy, proc=None):
        return toy._execute(Connection._encode(toy, 4, proc)).data.rstrip(b'\0')

    @staticmethod
    def get_bluetooth_advertising_name(toy, proc=None):
        return toy._execute(Connection._encode(toy, 5, proc)).data.rstrip(b'\0')
