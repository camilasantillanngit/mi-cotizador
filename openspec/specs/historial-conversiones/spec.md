# historial-conversiones Specification

## Purpose
Mantiene un registro persistente de todas las conversiones realizadas, ligado a quien las hizo y con fecha y hora, en la base de datos, con acceso limitado según el rol.

## Requirements

### Requirement: Registro de cada conversión
La aplicación SHALL guardar en la base de datos una consulta por cada conversión exitosa, con el usuario que la hizo, el monto en pesos, la cotización, el resultado en dólares y la fecha y hora, y MUST NOT escribir `historial.txt`.

#### Scenario: Primera conversión
- **WHEN** un usuario con sesión convierte por primera vez 150000 pesos con cotización 1550
- **THEN** se crea una consulta con su usuario, monto 150000, cotización 1550, resultado 96,77 y la fecha y hora actuales, y no se crea ningún archivo `historial.txt`

#### Scenario: Conversiones sucesivas
- **WHEN** el usuario realiza otra conversión
- **THEN** se agrega una consulta nueva sin modificar las anteriores

### Requirement: Ubicación y persistencia del historial
El historial SHALL guardarse en la base de datos y MUST conservarse entre ejecuciones de la aplicación y desde cualquier computadora que use la misma base.

#### Scenario: Reabrir la aplicación
- **WHEN** el usuario cierra y vuelve a abrir Mi Cotizador e inicia sesión
- **THEN** ve en "Historial" las consultas hechas antes

### Requirement: Datos inválidos no se registran
La aplicación MUST NOT guardar ninguna consulta cuando la conversión falla por datos inválidos.

#### Scenario: Conversión rechazada
- **WHEN** la validación rechaza los datos ingresados
- **THEN** no se crea ninguna consulta

### Requirement: Error al guardar el historial
Si no se puede guardar la consulta en la base de datos, la aplicación SHALL informar el problema al usuario y MUST seguir mostrando el resultado de la conversión.

#### Scenario: Base de datos no disponible al guardar
- **WHEN** la conversión es válida pero la base de datos no responde
- **THEN** se muestra el resultado y un aviso de que no se pudo guardar el historial

### Requirement: Cada usuario ve solo su historial
La pestaña "Historial" SHALL mostrar al usuario común únicamente sus propias consultas, de la más reciente a la más antigua, y la base de datos MUST impedirle ver las de otras personas.

#### Scenario: Usuario consulta su historial
- **WHEN** un usuario común abre "Historial"
- **THEN** ve solo sus consultas, con fecha y hora, monto, cotización y resultado

#### Scenario: Pedido directo a otras consultas
- **WHEN** un usuario común pide a la base las consultas de otro usuario
- **THEN** la base no se las devuelve

### Requirement: El admin ve las consultas de todos
El admin SHALL ver en "Historial" las consultas de todos los usuarios, indicando el correo de quien consultó.

#### Scenario: Admin abre el historial
- **WHEN** un admin abre "Historial"
- **THEN** ve las consultas de todos, cada una con el correo del usuario que la hizo

### Requirement: Las consultas no se alteran ni se borran
Las consultas guardadas MUST NOT poder modificarse ni borrarse desde la aplicación ni desde la API por ningún usuario, y un usuario solo SHALL poder crear consultas a su propio nombre.

#### Scenario: Crear una consulta a nombre de otro
- **WHEN** un usuario intenta crear una consulta a nombre de otra persona
- **THEN** la base rechaza el pedido

#### Scenario: Editar o borrar una consulta
- **WHEN** cualquier usuario, incluso un admin, intenta modificar o borrar una consulta por la API
- **THEN** la base rechaza el pedido
