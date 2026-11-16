#!/bin/sh
# Genera dist/Mi Cotizador.app con PyInstaller.
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements-dev.txt
pyinstaller --noconfirm --clean --windowed --name "Mi Cotizador" app.py
echo "Listo: dist/Mi Cotizador.app"
