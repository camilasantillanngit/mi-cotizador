"""Mi Cotizador: ventana de escritorio (pywebview) para convertir pesos a dólares."""
import webview

import cotizador

HTML = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<style>
  body{font-family:-apple-system,Helvetica,sans-serif;margin:0;padding:28px;background:#f5f5f7;color:#1d1d1f}
  h1{font-size:22px;margin:0 0 18px}
  label{display:block;font-size:13px;margin:12px 0 4px;color:#555}
  input{width:100%;box-sizing:border-box;font-size:16px;padding:9px;border:1px solid #bbb;border-radius:8px}
  button{margin-top:18px;width:100%;font-size:16px;padding:11px;border:0;border-radius:8px;background:#0a6cff;color:#fff;cursor:pointer}
  button:active{background:#0555cc}
  #resultado{margin-top:20px;font-size:26px;font-weight:600;min-height:34px}
  #error{color:#c0212a;font-size:14px;min-height:18px;margin-top:10px}
  #aviso{color:#9a6700;font-size:13px;margin-top:6px}
</style></head><body>
<h1>Mi Cotizador</h1>
<label for="monto">Monto en pesos (ARS)</label>
<input id="monto" inputmode="decimal" autofocus>
<label for="cotizacion">Cotización del dólar</label>
<input id="cotizacion" inputmode="decimal">
<button id="convertir">Convertir</button>
<div id="error"></div>
<div id="resultado"></div>
<div id="aviso"></div>
<script>
async function convertir(){
  const r = await window.pywebview.api.convertir(
    document.getElementById('monto').value,
    document.getElementById('cotizacion').value);
  document.getElementById('error').textContent = r.ok ? '' : r.error;
  document.getElementById('resultado').textContent = r.ok ? r.resultado : '';
  document.getElementById('aviso').textContent = (r.ok && r.aviso) ? r.aviso : '';
}
document.getElementById('convertir').addEventListener('click', convertir);
document.addEventListener('keydown', e => { if (e.key === 'Enter') convertir(); });
</script></body></html>"""


class Api:
    def convertir(self, monto, cotizacion):
        return cotizador.procesar(monto, cotizacion)


if __name__ == "__main__":
    webview.create_window("Mi Cotizador", html=HTML, js_api=Api(), width=420, height=460)
    webview.start()
