from functools import partial

from spherov2.packet import Packet


class SystemMode:
    __encode = partial(Packet, device_id=18)

    @staticmethod
    def get_out_of_box_state(target_id=None):
        return SystemMode.__encode(command_id=43, target_id=target_id)

    @staticmethod
    def enable_out_of_box_state(enable: bool, target_id=None):
        return SystemMode.__encode(command_id=44, data=[int(enable)], target_id=target_id)
