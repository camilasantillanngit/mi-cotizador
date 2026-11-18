# Tasks

## 1. Estructura y reglas de la base

- [x] 1.1 Crear `pb_migrations/` con la migración que agrega `rol` y `desactivado` a `users` y define las reglas de la decisión de diseño; ajustar `pocketbase.sh` para usar `--migrationsDir=./pb_migrations`. Verificación: al reiniciar PocketBase la migración se aplica y el panel muestra los campos y reglas.
- [x] 1.2 Verificar las reglas con pedidos directos a la API usando una cuenta usuario y una admin de prueba: el usuario no lista otras cuentas, no se da rol admin y no puede registrarse como admin; el admin sí lista, desactiva y resetea. Verificación: tabla de resultados esperados vs. obtenidos, todos coinciden.

## 2. Cliente y servicio

- [x] 2.1 Ampliar `pocketbase_cliente.py` con rol en el inicio de sesión, `listar_cuentas`, `desactivar`/`reactivar` y `resetear_clave`, con validación de contraseña (8+). Verificación: tests con servidor simulado cubren cada operación y errores; `python -m unittest discover -s tests` pasa.
- [x] 2.2 Ampliar `servicio.py`: guardar el rol, rechazar acciones de admin a usuarios comunes y bloquear que el admin se desactive a sí mismo. Verificación: tests de cada rechazo pasan.

## 3. Interfaz

- [x] 3.1 Agregar la pestaña "Cuentas" (solo admin) con lista, botones desactivar/reactivar y formulario de nueva contraseña, con mensajes de error. Verificación: pruebas en pantalla con un admin muestran la lista y las acciones; con un usuario común no aparece la pestaña.
- [x] 3.2 Actualizar el README (marcar el primer admin, migraciones). Verificación: seguir el README en una base nueva (carpeta `pb_data` vacía) deja roles y reglas funcionando.

## 4. Verificación final

- [x] 4.1 Con dos usuarios y un admin: el admin desactiva a un usuario y ese usuario ya no puede entrar; el admin resetea una clave y el usuario entra con la nueva. Verificación: cada paso observado en la app y confirmado en el panel de PocketBase.
