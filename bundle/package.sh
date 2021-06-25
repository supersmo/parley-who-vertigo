#!/bin/bash
# Package Parley Who Vertigo

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SRC="$DIR/.."
OUT="$DIR/tmp"

DEST="$OUT/Parley Who Vertigo.app"

rm -rf "$OUT"
mkdir -p "$OUT" "$DEST/Contents/MacOS" "$DEST/Contents/Resources"

cp $SRC/README.md "$OUT"
cp $SRC/LICENSE "$OUT"
cp $SRC/docs/*.pdf "$OUT"

cp "$DIR/macos/Info.plist" "$DEST/Contents"
cp "$DIR/macos/parleywhovertigo.icns" "$DEST/Contents/Resources"

cp -rpv \
    "$SRC"/python/parley-who-vertigo \
    "$SRC"/python/*.py \
    "$SRC"/python/external \
    "$SRC"/python/minigames \
    "$SRC"/python/sounds \
    "$SRC"/python/art \
    "$DEST/Contents/MacOS"

cp -rpv \
    "$DIR"/macos/{bin,lib} \
    "$DEST/Contents/MacOS/external"

rm -rf "$DEST"/Contents/MacOS/external/{pocketchip,win32}
find "$DEST" -name __pycache__ -exec rm -rf {} +
ZIPNAME="parley-who-vertigo-$(date +%F)-macos.zip"
rm -f "$ZIPNAME"
(cd "$OUT" && zip -r ../"$ZIPNAME" *)

rm -rf "$OUT"

mkdir -p "$OUT"

cp $SRC/README.md "$OUT"
cp $SRC/LICENSE "$OUT"
cp $SRC/docs/*.pdf "$OUT"

cp -rpv \
    "$SRC"/python/parley-who-vertigo.bat \
    "$SRC"/python/*.py \
    "$SRC"/python/external \
    "$SRC"/python/minigames \
    "$SRC"/python/sounds \
    "$SRC"/python/art \
    "$OUT/"

rm -rf "$OUT"/external/{pocketchip,macos}
find "$DEST" -name __pycache__ -exec rm -rf {} +
ZIPNAME="parley-who-vertigo-$(date +%F)-win32.zip"
rm -f "$ZIPNAME"
(cd "$OUT" && zip -r ../"$ZIPNAME" *)

rm -rf "$OUT"

mkdir -p "$OUT"

cp $SRC/README.md "$OUT"
cp $SRC/LICENSE "$OUT"
cp $SRC/docs/*.pdf "$OUT"

cp -rpv \
    "$SRC"/python/parley-who-vertigo \
    "$SRC"/python/*.py \
    "$SRC"/python/external \
    "$SRC"/python/minigames \
    "$SRC"/python/sounds \
    "$SRC"/python/art \
    "$OUT/"

rm -rf "$OUT"/external/{win32,macos}
find "$DEST" -name __pycache__ -exec rm -rf {} +
ZIPNAME="parley-who-vertigo-$(date +%F)-pocketchip.zip"
rm -f "$ZIPNAME"
(cd "$OUT" && zip -r ../"$ZIPNAME" *)

rm -rf "$OUT"
