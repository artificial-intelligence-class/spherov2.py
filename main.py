import time

from spherov2 import scanner
from spherov2.toy.r2q5 import R2Q5
from spherov2.sphero_edu import SpheroEduAPI, Stance

if __name__ == '__main__':
    toy: R2Q5 = scanner.find_toys(toy_types=[R2Q5])[0]
    with SpheroEduAPI(toy) as api:
        api.set_stance(Stance.Tripod)
        time.sleep(2)
        api.set_speed(40)
        api.spin(840, 0)
        api.stop_roll()
        api.roll(0, -10, 10)
