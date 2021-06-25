#
# Parley Who Vertigo
# Copyright 2016, 2017 Thomas Perl, Josef Who
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#


import coroutine
import psmoveapi
import math
import psmovecolor

from color import Color


class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        length = math.sqrt(self.x * self.x + self.y * self.y)
        self.x /= length
        self.y /= length


class AnimationPart(object):
    def __init__(self, color, duration, rumble=0.0):
        self.color = color
        self.duration = duration
        self.rumble = rumble


class MovePlayer(object):
    def __init__(self, player_number, controller):
        self.player_number = player_number
        self.controller = controller
        self.led_color = Color.BLACK
        self.rumble = 0.0
        self.score = 0
        self.last_buttons = 0

    @property
    def acceleration(self):
        return self.controller.accelerometer

    def update(self):
        self.controller.color = self.led_color
        self.controller.rumble = self.rumble
        self.last_buttons = self.controller.buttons

    def sphere_color_animation(self, parts, on_finished, on_changed=None):
        for part in parts:
            self.led_color = part.color
            self.rumble = part.rumble
            if on_changed is not None:
                on_changed()
            yield coroutine.WaitForSeconds(part.duration)

        on_finished()

    def win_animation(self, tunables, on_finished):
        parts = []
        for i in range(tunables.WinAnimationBlinks):
            parts.append(AnimationPart(tunables.WinAnimationColor, tunables.BlinkDurationSec))
            parts.append(AnimationPart(Color.BLACK, tunables.BlinkDurationSec))

        return self.sphere_color_animation(parts, on_finished)

    def game_win_animation(self, tunables, on_finished):
        parts = []
        parts.append(AnimationPart(Color.BLACK, tunables.GameWinAnimationWaitBeforeSec))

        current_color = Color.WHITE
        for i in range(tunables.GameWinAnimationFades):
            next_color = (psmovecolor.PSMoveColor.get_random_color()
                          if current_color == Color.WHITE else Color.WHITE)
            jmax = tunables.GameWinAnimationFadeSteps
            for j in range(jmax):
                alpha = float(j) / float(jmax - 1.0)
                mixed = current_color * (1.0 - alpha) + next_color * alpha
                parts.append(AnimationPart(mixed, tunables.FadeDurationSec))
            current_color = next_color

        parts.append(AnimationPart(Color.BLACK, tunables.GameWinAnimationWaitAfterSec))

        return self.sphere_color_animation(parts, on_finished)

    def now_shaking(self, tunables):
        return self.controller.accelerometer.length() >= tunables.ShakeThreshold

    def is_unstable(self, tunables):
        return self.controller.accelerometer.length() >= tunables.UnstableThreshold

    def get_accelerometer_x(self):
        return self.controller.accelerometer.x

    def safe_angle(self):
        v = Vec2(self.acceleration.x, self.acceleration.y)
        v.normalize()
        result = math.atan2(v.x, v.y) * 180.0 / math.pi
        if result < 0.0:
            result += 360.0
        return result

    def is_trigger_pressed(self):
        return self.controller.still_pressed(psmoveapi.Button.T)

    def is_move_pressed(self):
        return self.controller.still_pressed(psmoveapi.Button.MOVE)

    def is_button_down(self, button):
        return self.controller.still_pressed(button)

    def is_button_pressed_now_and_not_before(self, button):
        return ((self.controller.buttons & button) != 0)  and ((self.last_buttons & button) == 0)
