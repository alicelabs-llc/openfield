// ============================================================
// ZOLO NEWS — Entrega multicanal (ORQUESTADOR)
// Subagente 125-C · AliceLabs
//
// deliverAll({reportMd, reportHtml?, videoPath?, audioPath?, sections, cfg})
// → { email, telegram, whatsapp, social } — NUNCA lanza excepciones.
//
// El núcleo (subagente 125-A) consume EXACTAMENTE esta función.
// Por canal: email con nodemailer + plantilla HTML, Telegram con Bot API,
// WhatsApp con CallMeBot y sociales como adaptadores listos sin tokens.
// ============================================================

import { renderBoletinHtml, fechaLarga, horaCorta } from '../../templates/email-template.js';
import { sendEmail } from './email.js';
import { sendTelegram } from './telegram.js';
import { sendWhatsApp } from './whatsapp.js';
import { deliverSocial } from './social.js';

const TZ = 'America/Guayaquil';

// ---------- helpers de texto (seguros ante secciones vacías) ----------

function truncar(texto, max) {
  const t = String(texto ?? '').replace(/\s+/g, ' ').trim();
  if (t.length <= max) return t;
  const cortado = t.slice(0, max);
  const esp = cortado.lastIndexOf(' ');
  return (esp > max * 0.6 ? cortado.slice(0, esp) : cortado) + '…';
}

