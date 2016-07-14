from minimove import sfx, players, button_colors
import random

class MiniGame:
    def start(self):
        players.p.active = True
        players.p.ready = False

        sfx('BalloonAnnounceSound')

        @players.each
        def intro_animation(player):
            for i in range(10):
                sfx('CycleBlipSound')
                player.color = random.choice(button_colors)
                yield 0.1

                sfx('CycleBlipSound')
                player.color = None
                yield 0.1

            player.p.ready = True

            if all(players.p.ready):
                for player in players:
                    player.color = random.choice(button_colors)

    def button(self, player, button):
        if player.p.active and button.color == player.color:
            sfx('BeepSound', 0.5)
            player.wins()
        else:
            player.color = None
            player.p.active = False

        if not any(players.p.active):
            players.end_game(lambda player: False)
