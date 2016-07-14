from minimove import sfx, players, button_colors, button_to_color
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
                player.p.color = random.choice(button_colors)
                yield 0.1

                sfx('CycleBlipSound')
                player.p.color = None
                yield 0.1

            player.p.ready = True

            if all(players.p.ready):
                for player in players:
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
            players.end_game(lambda player: False)
