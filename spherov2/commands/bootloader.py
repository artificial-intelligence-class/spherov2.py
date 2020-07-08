from spherov2.commands import Commands


class Bootloader(Commands):
    _did = 1

    @staticmethod
    def begin_reflash(toy, proc=None):
        toy._execute(Bootloader._encode(toy, 2, proc))

    @staticmethod
    def here_is_page(toy, proc=None):
        toy._execute(Bootloader._encode(toy, 3, proc))

    @staticmethod
    def jump_to_main(toy, proc=None):
        toy._execute(Bootloader._encode(toy, 4, proc))
