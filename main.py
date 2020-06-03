import time

from spherov2 import scanner
from spherov2.toy.r2q5 import R2Q5

if __name__ == '__main__':
    toys = scanner.find_toys()
    with toys[0] as toy:
        toy.wake()
        time.sleep(1)
        toy.play_animation(R2Q5.Animations.CHARGER_2, wait=True)
        toy.set_leg_position(0)
        time.sleep(5)
        # # print('slept')
        toy.sleep()
        print('finished')
    print('wow')
