import struct
from enum import IntEnum
from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class R2LegActions(IntEnum):
    STOP = 0
    THREE_LEGS = 1
    TWO_LEGS = 2
    WADDLE = 3


class Animatronic:
    __encode = partial(Packet, device_id=23)
    play_animation_complete_notify = (23, 17, 0xff)

    @staticmethod
    def play_animation(animation: IntEnum, target_id=None):
        return Animatronic.__encode(command_id=5, data=to_bytes(animation, 2), target_id=target_id)

    @staticmethod
    def perform_leg_action(leg_action: R2LegActions, target_id=None):
        return Animatronic.__encode(command_id=13, data=[leg_action], target_id=target_id)

    @staticmethod
    def set_head_position(head_position: float, target_id=None):
        return Animatronic.__encode(command_id=15, data=struct.pack('>f', head_position), target_id=target_id)

    @staticmethod
    def set_leg_position(leg_position: float, target_id=None):
        return Animatronic.__encode(command_id=21, data=struct.pack('>f', leg_position), target_id=target_id)

    @staticmethod
    def get_leg_position(target_id=None):
        return Animatronic.__encode(command_id=22, target_id=target_id)

    @staticmethod
    def stop_animation(target_id=None):
        return Animatronic.__encode(command_id=43, target_id=target_id)
