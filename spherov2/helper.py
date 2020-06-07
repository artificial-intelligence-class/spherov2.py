from spherov2.types import Color


def to_int(ba):
    return int.from_bytes(ba, byteorder='big')


def to_bytes(i: int, size):
    return i.to_bytes(size, byteorder='big')


def bound_value(lower, value, upper):
    return min(upper, max(lower, value))


def bound_color(color: Color, default_color: Color):
    return Color(
        r=default_color.r if color.r is None else bound_value(0, color.r, 255),
        g=default_color.g if color.g is None else bound_value(0, color.g, 255),
        b=default_color.b if color.b is None else bound_value(0, color.b, 255)
    )
