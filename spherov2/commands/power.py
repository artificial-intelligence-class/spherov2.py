import struct
from enum import IntEnum, IntFlag

from spherov2.commands import Commands
from spherov2.helper import to_int
from spherov2.listeners.power import BatteryVoltageStateThresholds


class PowerOptions(IntFlag):
    SLEEP_WHILE_CHARGING = 0x1  # 0b1
    DOUBLE_TAP_TO_WAKE = 0x2  # 0b10


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


class ChargerStates(IntEnum):
    UNKNOWN = 0
    NOT_CHARGING = 1
    CHARGING = 2
    CHARGED = 3


class AmplifierIds(IntEnum):
    LEFT_MOTOR = 0
    RIGHT_MOTOR = 1


class EfuseIds(IntEnum):
    PRIMARY_EFUSE = 0


class Power(Commands):
    _did = 19

    @staticmethod
    def enter_deep_sleep(toy, s, proc=None):
        toy._execute(Power._encode(toy, 0, proc, [s]))

    @staticmethod
    def sleep(toy, proc=None):
        toy._execute(Power._encode(toy, 1, proc))

    @staticmethod
    def get_battery_voltage(toy, proc=None):
        return to_int(toy._execute(Power._encode(toy, 3, proc)).data) / 100

    @staticmethod
    def get_battery_state(toy, proc=None):
        return BatteryStates(toy._execute(Power._encode(toy, 4, proc)).data[0])

    @staticmethod
    def enable_battery_state_changed_notify(toy, enable: bool, proc=None):
        toy._execute(Power._encode(toy, 5, proc, [int(enable)]))

    battery_state_changed_notify = (19, 6, 0xff), lambda listener, p: listener(BatteryVoltageAndStateStates(p.data[0]))

    @staticmethod
    def force_battery_refresh(toy, proc=None):
        toy._execute(Power._encode(toy, 12, proc))

    @staticmethod
    def wake(toy, proc=None):
        toy._execute(Power._encode(toy, 13, proc))

    @staticmethod
    def get_battery_percentage(toy, proc=None):
        return toy._execute(Power._encode(toy, 16, proc)).data[0]

    @staticmethod
    def get_battery_voltage_state(toy, proc=None):
        return BatteryVoltageStates(toy._execute(Power._encode(toy, 23, proc)).data[0])

    will_sleep_notify = (19, 25, 0xff), lambda listener, _: listener()
    did_sleep_notify = (19, 26, 0xff), lambda listener, _: listener()

    @staticmethod
    def enable_battery_voltage_state_change_notify(toy, enable: bool, proc=None):
        toy._execute(Power._encode(toy, 27, proc, [int(enable)]))

    battery_voltage_state_change_notify = (19, 28, 0xff), lambda listener, p: listener(BatteryVoltageStates(p.data[0]))

    @staticmethod
    def get_charger_state(toy, proc=None):  # Untested
        return toy._execute(Power._encode(toy, 31, proc)).data[0]

    @staticmethod
    def enable_charger_state_changed_notify(toy, enable: bool, proc=None):
        toy._execute(Power._encode(toy, 32, proc, [int(enable)]))

    charger_state_changed_notify = (19, 33, 0xff), lambda listener, p: listener(
        BatteryVoltageStates(p.data[0]))  # Untested / Unknown param name

    @staticmethod
    def get_battery_adc_reading(toy, proc=None):  # Untested
        return toy._execute(Power._encode(toy, 34, proc)).data[0]

    @staticmethod
    def set_battery_calibration_slope_and_intercept(toy, f, f2, proc=None):  # untested / Unknown param names
        toy._execute(Power._encode(toy, 35, proc, [f, f2]))

    @staticmethod
    def get_battery_calibration_slope_intercept(toy, proc=None):  # Untested
        return toy._execute(Power._encode(toy, 36, proc)).data[0]

    @staticmethod
    def get_battery_voltage_in_volts(toy, reading_type: BatteryVoltageReadingTypes, proc=None):
        return struct.unpack('>f', toy._execute(Power._encode(toy, 37, proc, [reading_type])).data)[0]

    @staticmethod
    def get_battery_voltage_state_thresholds(toy, proc=None):
        return BatteryVoltageStateThresholds(
            *struct.unpack('>3f', toy._execute(Power._encode(toy, 38, proc)).data))

    @staticmethod
    def get_current_sense_amplifier_current(toy, amplifier_id: AmplifierIds, proc=None):
        return struct.unpack('>f', toy._execute(Power._encode(toy, 39, proc, [amplifier_id])).data)[0]

    @staticmethod
    def get_efuse_fault_status(toy, efuse_id: EfuseIds, proc=None):
        return toy._execute(Power._encode(toy, 40, proc, [efuse_id])).data[0]

    efuse_fault_occurred_notify = (19, 41, 0xff), lambda listener, p: listener(EfuseIds(p.data[0]))

    @staticmethod
    def enable_efuse(toy, efuse_id: EfuseIds, proc=None):
        toy._execute(Power._encode(toy, 42, proc, [efuse_id]))
