import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pocketbase_cliente as pb  # noqa: E402

USUARIOS = {}


class FalsoPocketBase(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _responder(self, codigo, cuerpo):
        datos = json.dumps(cuerpo).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self):
        cuerpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.path.endswith("/records"):
            if cuerpo["email"] in USUARIOS:
                return self._responder(400, {"data": {"email": {"code": "validation_not_unique"}}})
            USUARIOS[cuerpo["email"]] = cuerpo["password"]
            return self._responder(200, {"id": "x"})
        if USUARIOS.get(cuerpo["identity"]) == cuerpo["password"]:
            return self._responder(200, {"token": "tok", "record": {"email": cuerpo["identity"]}})
        return self._responder(400, {"data": {}, "message": "Failed to authenticate."})


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

    def test_registro_correcto_inicia_sesion(self):
        token, correo = pb.registrar("a@b.com", "12345678", "12345678", self.base)
        self.assertEqual((token, correo), ("tok", "a@b.com"))

    def test_correo_repetido(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        with self.assertRaisesRegex(pb.ErrorAcceso, "ya está registrado"):
            pb.registrar("a@b.com", "12345678", "12345678", self.base)

    def test_credenciales_incorrectas(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        with self.assertRaisesRegex(pb.ErrorAcceso, "Correo o contraseña incorrectos"):
            pb.iniciar_sesion("a@b.com", "mala", self.base)
        with self.assertRaisesRegex(pb.ErrorAcceso, "Correo o contraseña incorrectos"):
            pb.iniciar_sesion("otro@b.com", "12345678", self.base)

    def test_inicio_correcto(self):
        pb.registrar("a@b.com", "12345678", "12345678", self.base)
        self.assertEqual(pb.iniciar_sesion(" a@b.com ", "12345678", self.base)[1], "a@b.com")

    def test_base_apagada(self):
        with self.assertRaises(pb.BaseNoDisponible):
            pb.iniciar_sesion("a@b.com", "12345678", "http://127.0.0.1:1")

    def test_validaciones_no_llaman_al_servidor(self):
        base_muerta = "http://127.0.0.1:1"
        for correo, clave, conf, texto in [
            ("sin-arroba", "12345678", "12345678", "correo válido"),
            ("a@b.com", "corta", "corta", "8 caracteres"),
            ("a@b.com", "12345678", "87654321", "no coinciden"),
        ]:
            with self.assertRaisesRegex(pb.ErrorAcceso, texto):
                pb.registrar(correo, clave, conf, base_muerta)


if __name__ == "__main__":
    unittest.main()
