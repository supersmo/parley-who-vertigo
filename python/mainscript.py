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


class Particle(object):
    NORMAL, FADING_OUT, FADING_IN = range(3)

    def __init__(self, text, dx, dy, rotation, dr):
        self.text = text
        self.state = self.FADING_IN
        self.x = random.uniform(-1000, 1000)
        self.y = random.uniform(-1000, 1000)
        self.dx = dx
        self.dy = dy
        self.rotation = rotation
        self.dr = dr
        self.opacity = 0.0

    def step(self):
        self.x += self.dx
        self.y += self.dy
        self.rotation += self.dr
        if self.state == self.FADING_IN:
            if self.opacity >= 1.0:
                self.opacity = 1.0
                self.state = self.NORMAL
            else:
                self.opacity += 0.02
        elif self.state == self.FADING_OUT:
            if self.opacity <= 0.0:
                self.opacity = 0.0
                self.reset()
            else:
                self.opacity -= 0.02
        elif self.x < -1000 or self.x > 1000:
            self.state = self.FADING_OUT
        elif self.y < -1000 or self.y > 1000:
            self.state = self.FADING_OUT

    def reset(self):
        if self.x < -1000:
            self.x = 1000
        elif self.x > 1000:
            self.x = -1000
        if self.y < -1000:
            self.y = 1000
        elif self.y > 1000:
            self.y = -1000
        self.state = self.FADING_IN


class MainScript(object):
    def __init__(self, api, use_chip):
        self.api = api
        self.coroutines = []
        if use_chip:
            self.eglo = eglo.EGLO()
        else:
            self.eglo = None
        self.screen = self.mixer = sdlmixer.SDLMixer(1024 if not use_chip else 0, 600 if not use_chip else 0)
        self.renderer = fontaine.GLTextRenderer(1024, 600)
        self.renderer.enable_blending()
        self.sounds = {}
        self.current_base_color = Color(0.3, 0.3, 0.3)
        self.line_particles = [
            Particle(random.choice(['Parley', 'Who', 'Vertigo']),
                     random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 3), random.uniform(-0.005, 0.005))
            for _ in range(30 if use_chip else 100)
        ]

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

        if self.gameflow.current_game is not None:
            self.current_base_color *= alpha
            self.current_base_color += self.gameflow.current_game.base_color() * (1.0 - alpha)

        base_color = self.current_base_color
        bg_color = base_color * 0.1
        self.renderer.clear(bg_color.r, bg_color.g, bg_color.b, 1.0)

        now = time.time()

        scale = 12.0

        for particle in self.line_particles:
            particle.step()

        lines = [
            # x, y, text, scale, rotation, color, opacity
            (p.x, p.y, p.text, scale, p.rotation, self.current_base_color * 0.3, 0.1 * p.opacity)
            for p in self.line_particles
        ]

        game_title, game_description, scores = self.gameflow.status_message()

        y = 500.0
        x = 30.0
        padding = 10

        scale = 5.0
        lines.append((x, y, game_title, scale, 0.0, base_color * 0.6, 1.0))
        y += 8 * scale + padding

        x += padding

        scale = 2.0
        lines.append((x, y, game_description, scale, 0.0, base_color * 0.4, 1.0))
        y += 8 * scale + padding

        x = 80.0
        y = 80.0
        scale = 7.0
        for idx, score in enumerate(scores):
            lines.append((x, y, 'Player %d: %s pts' % (idx+1, score), scale, 0.0, base_color * 1.0, 1.0))
            y += 8 * scale + padding

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

