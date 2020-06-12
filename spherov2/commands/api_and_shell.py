from functools import partial

from spherov2.packet import Packet


class APIAndShell:
    __encode = partial(Packet, device_id=16)

    @staticmethod
    def ping(data, target_id=None):
        return APIAndShell.__encode(command_id=0, data=data, target_id=target_id)
