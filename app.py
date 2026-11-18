"""Mi Cotizador: ventana de escritorio (pywebview) para convertir pesos a dólares."""
import webview

from servicio import Servicio

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
  .vista{display:none}.vista.activa{display:block}
  .enlace{background:none;color:#0a6cff;margin-top:10px;padding:4px}
  .secundario{background:#e5e5ea;color:#1d1d1f;margin-top:0;padding:6px 12px;width:auto;font-size:13px}
  .barra{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;font-size:13px;color:#555}
  .err{color:#c0212a;font-size:14px;min-height:18px;margin-top:10px}
</style></head><body>
<h1>Mi Cotizador</h1>

<div id="v-login" class="vista activa">
  <label for="l-correo">Correo</label><input id="l-correo" type="email" autocomplete="username">
  <label for="l-clave">Contraseña</label><input id="l-clave" type="password" autocomplete="current-password">
  <button id="b-login">Iniciar sesión</button>
  <div class="err" id="l-err"></div>
  <button class="enlace" id="ir-registro">¿No tenés cuenta? Registrate</button>
</div>

<div id="v-registro" class="vista">
  <label for="r-correo">Correo</label><input id="r-correo" type="email" autocomplete="username">
  <label for="r-clave">Contraseña (mínimo 8 caracteres)</label><input id="r-clave" type="password" autocomplete="new-password">
  <label for="r-conf">Repetir contraseña</label><input id="r-conf" type="password" autocomplete="new-password">
  <button id="b-registro">Registrarse</button>
  <div class="err" id="r-err"></div>
  <button class="enlace" id="ir-login">Ya tengo cuenta</button>
</div>

<div id="v-conversor" class="vista">
  <div class="barra"><span id="usuario"></span><button class="secundario" id="b-salir">Cerrar sesión</button></div>
  <label for="monto">Monto en pesos (ARS)</label>
  <input id="monto" inputmode="decimal">
  <label for="cotizacion">Cotización del dólar</label>
  <input id="cotizacion" inputmode="decimal">
  <button id="convertir">Convertir</button>
  <div id="error"></div>
  <div id="resultado"></div>
  <div id="aviso"></div>
</div>

<script>
const $ = id => document.getElementById(id);
function ver(nombre){
  for (const v of document.querySelectorAll('.vista')) v.classList.remove('activa');
  $('v-' + nombre).classList.add('activa');
}
function limpiarClaves(){ for (const i of ['l-clave','r-clave','r-conf']) $(i).value=''; }
function entrar(r){
  limpiarClaves();
  $('usuario').textContent = r.correo;
  $('l-err').textContent = ''; $('r-err').textContent = '';
  $('resultado').textContent = ''; $('error').textContent = ''; $('aviso').textContent = '';
  ver('conversor');
}
$('ir-registro').addEventListener('click', () => ver('registro'));
$('ir-login').addEventListener('click', () => ver('login'));
$('b-login').addEventListener('click', async () => {
  const r = await window.pywebview.api.iniciar_sesion($('l-correo').value, $('l-clave').value);
  if (r.ok) entrar(r); else $('l-err').textContent = r.error;
});
$('b-registro').addEventListener('click', async () => {
  const r = await window.pywebview.api.registrar($('r-correo').value, $('r-clave').value, $('r-conf').value);
  if (r.ok) entrar(r); else $('r-err').textContent = r.error;
});
$('b-salir').addEventListener('click', async () => {
  await window.pywebview.api.cerrar_sesion();
  limpiarClaves(); ver('login');
});
async function convertir(){
  const r = await window.pywebview.api.convertir($('monto').value, $('cotizacion').value);
  $('error').textContent = r.ok ? '' : r.error;
  $('resultado').textContent = r.ok ? r.resultado : '';
  $('aviso').textContent = (r.ok && r.aviso) ? r.aviso : '';
}
$('convertir').addEventListener('click', convertir);
document.addEventListener('keydown', e => {
  if (e.key !== 'Enter') return;
  const activa = document.querySelector('.vista.activa').id;
  if (activa === 'v-login') $('b-login').click();
  else if (activa === 'v-registro') $('b-registro').click();
  else convertir();
});
</script></body></html>"""


Api = Servicio


if __name__ == "__main__":
    webview.create_window("Mi Cotizador", html=HTML, js_api=Api(), width=420, height=560)
    webview.start()
