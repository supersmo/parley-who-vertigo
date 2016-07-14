from minimove import tasks, players, sounds, Winners

#from shakeit import MiniGame
#from freeze import MiniGame
#from safecracker import MiniGame
from movesays import MiniGame

def run_game(game):
    game.start()

    players.p.ready = False
    @players.each
    def run_intro(player):
        yield from game.intro(player)
        player.p.ready = True

    @players.each
    def run_each(player):
        while True:
            if all(players.p.ready):
                game.each(player)
            yield 1. / 60.

    while tasks:
        tasks.schedule()
        sounds.play()
        print(', '.join(repr((player.p.color, player.p.rumble)) for player in players), end='\r')

try:
    run_game(MiniGame())
except Winners as winners:
    print('Winners: {}'.format(winners.winners))
