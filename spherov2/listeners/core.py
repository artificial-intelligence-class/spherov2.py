from typing import NamedTuple

from spherov2.commands.core import PowerStates


class Versions(NamedTuple):
    record_version: int
    model_number: int
    hardware_version_code: int
    main_app_version_major: int
    main_app_version_minor: int
    bootloader_version: str
    orb_basic_version: str
    overlay_version: str


class BluetoothInfo(NamedTuple):
    name: str
    address: str


class PowerState(NamedTuple):
    record_version: int
    state: PowerStates
    voltage: float
    number_of_charges: int
    time_since_last_charge: int
