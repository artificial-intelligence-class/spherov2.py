from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

if __name__ == '__main__':
    toy = scanner.find_R2Q5()
    with SpheroEduAPI(toy) as api:
        ...
