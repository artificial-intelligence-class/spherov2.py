from enum import IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class PowerStates(IntEnum):
    UNKNOWN = 0
    CHARGING = 1
    OK = 2
    LOW = 3
    CRITICAL = 4


class IntervalOptions(IntEnum):
    NONE = 0
    DEEP_SLEEP = 0xffff


class Core:
    __encode = partial(Packet, device_id=0)

    @staticmethod
    def ping(target_id=None):
        return Core.__encode(command_id=1, target_id=target_id)

    @staticmethod
    def get_versions(target_id=None):
        return Core.__encode(command_id=2, target_id=target_id)

    @staticmethod
    def set_bluetooth_name(name: str, target_id=None):
        return Core.__encode(command_id=16, data=name.encode('ascii') + bytes(1), target_id=target_id)

    @staticmethod
    def get_bluetooth_info(target_id=None):
        return Core.__encode(command_id=17, target_id=target_id)

    @staticmethod
    def get_power_state(target_id=None):
        return Core.__encode(command_id=32, target_id=target_id)

    @staticmethod
    def enable_battery_state_changed_notify(enable: bool, target_id=None):
        return Core.__encode(command_id=33, data=[int(enable)], target_id=target_id)

    @staticmethod
    def sleep(interval_option: IntervalOptions, unk: int, unk2: int, target_id=None):
        return Core.__encode(command_id=34, data=[interval_option, unk, *to_bytes(unk2, 2)], target_id=target_id)

    @staticmethod
    def set_inactivity_timeout(timeout: int, target_id=None):
        return Core.__encode(command_id=37, data=to_bytes(timeout, 2), target_id=target_id)
