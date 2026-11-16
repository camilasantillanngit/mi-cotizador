# Design

## Context

Proyecto nuevo y vacío. Equipo del usuario: macOS (Apple Silicon, arm64) con Python 3.9.6 del sistema, cuyo Tk 8.5 se cierra al abrir una ventana ("macOS 26 or later required"; verificado). Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- App mínima, un solo archivo fuente, sin dependencias en tiempo de ejecución.
- Lógica de conversión y de historial separadas de la interfaz para poder probarlas sin abrir ventanas.
- Ejecutable que se abra con doble clic en macOS.

**Non-Goals:**
- Cotización automática desde internet, otras monedas, ver el historial dentro de la app.
- Firma/notarización de Apple y ejecutables para otros sistemas operativos.

## Decisions

- **pywebview** para la interfaz: ventana nativa de macOS (WKWebView) con HTML/JS simple y una API en Python. No depende de Tk, que en este Mac falla. Alternativas: Tkinter (descartado: se cierra en este macOS con el Python del sistema), PyQt (pesado, licencia).
- **Decimal en lugar de float** para el cálculo: evita errores de redondeo con dinero. Se redondea a 2 decimales con `ROUND_HALF_UP`.
- **Entrada tolerante**: se acepta coma o punto decimal; se descarta cualquier otro formato (sin separadores de miles) para evitar ambigüedad.
- **Estructura**: `cotizador.py` (lógica pura: parsear, convertir, formatear línea de historial, escribir), `app.py` (ventana pywebview), `tests/` con `unittest`.
- **Ubicación del historial**: carpeta del ejecutable (`sys.executable` cuando está empaquetado, carpeta del script en desarrollo). Para un `.app` se usa la carpeta que contiene el `.app`, no su interior. Formato de línea con separador ` | ` y codificación UTF-8, modo append.
- **PyInstaller** (`--windowed --name "Mi Cotizador"`) para generar el ejecutable. Alternativa: py2app (menos mantenido, más configuración).

## Risks / Trade-offs

- [pywebview agrega una dependencia (pyobjc) al empaquetar] → Se instala en `.venv` y PyInstaller la incluye en el `.app`.
- [El ejecutable no está firmado: macOS Gatekeeper puede bloquearlo al moverlo] → Documentar abrirlo con clic derecho > Abrir; no se firma en este alcance.
- [El ejecutable solo corre en el mismo tipo de Mac (arm64)] → Aceptado; el usuario pidió uno para su sistema.
- [Historial junto al ejecutable puede estar en carpeta sin permisos] → Se avisa en pantalla y no se pierde el resultado (ver spec).
