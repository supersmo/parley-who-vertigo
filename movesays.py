from minimove import sfx, players, button_colors
import random

class MiniGame:
    def start(self):
        players.p.active = True
        sfx('BalloonAnnounceSound')

    def intro(self, player):
        for i in range(10):
            sfx('CycleBlipSound')
            player.p.color = random.choice(button_colors)
            yield 0.1

            sfx('CycleBlipSound')
            player.p.color = None
            yield 0.1

        player.p.color = random.choice(button_colors)

    def each(self, player):
        if player.pressed_colors:
            if player.p.active and player.p.color in player.pressed_colors:
                sfx('BeepSound', 0.5)
                player.wins()
            else:
                player.p.color = None
                player.p.active = False

        if not any(players.p.active):
            players.lose()
