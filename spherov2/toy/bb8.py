from spherov2.commands.core import Core
from spherov2.toy.ollie import Ollie
from spherov2.types import ToyType


class BB8(Ollie):
    toy_type = ToyType('BB-8', 'BB-', 'BB', .06)

    # Core
    get_factory_config_block_crc = Core.get_factory_config_block_crc
