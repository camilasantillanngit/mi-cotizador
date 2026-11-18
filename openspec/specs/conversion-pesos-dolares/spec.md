# conversion-pesos-dolares Specification

## Purpose
Permite al usuario convertir un monto en pesos a dólares a partir de una cotización que ingresa manualmente, mostrando el resultado en pantalla.

## Requirements

### Requirement: Campos de entrada y botón de conversión
La aplicación SHALL mostrar un campo para el monto en pesos, un campo para la cotización del dólar y un botón "Convertir".

#### Scenario: Ventana inicial
- **WHEN** el usuario abre Mi Cotizador
- **THEN** ve los dos campos vacíos, el botón "Convertir" y un área de resultado sin valor

### Requirement: Cálculo del resultado en dólares
Al presionar "Convertir", la aplicación SHALL mostrar el resultado en dólares igual al monto en pesos dividido por la cotización, redondeado a 2 decimales.

#### Scenario: Conversión correcta
- **WHEN** el usuario ingresa monto 100000 y cotización 1000 y presiona "Convertir"
- **THEN** la aplicación muestra "USD 100,00"

#### Scenario: Decimales con coma o punto
- **WHEN** el usuario ingresa monto "1500,50" o "1500.50" y una cotización válida
- **THEN** la aplicación interpreta ambos como el mismo número

### Requirement: Validación de datos
La aplicación SHALL rechazar montos o cotizaciones vacíos, no numéricos o menores o iguales a cero, y MUST mostrar un mensaje de error claro sin calcular ni guardar nada.

#### Scenario: Cotización cero
- **WHEN** el usuario ingresa cotización 0 y presiona "Convertir"
- **THEN** la aplicación muestra un mensaje de error y no muestra resultado

#### Scenario: Texto no numérico
- **WHEN** el usuario ingresa "abc" como monto y presiona "Convertir"
- **THEN** la aplicación muestra un mensaje de error indicando que el monto no es válido
