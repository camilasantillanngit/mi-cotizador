# Design

## Context

PocketBase v0.40.6 con la colección `users` (auth) creada por defecto. La app llama a su API REST desde Python (`pocketbase_cliente.py`) y guarda la sesión en memoria (`servicio.py`). Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- La seguridad vive en las reglas de PocketBase; la interfaz solo oculta lo que no corresponde.
- La estructura de la base se reproduce desde el repositorio.

**Non-Goals:**
- Crear o borrar cuentas desde el panel, cambiar roles desde la app, auditoría de acciones.

## Decisions

- **Campos nuevos en `users`**: `rol` (select: `usuario`, `admin`) y `desactivado` (bool). Se usa `desactivado` y no `activo` porque un booleano nuevo vale `false` por defecto: las cuentas existentes seguirían activas sin tocar datos. Alternativa descartada: `activo` (dejaría a todos bloqueados tras migrar).
- **Migración en `pb_migrations/` (JavaScript, versionada en Git)** y `pocketbase.sh` arranca con `--migrationsDir=./pb_migrations`. Alternativa: configurar a mano en el panel (no reproducible, contra lo que pide la clase: "la estructura de la base" se sube).
- **Reglas (en la migración)**:
  - `createRule`: el registro no puede traer `rol` ni `desactivado`.
  - `authRule`: `desactivado = false` — bloquea el login de cuentas desactivadas.
  - `listRule` / `viewRule`: `id = @request.auth.id || (@request.auth.rol = "admin" && @request.auth.desactivado = false)`.
  - `updateRule`: admin activo, o la propia cuenta sin tocar `rol` ni `desactivado`.
  - `manageRule`: admin activo (permite cambiar la contraseña de otros sin la anterior).
  - `deleteRule`: nadie desde la API (el borrado se hace desde el panel de PocketBase).
- **Tokens ya emitidos**: al desactivar una cuenta, su token sigue siendo válido hasta vencer; las reglas de lista/edición exigen `@request.auth.desactivado = false` para que no pueda seguir operando como admin. La app no usa el token para nada más sensible que eso en la v3.
- **Cliente**: `listar_cuentas`, `desactivar`, `reactivar`, `resetear_clave` con el token en el encabezado `Authorization`. `iniciar_sesion` devuelve también el rol. El servicio rechaza estas acciones si el rol no es `admin` (la regla de PocketBase es la barrera real).
- **Interfaz**: el conversor y el panel conviven en la misma ventana con dos pestañas visibles solo para el admin.
- **Primer admin**: se marca a mano en el panel de PocketBase (`users` → campo `rol` = `admin`), como en la clase.

## Risks / Trade-offs

- [Reglas mal escritas pueden dejar abierta la gestión de cuentas] → Verificación obligatoria contra la base real con dos cuentas (usuario y admin) y pedidos directos a la API, no solo por la interfaz.
- [Un admin podría desactivarse a sí mismo y quedar sin acceso] → La app lo impide; si pasara, se reactiva desde el panel de PocketBase.
- [El token de una cuenta desactivada sigue vivo un tiempo] → Las reglas impiden que opere como admin y la desactivación bloquea nuevos inicios de sesión.
- [La API de migraciones JS puede variar entre versiones de PocketBase] → Versión fija (0.40.6); se comprueba al aplicar.
