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

        droid.set_main_led(Color(r=255, g=0, b=0)) #Sets whole Matrix
        print("Testing End...")
  
  #droid.register_event(EventType.on_sensor_streaming_data, droid.SensorStreamingInfo) #how you would register to data (function name is custom)