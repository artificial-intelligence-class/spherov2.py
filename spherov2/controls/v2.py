from spherov2.command.driving import DriveFlags
from spherov2.toy.core import Toy


class DriveControl:
    def __init__(self, toy: Toy):
        self.__toy = toy
        self.__is_boosting = False

    def roll_start(self, heading, speed):
        flag = DriveFlags.forward
        if speed < 0:
            flag = DriveFlags.backward
            heading += 180
        if self.__is_boosting:
            flag |= DriveFlags.turbo
        speed = min(255, abs(speed))
        heading %= 360
        self.__toy.drive_with_heading(speed, heading, flag)

    def roll_stop(self, heading):
        self.roll_start(heading, 0)

    def set_stabilization(self, stabilize):
        self.__toy.set_stabilization(stabilize)