"""Estado de sesión de Mi Cotizador: lo que expone la interfaz a Python."""
import cotizador
import pocketbase_cliente as pb


class Servicio:
    def __init__(self, base=None):
        self._base = base
        self._token = None
        self._correo = None

    def _entrar(self, accion):
        try:
            self._token, self._correo = accion()
            return {"ok": True, "correo": self._correo}
        except pb.ErrorAcceso as error:
            return {"ok": False, "error": str(error)}

    def registrar(self, correo, clave, confirmacion):
        return self._entrar(lambda: pb.registrar(correo, clave, confirmacion, self._base))

    def iniciar_sesion(self, correo, clave):
        return self._entrar(lambda: pb.iniciar_sesion(correo, clave, self._base))

    def cerrar_sesion(self):
        self._token = None
        self._correo = None
        return {"ok": True}

    def convertir(self, monto, cotizacion):
        if not self._token:
            return {"ok": False, "error": "Iniciá sesión para convertir."}
        return cotizador.procesar(monto, cotizacion)
