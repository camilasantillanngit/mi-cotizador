# Spec Delta

## MODIFIED Requirements

### Requirement: Campos de entrada y botón de conversión
La aplicación SHALL mostrar un campo para el monto en pesos, un campo para la cotización del dólar y un botón "Convertir"; el campo de cotización SHALL completarse con la cotización del día cuando esté disponible.

#### Scenario: Ventana inicial
- **WHEN** el usuario abre el conversor
- **THEN** ve el monto vacío, el botón "Convertir", un área de resultado sin valor y el campo de cotización completado con la del día, o vacío si no se pudo obtener
