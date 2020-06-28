from typing import NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    revision: int


class LastErrorInfo(NamedTuple):
    file_name: bytes
    line_number: int
    data: bytes


class ConfigBlock(NamedTuple):
    metadata_version: int
    config_block_version: int
    application_data: bytes


class ManufacturingDate(NamedTuple):
    year: int
    month: int
    day: int


class EventLogStatus(NamedTuple):
    log_capacity: int
    bytes_used: int
    events_in_log: int
