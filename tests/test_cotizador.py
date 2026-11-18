import sys
import unittest
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


class TestCalcular(unittest.TestCase):
    def test_calculo_correcto(self):
        r = c.calcular("150000", "1550")
        self.assertEqual(
            (r["ok"], r["monto"], r["cotizacion"], r["resultado"]),
            (True, Decimal("150000.00"), Decimal("1550.00"), Decimal("96.77")),
        )

    def test_error_de_validacion(self):
        for monto, cot in [("abc", "1000"), ("100", "0"), ("", "10")]:
            r = c.calcular(monto, cot)
            self.assertFalse(r["ok"])
            self.assertIn("error", r)

    def test_no_hay_codigo_de_archivo(self):
        for nombre in ("procesar", "guardar_en_historial", "ruta_historial", "linea_historial"):
            self.assertFalse(hasattr(c, nombre), nombre)


if __name__ == "__main__":
    unittest.main()
