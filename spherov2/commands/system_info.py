from functools import partial

from spherov2.packet import Packet


class SystemInfo:
    __encode = partial(Packet, device_id=17)

    @staticmethod
    def get_main_app_version(target_id=None):
        return SystemInfo.__encode(command_id=0, target_id=target_id)

    @staticmethod
    def get_bootloader_version(target_id=None):
        return SystemInfo.__encode(command_id=1, target_id=target_id)

    @staticmethod
    def get_board_revision(target_id=None):
        return SystemInfo.__encode(command_id=3, target_id=target_id)

    @staticmethod
    def get_mac_address(target_id=None):
        return SystemInfo.__encode(command_id=6, target_id=target_id)

    @staticmethod
    def get_stats_id(target_id=None):
        return SystemInfo.__encode(command_id=19, target_id=target_id)

    @staticmethod
    def get_secondary_main_app_version(target_id=None):
        return SystemInfo.__encode(command_id=23, target_id=target_id)

    secondary_main_app_version_notify = (17, 24, 0xff)

    @staticmethod
    def get_processor_name(target_id=None):
        return SystemInfo.__encode(command_id=31, target_id=target_id)

    @staticmethod
    def get_secondary_mcu_bootloader_version(target_id=None):
        return SystemInfo.__encode(command_id=36, target_id=target_id)

    secondary_mcu_bootloader_version_notify = (17, 37, 0xff)

    @staticmethod
    def get_three_character_sku(target_id=None):
        return SystemInfo.__encode(command_id=40, target_id=target_id)
