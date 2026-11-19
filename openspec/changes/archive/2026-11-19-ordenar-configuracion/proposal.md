# Proposal

## Why

La dirección de PocketBase está escrita en el código y, a medida que el proyecto crezca (MCP, claves de servicios), habrá datos sensibles que no deben vivir en el código ni subirse a GitHub. El paso "Ordenar el proyecto" de la clase pide pasarlos a variables de entorno en un archivo `.env` que nunca se sube, con un `.env.example` sin valores.

## What Changes

- La app lee su configuración de un archivo `.env` (y de variables de entorno reales) en lugar de tenerla fija en el código.
- Se agrega `.env.example` (versionado, sin valores secretos) y `.env` queda ignorado por Git.
- Hoy la única variable que usa la app es `POCKETBASE_URL`; sigue funcionando sin `.env` con el valor por defecto.
- El README explica cómo crear el `.env` y dónde ponerlo para el ejecutable.

## Capabilities

### New Capabilities
- `configuracion-entorno`: lectura de la configuración desde `.env` y variables de entorno, con valores por defecto, y garantía de que los datos sensibles no se suben a Git.

### Modified Capabilities

Ninguna: el comportamiento visible de la app no cambia.

## Impact

- Código: módulo nuevo de configuración y ajuste de `pocketbase_cliente.py`; tests.
- Archivos: `.env.example` (se sube), `.env` (local, ignorado), `.gitignore` y README.
- Fuera de alcance: cifrar secretos, gestores de secretos, variables del MCP (clase 12) y de OpenAI (v7): se agregarán cuando existan.
