def to_int(ba):
    return int.from_bytes(ba, byteorder='big')


def to_bytes(i: int, size):
    return i.to_bytes(size, byteorder='big')
