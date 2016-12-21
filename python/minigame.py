class MiniGame(object):
    def __init__(self, gameflow):
        self.gameflow = gameflow

    def button_pressed(self, player, button):
        ...

    def status_message(self):
        return ''

    def start_game(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError
