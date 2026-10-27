// ============================================================
// ZOLO NEWS — Canal EMAIL (SMTP vía nodemailer)
// Subagente 125-C · AliceLabs
//
// sendEmail(channelCfg, {subject, html, attachments?, videoPath?, audioPath?, text?})
// → {sent, skipped?, info?, error?} — NUNCA lanza excepciones.
//
// Reglas de skip (documentadas en docs/CANALES.md):
//  - enabled !== true → skip
//  - credenciales placeholder ("TU_CORREO", "APP_PASSWORD") → skip
//  - adjuntos > 25 MB → se omiten y se anota en info
// ============================================================

import nodemailer from 'nodemailer';
import fs from 'node:fs';

const MB = 1024 * 1024;
const MAX_ADJUNTO = 25 * MB; // límite razonable para correo (Gmail admite 25 MB en total)

const PLACEHOLDERS = ['TU_CORREO', 'APP_PASSWORD', 'TU_CORREO@GMAIL.COM'];

function esPlaceholder(valor) {
  const v = String(valor ?? '').trim().toUpperCase();
  if (!v) return true;
  return PLACEHOLDERS.some((p) => v === p || v.includes(p));
}

/**
 * Prepara los adjuntos (video bulletin.mp4 y audio bulletin.mp3).
 * Omite los que no existan o superen 25 MB; anota el motivo en `notas`.
 */
function prepararAdjuntos({ videoPath, audioPath }, notas) {
  const adjuntos = [];
  const pares = [
    [videoPath, 'bulletin.mp4'],
    [audioPath, 'bulletin.mp3'],
  ];
  for (const [ruta, nombre] of pares) {
    if (!ruta) continue;
    try {
      if (!fs.existsSync(ruta)) {
        notas.push(`adjunto omitido (no existe): ${nombre}`);
        continue;
      }
      const size = fs.statSync(ruta).size;
      if (size >= MAX_ADJUNTO) {
        notas.push(`adjunto omitido (pesa ${(size / MB).toFixed(1)} MB ≥ 25 MB): ${nombre}`);
        continue;
      }
      adjuntos.push({ filename: nombre, path: ruta });
    } catch (e) {
      notas.push(`adjunto omitido (error: ${e?.message || e}): ${nombre}`);
    }
  }
  return adjuntos;
}

/**
 * Envía el boletín por correo.
 * @param {object} channelCfg - cfg.channels.email ({enabled, smtp:{host,port,secure,user,pass}, to})
 * @param {{subject:string, html:string, attachments?:Array, videoPath?:string|null, audioPath?:string|null, text?:string}} opts
 * @returns {Promise<{sent:boolean, skipped?:boolean, info?:string, error?:string}>}
 */
export async function sendEmail(channelCfg, { subject, html, attachments = null, videoPath = null, audioPath = null, text = '' } = {}) {
  try {
    if (!channelCfg || channelCfg.enabled !== true) {
      return { sent: false, skipped: true, info: 'correo no configurado — ver docs/CANALES.md' };
    }
    const smtp = channelCfg.smtp || {};
    if (!smtp.user || !smtp.pass || esPlaceholder(smtp.user) || esPlaceholder(smtp.pass)) {
      return { sent: false, skipped: true, info: 'correo no configurado — ver docs/CANALES.md' };
    }

    const notas = [];
    const adjuntos = Array.isArray(attachments) && attachments.length
      ? attachments
      : prepararAdjuntos({ videoPath, audioPath }, notas);

    const transport = nodemailer.createTransport({
      host: smtp.host || 'smtp.gmail.com',
      port: Number(smtp.port) || 465,
      secure: smtp.secure !== false, // 465 = TLS implícito
      auth: { user: smtp.user, pass: smtp.pass },
    });

    const destinatario = channelCfg.to || smtp.user;
    const info = await transport.sendMail({
      from: `"ZOLO Noticias" <${smtp.user}>`,
      to: destinatario,
      subject,
      html,
      text: text || undefined,
      attachments: adjuntos,
    });

    const base = `entregado a ${destinatario} (${info?.messageId || 'sin messageId'})`;
    return { sent: true, info: notas.length ? `${base}; ${notas.join('; ')}` : base };
  } catch (e) {
    return { sent: false, error: `email: ${e?.message || e}` };
  }
}

export default sendEmail;
