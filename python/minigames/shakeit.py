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
import moveplayer

from color import Color

class ShakeIt(minigame.MiniGame):
    ENABLED = True

    PUMPING_COLOR = Color.GREEN

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.counters = []
        self.players_ready = 0

    def start_game(self):
        def on_intro_blinking_finished():
            self.players_ready += 1

            if self.players_ready == len(self.gameflow.players):
                self.counters = [0 for player in self.gameflow.players]

        self.gameflow.play_sound('BalloonAnnounceSound')

        for player in self.gameflow.players:
            parts = []

            iterations = 20
            for i in range(iterations):
                parts.append(moveplayer.AnimationPart(self.PUMPING_COLOR *
                                                      float(iterations - 1 - i) / float(iterations), 0.1))
            self.gameflow.start_coroutine(player.sphere_color_animation(parts, on_intro_blinking_finished))

    def status_message(self):
        return 'Baloooon it pump it baloo the bear'

    def base_color(self):
        return self.PUMPING_COLOR

    def update(self):
        if self.players_ready < len(self.gameflow.players):
            return

        tunables = self.gameflow.get_tunables()

        for player in self.gameflow.players:
            if player.now_shaking(tunables):
                self.counters[player.player_number] += 1
                current_value = self.counters[player.player_number]
                mod = 7
                if current_value == tunables.ShakeItWinThreshold:
                    self.gameflow.play_sound('BalloonExplosionSound')
                    player.rumble = 1.0
                elif current_value % mod == 0:
                    mode = (current_value / mod) % 2
                    self.gameflow.play_sound('SqueakSound', 3.0 * float(current_value) / 100.0,
                                             1.0 if mode == 0 else 1.5)


            intensity = float(self.counters[player.player_number]) / float(tunables.ShakeItWinThreshold)
            base_intensity = tunables.ColorIntensityDuringGameplay

            player.led_color = self.PUMPING_COLOR * (base_intensity + (1.0 - base_intensity) * intensity)

            if self.counters[player.player_number] >= tunables.ShakeItWinThreshold:
                self.gameflow.end_current_game(player)
                break
