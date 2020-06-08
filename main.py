import time

from spherov2 import scanner
from spherov2.command.io import AudioPlaybackModes
from spherov2.toy.r2q5 import R2Q5
from spherov2.sphero_edu import SpheroEduAPI, Color

if __name__ == '__main__':
    toy: R2Q5 = scanner.find_toys()[0]
    with SpheroEduAPI(toy) as api:
        while True:
            print(api.get_acceleration())
            time.sleep(0.5)
        time.sleep(1000)
