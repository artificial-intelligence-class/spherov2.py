from spherov2.commands import Commands


class SystemMode(Commands):
    _did = 18

    @staticmethod
    def enable_desktoy_mode(toy, enable: bool, proc=None):
        toy._execute(SystemMode.__encode(toy, 41, proc, [int(enable)]))

    @staticmethod
    def get_out_of_box_state(toy, proc=None):
        return bool(toy._execute(SystemMode._encode(toy, 43, proc)).data[0])

    @staticmethod
    def enable_out_of_box_state(toy, enable: bool, proc=None):
        toy._execute(SystemMode.__encode(toy, 44, proc, [int(enable)]))
