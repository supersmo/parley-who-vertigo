# Fontaine Bindings for Python
# 2016-12-26 Thomas Perl <m@thp.io>

from ctypes import CDLL, c_char_p, c_void_p, c_int, Structure, byref, c_byte, c_float, c_uint32

import time
import math
import os

import sdl


class GLTextRenderer(object):
    def __init__(self, width, height, tile_filename=None):
        self.libfontainegl = CDLL('fontainegl')
        self.fontaine_new = self.libfontainegl.fontaine_new
        self.fontaine_new.argtypes = [c_void_p, c_void_p, c_void_p]
        self.fontaine_new.restype = c_void_p
        self.fontaine_free = self.libfontainegl.fontaine_free
        self.fontaine_free.argtypes = [c_void_p]
        self.tile_context_new = self.libfontainegl.tile_context_new
        self.tile_context_new.argtypes = []
        self.tile_context_new.restype = c_void_p
        self.tile_context_load_file = self.libfontainegl.tile_context_load_file
        self.tile_context_load_file.argtypes = [c_void_p, c_char_p]
        self.tile_context_destroy = self.libfontainegl.tile_context_destroy
        self.tile_context_destroy.argtypes = [c_void_p]

        self._font = self.fontaine_new(None, None, None)
        self._tile = self.tile_context_new()

        if tile_filename is not None:
            self.tile_context_load_file(self._tile, c_char_p(tile_filename.encode('utf-8')))

        self.gl_font_renderer_new_with_tile = self.libfontainegl.gl_font_renderer_new_with_tile
        self.gl_font_renderer_new_with_tile.argtypes = [c_void_p, c_int, c_int, c_void_p]
        self.gl_font_renderer_new_with_tile.restype = c_void_p
        self.gl_font_renderer_free = self.libfontainegl.gl_font_renderer_free
        self.gl_font_renderer_free.argtypes = [c_void_p]

        self._renderer = self.gl_font_renderer_new_with_tile(self._font, width, height, self._tile)
        self.gl_font_renderer_enable_blending = self.libfontainegl.gl_font_renderer_enable_blending
        self.gl_font_renderer_enable_blending.argtypes = [c_void_p]
        self.gl_font_renderer_clear = self.libfontainegl.gl_font_renderer_clear
        self.gl_font_renderer_clear.argtypes = [c_void_p, c_float, c_float, c_float, c_float]
        self.gl_font_renderer_enqueue = self.libfontainegl.gl_font_renderer_enqueue
        self.gl_font_renderer_enqueue.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_uint32, c_char_p]
        self.gl_font_renderer_flush = self.libfontainegl.gl_font_renderer_flush
        self.gl_font_renderer_flush.argtypes = [c_void_p]
        self.gl_font_renderer_lookup_image = self.libfontainegl.gl_font_renderer_lookup_image
        self.gl_font_renderer_lookup_image.argtypes = [c_void_p, c_char_p]
        self.gl_font_renderer_lookup_image.restype = c_uint32
        self.gl_font_renderer_render_image = self.libfontainegl.gl_font_renderer_render_image
        self.gl_font_renderer_render_image.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_uint32, c_uint32]

    def enable_blending(self):
        self.gl_font_renderer_enable_blending(self._renderer)

    def clear(self, r, g, b, a):
        self.gl_font_renderer_clear(self._renderer, r, g, b, a)

    def enqueue(self, x, y, scale, angle, color, text):
        self.gl_font_renderer_enqueue(self._renderer, x, y, scale, angle, color, c_char_p(text.encode('utf-8')))

    def flush(self):
        self.gl_font_renderer_flush(self._renderer)

    def lookup_image(self, name):
        return self.gl_font_renderer_lookup_image(self._renderer, c_char_p(name.encode('utf-8')))

    def render_image(self, x, y, scale, angle, color, image_id):
        self.gl_font_renderer_render_image(self._renderer, x, y, scale, angle, color, image_id)

    def __del__(self):
        try:
            self.gl_font_renderer_free(self._renderer)
        except:
            ...

        try:
            self.fontaine_free(self._font)
        except:
            ...

        try:
            self.tile_context_destroy(self._tile)
        except:
            ...

