import random
import psmoveapi

from color import Color

class PSMoveColor(object):
    BUTTON_TO_COLOR = {
        psmoveapi.Button.SQUARE: Color.MAGENTA,
        psmoveapi.Button.TRIANGLE: Color.GREEN,
        psmoveapi.Button.CROSS: Color.BLUE,
        psmoveapi.Button.CIRCLE: Color.RED,
    }

    COLORS = list(BUTTON_TO_COLOR.values())

    @classmethod
    def get_random_color(cls):
        return random.choice(cls.COLORS)

    @classmethod
    def is_color_button(cls, button):
        return button in cls.BUTTON_TO_COLOR.keys()

    @classmethod
    def color_for_button(cls, button):
        return cls.BUTTON_TO_COLOR[button]
