# SDL Mixer Bindings for Python
# 2016-12-20 Thomas Perl <m@thp.io>

from ctypes import CDLL, c_char_p, c_void_p, c_int

import time
import platform
import sys


if platform.system() == 'Darwin':
    ext = '.dylib'
elif platform.system() == 'Windows':
    ext = '.dll'
else:
    ext = '.so'


class SDLMixer(object):
    SDL_INIT_AUDIO = 0x00000010
    AUDIO_S16LSB = 0x8010

    def __init__(self, frequency=22050, channels=2, init_sdl=True):
        self.libSDL = CDLL('libSDL' + ext)
        self.SDL_Init = self.libSDL.SDL_Init
        self.SDL_Init.argtypes = [c_int]
        self.SDL_Quit = self.libSDL.SDL_Quit
        self.SDL_RWFromFile = self.libSDL.SDL_RWFromFile
        self.SDL_RWFromFile.argtypes = [c_char_p, c_char_p]
        self.SDL_RWFromFile.restype = c_void_p
        self.SDL_GetError = self.libSDL.SDL_GetError
        self.SDL_GetError.restype = c_char_p

        self.libSDL_mixer = CDLL('libSDL_mixer' + ext)
        self.Mix_Init = self.libSDL_mixer.Mix_Init
        self.Mix_Quit = self.libSDL_mixer.Mix_Quit
        self.Mix_OpenAudio = self.libSDL_mixer.Mix_OpenAudio
        self.Mix_OpenAudio.argtypes = [c_int, c_int, c_int, c_int]
        self.Mix_CloseAudio = self.libSDL_mixer.Mix_CloseAudio
        self.Mix_LoadWAV_RW = self.libSDL_mixer.Mix_LoadWAV_RW
        self.Mix_LoadWAV_RW.argtypes = [c_void_p, c_int]
        self.Mix_LoadWAV_RW.restype = c_void_p
        self.Mix_PlayChannelTimed = self.libSDL_mixer.Mix_PlayChannelTimed
        self.Mix_PlayChannelTimed.argtypes = [c_int, c_void_p, c_int, c_int]
        self.Mix_FreeChunk = self.libSDL_mixer.Mix_FreeChunk
        self.Mix_FreeChunk.argtypes = [c_void_p]

        self.sdl_inited = False
        if init_sdl:
            if self.SDL_Init(self.SDL_INIT_AUDIO) == -1:
                raise RuntimeError(SDL_GetError().decode('utf-8'))
            self.sdl_inited = True

        self.Mix_Init(0)

        if self.Mix_OpenAudio(frequency, self.AUDIO_S16LSB, channels, 1024) == -1:
            raise RuntimeError(SDL_GetError().decode('utf-8'))

    def load(self, filename):
        rw = self.SDL_RWFromFile(c_char_p(filename.encode('utf-8')), c_char_p(b'rb'))
        chunk = self.Mix_LoadWAV_RW(rw, 1)
        return Sample(self, chunk)

    def __del__(self):
        self.Mix_CloseAudio()
        self.Mix_Quit()
        if self.sdl_inited:
            self.SDL_Quit()


class Sample(object):
    def __init__(self, mixer, chunk):
        self.mixer = mixer
        self.chunk = chunk

    def play(self, loops=0):
        self.mixer.Mix_PlayChannelTimed(-1, self.chunk, loops, -1)

    def __del__(self):
        self.mixer.Mix_FreeChunk(self.chunk)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: {} /path/to/wavfile.wav'.format(sys.argv[0]))
        sys.exit(1)
    mixer = SDLMixer()
    sound = mixer.load(sys.argv[1])
    print('Playing sound 4 times...')
    for i in range(4):
        sound.play()
        time.sleep(0.3)
    print('Will stop playing after 3 seconds...')
    time.sleep(3)
