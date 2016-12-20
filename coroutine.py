import time


class WaitForSeconds(object):
    def __init__(self, duration):
        self.duration = duration


class Coroutine(object):
    def __init__(self, iterable):
        self.iterable = iterable
        self.next_run = time.time()
        self.active = True

    def schedule(self):
        if not self.active:
            return False

        now = time.time()
        if self.next_run <= now:
            try:
                value = next(self.iterable)
            except StopIteration:
                self.active = False
                return False

            if isinstance(value, WaitForSeconds):
                self.next_run = now + value.duration
            else:
                raise ValueError('Do not know how to handle: {:r}'.format(value))

        return True
