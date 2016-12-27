# EGLO Bindings for Python
# 2016-12-27 Thomas Perl <m@thp.io>

from ctypes import CDLL, c_char_p, c_void_p, c_int, Structure, byref, c_byte, c_float, c_uint, POINTER

import time
import math
import os

class EgloEvent(Structure):
    _fields_ = [
            ('type', c_int),
            ('data', c_int * 3),
    ]

class EGLO(object):
    def __init__(self):
        self.libeglo = CDLL('eglo')
        self.eglo_init = self.libeglo.eglo_init
        self.eglo_init.argtypes = [POINTER(c_int), POINTER(c_int), c_int]
        self.eglo_init.restype = c_int
        self.eglo_next_event = self.libeglo.eglo_next_event
        self.eglo_next_event.argtypes = [c_void_p]
        self.eglo_next_event.restype = c_int
        self.eglo_swap_buffers = self.libeglo.eglo_swap_buffers
        self.eglo_quit = self.libeglo.eglo_quit

        width = c_int()
        height = c_int()
        self.eglo_init(byref(width), byref(height), 2)

    def swap_buffers(self):
        self.eglo_swap_buffers()

    def next_event(self):
        ev = EgloEvent()
        result = bool(self.eglo_next_event(byref(ev)))
        return result

    def __del__(self):
        try:
            self.eglo_quit()
        except:
            ...
