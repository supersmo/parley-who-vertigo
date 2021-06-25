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


import os
import sys
import platform

os.chdir(os.path.dirname(__file__))

EXTERNAL = os.path.join(os.path.dirname(__file__), 'external')

sys.path.insert(0, EXTERNAL)

import ctypes_dll_search

use_chip = False
if platform.system() == 'Linux' and os.path.exists('/usr/bin/pocket-home'):
    ctypes_dll_search.library_path = os.path.join(EXTERNAL, 'pocketchip')
    use_chip = True
elif platform.system() == 'Darwin':
    ctypes_dll_search.library_path = os.path.join(EXTERNAL, 'macos')
elif platform.system() == 'Windows':
    ctypes_dll_search.library_path = os.path.join(EXTERNAL, 'win32')
else:
    print('Unknown/unsupported platform:', platform.system())


import psmoveapi
import time

from mainscript import MainScript

class API(psmoveapi.PSMoveAPI):
    def __init__(self):
        super().__init__()
        self.quit = False
        self.main_script = MainScript(self, use_chip)
        self.connected_controllers = []

    def on_connect(self, controller):
        print('Controller connected:', controller)
        if controller.bluetooth:
            self.connected_controllers.append(controller)

    def on_update(self, controller):
        ...

    def on_disconnect(self, controller):
        print('Controller disconnected:', controller)
        if controller in self.connected_controllers:
            self.connected_controllers.remove(controller)


class FixedUpdate(object):
    def __init__(self, fps):
        self.step = 1. / float(fps)
        self.accumulator = 0
        self.last = time.time()

    def update(self, callback):
        now = time.time()
        self.accumulator += (now - self.last)
        self.last = now
        while self.accumulator >= self.step:
            callback()
            self.accumulator -= self.step


api = API()
api.update()
api.main_script.start()

fup = FixedUpdate(30)
while not api.quit:
    api.update()
    fup.update(api.main_script.update)
    time.sleep(1./60.)
