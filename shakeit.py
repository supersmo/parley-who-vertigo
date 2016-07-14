from minimove import sfx, players, tunables

PumpingColor = color(0., 1., 0.)

class MiniGame:
    def start(self):
        players.p.counter = 0
        players.p.ready = False

        sfx('BalloonAnnounceSound')

        @players.each
        def intro_animation(player):
            for i in range(20):
                player.color = PumpingColor * i / 19.
                yield 0.1

            player.p.ready = True

            if all(players.p.ready):
                players.p.alive = True

    def each(self, player):
        if not all(players.p.ready):
            return

        if player.now_shaking:
            player.p.counter += 1
            if player.p.counter == tunables.shake_it_win_threshold:
                sfx('BalloonExplosionSound')
                player.rumble = 1.
                player.wins()
            elif player.p.counter % 7 == 0:
                sfx('SqueakSound', player.p.counter / 100.)

        base = tunables.color_intensity_during_gameplay
        intensity = (base + (1. - base) * player.p.counter / 100.)
        player.color = PumpingColor * intensity
