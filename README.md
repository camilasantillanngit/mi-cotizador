# Mi Cotizador

App de escritorio (macOS) para convertir un monto en pesos a dólares con la cotización que ingreses. Cada conversión se guarda con fecha y hora en `historial.txt`.

## Qué necesita
- Python 3.9 o superior y macOS (Apple Silicon probado).

## Ejecutar en desarrollo
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Tests
```bash
python -m unittest discover -s tests
```

## Crear el ejecutable
```bash
./build.sh
xattr -cr "dist/Mi Cotizador.app" && codesign --force --deep -s - "dist/Mi Cotizador.app"
```
Resultado: `dist/Mi Cotizador.app`. Si macOS lo bloquea: clic derecho > Abrir.

## Historial
`historial.txt` se crea junto al ejecutable (en `dist/` si abrís `dist/Mi Cotizador.app`). Formato:
```
2026-11-16 17:45:03 | ARS 100000.00 | cotización 1000.00 | USD 100.00
```
