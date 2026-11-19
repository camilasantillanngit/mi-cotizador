import json
import sys
import threading
import unittest
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import dolarapi  # noqa: E402

ESTADO = {"codigo": 200, "cuerpo": b"", "pedidos": []}


class Falso(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        ESTADO["pedidos"].append((self.path, dict(self.headers)))
        self.send_response(ESTADO["codigo"])
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(ESTADO["cuerpo"])


def responder(codigo=200, cuerpo=None):
    ESTADO["codigo"] = codigo
    ESTADO["cuerpo"] = cuerpo if isinstance(cuerpo, bytes) else json.dumps(cuerpo).encode()


class TestDolarApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = HTTPServer(("127.0.0.1", 0), Falso)
        cls.url = f"http://127.0.0.1:{cls.servidor.server_port}/v1/dolares/oficial"
        threading.Thread(target=cls.servidor.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()

    def setUp(self):
        ESTADO["pedidos"].clear()

    def test_respuesta_correcta(self):
        responder(200, {"compra": 1530, "venta": 1580, "fechaActualizacion": "2026-11-18T18:00:00.000Z"})
        r = dolarapi.obtener_venta(self.url)
        self.assertEqual(r, {"venta": Decimal("1580"), "fecha": "2026-11-18T18:00:00.000Z"})

    def test_venta_decimal(self):
        responder(200, {"venta": 1580.5})
        self.assertEqual(dolarapi.obtener_venta(self.url)["venta"], Decimal("1580.5"))

    def test_respuestas_invalidas(self):
        for cuerpo in [{}, {"venta": None}, {"venta": "1580"}, {"venta": 0}, {"venta": -5},
                       {"venta": True}, [1, 2], "texto", {"compra": 1530}]:
            responder(200, cuerpo)
            with self.assertRaises(dolarapi.CotizacionNoDisponible, msg=str(cuerpo)):
                dolarapi.obtener_venta(self.url)

    def test_no_json(self):
        responder(200, b"<html>no es json</html>")
        with self.assertRaises(dolarapi.CotizacionNoDisponible):
            dolarapi.obtener_venta(self.url)

    def test_error_http(self):
        responder(500, {"error": "x"})
        with self.assertRaises(dolarapi.CotizacionNoDisponible):
            dolarapi.obtener_venta(self.url)

    def test_servicio_caido(self):
        with self.assertRaisesRegex(dolarapi.CotizacionNoDisponible, "Ingresala a mano"):
            dolarapi.obtener_venta("http://127.0.0.1:1/x")

    def test_el_pedido_no_lleva_datos_del_usuario(self):
        responder(200, {"venta": 1580})
        dolarapi.obtener_venta(self.url)
        ruta, cabeceras = ESTADO["pedidos"][0]
        self.assertEqual(ruta, "/v1/dolares/oficial")  # sin parámetros
        nombres = {k.lower() for k in cabeceras}
        self.assertFalse(nombres & {"authorization", "cookie", "x-api-key"}, nombres)


if __name__ == "__main__":
    unittest.main()
