from enum import IntFlag, IntEnum
from functools import partial

from spherov2.packet import Packet


class PendingUpdateFlags(IntFlag):
    nordic = 0b1
    st = 0b10
    esp2886 = 0b100
    audio = 0b1000
    animations = 0b10000
    st_bootloader = 0b100000


class ApplicationIds(IntEnum):
    BOOTLOADER = 0
    MAIN_APP = 1


class ResetStrategies(IntEnum):
    RESET_INTO_OR_JUMP_TO_MAIN_APP = 1
    RESET_INTO_OR_JUMP_TO_BOOTLOADER = 2


class Firmware:
    __encode = partial(Packet, device_id=29)

    @staticmethod
    def get_pending_update_flags(target_id=None):
        return Firmware.__encode(command_id=13, target_id=target_id)

    @staticmethod
    def get_current_application_id(target_id=None):
        return Firmware.__encode(command_id=21, target_id=target_id)

    @staticmethod
    def get_all_updatable_processors(target_id=None):
        return Firmware.__encode(command_id=22, target_id=target_id)

    @staticmethod
    def get_version_for_updatable_processors(target_id=None):
        return Firmware.__encode(command_id=24, target_id=target_id)

    @staticmethod
    def set_pending_update_for_processors(data, target_id=None):
        return Firmware.__encode(command_id=26, data=data, target_id=target_id)

    @staticmethod
    def get_pending_update_for_processors(target_id=None):
        return Firmware.__encode(command_id=27, target_id=target_id)

    @staticmethod
    def reset_with_parameters(strategy, target_id=None):
        return Firmware.__encode(command_id=28, data=[strategy], target_id=target_id)

    @staticmethod
    def clear_pending_update_processors(data, target_id=None):
        return Firmware.__encode(command_id=38, data=data, target_id=target_id)
