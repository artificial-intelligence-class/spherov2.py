import threading
import time
from collections import namedtuple, defaultdict
from enum import Enum, IntEnum
from functools import partial
from typing import Union

from spherov2.command.animatronic import R2LegActions
from spherov2.controls.enums import RawMotorModes
from spherov2.helper import bound_value, bound_color
from spherov2.toy.bb8 import BB8
from spherov2.toy.bb9e import BB9E
from spherov2.toy.bolt import BOLT
from spherov2.toy.core import Toy
from spherov2.toy.mini import Mini
from spherov2.toy.ollie import Ollie
from spherov2.toy.r2d2 import R2D2
from spherov2.toy.r2q5 import R2Q5
from spherov2.toy.rvr import RVR
from spherov2.toy.sphero import Sphero
from spherov2.types import Color
from spherov2.utils import ToyUtil, SensorManager


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
        self.__raw_motor = namedtuple('rawMotor', ('left', 'right'))(0, 0)
        self.__leds = defaultdict(partial(Color, 0, 0, 0))

        self.__sensor_manager = SensorManager(toy)

        self.__stopped = threading.Event()
        self.__updating = threading.Lock()
        self.__thread = threading.Thread(target=self.__background)

    def __enter__(self):
        self.__toy.__enter__()
        self.__thread.start()
        self.__toy.wake()
        ToyUtil.set_robot_state_on_start(self.__toy)
        self.__sensor_manager.start_capturing_sensor_data()
        return self

    def __exit__(self, *args):
        self.__stopped.set()
        self.__thread.join()
        self.__toy.sleep()
        self.__toy.__exit__(*args)

    def __background(self):
        while not self.__stopped.wait(0.8):
            with self.__updating:
                self.__update_speeds()

    # Movements: control the robot's motors and control system.
    def __update_speeds(self):
        if self.__speed != 0:
            self.__update_speed()
        if self.__raw_motor.left != 0 or self.__raw_motor.right != 0:
            self.__update_raw_motor()

    def __stop_all(self):
        if self.__speed != 0:
            self.__speed = 0
            self.__update_speed()
        if self.__raw_motor.left != 0 or self.__raw_motor.right != 0:
            self.__raw_motor.left = self.__raw_motor.right = 0
            self.__update_raw_motor()

    def roll(self, heading: int, speed: int, duration: float):
        """Combines heading(0-360°), speed(-255-255), and duration to make the robot roll with one line of code.
        For example, to have the robot roll at 90°, at speed 200 for 2s, use ``roll(90, 200, 2)``"""
        if isinstance(self.__toy, Mini):
            speed = round((speed + 126) * 2 / 3) if speed > 0 else round((speed - 126) * 2 / 3)
        self.__speed = bound_value(-255, speed, 255)
        self.__heading = heading % 360
        if speed < 0:
            self.__heading = (self.__heading + 180) % 360
        self.__update_speed()
        time.sleep(duration)
        self.stop_roll()

    def __update_speed(self):
        ToyUtil.roll_start(self.__toy, self.__heading, self.__speed)

    def set_speed(self, speed: int):
        """Sets the speed of the robot from -255 to 255, where positive speed is forward, negative speed is backward,
        and 0 is stopped. Each robot type translates this value differently into a real world speed;
        Ollie is almost three times faster than Sphero. For example, use ``set_speed(188)`` to set the speed to 188
        which persists until you set a different speed. You can also read the real-time velocity value in centimeters
        per second reported by the motor encoders.
        """
        if isinstance(self.__toy, Mini):
            speed = round((speed + 126) * 2 / 3) if speed > 0 else round((speed - 126) * 2 / 3)
        self.__speed = bound_value(-255, speed, 255)
        self.__update_speed()

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

        Note: Unlike official API, performance of spin is guaranteed, but may be longer than the specified duration."""

        if angle == 0:
            return

        time_pre_rev = .45

        if isinstance(self.__toy, RVR):
            time_pre_rev = 1.5
        elif isinstance(self.__toy, (R2D2, R2Q5)):
            time_pre_rev = .7
        elif isinstance(self.__toy, Mini):
            time_pre_rev = .5
        elif isinstance(self.__toy, Ollie):
            time_pre_rev = .6

        abs_angle = abs(angle)
        duration = max(duration, time_pre_rev * abs_angle / 360)

        start = time.time()
        angle_gone = 0
        with self.__updating:
            while angle_gone < abs_angle:
                delta = round(min((time.time() - start) / duration, 1.) * abs_angle) - angle_gone
                self.set_heading(self.__heading + delta if angle > 0 else self.__heading - delta)
                angle_gone += delta

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
        to be on to function. However, you can control the motors using Motor Power with :func:`raw_motor` when
        the control system is off."""
        self.__stabilization = stabilize
        if isinstance(self.__toy, (Sphero, Mini, Ollie, BB8, BB9E, BOLT)):
            ToyUtil.set_stabilization(self.__toy, stabilize)

    def __update_raw_motor(self):
        ToyUtil.set_raw_motor(self.__toy,
                              RawMotorModes.REVERSE if self.__raw_motor.left < 0 else RawMotorModes.FORWARD,
                              abs(self.__raw_motor.left),
                              RawMotorModes.REVERSE if self.__raw_motor.right < 0 else RawMotorModes.FORWARD,
                              abs(self.__raw_motor.right))

    def raw_motor(self, left: int, right: int, duration: float):
        """Controls the electrical power sent to the left and right motors independently, on a scale from -255 to 255
        where positive is forward, negative is backward, and 0 is stopped. If you set both motors to full power
        the robot will jump because stabilization (use of the IMU to keep the robot upright) is disabled when using
        this command. This is different from :func:`set_speed` because Raw Motor sends an "Electromotive force"
        to the motors, whereas Set Speed is a target speed measured by the encoders. For example, to set the raw motor
        to full power for 4s, making the robot jump off the ground, use ``raw_motor(255, 255, 4)``."""
        stabilize = self.__stabilization
        if stabilize:
            self.set_stabilization(False)
        self.__raw_motor.left = bound_value(-255, left, 255)
        self.__raw_motor.right = bound_value(-255, right, 255)
        self.__update_raw_motor()
        if duration is not None:
            time.sleep(duration)
            if stabilize:
                self.set_stabilization(True)
            self.__raw_motor.left = self.__raw_motor.right = 0
            ToyUtil.set_raw_motor(self.__toy, RawMotorModes.OFF, 0, RawMotorModes.OFF, 0)

    def reset_aim(self):
        """Resets the heading calibration (aim) angle to use the current direction of the robot as 0°."""
        ToyUtil.reset_heading(self.__toy)

    # Star Wars Droid Movements
    def play_animation(self, animation: IntEnum):
        """Plays iconic `Star Wars Droid animations <https://edu.sphero.com/remixes/1195472/>`_ unique to BB-8, BB-9E,
        R2-D2 and R2-Q5 that combine movement, lights and sound. All animation enums can be accessed under the droid
        class, such as :class:`R2D2.Animations.CHARGER_1`."""
        if hasattr(self.__toy, 'Animations'):
            if animation not in self.__toy.Animations:
                raise ValueError(f'Animation {animation} cannot be played by this toy')
            with self.__updating:
                self.__stop_all()
            ToyUtil.play_animation(self.__toy, animation, True)

    # The R2-D2 and R2-Q5 Droids are physically different from other Sphero robots,
    # so there are some unique commands that only they can use.
    def set_dome_position(self, angle: float):
        """Rotates the dome on its axis, from -160° to 180°. For example, set to 45° using ``set_dome_position(45).``"""
        if isinstance(self.__toy, (R2D2, R2Q5)):
            ToyUtil.set_head_position(self.__toy, bound_value(-160., angle, 180.))

    def set_stance(self, stance: Stance):
        """Changes the stance between bipod and tripod. Set to bipod using ``set_stance(Stance.Bipod)`` and
        to tripod using ``set_stance(Stance.Tripod)``. Tripod is required for rolling."""
        if isinstance(self.__toy, (R2D2, R2Q5)):
            if stance == Stance.Bipod:
                ToyUtil.perform_leg_action(self.__toy, R2LegActions.TWO_LEGS)
            elif stance == Stance.Tripod:
                ToyUtil.perform_leg_action(self.__toy, R2LegActions.THREE_LEGS)
            else:
                raise ValueError(f'Stance {stance} is not supported')

    def set_waddle(self, waddle: bool):
        """Turns the waddle walk on using ``set_waddle(true)`` and off using ``set_waddle(false)``."""
        if isinstance(self.__toy, (R2D2, R2Q5)):
            with self.__updating:
                self.__stop_all()
            ToyUtil.perform_leg_action(self.__toy, R2LegActions.WADDLE if waddle else R2LegActions.STOP)

    # Lights: control the color and brightness of LEDs on a robot.
    def set_main_led(self, color: Color):
        """Changes the color of the main LED light, or the full matrix on Sphero BOLT. Set this using RGB
        (red, green, blue) values on a scale of 0 - 255. For example, ``set_main_led(Color(r=90, g=255, b=90))``."""
        self.__leds['main'] = bound_color(color, self.__leds['main'])
        ToyUtil.set_main_led(self.__toy, **self.__leds['main']._asdict(), is_user_color=False)
        if isinstance(self.__toy, (R2D2, R2Q5)):
            self.__leds['front'] = self.__leds['back'] = self.__leds['main']
        elif isinstance(self.__toy, RVR):
            self.__leds['front'] = \
                self.__leds['left_status_indication'] = self.__leds['right_status_indication'] = \
                self.__leds['battery_door_rear'] = self.__leds['battery_door_front'] = \
                self.__leds['power_button_front'] = self.__leds['power_button_rear'] = \
                self.__leds['back'] = self.__leds['main']

    def set_front_led(self, color: Color):
        """For Sphero RVR: Changes the color of RVR's front two LED headlights together.

        For Sphero BOLT, R2D2, R2Q5: Changes the color of the front LED light.

        Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the magenta color is expressed
        as ``set_front_color(Color(239, 0, 255))``."""
        if isinstance(self.__toy, (R2D2, R2Q5, BOLT, RVR)):
            self.__leds['front'] = bound_color(color, self.__leds['front'])
            ToyUtil.set_front_led(self.__toy, **self.__leds['front']._asdict())

    def set_back_led(self, color: Union[Color, int]):
        """For older Sphero:
        Sets the brightness of the back aiming LED, aka the "Tail Light." This LED is limited to blue only, with a
        brightness scale from 0 to 255. For example, use ``set_back_led(255)`` to set the back LED to full brightness.
        Use :func:`time.sleep` to set it on for a duration. For example, to create a dim and a bright blink
        sequence use::

            set_back_led(0)  # Dim
            delay(0.33)
            set_back_led(255)  # Bright
            delay(0.33)

        For Sphero BOLT, R2D2, R2Q5:
        Changes the color of the back LED light. Set this using RGB (red, green, blue) values on a scale of 0 - 255.

        For Sphero RVR:
        Changes the color of the left and right breaklight LED light. Set this using RGB (red, green, blue) values
        on a scale of 0 - 255."""
        if isinstance(color, int):
            self.__leds['back'] = Color(r=0, g=0, b=bound_value(0, color, 255))
            ToyUtil.set_back_led_brightness(self.__toy, self.__leds['back'].b)
        elif isinstance(self.__toy, (R2D2, R2Q5, BOLT, RVR)):
            self.__leds['back'] = bound_color(color, self.__leds['back'])
            ToyUtil.set_back_led(self.__toy, **self.__leds['back']._asdict())

    def fade(self, from_color: Color, to_color: Color, duration: float):
        """Changes the main LED lights from one color to another over a period of seconds. For example, to fade from
        green to blue over 3s, use: ``fade(Color(0, 255, 0), Color(0, 0, 255), 3.0)``."""
        from_color = bound_color(from_color, self.__leds['main'])
        to_color = bound_color(to_color, self.__leds['main'])

        start = time.time()
        while True:
            frac = (time.time() - start) / duration
            if frac >= 1:
                break
            self.set_main_led(Color(
                r=round(from_color.r * (1 - frac) + to_color.r * frac),
                g=round(from_color.g * (1 - frac) + to_color.g * frac),
                b=round(from_color.b * (1 - frac) + to_color.b * frac)))
        self.set_main_led(to_color)

    def strobe(self, color: Color, period: float, count: int):
        """Repeatedly blinks the main LED lights. The period is the time, in seconds, the light stays on during a
        single blink; cycles is the total number of blinks. The time for a single cycle is twice the period
        (time for a blink plus the same amount of time for the light to be off). Another way to say this is the period
        is 1/2 the time it takes for a single cycle. So, to strobe red 15 times in 3 seconds, use:
        ``strobe(Color(255, 57, 66), 3 / 15 / 2, 15)``."""
        for i in range(count * 2):
            if i & 1:
                self.set_main_led(color)
            else:
                self.set_main_led(Color(0, 0, 0))
            time.sleep(period)

    # TODO Sphero BOLT Lights

    # TODO Sphero RVR Lights

    # BB-9E Lights
    def set_dome_leds(self, brightness: int):
        """Controls the brightness of the two single color LEDs (red and blue) in the dome, from 0 to 15. We don't use
        0-255 for this light because it has less granular control. For example, set them to full brightness using
        ``set_dome_leds(15)``."""
        if isinstance(self.__toy, BB9E):
            self.__leds['dome'] = bound_value(0, brightness, 15)
            ranged = self.__leds['dome'] * 255 // 15
            ToyUtil.set_head_led(self.__toy, ranged)

    # R2-D2 & R2-Q5 Lights
    def set_holo_projector_led(self, brightness: int):
        """Changes the brightness of the Holographic Projector white LED, from 0 to 255. For example, set it to full
        brightness using ``set_holo_projector_led(255)``."""
        if isinstance(self.__toy, (R2D2, R2Q5)):
            self.__leds['holo_projector'] = bound_value(0, brightness, 255)
            ToyUtil.set_holo_projector(self.__toy, self.__leds['holo_projector'])

    def set_logic_display_leds(self, brightness: int):
        """Changes the brightness of the Logic Display LEDs, from 0 to 255. For example, set it to full brightness
        using ``set_logic_display_leds(255)``."""
        if isinstance(self.__toy, (R2D2, R2Q5)):
            self.__leds['logic_display'] = bound_value(0, brightness, 255)
            ToyUtil.set_logic_display(self.__toy, self.__leds['logic_display'])

    # Sounds: Control sounds and words which can play from your programming device's speaker or the robot.
    def play_sound(self, sound: IntEnum):
        """Unique Star Wars Droid Sounds are available for BB-8, BB-9E and R2-D2. For example, to play the R2-D2 Burnout
        sound use ``play_sound(R2D2.Audio.R2_BURNOUT)``."""
        if hasattr(self.__toy, 'Audio'):
            if sound not in self.__toy.Audio:
                raise ValueError(f'Sound {sound} cannot be played by this toy')
            ToyUtil.play_sound(self.__toy, sound, False)

    # Sensors: Querying sensor data allows you to react to real-time values coming from the robots' physical sensors.
    def get_acceleration(self):
        """Provides motion acceleration data along a given axis measured by the Accelerometer, in g's, where g =
        9.80665 m/s^2.

        ``get_acceleration()['x']`` is the left-to-right acceleration, from -8 to 8 g's.

        ``get_acceleration()['y']`` is the forward-to-back acceleration, from of -8 to 8 g's.

        ``get_acceleration()['z']`` is the upward-to-downward acceleration, from -8 to 8 g's."""
        return self.__sensor_manager.accelerometer

    def get_vertical_acceleration(self):
        """This is the upward or downward acceleration regardless of the robot's orientation, from -8 to 8 g's."""
        return self.__sensor_manager.vertical_accel
