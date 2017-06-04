from gameflow import GameFlow
from coroutine import Coroutine
from color import Color, to_rgba32
import psmovecolor

import os
import time
import math
import random

import sdl
import sdlmixer
import eglo
import fontaine


class MainScript(object):
    def __init__(self, api, use_chip):
        self.api = api
        self.coroutines = []
        if use_chip:
            self.eglo = eglo.EGLO()
        else:
            self.eglo = None
        scale = 2 if not use_chip else 0
        self.screen = self.mixer = sdlmixer.SDLMixer(480*scale, 272*scale)
        self.renderer = fontaine.GLTextRenderer(480, 272, os.path.join(os.path.dirname(__file__), 'art', 'pwv.tile'))

        self.renderer.enable_blending()
        self.sounds = {}

    def start(self):
        self.gameflow = GameFlow(self)

    def on_gui(self):
        print(end='\033[2J\033[;H')
        print('Parley Who Vertigo')
        print('='*30)
        game_title, game_description, scores = self.gameflow.status_message()
        print(game_title)
        print(game_description)
        print('='*30)
        for idx, score in enumerate(scores):
            print('Player %d: %s pts' % (idx+1, score))
        print('='*30)

    def update(self):
        alpha = 0.9

        base_color = Color(0.3, 0.3, 0.3)
        self.renderer.clear(0.0, 0.0, 0.0, 1.0)

        now = time.time()

        scale = 12.0

        move_says_choices = ['MoveSaysBlue', 'MoveSaysGreen', 'MoveSaysPurple', 'MoveSaysRed']
        move_says_now = move_says_choices[int(time.time())%len(move_says_choices)]

        lines = []

        game_title, game_description, scores = self.gameflow.status_message()

        image_name = {
            'MoveSays': move_says_now,
            'SafeCracker': 'SafeCrackerNormal',
            'ShakeIt': 'ShakeIt',
        }.get(game_title, 'ParleyWhoVertigo3')

        y = 220.0
        x = 20.0
        padding = 10

        scale = 2.0
        if image_name == 'ParleyWhoVertigo3' and game_title != 'AttractMode':
            lines.append((x, y, game_title, scale, 0.0, base_color * 0.6, 1.0))
        y += 8 * scale + padding

        scale = 1.0
        lines.append((x, y, game_description, scale, 0.0, base_color * 0.4, 1.0))
        y += 8 * scale + padding

        x = 10.0
        y = 10.0
        scale = 1.0
        for idx, score in enumerate(scores):
            lines.append((x, y, 'Player %d: %s pts' % (idx+1, score), scale, 0.0, base_color * 1.0, 1.0))
            y += 8 * scale + padding

        image_id = self.renderer.lookup_image(image_name)
        self.renderer.render_image(0, 0, 1.0, 0.0, 0xFFFFFFFF, image_id)

        self.renderer.flush()

        for x, y, text, scale, rotation, color, opacity in lines:
            self.renderer.enqueue(x, y, scale, rotation, to_rgba32(color, opacity), text)

        self.renderer.flush()

        if self.eglo is not None:
            self.eglo.swap_buffers()
        else:
            self.screen.update()

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

