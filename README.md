# Mi Cotizador

App de escritorio (macOS) para convertir un monto en pesos a dólares con la cotización que ingreses. Hay que registrarse e iniciar sesión (usuarios en PocketBase). Cada conversión se guarda en PocketBase (tabla `consultas`) con usuario, monto, cotización, resultado y fecha y hora.

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

### Roles y administrador (v3)
La estructura de la base (campos `rol` y `desactivado` y las reglas de acceso) está en `pb_migrations/` y se aplica sola al iniciar `./pocketbase.sh`: no hay que configurar nada a mano.

- Las cuentas nuevas son `usuario`. **El primer admin se marca a mano**: en el panel de PocketBase, colección `users`, abrí la cuenta y poné el campo `rol` en `admin`.
- Un admin ve en la app la pestaña **Cuentas**: lista, desactivar/reactivar y asignar contraseña nueva. No puede desactivarse a sí mismo.
- Una cuenta desactivada no puede iniciar sesión. Un usuario común no ve otras cuentas ni puede darse rol admin (lo impide PocketBase, no solo la pantalla).

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
Cada conversión exitosa se guarda en la base (colección `consultas`): usuario, monto, cotización, resultado y fecha y hora (la pone el servidor). La app ya no escribe `historial.txt`.

- Pestaña **Historial**: un usuario común ve solo sus consultas (las 50 más recientes); el admin ve las de todos, con el correo de quien consultó.
- Las consultas no se pueden editar ni borrar por la API; cada persona solo crea consultas a su nombre. Las reglas están en `pb_migrations/` y se aplican solas.
- Si la base no responde al guardar, la app muestra igual el resultado y avisa que no se guardó.
- Un `historial.txt` de versiones anteriores, si existe, no se usa ni se importa.
