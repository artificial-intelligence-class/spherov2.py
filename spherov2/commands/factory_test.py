from functools import partial

from spherov2.helper import to_bytes
from spherov2.packet import Packet


class FactoryTest:
    __encode = partial(Packet, device_id=31)

    @staticmethod
    def get_factory_mode_challenge(target_id=None):
        return FactoryTest.__encode(command_id=19, target_id=target_id)

    @staticmethod
    def enter_factory_mode(challenge: int, target_id=None):
        return FactoryTest.__encode(command_id=20, data=to_bytes(challenge, 4), target_id=target_id)

    @staticmethod
    def exit_factory_mode(target_id=None):
        return FactoryTest.__encode(command_id=21, target_id=target_id)
