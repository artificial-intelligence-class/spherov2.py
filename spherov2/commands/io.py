import struct
from enum import IntFlag, IntEnum

from spherov2.commands import Commands
from spherov2.helper import to_bytes, to_int


class AudioPlaybackModes(IntFlag):
    PLAY_IMMEDIATELY = 0b0
    PLAY_ONLY_IF_NOT_PLAYING = 0b1
    PLAY_AFTER_CURRENT_SOUND = 0b10


class SpecdrumsColorPaletteIndicies(IntEnum):
    DEFAULT = 0
    MIDI = 1


class FrameInfoTypes(IntEnum):
    COMPRESSED_FRAME_PLAYER_INFO_TYPE_8_BIT = 0
    COMPRESSED_FRAME_PLAYER_INFO_TYPE_16_BIT = 1
    COMPRESSED_FRAME_PLAYER_INFO_TYPE_32_BIT = 2
    COMPRESSED_FRAME_PLAYER_INFO_TYPE_64_BIT = 3


class IO(Commands):
    _did = 26

    @staticmethod
    def play_audio_file(toy, sound, playback_mode: AudioPlaybackModes, proc=None):
        toy._execute(IO._encode(toy, 7, proc, [*to_bytes(sound, 2), playback_mode]))

    @staticmethod
    def set_audio_volume(toy, volume, proc=None):
        toy._execute(IO._encode(toy, 8, proc, [volume]))

    @staticmethod
    def get_audio_volume(toy, proc=None):
        return toy._execute(IO._encode(toy, 9, proc)).data[0]

    @staticmethod
    def stop_all_audio(toy, proc=None):
        toy._execute(IO._encode(toy, 10, proc))

    @staticmethod
    def set_all_leds_with_16_bit_mask(toy, mask, values, proc=None):
        toy._execute(IO._encode(toy, 14, proc, [*to_bytes(mask, 2), *values]))

    @staticmethod
    def start_idle_led_animation(toy, proc=None):
        toy._execute(IO._encode(toy, 25, proc))

    @staticmethod
    def set_all_leds_with_32_bit_mask(toy, mask, values, proc=None):
        toy._execute(IO._encode(toy, 26, proc, [*to_bytes(mask, 4), *values]))

    @staticmethod
    def set_compressed_frame_player_one_color(toy, s, s2, s3, proc=None):  # unknown names
        toy._execute(IO._encode(toy, 47, proc, [s, s2, s3]))

    @staticmethod
    def save_compressed_frame_player_animation(toy, s, s2, z, s3, s_arr, i, i_arr, proc=None):  # unknown names
        toy._execute(IO._encode(
            toy, 49, proc, [s, s2, int(z), s3, *s_arr, *struct.pack('>%dH' % (len(i_arr) + 1), i, *i_arr)]))

    @staticmethod
    def play_compressed_frame_player_animation(toy, s, proc=None):  # unknown names
        toy._execute(IO._encode(toy, 50, proc, [s]))

    @staticmethod
    def play_compressed_frame_player_frame(toy, i, proc=None):  # unknown names
        toy._execute(IO._encode(toy, 51, proc, to_bytes(i, 2)))

    @staticmethod
    def get_compressed_frame_player_list_of_frames(toy, proc=None):
        data = toy._execute(IO._encode(toy, 52, proc)).data
        return struct.unpack('>%dH' % (len(data) // 2), data)

    @staticmethod
    def delete_all_compressed_frame_player_animations_and_frames(toy, proc=None):
        toy._execute(IO._encode(toy, 53, proc))

    @staticmethod
    def pause_compressed_frame_player_animation(toy, proc=None):
        toy._execute(IO._encode(toy, 54, proc))

    @staticmethod
    def resume_compressed_frame_player_animation(toy, proc=None):
        toy._execute(IO._encode(toy, 55, proc))

    @staticmethod
    def reset_compressed_frame_player_animation(toy, proc=None):
        toy._execute(IO._encode(toy, 56, proc))

    compressed_frame_player_animation_complete_notify = (26, 63, 0xff), lambda listener, p: listener(p.data[0])

    @staticmethod
    def assign_compressed_frame_player_frames_to_animation(toy, s, i, i_arr, proc=None):  # unknown names
        toy._execute(IO._encode(toy, 64, proc, [s, *struct.pack('>%dH' % (len(i_arr) + 1), i, *i_arr)]))

    @staticmethod
    def save_compressed_frame_player_animation_without_frames(toy, s, s2, z, s3, s_arr, i, proc=None):  # unknown names
        toy._execute(IO._encode(toy, 65, proc, [s, s2, int(z), s3, *s_arr, *to_bytes(i, 2)]))

    @staticmethod
    def play_compressed_frame_player_animation_with_loop_option(toy, s, z, proc=None):
        toy._execute(IO._encode(toy, 67, proc, [s, int(z)]))

    @staticmethod
    def get_active_color_palette(toy, proc=None):
        return toy._execute(IO._encode(toy, 68, proc)).data

    @staticmethod
    def set_active_color_palette(toy, rgb_index_bytes, proc=None):
        toy._execute(IO._encode(toy, 69, proc, rgb_index_bytes))

    @staticmethod
    def get_color_identification_report(toy, red, green, blue, confidence_threshold, proc=None):
        return toy._execute(IO._encode(toy, 70, proc, [red, green, blue, confidence_threshold])).data

    @staticmethod
    def load_color_palette(toy, palette_index, proc=None):
        toy._execute(IO._encode(toy, 71, proc, [palette_index]))

    @staticmethod
    def save_color_palette(toy, palette_index, proc=None):
        toy._execute(IO._encode(toy, 72, proc, [palette_index]))

    @staticmethod
    def get_compressed_frame_player_frame_info_type(toy, proc=None):
        return FrameInfoTypes(toy._execute(IO._encode(toy, 76, proc)).data[0])

    @staticmethod
    def save_compressed_frame_player16_bit_frame(toy, i, i2, i3, i4, i5, proc=None):  # unknown names
        return to_int(toy._execute(IO._encode(toy, 77, proc, struct.pack('>5H', i, i2, i3, i4, i5))).data)

    @staticmethod
    def release_led_requests(toy, proc=None):
        toy._execute(IO._encode(toy, 78, proc))
