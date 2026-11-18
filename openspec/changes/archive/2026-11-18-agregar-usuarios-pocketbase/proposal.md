# Proposal

## Why

Hoy cualquiera que abre Mi Cotizador puede usarlo y no se sabe quién hizo cada conversión. La versión 2 del recorrido de la clase agrega cuentas de usuario para tener control de acceso y dejar la base para saber quién consulta (v3 roles, v4 historial por usuario).

## What Changes

- Se incorpora PocketBase como base de datos local (un solo ejecutable, con panel de administración y API) en una carpeta `pocketbase/` del proyecto.
- La app muestra primero una pantalla de **inicio de sesión** y otra de **registro** (correo y contraseña), usando los usuarios de PocketBase.
- Solo después de iniciar sesión se muestra el conversor; hay un botón para **cerrar sesión**.
- Si PocketBase no está en marcha, la app lo informa con un mensaje claro en lugar de fallar.
- El historial sigue siendo `historial.txt` (pasa a la base en la v4). No hay roles todavía (v3).

## Capabilities

### New Capabilities
- `inicio-sesion-usuarios`: registro, inicio y cierre de sesión con cuentas de PocketBase, y acceso al conversor solo con sesión iniciada.

### Modified Capabilities

Ninguna: la conversión y el historial no cambian de comportamiento.

## Impact

- Código nuevo: cliente de PocketBase en Python (solo biblioteca estándar), pantallas de acceso en la interfaz y tests.
- Archivos nuevos: carpeta `pocketbase/` (el programa y los datos locales no se suben a Git), script para levantarlo, `.gitignore` actualizado y README ampliado.
- Descarga externa: el programa PocketBase v0.40.6 (macOS arm64, ~12 MB) desde su repositorio oficial de GitHub.
- Fuera de alcance: roles y panel de admin (v3), historial en la base (v4), `.env` (paso de orden posterior), cotización automática (v5), recuperar contraseña por correo.
