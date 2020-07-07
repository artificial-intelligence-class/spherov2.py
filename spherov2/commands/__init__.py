from spherov2.helper import nibble_to_byte


class Commands:
    @classmethod
    def _encode(cls, toy, cid, proc, data=None):
        if toy._require_target and not proc:
            raise ValueError(f'Robot type {cls} requires target processor')
        if proc:
            proc = nibble_to_byte(1, proc)
        return toy._packet_manager.new_packet(cls._did, cid, proc, data)
