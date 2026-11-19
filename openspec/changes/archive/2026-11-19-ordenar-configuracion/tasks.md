# Tasks

## 1. Lectura de configuración

- [x] 1.1 Crear `config.py` con la lectura de `.env` (comentarios, comillas, líneas mal formadas) y la prioridad entorno > `.env` > por defecto, más `tests/test_config.py`. Verificación: `python -m unittest discover -s tests` pasa con casos de precedencia, comillas, comentarios, línea inválida y archivo ausente.
- [x] 1.2 Usar `config` en `pocketbase_cliente.url_base()`. Verificación: tests que cambian la dirección mediante `.env` y mediante variable de entorno pasan.

## 2. Archivos y documentación

- [x] 2.1 Crear `.env.example`, crear tu `.env` local y agregar `.env` a `.gitignore`. Verificación: `git check-ignore .env` lo confirma y `git ls-files` lista `.env.example` y no `.env`.
- [x] 2.2 Documentar en el README cómo crear el `.env` y dónde ponerlo para el ejecutable. Verificación: seguir los pasos desde cero funciona.

## 3. Verificación final

- [x] 3.1 Con la app real: poner una dirección incorrecta en el `.env` y comprobar el aviso de base no disponible; restaurar el valor correcto y comprobar que inicia sesión. Verificación: ambos comportamientos observados en la app.
