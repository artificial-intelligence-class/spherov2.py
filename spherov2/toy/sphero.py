from spherov2.toy.core import Toy
from spherov2.types import ToyType


class Sphero(Toy):
    toy_type = ToyType('SPRK/2.0', None, 'Sphero', .06)
