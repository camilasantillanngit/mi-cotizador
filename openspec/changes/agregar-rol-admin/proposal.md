# Proposal

## Why

Con la v2 todas las cuentas son iguales. Hace falta una persona de confianza que pueda ver las cuentas, bloquear a quien corresponda y ayudar a quien olvidó su contraseña, sin que un usuario común pueda hacer lo mismo. Es el paso 3 del recorrido de la clase.

## What Changes

- Las cuentas suman un **rol**: `usuario` (por defecto) o `admin`, y un indicador de **cuenta desactivada**.
- Si entra un admin, la app muestra un panel extra de **Cuentas**: lista de usuarios, desactivar/reactivar y asignar una contraseña nueva.
- Una cuenta desactivada no puede iniciar sesión.
- La seguridad la aplica PocketBase con **reglas**: solo un admin puede listar otras cuentas, cambiar roles, desactivar o resetear contraseñas; un usuario común solo ve y edita su propia cuenta y no puede darse el rol admin.
- La estructura de la base (campo `rol`, campo de desactivación y reglas) queda como **migración versionada** en el proyecto, para que cualquiera que clone el repositorio obtenga la misma base.
- El primer admin se marca a mano desde el panel de PocketBase.

## Capabilities

### New Capabilities
- `roles-usuarios`: roles usuario/admin en las cuentas y reglas de PocketBase que limitan qué puede hacer cada rol.
- `administracion-cuentas`: panel de admin dentro de la app para listar, desactivar/reactivar y resetear la contraseña de cuentas, y bloqueo de inicio de sesión de cuentas desactivadas.

### Modified Capabilities

Ninguna: no cambia el texto de los requisitos existentes de inicio de sesión ni del conversor; el bloqueo de cuentas desactivadas se agrega como requisito nuevo.

## Impact

- Base de datos: migración nueva en `pb_migrations/` (se sube a Git); `pocketbase.sh` pasa a usarla.
- Código: ampliaciones en `pocketbase_cliente.py`, `servicio.py`, `app.py` y tests.
- Usuarios ya registrados en la v2 siguen funcionando: sin rol cargado se tratan como `usuario` y activos.
- Fuera de alcance: crear cuentas desde el panel, borrar cuentas, cambiar roles desde la app (se hace en el panel de PocketBase), historial en la base (v4), `.env`, DolarAPI (v5).
