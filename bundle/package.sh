#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$DIR/.."
DEST="$DIR/Parley Who Vertigo.app"
rm -rf "$DEST"
mkdir -p "$DEST/Contents/MacOS" "$DEST/Contents/Resources"
cp "$SRC/../tools/psmovepair" "$DIR"
cp $SRC/../docs/*.pdf "$DIR"
cp "$DIR/Info.plist" "$DEST/Contents"
cp "$DIR/parleywhovertigo.icns" "$DEST/Contents/Resources"
cp -rpv "$SRC"/*.py "$SRC/parley-who-vertigo" "$SRC/external" "$SRC/minigames" "$SRC/sounds" "$SRC/art" "$DEST/Contents/MacOS"
find "$DEST" -name __pycache__ -exec rm -rf {} +
ZIPNAME="$(basename "$DEST" .app).zip"
rm -f "$ZIPNAME"
(cd "$(dirname "$DEST")" && zip -r "$ZIPNAME" "$(basename "$DEST")" *.pdf psmovepair)
