# Fontaine Bindings for Python
# 2016-12-26 Thomas Perl <m@thp.io>

from ctypes import CDLL, c_char_p, c_void_p, c_int, Structure, byref, c_byte, c_float, c_uint

import platform
import time
import math
import os

import sdl


if platform.system() == 'Darwin':
    ext = '.dylib'
elif platform.system() == 'Windows':
    ext = '.dll'
else:
    ext = '.so'

BASE = os.path.dirname(__file__)


class GLTextRenderer(object):
    def __init__(self, width, height):
        self.libfontainegl = CDLL(os.path.join(BASE, 'libfontainegl' + ext))
        self.fontaine_new = self.libfontainegl.fontaine_new
        self.fontaine_new.argtypes = [c_void_p, c_void_p, c_void_p]
        self.fontaine_new.restype = c_void_p
        self.fontaine_free = self.libfontainegl.fontaine_free
        self.fontaine_free.argtypes = [c_void_p]

        self._font = self.fontaine_new(None, None, None)

        self.gl_font_renderer_new = self.libfontainegl.gl_font_renderer_new
        self.gl_font_renderer_new.argtypes = [c_void_p, c_int, c_int]
        self.gl_font_renderer_new.restype = c_void_p
        self.gl_font_renderer_free = self.libfontainegl.gl_font_renderer_free
        self.gl_font_renderer_free.argtypes = [c_void_p]

        self._renderer = self.gl_font_renderer_new(self._font, width, height)
        self.gl_font_renderer_enable_blending = self.libfontainegl.gl_font_renderer_enable_blending
        self.gl_font_renderer_enable_blending.argtypes = [c_void_p]
        self.gl_font_renderer_clear = self.libfontainegl.gl_font_renderer_clear
        self.gl_font_renderer_clear.argtypes = [c_void_p, c_float, c_float, c_float, c_float]
        self.gl_font_renderer_enqueue = self.libfontainegl.gl_font_renderer_enqueue
        self.gl_font_renderer_enqueue.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_uint, c_char_p]
        self.gl_font_renderer_flush = self.libfontainegl.gl_font_renderer_flush
        self.gl_font_renderer_flush.argtypes = [c_void_p]

    def enable_blending(self):
        self.gl_font_renderer_enable_blending(self._renderer)

    def clear(self, r, g, b, a):
        self.gl_font_renderer_clear(self._renderer, r, g, b, a)

    def enqueue(self, x, y, scale, angle, color, text):
        self.gl_font_renderer_enqueue(self._renderer, x, y, scale, angle, color, c_char_p(text.encode('utf-8')))

    def flush(self):
        self.gl_font_renderer_flush(self._renderer)

    def __del__(self):
        try:
            self.gl_font_renderer_free(self._renderer)
        except:
            ...

        try:
            self.fontaine_free(self._font)
        except:
            ...


if __name__ == '__main__':
    screen = sdl.SDL(640, 480)
    renderer = GLTextRenderer(screen.width, screen.height)
    renderer.enable_blending()
    while True:
        for i in range(20):
            renderer.enqueue(i * 15.0, 4 * (i + 20.), 2. + .5 * math.sin(time.time()),
                    i, ((i*10) << 24) | 0x00006090, 'Hello World!')
        renderer.clear(0., 1., 1., 1.0)
        renderer.flush()
        screen.update()
