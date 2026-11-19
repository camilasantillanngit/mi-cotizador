"""Configuración de Mi Cotizador: variables de entorno y archivo .env.

Prioridad: variable del sistema > archivo .env > valor por defecto.
Nunca se imprimen ni se registran los valores (pueden ser secretos).
"""
import os
import sys
from pathlib import Path


def carpeta_base():
    """Carpeta del proyecto, o la que contiene el .app cuando está empaquetado."""
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        for padre in exe.parents:
            if padre.suffix == ".app":
                return padre.parent
        return exe.parent
    return Path(__file__).resolve().parent


def leer_env(ruta=None):
    """Lee un archivo .env y devuelve un dict. Ignora comentarios y líneas mal formadas."""
    ruta = Path(ruta) if ruta else carpeta_base() / ".env"
    valores = {}
    try:
        lineas = ruta.read_text(encoding="utf-8").splitlines()
    except OSError:
        return valores
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        clave = clave.strip()
        if clave.startswith("export "):
            clave = clave[7:].strip()
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        if clave:
            valores[clave] = valor
    return valores


def obtener(nombre, por_defecto=None, ruta_env=None):
    """Valor de una variable: entorno del sistema, luego .env, luego por defecto."""
    if nombre in os.environ:
        return os.environ[nombre]
    return leer_env(ruta_env).get(nombre, por_defecto)
