# historial-conversiones Specification

## Purpose
Mantiene un registro persistente y legible de todas las conversiones realizadas, con fecha y hora, en un archivo de texto plano.

## Requirements

### Requirement: Registro de cada conversión
La aplicación SHALL agregar una línea a `historial.txt` por cada conversión exitosa, con fecha y hora, monto en pesos, cotización y resultado en dólares.

#### Scenario: Primera conversión
- **WHEN** el usuario convierte por primera vez y `historial.txt` no existe
- **THEN** la aplicación crea el archivo y escribe una línea como `2026-11-16 17:45:03 | ARS 100000.00 | cotización 1000.00 | USD 100.00`

#### Scenario: Conversiones sucesivas
- **WHEN** el usuario realiza otra conversión
- **THEN** la aplicación agrega una nueva línea al final sin borrar las anteriores

### Requirement: Ubicación y persistencia del historial
El archivo `historial.txt` SHALL guardarse en la misma carpeta donde está el ejecutable y MUST conservarse entre ejecuciones de la aplicación.

#### Scenario: Reabrir la aplicación
- **WHEN** el usuario cierra y vuelve a abrir Mi Cotizador y convierte de nuevo
- **THEN** la nueva línea se agrega al `historial.txt` existente

### Requirement: Datos inválidos no se registran
La aplicación MUST NOT escribir en `historial.txt` cuando la conversión falla por datos inválidos.

#### Scenario: Conversión rechazada
- **WHEN** la validación rechaza los datos ingresados
- **THEN** `historial.txt` queda sin cambios

### Requirement: Error al escribir el historial
Si no se puede escribir en `historial.txt`, la aplicación SHALL informar el problema al usuario y MUST seguir mostrando el resultado de la conversión.

#### Scenario: Carpeta sin permiso de escritura
- **WHEN** la carpeta del ejecutable no permite escribir
- **THEN** se muestra el resultado y un aviso de que no se pudo guardar el historial
