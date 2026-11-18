# Spec Delta

## Purpose

Permite que cada persona tenga su cuenta con correo y contraseña y que el conversor solo esté disponible para quienes iniciaron sesión.

## ADDED Requirements

### Requirement: Pantalla de acceso al abrir la app
La aplicación SHALL mostrar al abrirse una pantalla de inicio de sesión, con acceso a la pantalla de registro, y MUST NOT mostrar el conversor hasta que haya una sesión iniciada.

#### Scenario: Apertura sin sesión
- **WHEN** el usuario abre Mi Cotizador
- **THEN** ve campos de correo y contraseña, un botón "Iniciar sesión" y un enlace para registrarse, y no ve el conversor

### Requirement: Registro de cuenta
La aplicación SHALL permitir crear una cuenta con correo, contraseña y confirmación de contraseña, y MUST rechazar correos con formato inválido, contraseñas de menos de 8 caracteres, contraseñas que no coinciden y correos ya registrados, con un mensaje claro.

#### Scenario: Registro correcto
- **WHEN** el usuario completa correo nuevo, contraseña de 8 o más caracteres y su confirmación, y presiona "Registrarse"
- **THEN** la cuenta se crea, la sesión queda iniciada y se muestra el conversor

#### Scenario: Correo ya registrado
- **WHEN** el usuario intenta registrar un correo que ya tiene cuenta
- **THEN** se muestra un mensaje de que ese correo ya está registrado y no se crea otra cuenta

#### Scenario: Contraseñas distintas
- **WHEN** la contraseña y su confirmación no coinciden
- **THEN** se muestra un error y no se crea la cuenta

### Requirement: Inicio de sesión
La aplicación SHALL iniciar sesión con correo y contraseña válidos y MUST rechazar credenciales incorrectas sin revelar cuál de los dos datos falló.

#### Scenario: Credenciales correctas
- **WHEN** el usuario ingresa correo y contraseña de una cuenta existente
- **THEN** se muestra el conversor con el correo del usuario visible

#### Scenario: Credenciales incorrectas
- **WHEN** el usuario ingresa una contraseña equivocada
- **THEN** se muestra "Correo o contraseña incorrectos" y se mantiene la pantalla de acceso

### Requirement: Cierre de sesión
La aplicación SHALL ofrecer un botón "Cerrar sesión" que descarte la sesión y vuelva a la pantalla de acceso.

#### Scenario: Cerrar sesión
- **WHEN** el usuario presiona "Cerrar sesión"
- **THEN** vuelve a la pantalla de acceso y el conversor deja de estar disponible hasta iniciar sesión otra vez

### Requirement: Contraseñas protegidas
Las contraseñas MUST NOT guardarse ni mostrarse en texto plano: la aplicación las envía solo a PocketBase y no las escribe en archivos ni en el historial.

#### Scenario: Contraseña no registrada en archivos
- **WHEN** el usuario se registra o inicia sesión
- **THEN** la contraseña no aparece en `historial.txt` ni en ningún otro archivo del proyecto

### Requirement: Base de datos no disponible
Si PocketBase no responde, la aplicación SHALL mostrar un mensaje que indique que la base de datos no está en marcha y cómo levantarla, y MUST NOT cerrarse.

#### Scenario: PocketBase apagado
- **WHEN** el usuario intenta iniciar sesión o registrarse con PocketBase apagado
- **THEN** se muestra el aviso de que la base de datos no está disponible y la ventana sigue abierta
