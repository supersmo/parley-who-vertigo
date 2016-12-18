class MainScript(object):
    def start(self):
        self.gameflow = GameFlow(self)

    def on_gui(self):
        # TODO: Draw self.gameflow.status_message()
        ...

    def update(self):
        self.gameflow.update()
