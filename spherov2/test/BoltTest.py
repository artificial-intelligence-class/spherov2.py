# python3
#import sys
#sys.path.append('/spherov2/')

import time

from spherov2 import scanner
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color

print("Testing Starting...")
print("Connecting to Bolt...")
toy = scanner.find_BOLT()

if toy is not None:
    print("Connected.")
    with SpheroEduAPI(toy) as droid:
        print("Testing Start...")
        droid.set_main_led(Color(r=0, g=255, b=0)) #Sets whole Matrix
        
        droid.reset_aim()
        droid.set_main_led(Color(r=0,g=0,b=255))
        
        print("Luminosity: " + str(droid.get_luminosity()))
        print("Accel: " + str(droid.get_acceleration()))
        
        """
        print("Testing Main LED")
        droid.set_main_led(Color(r=0, g=0, b=255)) #Sets whole Matrix
        time.sleep(1)
        print("Testing Front LED")
        droid.set_front_led(Color(r=0, g=255, b=0)) #Sets front LED
        time.sleep(1)
        print("Testing Back LED")
        droid.set_back_led(Color(r=255, g=0, b=0)) #Sets back LED
        time.sleep(1)
        print("Set Matrix Pixel")
        droid.set_matrix_pixel(0, 0, Color(r=255, g=255, b=0)) #Set Matrix Pixel
        time.sleep(1)
        print("Set Matrix Line")
        droid.set_matrix_line(1, 0, 1, 7, Color(r=255, g=0, b=255)) #Set Matrix Line
        time.sleep(1)
        print("Set Matrix Fill")
        droid.set_matrix_fill(2, 0, 6, 6, Color(r=0, g=255, b=255)) #Set Matrix Box
        time.sleep(2)
        """

        droid.set_main_led(Color(r=255, g=0, b=0)) #Sets whole Matrix
        print("Testing End...")
  
  #droid.register_event(EventType.on_sensor_streaming_data, droid.SensorStreamingInfo) #how you would register to data (function name is custom)