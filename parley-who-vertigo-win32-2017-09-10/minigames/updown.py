import minigame
import moveplayer

from color import Color

class UpDown(minigame.MiniGame):
    ENABLED = False

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.current_color = Color.WHITE

    def start_game(self):
        ...

    def status_message(self):
        return 'Up and Down we GO!'

    def base_color(self):
        return self.current_color

    def update(self):
        tunables = self.gameflow.get_tunables()

        for player in self.gameflow.players:
            value = player.get_accelerometer_x()
            if value < -1:
                value = -1
            elif value > +1:
                value = +1

            if value > 0:
                sign_color = Color.GREEN
            else:
                sign_color = Color.RED
                value *= -1

            player.led_color = sign_color * value
            if player.player_number == 0:
                self.current_color = player.led_color
