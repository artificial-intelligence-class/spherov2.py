from functools import partial

from spherov2.packet import Packet


class ApiAndShell:
    __encode = partial(Packet, device_id=16)

    @staticmethod
    def ping(data, target_id=None):
        return ApiAndShell.__encode(command_id=0, data=data, target_id=target_id)

    @staticmethod
    def get_api_protocol_version(target_id=None):
        return ApiAndShell.__encode(command_id=1, target_id=target_id)

    @staticmethod
    def send_command_to_shell(command, target_id=None):
        return ApiAndShell.__encode(command_id=2, data=[*command, 0], target_id=target_id)

    send_string_to_console = (16, 3, 0xff)
