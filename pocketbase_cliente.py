"""Cliente mínimo de PocketBase (solo biblioteca estándar) para usuarios."""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import namedtuple

URL_POR_DEFECTO = "http://127.0.0.1:8090"
CORREO_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

Sesion = namedtuple("Sesion", "token correo rol id")
Cuenta = namedtuple("Cuenta", "id correo rol desactivado")


class ErrorAcceso(Exception):
    """Error mostrable al usuario (mensaje en español)."""


class BaseNoDisponible(ErrorAcceso):
    pass


class _ErrorHTTP(Exception):
    def __init__(self, codigo, cuerpo):
        self.codigo, self.cuerpo = codigo, cuerpo


def url_base():
    return os.environ.get("POCKETBASE_URL", URL_POR_DEFECTO).rstrip("/")


def validar_clave(clave):
    if len(clave or "") < 8:
        raise ErrorAcceso("La contraseña debe tener al menos 8 caracteres.")


def validar_registro(correo, clave, confirmacion):
    if not CORREO_RE.match((correo or "").strip()):
        raise ErrorAcceso("Ingresá un correo válido.")
    validar_clave(clave)
    if clave != confirmacion:
        raise ErrorAcceso("Las contraseñas no coinciden.")


def _llamar(metodo, ruta, datos=None, token=None, base=None):
    cabeceras = {"Content-Type": "application/json"}
    if token:
        cabeceras["Authorization"] = token
    pedido = urllib.request.Request(
        (base or url_base()) + ruta,
        data=None if datos is None else json.dumps(datos).encode("utf-8"),
        headers=cabeceras,
        method=metodo,
    )
    try:
        with urllib.request.urlopen(pedido, timeout=5) as respuesta:
            return json.loads(respuesta.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as error:
        try:
            cuerpo = json.loads(error.read().decode("utf-8"))
        except ValueError:
            cuerpo = {}
        raise _ErrorHTTP(error.code, cuerpo) from None
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        raise BaseNoDisponible(
            "La base de datos no está disponible. Levantala con ./pocketbase.sh"
        ) from None


def registrar(correo, clave, confirmacion, base=None):
    """Crea la cuenta e inicia sesión. Devuelve una Sesion."""
    validar_registro(correo, clave, confirmacion)
    correo = correo.strip()
    try:
        _llamar("POST", "/api/collections/users/records",
                {"email": correo, "password": clave, "passwordConfirm": confirmacion}, base=base)
    except _ErrorHTTP as error:
        campos = error.cuerpo.get("data") or {}
        if campos.get("email", {}).get("code") == "validation_not_unique":
            raise ErrorAcceso("Ese correo ya está registrado.") from None
        raise ErrorAcceso("No se pudo crear la cuenta: revisá los datos ingresados.") from None
    return iniciar_sesion(correo, clave, base)


def iniciar_sesion(correo, clave, base=None):
    """Devuelve una Sesion. Cuenta desactivada = credenciales incorrectas."""
    if not (correo or "").strip() or not clave:
        raise ErrorAcceso("Ingresá tu correo y contraseña.")
    try:
        datos = _llamar("POST", "/api/collections/users/auth-with-password",
                        {"identity": correo.strip(), "password": clave}, base=base)
    except _ErrorHTTP:
        raise ErrorAcceso("Correo o contraseña incorrectos.") from None
    registro = datos["record"]
    return Sesion(datos["token"], registro["email"], registro.get("rol") or "usuario", registro["id"])


def _administrar(metodo, ruta, token, datos=None, base=None):
    try:
        return _llamar(metodo, ruta, datos, token, base)
    except _ErrorHTTP as error:
        if error.codigo in (401, 403, 404):
            raise ErrorAcceso("No tenés permiso para hacer esto.") from None
        raise ErrorAcceso("No se pudo completar la operación.") from None


def listar_cuentas(token, base=None):
    datos = _administrar(
        "GET", "/api/collections/users/records?" + urllib.parse.urlencode({"perPage": 200, "sort": "email"}),
        token, base=base)
    return [
        Cuenta(i["id"], i["email"], i.get("rol") or "usuario", bool(i.get("desactivado")))
        for i in datos.get("items", [])
    ]


def cambiar_desactivado(token, id_cuenta, desactivado, base=None):
    _administrar("PATCH", f"/api/collections/users/records/{urllib.parse.quote(id_cuenta)}",
                 token, {"desactivado": bool(desactivado)}, base)


def resetear_clave(token, id_cuenta, clave, base=None):
    validar_clave(clave)
    _administrar("PATCH", f"/api/collections/users/records/{urllib.parse.quote(id_cuenta)}",
                 token, {"password": clave, "passwordConfirm": clave}, base)
