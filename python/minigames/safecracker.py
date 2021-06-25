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


import minigame
import random
import moveplayer
import coroutine

from color import Color


class SolveState(object):
    Searching, Found, Activated, Afterglow = range(4)


class SafeCracker(minigame.MiniGame):
    ENABLED = True

    SAFE_COLOR = Color(0.91, 0.78, 0.0)

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.angles = []
        self.target_angles = []
        self.last_click_angles = []
        self.solved_locks = []
        self.solve_state = []
        self.angle_steps = 12
        self.number_of_locks = 2
        self.players_ready = 0

    def status_message(self):
        return 'You crack me up lil\' buddy'

    def base_color(self):
        return self.SAFE_COLOR

    def start_game(self):
        def on_intro_blinking_finished():
            self.players_ready += 1

            if self.players_ready == len(self.gameflow.players):
                self.angles = [0 for player in self.gameflow.players]

                self.target_angles = [random.randint(0, self.angle_steps-1) * 360 / self.angle_steps
                                      for player in self.gameflow.players]

                self.last_click_angles = [0 for player in self.gameflow.players]
                self.solved_locks = [0 for player in self.gameflow.players]
                self.solve_state = [SolveState.Searching for player in self.gameflow.players]

        self.gameflow.play_sound('SafeAnnounceSound')

        for player in self.gameflow.players:
            parts = []
            parts.append(moveplayer.AnimationPart(self.SAFE_COLOR * 0.2, 0.4, 0.6))
            parts.append(moveplayer.AnimationPart(self.SAFE_COLOR, 0.5, 0.7))
            parts.append(moveplayer.AnimationPart(Color.BLACK, 0.4))

            self.gameflow.start_coroutine(player.sphere_color_animation(parts, on_intro_blinking_finished))

    def reset_search(self, player, delay):
        yield coroutine.WaitForSeconds(delay)

        self.solved_locks[player.player_number] += 1
        if self.solved_locks[player.player_number] == self.number_of_locks:
            self.gameflow.end_current_game(player)
        else:
            self.target_angles[player.player_number] = random.randint(0, self.angle_steps-1) * 360 / self.angle_steps
            self.solve_state[player.player_number] = SolveState.Searching

    def update(self):
        tunables = self.gameflow.get_tunables()

        if self.players_ready < len(self.gameflow.players):
            return

        threshold = int(360 / self.angle_steps)

        for player in self.gameflow.players:
            new_angle = int(player.safe_angle())
            if abs(new_angle - self.last_click_angles[player.player_number]) > 20.0:
                self.gameflow.play_sound('SafeClickSound', 0.3)
                self.last_click_angles[player.player_number] = new_angle
            self.angles[player.player_number] = new_angle

            is_near = (self.angles[player.player_number] >= self.target_angles[player.player_number] and
                       self.angles[player.player_number] <= self.target_angles[player.player_number] + threshold)

            # State transitions
            if self.solve_state[player.player_number] == SolveState.Searching:
                if is_near and not player.is_trigger_pressed():
                    self.solve_state[player.player_number] = SolveState.Found
            elif self.solve_state[player.player_number] == SolveState.Found:
                if not is_near:
                    self.solve_state[player.player_number] = SolveState.Searching
                elif player.is_trigger_pressed():
                    self.solve_state[player.player_number] = SolveState.Activated
            elif self.solve_state[player.player_number] == SolveState.Activated:
                self.gameflow.start_coroutine(self.reset_search(player, 0.2))
                self.solve_state[player.player_number] = SolveState.Afterglow
            elif self.solve_state[player.player_number] == SolveState.Afterglow:
                ...

            # State actions
            if self.solve_state[player.player_number] == SolveState.Searching:
                player.led_color = self.SAFE_COLOR * tunables.ColorIntensityDuringGameplay
                player.rumble = 0.0
            elif self.solve_state[player.player_number] == SolveState.Found:
                player.led_color = self.SAFE_COLOR * tunables.ColorIntensityDuringGameplay
                player.rumble = 0.5
            elif self.solve_state[player.player_number] == SolveState.Activated:
                player.led_color = self.SAFE_COLOR
                player.rumble = 0.5
            elif self.solve_state[player.player_number] == SolveState.Afterglow:
                player.led_color = self.SAFE_COLOR
                player.rumble = 1.0
