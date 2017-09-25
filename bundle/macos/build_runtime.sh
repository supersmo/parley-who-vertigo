#!/bin/sh
# Build (a subset of) Python 3.5 locally
# 2016-12-22 Thomas Perl <m@thp.io>

set -x
set -e

wget -c https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz

tar xvf Python-3.5.2.tar.xz
cd Python-3.5.2
./configure
make install DESTDIR=$(pwd)/tmp/
find tmp -name __pycache__ -exec rm -rf {} +
rm -rf \
    tmp/usr/local/bin/{python3,python3.5m,2to3*,idle3*,pydoc3*,python3*-config,pyvenv*} \
    tmp/usr/local/include \
    tmp/usr/local/lib/{pkgconfig,libpython3.5m.a} \
    tmp/usr/local/lib/python3.5/{unittest,turtledemo,test,config-3.5m,distutils,ensurepip} \
    tmp/usr/local/lib/python3.5/{idlelib,lib2to3,tkinter,email,pydoc_data,ctypes/test,sqlite3/test} \
    tmp/usr/local/share
cd ..

mv Python-3.5.2/tmp/usr/local/* .
rm -rf Python-3.5.2.tar.xz Python-3.5.2/
