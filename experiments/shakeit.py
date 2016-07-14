from minimove import sfx, players, tunables, color

PumpingColor = color(0., 1., 0.)

class MiniGame:
    def start(self):
        players.p.counter = 0
        players.p.alive = True
        sfx('BalloonAnnounceSound')

    def intro(self, player):
        for i in range(20):
            player.p.color = PumpingColor * i / 19.
            yield 0.1

    def each(self, player):
        if player.now_shaking:
            player.p.counter += 1
            if player.p.counter == tunables.shake_it_win_threshold:
                sfx('BalloonExplosionSound')
                player.wins()
            elif player.p.counter % 7 == 0:
                sfx('SqueakSound', player.p.counter / 100.)

        base = tunables.color_intensity_during_gameplay
        intensity = (base + (1. - base) * player.p.counter / 100.)
        player.p.color = PumpingColor * intensity
