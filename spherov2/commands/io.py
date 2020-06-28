import struct
from enum import IntFlag, IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class AudioPlaybackModes(IntFlag):
    PLAY_IMMEDIATELY = 0b0
    PLAY_ONLY_IF_NOT_PLAYING = 0b1
    PLAY_AFTER_CURRENT_SOUND = 0b10


class SpecdrumsColorPaletteIndicies(IntEnum):
    DEFAULT = 0
    MIDI = 1


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

    @staticmethod
    def set_all_leds_with_32_bit_mask(mask, values, target_id=None):
        return IO.__encode(command_id=26, data=[*to_bytes(mask, 4), *values], target_id=target_id)

    @staticmethod
    def set_compressed_frame_player_one_color(s, s2, s3, target_id=None):
        return IO.__encode(command_id=47, data=[s, s2, s3], target_id=target_id)

    @staticmethod
    def save_compressed_frame_player_animation(s, s2, z, s3, s_arr, i, i_arr, target_id=None):
        return IO.__encode(
            command_id=49,
            data=[s, s2, int(z), s3, *s_arr, *struct.pack('>%dH' % (len(i_arr) + 1), i, *i_arr)],
            target_id=target_id
        )

    @staticmethod
    def play_compressed_frame_player_animation(s, target_id=None):
        return IO.__encode(command_id=50, data=[s], target_id=target_id)

    @staticmethod
    def play_compressed_frame_player_frame(i, target_id=None):
        return IO.__encode(command_id=51, data=to_bytes(i, 2), target_id=target_id)

    @staticmethod
    def get_compressed_frame_player_list_of_frames(target_id=None):
        return IO.__encode(command_id=52, target_id=target_id)

    @staticmethod
    def delete_all_compressed_frame_player_animations_and_frames(target_id=None):
        return IO.__encode(command_id=53, target_id=target_id)

    @staticmethod
    def pause_compressed_frame_player_animation(target_id=None):
        return IO.__encode(command_id=54, target_id=target_id)

    @staticmethod
    def resume_compressed_frame_player_animation(target_id=None):
        return IO.__encode(command_id=55, target_id=target_id)

    @staticmethod
    def reset_compressed_frame_player_animation(target_id=None):
        return IO.__encode(command_id=56, target_id=target_id)

    compressed_frame_player_animation_complete_notify = (26, 63, 0xff)

    @staticmethod
    def assign_compressed_frame_player_frames_to_animation(s, i, i_arr, target_id=None):
        return IO.__encode(command_id=64, data=[s, *struct.pack('>%dH' % (len(i_arr) + 1), i, i_arr)],
                           target_id=target_id)

    @staticmethod
    def save_compressed_frame_player_animation_without_frames(s, s2, z, s3, s_arr, i, target_id=None):
        return IO.__encode(command_id=65, data=[s, s2, int(z), s3, *s_arr, *to_bytes(i, 2)], target_id=target_id)

    @staticmethod
    def play_compressed_frame_player_animation_with_loop_option(s, z, target_id=None):
        return IO.__encode(command_id=67, data=[s, int(z)], target_id=target_id)

    @staticmethod
    def get_active_color_palette(target_id=None):
        return IO.__encode(command_id=68, target_id=target_id)

    @staticmethod
    def set_active_color_palette(rgb_index_bytes, target_id=None):
        return IO.__encode(command_id=69, data=rgb_index_bytes, target_id=target_id)

    @staticmethod
    def get_color_identification_report(red, green, blue, confidence_threshold, target_id=None):
        return IO.__encode(command_id=70, data=[red, green, blue, confidence_threshold], target_id=target_id)

    @staticmethod
    def load_color_palette(palette_index, target_id=None):
        return IO.__encode(command_id=71, data=[palette_index], target_id=target_id)

    @staticmethod
    def save_color_palette(palette_index, target_id=None):
        return IO.__encode(command_id=72, data=[palette_index], target_id=target_id)

    @staticmethod
    def get_compressed_frame_player_frame_info_type(target_id=None):
        return IO.__encode(command_id=76, target_id=target_id)

    @staticmethod
    def save_compressed_frame_player16_bit_frame(i, i2, i3, i4, i5, target_id=None):
        return IO.__encode(command_id=77, data=struct.pack('>5H', i, i2, i3, i4, i5), target_id=target_id)

    @staticmethod
    def release_led_requests(target_id=None):
        return IO.__encode(command_id=78, target_id=target_id)
