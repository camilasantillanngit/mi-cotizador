# Proposal

## Why

La cotización del dólar se escribe a mano cada vez: es lento y propenso a errores. El paso 5 del recorrido de la clase conecta Mi Cotizador a internet para traerla sola desde DolarAPI, un servicio público y gratuito.

## What Changes

- Al abrirse el conversor, la app trae sola la cotización del **dólar oficial (venta)** desde `https://dolarapi.com/v1/dolares/oficial` y completa el campo de cotización.
- Se muestra de dónde viene el valor y cuándo fue actualizado.
- Un botón **Actualizar cotización** vuelve a consultarla.
- El campo sigue siendo editable: se puede escribir otra cotización a mano.
- Si no hay internet o el servicio falla, la app lo avisa y se puede seguir ingresando la cotización a mano.
- La dirección del servicio es configurable desde el `.env` (`DOLARAPI_URL`).

## Capabilities

### New Capabilities
- `cotizacion-automatica`: obtención de la cotización del dólar oficial desde DolarAPI, con actualización manual y manejo de fallos.

### Modified Capabilities
- `conversion-pesos-dolares`: la ventana inicial del conversor ya no tiene la cotización vacía: se completa con la del día cuando está disponible.

## Impact

- Código: módulo de consulta a DolarAPI, ajustes en `servicio.py`, `app.py` y tests; nueva dependencia `certifi` para validar el certificado HTTPS en el ejecutable.
- Red: un pedido GET público a `dolarapi.com`. No se envía ningún dato del usuario ni de la app.
- Configuración: `DOLARAPI_URL` en `.env` y `.env.example`.
- Fuera de alcance: otros tipos de dólar, historial de cotizaciones, caché persistente, actualización automática periódica y la guardia de datos viejos.
