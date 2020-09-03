==============
Sphero Edu API
==============
.. currentmodule:: spherov2.sphero_edu
.. autoclass:: SpheroEduAPI

Get Started
===========
Sphero robots aren't just toys – they are programmable robots that are great for learning about computer science! This wiki is a guide to learn how to program Sphero robots with Python. You will need a `Sphero robot <https://sphero.com/collections/all>`_, a Python 3 environment, and a hunger to learn.

Hello World!
------------
Using your device with the Sphero Edu API, create a new python code file, and copy and paste these code samples into the file. Don't forget to aim your robot, and then run the script to see what happens!

.. code-block:: python

    import time
    from spherov2 import scanner
    from spherov2.sphero_edu import SpheroEduAPI
    from spherov2.types import Color

    toy = scanner.find_toy()
    with SpheroEduAPI(toy) as droid:
        droid.set_main_led(Color(r=0, g=0, b=255))
        droid.set_speed(60)
        time.sleep(2)
        droid.set_speed(0)

Movement
========
Movements control the robot's motors and control system. You can use sequential movement commands by separating them with line breaks, like the `Hello World! <#hello-world>`_ program. Sphero robots move with three basic instructions: heading, speed, and duration. For example, if you set heading = 0°, speed = 60, duration = 3s, the robot would roll forward for 3s at a moderate speed.

.. class:: SpheroEduAPI

    .. automethod:: roll
    .. automethod:: set_speed
    .. automethod:: stop_roll
    .. automethod:: set_heading
    .. automethod:: spin
    .. automethod:: set_stabilization
    .. automethod:: raw_motor
    .. automethod:: reset_aim

Sphero BOLT Movements
---------------------
Sphero BOLT has a compass (magnetometer) sensor that has unique functionality. Nearby metallic and magnetic objects can affect the accuracy of the compass, so try to use this feature in an area without that interference, or hold it up in the air if you can't get away from interference.

Star Wars Droid Movements
-------------------------
.. class:: SpheroEduAPI

    .. automethod:: play_animation

R2-D2 & R2-Q5 Movements
-----------------------
The R2-D2 and R2-Q5 Droids are physically different from other Sphero robots, so there are some unique commands that only they can use.

.. class:: SpheroEduAPI

    .. automethod:: set_dome_position
    .. automethod:: set_stance
    .. automethod:: set_waddle

Lights
======
Lights control the color and brightness of LEDs on a robot.

.. class:: SpheroEduAPI

    .. automethod:: set_main_led
    .. method:: set_back_led(color: int)

        Sets the brightness of the back aiming LED, aka the "Tail Light." This LED is limited to blue only, with a brightness scale from 0 to 255. For example, use ``set_back_led(255)`` to set the back LED to full brightness. Use :func:`time.sleep` to set it on for a duration. For example, to create a dim and a bright blink sequence use::

            set_back_led(0)  # Dim
            delay(0.33)
            set_back_led(255)  # Bright
            delay(0.33)

    .. automethod:: fade
    .. automethod:: strobe

Sphero BOLT Lights
------------------
Sphero BOLT has unique lighting capabilities with a front led, back led, and 8x8 led matrix. The matrix has 3 methods to program in increasing abstraction and sophistication that are very fun to play with! The 3 methods are setting pixels, text, and animations.

.. class:: SpheroEduAPI

    .. method:: set_front_led(color: spherov2.types.Color)

        Changes the color of the front LED light. Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the magenta color is expressed as ``set_front_color(Color(239, 0, 255))``

    .. method:: set_back_led(color: spherov2.types.Color)

        Changes the color of the back LED light, aka the "Tail Light" or "Aim Light." Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the green color is expressed as ``set_back_led(Color(0, 255, 0))``. Sphero BOLT has this as an RGB LED on the back, whereas previous Spheros are limited to `blue only <#spherov2.sphero_edu.SpheroEduAPI.set_back_led>`_.

Sphero RVR Lights
-----------------
.. class:: SpheroEduAPI

    .. automethod:: set_left_headlight_led
    .. automethod:: set_right_headlight_led
    .. automethod:: set_left_led
    .. automethod:: set_right_led

    .. method:: set_front_led(color: spherov2.types.Color)

        Changes the color of RVR's front two LED headlights together. Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the magenta color is expressed as ``set_front_color(Color(239, 0, 255))``.

    .. method:: set_back_led(color: spherov2.types.Color)

        Changes the color of the back LED light, aka the "Tail Light" or "Aim Light." Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the above green color is expressed as ``set_back_led(Color(0, 255, 0))``.

BB-9E Lights
------------
.. class:: SpheroEduAPI

    .. automethod:: set_dome_leds

