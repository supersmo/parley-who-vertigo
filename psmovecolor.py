import random
import psmoveapi
import color

class PSMoveColor(object):
    BUTTON_TO_COLOR = {
        psmoveapi.Button.SQUARE: color.Color.MAGENTA,
        psmoveapi.Button.TRIANGLE: color.Color.GREEN,
        psmoveapi.Button.CROSS: color.Color.BLUE,
        psmoveapi.Button.CIRCLE: color.Color.RED,
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
