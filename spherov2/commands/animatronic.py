import struct
from enum import IntEnum

from spherov2.commands import Commands
from spherov2.helper import to_bytes


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


class SuspensionAnimationModes(IntEnum):
    NON_ACTIVE = 0
    ACTIVE = 1


class Animatronic(Commands):
    _did = 23

    @staticmethod
    def play_animation(toy, animation: IntEnum, proc=None):
        toy._execute(Animatronic._encode(toy, 5, proc, to_bytes(animation, 2)))

    @staticmethod
    def perform_leg_action(toy, leg_action: R2LegActions, proc=None):
        toy._execute(Animatronic._encode(toy, 13, proc, [leg_action]))

    @staticmethod
    def set_head_position(toy, head_position: float, proc=None):
        toy._execute(Animatronic._encode(toy, 15, proc, struct.pack('>f', head_position)))

    play_animation_complete_notify = (23, 17, 0xff)

    @staticmethod
    def get_head_position(toy, proc=None):
        return struct.unpack('>f', toy._execute(Animatronic._encode(toy, 20, proc)).data)[0]

    @staticmethod
    def set_leg_position(toy, leg_position: float, proc=None):
        toy._execute(Animatronic._encode(toy, 21, proc, struct.pack('>f', leg_position)))

    @staticmethod
    def get_leg_position(toy, proc=None):
        return struct.unpack('>f', toy._execute(Animatronic._encode(toy, 22, proc)).data)[0]

    @staticmethod
    def get_leg_action(toy, proc=None):
        return R2DoLegActions(toy._execute(Animatronic._encode(toy, 37, proc)).data[0])

    leg_action_complete_notify = (23, 38, 0xff)

    @staticmethod
    def enable_leg_action_notify(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 42, proc, [int(enable)]))

    @staticmethod
    def stop_animation(toy, proc=None):
        toy._execute(Animatronic._encode(toy, 43, proc))

    @staticmethod
    def enable_idle_animations(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 44, proc, [int(enable)]))

    @staticmethod
    def enable_trophy_mode(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 45, proc, [int(enable)]))

    @staticmethod
    def get_trophy_mode_enabled(toy, proc=None):
        return bool(toy._execute(Animatronic._encode(toy, 46, proc)).data[0])

    @staticmethod
    def enable_head_reset_to_zero_notify(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 57, proc, [int(enable)]))

    head_reset_to_zero_notify = (23, 58, 0xff), lambda listener, _: listener()
