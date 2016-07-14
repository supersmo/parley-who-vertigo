from minimove import sfx, players, tunables, color

import random

SafeColor = color(0.91, 0.78, 0.)

class SolveState:
    Searching, Found, Activated, Afterglow = range(4)

class MiniGame:
    angle_steps = 12
    threshold = 360 / angle_steps
    number_of_locks = 2

    def start(self):
        players.p.angle = 0.
        players.p.last_click_angle = 0.
        players.p.solved_locks = 0
        sfx('SafeAnnounceSound')

    def randomize_target_angle(self, player):
        player.p.target_angle = random.randint(0, self.angle_steps - 1) * 360 / self.angle_steps
        player.p.solve_state = SolveState.Searching

    def intro(self, player):
        for color, rumble, wait in ((SafeColor * 0.2, 0.6, 0.4), (SafeColor, 0, 0.5), (None, 0, 0.4)):
            player.p.color = color
            player.p.rumble = rumble
            yield wait

        self.randomize_target_angle(player)

    def each(self, player):
        if abs(player.safe_angle - player.p.last_click_angle) > 20.:
            sfx('SafeClickSound', 0.3)
            player.p.last_click_angle = player.safe_angle

        is_near = (player.safe_angle >= player.p.target_angle and
                   player.safe_angle <= player.p.target_angle + self.threshold)

        if player.p.solve_state == SolveState.Searching:
            if is_near and 'trigger' not in player.pressed:
                player.p.solve_state = SolveState.Found
        elif player.p.solve_state == SolveState.Found:
            if is_near:
                player.p.solve_state = SolveState.Searching
            elif 'trigger' in player.pressed:
                player.p.solve_state = SolveState.Activated
        elif player.p.solve_state == SolveState.Activated:
            player.p.solve_state = SolveState.Afterglow
            @player.schedule
            def reset_search():
                yield 0.2
                player.p.solved_locks += 1
                if player.p.solved_locks == self.number_of_locks:
                    player.wins()
                self.randomize_target_angle(player)

        if player.p.solve_state == SolveState.Searching:
            player.p.color = SafeColor * tunables.color_intensity_during_gameplay
            player.p.rumble = 0.
        elif player.p.solve_state == SolveState.Found:
            player.p.color = SafeColor * tunables.color_intensity_during_gameplay
            player.p.rumble = 0.5
        elif player.p.solve_state == SolveState.Activated:
            player.p.color = SafeColor
            player.p.rumble = 0.5
        elif player.p.solve_state == SolveState.Afterglow:
            player.p.color = SafeColor
            player.p.rumble = 1.
