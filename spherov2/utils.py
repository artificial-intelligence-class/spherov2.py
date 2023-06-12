from enum import IntEnum
from typing import Callable, Dict, List, Iterable, Coroutine

from spherov2.commands.animatronic import R2LegActions, Animatronic
from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.core import IntervalOptions, Core
from spherov2.commands.io import AudioPlaybackModes, IO, FrameRotationOptions, FadeOverrideOptions
from spherov2.commands.power import Power
from spherov2.commands.sensor import CollisionDetectionMethods, Sensor, SensitivityBasedCollisionDetectionMethods, \
    SensitivityLevels
from spherov2.commands.sphero import CollisionDetectionMethods as SpheroCollisionDetectionMethods, Sphero
from spherov2.controls import RawMotorModes
from spherov2.controls.v2 import Processors
from spherov2.toy import Toy
from spherov2.toy.bb9e import BB9E
from spherov2.toy.bolt import BOLT
from spherov2.toy.mini import Mini
from spherov2.toy.r2d2 import R2D2
from spherov2.toy.r2q5 import R2Q5
from spherov2.toy.rvr import RVR
from spherov2.types import Color


class ToyUtil:
    @staticmethod
    async def sleep(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Core.sleep):
            await toy.sleep(IntervalOptions.NONE, 0, 0)
        elif toy.implements(Power.sleep):
            await toy.sleep()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def ping(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Core.ping):
            await toy.ping()
        elif toy.implements(ApiAndShell.ping):
            await toy.ping(None)
        elif toy.implements(ApiAndShell.ping, True):
            await toy.ping(None, Processors.PRIMARY)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def roll_start(toy: Toy, heading: int, speed: int, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            await toy.drive_control.roll_start(heading, speed)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def roll_stop(toy: Toy, heading: int, is_reverse: bool, not_supported_handler: Callable[[], Coroutine] = None):
        if hasattr(toy, 'drive_control'):
            if is_reverse:
                heading = (heading + 180) % 360
            await toy.drive_control.roll_stop(heading)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def perform_leg_action(toy: Toy, leg_action: R2LegActions, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Animatronic.perform_leg_action):
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
    async def set_raw_motor(toy: Toy, left_mode: RawMotorModes, left_speed: int, right_mode: RawMotorModes, right_speed: int,
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
        if toy.implements(Animatronic.play_animation):
            await toy.play_animation(animation, wait)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_head_position(toy: Toy, head_position: float, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Animatronic.set_head_position):
            await toy.set_head_position(head_position)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_main_led(toy: Toy, r: int, g: int, b: int, is_user_color: bool,
                     not_supported_handler: Callable[[], Coroutine] = None):
        async def _fallback():
            if isinstance(toy, (R2D2, R2Q5)):
                mapping = {
                    toy.LEDs.BACK_RED: r,
                    toy.LEDs.BACK_GREEN: g,
                    toy.LEDs.BACK_BLUE: b,
                    toy.LEDs.FRONT_RED: r,
                    toy.LEDs.FRONT_GREEN: g,
                    toy.LEDs.FRONT_BLUE: b
                }
            elif isinstance(toy, BB9E):
                mapping = {
                    toy.LEDs.BODY_RED: r,
                    toy.LEDs.BODY_GREEN: g,
                    toy.LEDs.BODY_BLUE: b
                }
            elif isinstance(toy, Mini):
                mapping = {
                    toy.LEDs.BODY_RED: r,
                    toy.LEDs.BODY_GREEN: g,
                    toy.LEDs.BODY_BLUE: b,
                    toy.LEDs.USER_BODY_RED: r,
                    toy.LEDs.USER_BODY_GREEN: g,
                    toy.LEDs.USER_BODY_BLUE: b
                }
            elif isinstance(toy, RVR):
                mapping = {
                    toy.LEDs.RIGHT_HEADLIGHT_RED: r,
                    toy.LEDs.RIGHT_HEADLIGHT_GREEN: g,
                    toy.LEDs.RIGHT_HEADLIGHT_BLUE: b,
                    toy.LEDs.LEFT_HEADLIGHT_RED: r,
                    toy.LEDs.LEFT_HEADLIGHT_GREEN: g,
                    toy.LEDs.LEFT_HEADLIGHT_BLUE: b,
                    toy.LEDs.LEFT_STATUS_INDICATION_RED: r,
                    toy.LEDs.LEFT_STATUS_INDICATION_GREEN: g,
                    toy.LEDs.LEFT_STATUS_INDICATION_BLUE: b,
                    toy.LEDs.RIGHT_STATUS_INDICATION_RED: r,
                    toy.LEDs.RIGHT_STATUS_INDICATION_GREEN: g,
                    toy.LEDs.RIGHT_STATUS_INDICATION_BLUE: b,
                    toy.LEDs.BATTERY_DOOR_FRONT_RED: r,
                    toy.LEDs.BATTERY_DOOR_FRONT_GREEN: g,
                    toy.LEDs.BATTERY_DOOR_FRONT_BLUE: b,
                    toy.LEDs.BATTERY_DOOR_REAR_RED: r,
                    toy.LEDs.BATTERY_DOOR_REAR_GREEN: g,
                    toy.LEDs.BATTERY_DOOR_REAR_BLUE: b,
                    toy.LEDs.POWER_BUTTON_FRONT_RED: r,
                    toy.LEDs.POWER_BUTTON_FRONT_GREEN: g,
                    toy.LEDs.POWER_BUTTON_FRONT_BLUE: b,
                    toy.LEDs.POWER_BUTTON_REAR_RED: r,
                    toy.LEDs.POWER_BUTTON_REAR_GREEN: g,
                    toy.LEDs.POWER_BUTTON_REAR_BLUE: b,
                    toy.LEDs.LEFT_BRAKELIGHT_RED: r,
                    toy.LEDs.LEFT_BRAKELIGHT_GREEN: g,
                    toy.LEDs.LEFT_BRAKELIGHT_BLUE: b,
                    toy.LEDs.RIGHT_BRAKELIGHT_RED: r,
                    toy.LEDs.RIGHT_BRAKELIGHT_GREEN: g,
                    toy.LEDs.RIGHT_BRAKELIGHT_BLUE: b
                }
            else:
                mapping = None

            async def __fallback():
                if toy.implements(Sphero.set_main_led):
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
    async def set_front_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
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
        elif isinstance(toy, Mini):
            mapping = {
                toy.LEDs.BODY_RED: r,
                toy.LEDs.BODY_GREEN: g,
                toy.LEDs.BODY_BLUE: b
            }
        else:
            mapping = None
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_back_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
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
        elif isinstance(toy, Mini):
            mapping = {
                toy.LEDs.USER_BODY_RED: r,
                toy.LEDs.USER_BODY_GREEN: g,
                toy.LEDs.USER_BODY_BLUE: b
            }
        else:
            mapping = None
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_back_led_brightness(toy: Toy, brightness: int, not_supported_handler: Callable[[], Coroutine] = None):
        if isinstance(toy, (R2D2, R2Q5, BOLT)):
            mapping = {
                toy.LEDs.BACK_RED: 0,
                toy.LEDs.BACK_GREEN: 0,
                toy.LEDs.BACK_BLUE: brightness,
            }
        elif isinstance(toy, (BB9E, Mini)):
            mapping = {
                toy.LEDs.AIMING: brightness
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
            if toy.implements(Sphero.set_back_led_brightness):
                await toy.set_back_led_brightness(brightness)
            elif not_supported_handler:
                await not_supported_handler()

        await ToyUtil.set_multiple_leds(toy, mapping, _fallback)

    @staticmethod
    async def set_left_front_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.LEFT_HEADLIGHT_RED: r,
                RVR.LEDs.LEFT_HEADLIGHT_GREEN: g,
                RVR.LEDs.LEFT_HEADLIGHT_BLUE: b
            }
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_right_front_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.RIGHT_HEADLIGHT_RED: r,
                RVR.LEDs.RIGHT_HEADLIGHT_GREEN: g,
                RVR.LEDs.RIGHT_HEADLIGHT_BLUE: b
            }
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_battery_side_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.BATTERY_DOOR_FRONT_RED: r,
                RVR.LEDs.BATTERY_DOOR_FRONT_GREEN: g,
                RVR.LEDs.BATTERY_DOOR_FRONT_BLUE: b
            }
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_power_side_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.POWER_BUTTON_FRONT_RED: r,
                RVR.LEDs.POWER_BUTTON_FRONT_GREEN: g,
                RVR.LEDs.POWER_BUTTON_FRONT_BLUE: b
            }
        await ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    async def set_holo_projector(toy: Toy, brightness: int, not_supported_handler: Callable[[], Coroutine] = None):
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
    async def set_multiple_leds(toy: Toy, mapping: Dict[IntEnum, int], not_supported_handler: Callable[[], Coroutine] = None):
        if mapping and hasattr(toy, 'multi_led_control'):
            await toy.multi_led_control.set_leds(mapping)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_led_matrix_one_colour(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.set_compressed_frame_player_one_color):
            await toy.set_compressed_frame_player_one_color(r, g, b)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_matrix_pixel(toy: Toy, x: int, y: int, r: int, g: int, b: int, is_user_color: bool,
                         not_supported_handler: Callable[[], Coroutine] = None):
        async def _fallback():
            await not_supported_handler()

        await ToyUtil.set_led_matrix_pixel(toy, x, y, r, g, b, _fallback)

    @staticmethod
    async def set_led_matrix_pixel(toy: Toy, x: int, y: int, r: int, g: int, b: int,
                             not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.set_compressed_frame_player_pixel):
            await toy.set_compressed_frame_player_pixel(x, y, r, g, b)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_matrix_line(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, is_user_color: bool,
                        not_supported_handler: Callable[[], Coroutine] = None):
        async def _fallback():
            await not_supported_handler()

        await ToyUtil.set_led_matrix_line(toy, x1, y1, x2, y2, r, g, b, _fallback)

    @staticmethod
    async def set_led_matrix_line(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.draw_compressed_frame_player_line):
            await toy.draw_compressed_frame_player_line(x1, y1, x2, y2, r, g, b)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_matrix_fill(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, is_user_color: bool,
                        not_supported_handler: Callable[[], Coroutine] = None):
        async def _fallback():
            await not_supported_handler()

        await ToyUtil.set_led_matrix_fill(toy, x1, y1, x2, y2, r, g, b, _fallback)

    @staticmethod
    async def set_led_matrix_fill(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.draw_compressed_frame_player_fill):
            await toy.draw_compressed_frame_player_fill(x1, y1, x2, y2, r, g, b)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_matrix_rotation(toy: Toy, rotation:FrameRotationOptions, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.set_compressed_frame_player_frame_rotation):
            await toy.set_compressed_frame_player_frame_rotation(rotation)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def turn_off_leds(toy: Toy):
        if hasattr(toy, 'LEDs'):
            mapping = dict((e, 0) for e in toy.LEDs)
        else:
            mapping = None

        if isinstance(toy, RVR):
            mapping.pop(RVR.LEDs.UNDERCARRIAGE_WHITE)

        async def __fallback():
            await ToyUtil.set_main_led(toy, 0, 0, 0, False)
            await ToyUtil.set_back_led_brightness(toy, 0)

        await ToyUtil.set_multiple_leds(toy, mapping, __fallback)
        await ToyUtil.set_led_matrix_one_colour(toy, 0, 0, 0)

    # Bolt Animation
    @staticmethod
    async def save_compressed_frame_player_animation(toy: Toy, animation_id, fps, fade_animation, palette_colors, frames_indexes,
                                  not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.save_compressed_frame_player_animation):
            await toy.save_compressed_frame_player_animation(animation_id, fps, fade_animation, palette_colors, frames_indexes)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def save_compressed_frame_player64_bit_frame(toy: Toy, frame_index, compressed_frame,
                                               not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.save_compressed_frame_player64_bit_frame):
            await toy.save_compressed_frame_player64_bit_frame(frame_index, compressed_frame)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def play_compressed_frame_player_animation_with_loop_option(toy: Toy, animation_id, loop, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.play_compressed_frame_player_animation_with_loop_option):
            await toy.play_compressed_frame_player_animation_with_loop_option(animation_id, loop)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def override_compressed_frame_player_animation_global_settings(toy: Toy, fps:int, fade_options:FadeOverrideOptions, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.override_compressed_frame_player_animation_global_settings):
            await toy.override_compressed_frame_player_animation_global_settings(fps, fade_options)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def reset_compressed_frame_player_animation(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.reset_compressed_frame_player_animation):
            await toy.reset_compressed_frame_player_animation()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def resume_compressed_frame_player_animation(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.resume_compressed_frame_player_animation):
            await toy.resume_compressed_frame_player_animation()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def pause_compressed_frame_player_animation(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.pause_compressed_frame_player_animation):
            await toy.pause_compressed_frame_player_animation()
        elif not_supported_handler:
            await not_supported_handler()

    # Sound
    @staticmethod
    async def play_sound(toy: Toy, sound: IntEnum, force_play: bool, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.play_audio_file):
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
    async def get_ambient_light_sensor_value(toy: Toy):
        return await toy.get_ambient_light_sensor_value()

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
        if hasattr(toy, 'add_robot_to_robot_infrared_message_received_notify_listener') and \
                hasattr(manager, '_robot_to_robot_infrared_message_received_notify'):
            toy.add_robot_to_robot_infrared_message_received_notify_listener(
                manager._robot_to_robot_infrared_message_received_notify)
        if hasattr(toy, 'add_sensor_streaming_data_notify_listener'):
            toy.add_sensor_streaming_data_notify_listener(manager._sensor_streaming_data_notify)
        if hasattr(toy, 'add_magnetometer_north_yaw_notify_listener'):
            toy.add_magnetometer_north_yaw_notify_listener(manager._magnetometer_north_yaw_notify)

    @staticmethod
    async def set_locator_flags(toy: Toy, flag: bool, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.set_locator_flags):
            await toy.set_locator_flags(flag)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def reset_locator(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sphero.configure_locator):
            await toy.configure_locator(0, 0, 0, 0)
        elif toy.implements(Sensor.reset_locator_x_and_y):
            await toy.reset_locator_x_and_y()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def configure_collision_detection(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        x, y, t = 90, 130, 1
        if toy.implements(Sensor.configure_collision_detection):
            await toy.configure_collision_detection(CollisionDetectionMethods.ACCELEROMETER_BASED_DETECTION, x, y, x, y, t)
        elif toy.implements(Sphero.configure_collision_detection):
            await toy.configure_collision_detection(SpheroCollisionDetectionMethods.DEFAULT, x, y, x, y, t)
        elif toy.implements(Sensor.configure_sensitivity_based_collision_detection):
            await toy.configure_sensitivity_based_collision_detection(
                SensitivityBasedCollisionDetectionMethods.ACCELEROMETER_BASED_DETECTION, SensitivityLevels.VERY_HIGH, t)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def start_robot_to_robot_infrared_broadcasting(toy: Toy, far: int, near: int,
                                                   not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.start_robot_to_robot_infrared_broadcasting):
            await toy.start_robot_to_robot_infrared_broadcasting(far, near)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def stop_robot_to_robot_infrared_broadcasting(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.stop_robot_to_robot_infrared_broadcasting):
            await toy.stop_robot_to_robot_infrared_broadcasting()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def start_robot_to_robot_infrared_following(toy: Toy, far: int, near: int,
                                                not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.start_robot_to_robot_infrared_following):
            await toy.start_robot_to_robot_infrared_following(far, near)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def stop_robot_to_robot_infrared_following(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.stop_robot_to_robot_infrared_following):
            await toy.stop_robot_to_robot_infrared_following()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def start_robot_to_robot_infrared_evading(toy: Toy, far: int, near: int,
                                              not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.start_robot_to_robot_infrared_evading):
            await toy.start_robot_to_robot_infrared_evading(far, near)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def stop_robot_to_robot_infrared_evading(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.stop_robot_to_robot_infrared_evading):
            await toy.stop_robot_to_robot_infrared_evading()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def send_robot_to_robot_infrared_message(toy: Toy, channel: int, intensity: int,
                                             not_supported_handler: Callable[[], Coroutine] = None):
        # if toy.implements(Sensor.send_robot_to_robot_infrared_message): TODO: BOLT
        #     toy.send_robot_to_robot_infrared_message(channel, intensity, intensity, intensity, intensity)
        if toy.implements(Sensor.send_infrared_message):
            await toy.send_infrared_message(channel, intensity, intensity, intensity, intensity)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def listen_for_robot_to_robot_infrared_message(toy: Toy, channels: Iterable[int], duration: int,
                                                   not_supported_handler: Callable[[], Coroutine] = None):
        # TODO: BOLT
        if toy.implements(Sensor.enable_robot_infrared_message_notify):
            await toy.enable_robot_infrared_message_notify(True)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_power_notifications(toy: Toy, enable: bool, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Power.enable_charger_state_changed_notify):
            await toy.enable_charger_state_changed_notify(enable)
        elif toy.implements(Power.enable_battery_state_changed_notify):
            await toy.enable_battery_state_changed_notify(enable)
        elif toy.implements(Power.enable_battery_voltage_state_change_notify):
            await toy.enable_battery_voltage_state_change_notify(enable)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def calibrate_compass(toy: Toy, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.magnetometer_calibrate_to_north):
            await toy.magnetometer_calibrate_to_north()
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def scroll_matrix_text(toy: Toy, text:str, color: Color, fps: int, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.set_compressed_frame_player_text_scrolling):
            await toy.set_compressed_frame_player_text_scrolling(text, color.r, color.g, color.b, fps, False)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_matrix_character(toy: Toy, character: str, color: Color, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(IO.set_compressed_frame_player_single_character):
            await toy.set_compressed_frame_player_single_character(color.r, color.g, color.b, character)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_color_detection(toy: Toy, enable: bool, not_supported_handler: Callable[[], Coroutine] = None):
        if toy.implements(Sensor.enable_color_detection):
            await toy.enable_color_detection(enable)
        elif not_supported_handler:
            await not_supported_handler()

    @staticmethod
    async def set_robot_state_on_start(toy: Toy):
        # TODO setUserColour
        await ToyUtil.set_head_position(toy, 0)
        await ToyUtil.perform_leg_action(toy, R2LegActions.THREE_LEGS)
        await ToyUtil.set_locator_flags(toy, False)
        await ToyUtil.configure_collision_detection(toy)
        await ToyUtil.set_power_notifications(toy, True)
        if toy.implements(Sensor.enable_gyro_max_notify):
            await toy.enable_gyro_max_notify(True)
        if hasattr(toy, 'sensor_control'):
            await toy.sensor_control.set_interval(150)
        await ToyUtil.turn_off_leds(toy)
        if isinstance(toy, RVR):
            await ToyUtil.set_color_detection(toy, True)
            await ToyUtil.reset_heading(toy)
        await ToyUtil.reset_locator(toy)
