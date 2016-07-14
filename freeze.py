from minimove import sfx, players, color

FreezingBlue = color(0., 0.4, 0.9)

class MiniGame:
    def start(self):
        players.p.alive = True

    def intro(self, player):
        for i in range(4):
            sfx('CycleBlipSound')
            player.p.color = FreezingBlue
            yield 0.4

            sfx('CycleBlipSound')
            player.p.color = None
            yield 0.2

        sfx('BeepSound')
        player.p.color = FreezingBlue

    def each(self, player):
        if player.p.alive and player.is_unstable:
            sfx('BalloonExplosionSound')
            player.p.alive = False

        player.p.color = FreezingBlue if player.p.alive else None

        if sum(players.p.alive) < 2:
            players.win(players.p.alive)