R2-D2 & R2-Q5 Lights
--------------------
.. class:: SpheroEduAPI

    .. method:: set_front_led(color: spherov2.types.Color)

        Changes the color of the front LED light. Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the fuchsia color is expressed as ``set_front_color(Color(232, 0, 255))``

    .. method:: set_back_led(color: spherov2.types.Color)

        Changes the color of the back LED light. Set this using RGB (red, green, blue) values on a scale of 0 - 255. For example, the above green color is expressed as ``set_back_led(Color(0, 255, 0))``.

    .. automethod:: set_holo_projector_led
    .. automethod:: set_logic_display_leds

Sounds
======
Control sounds and words which can play from your programming device's speaker or the robot (R2-D2 & R2-Q5 only).

.. class:: SpheroEduAPI

    .. automethod:: play_sound

Sensors
=======
Querying sensor data allows you to react to real-time values coming from the robots' physical sensors. For example, "if accelerometer z-axis > 3G's, then set LED's to green."

.. class:: SpheroEduAPI

    .. automethod:: get_acceleration
    .. automethod:: get_vertical_acceleration
    .. automethod:: get_orientation
    .. automethod:: get_gyroscope
    .. automethod:: get_velocity
    .. automethod:: get_location
    .. automethod:: get_distance
    .. automethod:: get_speed
    .. automethod:: get_heading
    .. automethod:: get_main_led
    .. method:: get_back_led

        ``get_back_led().b`` is the brightness of the back LED, from 0 to 255. For Sphero BOLT, use ``get_back_led()`` to get the RGB value.

Sphero BOLT Sensors
-------------------
.. class:: SpheroEduAPI

    .. automethod:: get_last_ir_message

    .. method:: get_back_led

        Provides the RGB color of the back LED, from 0 to 255 for each color channel.

    .. method:: get_front_led

        Provides the RGB color of the front LED, from 0 to 255 for each color channel.

Sphero RVR Sensors
------------------
.. class:: SpheroEduAPI

    .. automethod:: get_color

R2-D2 & R2-Q5 Sensors
---------------------
.. class:: SpheroEduAPI

    .. method:: get_back_led

        Provides the RGB color of the back LED, from 0 to 255 for each color channel.

    .. method:: get_front_led

        Provides the RGB color of the front LED, from 0 to 255 for each color channel.

    .. automethod:: get_dome_leds
    .. automethod:: get_holo_projector_led
    .. automethod:: get_logic_display_leds

Communications
==============
Infrared (IR) is invisible light with longer wavelengths than visible light, and it is commonly used in TV remote controls to transmit small amounts of data. IR is used in Sphero BOLT to transmit data such as relative distance and heading between robots to enable following and evading behavior among multiple robots, as well as to send custom messages. There are four IR emitters and receivers (pairs) for 360° awareness assuming there is a clear line of sight between two or more robots. The effective range is up to about 3 meters.

.. class:: SpheroEduAPI

    .. automethod:: start_ir_broadcast
    .. automethod:: stop_ir_broadcast
    .. automethod:: start_ir_follow
    .. automethod:: stop_ir_follow
    .. automethod:: start_ir_evade
    .. automethod:: stop_ir_evade
    .. automethod:: send_ir_message
    .. method:: listen_for_ir_message

        Refer to `IR Message Received Event <#on-ir-message-received>`_ for usage.

    .. method:: listen_for_color_sensor

        Refer to `Color Event <#on-color>`_ for usage.

Events
======
Events are predefined robot functions into which you can embed conditional logic. When an event occurs, the conditional logic is called in a newly spawned thread. The event will be called every time it occurs by default, unless you customize it. For example, "on collision, change LED lights to red and play the Collision sound," while the main loop is still running.

.. class:: SpheroEduAPI

    .. automethod:: register_event

On Collision
------------
Executes conditional logic when the robot collides with an object.

.. code-block:: python

    def on_collision(api):
        # code to execute on collision

    api.register_event(EventType.on_collision, on_collision)

For example, below is a basic `pong <https://en.wikipedia.org/wiki/Pong>`_ program where Sphero bounces off walls, or your hands/feet in perpetuity. Place the robot on the floor between two parallel walls/objects and run the program with the robot pointed perpendicularly at one wall. On collision, the program will print "collision" and change the LED's to red, then continue in the opposite direction:

.. code-block:: python

    def on_collision(api):
        api.stop_roll()
        api.set_main_led(Color(255, 0, 0))
        print('Collision')
        api.set_heading(api.get_heading() + 180)
        time.sleep(0.5)
        api.set_main_led(Color(255, 22, 255))
        api.set_speed(100)

    api.register_event(EventType.on_collision, on_collision)
    api.set_main_led(Color(255, 255, 255))
    api.set_speed(100)

