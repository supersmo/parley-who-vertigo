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
import psmovecolor
import psmoveapi

from color import Color

class Blinking(minigame.MiniGame):
    ENABLED = False

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.counters = []
        self.BLINKING_COLOR = psmovecolor.PSMoveColor.get_random_color()

    def start_game(self):
        for player in self.gameflow.players:
            player.was_unstable_last_time = False

    def status_message(self):
        return 'is Josefs game running, who knows?'

    def base_color(self):
        return self.BLINKING_COLOR

    def update(self):

        tunables = self.gameflow.get_tunables()

        for player in self.gameflow.players:
            # if player.is_trigger_pressed():
            # if player.is_button_down(psmoveapi.Button.TRIANGLE):
            if player.is_unstable(tunables):
                player.rumble = 0.5
                player.led_color = self.BLINKING_COLOR * 0.5
                if not player.was_unstable_last_time:
                    self.gameflow.play_sound("SafeAnnounceSound")
                player.was_unstable_last_time = True
            else: 
                player.rumble = 0
                player.led_color = Color.BLACK
                player.was_unstable_last_time = False
