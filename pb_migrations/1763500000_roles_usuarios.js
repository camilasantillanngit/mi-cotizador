/// <reference path="../pocketbase/pb_data/types.d.ts" />
// v3: rol y desactivación de cuentas, con reglas de acceso.
migrate((app) => {
  const users = app.findCollectionByNameOrId("users");

  users.fields.add(new SelectField({
    name: "rol",
    values: ["usuario", "admin"],
    maxSelect: 1,
  }));
  users.fields.add(new BoolField({ name: "desactivado" }));

  const esAdmin = '@request.auth.rol = "admin" && @request.auth.desactivado = false';
  const propia = "id = @request.auth.id && @request.auth.desactivado = false";

  // Registro abierto, pero sin poder fijar rol ni desactivación.
  users.createRule = '@request.body.rol:isset = false && @request.body.desactivado:isset = false';
  // Cuentas desactivadas no inician sesión.
  users.authRule = "desactivado = false";
  users.listRule = `(${propia}) || (${esAdmin})`;
  users.viewRule = `(${propia}) || (${esAdmin})`;
  // Cada persona edita lo suyo (sin tocar rol/desactivado); el admin edita cualquiera.
  users.updateRule = `(${propia} && @request.body.rol:isset = false && @request.body.desactivado:isset = false) || (${esAdmin})`;
  // Permite al admin cambiar contraseñas ajenas sin la anterior.
  users.manageRule = esAdmin;
  // Sin borrado desde la API (se hace desde el panel de PocketBase).
  users.deleteRule = null;

  return app.save(users);
}, (app) => {
  const users = app.findCollectionByNameOrId("users");
  users.fields.removeByName("rol");
  users.fields.removeByName("desactivado");
  users.createRule = "";
  users.authRule = "";
  users.listRule = "id = @request.auth.id";
  users.viewRule = "id = @request.auth.id";
  users.updateRule = "id = @request.auth.id";
  users.manageRule = null;
  users.deleteRule = "id = @request.auth.id";
  return app.save(users);
});
