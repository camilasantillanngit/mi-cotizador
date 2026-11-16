"""Lógica de Mi Cotizador: conversión de pesos a dólares e historial en TXT."""
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

CENTAVOS = Decimal("0.01")


class DatoInvalido(ValueError):
    """El monto o la cotización ingresados no son válidos."""


def parsear_numero(texto, nombre):
    """Convierte texto (con coma o punto decimal) en Decimal > 0."""
    limpio = (texto or "").strip().replace(",", ".")
    if not limpio:
        raise DatoInvalido(f"Ingresá {nombre}.")
    try:
        valor = Decimal(limpio)
    except InvalidOperation:
        raise DatoInvalido(f"{nombre.capitalize()} no es válido: usá solo números.") from None
    if not valor.is_finite() or valor <= 0:
        raise DatoInvalido(f"{nombre.capitalize()} debe ser mayor que cero.")
    return valor


def convertir(monto, cotizacion):
    """Pesos / cotización, redondeado a 2 decimales."""
    return (monto / cotizacion).quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def formatear_usd(valor):
    """100.00 -> 'USD 100,00' (formato argentino, con miles)."""
    texto = f"{valor:,.2f}"
    return "USD " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def linea_historial(monto, cotizacion, resultado, ahora=None):
    ahora = ahora or datetime.now()
    return (
        f"{ahora:%Y-%m-%d %H:%M:%S} | ARS {monto.quantize(CENTAVOS)} | "
        f"cotización {cotizacion.quantize(CENTAVOS)} | USD {resultado}"
    )


def carpeta_base():
    """Carpeta donde vive el ejecutable (o el script, en desarrollo)."""
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        for padre in exe.parents:  # dentro de un .app: usar la carpeta que lo contiene
            if padre.suffix == ".app":
                return padre.parent
        return exe.parent
    return Path(__file__).resolve().parent


def ruta_historial():
    return carpeta_base() / "historial.txt"


def guardar_en_historial(linea, ruta=None):
    """Agrega una línea al historial. Lanza OSError si no se puede escribir."""
    ruta = Path(ruta) if ruta else ruta_historial()
    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")


def procesar(texto_monto, texto_cotizacion, ruta=None, ahora=None):
    """Valida, convierte y guarda. Devuelve un dict listo para la interfaz."""
    try:
        monto = parsear_numero(texto_monto, "el monto")
        cotizacion = parsear_numero(texto_cotizacion, "la cotización")
    except DatoInvalido as error:
        return {"ok": False, "error": str(error)}

    resultado = convertir(monto, cotizacion)
    respuesta = {"ok": True, "resultado": formatear_usd(resultado), "aviso": None}
    try:
        guardar_en_historial(linea_historial(monto, cotizacion, resultado, ahora), ruta)
    except OSError:
        respuesta["aviso"] = "No se pudo guardar el historial (sin permiso de escritura)."
    return respuesta