/** Escape para parse_mode HTML de Telegram (el <b> real lo añadimos nosotros). */
function escapeTg(v = '') {
  return String(v ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function primerasNoticias(sections, n = 3) {
  return (Array.isArray(sections) ? sections : [])
    .filter((s) => s?.kind === 'news')
    .slice(0, n);
}

/** Mensaje Telegram (HTML): 3 titulares + clima + curiosidad. */
export function buildTelegramMessage({ sections = [], fecha = '', cfg = {} } = {}) {
  const noticias = primerasNoticias(sections, 3);
  const clima = (Array.isArray(sections) ? sections : []).find((s) => s?.kind === 'weather');
  const curiosa = (Array.isArray(sections) ? sections : []).find((s) => s?.kind === 'curious');
  const ciudad = cfg?.city?.name || '';

  const lineas = [];
  lineas.push(`📰 <b>ZOLO Noticias${fecha ? ` — ${escapeTg(fecha)}` : ''}</b>`);
  if (noticias.length) {
    lineas.push('', '<b>🗞️ Titulares</b>');
    for (const n of noticias) {
      lineas.push(`• ${escapeTg(truncar(n.title || 'Titular', 140))}${n.source ? ` <i>(${escapeTg(n.source)})</i>` : ''}`);
      if (n.url) lineas.push(`  ${escapeTg(n.url)}`);
    }
  }
  if (clima?.text) {
    lineas.push('', `<b>🌤️ Clima${ciudad ? ` · ${escapeTg(ciudad)}` : ''}</b>`, escapeTg(truncar(clima.text, 220)));
  }
  if (curiosa?.text) {
    lineas.push('', '<b>🎲 ¿Sabías que…?</b>', escapeTg(truncar(curiosa.text, 220)));
  }
  if (!noticias.length && !clima?.text && !curiosa?.text) {
    lineas.push('', '(boletín sin secciones — corrida de prueba)');
  }
  lineas.push('', '— ZOLO · AliceLabs 🇪🇨');
  return lineas.join('\n');
}

/** Versión texto plano corta para WhatsApp (≤ maxLen chars, negrita con asteriscos). */
export function buildPlainSummary({ sections = [], fecha = '', cfg = {} } = {}, maxLen = 800) {
  const noticias = primerasNoticias(sections, 3);
  const clima = (Array.isArray(sections) ? sections : []).find((s) => s?.kind === 'weather');
  const curiosa = (Array.isArray(sections) ? sections : []).find((s) => s?.kind === 'curious');
  const ciudad = cfg?.city?.name || '';

  const lineas = [`*📰 ZOLO Noticias${fecha ? ` — ${fecha}` : ''}*`, ''];
  for (const n of noticias) {
    lineas.push(`• ${truncar(n.title || 'Titular', 120)}${n.source ? ` (${n.source})` : ''}`);
  }
  if (clima?.text) lineas.push('', `🌤️ *Clima${ciudad ? ` ${ciudad}` : ''}:* ${truncar(clima.text, 180)}`);
  if (curiosa?.text) lineas.push('', `🎲 ${truncar(curiosa.text, 180)}`);
  if (!noticias.length && !clima?.text && !curiosa?.text) {
    lineas.push('', '(boletín sin secciones — corrida de prueba)');
  }
  lineas.push('', '— ZOLO · AliceLabs');
  return truncar(lineas.join('\n'), maxLen);
}

/** Ejecuta una promesa (o función que la produce) y NUNCA deja escapar la excepción. */
async function seguro(promesa) {
  try {
    return await (typeof promesa === 'function' ? promesa() : promesa);
  } catch (e) {
    return { sent: false, error: `${e?.message || e}` };
  }
}

// ---------- orquestador principal ----------

/**
 * Entrega el boletín por todos los canales habilitados en cfg.channels.
 * @param {{reportMd:string, reportHtml?:string|null, videoPath?:string|null,
 *          audioPath?:string|null, sections:Array, cfg:object}} payload
 * @returns {Promise<{
 *   email:    {sent:boolean, skipped?:boolean, info?:string, error?:string},
 *   telegram: {sent:boolean, skipped?:boolean, info?:string, error?:string},
 *   whatsapp: {sent:boolean, skipped?:boolean, info?:string, error?:string},
 *   social:   Array<{channel:string, status:string, note?:string}>
 * }>}
 */
export async function deliverAll({ reportMd = '', reportHtml = null, videoPath = null, audioPath = null, sections = [], cfg = {} } = {}) {
  const resultado = {
    email: { sent: false, skipped: true, info: 'no procesado' },
    telegram: { sent: false, skipped: true, info: 'no procesado' },
    whatsapp: { sent: false, skipped: true, info: 'no procesado' },
    social: [],
  };

  try {
    const canales = cfg?.channels || {};
    const ahora = new Date();
    const fecha = fechaLarga(ahora);
    const hora = horaCorta(ahora);
    const subject = `📰 ZOLO Noticias — ${fecha}`;

    // HTML: el que venga del núcleo o, en su defecto, la plantilla propia.
    let html = reportHtml || '';
    if (!html) {
      try {
        html = renderBoletinHtml({ cfg, sections, date: ahora });
      } catch (e) {
        // Última línea de defensa: boletín plano en <pre>.
        html = `<!DOCTYPE html><html lang="es"><body style="background:#0f1214;color:#e6e8ea;font-family:Arial,sans-serif;padding:24px;">
<h3 style="color:#5aacd5;">📰 ZOLO Noticias — ${fecha}</h3>
<pre style="white-space:pre-wrap;color:#e6e8ea;">${String(reportMd || '(sin contenido)').replaceAll('&', '&amp;').replaceAll('<', '&lt;')}</pre>
<p style="color:#8d979f;font-size:12px;">ZOLO · AliceLabs — generado automáticamente a las ${hora}</p></body></html>`;
      }
    }

    const tgMessage = buildTelegramMessage({ sections, fecha, cfg });
    const textoPlano = buildPlainSummary({ sections, fecha, cfg }, 800);

    // ---- EMAIL ----
    resultado.email = await seguro(() => canales.email
      ? sendEmail(canales.email, { subject, html, text: textoPlano, videoPath, audioPath })
      : Promise.resolve({ sent: false, skipped: true, info: 'canal "email" ausente en config.json' }));

    // ---- TELEGRAM (texto + video si existe) ----
    resultado.telegram = await seguro(() => canales.telegram
      ? sendTelegram(canales.telegram, { message: tgMessage, documentPath: videoPath || null })
      : Promise.resolve({ sent: false, skipped: true, info: 'canal "telegram" ausente en config.json' }));

    // ---- WHATSAPP (texto corto CallMeBot) ----
    resultado.whatsapp = await seguro(() => canales.whatsapp
      ? sendWhatsApp(canales.whatsapp, { message: textoPlano })
      : Promise.resolve({ sent: false, skipped: true, info: 'canal "whatsapp" ausente en config.json' }));

    // ---- SOCIAL (facebook/instagram/tiktok — sin tokens no llama APIs) ----
    resultado.social = await seguro(() =>
      deliverSocial(canales, { sections, reportMd, videoPath, fecha, hora, tz: TZ }));
    if (!Array.isArray(resultado.social)) resultado.social = [];
  } catch (e) {
    // Red de seguridad final: NUNCA lanzar hacia el núcleo.
    const motivo = `error de orquestación: ${e?.message || e}`;
    for (const canal of ['email', 'telegram', 'whatsapp']) {
      const r = resultado[canal];
      if (!r || (!r.sent && !r.error && !r.info)) resultado[canal] = { sent: false, error: motivo };
    }
    if (!Array.isArray(resultado.social) || !resultado.social.length) {
      resultado.social = [{ channel: 'facebook', status: 'error', note: motivo }];
    }
  }

  return resultado;
}

export default deliverAll;
