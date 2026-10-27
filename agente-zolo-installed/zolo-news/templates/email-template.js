// ============================================================
// ZOLO NEWS — Plantilla HTML del boletín por correo
// Subagente 125-C · AliceLabs (Ecuador)
//
// HTML con CSS inline 100% (compatible Gmail / Outlook: tablas,
// bgcolor, sin flexbox/grid). Paleta:
//   fondo #0f1214 · acento #5aacd5 · texto #e6e8ea
// ============================================================

const TZ = 'America/Guayaquil';

// ---------- utilidades de fecha/hora en español (EC) ----------

/** Fecha larga en español: "Sábado 24 de octubre de 2026". */
export function fechaLarga(date = new Date()) {
  const d = date instanceof Date ? date : new Date(date);
  if (isNaN(d.getTime())) return '';
  const s = new Intl.DateTimeFormat('es-EC', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: TZ,
  }).format(d);
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Hora corta "HH:MM" en Ecuador. */
export function horaCorta(date = new Date()) {
  const d = date instanceof Date ? date : new Date(date);
  if (isNaN(d.getTime())) return '--:--';
  return new Intl.DateTimeFormat('es-EC', {
    hour: '2-digit', minute: '2-digit', hour12: false, timeZone: TZ,
  }).format(d);
}

