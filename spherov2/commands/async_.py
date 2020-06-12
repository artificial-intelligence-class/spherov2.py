class Async:
    battery_state_changed_notify = (0xff, 1, 0xff)
    sensor_streaming_data_notify = (0xff, 3, 0xff)
    will_sleep_notify = (0xff, 5, 0xff)
    collision_detected_notify = (0xff, 7, 0xff)
    gyro_max_notify = (0xff, 12, 0xff)
    did_sleep_notify = (0xff, 20, 0xff)
