"""Estado de sesión de Mi Cotizador: lo que expone la interfaz a Python."""
import cotizador
import dolarapi
import pocketbase_cliente as pb


class Servicio:
    def __init__(self, base=None):
        self._base = base
        self._sesion = None

    def _entrar(self, accion):
        try:
            self._sesion = accion()
            return {"ok": True, "correo": self._sesion.correo, "rol": self._sesion.rol}
        except pb.ErrorAcceso as error:
            return {"ok": False, "error": str(error)}

    def registrar(self, correo, clave, confirmacion):
        return self._entrar(lambda: pb.registrar(correo, clave, confirmacion, self._base))

    def iniciar_sesion(self, correo, clave):
        return self._entrar(lambda: pb.iniciar_sesion(correo, clave, self._base))

    def cerrar_sesion(self):
        self._sesion = None
        return {"ok": True}

    def convertir(self, monto, cotizacion):
        if not self._sesion:
            return {"ok": False, "error": "Iniciá sesión para convertir."}
        calculo = cotizador.calcular(monto, cotizacion)
        if not calculo["ok"]:
            return calculo
        respuesta = {"ok": True, "resultado": cotizador.formatear_usd(calculo["resultado"]), "aviso": None}
        try:
            pb.guardar_consulta(self._sesion.token, self._sesion.id, calculo["monto"],
                                calculo["cotizacion"], calculo["resultado"], self._base)
        except pb.ErrorAcceso as error:
            respuesta["aviso"] = str(error)
        return respuesta

    def listar_historial(self):
        if not self._sesion:
            return {"ok": False, "error": "Iniciá sesión para ver el historial."}
        try:
            consultas = pb.listar_consultas(self._sesion.token, self._base)
        except pb.ErrorAcceso as error:
            return {"ok": False, "error": str(error)}
        return {"ok": True, "es_admin": self._sesion.rol == "admin", "consultas": [
            {"id": c.id, "correo": c.correo, "monto": c.monto, "cotizacion": c.cotizacion,
             "resultado": c.resultado, "fecha": c.fecha} for c in consultas]}

    # --- administración de cuentas (la barrera real son las reglas de PocketBase) ---
    def _admin(self, accion):
        if not self._sesion or self._sesion.rol != "admin":
            return {"ok": False, "error": "No tenés permiso para hacer esto."}
        try:
            return {"ok": True, **accion(self._sesion.token)}
        except pb.ErrorAcceso as error:
            return {"ok": False, "error": str(error)}

    def listar_cuentas(self):
        return self._admin(lambda t: {"cuentas": [
            {"id": c.id, "correo": c.correo, "rol": c.rol, "desactivado": c.desactivado}
            for c in pb.listar_cuentas(t, self._base)]})

    def _cambiar_desactivado(self, id_cuenta, valor):
        if valor and self._sesion and id_cuenta == self._sesion.id:
            return {"ok": False, "error": "No podés desactivar tu propia cuenta."}
        return self._admin(lambda t: pb.cambiar_desactivado(t, id_cuenta, valor, self._base) or {})

    def desactivar(self, id_cuenta):
        return self._cambiar_desactivado(id_cuenta, True)

    def reactivar(self, id_cuenta):
        return self._cambiar_desactivado(id_cuenta, False)

    def resetear_clave(self, id_cuenta, clave):
        return self._admin(lambda t: pb.resetear_clave(t, id_cuenta, clave, self._base) or {})

    def obtener_cotizacion(self):
        """Venta del dólar oficial. No requiere ni envía datos de la sesión."""
        try:
            datos = dolarapi.obtener_venta()
        except dolarapi.CotizacionNoDisponible as error:
            return {"ok": False, "error": str(error)}
        valor = f"{datos['venta']:.2f}".replace(".", ",")
        return {"ok": True, "valor": valor, "fecha": datos["fecha"], "origen": "Dólar oficial (venta)"}
