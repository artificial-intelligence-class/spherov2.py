from spherov2.commands import Commands


class Connection(Commands):
    _did = 25

    @staticmethod
    def set_bluetooth_name(toy, name: bytes, proc=None):
        toy._execute(Connection._encode(toy, 3, proc, [*name, 0]))

    @staticmethod
    def get_bluetooth_name(toy, proc=None):
        return toy._execute(Connection._encode(toy, 4, proc)).data.rstrip(b'\0')

    @staticmethod
    def get_bluetooth_advertising_name(toy, proc=None):
        return toy._execute(Connection._encode(toy, 5, proc)).data.rstrip(b'\0')
