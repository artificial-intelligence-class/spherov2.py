from functools import partial

from spherov2.packet import Packet


class Connection:
    __encode = partial(Packet, device_id=25)

    @staticmethod
    def set_bluetooth_name(name: bytes, target_id=None):
        return Connection.__encode(command_id=3, data=[*name, 0], target_id=target_id)

    @staticmethod
    def get_bluetooth_name(target_id=None):
        return Connection.__encode(command_id=4, target_id=target_id)
