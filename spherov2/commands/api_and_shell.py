from spherov2.commands import Commands
from spherov2.listeners.api_and_shell import ApiProtocolVersion


class ApiAndShell(Commands):
    _did = 16

    @staticmethod
    async def ping(toy, data, proc=None) -> bytearray:
        return await toy._execute(ApiAndShell._encode(toy, 0, proc, data)).data

    @staticmethod
    async def get_api_protocol_version(toy, proc=None) -> ApiProtocolVersion:
        data = await toy._execute(ApiAndShell._encode(toy, 1, proc)).data
        return ApiProtocolVersion(major_version=data[0], minor_version=data[1])

    @staticmethod
    async def send_command_to_shell(toy, command: bytes, proc=None):
        await toy._execute(ApiAndShell._encode(toy, 2, proc, [*command, 0]))

    send_string_to_console = (16, 3, lambda listener, p: listener(bytes(p.data).rstrip(b'\0')))

    @staticmethod
    async def get_supported_dids(toy, proc=None):
        return list(await toy._execute(ApiAndShell._encode(toy, 5, proc)).data)

    @staticmethod
    async def get_supported_cids(toy, s, proc=None):
        return list(await toy._execute(ApiAndShell._encode(toy, 6, proc, [s])).data)
