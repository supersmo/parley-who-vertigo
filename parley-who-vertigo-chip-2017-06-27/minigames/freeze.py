import minigame
import moveplayer

from color import Color

class Freeze(minigame.MiniGame):
    ENABLED = True

    FREEZING_BLUE = Color(0, 0.4, 0.9)

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.alive = []
        self.alive_players = 0
        self.players_ready = 0

    def start_game(self):
        def on_intro_blinking_finished():
            self.gameflow.play_sound('BeepSound')

            self.players_ready += 1

            if self.players_ready == len(self.gameflow.players):
                self.alive = [True for player in self.gameflow.players]

                for player in self.gameflow.players:
                    player.led_color = self.FREEZING_BLUE

                self.alive_players = len(self.gameflow.players)

        for player in self.gameflow.players:
            parts = []

            for i in range(4):
                parts.append(moveplayer.AnimationPart(self.FREEZING_BLUE, 0.4))
                parts.append(moveplayer.AnimationPart(Color.BLACK, 0.2))

            def on_changed():
                self.gameflow.play_sound('CycleBlipSound')

            self.gameflow.start_coroutine(player.sphere_color_animation(parts, on_intro_blinking_finished, on_changed))

    def status_message(self):
        return 'Freeze, man!'

    def base_color(self):
        return self.FREEZING_BLUE

    def update(self):
        if self.players_ready < len(self.gameflow.players):
            return

        tunables = self.gameflow.get_tunables()

        for player in self.gameflow.players:
            if self.alive[player.player_number] and player.is_unstable(tunables):
                self.alive[player.player_number] = False
                self.alive_players -= 1
                player.led_color = Color.BLACK
                self.gameflow.play_sound('BalloonExplosionSound')

                if self.alive_players == 1:
                    for winner in self.gameflow.players:
                        if self.alive[winner.player_number]:
                            self.gameflow.end_current_game(winner)
                            return
