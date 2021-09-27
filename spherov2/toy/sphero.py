from collections import OrderedDict
from functools import partialmethod, lru_cache

from spherov2.commands.bootloader import Bootloader
from spherov2.commands.core import Core
from spherov2.commands.power import Power
from spherov2.commands.sensor import Sensor
from spherov2.commands.sphero import Sphero as SpheroCmd
from spherov2.controls.v1 import DriveControl, SensorControl
from spherov2.toy import ToySensor, Toy
from spherov2.types import ToyType


class Sphero(Toy):
    toy_type = ToyType('SPRK/2.0', None, 'Sphero', .06)

    sensors = OrderedDict(
        attitude=OrderedDict(
            pitch=ToySensor(0x40000, -179., 180.),
            roll=ToySensor(0x20000, -179., 180.),
            yaw=ToySensor(0x10000, -179., 180.)
        ),
        accelerometer=OrderedDict(
            x=ToySensor(0x8000, -32768., 32767., lambda x: x / 4096),
            y=ToySensor(0x4000, -32768., 32767., lambda x: x / 4096),
            z=ToySensor(0x2000, -32768., 32767., lambda x: x / 4096)
        ),
        gyroscope=OrderedDict(
            x=ToySensor(0x1000, -20000., 20000., lambda x: x * .1),
            y=ToySensor(0x800, -20000., 20000., lambda x: x * .1),
            z=ToySensor(0x400, -20000., 20000., lambda x: x * .1)
        ),
        back_emf=OrderedDict(
            left=ToySensor(0x40, -32768., 32767.),
            right=ToySensor(0x20, -32768., 32767.),
        )
    )

    extended_sensors = OrderedDict(
        quaternion=OrderedDict(
            x=ToySensor(0x80000000, -10000., 10000., lambda x: x / 10000),
            y=ToySensor(0x40000000, -10000., 10000., lambda x: x / 10000),
            z=ToySensor(0x20000000, -10000., 10000., lambda x: x / 10000),
            w=ToySensor(0x10000000, -10000., 10000., lambda x: x / 10000)
        ),
        locator=OrderedDict(
            x=ToySensor(0x8000000, -32768., 32767.),
            y=ToySensor(0x4000000, -32768., 32767.),
        ),
        accel_one=OrderedDict(accel_one=ToySensor(0x2000000, 0., 8000.)),
        velocity=OrderedDict(
            x=ToySensor(0x1000000, -32768., 32767., lambda x: x * .1),
            y=ToySensor(0x800000, -32768., 32767., lambda x: x * .1),
        ),
        speed=OrderedDict(speed=ToySensor(0x400000, 0., 32767.)),
    )

    def wake(self):
        self._Toy__adapter.write('22bb746f-2bbf-7554-2d6f-726568705327', bytearray([1]))

    # Async
    add_battery_state_changed_notify_listener = partialmethod(Toy._add_listener,
                                                              Power.battery_state_changed_notify)  # BatteryStateChangedNotifyCommand
    remove_battery_state_changed_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Power.battery_state_changed_notify)  # BatteryStateChangedNotifyCommand
    add_collision_detected_notify_listener = partialmethod(Toy._add_listener,
                                                           Sensor.collision_detected_notify)  # CollisionDetectedNotifyCommand
    remove_collision_detected_notify_listener = partialmethod(Toy._remove_listener,
                                                              Sensor.collision_detected_notify)  # CollisionDetectedNotifyCommand
    add_did_sleep_notify_listener = partialmethod(Toy._add_listener, Power.did_sleep_notify)  # DidSleepNotifyCommand
    remove_did_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                     Power.did_sleep_notify)  # DidSleepNotifyCommand
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_max_notify)  # GyroMaxNotifyCommand
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener,
                                                    Sensor.gyro_max_notify)  # GyroMaxNotifyCommand
    add_sensor_streaming_data_notify_listener = partialmethod(Toy._add_listener,
                                                              Sensor.sensor_streaming_data_notify)  # SensorStreamingDataNotifyCommand
    remove_sensor_streaming_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Sensor.sensor_streaming_data_notify)  # SensorStreamingDataNotifyCommand
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener, Power.will_sleep_notify)  # WillSleepNotifyCommand
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                      Power.will_sleep_notify)  # WillSleepNotifyCommand

    # Bootloader
    begin_reflash = Bootloader.begin_reflash  # BeginReflashCommand
    here_is_page = Bootloader.here_is_page  # HereIsPageCommand
    jump_to_main = Bootloader.jump_to_main  # JumpToMainCommand

    # Core
    enable_battery_state_changed_notify = Core.enable_battery_state_changed_notify  # EnableBatteryStateChangedNotifyCommand
    get_bluetooth_info = Core.get_bluetooth_info  # GetBluetoothInfoCommand
    get_charger_state = Core.get_charger_state  # GetChargerStateCommand
    get_power_state = Core.get_power_state  # GetPowerStateCommand
    get_versions = Core.get_versions  # GetVersionsCommand
    jump_to_bootloader = Core.jump_to_bootloader  # JumpToBootloaderCommand
    ping = Core.ping  # PingCommand
    set_bluetooth_name = Core.set_bluetooth_name  # SetBluetoothNameCommand
    set_inactivity_timeout = Core.set_inactivity_timeout  # SetInactivityTimeoutCommand
    sleep = Core.sleep  # SleepCommand

    # Sphero
    boost = SpheroCmd.boost  # BoostCommand
    configure_collision_detection = SpheroCmd.configure_collision_detection  # ConfigureCollisionDetectionCommand
    configure_locator = SpheroCmd.configure_locator  # ConfigureLocatorCommand
    get_chassis_id = SpheroCmd.get_chassis_id  # GetChassisId
    get_persistent_options = SpheroCmd.get_persistent_options  # GetPersistentOptionsCommand
    get_temperature = SpheroCmd.get_temperature  # GetTemperatureCommand
    set_temporary_options = SpheroCmd.set_temporary_options  # GetTemporaryOptionsCommand
    roll = SpheroCmd.roll  # RollCommand
    self_level = SpheroCmd.self_level  # SelfLevelCommand
    set_back_led_brightness = SpheroCmd.set_back_led_brightness  # SetBackLedBrightnessCommand
    set_data_streaming = SpheroCmd.set_data_streaming  # SetDataSteamingCommand
    set_heading = SpheroCmd.set_heading  # SetHeadingCommand
    set_main_led = SpheroCmd.set_main_led  # SetMainLedCommand
    set_motion_timeout = SpheroCmd.set_motion_timeout  # SetMotionTimeoutCommand
    set_persistent_options = SpheroCmd.set_persistent_options  # SetPersistentOptionsCommand
    set_raw_motors = SpheroCmd.set_raw_motors  # SetRawMotorsCommand
    set_rotation_rate = SpheroCmd.set_rotation_rate  # SetRotationRateCommand
    set_stabilization = SpheroCmd.set_stabilization  # SetStabilizationCommand
    set_temporary_options = SpheroCmd.set_temporary_options  # SetTemporaryOptionsCommand

    # Controls - V1
    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    # The way utils.py is implemented this doesnt need to be present
    # @property
    # @lru_cache(None)
    # def multi_led_control(self):
    #    return LedControl(self)

    @property
    @lru_cache(None)
    def sensor_control(self):
        return SensorControl(self)

    @property
    @lru_cache(None)
    def stats_control(self):
        return StatsControl(self)
