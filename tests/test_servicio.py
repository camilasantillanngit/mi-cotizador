import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pocketbase_cliente as pb  # noqa: E402
from servicio import Servicio  # noqa: E402

ADMIN = pb.Sesion("tok", "adm@b.com", "admin", "idAdmin")
USUARIO = pb.Sesion("tok", "u@b.com", "usuario", "idUser")


def servicio_con(sesion):
    s = Servicio()
    with mock.patch("pocketbase_cliente.iniciar_sesion", return_value=sesion):
        s.iniciar_sesion(sesion.correo, "12345678")
    return s


class TestSesion(unittest.TestCase):
    def test_convertir_sin_sesion_se_rechaza(self):
        with mock.patch("cotizador.procesar") as procesar:
            r = Servicio().convertir("100", "10")
        self.assertFalse(r["ok"])
        procesar.assert_not_called()

    def test_con_sesion_convierte_y_cerrar_la_quita(self):
        s = servicio_con(USUARIO)
        with mock.patch("cotizador.procesar", return_value={"ok": True}) as procesar:
            self.assertTrue(s.convertir("100", "10")["ok"])
            procesar.assert_called_once()
        s.cerrar_sesion()
        self.assertFalse(s.convertir("100", "10")["ok"])

    def test_inicio_devuelve_rol(self):
        s = Servicio()
        with mock.patch("pocketbase_cliente.iniciar_sesion", return_value=ADMIN):
            self.assertEqual(s.iniciar_sesion("a", "b"), {"ok": True, "correo": "adm@b.com", "rol": "admin"})

    def test_error_de_acceso_no_inicia_sesion(self):
        s = Servicio()
        with mock.patch("pocketbase_cliente.iniciar_sesion", side_effect=pb.ErrorAcceso("Correo o contraseña incorrectos.")):
            r = s.iniciar_sesion("a@b.com", "mala")
        self.assertEqual(r, {"ok": False, "error": "Correo o contraseña incorrectos."})
        self.assertFalse(s.convertir("100", "10")["ok"])


class TestAdministracion(unittest.TestCase):
    def test_usuario_comun_no_administra(self):
        s = servicio_con(USUARIO)
        with mock.patch("pocketbase_cliente.listar_cuentas") as listar, \
             mock.patch("pocketbase_cliente.cambiar_desactivado") as cambiar, \
             mock.patch("pocketbase_cliente.resetear_clave") as resetear:
            for r in (s.listar_cuentas(), s.desactivar("x"), s.reactivar("x"), s.resetear_clave("x", "12345678")):
                self.assertFalse(r["ok"])
                self.assertIn("permiso", r["error"])
        listar.assert_not_called(); cambiar.assert_not_called(); resetear.assert_not_called()

    def test_sin_sesion_no_administra(self):
        self.assertFalse(Servicio().listar_cuentas()["ok"])

    def test_admin_lista(self):
        s = servicio_con(ADMIN)
        with mock.patch("pocketbase_cliente.listar_cuentas", return_value=[pb.Cuenta("1", "a@b.com", "usuario", False)]):
            r = s.listar_cuentas()
        self.assertEqual(r["cuentas"], [{"id": "1", "correo": "a@b.com", "rol": "usuario", "desactivado": False}])

    def test_admin_no_se_desactiva_a_si_mismo(self):
        s = servicio_con(ADMIN)
        with mock.patch("pocketbase_cliente.cambiar_desactivado") as cambiar:
            r = s.desactivar("idAdmin")
        self.assertFalse(r["ok"])
        self.assertIn("propia cuenta", r["error"])
        cambiar.assert_not_called()

    def test_admin_desactiva_reactiva_y_resetea(self):
        s = servicio_con(ADMIN)
        with mock.patch("pocketbase_cliente.cambiar_desactivado") as cambiar, \
             mock.patch("pocketbase_cliente.resetear_clave") as resetear:
            self.assertTrue(s.desactivar("idUser")["ok"])
            self.assertTrue(s.reactivar("idUser")["ok"])
            self.assertTrue(s.resetear_clave("idUser", "12345678")["ok"])
        self.assertEqual([c.args[1:3] for c in cambiar.call_args_list], [("idUser", True), ("idUser", False)])
        resetear.assert_called_once()

    def test_clave_corta_devuelve_error(self):
        s = servicio_con(ADMIN)
        r = s.resetear_clave("idUser", "corta")
        self.assertFalse(r["ok"])
        self.assertIn("8 caracteres", r["error"])


if __name__ == "__main__":
    unittest.main()
