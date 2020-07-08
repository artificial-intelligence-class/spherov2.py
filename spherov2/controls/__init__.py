from spherov2.commands.sphero import RawMotorModes

_ = RawMotorModes


class PacketDecodingException(Exception):
    ...


class CommandExecuteError(Exception):
    ...