On Freefall
-----------
Executes conditional logic when gravity is the only force acting on the robot, such as when dropping or throwing it. Freefall is measured by an accelerometer reading of < 0.1g for => 0.1s, where 1g is resting. On earth, objects in freefall accelerate downwards at 9.81 m/s^2. If you are in orbit, objects appear to be at rest with a reading of 0g because they (and you) are always in freefall, but they never hit the Earth.

.. code-block:: python

    def on_freefall(api):
        # code to execute on freefall

    api.register_event(EventType.on_freefall, on_freefall)

For example, to print "freefall" and change the LED's to red on freefall use:

.. code-block:: python

    def on_freefall(api):
        api.set_main_led(Color(255, 0, 0))
        print('freefall')

    api.register_event(EventType.on_freefall, on_freefall)
    api.set_main_led(Color(255, 255, 255))

On Landing
----------
Executes conditional logic when the robot lands after an being in freefall. You don't need to define an ``on_freefall`` event for the robot to experience an ``on_landing``, but the robot must meet the conditions for freefall before land.

.. code-block:: python

    def on_landing(api):
        # code to execute on landing

    api.register_event(EventType.on_landing, on_landing)

For example, to print "landing" and change the LED's to green after landing use:

.. code-block:: python

    def on_landing(api):
        api.set_main_led(Color(0, 255, 0))
        print('land')

    api.register_event(EventType.on_landing, on_landing)
    api.set_main_led(Color(255, 255, 255))

On Gyro Max
-----------
Executes conditional logic when the robot exceeds the bounds of measurable rotational velocity of -2,000° - 2,000° per second. This can be triggered by spinning the robot around like a top on a table really fast. You need to spin it around > 5.5 revolutions per second.

.. code-block:: python

    def on_gyro_max(api):
        # code to execute on gyromax

    api.register_event(EventType.on_gyro_max, on_gyro_max)

For example, to print "gyromax" and change the LED's to red when you reach gyromax, use:

.. code-block:: python

    def on_gyro_max(api):
        api.set_main_led(Color(255, 0, 0))
        print('gyromax')

    api.register_event(EventType.on_gyro_max, on_gyro_max)
    api.set_stabilization(False)
    api.set_back_led(255)
    api.set_main_led(Color(255, 255, 255))

On Charging
-----------
Executes conditional logic called when the robot starts charging its battery. This can be triggered by placing your robot in it's charging cradle, or by plugging it in.

.. code-block:: python

    def on_charging(api):
        # code to execute on charging

    api.register_event(EventType.on_charging, on_charging)

On Not Charging
---------------
Executes conditional logic called when the robot stops charging its battery. This can be triggered by removing your robot from it's charging cradle, or unplugging it.

.. code-block:: python

    def on_not_charging(api):
        # code to execute on not charging

    api.register_event(EventType.on_not_charging, on_not_charging)

For example, to have Sphero execute 2 different conditions for on charging, and on not charging, use the below.

.. code-block:: python

    def on_charging(api):
        api.set_main_led(Color(6, 0, 255))
        print('charging')
        time.sleep(1)
        print('remove me from my charger')

    api.register_event(EventType.on_charging, on_charging)

    def on_not_charging(api):
        api.set_main_led(Color(255, 0, 47))
        print('not charging')

    api.register_event(EventType.on_not_charging, on_not_charging)

    print('place me in my charger')
    while True:
        api.set_main_led(Color(3, 255, 0))
        time.sleep(0.5)

On IR Message Received
----------------------
Executes conditional logic called when an infrared message is received on the specified channel. This can be triggered by one Sphero BOLT robot receiving a message from another Sphero BOLT. For example, to have Sphero BOLT change the matrix to red when receiving a message on channel 4:

.. code-block:: python

    message_channels = (4, )

    def on_ir_message_4(api, channel):
        if channel != 4:
            return
        api.set_main_led(Color(255, 0, 0))
        api.listen_for_ir_message(message_channels)

    api.register_event(EventType.on_ir_message, on_ir_message_4)
    api.listen_for_ir_message(message_channels)

On Color
--------
Executes conditional logic called when Sphero RVR's color sensor returns a specified RGB color value.

.. code-block:: python

    color = (Color(255, 15, 60), )

    def on_color(api, color):
        if color != Color(255, 15, 60):
            return

    api.register_event(EventType.on_color, on_color)
    api.listen_for_color_sensor(colors)

The color that RVR's color sensor returns needs to be very close to the color set with :func:`listen_for_color_sensor` for the event to execute correctly.
