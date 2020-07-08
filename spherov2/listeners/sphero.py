from typing import NamedTuple


class Options(NamedTuple):
    disable_sleep_in_charger: bool
    enable_vector_drive: bool
    disable_self_level_in_charger: bool
    enable_tail_light_always_on: bool
    enable_motion_timeout: bool
    enable_gyro_max_notify: bool
    enable_full_speed: bool
