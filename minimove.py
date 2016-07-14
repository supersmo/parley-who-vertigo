import time

class Tasks(list):
    def schedule(self):
        time.sleep(max(task.wait_time for task in self))

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
                #print('Would wait for {} seconds'.format(wait_time))
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

    def end_game(self, winning_condition):
        raise Winners([player for player in self if winning_condition(player)])

class PlayerProperties:
    ...

class Player:
    def __init__(self, index):
        self.index = index
        self.p = PlayerProperties()
        self._color = None

    def __repr__(self):
        return '<Player {} (p={})>'.format(self.index, self.p.__dict__)

    def __setattr__(self, key, value):
        if key == 'color':
            if self._color != value:
                print('Would set color to {}'.format(value))
                self._color = value
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        if key == 'is_unstable':
            return (input('Is {} unstable? (y/n) '.format(self)) == 'y')
        else:
            return super().__getattr__(key)

players = PlayerList([Player(i+1) for i in range(5)])

class tunables:
    ...

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
