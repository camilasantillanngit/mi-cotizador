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
  .tabs{display:flex;gap:6px;margin-bottom:14px}
  #t-cuentas{display:none}.tabs.admin #t-cuentas{display:inline-block}
  .consulta{background:#fff;border-radius:8px;padding:8px 10px;margin-bottom:8px;font-size:13px}
  .consulta .fecha{color:#666;font-size:12px}.consulta .quien{color:#0a6cff;font-size:12px}
  .vacio{color:#666;font-size:13px}
  .tab{margin:0;padding:6px 14px;width:auto;font-size:13px;background:#e5e5ea;color:#1d1d1f}
  .tab.sel{background:#1d1d1f;color:#fff}
  .fila{display:grid;grid-template-columns:1fr auto;gap:4px 8px;align-items:center;background:#fff;border-radius:8px;padding:8px 10px;margin-bottom:8px;font-size:13px}
  .fila .estado{color:#2a7a2a}.fila.off .estado{color:#c0212a}
  .acciones{grid-column:1/3;display:flex;gap:6px}
  .acciones button{margin:0;padding:5px 10px;width:auto;font-size:12px}
  .acciones .peligro{background:#c0212a}
  #form-clave{display:none;background:#fff;border-radius:8px;padding:10px;margin-top:8px}
  #form-clave.ver{display:block}
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
  <div class="tabs" id="tabs">
    <button class="tab sel" id="t-conv">Conversor</button>
    <button class="tab" id="t-hist">Historial</button>
    <button class="tab" id="t-cuentas">Cuentas</button>
  </div>
  <div id="panel-conv">
  <label for="monto">Monto en pesos (ARS)</label>
  <input id="monto" inputmode="decimal">
  <label for="cotizacion">Cotización del dólar</label>
  <input id="cotizacion" inputmode="decimal">
  <button id="convertir">Convertir</button>
  <div id="error"></div>
  <div id="resultado"></div>
  <div id="aviso"></div>
  </div>
  <div id="panel-hist" style="display:none">
    <div id="lista-hist"></div>
    <div class="err" id="h-err"></div>
  </div>
  <div id="panel-cuentas" style="display:none">
    <div id="lista"></div>
    <div id="form-clave">
      <label for="nueva-clave" id="clave-para"></label>
      <input id="nueva-clave" type="password" autocomplete="new-password">
      <button id="b-clave">Guardar contraseña nueva</button>
    </div>
    <div class="err" id="c-err"></div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
function ver(nombre){
  for (const v of document.querySelectorAll('.vista')) v.classList.remove('activa');
  $('v-' + nombre).classList.add('activa');
}
function limpiarClaves(){ for (const i of ['l-clave','r-clave','r-conf']) $(i).value=''; }
let cuentaClave = null;
function pestana(nombre){
  $('panel-conv').style.display = nombre === 'conv' ? 'block' : 'none';
  $('panel-hist').style.display = nombre === 'hist' ? 'block' : 'none';
  $('panel-cuentas').style.display = nombre === 'cuentas' ? 'block' : 'none';
  $('t-conv').classList.toggle('sel', nombre === 'conv');
  $('t-hist').classList.toggle('sel', nombre === 'hist');
  $('t-cuentas').classList.toggle('sel', nombre === 'cuentas');
  if (nombre === 'hist'){ $('h-err').textContent = ''; cargarHistorial(); }
  if (nombre === 'cuentas'){ $('c-err').textContent = ''; cargarCuentas(); }
}
function boton(texto, clase, accion){
  const b = document.createElement('button');
  b.textContent = texto; if (clase) b.className = clase;
  b.addEventListener('click', accion); return b;
}
const num = new Intl.NumberFormat('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
function fechaLocal(texto){
  const d = new Date(texto.replace(' ', 'T'));
  return isNaN(d) ? texto : d.toLocaleString('es-AR');
}
async function cargarHistorial(){
  const r = await window.pywebview.api.listar_historial();
  const lista = $('lista-hist'); lista.replaceChildren();
  if (!r.ok){ $('h-err').textContent = r.error; return; }
  if (!r.consultas.length){
    const v = document.createElement('div'); v.className = 'vacio'; v.textContent = 'Todavía no hay consultas.'; lista.append(v); return;
  }
  for (const c of r.consultas){
    const fila = document.createElement('div'); fila.className = 'consulta';
    const fecha = document.createElement('div'); fecha.className = 'fecha'; fecha.textContent = fechaLocal(c.fecha);
    const datos = document.createElement('div');
    datos.textContent = 'ARS ' + num.format(c.monto) + ' · cotización ' + num.format(c.cotizacion) + ' → USD ' + num.format(c.resultado);
    fila.append(fecha, datos);
    if (r.es_admin){
      const quien = document.createElement('div'); quien.className = 'quien'; quien.textContent = c.correo || '(usuario eliminado)'; fila.append(quien);
    }
    lista.append(fila);
  }
}
async function cargarCuentas(){
  const r = await window.pywebview.api.listar_cuentas();
  if (!r.ok) $('c-err').textContent = r.error;
  const lista = $('lista'); lista.replaceChildren();
  if (!r.ok) return;
  for (const c of r.cuentas){
    const fila = document.createElement('div');
    fila.className = 'fila' + (c.desactivado ? ' off' : '');
    const nombre = document.createElement('span'); nombre.textContent = c.correo + ' · ' + c.rol;
    const estado = document.createElement('span'); estado.className = 'estado';
    estado.textContent = c.desactivado ? 'Desactivada' : 'Activa';
    const acc = document.createElement('div'); acc.className = 'acciones';
    acc.append(
      boton(c.desactivado ? 'Reactivar' : 'Desactivar', c.desactivado ? '' : 'peligro', async () => {
        const x = await (c.desactivado ? window.pywebview.api.reactivar(c.id) : window.pywebview.api.desactivar(c.id));
        $('c-err').style.color = ''; $('c-err').textContent = x.ok ? '' : x.error; cargarCuentas();
      }),
      boton('Nueva contraseña', '', () => {
        cuentaClave = c.id; $('clave-para').textContent = 'Contraseña nueva para ' + c.correo;
        $('nueva-clave').value = ''; $('form-clave').classList.add('ver'); $('nueva-clave').focus();
      }));
    fila.append(nombre, estado, acc); lista.append(fila);
  }
}
function entrar(r){
  limpiarClaves();
  $('usuario').textContent = r.correo + (r.rol === 'admin' ? ' (admin)' : '');
  $('tabs').classList.toggle('admin', r.rol === 'admin');
  $('form-clave').classList.remove('ver'); $('c-err').textContent = ''; cuentaClave = null;
  pestana('conv');
  $('l-err').textContent = ''; $('r-err').textContent = '';
  $('resultado').textContent = ''; $('error').textContent = ''; $('aviso').textContent = '';
  ver('conversor');
}
$('t-conv').addEventListener('click', () => pestana('conv'));
$('t-hist').addEventListener('click', () => pestana('hist'));
$('t-cuentas').addEventListener('click', () => pestana('cuentas'));
$('b-clave').addEventListener('click', async () => {
  const r = await window.pywebview.api.resetear_clave(cuentaClave, $('nueva-clave').value);
  $('c-err').textContent = r.ok ? '' : r.error;
  if (r.ok){ $('form-clave').classList.remove('ver'); $('nueva-clave').value = ''; $('c-err').style.color = '#2a7a2a'; $('c-err').textContent = 'Contraseña actualizada.'; }
  else $('c-err').style.color = '';
});
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
  else if ($('panel-hist').style.display === 'block'){ /* nada */ }
  else if ($('panel-cuentas').style.display === 'block'){
    if ($('form-clave').classList.contains('ver')) $('b-clave').click();
  } else convertir();
});
</script></body></html>"""


Api = Servicio


if __name__ == "__main__":
    webview.create_window("Mi Cotizador", html=HTML, js_api=Api(), width=460, height=640)
    webview.start()
