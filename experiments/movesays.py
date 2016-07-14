from minimove import sfx, players, button_colors
import random

class MiniGame:
    def start(self):
        players.p.alive = True

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
            if player.p.alive and player.p.color in player.pressed_colors:
                sfx('BeepSound', 0.5)
                player.wins()
            else:
                player.p.color = None
                player.p.alive = False

        if not any(players.p.alive):
            players.lose()
