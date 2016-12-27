# Monkey-patch ctypes' CDLL class to auto-resolve library path and names
# 2016-12-27 Thomas Perl <m@thp.io>

import ctypes
import platform
import os

if platform.system() == 'Darwin':
    ext = '.dylib'
    pfx = 'lib'
elif platform.system() == 'Windows':
    ext = '.dll'
    pfx = ''
else:
    ext = '.so'
    pfx = 'lib'

library_path = ''

def resolve_filename(filename):
    initial_filename = filename

    if '.' not in os.path.basename(filename):
        filename += ext

    if not os.path.basename(filename).startswith(pfx):
        filename = pfx + filename

    if os.path.exists(filename):
        return filename

    filename = os.path.join(library_path, filename)
    if os.path.exists(filename):
        return filename

    print('Warning: Library "%s" (%s) not found' % (initial_filename, filename))
    return filename


class CDLLResolvePath(ctypes.CDLL):
    def __init__(self, filename):
        super().__init__(resolve_filename(filename))

ctypes.CDLL = CDLLResolvePath
