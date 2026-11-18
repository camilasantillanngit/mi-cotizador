"""Cliente mínimo de PocketBase (solo biblioteca estándar) para usuarios."""
import json
import os
import re
import urllib.error
import urllib.request

URL_POR_DEFECTO = "http://127.0.0.1:8090"
CORREO_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ErrorAcceso(Exception):
    """Error mostrable al usuario (mensaje en español)."""


class BaseNoDisponible(ErrorAcceso):
    pass


def url_base():
    return os.environ.get("POCKETBASE_URL", URL_POR_DEFECTO).rstrip("/")


def validar_registro(correo, clave, confirmacion):
    if not CORREO_RE.match((correo or "").strip()):
        raise ErrorAcceso("Ingresá un correo válido.")
    if len(clave or "") < 8:
        raise ErrorAcceso("La contraseña debe tener al menos 8 caracteres.")
    if clave != confirmacion:
        raise ErrorAcceso("Las contraseñas no coinciden.")


def _post(ruta, datos, base=None):
    pedido = urllib.request.Request(
        (base or url_base()) + ruta,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(pedido, timeout=5) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            cuerpo = json.loads(error.read().decode("utf-8"))
        except ValueError:
            cuerpo = {}
        raise _traducir(error.code, cuerpo) from None
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        raise BaseNoDisponible(
            "La base de datos no está disponible. Levantala con ./pocketbase.sh"
        ) from None


def _traducir(codigo, cuerpo):
    campos = cuerpo.get("data") or {}
    if campos.get("email", {}).get("code") == "validation_not_unique":
        return ErrorAcceso("Ese correo ya está registrado.")
    if campos:
        return ErrorAcceso("No se pudo crear la cuenta: revisá los datos ingresados.")
    return ErrorAcceso("Correo o contraseña incorrectos.")


def registrar(correo, clave, confirmacion, base=None):
    """Crea la cuenta e inicia sesión. Devuelve (token, correo)."""
    validar_registro(correo, clave, confirmacion)
    correo = correo.strip()
    _post("/api/collections/users/records",
          {"email": correo, "password": clave, "passwordConfirm": confirmacion}, base)
    return iniciar_sesion(correo, clave, base)


def iniciar_sesion(correo, clave, base=None):
    """Devuelve (token, correo)."""
    if not (correo or "").strip() or not clave:
        raise ErrorAcceso("Ingresá tu correo y contraseña.")
    datos = _post("/api/collections/users/auth-with-password",
                  {"identity": correo.strip(), "password": clave}, base)
    return datos["token"], datos["record"]["email"]
