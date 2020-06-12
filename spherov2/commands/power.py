from enum import IntEnum
from functools import partial

from spherov2.packet import Packet


class BatteryStates(IntEnum):
    CHARGED = 0
    CHARGING = 1
    NOT_CHARGING = 2
    OK = 3
    LOW = 4
    CRITICAL = 5
    UNKNOWN = 255


class BatteryVoltageAndStateStates(IntEnum):
    CHARGED = 0
    CHARGING = 1
    NOT_CHARGING = 2
    OK = 3
    LOW = 4
    CRITICAL = 5
    RESERVED = 6
    UNUSED = 7


class Power:
    __encode = partial(Packet, device_id=19)

    @staticmethod
    def sleep(target_id=None):
        return Power.__encode(command_id=1, target_id=target_id)

    @staticmethod
    def get_battery_voltage(target_id=None):
        return Power.__encode(command_id=3, target_id=target_id)

    @staticmethod
    def get_battery_state(target_id=None):
        return Power.__encode(command_id=4, target_id=target_id)

    battery_state_changed_notify = (19, 6, 0xff)

    @staticmethod
    def wake(target_id=None):
        return Power.__encode(command_id=13, target_id=target_id)

    will_sleep_notify = (19, 25, 0xff)

    @staticmethod
    def enable_battery_voltage_state_change_notify(enable, target_id=None):
        return Power.__encode(command_id=27, data=[int(enable)], target_id=target_id)
