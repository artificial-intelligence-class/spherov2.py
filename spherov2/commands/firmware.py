from enum import IntFlag, IntEnum

from spherov2.commands import Commands
from spherov2.helper import to_int


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


class Firmware(Commands):
    _did = 29

    @staticmethod
    def get_pending_update_flags(toy, proc=None):
        return PendingUpdateFlags(to_int(toy._execute(Firmware._encode(toy, 13, proc)).data))

    @staticmethod
    def get_current_application_id(toy, proc=None):
        return ApplicationIds(toy._execute(Firmware._encode(toy, 21, proc)).data[0])

    @staticmethod
    def get_all_updatable_processors(toy, proc=None):
        toy._execute(Firmware._encode(toy, 22, proc))

    @staticmethod
    def get_version_for_updatable_processors(toy, proc=None):
        toy._execute(Firmware._encode(toy, 24, proc))

    @staticmethod
    def set_pending_update_for_processors(toy, data, proc=None):  # unknown names
        return ResetStrategies(toy._execute(Firmware._encode(toy, 26, proc, data)).data[0])

    @staticmethod
    def get_pending_update_for_processors(toy, proc=None):
        return toy._execute(Firmware._encode(toy, 27, proc)).data

    @staticmethod
    def reset_with_parameters(toy, strategy, proc=None):
        toy._execute(Firmware._encode(toy, 28, proc, [strategy]))

    @staticmethod
    def clear_pending_update_processors(toy, data, proc=None):  # unknown names
        toy._execute(Firmware._encode(toy, 38, proc, data))
