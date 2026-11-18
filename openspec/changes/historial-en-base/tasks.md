# Tasks

## 1. Tabla de consultas

- [x] 1.1 Crear la migración `pb_migrations/…_consultas.js` con la colección `consultas` y sus reglas. Verificación: al iniciar PocketBase sobre una base nueva la migración se aplica y el panel muestra la colección y las reglas.
- [x] 1.2 Verificar las reglas con pedidos directos a la API (base temporal): un usuario crea solo a su nombre y ve solo las suyas, el admin ve todas, nadie edita ni borra, y una cuenta desactivada no crea. Verificación: tabla de resultados esperados vs. obtenidos, todos coinciden.

## 2. Lógica y cliente

- [x] 2.1 Refactorizar `cotizador.py`: dejar `calcular` y eliminar las funciones de `historial.txt`; actualizar `tests/test_cotizador.py`. Verificación: `python -m unittest discover -s tests` pasa y no queda código que escriba `historial.txt`.
- [x] 2.2 Agregar a `pocketbase_cliente.py` `guardar_consulta` y `listar_consultas` (con `expand=usuario` y orden por fecha); tests con servidor simulado. Verificación: los tests cubren alta, listado y errores; pasan.
- [x] 2.3 Conectar `servicio.convertir` para guardar la consulta con el usuario de la sesión, avisando si falla el guardado, y exponer `listar_historial`. Verificación: tests con y sin base disponible; el resultado se devuelve igual en ambos casos.

## 3. Interfaz

- [x] 3.1 Agregar la pestaña "Historial" para todos (con correo del usuario cuando es admin) y mostrar el aviso si no se guardó. Verificación: pruebas en pantalla con un usuario común y un admin muestran lo que corresponde a cada uno.
- [x] 3.2 Actualizar el README: el historial ahora vive en la base. Verificación: el README ya no menciona `historial.txt` como historial vigente y los pasos funcionan en una base nueva.

## 4. Verificación final

- [ ] 4.1 En la app real: convertir con dos usuarios distintos y comprobar que cada uno ve solo lo suyo, que el admin ve todo y que las consultas aparecen en el panel de PocketBase con usuario y fecha. Verificación: coincide con lo esperado en la app y en el panel.
