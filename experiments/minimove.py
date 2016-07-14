import time
import random

class Tasks(list):
    def schedule(self):
        time.sleep(min(task.wait_time for task in self))

        for task in list(self):
            if not task.schedule():
                self.remove(task)

tasks = Tasks()

class Task:
    def __init__(self, iterator):
        self.iterator = iterator
        self.run_after = time.time()

    @property
    def wait_time(self):
        return max(0., self.run_after - time.time())

    def schedule(self):
        if self.wait_time == 0.:
            try:
                wait_time = next(self.iterator)
                self.run_after = time.time() + wait_time
                return True
            except StopIteration:
                return False
        else:
            return True

class Winners(Exception):
    def __init__(self, winners):
        super().__init__('Winners are: {}'.format(repr(winners)))
        self.winners = winners

class color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return 'color(%.2f, %.2f, %.2f)' % (self.r, self.g, self.b)

    def __mul__(self, f):
        return color(self.r * f, self.g * f, self.b * f)

    __rmul__ = __mul__

    def __truediv__(self, f):
        return color(self.r / f, self.g / f, self.b / f)


class ForEachPlayerProperty:
    def __setattr__(self, key, value):
        for player in players:
            setattr(player.p, key, value)

    def __getattr__(self, key):
        return tuple(getattr(player.p, key) for player in players)

class PlayerList(list):
    def __init__(self, values):
        super().__init__(values)
        self.p = ForEachPlayerProperty()

    def each(self, func):
        tasks.extend(Task(func(player)) for player in self)

    def win(self, winning):
        raise Winners([player for player, is_winning in zip(self, winning) if is_winning])

    def update(self):
        for player in self:
            print('Would set {} to color={} and rumble={}'.format(player, player.p.color, player.p.rumble))

    def lose(self):
        raise Winners([])

class PlayerProperties:
    def __init__(self, player):
        self.player = player
        self.color = None
        self.rumble = 0

class Player:
    def __init__(self, index):
        self.index = index
        self.p = PlayerProperties(self)

    def wins(self):
        raise Winners([self])

    def __repr__(self):
        return '<Player {} (p={})>'.format(self.index, self.p.__dict__)

    def schedule(self, iterable):
        tasks.append(Task(iterable))

    @property
    def is_unstable(self):
        return (move.acceleration.magnitude >= tunables.unstable_threshold)

    @property
    def now_shaking(self):
        return random.choice([True, False])

    @property
    def safe_angle(self):
        v = vec2(move.acceleration.x, move.acceleration.y).normalized()
        result = math.atan2(v.x, v.y) * 180. / math.pi
        if result < 0:
            result += 360
        return result

    @property
    def pressed(self):
        return ['trigger']

    @property
    def pressed_colors(self):
        return [color for button, color in button_to_color.items() if button in self.pressed]

players = PlayerList([Player(i+1) for i in range(5)])

class tunables:
    win_animation_blinks = 10
    blink_duration_sec = 0.1
    win_animation_color = color(1., 1., 1.)
    shake_threshold = 3.5
    unstable_threshold = 1.2
    shake_it_win_threshold = 100
    default_number_of_games = 10
    game_win_animation_fades = 25
    game_win_animation_fade_steps = 5
    fade_duration_sec = 0.02
    game_win_animation_wait_before_sec = 0.5
    game_win_animation_wait_after_sec = 2
    color_intensity_during_gameplay = 0.2
    attract_loop_delay_sec = 0.4
    attract_start_delay_sec = 7.0

magenta = color(1., 0., 1.)
green = color(0., 1., 0.)
blue = color(0., 0., 1.)
red = color(1., 0., 0.)

button_to_color = {
    'square': magenta,
    'triangle': green,
    'cross': blue,
    'circle': red,
}

button_colors = list(button_to_color.values())

class Sounds(set):
    def play(self):
        for effect, volume in self:
            print('Would play {} at volume {}'.format(effect, volume))
        self.clear()

sounds = Sounds()

def sfx(effect, volume=1.0):
    sounds.add((effect, volume))