/** Escape HTML básico para todo texto dinámico. */
export function escapeHtml(v = '') {
  return String(v ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

/** Trunca un texto en límite de palabra añadiendo elipsis. */
function truncar(texto, max) {
  const t = String(texto ?? '').replace(/\s+/g, ' ').trim();
  if (t.length <= max) return t;
  const cortado = t.slice(0, max);
  const ultEspacio = cortado.lastIndexOf(' ');
  return (ultEspacio > max * 0.6 ? cortado.slice(0, ultEspacio) : cortado) + '…';
}

// ---------- fuentes tipográficas seguras para correo ----------
const FONT = "font-family:Arial,Helvetica,sans-serif;";
const C = {
  fondo: '#0f1214',   // fondo principal (oscuro)
  panel: '#161c22',   // paneles/tarjetas
  borde: '#262d34',   // bordes sutiles
  acento: '#5aacd5',  // azul acento ZOLO
  texto: '#e6e8ea',   // texto principal
  suave: '#b9c2ca',   // texto secundario
  muted: '#8d979f',   // texto terciario
};

// ---------- bloques ----------

function bloqueHeader({ fecha, ciudad }) {
  return `
    <tr>
      <td style="background-color:${C.fondo};padding:28px 28px 20px;border-bottom:3px solid ${C.acento};">
        <div style="${FONT}font-size:12px;letter-spacing:4px;color:${C.acento};font-weight:bold;">ZOLO NOTICIAS</div>
        <div style="${FONT}font-size:22px;line-height:1.25;color:${C.texto};font-weight:bold;padding-top:8px;">📰 Tu boletín del amanecer</div>
        <div style="${FONT}font-size:13px;color:${C.muted};padding-top:6px;">${escapeHtml(fecha)}${ciudad ? ` &nbsp;·&nbsp; ${escapeHtml(ciudad)}` : ''}</div>
      </td>
    </tr>`;
}

function bloqueTextoSimple(titulo, texto) {
  if (!texto) return '';
  return `
    <tr><td style="padding:18px 28px 0;">
      <div style="${FONT}font-size:15px;line-height:1.6;color:${C.suave};">${texto}</div>
    </td></tr>`;
}

function bloqueTldr(noticias) {
  if (!noticias.length) return '';
  const items = noticias.slice(0, 4).map((n) =>
    `<tr><td style="${FONT}font-size:14px;line-height:1.55;color:${C.texto};padding:4px 0 4px 14px;border-left:3px solid ${C.acento};">
      ${escapeHtml(truncar(n.title || 'Titular', 90))}${n.source ? ` <span style="color:${C.muted};">— ${escapeHtml(n.source)}</span>` : ''}
    </td></tr>`
  ).join('\n');
  return `
    <tr><td style="padding:24px 28px 2px;">
      <div style="${FONT}font-size:16px;font-weight:bold;color:${C.acento};">⚡ En 30 segundos</div>
    </td></tr>
    <tr><td style="padding:8px 28px 0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">${items}</table>
    </td></tr>`;
}

function botonLeerMas(url) {
  if (!url) return '';
  return `
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;">
            <tr>
              <td bgcolor="${C.acento}" style="background-color:${C.acento};border-radius:8px;" align="center">
                <a href="${escapeHtml(url)}" target="_blank" style="${FONT}display:inline-block;padding:10px 18px;font-size:13px;font-weight:bold;color:#0f1214;text-decoration:none;border-radius:8px;">Leer más →</a>
              </td>
            </tr>
          </table>`;
}

function tarjetaNoticia(n, indice) {
  const cuerpo = n.text ? `<div style="${FONT}font-size:14px;line-height:1.6;color:${C.suave};padding-top:8px;">${escapeHtml(truncar(n.text, 320))}</div>` : '';
  const fuente = n.source ? `<div style="${FONT}font-size:12px;color:${C.muted};padding-top:8px;">— ${escapeHtml(n.source)}</div>` : '';
  return `
    <tr><td style="padding:10px 28px 0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="${C.panel}" style="background-color:${C.panel};border:1px solid ${C.borde};border-radius:12px;">
        <tr><td style="padding:18px 20px;">
          <div style="${FONT}font-size:16px;line-height:1.4;font-weight:bold;color:${C.texto};">${escapeHtml(n.title || `Noticia ${indice}`)}</div>
          ${cuerpo}${fuente}${botonLeerMas(n.url)}
        </td></tr>
      </table>
    </td></tr>`;
}

function bloqueNoticias(noticias) {
  if (!noticias.length) return '';
  const tarjetas = noticias.map((n, i) => tarjetaNoticia(n, i + 1)).join('\n');
  return `
    <tr><td style="padding:24px 28px 0;">
      <div style="${FONT}font-size:16px;font-weight:bold;color:${C.acento};">🗞️ Las noticias</div>
    </td></tr>${tarjetas}`;
}

function bloqueClima(weather, ciudad) {
  if (!weather) return '';
  const consejo = weather.caption
    ? `<div style="${FONT}font-size:13px;line-height:1.55;color:${C.acento};padding-top:10px;">💡 ${escapeHtml(truncar(weather.caption, 220))}</div>`
    : '';
  return `
    <tr><td style="padding:22px 28px 0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#12212b" style="background-color:#12212b;border:1px solid #2a4356;border-radius:12px;">
        <tr><td style="padding:18px 20px;">
          <div style="${FONT}font-size:16px;font-weight:bold;color:${C.acento};">🌤️ Clima${ciudad ? ` · ${escapeHtml(ciudad)}` : ''}</div>
          <div style="${FONT}font-size:14px;line-height:1.6;color:${C.texto};padding-top:8px;">${escapeHtml(truncar(weather.text || 'Sin datos de clima esta mañana.', 300))}</div>
          ${consejo}
        </td></tr>
      </table>
    </td></tr>`;
}

function bloqueCuriosidades(curious) {
  if (!curious) return '';
  return `
    <tr><td style="padding:22px 28px 0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="${C.panel}" style="background-color:${C.panel};border:1px solid ${C.borde};border-radius:12px;">
        <tr><td style="padding:18px 20px;">
          <div style="${FONT}font-size:16px;font-weight:bold;color:${C.acento};">🎲 ¿Sabías que…?</div>
          <div style="${FONT}font-size:14px;line-height:1.6;color:${C.suave};padding-top:8px;">${escapeHtml(truncar(curious.text || '', 400))}</div>
        </td></tr>
      </table>
    </td></tr>`;
}

function bloqueFooter(hora) {
  return `
    <tr><td style="padding:26px 28px 4px;">
      <div style="border-top:1px solid ${C.borde};padding-top:14px;">
        <div style="${FONT}font-size:12px;line-height:1.6;color:${C.muted};">
          ZOLO · AliceLabs — generado automáticamente a las ${escapeHtml(hora)}<br>
          Noticiero matutino autónomo del agente ZOLO · Ecuador 🇪🇨
        </div>
      </div>
    </td></tr>`;
}

// ---------- render principal ----------

/**
 * Genera el HTML completo del boletín.
 * @param {{cfg?:object, sections?:Array, date?:Date|string}} params
 * @returns {string} HTML con CSS inline (Gmail/Outlook friendly)
 */
export function renderBoletinHtml({ cfg = {}, sections = [], date = new Date() } = {}) {
  const fecha = fechaLarga(date);
  const hora = horaCorta(date);
  const ciudad = cfg?.city?.name || '';
  const secs = Array.isArray(sections) ? sections : [];

  const intro = secs.find((s) => s.kind === 'intro');
  const noticias = secs.filter((s) => s.kind === 'news');
  const weather = secs.find((s) => s.kind === 'weather');
  const curious = secs.find((s) => s.kind === 'curious');
  const outro = secs.find((s) => s.kind === 'outro');

  const introHtml = intro ? bloqueTextoSimple('intro', escapeHtml(truncar(intro.text, 400))) : '';
  const outroHtml = outro ? bloqueTextoSimple('outro', escapeHtml(truncar(outro.text, 300))) : '';
  const tldr = bloqueTldr(noticias);
  const tarjetas = bloqueNoticias(noticias);
  const clima = bloqueClima(weather, ciudad);
  const curios = bloqueCuriosidades(curious);

  const vacio = !intro && !noticias.length && !weather && !curious
    ? `
    <tr><td style="padding:24px 28px;">
      <div style="${FONT}font-size:14px;line-height:1.6;color:${C.suave};">Esta mañana no hay secciones en el boletín (posible corrida de prueba). Revisa <strong>output/</strong> o ejecuta el agente de nuevo.</div>
    </td></tr>`
    : '';

  return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZOLO Noticias — ${escapeHtml(fecha)}</title>
</head>
<body style="margin:0;padding:0;background-color:${C.fondo};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">ZOLO Noticias · ${escapeHtml(fecha)}${noticias.length ? ` · ${noticias.length} noticias` : ''}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="${C.fondo}" style="background-color:${C.fondo};">
  <tr>
    <td align="center" style="padding:24px 12px;">
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:100%;background-color:${C.fondo};border:1px solid ${C.borde};border-radius:14px;overflow:hidden;">
        ${bloqueHeader({ fecha, ciudad })}
        ${introHtml}
        ${tldr}
        ${tarjetas}
        ${clima}
        ${curios}
        ${outroHtml}
        ${vacio}
        ${bloqueFooter(hora)}
      </table>
    </td>
  </tr>
</table>
</body>
</html>`;
}

export default renderBoletinHtml;
