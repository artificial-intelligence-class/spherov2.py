from typing import NamedTuple


class BatteryVoltageStateThresholds(NamedTuple):
    critical_threshold: float
    low_threshold: float
    hysteresis: float
