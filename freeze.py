FreezingBlue = color(0., 0.4, 0.9)

class MiniGame:
    def status(self):
        return 'Freeze, man!'

    def start(self):
        # Set minigame-specific property on all players
        players.p.ready = False

        def intro_animation(player):
            for i in range(4):
                sfx('CycleBlipSound') # play sound effect
                player.color = FreezingBlue # set color of single player
                yield 0.4 # wait for 0.4 seconds

                sfx('CycleBlipSound')
                player.color = black
                yield 0.2

            sfx('BeepSound')
            player.p.ready = True

            # players.p.ready returns list of properties for each player
            if all(players.p.ready):
                # Set property on all players
                players.p.alive = True
                # set color of all players
                players.color = FreezingBlue

        # run coroutine for each playyer
        players.each(intro_animation)

    def update(self):
        for player in players:
            if player.p.alive and player.is_unstable:
                player.p.alive = False
                player.color = black
                sfx('BalloonExplosionSound')

                if sum(players.p.alive) == 1:
                    # Assign the winner property from the alive property
                    players.p.winner = players.p.alive
                    return end_game()

    def can_support(self, num_players):
        return True
