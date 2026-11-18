# Mi Cotizador

App de escritorio (macOS) para convertir un monto en pesos a dólares con la cotización que ingreses. Hay que registrarse e iniciar sesión (usuarios en PocketBase). Cada conversión se guarda con fecha y hora en `historial.txt`.

## Qué necesita
- Python 3.9 o superior y macOS (Apple Silicon probado).

## PocketBase (base de datos de usuarios)
La app necesita PocketBase en marcha. En una terminal aparte:
```bash
./pocketbase.sh
```
La primera vez descarga PocketBase v0.40.6 (verifica el checksum) y queda en `pocketbase/` (no se sube a Git). Después:
1. Abrí `http://127.0.0.1:8090/_/` y creá el usuario administrador de la base (correo y contraseña a tu elección).
2. Los usuarios de la app se registran desde la propia app (pantalla "Registrate"). Para probar, registrá dos y verlos en el panel: colección `users`.

Si PocketBase está en otra dirección, definí `POCKETBASE_URL`.

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
```
Resultado: `~/Applications/Mi Cotizador.app` (firmado de forma local). Si macOS lo bloquea: clic derecho > Abrir.

## Historial
`historial.txt` se crea junto al ejecutable (en `~/Applications/` si abrís `~/Applications/Mi Cotizador.app`). Formato:
```
2026-11-16 17:45:03 | ARS 100000.00 | cotización 1000.00 | USD 100.00
```
