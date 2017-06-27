from gameflow import GameFlow
from coroutine import Coroutine
from color import Color, to_rgba32
import psmovecolor

import os
import time
import math
import random
import threading

import sdl
import sdlmixer
import eglo
import fontaine


class MainScript(object):
    def __init__(self, api, use_chip):
        self.api = api
        self.use_chip = use_chip
        self.coroutines = []
        self._render_thread = threading.Thread(target=self.ui_loop)
        self._render_thread.setDaemon(True)
        self._render_thread.start()
        self.sounds = {}

    def ui_loop(self):
        if self.use_chip:
            self.eglo = eglo.EGLO()
        else:
            self.eglo = None
        scale = 2 if not self.use_chip else 0
        self.screen = self.mixer = sdlmixer.SDLMixer(480*scale, 272*scale)
        self.renderer = fontaine.GLTextRenderer(480, 272, os.path.join(os.path.dirname(__file__), 'art', 'pwv.tile'))

        self.renderer.enable_blending()

        while True:
            self.render()
            time.sleep(1./20.)

    def start(self):
        self.gameflow = GameFlow(self)

    def update(self):
        self.gameflow.update()
        self.coroutines = [coroutine for coroutine in self.coroutines if coroutine.schedule()]

    def render(self):
        self.renderer.clear(0.0, 0.0, 0.0, 1.0)

        move_says_choices = ['MoveSaysBlue', 'MoveSaysGreen', 'MoveSaysPurple', 'MoveSaysRed']
        move_says_now = move_says_choices[int(time.time())%len(move_says_choices)]

        game_title, game_description, scores = self.gameflow.status_message()

        image_name = {
            'MoveSays': move_says_now,
            'SafeCracker': 'SafeCrackerNormal',
            'ShakeIt': 'ShakeIt',
            'Freeze': 'Freeze',
            'AttractMode': 'ParleyWhoVertigo3',
        }.get(game_title, 'PWVLogo272')

        image_id = self.renderer.lookup_image(image_name)
        self.renderer.render_image(0, 0, 1.0, 0.0, 0xFFFFFFFF, image_id)

        self.renderer.flush()

        if self.eglo is not None:
            self.eglo.swap_buffers()
        else:
            self.screen.update()

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

