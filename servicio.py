"""Estado de sesión de Mi Cotizador: lo que expone la interfaz a Python."""
import cotizador
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
        return cotizador.procesar(monto, cotizacion)

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
