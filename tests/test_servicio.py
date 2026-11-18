import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pocketbase_cliente as pb  # noqa: E402
from servicio import Servicio  # noqa: E402


class TestServicio(unittest.TestCase):
    def test_convertir_sin_sesion_se_rechaza(self):
        with mock.patch("cotizador.procesar") as procesar:
            r = Servicio().convertir("100", "10")
        self.assertFalse(r["ok"])
        procesar.assert_not_called()

    def test_con_sesion_convierte_y_cerrar_la_quita(self):
        s = Servicio()
        with mock.patch("pocketbase_cliente.iniciar_sesion", return_value=("tok", "a@b.com")):
            self.assertEqual(s.iniciar_sesion("a@b.com", "12345678"), {"ok": True, "correo": "a@b.com"})
        with mock.patch("cotizador.procesar", return_value={"ok": True}) as procesar:
            self.assertTrue(s.convertir("100", "10")["ok"])
            procesar.assert_called_once()
        s.cerrar_sesion()
        self.assertFalse(s.convertir("100", "10")["ok"])

    def test_error_de_acceso_no_inicia_sesion(self):
        s = Servicio()
        with mock.patch("pocketbase_cliente.iniciar_sesion", side_effect=pb.ErrorAcceso("Correo o contraseña incorrectos.")):
            r = s.iniciar_sesion("a@b.com", "mala")
        self.assertEqual(r, {"ok": False, "error": "Correo o contraseña incorrectos."})
        self.assertFalse(s.convertir("100", "10")["ok"])


if __name__ == "__main__":
    unittest.main()
