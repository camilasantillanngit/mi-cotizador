# configuracion-entorno Specification

## Purpose
Mantiene la configuración y los datos sensibles fuera del código y fuera del repositorio, permitiendo que cada persona use sus propios valores.

## Requirements

### Requirement: Configuración desde archivo .env
La aplicación SHALL leer su configuración de un archivo `.env` ubicado junto a la aplicación y MUST funcionar con los valores por defecto cuando el archivo no existe.

#### Scenario: Dirección de PocketBase en el .env
- **WHEN** el `.env` define `POCKETBASE_URL=http://127.0.0.1:9000`
- **THEN** la aplicación usa esa dirección para conectarse a la base de datos

#### Scenario: Sin .env
- **WHEN** no existe el archivo `.env`
- **THEN** la aplicación usa `http://127.0.0.1:8090` y funciona normalmente

### Requirement: Prioridad de las variables de entorno
Una variable definida en el entorno del sistema SHALL tener prioridad sobre el mismo nombre en el `.env`.

#### Scenario: Variable real y archivo en conflicto
- **WHEN** `POCKETBASE_URL` está definida en el entorno y también en el `.env` con otro valor
- **THEN** la aplicación usa el valor del entorno

### Requirement: Formato tolerante del .env
La lectura del `.env` SHALL ignorar líneas vacías y comentarios que empiezan con `#`, aceptar valores entre comillas y MUST NOT fallar por líneas mal formadas.

#### Scenario: Archivo con comentarios y comillas
- **WHEN** el `.env` contiene comentarios, líneas vacías y `POCKETBASE_URL="http://127.0.0.1:9000"`
- **THEN** se lee la dirección sin comillas y se ignora el resto

#### Scenario: Línea mal formada
- **WHEN** el `.env` contiene una línea sin signo `=`
- **THEN** esa línea se ignora y las demás se leen igual

### Requirement: Los datos sensibles no se suben a Git
El archivo `.env` MUST estar ignorado por Git, y el repositorio SHALL incluir un `.env.example` con los mismos nombres de variables y sin valores secretos.

#### Scenario: Estado de Git
- **WHEN** se ejecuta `git status` con un `.env` creado
- **THEN** el `.env` no aparece como archivo para subir y `.env.example` sí está versionado
