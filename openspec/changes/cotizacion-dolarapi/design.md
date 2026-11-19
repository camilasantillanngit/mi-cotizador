# Design

## Context

El conversor valida y calcula con `cotizador.py`; `servicio.py` expone los métodos a la ventana y `app.py` define la interfaz. La configuración se lee con `config.py` (cambio previo `ordenar-configuracion`). DolarAPI responde un JSON con `compra`, `venta` y `fechaActualizacion` (verificado). Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Traer y mostrar la cotización sin bloquear la app si falla.
- Funcionar también dentro del ejecutable empaquetado.

**Non-Goals:**
- Otros tipos de dólar, caché persistente, actualización periódica.

## Decisions

- **Se usa `venta` del dólar oficial**: es el valor al que se compran dólares con pesos, que es lo que se convierte en este cotizador. `compra` queda fuera (es lo que paga el banco por dólares).
- **Consulta desde Python con `urllib`** (módulo `dolarapi.py`), no desde el JavaScript de la ventana: mismo criterio que con PocketBase, sin problemas de CORS y con timeout de 5 s.
- **Validación estricta de la respuesta**: `venta` debe ser un número finito mayor que cero; si no, se trata como fallo. La fecha de `fechaActualizacion` se convierte a hora local en la interfaz.
- **Certificados HTTPS con `certifi`**: el Python empaquetado no siempre encuentra los certificados del sistema en macOS; se usa el paquete de certificados de `certifi` explícitamente. Alternativa: desactivar la verificación (descartada: inseguro).
- **No se pisa lo escrito a mano**: se completa el campo al mostrar el conversor solo si está vacío; el botón "Actualizar cotización" siempre lo reemplaza.
- **`DOLARAPI_URL` configurable por `.env`** con valor por defecto `https://dolarapi.com/v1/dolares/oficial`; permite probar con un servidor local y apagar la salida a internet en pruebas.
- **Bandera de diagnóstico `--probar-cotizacion`** en `app.py`: imprime el resultado de la consulta y termina, para verificar el ejecutable sin abrir la ventana.
- **Privacidad**: el pedido es un GET sin datos de la persona (ver spec).

## Risks / Trade-offs

- [DolarAPI deja de estar disponible o cambia el formato] → Fallo controlado: aviso y entrada manual; la validación de la respuesta evita valores absurdos.
- [El ejecutable no valida el certificado HTTPS] → `certifi` y verificación del `.app` con `--probar-cotizacion`.
- [Cotización vieja por un valor desactualizado en el servicio] → Se muestra la fecha de actualización para que la persona la juzgue.
- [Una dependencia más] → `certifi` es de uso muy extendido y ya viaja con muchas herramientas de Python.
