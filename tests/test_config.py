import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.env = Path(self.dir.name) / ".env"
        patcher = mock.patch.dict(os.environ, {}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("MC_PRUEBA", None)

    def tearDown(self):
        self.dir.cleanup()

    def test_lee_valor_del_env(self):
        self.env.write_text("MC_PRUEBA=http://127.0.0.1:9000\n", encoding="utf-8")
        self.assertEqual(config.obtener("MC_PRUEBA", "x", self.env), "http://127.0.0.1:9000")

    def test_sin_archivo_usa_por_defecto(self):
        self.assertEqual(config.obtener("MC_PRUEBA", "defecto", Path(self.dir.name) / "no-existe"), "defecto")

    def test_entorno_tiene_prioridad_sobre_el_archivo(self):
        self.env.write_text("MC_PRUEBA=del-archivo\n", encoding="utf-8")
        os.environ["MC_PRUEBA"] = "del-entorno"
        self.assertEqual(config.obtener("MC_PRUEBA", "x", self.env), "del-entorno")

    def test_comentarios_vacias_y_comillas(self):
        self.env.write_text('# comentario\n\nMC_PRUEBA="entre comillas"\nOTRA=\'simple\'\nexport TERCERA=3\n', encoding="utf-8")
        valores = config.leer_env(self.env)
        self.assertEqual(valores, {"MC_PRUEBA": "entre comillas", "OTRA": "simple", "TERCERA": "3"})

    def test_linea_mal_formada_se_ignora(self):
        self.env.write_text("esto no tiene igual\nMC_PRUEBA=ok\n=sinclave\n", encoding="utf-8")
        self.assertEqual(config.leer_env(self.env), {"MC_PRUEBA": "ok"})

    def test_valor_con_signo_igual(self):
        self.env.write_text("MC_PRUEBA=a=b=c\n", encoding="utf-8")
        self.assertEqual(config.obtener("MC_PRUEBA", None, self.env), "a=b=c")

    def test_no_imprime_valores(self):
        self.env.write_text("MC_PRUEBA=secreto-123\n", encoding="utf-8")
        import io
        from contextlib import redirect_stdout, redirect_stderr
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            config.obtener("MC_PRUEBA", None, self.env)
        self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
