from enum import IntEnum
from inspect import signature
from typing import Callable, Dict, List, Coroutine, Optional

from spherov2.commands.animatronic import R2LegActions
from spherov2.commands.core import IntervalOptions
from spherov2.commands.io import AudioPlaybackModes
from spherov2.commands.sensor import CollisionDetectionMethods
from spherov2.controls.enums import RawMotorModes
from spherov2.toy.bb9e import BB9E
from spherov2.toy.bolt import BOLT
from spherov2.toy.core import Toy
from spherov2.toy.mini import Mini
from spherov2.toy.r2d2 import R2D2
from spherov2.toy.r2q5 import R2Q5
from spherov2.toy.rvr import RVR


class ToyUtil:
    @staticmethod
    async def sleep(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'sleep'):
            if len(signature(toy.sleep).parameters) == 0:
                await toy.sleep()
            else:
                await toy.sleep(IntervalOptions.NONE, 0, 0)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def ping(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'ping'):
            le = len(signature(toy.ping).parameters)
            if le == 0:
                await toy.ping()
            elif le == 1:
                await toy.ping(None)
            # elif l == 2: TODO
            #     toy.ping(None, ToyUtil.getPrimaryTargetId(toy))
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def roll_start(toy: Toy, heading: int, speed: int,
                         not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            await toy.drive_control.roll_start(heading, speed)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def roll_stop(toy: Toy, heading: int, is_reverse: bool,
                        not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            if is_reverse:
                heading = (heading + 180) % 360
            await toy.drive_control.roll_stop(heading)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def perform_leg_action(toy: Toy, leg_action: R2LegActions,
                                 not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'perform_leg_action'):
            await toy.perform_leg_action(leg_action)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_stabilization(toy: Toy, stabilize, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            await toy.drive_control.set_stabilization(stabilize)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_raw_motor(toy: Toy, left_mode: RawMotorModes, left_speed: int, right_mode: RawMotorModes,
                            right_speed: int,
                            not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            await toy.drive_control.set_raw_motors(left_mode, left_speed, right_mode, right_speed)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def reset_heading(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            await toy.drive_control.reset_heading()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def play_animation(toy: Toy, animation: IntEnum, wait: bool = False,
                             not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'play_animation'):
            await toy.play_animation(animation, wait)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_head_position(toy: Toy, head_position: float,
                                not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'set_head_position'):
            await toy.set_head_position(head_position)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_main_led(toy: Toy, r: int, g: int, b: int, is_user_color: bool,
                           not_supported_handler: Callable[[], Coroutine] = None):
        async def _fallback():
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

            async def __fallback():
                if hasattr(toy, 'set_main_led'):
                    await toy.set_main_led(r, g, b)
                elif not_supported_handler:
                    await not_supported_handler()

            await ToyUtil.set_multiple_leds(toy, mapping, __fallback)

        await ToyUtil.set_led_matrix_one_colour(toy, r, g, b, _fallback)

    @staticmethod
    async def set_head_led(toy: Toy, brightness: int, not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, BB9E):
            await ToyUtil.set_multiple_leds(toy, {BB9E.LEDs.HEAD: brightness}, not_supported_handler)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_front_led(toy: Toy, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.RIGHT_HEADLIGHT_RED: r,
                RVR.LEDs.RIGHT_HEADLIGHT_GREEN: g,
                RVR.LEDs.RIGHT_HEADLIGHT_BLUE: b,
                RVR.LEDs.LEFT_HEADLIGHT_RED: r,
                RVR.LEDs.LEFT_HEADLIGHT_GREEN: g,
                RVR.LEDs.LEFT_HEADLIGHT_BLUE: b
            }
        elif isinstance(toy, (R2D2, R2Q5, BOLT)):
            mapping = {
                toy.LEDs.FRONT_RED: r,
                toy.LEDs.FRONT_GREEN: g,
                toy.LEDs.FRONT_BLUE: b
            }
        else:
            mapping = None
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_back_led(toy: Toy, r: int, g: int, b: int,
                           not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.RIGHT_BRAKELIGHT_RED: r,
                RVR.LEDs.RIGHT_BRAKELIGHT_GREEN: g,
                RVR.LEDs.RIGHT_BRAKELIGHT_BLUE: b,
                RVR.LEDs.LEFT_BRAKELIGHT_RED: r,
                RVR.LEDs.LEFT_BRAKELIGHT_GREEN: g,
                RVR.LEDs.LEFT_BRAKELIGHT_BLUE: b
            }
        elif isinstance(toy, (R2D2, R2Q5, BOLT)):
            mapping = {
                toy.LEDs.BACK_RED: r,
                toy.LEDs.BACK_GREEN: g,
                toy.LEDs.BACK_BLUE: b
            }
        else:
            mapping = None
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_back_led_brightness(toy: Toy, brightness: int,
                                      not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, (BB9E, Mini)):
            mapping = {
                toy.LEDs.AIMING: brightness
            }
        elif isinstance(toy, (R2D2, R2Q5, BOLT)):
            mapping = {
                toy.LEDs.BACK_RED: 0,
                toy.LEDs.BACK_GREEN: 0,
                toy.LEDs.BACK_BLUE: brightness,
            }
        elif isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.RIGHT_BRAKELIGHT_RED: 0,
                RVR.LEDs.RIGHT_BRAKELIGHT_GREEN: 0,
                RVR.LEDs.RIGHT_BRAKELIGHT_BLUE: brightness,
                RVR.LEDs.LEFT_BRAKELIGHT_RED: 0,
                RVR.LEDs.LEFT_BRAKELIGHT_GREEN: 0,
                RVR.LEDs.LEFT_BRAKELIGHT_BLUE: brightness
            }
        else:
            mapping = None

        async def _fallback():
            if hasattr(toy, 'set_back_led_brightness'):
                await toy.set_back_led_brightness(brightness)
            elif not_supported_handler:
                await not_supported_handler()

        await ToyUtil.set_multiple_leds(toy, mapping, _fallback)

    @staticmethod
    async def set_holo_projector(toy: Toy, brightness: int,
                                 not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, (R2D2, R2Q5)):
            mapping = {toy.LEDs.HOLO_PROJECTOR: brightness}
        else:
            mapping = None
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_logic_display(toy: Toy, brightness: int, not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, (R2D2, R2Q5)):
            mapping = {toy.LEDs.LOGIC_DISPLAYS: brightness}
        else:
            mapping = None
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_multiple_leds(toy: Toy, mapping: Optional[Dict[IntEnum, int]],
                                not_supported_handler: Callable[[], Coroutine] = None):
        if mapping and hasattr(toy, 'multi_led_control'):
            await toy.multi_led_control.set_leds(mapping)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_led_matrix_one_colour(toy: Toy, r: int, g: int, b: int,
                                        not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'set_compressed_frame_player_one_color'):
            await toy.set_compressed_frame_player_one_color(r, g, b)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def turn_off_leds(toy: Toy):
        if hasattr(toy, 'LEDs'):
            mapping = dict((e, 0) for e in toy.LEDs)
        else:
            mapping = None

        async def __fallback():
            await ToyUtil.set_main_led(toy, 0, 0, 0, False)
            await ToyUtil.set_back_led_brightness(toy, 0)

        await ToyUtil.set_multiple_leds(toy, mapping, __fallback)
        await ToyUtil.set_led_matrix_one_colour(toy, 0, 0, 0)

    @staticmethod
    async def play_sound(toy: Toy, sound: IntEnum, force_play: bool,
                         not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'play_audio_file'):
            await toy.play_audio_file(sound,
                                      AudioPlaybackModes.PLAY_IMMEDIATELY if force_play
                                      else AudioPlaybackModes.PLAY_ONLY_IF_NOT_PLAYING)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def enable_sensors(toy: Toy, sensors: List[str], not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'sensor_control'):
            await toy.sensor_control.enable(*sensors)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def disable_sensors(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'sensor_control'):
            await toy.sensor_control.disable_all()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    def add_listeners(toy: Toy, manager):
        if hasattr(toy, 'sensor_control') and hasattr(manager, '_sensor_data_listener'):
            toy.sensor_control.add_sensor_data_listener(manager._sensor_data_listener)
        if hasattr(toy, 'add_collision_detected_notify_listener') and hasattr(manager, '_collision_detected_notify'):
            toy.add_collision_detected_notify_listener(manager._collision_detected_notify)
        if hasattr(toy, 'add_battery_state_changed_notify_listener') and \
                hasattr(manager, '_battery_state_changed_notify'):
            toy.add_battery_state_changed_notify_listener(manager._battery_state_changed_notify)
        if hasattr(toy, 'add_gyro_max_notify_listener') and hasattr(manager, '_gyro_max_notify'):
            toy.add_gyro_max_notify_listener(manager._gyro_max_notify)
        if hasattr(toy, 'add_will_sleep_notify_listener') and hasattr(manager, '_will_sleep_notify'):
            toy.add_will_sleep_notify_listener(manager._will_sleep_notify)

    @staticmethod
    async def set_locator_flags(toy: Toy, flag: bool, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'set_locator_flags'):
            await toy.set_locator_flags(flag)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def reset_locator(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'configure_locator'):
            await toy.configure_locator(0, 0, 0, 0)
        elif hasattr(toy, 'reset_locator_x_and_y'):
            await toy.reset_locator_x_and_y()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def configure_collision_detection(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        x, y, t = 90, 130, 1
        if hasattr(toy, 'configure_collision_detection'):
            await toy.configure_collision_detection(
                CollisionDetectionMethods.ACCELEROMETER_BASED_DETECTION, x, y, x, y, t)
        # TODO other toys
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_power_notifications(toy: Toy, enable: bool,
                                      not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'enable_charger_state_changed_notify'):
            await toy.enable_charger_state_changed_notify(enable)
        elif hasattr(toy, 'enable_battery_state_changed_notify'):
            await toy.enable_battery_state_changed_notify(enable)
        elif hasattr(toy, 'enable_battery_voltage_state_change_notify'):
            await toy.enable_battery_voltage_state_change_notify(enable)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_robot_state_on_start(toy: Toy):
        # TODO setUserColour
        await ToyUtil.reset_heading(toy)
        await ToyUtil.set_head_position(toy, 0)
        await ToyUtil.perform_leg_action(toy, R2LegActions.THREE_LEGS)
        await ToyUtil.set_locator_flags(toy, False)
        await ToyUtil.configure_collision_detection(toy)
        await ToyUtil.set_power_notifications(toy, True)
        if hasattr(toy, 'enable_gyro_max_notify'):
            await toy.enable_gyro_max_notify(True)
        if hasattr(toy, 'sensor_control'):
            await toy.sensor_control.set_interval(150)
        await ToyUtil.turn_off_leds(toy)
        '''if (toy instanceof HasSpheroRVRToy) {
                setColorDetection$default(toy, true, (Function0) null, 2, (Object) null);
                resetHeading$default(toy, (Function0) null, 1, (Object) null);
            }'''
        await ToyUtil.reset_locator(toy)
