import struct
from enum import IntEnum

from spherov2.commands import Commands
from spherov2.helper import to_bytes, to_int
from spherov2.listeners.system_info import Version, LastErrorInfo, ConfigBlock, ManufacturingDate, EventLogStatus


class ApplicationIndexes(IntEnum):
    BOOTLOADER = 0
    MAIN_APPLICATION = 1


class ConfigBlockWriteCodes(IntEnum):
    CS_SUCCESS = 0
    CB_BUSY = 1
    BC_FS_ERROR = 2


class DeviceModes(IntEnum):
    FACTORY_MODE = 0
    USER_PLAY_TEST_MODE = 1
    USER_OUT_OF_BOX_MODE = 2
    USER_FULL_MODE = 3


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


class SystemInfo(Commands):
    _did = 17

    @staticmethod
    def get_main_app_version(toy, proc=None):
        return Version(*struct.unpack('>3H', toy._execute(SystemInfo._encode(toy, 0, proc)).data))

    @staticmethod
    def get_bootloader_version(toy, proc=None):
        return Version(*struct.unpack('>3H', toy._execute(SystemInfo._encode(toy, 1, proc)).data))

    @staticmethod
    def get_board_revision(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 3, proc)).data[0]

    @staticmethod
    def get_mac_address(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 6, proc)).data

    @staticmethod
    def get_model_number(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 18, proc)).data

    @staticmethod
    def get_stats_id(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 19, proc)).data

    @staticmethod
    def get_secondary_main_app_version(toy, proc=None):
        toy._execute(SystemInfo._encode(toy, 23, proc))
        return Version(
            *struct.unpack('>3H', toy._wait_packet(SystemInfo.secondary_main_app_version_notify).data))

    secondary_main_app_version_notify = (17, 24, 0xff)

    @staticmethod
    def get_processor_name(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 31, proc)).data.rstrip(b'\0')

    @staticmethod
    def get_boot_reason(toy, proc=None):
        return BootReasons(toy._execute(SystemInfo._encode(toy, 32, proc)).data[0])

    @staticmethod
    def get_last_error_info(toy, proc=None):
        return LastErrorInfo(
            *struct.unpack('>32sH12s', toy._execute(SystemInfo._encode(toy, 33, proc)).data))

    @staticmethod
    def get_secondary_mcu_bootloader_version(toy, proc=None):
        toy._execute(SystemInfo._encode(toy, 36, proc))
        return Version(*struct.unpack('>3H', toy._wait_packet(SystemInfo.secondary_mcu_bootloader_version_notify).data))

    secondary_mcu_bootloader_version_notify = (17, 37, 0xff)

    @staticmethod
    def get_three_character_sku(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 40, proc)).data

    @staticmethod
    def write_config_block(toy, proc=None):
        toy._execute(SystemInfo._encode(toy, 43, proc))

    @staticmethod
    def get_config_block(toy, proc=None):
        data = toy._execute(SystemInfo.get_config_block(SystemInfo._encode(toy, 44, proc).data))
        return ConfigBlock(*struct.unpack('>2I', data[:8]), data[8:])

    @staticmethod
    def set_config_block(toy, metadata_version, config_block_version, application_data, proc=None):
        toy._execute(SystemInfo._encode(
            45, proc, [*to_bytes(metadata_version, 4), *to_bytes(config_block_version, 4), *application_data]))

    @staticmethod
    def erase_config_block(toy, j, proc=None):
        toy._execute(SystemInfo._encode(toy, 46, proc, to_bytes(j, 4)))

    @staticmethod
    def get_swd_locking_status(toy, proc=None):
        return bool(toy._execute(SystemInfo._encode(toy, 48, proc)).data[0])

    @staticmethod
    def get_manufacturing_date(toy, proc=None):
        return ManufacturingDate(
            *struct.unpack('>HBB', toy._execute(SystemInfo._encode(toy, 51, proc)).data))

    @staticmethod
    def get_sku(toy, proc=None):
        return toy._execute(SystemInfo._encode(toy, 56, proc)).data.rstrip(b'\0')

    @staticmethod
    def get_core_up_time_in_milliseconds(toy, proc=None):
        return to_int(toy._execute(SystemInfo._encode(toy, 57, proc)).data)

    @staticmethod
    def get_event_log_status(toy, proc=None):
        return EventLogStatus(*struct.unpack('>3I', toy._execute(SystemInfo._encode(toy, 58, proc)).data))

    @staticmethod
    def get_event_log_data(toy, j, j2, proc=None):  # unknown name
        return toy._execute(SystemInfo._encode(toy, 59, proc, to_bytes(j, 4) + to_bytes(j2, 4))).data

    @staticmethod
    def clear_event_log(toy, proc=None):
        toy._execute(SystemInfo._encode(toy, 60, proc))

    @staticmethod
    def enable_sos_message_notify(toy, enable: bool, proc=None):
        toy._execute(SystemInfo._encode(toy, 61, proc, [int(enable)]))

    sos_message_notify = (17, 62, 0xff), lambda listener, p: listener(SosMessages(p.data[0]))

    @staticmethod
    def get_sos_message(toy, proc=None):
        toy._execute(SystemInfo._encode(toy, 63, proc))

    @staticmethod
    def clear_sos_message(toy, proc=None):
        toy._execute(SystemInfo._encode(toy, 68, proc))
