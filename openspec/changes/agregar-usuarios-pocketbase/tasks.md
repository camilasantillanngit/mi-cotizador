# Tasks

## 1. PocketBase local

- [x] 1.1 Crear `pocketbase.sh` que descargue PocketBase v0.40.6 (darwin_arm64) en `pocketbase/`, verifique el checksum y lo ejecute con `serve`; agregar `pocketbase/` al `.gitignore`. Verificación: `./pocketbase.sh` deja el servidor en marcha y `curl http://127.0.0.1:8090/api/health` responde 200.
- [x] 1.2 Crear el superusuario en el panel `http://127.0.0.1:8090/_/` y confirmar que existe la colección `users` con registro abierto. Verificación: el panel muestra `users` y una petición de alta de prueba funciona.

## 2. Cliente y reglas de usuario

- [x] 2.1 Crear `pocketbase_cliente.py` (registro, inicio de sesión, error de base no disponible, cierre de sesión) con `urllib`. Verificación: tests `unittest` con un servidor HTTP simulado cubren registro correcto, correo repetido, credenciales incorrectas y base apagada; `python -m unittest discover -s tests` pasa.
- [x] 2.2 Agregar validaciones (correo, largo de contraseña, confirmación) en el módulo y que `Api.convertir` rechace llamadas sin sesión. Verificación: tests que cubren cada rechazo y la conversión sin sesión; pasan.

## 3. Interfaz

- [x] 3.1 Agregar a `app.py` las vistas de inicio de sesión y registro, el correo visible y el botón "Cerrar sesión" sobre el conversor, con mensajes de error. Verificación: al ejecutar `python app.py` con PocketBase en marcha se ve la pantalla de acceso y el conversor solo aparece tras iniciar sesión.
- [x] 3.2 Documentar en el README cómo levantar PocketBase, crear el superusuario y registrar usuarios de prueba. Verificación: seguir los pasos del README desde cero funciona.

## 4. Verificación final

- [ ] 4.1 Registrar dos usuarios, iniciar y cerrar sesión, convertir, y confirmar en el panel de PocketBase que aparecen las dos cuentas. Verificación: el panel lista los dos usuarios; con PocketBase apagado la app muestra el aviso sin cerrarse.
