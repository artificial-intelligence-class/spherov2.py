from spherov2.commands import Commands
from spherov2.helper import to_bytes, to_int


class FactoryTest(Commands):
    _did = 31

    @staticmethod
    async def get_factory_mode_challenge(toy, proc=None):
        return to_int(await toy._execute(FactoryTest._encode(toy, 19, proc)).data)

    @staticmethod
    async def enter_factory_mode(toy, challenge: int, proc=None):
        await toy._execute(FactoryTest._encode(toy, 20, proc, to_bytes(challenge, 4)))

    @staticmethod
    async def exit_factory_mode(toy, proc=None):
        await toy._execute(FactoryTest._encode(toy, 21, proc))

    @staticmethod
    async def get_chassis_id(toy, proc=None):
        return to_int(await toy._execute(FactoryTest._encode(toy, 39, proc)).data)

    @staticmethod
    async def enable_extended_life_test(toy, enable, proc=None):
        await toy._execute(FactoryTest._encode(toy, 49, proc, [int(enable)]))

    @staticmethod
    async def get_factory_mode_status(toy, proc=None):
        return bool(await toy._execute(FactoryTest._encode(toy, 52, proc)).data[0])
