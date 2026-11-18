#!/bin/sh
# Descarga PocketBase (si falta), verifica el checksum y lo ejecuta.
set -e
cd "$(dirname "$0")"
VERSION="0.40.6"
ZIP="pocketbase_${VERSION}_darwin_arm64.zip"
BASE="https://github.com/pocketbase/pocketbase/releases/download/v${VERSION}"
if [ ! -x pocketbase/pocketbase ]; then
  mkdir -p pocketbase
  curl -fsSL -o "pocketbase/$ZIP" "$BASE/$ZIP"
  curl -fsSL -o pocketbase/checksums.txt "$BASE/checksums.txt"
  ( cd pocketbase && grep " $ZIP\$" checksums.txt | shasum -a 256 -c - )
  unzip -q -o "pocketbase/$ZIP" -d pocketbase
  rm -f "pocketbase/$ZIP"
  chmod +x pocketbase/pocketbase
fi
exec ./pocketbase/pocketbase serve --http=127.0.0.1:8090
