#!./external/bin/python3.5

import os
import sys

EXTERNAL = os.path.join(os.path.dirname(__file__), 'external')

if 'PSMOVEAPI_LIBRARY_PATH' not in os.environ:
    os.environ['PSMOVEAPI_LIBRARY_PATH'] = EXTERNAL

sys.path.insert(0, EXTERNAL)

import psmoveapi
import time

from mainscript import MainScript

class API(psmoveapi.PSMoveAPI):
    def __init__(self):
        super().__init__()
        self.quit = False
        self.main_script = MainScript(self)
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

if len(api.connected_controllers) < 2:
    print('Not enough controllers to start the game')
    sys.exit(1)

fup = FixedUpdate(30)
gui = FixedUpdate(33)
while not api.quit:
    api.update()
    fup.update(api.main_script.update)
    gui.update(api.main_script.on_gui)
    time.sleep(1./60.)
