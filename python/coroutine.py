#
# Parley Who Vertigo
# Copyright 2016, 2017 Thomas Perl, Josef Who
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#


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
