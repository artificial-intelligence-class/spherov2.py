# python3
import time

from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

print("Testing Starting...")
print("Connecting to BB8...")
toy = scanner.find_BB8()
if toy is not None:
    print("Connected.")
    with SpheroEduAPI(toy) as droid:
        print("Testing Main LED")
        droid.set_main_led(Color(r=255, g=0, b=0))  # Sets Main LED
        time.sleep(1)

        print("Testing Aiming LED")
        droid.set_back_led(255)  # Sets Aiming light on
        time.sleep(1)

        print("Testing Roll")
        droid.roll(0, 100, 5)
        time.sleep(1)

        print("Testing End!")
