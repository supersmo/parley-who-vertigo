import minigame
import psmovecolor
import color
import moveplayer

class MoveSays(minigame.MiniGame):
    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.players_ready = 0
        self.players_remaining = 0

    def status_message(self):
        return 'Pressz se KOLOR!'

    def start_game(self):
        def on_intro_blinking_finished():
            self.players_ready += 1
            if self.players_ready == len(self.gameflow.players):
                for player in self.gameflow.players:
                    player.led_color = psmovecolor.PSMoveColor.get_random_color()
                self.players_remaining = self.players_ready

        for player in self.gameflow.players:
            parts = []
            for i in range(10):
                parts.append(moveplayer.AnimationPart(psmovecolor.PSMoveColor.get_random_color(), 0.1))
                parts.append(moveplayer.AnimationPart(color.Color.BLACK, 0.1))

            def on_changed():
                self.gameflow.play_sound('CycleBlipSound')

            self.gameflow.start_coroutine(player.sphere_color_animation(parts, on_intro_blinking_finished, on_changed))

    def button_pressed(self, player, button):
        if self.players_ready < len(self.gameflow.players):
            return

        if psmovecolor.PSMoveColor.is_color_button(button):
            color = psmovecolor.PSMoveColor.color_for_button(button)
            if color == player.led_color:
                self.gameflow.play_sound('BeepSound', 0.5)
                self.gameflow.end_current_game(player)
            else:
                self.gameflow.play_sound('BadBeepSound', 0.5)
                # TODO: Play "dead" animation
                player.led_color = color.Color.BLACK
                self.players_remaining -= 1
                if self.players_remaining == 0:
                    self.gameflow.end_current_game_no_winner()

    def update(self):
        ...
