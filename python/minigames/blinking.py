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
