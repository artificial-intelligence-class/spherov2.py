from spherov2.commands import Commands


class Bootloader(Commands):
    _did = 1

    @staticmethod
    async def begin_reflash(toy, proc=None):
        await toy._execute(Bootloader._encode(toy, 2, proc))

    @staticmethod
    async def here_is_page(toy, proc=None):
        await toy._execute(Bootloader._encode(toy, 3, proc))

    @staticmethod
    async def jump_to_main(toy, proc=None):
        await toy._execute(Bootloader._encode(toy, 4, proc))
