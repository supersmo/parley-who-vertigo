from minimove import tasks, players, sounds, Winners

from shakeit import MiniGame as ShakeItMiniGame
from freeze import MiniGame as FreezeMiniGame
from safecracker import MiniGame as SafeCrackerMiniGame
from movesays import MiniGame as MoveSaysMiniGame

def run_game(game):
    players.p.ready = False

    game.start()

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
        players.update()
        tasks.schedule()
        sounds.play()

try:
    run_game(ShakeItMiniGame())
except Winners as winners:
    print('Winners: {}'.format(winners.winners))
