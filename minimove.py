import glob
import os
import sys

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'github', 'psmoveapi')

if 'PSMOVEAPI_LIBRARY_PATH' not in os.environ:
    os.environ['PSMOVEAPI_LIBRARY_PATH'] = os.path.join(BASE, 'build')

sys.path.insert(0, os.path.join(BASE, 'bindings', 'python'))

import psmoveapi
import simpleaudio

class Sounds():
    def __init__(self, dirname):
        self.dirname = dirname
        self._sounds = {}

    def play(self, filename):
        if filename not in self._sounds:
            self._sounds[filename] = simpleaudio.WaveObject.from_wave_file(os.path.join(self.dirname, filename))

        return self._sounds[filename].play()


sounds = Sounds('sounds')

#for filename in glob.glob('sounds/*.wav'):
#    print(filename)
#    sounds.play(os.path.basename(filename)).wait_done()

class MoveTestApp(psmoveapi.PSMoveAPI):
    def __init__(self):
        super().__init__()
        self.quit = False

    def on_connect(self, controller):
        print('Controller connected:', controller)

    def on_update(self, controller):
        print('Update controller:', controller)
        print(controller.accelerometer, '->', controller.color, 'usb:', controller.usb, 'bt:', controller.bluetooth)
        up_pointing = min(1, max(0, 0.5 + 0.5 * controller.accelerometer.y))
        controller.color = psmoveapi.RGB(controller.trigger, up_pointing, 1.0 if controller.usb else 0.0)
        if controller.now_pressed(psmoveapi.Button.CROSS):
            sounds.play('ready.wav')
        if controller.now_pressed(psmoveapi.Button.SQUARE):
            sounds.play('beep.wav')
        if controller.now_pressed(psmoveapi.Button.TRIANGLE):
            sounds.play('cycle-blip.wav')
        if controller.now_pressed(psmoveapi.Button.CIRCLE):
            sounds.play('safe-click.wav')

        if controller.now_pressed(psmoveapi.Button.PS):
            self.quit = True

    def on_disconnect(self, controller):
        print('Controller disconnected:', controller)


api = MoveTestApp()
while not api.quit:
    api.update()
