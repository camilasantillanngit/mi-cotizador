# Tasks

## 1. Preparación del entorno

- [x] 1.1 Verificar que Tkinter abre una ventana en este macOS; como falla, usar pywebview (sin Tk). Verificación: `python app.py` abre la ventana sin errores.
- [x] 1.2 Crear entorno virtual `.venv`, `requirements.txt` (pywebview) y `requirements-dev.txt` (pyinstaller) e instalarlo. Verificación: `pyinstaller --version` imprime una versión.

## 2. Lógica de conversión e historial

- [x] 2.1 Crear `cotizador.py` con `parsear_numero` (coma/punto, rechaza vacío, no numérico, <= 0) y `convertir` (Decimal, 2 decimales). Verificación: tests `unittest` en `tests/test_cotizador.py` cubren 100000/1000 = 100.00, "1500,50" = "1500.50" y los errores; `python3 -m unittest` pasa.
- [x] 2.2 Agregar a `cotizador.py` `linea_historial` y `guardar_en_historial` (append UTF-8, crea el archivo, devuelve error si no puede escribir) y la resolución de la ruta junto al ejecutable. Verificación: tests con carpeta temporal confirman creación, anexado sin borrar, formato de línea y que un dato inválido no escribe; `python3 -m unittest` pasa.

## 3. Interfaz de escritorio

- [x] 3.1 Crear `app.py` con ventana pywebview: campo monto, campo cotización, botón "Convertir", etiqueta de resultado "USD x,xx" y mensajes de error/aviso. Verificación: al ejecutar `python3 app.py` la ventana muestra los campos y el botón.
- [x] 3.2 Conectar el botón a la lógica: calcular, mostrar el resultado, guardar en el historial y mostrar aviso si falla la escritura. Verificación: convertir 100000 con 1000 muestra "USD 100,00" y agrega la línea en `historial.txt`; un valor inválido muestra error y no cambia el archivo.

## 4. Ejecutable

- [x] 4.1 Crear `build.sh` que ejecute PyInstaller (`--windowed --name "Mi Cotizador"`) sobre `app.py`. Verificación: tras correr `./build.sh` existe `dist/Mi Cotizador.app`.
- [x] 4.2 Documentar en `README.md` cómo ejecutar, construir y abrir el ejecutable (incluido el aviso de Gatekeeper, clic derecho > Abrir). Verificación: seguir los pasos del README desde cero funciona.

## 5. Verificación final

- [ ] 5.1 Abrir el ejecutable `dist/Mi Cotizador.app`, convertir al menos dos montos y abrir `historial.txt` para comprobar fecha, hora y valores. Verificación: el archivo tiene una línea por conversión con el formato de la spec.
