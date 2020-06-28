from enum import IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class SosMessages(IntEnum):
    UNKNOWN = 0
    SUBPROCESSOR_CRASHED = 1


class BootReasons(IntEnum):
    COLD_BOOT = 0
    UNEXPECTED_RESET = 1
    APPLICATION_RESET_DUE_TO_ERROR = 2
    APPLICATION_RESET_FOR_A_FIRMWARE_UPDATE = 3
    PROCESSOR_IS_BOOTING_FROM_SLEEP = 4
    PROCESSOR_IS_RESETTING_FOR_SOME_NON_ERROR_REASON = 5


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
    def get_boot_reason(target_id=None):
        return SystemInfo.__encode(command_id=32, target_id=target_id)

    @staticmethod
    def get_last_error_info(target_id=None):
        return SystemInfo.__encode(command_id=33, target_id=target_id)

    @staticmethod
    def get_secondary_mcu_bootloader_version(target_id=None):
        return SystemInfo.__encode(command_id=36, target_id=target_id)

    secondary_mcu_bootloader_version_notify = (17, 37, 0xff)

    @staticmethod
    def get_three_character_sku(target_id=None):
        return SystemInfo.__encode(command_id=40, target_id=target_id)

    @staticmethod
    def write_config_block(target_id=None):
        return SystemInfo.__encode(command_id=43, target_id=target_id)

    @staticmethod
    def get_config_block(target_id=None):
        return SystemInfo.__encode(command_id=44, target_id=target_id)

    @staticmethod
    def set_config_block(metadata_version, config_block_version, application_data, target_id=None):
        return SystemInfo.__encode(
            command_id=45,
            data=[*to_bytes(metadata_version, 4), *to_bytes(config_block_version, 4), *application_data],
            target_id=target_id
        )

    @staticmethod
    def erase_config_block(j, target_id=None):
        return SystemInfo.__encode(command_id=46, data=to_bytes(j, 4), target_id=target_id)

    @staticmethod
    def get_swd_locking_status(target_id=None):
        return SystemInfo.__encode(command_id=48, target_id=target_id)

    @staticmethod
    def get_manufacturing_date(target_id=None):
        return SystemInfo.__encode(command_id=51, target_id=target_id)

    @staticmethod
    def get_sku(target_id=None):
        return SystemInfo.__encode(command_id=56, target_id=target_id)

    @staticmethod
    def get_core_up_time_in_milliseconds(target_id=None):
        return SystemInfo.__encode(command_id=57, target_id=target_id)

    @staticmethod
    def get_event_log_status(target_id=None):
        return SystemInfo.__encode(command_id=58, target_id=target_id)

    @staticmethod
    def get_event_log_data(j, j2, target_id=None):
        return SystemInfo.__encode(command_id=59, data=to_bytes(j, 4) + to_bytes(j2, 4), target_id=target_id)

    @staticmethod
    def clear_event_log(target_id=None):
        return SystemInfo.__encode(command_id=60, target_id=target_id)

    @staticmethod
    def enable_sos_message_notify(enable: bool, target_id=None):
        return SystemInfo.__encode(command_id=61, data=[int(enable)], target_id=target_id)

    sos_message_notify = (17, 62, 0xff)

    @staticmethod
    def get_sos_message(target_id=None):
        return SystemInfo.__encode(command_id=63, target_id=target_id)

    @staticmethod
    def clear_sos_message(target_id=None):
        return SystemInfo.__encode(command_id=68, target_id=target_id)
