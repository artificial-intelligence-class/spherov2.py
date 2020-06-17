import struct
from enum import IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class R2DoLegActions(IntEnum):
    UNKNOWN = 0
    THREE_LEGS = 1
    TWO_LEGS = 2
    WADDLE = 3
    TRANSITIONING = 4


class R2LegActions(IntEnum):
    STOP = 0
    THREE_LEGS = 1
    TWO_LEGS = 2
    WADDLE = 3


class Animatronic:
    __encode = partial(Packet, device_id=23)

    @staticmethod
    def play_animation(animation: IntEnum, target_id=None):
        return Animatronic.__encode(command_id=5, data=to_bytes(animation, 2), target_id=target_id)

    @staticmethod
    def perform_leg_action(leg_action: R2LegActions, target_id=None):
        return Animatronic.__encode(command_id=13, data=[leg_action], target_id=target_id)

    @staticmethod
    def set_head_position(head_position: float, target_id=None):
        return Animatronic.__encode(command_id=15, data=struct.pack('>f', head_position), target_id=target_id)

    play_animation_complete_notify = (23, 17, 0xff)

    @staticmethod
    def get_head_position(target_id=None):
        return Animatronic.__encode(command_id=20, target_id=target_id)

    @staticmethod
    def set_leg_position(leg_position: float, target_id=None):
        return Animatronic.__encode(command_id=21, data=struct.pack('>f', leg_position), target_id=target_id)

    @staticmethod
    def get_leg_position(target_id=None):
        return Animatronic.__encode(command_id=22, target_id=target_id)

    @staticmethod
    def get_leg_action(target_id=None):
        return Animatronic.__encode(command_id=37, target_id=target_id)

    leg_action_complete_notify = (23, 38, 0xff)

    @staticmethod
    def enable_leg_action_notify(enable: bool, target_id=None):
        return Animatronic.__encode(command_id=42, data=[int(enable)], target_id=target_id)

    @staticmethod
    def stop_animation(target_id=None):
        return Animatronic.__encode(command_id=43, target_id=target_id)

    @staticmethod
    def enable_idle_animations(enable: bool, target_id=None):
        return Animatronic.__encode(command_id=44, data=[int(enable)], target_id=target_id)

    @staticmethod
    def enable_trophy_mode(enable: bool, target_id=None):
        return Animatronic.__encode(command_id=45, data=[int(enable)], target_id=target_id)

    @staticmethod
    def get_trophy_mode_enabled(target_id=None):
        return Animatronic.__encode(command_id=46, target_id=target_id)

    @staticmethod
    def enable_head_reset_to_zero_notify(target_id=None):
        return Animatronic.__encode(command_id=57, target_id=target_id)

    head_reset_to_zero_notify = (23, 58, 0xff)
