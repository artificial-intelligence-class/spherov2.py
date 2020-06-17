from enum import IntFlag
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class AudioPlaybackModes(IntFlag):
    PLAY_IMMEDIATELY = 0b0
    PLAY_ONLY_IF_NOT_PLAYING = 0b1
    PLAY_AFTER_CURRENT_SOUND = 0b10


class IO:
    __encode = partial(Packet, device_id=26)

    @staticmethod
    def play_audio_file(sound, playback_mode: AudioPlaybackModes, target_id=None):
        return IO.__encode(command_id=7, data=[*to_bytes(sound, 2), playback_mode], target_id=target_id)

    @staticmethod
    def set_audio_volume(volume, target_id=None):
        return IO.__encode(command_id=8, data=[volume], target_id=target_id)

    @staticmethod
    def get_audio_volume(target_id=None):
        return IO.__encode(command_id=9, target_id=target_id)

    @staticmethod
    def stop_all_audio(target_id=None):
        return IO.__encode(command_id=10, target_id=target_id)

    @staticmethod
    def set_all_leds_with_16_bit_mask(mask, values, target_id=None):
        return IO.__encode(command_id=14, data=[*to_bytes(mask, 2), *values], target_id=target_id)

    @staticmethod
    def start_idle_led_animation(target_id=None):
        return IO.__encode(command_id=25, target_id=target_id)
