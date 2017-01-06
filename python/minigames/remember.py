import minigame
import moveplayer
import psmovecolor

from color import Color

import time
import math

class Remember(minigame.MiniGame):
    ENABLED = False

    REPLAY_DELAY_SECONDS = 2.0

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.started = time.time()

    def delta_time(self):
        return time.time() - self.started

    def start_game(self):
        for player in self.gameflow.players:
            player.last_button_press_time = self.delta_time()
            player.is_recording = False
            player.recording_start_time = self.delta_time()
            player.playback_start_time = self.delta_time()
            player.recorded_sequence = []

    def status_message(self):
        return 'We do what you do and you press it'

    def base_color(self):
        return Color.WHITE

    def button_pressed(self, player, button):
        if not psmovecolor.PSMoveColor.is_color_button(button):
            return

        self.gameflow.play_sound('CycleBlipSound')
        color = psmovecolor.PSMoveColor.color_for_button(button)
        player.led_color = color

        player.last_button_press_time = self.delta_time()

        if not player.is_recording:
            player.is_recording = True
            player.recording_start_time = self.delta_time()
            player.recorded_sequence = [(0, color)]
        else:
            player.recorded_sequence.append((self.delta_time() - player.recording_start_time, color))

    def get_recorded_sequence_duration(self, player):
        if len(player.recorded_sequence) > 1:
            last_time, color = player.recorded_sequence[-1]
            return last_time

        # if no recording exists, loop for 1 second
        return 1.0

    def get_recorded_color(self, player, position):
        for recorded_position, recorded_color in reversed(player.recorded_sequence):
            if position >= recorded_position:
                return recorded_color

        return Color.BLACK

    def update(self):
        tunables = self.gameflow.get_tunables()

        for player in self.gameflow.players:
            if player.is_recording and player.last_button_press_time < self.delta_time() - self.REPLAY_DELAY_SECONDS:
                player.recorded_sequence.append((self.delta_time() - player.recording_start_time, Color.BLACK))
                player.is_recording = False
                player.led_color = Color.BLACK
                player.playback_start_time = self.delta_time()

            if not player.is_recording:
                current_position = self.delta_time() - player.playback_start_time
                duration = self.get_recorded_sequence_duration(player)
                current_position = math.fmod(current_position, duration)
                player.led_color = self.get_recorded_color(player, current_position)

