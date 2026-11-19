#!/bin/sh
# Genera "Mi Cotizador.app" con PyInstaller y lo deja firmado en ~/Applications.
# (Se copia fuera de Escritorio/Documentos: iCloud agrega metadatos que impiden abrirlo.)
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements-dev.txt
pyinstaller --noconfirm --clean --windowed --name "Mi Cotizador" app.py
DEST="$HOME/Applications/Mi Cotizador.app"
mkdir -p "$HOME/Applications"
rm -rf "$DEST"
ditto --noextattr --norsrc --noqtn "dist/Mi Cotizador.app" "$DEST"
xattr -cr "$DEST"
codesign --force --deep -s - "$DEST"
echo "Listo: $DEST"
