from minimove import sfx, players, color

FreezingBlue = color(0., 0.4, 0.9)

class MiniGame:
    def start(self):
        players.p.alive = True
        players.p.ready = False

        @players.each
        def intro_animation(player):
            for i in range(4):
                sfx('CycleBlipSound')
                player.color = FreezingBlue
                yield 0.4

                sfx('CycleBlipSound')
                player.color = None
                yield 0.2

            sfx('BeepSound')
            player.color = FreezingBlue
            player.p.ready = True

            if all(players.p.ready):
                players.p.alive = True

    def each(self, player):
        if not all(players.p.ready):
            return

        if player.p.alive and player.is_unstable:
            sfx('BalloonExplosionSound')
            player.p.alive = False

        player.color = FreezingBlue if player.p.alive else None

        if sum(players.p.alive) < 2:
            players.end_game(lambda player: player.p.alive)
