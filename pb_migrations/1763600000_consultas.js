/// <reference path="../pocketbase/pb_data/types.d.ts" />
// v4: historial de conversiones en la base (reemplaza historial.txt).
migrate((app) => {
  const users = app.findCollectionByNameOrId("users");

  const activo = "@request.auth.desactivado = false";
  const admin = `@request.auth.rol = "admin" && ${activo}`;

  const consultas = new Collection({
    type: "base",
    name: "consultas",
    fields: [
      { type: "relation", name: "usuario", required: true, collectionId: users.id, maxSelect: 1, cascadeDelete: true },
      { type: "number", name: "monto", required: true },
      { type: "number", name: "cotizacion", required: true },
      { type: "number", name: "resultado", required: true },
      { type: "autodate", name: "created", onCreate: true, onUpdate: false },
    ],
    // Solo con sesión activa y siempre a nombre propio.
    createRule: `@request.auth.id != "" && ${activo} && @request.body.usuario = @request.auth.id`,
    // El dueño ve lo suyo; el admin activo ve todo.
    listRule: `(usuario = @request.auth.id && ${activo}) || (${admin})`,
    viewRule: `(usuario = @request.auth.id && ${activo}) || (${admin})`,
    // Las consultas no se alteran ni se borran por la API.
    updateRule: null,
    deleteRule: null,
  });

  return app.save(consultas);
}, (app) => {
  return app.delete(app.findCollectionByNameOrId("consultas"));
});
