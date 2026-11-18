# Spec Delta

## Purpose

Da a los administradores una pantalla dentro de Mi Cotizador para gestionar las cuentas: ver quién tiene acceso, bloquear cuentas y ayudar a recuperar el acceso con una contraseña nueva.

## ADDED Requirements

### Requirement: Panel de cuentas solo para admin
La aplicación SHALL mostrar el panel de cuentas únicamente cuando inicia sesión un usuario con rol `admin`, y MUST NOT mostrarlo ni permitir sus acciones a un usuario común.

#### Scenario: Entra un admin
- **WHEN** inicia sesión un admin
- **THEN** ve, además del conversor, una sección "Cuentas"

#### Scenario: Entra un usuario común
- **WHEN** inicia sesión un usuario común
- **THEN** no ve la sección "Cuentas" y sus pedidos de administración son rechazados

### Requirement: Lista de cuentas
El panel SHALL listar todas las cuentas con su correo, rol y estado (activa o desactivada).

#### Scenario: Ver la lista
- **WHEN** el admin abre "Cuentas"
- **THEN** ve una fila por cada cuenta con correo, rol y estado

### Requirement: Desactivar y reactivar cuentas
El admin SHALL poder desactivar y reactivar cuentas de otras personas, y MUST NOT poder desactivar su propia cuenta.

#### Scenario: Desactivar una cuenta
- **WHEN** el admin desactiva la cuenta de un usuario
- **THEN** la lista muestra esa cuenta como desactivada

#### Scenario: Desactivar la propia cuenta
- **WHEN** el admin intenta desactivar su propia cuenta
- **THEN** la aplicación lo impide y muestra un mensaje

### Requirement: Cuenta desactivada no inicia sesión
Una cuenta desactivada MUST NOT poder iniciar sesión y SHALL recibir el mismo mensaje que una credencial incorrecta.

#### Scenario: Login de cuenta desactivada
- **WHEN** alguien con una cuenta desactivada ingresa su correo y contraseña correctos
- **THEN** se muestra "Correo o contraseña incorrectos" y no se abre el conversor

### Requirement: Resetear contraseña
El admin SHALL poder asignar una contraseña nueva de al menos 8 caracteres a otra cuenta, y la contraseña anterior MUST dejar de funcionar.

#### Scenario: Reset correcto
- **WHEN** el admin asigna una contraseña nueva válida a una cuenta
- **THEN** esa persona puede iniciar sesión con la nueva y no con la anterior

#### Scenario: Contraseña demasiado corta
- **WHEN** el admin ingresa una contraseña de menos de 8 caracteres
- **THEN** se muestra un error y la contraseña no cambia
