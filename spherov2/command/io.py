from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class IO:
    __encode = partial(Packet, device_id=26)

    @staticmethod
    def set_audio_volume(volume, target_id=None):
        return IO.__encode(command_id=8, data=[volume], target_id=target_id)

    @staticmethod
    def stop_all_audio(target_id=None):
        return IO.__encode(command_id=10, target_id=target_id)

    @staticmethod
    def set_all_leds_with_16_bit_mask(mask, values, target_id=None):
        return IO.__encode(command_id=14, data=[*to_bytes(mask, 2), *values], target_id=target_id)

    @staticmethod
    def start_idle_led_animation(target_id=None):
        return IO.__encode(command_id=25, target_id=target_id)
