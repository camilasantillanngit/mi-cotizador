# Design

## Context

La única configuración de la app es la dirección de PocketBase, leída con `os.environ.get("POCKETBASE_URL", …)` en `pocketbase_cliente.py`. No hay contraseñas en el código: las cuentas usan tokens de sesión. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Un único lugar (`config.py`) para leer configuración, con prioridad clara.
- Sin dependencias nuevas.

**Non-Goals:**
- Cifrado de secretos; variables que todavía no se usan.

## Decisions

- **Lector propio de `.env` con la biblioteca estándar** (`config.py`): el formato necesario es mínimo (`CLAVE=valor`, comentarios, comillas). Alternativa: `python-dotenv` (otra dependencia para algo trivial).
- **Prioridad**: variable del sistema > `.env` > valor por defecto. Permite sobrescribir sin tocar archivos.
- **Ubicación del `.env`**: carpeta del proyecto en desarrollo; para el ejecutable, la carpeta que contiene el `.app` (por ejemplo `~/Applications/`), como ya ocurría con otros archivos locales. Se documenta en el README.
- **`.env.example` con solo lo que se usa hoy** (`POCKETBASE_URL`) y comentarios sobre variables futuras; así no hay configuración muerta.
- **El lector no registra ni imprime valores** para no filtrar secretos en consolas o logs.

## Risks / Trade-offs

- [Un `.env` mal ubicado se ignora en silencio] → Los valores por defecto hacen que la app siga funcionando, y el README indica dónde ponerlo.
- [Subir el `.env` por error] → `.gitignore` y una verificación explícita con `git check-ignore`; si alguna vez se subiera una clave, hay que cambiarla (borrar el archivo no alcanza).
