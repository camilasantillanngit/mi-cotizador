"""Lógica de Mi Cotizador: validación y conversión de pesos a dólares."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

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


def calcular(texto_monto, texto_cotizacion):
    """Valida y convierte. No guarda nada.

    Devuelve {"ok": True, "monto", "cotizacion", "resultado"} (Decimal, 2 decimales)
    o {"ok": False, "error": mensaje}.
    """
    try:
        monto = parsear_numero(texto_monto, "el monto")
        cotizacion = parsear_numero(texto_cotizacion, "la cotización")
    except DatoInvalido as error:
        return {"ok": False, "error": str(error)}
    return {
        "ok": True,
        "monto": monto.quantize(CENTAVOS, rounding=ROUND_HALF_UP),
        "cotizacion": cotizacion.quantize(CENTAVOS, rounding=ROUND_HALF_UP),
        "resultado": convertir(monto, cotizacion),
    }
