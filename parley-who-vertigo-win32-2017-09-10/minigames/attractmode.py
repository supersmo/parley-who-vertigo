import minigame
import time

from color import Color

class AttractMode(minigame.MiniGame):
    # Not enabled as "normal" minigame, it's a special minigame we use directly
    ENABLED = False

    READY_COLOR = Color(0.4, 0.9, 0.0)

    def __init__(self, gameflow):
        super().__init__(gameflow)
        self.ticks = 0
        self.last_update = 0.0
        self.accumulator = 0.0
        self.everyone_ready = False
        self.game_start_time = 0.0
        self.intensities = []
        self.readyness = []

    def start_game(self):
        self.ticks = 0
        self.last_update = time.time()
        self.accumulator = 0.0
        self.everyone_ready = False
        self.game_start_time = 0.0
        self.intensities = [0.0 for player in self.gameflow.players]
        self.readyness = [False for player in self.gameflow.players]

    def base_color(self):
        return self.READY_COLOR

    def status_message(self):
        if len(self.intensities) < 2:
            return '%d controller(s) connected, need at least 2!' % (len(self.intensities),)
        elif self.everyone_ready:
            return 'Game starts in {:.2f} secs'.format(self.seconds_to_start())
        else:
            return 'Come and Play! Press MOVE'

    def seconds_to_start(self):
        return (self.game_start_time - time.time())

    def update(self):
        if len(self.intensities) < 2:
            return

        tunables = self.gameflow.get_tunables()

        for i in range(len(self.intensities)):
            self.intensities[i] *= 0.9

        # Update timestep
        now = time.time()
        self.accumulator += (now - self.last_update)
        self.last_update = now
        while self.accumulator > tunables.AttractLoopDelaySec and tunables.AttractLoopDelaySec > 0.001:
            self.intensities[self.ticks % len(self.intensities)] = 1.0
            self.ticks += 1
            self.accumulator -= tunables.AttractLoopDelaySec

        if self.everyone_ready:
            # Check if we're ready already
            if now >= self.game_start_time:
                self.gameflow.everyone_is_ready()
            else:
                # Fade out the controllers
                intensity = 2.0 * max(0.0, (self.game_start_time - now) / tunables.AttractStartDelaySec - 0.5)
                for player in self.gameflow.players:
                    player.led_color = self.READY_COLOR * intensity

            return

        # Update controllers and count how many are active
        num_pressed = 0
        for player in self.gameflow.players:
            if self.everyone_ready or player.is_move_pressed():
                if not self.readyness[player.player_number]:
                    self.gameflow.play_sound('ReadySound')
                self.intensities[player.player_number] = 1.0
                num_pressed += 1
                self.readyness[player.player_number] = True
            else:
                self.readyness[player.player_number] = False

            player.led_color = self.READY_COLOR * self.intensities[player.player_number]

        if not self.everyone_ready and num_pressed == len(self.gameflow.players):
            self.gameflow.play_sound('GameWin1Sound')
            self.everyone_ready = True
            self.game_start_time = time.time() + tunables.AttractStartDelaySec
