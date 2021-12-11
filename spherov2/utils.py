from enum import IntEnum
from typing import Callable, Dict, List, Iterable

from spherov2.commands.animatronic import R2LegActions, Animatronic
from spherov2.commands.api_and_shell import ApiAndShell
from spherov2.commands.core import IntervalOptions, Core
from spherov2.commands.io import AudioPlaybackModes, IO
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


class ToyUtil:
    @staticmethod
    def sleep(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Core.sleep):
            toy.sleep(IntervalOptions.NONE, 0, 0)
        elif toy.implements(Power.sleep):
            toy.sleep()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def ping(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Core.ping):
            toy.ping()
        elif toy.implements(ApiAndShell.ping):
            toy.ping(None)
        elif toy.implements(ApiAndShell.ping, True):
            toy.ping(None, Processors.PRIMARY)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def roll_start(toy: Toy, heading: int, speed: int, not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.roll_start(heading, speed)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def roll_stop(toy: Toy, heading: int, is_reverse: bool, not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'drive_control'):
            if is_reverse:
                heading = (heading + 180) % 360
            toy.drive_control.roll_stop(heading)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def perform_leg_action(toy: Toy, leg_action: R2LegActions, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Animatronic.perform_leg_action):
            toy.perform_leg_action(leg_action)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_stabilization(toy: Toy, stabilize, not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.set_stabilization(stabilize)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_raw_motor(toy: Toy, left_mode: RawMotorModes, left_speed: int, right_mode: RawMotorModes, right_speed: int,
                      not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.set_raw_motors(left_mode, left_speed, right_mode, right_speed)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def reset_heading(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'drive_control'):
            toy.drive_control.reset_heading()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def play_animation(toy: Toy, animation: IntEnum, wait: bool = False,
                       not_supported_handler: Callable[[], None] = None):
        if toy.implements(Animatronic.play_animation):
            toy.play_animation(animation, wait)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_head_position(toy: Toy, head_position: float, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Animatronic.set_head_position):
            toy.set_head_position(head_position)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_main_led(toy: Toy, r: int, g: int, b: int, is_user_color: bool,
                     not_supported_handler: Callable[[], None] = None):
        def _fallback():
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

            def __fallback():
                if toy.implements(Sphero.set_main_led):
                    toy.set_main_led(r, g, b)
                elif not_supported_handler:
                    not_supported_handler()

            ToyUtil.set_multiple_leds(toy, mapping, __fallback)

        ToyUtil.set_led_matrix_one_colour(toy, r, g, b, _fallback)

    @staticmethod
    def set_head_led(toy: Toy, brightness: int, not_supported_handler: Callable[[], None] = None):
        if isinstance(toy, BB9E):
            ToyUtil.set_multiple_leds(toy, {BB9E.LEDs.HEAD: brightness}, not_supported_handler)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_front_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
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
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_back_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
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
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_back_led_brightness(toy: Toy, brightness: int, not_supported_handler: Callable[[], None] = None):
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

        def _fallback():
            if toy.implements(Sphero.set_back_led_brightness):
                toy.set_back_led_brightness(brightness)
            elif not_supported_handler:
                not_supported_handler()

        ToyUtil.set_multiple_leds(toy, mapping, _fallback)

    @staticmethod
    def set_left_front_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.LEFT_HEADLIGHT_RED: r,
                RVR.LEDs.LEFT_HEADLIGHT_GREEN: g,
                RVR.LEDs.LEFT_HEADLIGHT_BLUE: b
            }
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_right_front_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.RIGHT_HEADLIGHT_RED: r,
                RVR.LEDs.RIGHT_HEADLIGHT_GREEN: g,
                RVR.LEDs.RIGHT_HEADLIGHT_BLUE: b
            }
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_battery_side_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.BATTERY_DOOR_FRONT_RED: r,
                RVR.LEDs.BATTERY_DOOR_FRONT_GREEN: g,
                RVR.LEDs.BATTERY_DOOR_FRONT_BLUE: b
            }
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_power_side_led(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
        mapping = None
        if isinstance(toy, RVR):
            mapping = {
                RVR.LEDs.POWER_BUTTON_FRONT_RED: r,
                RVR.LEDs.POWER_BUTTON_FRONT_GREEN: g,
                RVR.LEDs.POWER_BUTTON_FRONT_BLUE: b
            }
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_holo_projector(toy: Toy, brightness: int, not_supported_handler: Callable[[], None] = None):
        if isinstance(toy, (R2D2, R2Q5)):
            mapping = {toy.LEDs.HOLO_PROJECTOR: brightness}
        else:
            mapping = None
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_logic_display(toy: Toy, brightness: int, not_supported_handler: Callable[[], None] = None):
        if isinstance(toy, (R2D2, R2Q5)):
            mapping = {toy.LEDs.LOGIC_DISPLAYS: brightness}
        else:
            mapping = None
        ToyUtil.set_multiple_leds(toy, mapping, not_supported_handler)

    @staticmethod
    def set_multiple_leds(toy: Toy, mapping: Dict[IntEnum, int], not_supported_handler: Callable[[], None] = None):
        if mapping and hasattr(toy, 'multi_led_control'):
            toy.multi_led_control.set_leds(mapping)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_led_matrix_one_colour(toy: Toy, r: int, g: int, b: int, not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.set_compressed_frame_player_one_color):
            toy.set_compressed_frame_player_one_color(r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_matrix_pixel(toy: Toy, x: int, y: int, r: int, g: int, b: int, is_user_color: bool,
                         not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()

        ToyUtil.set_led_matrix_pixel(toy, x, y, r, g, b, _fallback)

    @staticmethod
    def set_led_matrix_pixel(toy: Toy, x: int, y: int, r: int, g: int, b: int,
                             not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.set_compressed_frame_player_pixel):
            toy.set_compressed_frame_player_pixel(x, y, r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_matrix_line(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, is_user_color: bool,
                        not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()

        ToyUtil.set_led_matrix_line(toy, x1, y1, x2, y2, r, g, b, _fallback)

    @staticmethod
    def set_led_matrix_line(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.draw_compressed_frame_player_line):
            toy.draw_compressed_frame_player_line(x1, y1, x2, y2, r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_matrix_fill(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, is_user_color: bool,
                        not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()

        ToyUtil.set_led_matrix_fill(toy, x1, y1, x2, y2, r, g, b, _fallback)

    @staticmethod
    def set_led_matrix_fill(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.draw_compressed_frame_player_fill):
            toy.draw_compressed_frame_player_fill(x1, y1, x2, y2, r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_matrix_pixel(toy: Toy, x: int, y: int, r: int, g: int, b: int, is_user_color: bool,
                         not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()

        ToyUtil.set_led_matrix_pixel(toy, x, y, r, g, b, _fallback)

    @staticmethod
    def set_led_matrix_pixel(toy: Toy, x: int, y: int, r: int, g: int, b: int,
                             not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.set_compressed_frame_player_pixel):
            toy.set_compressed_frame_player_pixel(x, y, r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_matrix_line(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, is_user_color: bool,
                        not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()

        ToyUtil.set_led_matrix_line(toy, x1, y1, x2, y2, r, g, b, _fallback)

    @staticmethod
    def set_led_matrix_line(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.draw_compressed_frame_player_line):
            toy.draw_compressed_frame_player_line(x1, y1, x2, y2, r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_matrix_fill(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, is_user_color: bool,
                        not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()

        ToyUtil.set_led_matrix_fill(toy, x1, y1, x2, y2, r, g, b, _fallback)

    @staticmethod
    def set_led_matrix_fill(toy: Toy, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int,
                            not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.draw_compressed_frame_player_fill):
            toy.draw_compressed_frame_player_fill(x1, y1, x2, y2, r, g, b)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def turn_off_leds(toy: Toy):
        if hasattr(toy, 'LEDs'):
            mapping = dict((e, 0) for e in toy.LEDs)
        else:
            mapping = None

        if isinstance(toy, RVR):
            mapping.pop(RVR.LEDs.UNDERCARRIAGE_WHITE)

        def __fallback():
            ToyUtil.set_main_led(toy, 0, 0, 0, False)
            ToyUtil.set_back_led_brightness(toy, 0)

        ToyUtil.set_multiple_leds(toy, mapping, __fallback)
        ToyUtil.set_led_matrix_one_colour(toy, 0, 0, 0)

    # Bolt Animation
    def register_matrix_animation(toy: Toy, s, s2, z, s3, s_arr, i, i_arr,
                                  not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()
        ToyUtil.save_compressed_frame_player_animation(toy, s, s2, z, s3, s_arr, i, i_arr, _fallback)

    def save_compressed_frame_player_animation(toy: Toy, s, s2, z, s3, s_arr, i, i_arr,
                                               not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.save_compressed_frame_player_animation):
            toy.save_compressed_frame_player_animation(s, s2, z, s3, s_arr, i, i_arr)
        elif not_supported_handler:
            not_supported_handler()

    def play_matrix_animation(toy: Toy, s, not_supported_handler: Callable[[], None] = None):
        def _fallback():
            not_supported_handler()
        #TODO: Add correct call #ToyUtil.save_compressed_frame_player_animation(toy, s, s2, z, s3, s_arr, i, i_arr, _fallback)

    def play_compressed_frame_player_animation(toy: Toy, s, not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.play_compressed_frame_player_animation):
            toy.play_compressed_frame_player_animation(s)
        elif not_supported_handler:
            not_supported_handler()

    # Sound
    @staticmethod
    def play_sound(toy: Toy, sound: IntEnum, force_play: bool, not_supported_handler: Callable[[], None] = None):
        if toy.implements(IO.play_audio_file):
            toy.play_audio_file(sound,
                                AudioPlaybackModes.PLAY_IMMEDIATELY if force_play
                                else AudioPlaybackModes.PLAY_ONLY_IF_NOT_PLAYING)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def enable_sensors(toy: Toy, sensors: List[str], not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'sensor_control'):
            toy.sensor_control.enable(*sensors)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def disable_sensors(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if hasattr(toy, 'sensor_control'):
            toy.sensor_control.disable_all()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def get_ambient_light_sensor_value(toy: Toy):
        return toy.get_ambient_light_sensor_value()

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
    def set_locator_flags(toy: Toy, flag: bool, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.set_locator_flags):
            toy.set_locator_flags(flag)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def reset_locator(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sphero.configure_locator):
            toy.configure_locator(0, 0, 0, 0)
        elif toy.implements(Sensor.reset_locator_x_and_y):
            toy.reset_locator_x_and_y()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def configure_collision_detection(toy: Toy, not_supported_handler: Callable[[], None] = None):
        x, y, t = 90, 130, 1
        if toy.implements(Sensor.configure_collision_detection):
            toy.configure_collision_detection(CollisionDetectionMethods.ACCELEROMETER_BASED_DETECTION, x, y, x, y, t)
        elif toy.implements(Sphero.configure_collision_detection):
            toy.configure_collision_detection(SpheroCollisionDetectionMethods.DEFAULT, x, y, x, y, t)
        elif toy.implements(Sensor.configure_sensitivity_based_collision_detection):
            toy.configure_sensitivity_based_collision_detection(
                SensitivityBasedCollisionDetectionMethods.ACCELEROMETER_BASED_DETECTION, SensitivityLevels.VERY_HIGH, t)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def start_robot_to_robot_infrared_broadcasting(toy: Toy, far: int, near: int,
                                                   not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.start_robot_to_robot_infrared_broadcasting):
            toy.start_robot_to_robot_infrared_broadcasting(far, near)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def stop_robot_to_robot_infrared_broadcasting(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.stop_robot_to_robot_infrared_broadcasting):
            toy.stop_robot_to_robot_infrared_broadcasting()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def start_robot_to_robot_infrared_following(toy: Toy, far: int, near: int,
                                                not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.start_robot_to_robot_infrared_following):
            toy.start_robot_to_robot_infrared_following(far, near)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def stop_robot_to_robot_infrared_following(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.stop_robot_to_robot_infrared_following):
            toy.stop_robot_to_robot_infrared_following()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def start_robot_to_robot_infrared_evading(toy: Toy, far: int, near: int,
                                              not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.start_robot_to_robot_infrared_evading):
            toy.start_robot_to_robot_infrared_evading(far, near)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def stop_robot_to_robot_infrared_evading(toy: Toy, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.stop_robot_to_robot_infrared_evading):
            toy.stop_robot_to_robot_infrared_evading()
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def send_robot_to_robot_infrared_message(toy: Toy, channel: int, intensity: int,
                                             not_supported_handler: Callable[[], None] = None):
        # if toy.implements(Sensor.send_robot_to_robot_infrared_message): TODO: BOLT
        #     toy.send_robot_to_robot_infrared_message(channel, intensity, intensity, intensity, intensity)
        if toy.implements(Sensor.send_infrared_message):
            toy.send_infrared_message(channel, intensity, intensity, intensity, intensity)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def listen_for_robot_to_robot_infrared_message(toy: Toy, channels: Iterable[int], duration: int,
                                                   not_supported_handler: Callable[[], None] = None):
        # TODO: BOLT
        if toy.implements(Sensor.enable_robot_infrared_message_notify):
            toy.enable_robot_infrared_message_notify(True)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_power_notifications(toy: Toy, enable: bool, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Power.enable_charger_state_changed_notify):
            toy.enable_charger_state_changed_notify(enable)
        elif toy.implements(Power.enable_battery_state_changed_notify):
            toy.enable_battery_state_changed_notify(enable)
        elif toy.implements(Power.enable_battery_voltage_state_change_notify):
            toy.enable_battery_voltage_state_change_notify(enable)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_color_detection(toy: Toy, enable: bool, not_supported_handler: Callable[[], None] = None):
        if toy.implements(Sensor.enable_color_detection):
            toy.enable_color_detection(enable)
        elif not_supported_handler:
            not_supported_handler()

    @staticmethod
    def set_robot_state_on_start(toy: Toy):
        # TODO setUserColour
        ToyUtil.set_head_position(toy, 0)
        ToyUtil.perform_leg_action(toy, R2LegActions.THREE_LEGS)
        ToyUtil.set_locator_flags(toy, False)
        ToyUtil.configure_collision_detection(toy)
        ToyUtil.set_power_notifications(toy, True)
        if toy.implements(Sensor.enable_gyro_max_notify):
            toy.enable_gyro_max_notify(True)
        if hasattr(toy, 'sensor_control'):
            toy.sensor_control.set_interval(150)
        ToyUtil.turn_off_leds(toy)
        if isinstance(toy, RVR):
            ToyUtil.set_color_detection(toy, True)
            ToyUtil.reset_heading(toy)
        ToyUtil.reset_locator(toy)
