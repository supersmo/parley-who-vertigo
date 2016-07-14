from minimove import sfx, players, tunables, color

import random

SafeColor = color(0.91, 0.78, 0.)

class SolveState:
    Searching, Found, Activated, Afterglow = range(4)

angle_steps = 12
threshold = 360 / angle_steps
number_of_locks = 2

def randomize_target_angle(player):
    player.p.target_angle = random.randint(0, angle_steps - 1) * 360 / angle_steps
    player.p.solve_state = SolveState.Searching

class MiniGame:
    def start(self):
        players.p.angle = 0.
        players.p.last_click_angle = 0.
        players.p.solved_locks = 0
        sfx('SafeAnnounceSound')

    def intro(self, player):
        player.p.color = SafeColor * 0.2
        player.p.rumble = 0.6
        yield 0.4

        player.p.color = SafeColor
        player.p.rumble = 0.
        yield 0.5

        player.p.color = None
        yield 0.4

        randomize_target_angle(player)

    def each(self, player):
        new_angle = player.safe_angle

        if abs(new_angle - player.p.last_click_angle) > 20.:
            sfx('SafeClickSound', 0.3)
            player.p.last_click_angle = new_angle

        player.p.angle = new_angle

        is_near = (player.p.angle >= player.p.target_angle and
                   player.p.angle <= player.p.target_angle + threshold)

        if player.p.solve_state == SolveState.Searching:
            if is_near and 'trigger' not in player.pressed:
                player.p.solve_state = SolveState.Found
        elif player.p.solve_state == SolveState.Found:
            if is_near:
                player.p.solve_state = SolveState.Searching
            elif 'trigger' in player.pressed:
                player.p.solve_state = SolveState.Activated
        elif player.p.solve_state == SolveState.Activated:
            @player.schedule
            def reset_search():
                yield 0.2
                player.p.solved_locks += 1
                if player.p.solved_locks == number_of_locks:
                    player.wins()
        randomize_target_angle(player)

            player.p.solve_state = SolveState.Afterglow

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
