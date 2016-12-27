# SDL Bindings for Python
# 2016-12-26 Thomas Perl <m@thp.io>

from ctypes import CDLL, c_char_p, c_void_p, c_int, Structure, byref, c_byte


class SDL_Event(Structure):
    _fields_ = [
            ('type', c_byte),
            ('padding', c_int * 1024),
    ]


class SDL(object):
    SDL_INIT_AUDIO = 0x00000010
    SDL_INIT_VIDEO = 0x00000020
    SDL_OPENGL = 0x00000002

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.libSDL = CDLL('SDL')
        self.SDL_Init = self.libSDL.SDL_Init
        self.SDL_Init.argtypes = [c_int]
        self.SDL_SetVideoMode = self.libSDL.SDL_SetVideoMode
        self.SDL_SetVideoMode.argtypes = [c_int, c_int, c_int, c_int]
        self.SDL_PollEvent = self.libSDL.SDL_PollEvent
        self.SDL_PollEvent.argtypes = [c_void_p]
        self.SDL_PollEvent.restype = c_int
        self.SDL_Quit = self.libSDL.SDL_Quit
        self.SDL_GetError = self.libSDL.SDL_GetError
        self.SDL_GetError.restype = c_char_p
        self.SDL_GL_SwapBuffers = self.libSDL.SDL_GL_SwapBuffers

        if self.SDL_Init(self.SDL_INIT_VIDEO | self.SDL_INIT_AUDIO) == -1:
            raise RuntimeError(SDL_GetError().decode('utf-8'))

        if self.width != 0 and self.height != 0:
            self.SDL_SetVideoMode(width, height, 0, self.SDL_OPENGL)

    def update(self):
        event = SDL_Event()
        while self.SDL_PollEvent(byref(event)):
            if event.type == 12:  # SDL_QUIT
                raise RuntimeError('Quit')
        if self.width != 0 and self.height != 0:
            self.SDL_GL_SwapBuffers()

    def __del__(self):
        try:
            self.SDL_Quit()
        except:
            ...
