# Spec Delta

## Purpose

Evita escribir la cotización a mano y los errores que eso trae, trayendo el valor del dólar oficial desde un servicio público y dejando siempre una salida manual.

## ADDED Requirements

### Requirement: Cotización automática al abrir el conversor
Al mostrarse el conversor, la aplicación SHALL consultar la cotización del dólar oficial (venta) y completar el campo de cotización con ese valor, indicando su origen y la fecha de actualización.

#### Scenario: Servicio disponible
- **WHEN** el usuario inicia sesión y el servicio responde con venta 1580
- **THEN** el campo de cotización muestra 1580, junto con "Dólar oficial (venta)" y la fecha de actualización

### Requirement: Botón para actualizar
La aplicación SHALL ofrecer un botón "Actualizar cotización" que vuelva a consultar el servicio y reemplace el valor del campo.

#### Scenario: Actualizar
- **WHEN** el usuario presiona "Actualizar cotización" y el servicio responde con un valor nuevo
- **THEN** el campo y la fecha de actualización muestran el valor nuevo

### Requirement: La cotización sigue siendo editable
El usuario SHALL poder escribir una cotización distinta en el campo, y la aplicación MUST NOT reemplazarla salvo que se presione "Actualizar cotización".

#### Scenario: Cotización escrita a mano
- **WHEN** el usuario cambia el valor del campo y convierte
- **THEN** la conversión usa el valor escrito por el usuario

### Requirement: Fallo del servicio
Si el servicio no responde o devuelve datos inválidos, la aplicación SHALL avisar que no pudo obtener la cotización, dejar el campo editable y MUST NOT cerrarse ni dejar de permitir conversiones manuales.

#### Scenario: Sin conexión
- **WHEN** no hay conexión a internet al abrir el conversor
- **THEN** se muestra un aviso de que no se pudo obtener la cotización y el usuario puede escribirla a mano

#### Scenario: Respuesta inválida
- **WHEN** el servicio responde sin un valor de venta numérico y mayor que cero
- **THEN** se trata como fallo y no se completa el campo

### Requirement: No se envían datos del usuario
El pedido al servicio SHALL ser una consulta pública sin datos del usuario, de la sesión ni de la base de datos.

#### Scenario: Contenido del pedido
- **WHEN** la aplicación consulta la cotización
- **THEN** el pedido no incluye correo, token, montos ni ningún dato de la cuenta
