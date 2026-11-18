# Design

## Context

Hoy `cotizador.procesar` valida, convierte y escribe `historial.txt`. La sesión (token, id, rol) vive en `servicio.py`; `pocketbase_cliente.py` habla con la API de PocketBase v0.40.6; la estructura de la base se versiona en `pb_migrations/`. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Guardar y consultar el historial en PocketBase, con permisos aplicados por la base.
- Separar cálculo (puro) de persistencia.

**Non-Goals:**
- Importar el TXT, filtros, exportar, editar o borrar consultas.

## Decisions

- **Colección `consultas`** (migración nueva, versionada): `usuario` (relación a `users`, obligatoria), `monto`, `cotizacion`, `resultado` (números) y `created` (campo de fecha automático que pone el servidor). Alternativa: guardar montos como texto para evitar decimales binarios; se descarta porque números permiten sumar y ordenar (las preguntas de la v6 por MCP, como el monto total por usuario) y todos los valores se redondean a 2 decimales antes de guardar.
- **Reglas**: `createRule` solo con sesión activa y `@request.body.usuario = @request.auth.id`; `listRule`/`viewRule`: dueño activo, o admin activo; `updateRule` y `deleteRule` nulas (nadie las altera por la API; solo el superusuario desde el panel).
- **Fecha automática**: la pone el servidor al crear, no la app, para que no dependa del reloj del equipo.
- **Cálculo vs. persistencia**: `cotizador.py` pasa a exponer `calcular(monto_texto, cotizacion_texto)` (valida y convierte, sin archivos); se eliminan las funciones de TXT. `servicio.convertir` calcula y luego guarda la consulta con el token del usuario.
- **Fallo al guardar no bloquea el resultado**: si PocketBase no responde, se devuelve el resultado con un aviso, igual que antes con el TXT.
- **Listado**: `GET .../consultas/records?sort=-created&perPage=50&expand=usuario`; el admin recibe el correo del usuario por `expand`. Se muestran las 50 más recientes; la paginación queda fuera de alcance. La fecha se muestra en hora local en la interfaz.
- **Interfaz**: la pestaña "Historial" aparece para todos; "Cuentas" sigue solo para admin.
- **`historial.txt` previo**: no se toca ni se importa; sigue ignorado por Git.

## Risks / Trade-offs

- [Reglas mal escritas expondrían consultas ajenas] → Verificación obligatoria con pedidos directos a la API con usuario común, admin y cuenta desactivada, sobre una base temporal, antes de aplicar a la base real.
- [Pérdida de consultas si la base no responde al guardar] → Se avisa; el historial local (TXT) se jubila a propósito, como pide la clase. Aceptado.
- [Números decimales en la base] → Se redondea a 2 decimales y el resultado se calcula con `Decimal` en la app.
- [`expand=usuario` podría fallar si el admin no puede ver a un usuario] → El admin activo puede ver todas las cuentas por las reglas de la v3.
