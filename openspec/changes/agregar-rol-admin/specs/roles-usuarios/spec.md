# Spec Delta

## Purpose

Distingue entre usuarios comunes y administradores y hace que la base de datos, no solo la interfaz, impida a un usuario común realizar tareas de administración.

## ADDED Requirements

### Requirement: Rol de cada cuenta
Cada cuenta SHALL tener un rol `usuario` o `admin`; las cuentas nuevas MUST crearse con rol `usuario` y las cuentas existentes sin rol MUST tratarse como `usuario`.

#### Scenario: Registro desde la app
- **WHEN** una persona se registra desde Mi Cotizador
- **THEN** su cuenta queda con rol `usuario`

#### Scenario: Cuenta anterior a los roles
- **WHEN** inicia sesión una cuenta creada en la v2, sin rol cargado
- **THEN** la app la trata como `usuario` y no muestra el panel de cuentas

### Requirement: No se puede elegir el rol al registrarse
La base de datos MUST rechazar cualquier registro que intente fijar el rol `admin` o la desactivación de la cuenta.

#### Scenario: Registro que intenta ser admin
- **WHEN** alguien envía a la base un registro nuevo con rol `admin`
- **THEN** la base rechaza el pedido y no se crea la cuenta

### Requirement: Un usuario común solo accede a su propia cuenta
La base de datos SHALL permitir a un usuario común ver y editar solo su propia cuenta, y MUST impedirle ver otras cuentas, cambiar su rol o desactivarse.

#### Scenario: Listar cuentas como usuario común
- **WHEN** un usuario común pide la lista de cuentas
- **THEN** recibe solamente su propia cuenta

#### Scenario: Autoascenso a admin
- **WHEN** un usuario común intenta cambiar su rol a `admin`
- **THEN** la base rechaza el cambio

### Requirement: El admin gestiona cuentas
La base de datos SHALL permitir a un admin activo listar todas las cuentas, desactivarlas o reactivarlas, y asignar una contraseña nueva sin conocer la anterior.

#### Scenario: Admin lista cuentas
- **WHEN** un admin activo pide la lista de cuentas
- **THEN** recibe todas las cuentas

### Requirement: Estructura de la base versionada
El campo de rol, el indicador de desactivación y las reglas de acceso SHALL definirse en una migración dentro del proyecto, que se aplica sola al iniciar PocketBase.

#### Scenario: Base nueva desde el repositorio
- **WHEN** alguien clona el repositorio y ejecuta `./pocketbase.sh` por primera vez
- **THEN** la base queda con roles y reglas sin pasos manuales en el panel
