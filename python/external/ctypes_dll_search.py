#
# Parley Who Vertigo
# Copyright 2016, 2017 Thomas Perl, Josef Who
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

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
