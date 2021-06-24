# SDL Mixer Bindings for Python
# 2016-12-20 Thomas Perl <m@thp.io>

from ctypes import CDLL, c_char_p, c_void_p, c_int, Structure, byref, c_byte

import sdl


class SDLMixer(sdl.SDL):
    AUDIO_S16LSB = 0x8010

    def __init__(self, width, height, frequency=22050, channels=2):
        super().__init__(width, height)

        self.SDL_RWFromFile = self.libSDL.SDL_RWFromFile
        self.SDL_RWFromFile.argtypes = [c_char_p, c_char_p]
        self.SDL_RWFromFile.restype = c_void_p

        self.libSDL_mixer = CDLL('SDL_mixer')
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
        self.Mix_AllocateChannels = self.libSDL_mixer.Mix_AllocateChannels
        self.Mix_AllocateChannels.argtypes = [c_int]

        self.Mix_Init(0)

        if self.Mix_OpenAudio(frequency, self.AUDIO_S16LSB, channels, 1024) == -1:
            raise RuntimeError(self.SDL_GetError().decode('utf-8'))

        self.Mix_AllocateChannels(64)

    def load(self, filename):
        rw = self.SDL_RWFromFile(c_char_p(filename.encode('utf-8')), c_char_p(b'rb'))
        chunk = self.Mix_LoadWAV_RW(rw, 1)
        return Sample(self, chunk)

    def __del__(self):
        self.Mix_CloseAudio()
        self.Mix_Quit()
        super().__del__()


class Sample(object):
    def __init__(self, mixer, chunk):
        self.mixer = mixer
        self.chunk = chunk

    def play(self, loops=0):
        self.mixer.Mix_PlayChannelTimed(-1, self.chunk, loops, -1)

    def __del__(self):
        self.mixer.Mix_FreeChunk(self.chunk)
