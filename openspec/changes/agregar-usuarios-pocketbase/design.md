# Design

## Context

La v1 es una ventana pywebview (HTML/JS) cuya API en Python (`Api.convertir`) usa `cotizador.py`. No hay usuarios ni base de datos. PocketBase trae una colección de usuarios (`users`) con autenticación por correo y contraseña lista para usar. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Registro, inicio y cierre de sesión contra PocketBase, sin dependencias nuevas en Python.
- Levantar PocketBase con un solo comando y una carpeta ignorada por Git.

**Non-Goals:**
- Roles, panel de admin, historial en la base, `.env`, recuperación de contraseña, verificación de correo.

## Decisions

- **PocketBase v0.40.6 en `pocketbase/`**: descarga del zip oficial `darwin_arm64`, verificado contra `checksums.txt` de la misma release. El programa y `pb_data/` quedan en `.gitignore` (datos reales de cada uno y binario dependiente del sistema).
- **Cliente en Python con `urllib` (`pocketbase_cliente.py`)** llamando a la API REST (`/api/collections/users/records` y `/auth-with-password`). Se hace desde Python y no desde el JS de la ventana: evita CORS y mantiene la contraseña fuera del navegador embebido. Alternativa: SDK de PocketBase (no hay oficial para Python; sumaría dependencia).
- **Sesión en memoria**: el token de autenticación vive en la clase `Api` mientras la app está abierta y se descarta al cerrar sesión o cerrar la app. No se guarda en disco (menos superficie de ataque; en la v2 no se pide "recordarme").
- **Validación en dos lugares**: formato de correo, largo de contraseña (8+) y coincidencia se validan en `cotizador`/cliente antes de llamar; PocketBase valida unicidad y devuelve el error de correo repetido.
- **Interfaz**: la misma ventana alterna tres vistas (inicio, registro, conversor) en HTML; la API de Python decide si una conversión está permitida (rechaza si no hay sesión), de modo que ocultar la vista no es la única barrera.
- **Dirección de PocketBase**: `http://127.0.0.1:8090`, configurable con la variable de entorno `POCKETBASE_URL` (el `.env` completo llega en un paso posterior).
- **Primer uso**: PocketBase pide crear el superusuario en su panel (`/_/`); la colección `users` ya existe con registro abierto, así que no hace falta crear colecciones a mano. Se verifica al implementar.
- **Script `pocketbase.sh`**: descarga si falta, verifica checksum y ejecuta `./pocketbase/pocketbase serve`.

## Risks / Trade-offs

- [El registro abierto permite crear cuentas a cualquiera con acceso a la base local] → Aceptable en una base local de prueba; los permisos finos llegan con la v3.
- [La descarga de un binario externo] → Fuente oficial, versión fija y checksum verificado; el binario no se sube a Git.
- [Si PocketBase cambia el formato de errores en otra versión] → Versión fija; los tests con un servidor simulado fijan el contrato usado.
- [El `.app` empaquetado necesita PocketBase corriendo aparte] → Se documenta en el README; embebido queda fuera de alcance.
- [Sesión solo en memoria: hay que iniciar sesión cada vez] → Decisión consciente por seguridad y simplicidad.
