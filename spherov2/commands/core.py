import struct
from enum import IntEnum

from spherov2.commands import Commands
from spherov2.helper import to_bytes
from spherov2.listeners.core import Versions, BluetoothInfo, PowerState, PowerStates


class IntervalOptions(IntEnum):
    NONE = 0
    DEEP_SLEEP = 0xffff


class Core(Commands):
    _did = 0

    @staticmethod
    def ping(toy, tid=None):
        return Core._encode(toy, 1, tid)

    @staticmethod
    def get_versions(toy, tid=None):
        unpacked = struct.unpack('>8B', toy._execute(Core._encode(toy, 2, tid)).data)
        return Versions(
            record_version=unpacked[0], model_number=unpacked[1], hardware_version_code=unpacked[2],
            main_app_version_major=unpacked[3], main_app_version_minor=unpacked[4],
            bootloader_version='%d.%d' % (unpacked[5] >> 4, unpacked[5] & 0xf),
            orb_basic_version='%d.%d' % (unpacked[6] >> 4, unpacked[6] & 0xf),
            overlay_version='%d.%d' % (unpacked[7] >> 4, unpacked[7] & 0xf),
        )

    @staticmethod
    def set_bluetooth_name(toy, name: bytes, tid=None):
        toy._execute(Core._encode(toy, 16, tid, [*name, 0]))

    @staticmethod
    def get_bluetooth_info(toy, tid=None):
        data = toy._execute(Core._encode(toy, 17, tid)).data.rstrip(b'\0')
        name, *_, address = data.split(b'\0')
        return BluetoothInfo(bytes(name), bytes(address))

    @staticmethod
    def get_power_state(toy, tid=None):
        unpacked = struct.unpack('>2B3H', toy._execute(Core._encode(toy, 32, tid)).data)
        return PowerState(record_version=unpacked[0], state=PowerStates(unpacked[1]), voltage=unpacked[2] / 100,
                          number_of_charges=unpacked[3], time_since_last_charge=unpacked[4])

    @staticmethod
    def enable_battery_state_changed_notify(toy, enable: bool, tid=None):
        toy._execute(Core._encode(toy, 33, tid, [int(enable)]))

    @staticmethod
    def sleep(toy, interval_option: IntervalOptions, unk: int, unk2: int, proc=None):
        return toy._execute(Core._encode(toy, 34, proc, [*to_bytes(interval_option, 2), unk, *to_bytes(unk2, 2)]))

    @staticmethod
    def set_inactivity_timeout(toy, timeout: int, tid=None):
        toy._execute(Core._encode(toy, 37, tid, to_bytes(timeout, 2)))
