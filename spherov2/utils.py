from enum import IntEnum
from typing import Callable, Any, Dict

from spherov2.command.animatronic import R2LegActions
from spherov2.controls.enums import RawMotorModes
from spherov2.toy.core import Toy
from spherov2.toy.r2d2 import R2D2
from spherov2.toy.r2q5 import R2Q5


class ToyUtil:
    @staticmethod
    def roll_start(toy: Toy, heading: int, speed: int, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.roll_start(heading, speed)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def roll_stop(toy: Toy, heading: int, is_reverse: bool, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'drive_control'):
            if is_reverse:
                heading = (heading + 180) % 360
            toy.drive_control.roll_stop(heading)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def perform_leg_action(toy: Toy, leg_action: R2LegActions, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'perform_leg_action'):
            toy.perform_leg_action(leg_action)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_stabilization(toy: Toy, stabilize, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.set_stabilization(stabilize)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_raw_motor(toy: Toy, left_mode: RawMotorModes, left_speed: int, right_mode: RawMotorModes, right_speed: int,
                      not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.set_raw_motors(left_mode, left_speed, right_mode, right_speed)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def reset_heading(toy: Toy, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.reset_heading()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def play_animation(toy: Toy, animation: IntEnum, wait: bool = False,
                       not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'play_animation'):
            toy.play_animation(animation, wait)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_head_position(toy: Toy, head_position: int, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'set_head_position'):
            toy.set_head_position(head_position)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_main_led(toy: Toy, r: int, g: int, b: int, is_user_color: bool,
                     not_supported_handler: Callable[[], Any] = None):
        def _fallback():
            # TODO toys other than R2Q5
            if isinstance(toy, (R2D2, R2Q5)):
                mapping = {
                    toy.LEDs.BACK_RED: r,
                    toy.LEDs.BACK_GREEN: g,
                    toy.LEDs.BACK_BLUE: b,
                    toy.LEDs.FRONT_RED: r,
                    toy.LEDs.FRONT_GREEN: g,
                    toy.LEDs.FRONT_BLUE: b
                }
            else:
                mapping = None

            def __fallback():
                if hasattr(toy, 'set_main_led'):
                    toy.set_main_led(r, g, b)
                elif not_supported_handler:
                    not_supported_handler()

            ToyUtil.set_multiple_leds(toy, mapping, __fallback)

        ToyUtil.set_led_matrix_one_colour(toy, r, g, b, _fallback)

    @staticmethod
    def set_back_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Any] = None):
        # TODO: other toys
        if isinstance(toy, (R2D2, R2Q5)):
            mapping = {
                toy.LEDs.BACK_RED: r,
                toy.LEDs.BACK_GREEN: g,
                toy.LEDs.BACK_BLUE: b
            }
        else:
            mapping = None
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_back_led_brightness(toy: Toy, brightness: int, not_supported_handler: Callable[[], Any] = None):
        # setMultipleLEDs(toy, MapsKt.mapOf(TuplesKt.to(HasBB9EToy.LEDs.AIMING, Integer.valueOf(i)),
        # TuplesKt.to(HasSpheroMiniToy.LEDs.AIMING, Integer.valueOf(i)),
        # TuplesKt.to(HasSpheroBoltToy.LEDs.BACK_RED, 0),
        # TuplesKt.to(HasSpheroBoltToy.LEDs.BACK_GREEN, 0),
        # TuplesKt.to(HasSpheroBoltToy.LEDs.BACK_BLUE, Integer.valueOf(i)),
        # TuplesKt.to(HasSpheroRVRToy.LEDs.LEFT_BRAKELIGHT_RED, 0),
        # TuplesKt.to(HasSpheroRVRToy.LEDs.LEFT_BRAKELIGHT_GREEN, 0),
        # TuplesKt.to(HasSpheroRVRToy.LEDs.LEFT_BRAKELIGHT_BLUE, Integer.valueOf(i)),
        # TuplesKt.to(HasSpheroRVRToy.LEDs.RIGHT_BRAKELIGHT_RED, 0),
        # TuplesKt.to(HasSpheroRVRToy.LEDs.RIGHT_BRAKELIGHT_GREEN, 0),
        # TuplesKt.to(HasSpheroRVRToy.LEDs.RIGHT_BRAKELIGHT_BLUE, Integer.valueOf(i))),
        # new ToyUtil$setBackLEDBrightness$1(toy, i, function0));
        if isinstance(toy, (R2D2, R2Q5)):
            mapping = {
                toy.LEDs.BACK_RED: 0,
                toy.LEDs.BACK_GREEN: 0,
                toy.LEDs.BACK_BLUE: brightness,
            }
        else:
            mapping = None

        def _fallback():
            if hasattr(toy, 'set_back_led_brightness'):
                toy.set_back_led_brightness(brightness)
            elif not_supported_handler:
                not_supported_handler()

        ToyUtil.set_multiple_leds(toy, mapping, _fallback)

    @staticmethod
    def set_multiple_leds(toy: Toy, mapping: Dict[IntEnum, int], not_supported_handler: Callable[[], Any] = None):
        if mapping and hasattr(toy, 'multi_led_control'):
            toy.multi_led_control.set_leds(mapping)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_led_matrix_one_colour(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Any] = None):
        if hasattr(toy, 'set_compressed_frame_player_one_color'):
            toy.set_compressed_frame_player_one_color(r, g, b)
        elif not_supported_handler:
            not_supported_handler()
