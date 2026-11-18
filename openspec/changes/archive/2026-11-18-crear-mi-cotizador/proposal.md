# Proposal

## Why

Se necesita una herramienta de escritorio simple para convertir un monto en pesos a dólares usando la cotización del día, y dejar un registro de cada conversión realizada. Hoy esto se hace a mano o con una calculadora, sin ningún registro.

## What Changes

- Nueva aplicación de escritorio en Python llamada **Mi Cotizador**.
- Ventana con un campo de monto en pesos, un campo de cotización del dólar y un botón **Convertir** que muestra el resultado en dólares.
- Cada conversión exitosa se guarda con fecha y hora en un archivo `historial.txt`.
- Empaquetado como ejecutable para el sistema operativo del usuario (macOS, Apple Silicon), sin requerir tener Python instalado para usarlo.

## Capabilities

### New Capabilities
- `conversion-pesos-dolares`: ingreso de monto y cotización, validación de los datos y cálculo/visualización del resultado en dólares.
- `historial-conversiones`: registro persistente de cada conversión, con fecha y hora, en `historial.txt`.

### Modified Capabilities

Ninguna (proyecto nuevo).

## Impact

- Código nuevo: aplicación Python (Tkinter) y script de empaquetado.
- Dependencias: PyInstaller (solo para construir el ejecutable). La app en sí usa solo la biblioteca estándar.
- Archivos generados: `dist/` con el ejecutable e `historial.txt` junto al ejecutable.
- Fuera de alcance: obtener la cotización automáticamente desde internet, otras monedas, ejecutables para Windows/Linux, interfaz para ver el historial dentro de la app.
