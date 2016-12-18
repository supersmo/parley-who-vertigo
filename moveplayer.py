import color
import coroutine
import psmoveapi
import math


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
    def __init__(self, player_number):
        self.player_number = player_number
        self.led_color = color.Color.WHITE
        self.rumble = 0.0
        self.score = 0
        self.acceleration = psmoveapi.Vec3(0.0, 0.0, 0.0)
        self.trigger_pressed = False
        self.move_pressed = False

    def update(self):
        # TODO: Actually update those values from the controller
        self.acceleration = psmoveapi.Vec3(0.0, 0.0, 0.0)
        self.trigger_pressed = False
        self.move_pressed = False

    def valid(self):
        # TODO return move.ConnectionType == PSMoveConnectionType.Bluetooth
        return True

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
            parts.append(AnimationPart(color.Color.BLACK, tunables.BlinkDurationSec))

        return SphereColorAnimation(parts, on_finished)

    def game_win_animation(self, tunables, on_finished):
        parts = []
        parts.append(AnimationPart(color.Color.BLACK, tunables.GameWinAnimationWaitBeforeSec))

        current_color = color.Color.WHITE
        for i in range(tunables.GameWinAnimationFades):
            next_color = (psmovecolor.PSMoveColor.get_random_color()
                          if current_color == color.Color.WHITE else color.Color.WHITE)
            jmax = tunables.GameWinAnimationFadeSteps
            for j in range(jmax):
                alpha = float(j) / float(jmax - 1.0)
                mixed = current_color * (1.0 - alpha) + next_color * alpha
                parts.append(AnimationPart(mixed, tunables.FadeDurationSec))
            current_color = next_color

        parts.append(AnimationPart(color.Color.BLACK, tunables.GameWinAnimationWaitAfterSec))

        return self.sphere_color_animation(parts, on_finished)

    def now_shaking(self, tunables):
        return self.acceleration_magnitude >= tunables.ShakeThreshold

    def is_unstable(self, tunables):
        return self.acceleration_magnitude >= tunables.UnstableThreshold

    def safe_angle(self):
        v = Vec2(self.acceleration.x, self.acceleration.y)
        v.normalize()
        result = math.atan2(v.x, v.y) * 180.0 / math.pi
        if result < 0.0:
            result += 360.0
        return result

    def is_trigger_pressed(self):
        return self.trigger_pressed

    def is_move_pressed(self):
        return self.move_pressed
