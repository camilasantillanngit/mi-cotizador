# Tasks

## 1. Consulta a DolarAPI

- [x] 1.1 Agregar `certifi` a `requirements.txt` y crear `dolarapi.py` con `obtener_venta` (timeout 5 s, validación estricta, URL desde `config`). Verificación: tests con servidor local simulado cubren respuesta correcta, número inválido o ausente, error HTTP, servicio caído y que el pedido no lleva datos de usuario; `python -m unittest discover -s tests` pasa.
- [x] 1.2 Exponer `obtener_cotizacion` en `servicio.py` (valor, origen y fecha, o mensaje de error) y la bandera `--probar-cotizacion` en `app.py`. Verificación: tests del servicio pasan y `python app.py --probar-cotizacion` imprime la venta actual.
- [x] 1.3 Agregar `DOLARAPI_URL` a `.env.example` y al README. Verificación: el valor del `.env` cambia la dirección consultada.

## 2. Interfaz

- [x] 2.1 En `app.py`: completar el campo de cotización al mostrar el conversor (solo si está vacío), mostrar origen y fecha local, agregar el botón "Actualizar cotización" y el aviso de fallo. Verificación: en pantalla, con el servicio real aparece la venta del día; con `DOLARAPI_URL` inválida aparece el aviso y se puede escribir a mano.
- [x] 2.2 Comprobar que un valor escrito a mano no se pisa al cambiar de pestaña y sí se reemplaza con "Actualizar cotización". Verificación: observado en pantalla.

## 3. Ejecutable y verificación final

- [x] 3.1 Reconstruir el `.app` y ejecutarlo con `--probar-cotizacion`. Verificación: el ejecutable empaquetado imprime la cotización sin errores de certificado.
- [ ] 3.2 Con la app real: iniciar sesión y ver la cotización completada, convertir 155000 pesos y comparar con la venta mostrada, y probar sin internet. Verificación: resultado = 155000 / venta, y sin internet aparece el aviso.
