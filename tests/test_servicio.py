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
        with mock.patch("pocketbase_cliente.guardar_consulta") as guardar:
            r = Servicio().convertir("100", "10")
        self.assertFalse(r["ok"])
        guardar.assert_not_called()

    def test_con_sesion_convierte_guarda_y_cerrar_la_quita(self):
        s = servicio_con(USUARIO)
        with mock.patch("pocketbase_cliente.guardar_consulta") as guardar:
            r = s.convertir("155000", "1550")
        self.assertEqual((r["ok"], r["resultado"], r["aviso"]), (True, "USD 100,00", None))
        token, usuario, monto, cot, res = guardar.call_args.args[:5]
        self.assertEqual((token, usuario, str(monto), str(cot), str(res)), ("tok", "idUser", "155000.00", "1550.00", "100.00"))
        s.cerrar_sesion()
        self.assertFalse(s.convertir("100", "10")["ok"])

    def test_si_falla_el_guardado_igual_muestra_el_resultado(self):
        s = servicio_con(USUARIO)
        with mock.patch("pocketbase_cliente.guardar_consulta", side_effect=pb.BaseNoDisponible("base caída")):
            r = s.convertir("155000", "1550")
        self.assertTrue(r["ok"])
        self.assertEqual(r["resultado"], "USD 100,00")
        self.assertEqual(r["aviso"], "base caída")

    def test_datos_invalidos_no_guardan(self):
        s = servicio_con(USUARIO)
        with mock.patch("pocketbase_cliente.guardar_consulta") as guardar:
            self.assertFalse(s.convertir("abc", "1550")["ok"])
            self.assertFalse(s.convertir("100", "0")["ok"])
        guardar.assert_not_called()

    def test_historial_exige_sesion_y_devuelve_rol(self):
        self.assertFalse(Servicio().listar_historial()["ok"])
        consulta = pb.Consulta("c1", "a@b.com", 150000, 1550, 96.77, "2026-11-18 22:29:17.101Z")
        for sesion, admin in ((USUARIO, False), (ADMIN, True)):
            s = servicio_con(sesion)
            with mock.patch("pocketbase_cliente.listar_consultas", return_value=[consulta]):
                r = s.listar_historial()
            self.assertEqual((r["ok"], r["es_admin"], r["consultas"][0]["correo"]), (True, admin, "a@b.com"))

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


class TestCotizacion(unittest.TestCase):
    def test_cotizacion_ok_formato_para_el_campo(self):
        from decimal import Decimal
        with mock.patch("dolarapi.obtener_venta", return_value={"venta": Decimal("1580"), "fecha": "2026-11-18T18:00:00.000Z"}):
            r = Servicio().obtener_cotizacion()
        self.assertEqual(r, {"ok": True, "valor": "1580,00", "fecha": "2026-11-18T18:00:00.000Z", "origen": "Dólar oficial (venta)"})

    def test_cotizacion_el_valor_del_campo_es_convertible(self):
        import cotizador
        from decimal import Decimal
        with mock.patch("dolarapi.obtener_venta", return_value={"venta": Decimal("1580.5"), "fecha": None}):
            valor = Servicio().obtener_cotizacion()["valor"]
        self.assertEqual(cotizador.parsear_numero(valor, "x"), Decimal("1580.50"))

    def test_cotizacion_fallo_no_rompe(self):
        import dolarapi
        with mock.patch("dolarapi.obtener_venta", side_effect=dolarapi.CotizacionNoDisponible("No se pudo obtener la cotización. Ingresala a mano.")):
            r = Servicio().obtener_cotizacion()
        self.assertEqual(r, {"ok": False, "error": "No se pudo obtener la cotización. Ingresala a mano."})

    def test_cotizacion_no_usa_la_sesion(self):
        # funciona sin sesión y no recibe ningún dato de ella
        import dolarapi
        from decimal import Decimal
        with mock.patch("dolarapi.obtener_venta", return_value={"venta": Decimal("1"), "fecha": None}) as m:
            Servicio().obtener_cotizacion()
        m.assert_called_once_with()
