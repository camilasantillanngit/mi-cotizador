import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pocketbase_cliente as pb  # noqa: E402

USUARIOS = {}  # correo -> {"id","password","rol","desactivado"}
ULTIMO = {}


class FalsoPocketBase(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _responder(self, codigo, cuerpo):
        datos = json.dumps(cuerpo).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(datos)

    def _cuerpo(self):
        largo = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(largo)) if largo else {}

    def do_POST(self):
        cuerpo = self._cuerpo()
        if self.path.endswith("/records"):
            if cuerpo["email"] in USUARIOS:
                return self._responder(400, {"data": {"email": {"code": "validation_not_unique"}}})
            USUARIOS[cuerpo["email"]] = {"id": f"id{len(USUARIOS)}", "password": cuerpo["password"],
                                         "rol": "", "desactivado": False}
            return self._responder(200, {"id": "x"})
        u = USUARIOS.get(cuerpo["identity"])
        if u and u["password"] == cuerpo["password"] and not u["desactivado"]:
            return self._responder(200, {"token": "tok", "record": {
                "email": cuerpo["identity"], "id": u["id"], "rol": u["rol"]}})
        return self._responder(403 if u and u["desactivado"] else 400, {"data": {}, "message": "Failed"})

    def do_GET(self):
        ULTIMO["auth"] = self.headers.get("Authorization")
        if ULTIMO["auth"] != "tok-admin":
            return self._responder(403, {})
        self._responder(200, {"items": [
            {"id": u["id"], "email": e, "rol": u["rol"], "desactivado": u["desactivado"]}
            for e, u in sorted(USUARIOS.items())]})

    def do_PATCH(self):
        ULTIMO["auth"] = self.headers.get("Authorization")
        cuerpo = self._cuerpo()
        ULTIMO["cuerpo"] = cuerpo
        ULTIMO["ruta"] = self.path
        if ULTIMO["auth"] != "tok-admin":
            return self._responder(404, {})
        self._responder(200, {})


class TestCliente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = HTTPServer(("127.0.0.1", 0), FalsoPocketBase)
        cls.base = f"http://127.0.0.1:{cls.servidor.server_port}"
        threading.Thread(target=cls.servidor.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()

    def setUp(self):
        USUARIOS.clear()
        ULTIMO.clear()

    def test_registro_correcto_inicia_sesion_como_usuario(self):
        s = pb.registrar("a@b.com", "12345678", "12345678", self.base)
        self.assertEqual((s.token, s.correo, s.rol), ("tok", "a@b.com", "usuario"))

    def test_rol_admin_se_conserva(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        USUARIOS["a@b.com"]["rol"] = "admin"
        self.assertEqual(pb.iniciar_sesion("a@b.com", "12345678", self.base).rol, "admin")

    def test_correo_repetido(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        with self.assertRaisesRegex(pb.ErrorAcceso, "ya está registrado"):
            pb.registrar("a@b.com", "12345678", "12345678", self.base)

    def test_credenciales_incorrectas(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        for correo, clave in [("a@b.com", "mala"), ("otro@b.com", "12345678")]:
            with self.assertRaisesRegex(pb.ErrorAcceso, "Correo o contraseña incorrectos"):
                pb.iniciar_sesion(correo, clave, self.base)

    def test_cuenta_desactivada_recibe_mismo_mensaje(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        USUARIOS["a@b.com"]["desactivado"] = True
        with self.assertRaisesRegex(pb.ErrorAcceso, "Correo o contraseña incorrectos"):
            pb.iniciar_sesion("a@b.com", "12345678", self.base)

    def test_base_apagada(self):
        with self.assertRaises(pb.BaseNoDisponible):
            pb.iniciar_sesion("a@b.com", "12345678", "http://127.0.0.1:1")

    def test_validaciones_no_llaman_al_servidor(self):
        muerta = "http://127.0.0.1:1"
        for correo, clave, conf, texto in [
            ("sin-arroba", "12345678", "12345678", "correo válido"),
            ("a@b.com", "corta", "corta", "8 caracteres"),
            ("a@b.com", "12345678", "87654321", "no coinciden"),
        ]:
            with self.assertRaisesRegex(pb.ErrorAcceso, texto):
                pb.registrar(correo, clave, conf, muerta)

    def test_listar_cuentas_usa_el_token(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        cuentas = pb.listar_cuentas("tok-admin", self.base)
        self.assertEqual([(c.correo, c.rol, c.desactivado) for c in cuentas], [("a@b.com", "usuario", False)])
        self.assertEqual(ULTIMO["auth"], "tok-admin")

    def test_listar_sin_permiso(self):
        with self.assertRaisesRegex(pb.ErrorAcceso, "permiso"):
            pb.listar_cuentas("tok-usuario", self.base)

    def test_desactivar_y_reactivar(self):
        pb.cambiar_desactivado("tok-admin", "id1", True, self.base)
        self.assertEqual((ULTIMO["ruta"], ULTIMO["cuerpo"]), ("/api/collections/users/records/id1", {"desactivado": True}))
        pb.cambiar_desactivado("tok-admin", "id1", False, self.base)
        self.assertEqual(ULTIMO["cuerpo"], {"desactivado": False})

    def test_resetear_clave(self):
        pb.resetear_clave("tok-admin", "id1", "nueva-clave-1", self.base)
        self.assertEqual(ULTIMO["cuerpo"], {"password": "nueva-clave-1", "passwordConfirm": "nueva-clave-1"})

    def test_resetear_clave_corta_no_llama(self):
        with self.assertRaisesRegex(pb.ErrorAcceso, "8 caracteres"):
            pb.resetear_clave("tok-admin", "id1", "corta", "http://127.0.0.1:1")

    def test_operacion_sin_permiso(self):
        with self.assertRaisesRegex(pb.ErrorAcceso, "permiso"):
            pb.cambiar_desactivado("tok-usuario", "id1", True, self.base)


if __name__ == "__main__":
    unittest.main()
