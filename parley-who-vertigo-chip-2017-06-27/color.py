import psmoveapi

class Color(psmoveapi.RGB):
    BLACK = psmoveapi.RGB(0.0, 0.0, 0.0)
    WHITE = psmoveapi.RGB(1.0, 1.0, 1.0)
    MAGENTA = psmoveapi.RGB(1.0, 0.0, 1.0)
    GREEN = psmoveapi.RGB(0.0, 1.0, 0.0)
    BLUE = psmoveapi.RGB(0.0, 0.0, 1.0)
    RED = psmoveapi.RGB(1.0, 0.0, 0.0)


def to_rgba32(color, opacity):
    r = int(255 * min(1, max(0, color.r)))
    g = int(255 * min(1, max(0, color.g)))
    b = int(255 * min(1, max(0, color.b)))
    a = int(255 * min(1, max(0, opacity)))
    return (r << 24) | (g << 16) | (b << 8) | a
