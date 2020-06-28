from enum import IntEnum
from functools import partial

from spherov2.packet import Packet


class BatteryVoltageAndStateStates(IntEnum):
    CHARGED = 0
    CHARGING = 1
    NOT_CHARGING = 2
    OK = 3
    LOW = 4
    CRITICAL = 5
    RESERVED = 6
    UNUSED = 7


class BatteryVoltageStates(IntEnum):
    UNKNOWN = 0
    OK = 1
    LOW = 2
    CRITICAL = 3


class BatteryStates(IntEnum):
    CHARGED = 0
    CHARGING = 1
    NOT_CHARGING = 2
    OK = 3
    LOW = 4
    CRITICAL = 5
    UNKNOWN = 255


class BatteryVoltageReadingTypes(IntEnum):
    CALIBRATED_AND_FILTERED = 0
    CALIBRATED_AND_UNFILTERED = 1
    UNCALIBRATED_AND_UNFILTERED = 2


class AmplifierIds(IntEnum):
    LEFT_MOTOR = 0
    RIGHT_MOTOR = 1


class EfuseIds(IntEnum):
    PRIMARY_EFUSE = 0


class Power:
    __encode = partial(Packet, device_id=19)

    @staticmethod
    def enter_deep_sleep(s, target_id=None):
        return Power.__encode(command_id=0, data=[s], target_id=target_id)

    @staticmethod
    def sleep(target_id=None):
        return Power.__encode(command_id=1, target_id=target_id)

    @staticmethod
    def get_battery_voltage(target_id=None):
        return Power.__encode(command_id=3, target_id=target_id)

    @staticmethod
    def get_battery_state(target_id=None):
        return Power.__encode(command_id=4, target_id=target_id)

    @staticmethod
    def enable_battery_state_changed_notify(enable: bool, target_id=None):
        return Power.__encode(command_id=5, data=[int(enable)], target_id=target_id)

    battery_state_changed_notify = (19, 6, 0xff)

    @staticmethod
    def force_battery_refresh(target_id=None):
        return Power.__encode(command_id=12, target_id=target_id)

    @staticmethod
    def wake(target_id=None):
        return Power.__encode(command_id=13, target_id=target_id)

    @staticmethod
    def get_battery_percentage(target_id=None):
        return Power.__encode(command_id=16, target_id=target_id)

    @staticmethod
    def get_battery_voltage_state(target_id=None):
        return Power.__encode(command_id=23, target_id=target_id)

    will_sleep_notify = (19, 25, 0xff)
    did_sleep_notify = (19, 26, 0xff)

    @staticmethod
    def enable_battery_voltage_state_change_notify(enable, target_id=None):
        return Power.__encode(command_id=27, data=[int(enable)], target_id=target_id)

    battery_voltage_state_change_notify = (19, 28, 0xff)

    @staticmethod
    def get_battery_voltage_in_volts(reading_type, target_id=None):
        return Power.__encode(command_id=37, data=[reading_type], target_id=target_id)

    @staticmethod
    def get_battery_voltage_state_thresholds(target_id=None):
        return Power.__encode(command_id=38, target_id=target_id)

    @staticmethod
    def get_current_sense_amplifier_current(amplifier_id, target_id=None):
        return Power.__encode(command_id=39, data=[amplifier_id], target_id=target_id)

    @staticmethod
    def get_efuse_fault_status(efuse_id, target_id=None):
        return Power.__encode(command_id=40, data=[efuse_id], target_id=target_id)

    efuse_fault_occurred_notify = (19, 41, 0xff)

    @staticmethod
    def enable_efuse(efuse_id, target_id=None):
        return Power.__encode(command_id=42, data=[efuse_id], target_id=target_id)
