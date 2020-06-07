import time

from spherov2 import scanner
from spherov2.toy.r2q5 import R2Q5
from spherov2.sphero_edu import SpheroEduAPI, Color

if __name__ == '__main__':
    toy: R2Q5 = scanner.find_toys()[0]
    with SpheroEduAPI(toy) as api:
        api.strobe(Color(255, 57, 66), (3 / 15) * 0.5, 20)
        time.sleep(5)
