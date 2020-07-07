from spherov2.commands import Commands
from spherov2.helper import to_bytes, to_int


class FactoryTest(Commands):
    _did = 31

    @staticmethod
    def get_factory_mode_challenge(toy, proc=None):
        return to_int(toy._execute(FactoryTest._encode(toy, 19, proc)).data)

    @staticmethod
    def enter_factory_mode(toy, challenge: int, proc=None):
        toy._execute(FactoryTest._encode(toy, 20, proc, to_bytes(challenge, 4)))

    @staticmethod
    def exit_factory_mode(toy, proc=None):
        toy._execute(FactoryTest._encode(toy, 21, proc))

    @staticmethod
    def get_chassis_id(toy, proc=None):
        return to_int(toy._execute(FactoryTest._encode(toy, 39, proc)).data)

    @staticmethod
    def enable_extended_life_test(toy, enable, proc=None):
        toy._execute(FactoryTest._encode(toy, 49, proc, [int(enable)]))

    @staticmethod
    def get_factory_mode_status(toy, proc=None):
        return bool(toy._execute(FactoryTest._encode(toy, 52, proc)).data[0])
