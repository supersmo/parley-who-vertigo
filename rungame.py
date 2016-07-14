from minimove import tasks, players, sounds

from freeze import MiniGame

class GameRunner:
    def __init__(self, game):
        self.game = game

    def run(self):
        self.game.start()

        @players.each
        def run_each(player):
            while hasattr(self.game, 'each'):
                self.game.each(player)
                yield 1. / 60.

        while tasks:
            tasks.schedule()
            sounds.play()

GameRunner(MiniGame()).run()
