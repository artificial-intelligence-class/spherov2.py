from spherov2.commands.sphero import Sphero as SpheroCmd
from spherov2.toy.sphero import Sphero
from spherov2.types import ToyType


class Ollie(Sphero):
    toy_type = ToyType('Ollie', '2B-', '2B', .06)

    get_sku = SpheroCmd.get_sku
