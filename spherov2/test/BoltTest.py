# python3
import time

from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

print("Testing Starting...")
print("Connecting to Bolt...")
toy = scanner.find_BOLT()
if toy is not None:
    print("Connected.")
    with SpheroEduAPI(toy) as droid:
        print("Testing Main LED")
        droid.set_main_led(Color(r=0, g=0, b=255))  # Sets whole Matrix
        time.sleep(1)
        print("Testing Front LED")
        droid.set_front_led(Color(r=0, g=255, b=0))  # Sets front LED
        time.sleep(1)
        print("Testing Back LED")
        droid.set_back_led(Color(r=255, g=0, b=0))  # Sets back LED
        time.sleep(1)
        print("Set Matrix Pixel")
        droid.set_matrix_pixel(0, 0, Color(r=255, g=255, b=0))  # Set Matrix Pixel
        time.sleep(1)
        print("Set Matrix Line")
        droid.set_matrix_line(1, 0, 1, 7, Color(r=255, g=0, b=255))  # Set Matrix Line
        time.sleep(1)
        print("Set Matrix Fill")
        droid.set_matrix_fill(2, 0, 6, 6, Color(r=0, g=255, b=255))  # Set Matrix Box
        time.sleep(2)
        print("Testing End!")

        # Smile (manual)
        # droid.set_main_led(Color(r=0, g=0, b=0)) #Sets whole Matrix
        # droid.set_matrix_line(2, 7, 5, 7, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_line(1, 6, 6, 6, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_line(0, 5, 1, 5, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_line(3, 5, 4, 5, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_line(6, 5, 7, 5, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_line(0, 4, 7, 4, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_line(0, 3, 7, 3, Color(r=255, g=0, b=255)) #Set Matrix Line
        # droid.set_matrix_pixel(0, 2, Color(r=255, g=0, b=255)) #Set Matrix Pixel
        # droid.set_matrix_pixel(7, 2, Color(r=255, g=0, b=255)) #Set Matrix Pixel
        # droid.set_matrix_pixel(1, 1, Color(r=255, g=0, b=255)) #Set Matrix Pixel
        # droid.set_matrix_pixel(6, 1, Color(r=255, g=0, b=255)) #Set Matrix Pixel
        # droid.set_matrix_line(2, 0, 5, 0, Color(r=255, g=0, b=255)) #Set Matrix Line
