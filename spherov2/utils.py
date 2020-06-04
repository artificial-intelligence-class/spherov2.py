from spherov2.command.animatronic import R2LegActions
from spherov2.toy.core import Toy


class ToyUtil:
    @staticmethod
    def roll_start(toy: Toy, heading: int, speed: int):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.roll_start(heading, speed)

    @staticmethod
    def roll_stop(toy: Toy, heading: int, is_reverse: bool):
        if hasattr(toy, 'drive_control'):
            if is_reverse:
                heading = (heading + 180) % 360
            toy.drive_control.roll_stop(heading)

    @staticmethod
    def perform_leg_action(toy: Toy, leg_action: R2LegActions):
        if hasattr(toy, 'perform_leg_action'):
            toy.perform_leg_action(leg_action)

    @staticmethod
    def set_stabilization(toy: Toy, stabilize):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.set_stabilization(stabilize)
