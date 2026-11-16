import sys
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cotizador as c  # noqa: E402


class TestConversion(unittest.TestCase):
    def test_conversion_basica(self):
        r = c.convertir(Decimal("100000"), Decimal("1000"))
        self.assertEqual(c.formatear_usd(r), "USD 100,00")

    def test_coma_y_punto_equivalen(self):
        self.assertEqual(c.parsear_numero("1500,50", "x"), c.parsear_numero("1500.50", "x"))

    def test_redondeo_dos_decimales(self):
        self.assertEqual(c.convertir(Decimal("100"), Decimal("3")), Decimal("33.33"))

    def test_formato_miles(self):
        self.assertEqual(c.formatear_usd(Decimal("1234.5")), "USD 1.234,50")

    def test_invalidos(self):
        for texto in ["", "   ", "abc", "0", "-5", "nan", "inf"]:
            with self.assertRaises(c.DatoInvalido, msg=texto):
                c.parsear_numero(texto, "el monto")


class TestHistorial(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.ruta = Path(self.dir.name) / "historial.txt"
        self.ahora = datetime(2026, 11, 16, 17, 45, 3)

    def tearDown(self):
        self.dir.cleanup()

    def test_crea_y_formato(self):
        r = c.procesar("100000", "1000", self.ruta, self.ahora)
        self.assertTrue(r["ok"])
        self.assertEqual(r["resultado"], "USD 100,00")
        self.assertEqual(
            self.ruta.read_text(encoding="utf-8"),
            "2026-11-16 17:45:03 | ARS 100000.00 | cotización 1000.00 | USD 100.00\n",
        )

    def test_agrega_sin_borrar(self):
        c.procesar("100", "10", self.ruta, self.ahora)
        c.procesar("200", "10", self.ruta, self.ahora)
        self.assertEqual(len(self.ruta.read_text(encoding="utf-8").splitlines()), 2)

    def test_invalido_no_escribe(self):
        r = c.procesar("abc", "1000", self.ruta, self.ahora)
        self.assertFalse(r["ok"])
        self.assertFalse(self.ruta.exists())
        r = c.procesar("100", "0", self.ruta, self.ahora)
        self.assertFalse(r["ok"])
        self.assertFalse(self.ruta.exists())

    def test_error_de_escritura_conserva_resultado(self):
        ruta_mala = Path(self.dir.name) / "no_existe" / "historial.txt"
        r = c.procesar("100", "10", ruta_mala, self.ahora)
        self.assertTrue(r["ok"])
        self.assertEqual(r["resultado"], "USD 10,00")
        self.assertIsNotNone(r["aviso"])


if __name__ == "__main__":
    unittest.main()
