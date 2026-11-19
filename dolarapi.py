"""Cotización del dólar oficial desde DolarAPI (consulta pública, sin datos del usuario)."""
import json
import ssl
import urllib.error
import urllib.request
from decimal import Decimal

import certifi

import config

URL_POR_DEFECTO = "https://dolarapi.com/v1/dolares/oficial"
MENSAJE_FALLO = "No se pudo obtener la cotización. Ingresala a mano."


class CotizacionNoDisponible(Exception):
    """El servicio no respondió o devolvió datos inválidos."""


def url_servicio():
    return config.obtener("DOLARAPI_URL", URL_POR_DEFECTO)


def obtener_venta(url=None):
    """Devuelve {"venta": Decimal, "fecha": str|None}. Lanza CotizacionNoDisponible."""
    url = url or url_servicio()
    # Pedido público: sin sesión, sin token y sin datos de la persona.
    pedido = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "MiCotizador"}, method="GET")
    contexto = ssl.create_default_context(cafile=certifi.where()) if url.lower().startswith("https") else None
    try:
        with urllib.request.urlopen(pedido, timeout=5, context=contexto) as respuesta:
            datos = json.loads(respuesta.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, ValueError):
        raise CotizacionNoDisponible(MENSAJE_FALLO) from None

    venta = datos.get("venta") if isinstance(datos, dict) else None
    if isinstance(venta, bool) or not isinstance(venta, (int, float)):
        raise CotizacionNoDisponible(MENSAJE_FALLO)
    valor = Decimal(str(venta))
    if not valor.is_finite() or valor <= 0:
        raise CotizacionNoDisponible(MENSAJE_FALLO)
    fecha = datos.get("fechaActualizacion")
    return {"venta": valor, "fecha": fecha if isinstance(fecha, str) else None}
