#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$DIR/.."
DEST="$DIR/Parley Who Vertigo.app"
mkdir -p "$DEST/Contents/MacOS"
cp "$DIR/Info.plist" "$DEST/Contents"
cp -rpv "$SRC"/*.py "$SRC/parley-who-vertigo" "$SRC/external" "$SRC/minigames" "$SRC/sounds" "$DEST/Contents/MacOS"
find "$DEST" -name __pycache__ -exec rm -rf {} +
ZIPNAME="$(basename "$DEST" .app).zip"
rm -f "$ZIPNAME"
(cd "$(dirname "$DEST")" && zip -r "$ZIPNAME" "$(basename "$DEST")")
