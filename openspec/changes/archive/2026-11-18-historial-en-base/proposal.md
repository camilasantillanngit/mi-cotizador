# Proposal

## Why

El historial en `historial.txt` no dice quién hizo cada consulta, vive en una carpeta junto al ejecutable y no se puede consultar ni compartir con permisos. Con usuarios y roles ya resueltos (v2 y v3), el historial puede guardarse en la base de datos, ligado a cada persona. Es el paso 4 del recorrido de la clase.

## What Changes

- Cada conversión exitosa se guarda en PocketBase, en una tabla `consultas` con **usuario, monto, cotización, resultado y fecha y hora** (la fecha la pone la base, automáticamente).
- **El TXT se jubila**: la app deja de escribir `historial.txt`.
- Nueva pestaña **Historial** para todos: cada usuario ve solo sus consultas; el admin ve las de todos, con el correo de quien consultó.
- La estructura de la tabla y sus reglas quedan en una migración versionada en `pb_migrations/`.
- Si la base no responde al guardar, la app igual muestra el resultado y avisa que no se pudo guardar el historial.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities
- `historial-conversiones`: el registro pasa de un archivo de texto a la base de datos, ligado al usuario; se agregan la consulta del propio historial y la vista del admin sobre el de todos.

## Impact

- Base de datos: migración nueva con la colección `consultas` y sus reglas.
- Código: `cotizador.py` deja de manejar archivos; `pocketbase_cliente.py`, `servicio.py` y `app.py` guardan y listan consultas; tests actualizados.
- El `historial.txt` existente no se borra ni se importa: queda como archivo viejo, sin usarse.
- Fuera de alcance: importar el TXT anterior, filtros, paginación avanzada y exportar, editar o borrar consultas, `.env` (paso posterior) y cotización automática (v5).
