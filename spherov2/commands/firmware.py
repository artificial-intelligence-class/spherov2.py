from enum import IntFlag
from functools import partial

from spherov2.packet import Packet


class PendingUpdateFlags(IntFlag):
    nordic = 0b1
    st = 0b10
    esp2886 = 0b100
    audio = 0b1000
    animations = 0b10000
    st_bootloader = 0b100000


class Firmware:
    __encode = partial(Packet, device_id=29)

    @staticmethod
    def get_pending_update_flags(target_id=None):
        return Firmware.__encode(command_id=13, target_id=target_id)
