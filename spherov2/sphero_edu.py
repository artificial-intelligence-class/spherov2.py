import threading
import time
from enum import Enum

from spherov2.command.animatronic import R2LegActions
from spherov2.toy.core import Toy, CommandExecuteError
from spherov2.toy.r2q5 import R2Q5
from spherov2.utils import ToyUtil


class Stance(str, Enum):
    Bipod = 'twolegs'
    Tripod = 'threelegs'


class SpheroEduAPI:
    """Implementation of Sphero Edu Javascript APIs: https://sphero.docsapp.io/docs/get-started"""

    def __init__(self, toy: Toy):
        self.__toy = toy
        self.__heading = 0
        self.__speed = 0
        self.__stabilization = True

        self.__stopped = threading.Event()
        self.__not_updating = threading.Event()
        self.__not_updating.set()
        self.__thread = threading.Thread(target=self.__background)

    def __enter__(self):
        self.__toy.__enter__()
        self.__toy.wake()
        self.__thread.start()
        return self

    def __exit__(self, *args):
        self.__stopped.set()
        self.__thread.join()
        self.__toy.sleep()
        self.__toy.__exit__(*args)

    def __background(self):
        while not self.__stopped.wait(0.8):
            self.__not_updating.wait()
            if self.__speed != 0:
                try:
                    self.set_speed(self.__speed)
                except CommandExecuteError:
                    pass
            # TODO raw motor

    def roll(self, heading: int, speed: int, duration: float):
        """Combines heading(0-360°), speed(-255-255), and duration to make the robot roll with one line of code.
        For example, to have the robot roll at 90°, at speed 200 for 2s, use ``roll(90, 200, 2)``"""
        # Mini: (t > 0 ? t = Math.round(.67 * (t + 126)) : t < 0 && (t = Math.round(.67 * (t - 126))))
        self.__speed = min(255, max(-255, speed))
        self.__heading = heading % 360
        if speed < 0:
            self.__heading = (self.__heading + 180) % 360
        ToyUtil.roll_start(self.__toy, self.__heading, self.__speed)
        time.sleep(duration)
        self.stop_roll()

    def set_speed(self, speed: int):
        """Sets the speed of the robot from -255 to 255, where positive speed is forward, negative speed is backward,
        and 0 is stopped. Each robot type translates this value differently into a real world speed;
        Ollie is almost three times faster than Sphero. For example, use ``set_speed(188)`` to set the speed to 188
        which persists until you set a different speed. You can also read the real-time velocity value in centimeters
        per second reported by the motor encoders.
        """
        # Mini: (e > 0 ? e = Math.round(.67 * (e + 126)) : e < 0 && (e = Math.round(.67 * (e - 126)))),
        self.__speed = min(255, max(-255, speed))
        ToyUtil.roll_start(self.__toy, self.__heading, self.__speed)

    def stop_roll(self, heading: int = None):
        """Sets the speed to zero to stop the robot, effectively the same as the ``set_speed(0)`` command."""
        if heading is not None:
            self.__heading = heading % 360
        ToyUtil.roll_stop(self.__toy, self.__heading, False)

    def set_heading(self, heading: int):
        """Sets the direction the robot rolls.
        Assuming you aim the robot with the blue tail light facing you, then 0° is forward, 90° is right,
        270° is left, and 180° is backward. For example, use ``set_heading(90)`` to face right."""
        self.__heading = heading % 360
        ToyUtil.roll_start(self.__toy, self.__heading, self.__speed)

    def spin(self, angle: int, duration: float):
        """Spins the robot for a given number of degrees over time, with 360° being a single revolution. 
        For example, to spin the robot 360° over 1s, use: ``spin(360, 1)``. 
        Use :func:`set_speed` prior to :func:`spin` to have the robot move in circle or an arc or circle.

        Note: Unlike official API, performance of spin is granted, but may be longer than the specified duration"""

        if angle == 0:
            return

        time_pre_rev = .45

        # Object(r.g)(r.b.RVR) && (time_pre_rev = 1500),
        # (Object(r.g)(r.b.R2D2) || Object(r.g)(r.b.R2Q5)) && (time_pre_rev = 700),
        # Object(r.g)(r.b.Mini) && (time_pre_rev = 500),
        # Object(r.g)(r.b.Ollie) && (time_pre_rev = 600);
        if isinstance(self.__toy, R2Q5):
            time_pre_rev = .7

        abs_angle = abs(angle)
        duration = max(duration, time_pre_rev * abs_angle / 360)

        start = time.time()
        angle_gone = 0
        try:
            self.__not_updating.clear()
            while angle_gone < abs_angle:
                delta = round(min((time.time() - start) / duration, 1.) * abs_angle) - angle_gone
                self.set_heading(self.__heading + delta if angle > 0 else self.__heading - delta)
                angle_gone += delta
        finally:
            self.__not_updating.set()

    def set_stabilization(self, stabilize: bool):
        """Turns the stabilization system on and ``set_stabilization(false)`` turns it off.
        Stabilization is normally on to keep the robot upright using the Inertial Measurement Unit (IMU),
        a combination of readings from the Accelerometer (directional acceleration), Gyroscope (rotation speed),
        and Encoders (location and distance). When ``set_stabilization(false)`` and you power the motors,
        the robot will not balance, resulting in possible unstable behaviors like wobbly driving,
        or even jumping if you set the power very high. Some use cases to turn it off are:

        1. Jumping: Set Motor Power to max values and the robot will jump off the ground!
        2. Gyro: Programs like the Spinning Top where you want to to isolate the Gyroscope readings rather than having
        the robot auto balance inside the shell.

        When stabilization is off you can't use :func:`set_speed` to set a speed because it requires the control system
        to be on to function. However, you can control the motors using Motor Power with :func:`right_motor_pwm` and
        :func:`left_motor_pwm` when the control system is off."""
        self.__stabilization = stabilize
        ToyUtil.set_stabilization(self.__toy, stabilize)

    def set_stance(self, stance: Stance):
        if stance == Stance.Bipod:
            ToyUtil.perform_leg_action(self.__toy, R2LegActions.TWO_LEGS)
        elif stance == Stance.Tripod:
            ToyUtil.perform_leg_action(self.__toy, R2LegActions.THREE_LEGS)
        else:
            raise ValueError(f'Stance {stance} is not supported')
