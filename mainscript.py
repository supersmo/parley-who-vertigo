from gameflow import GameFlow
from coroutine import Coroutine

import os
import sdlmixer

class MainScript(object):
    def __init__(self, api):
        self.api = api
        self.coroutines = []
        self.mixer = sdlmixer.SDLMixer()
        self.sounds = {}

    def start(self):
        self.gameflow = GameFlow(self)

    def on_gui(self):
        print('='*30)
        print(self.gameflow.status_message())
        print('='*30)

    def update(self):
        self.gameflow.update()
        self.coroutines = [coroutine for coroutine in self.coroutines if coroutine.schedule()]

    def start_coroutine(self, crt):
        self.coroutines.append(Coroutine(crt))

    def get_controllers(self):
        return self.api.connected_controllers

    def play_sound(self, sound, volume=1.0, pitch=1.0):
        filename = {
            'GameWin1Sound': 'game-win1.wav',
            'GameWin2Sound': 'game-win2.wav',
            'WinPlayer1Sound': 'win-player1.wav',
            'WinPlayer2Sound': 'win-player2.wav',
            'ReadySound': 'ready.wav',
            'CycleBlipSound': 'cycle-blip.wav',
            'BeepSound': 'beep.wav',
            'BadBeepSound': 'bad-beep.wav',
            'SafeAnnounceSound': 'safe-announce.wav',
            'SafeClickSound': 'safe-click.wav',
            'BalloonAnnounceSound': 'balloon-announce.wav',
            'BalloonExplosionSound': 'balloon-explosion.wav',
            'SqueakSound': 'squeak.wav',
        }[sound]

        if filename not in self.sounds:
            self.sounds[filename] = self.mixer.load(os.path.join(os.path.dirname(__file__), 'sounds', filename))

        self.sounds[filename].play()

