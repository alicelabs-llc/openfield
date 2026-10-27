// ============================================================
// ZOLO NEWS — Canal TELEGRAM (Bot API oficial)
// Subagente 125-C · AliceLabs
//
// sendTelegram(channelCfg, {message, documentPath?})
// → {sent, skipped?, info?, error?} — NUNCA lanza excepciones.
//
// - sendMessage: POST JSON https://api.telegram.org/bot<token>/sendMessage
//   con chat_id, text en parse_mode HTML y disable_web_page_preview:false.
//   ⚠️ El texto debe llegar YA escapado en HTML (deliverAll lo hace).
// - sendDocument: FormData + Blob nativos (Node ≥ 20) con el video.
// - Regla de skip: enabled !== true o token/chat_id placeholder.
// ============================================================

import fs from 'node:fs';

const MB = 1024 * 1024;
const MAX_DOC = 50 * MB; // límite de la Bot API para sendDocument

const SKIP = 'telegram no configurado — ver docs/CANALES.md';

function esPlaceholder(valor) {
  const v = String(valor ?? '').trim();
  if (!v) return true;
  return /TOKEN_DEL_BOT/i.test(v) || /TU_CHAT_ID/i.test(v) || v.toUpperCase() === 'TOKEN';
}

/**
 * Envía el mensaje (y opcionalmente el video) a Telegram.
 * @param {object} channelCfg - cfg.channels.telegram ({enabled, botToken, chatId})
 * @param {{message:string, documentPath?:string|null, documentName?:string}} opts
 * @returns {Promise<{sent:boolean, skipped?:boolean, info?:string, error?:string}>}
 */
export async function sendTelegram(channelCfg, { message, documentPath = null, documentName = 'bulletin.mp4' } = {}) {
  try {
    if (!channelCfg || channelCfg.enabled !== true) {
      return { sent: false, skipped: true, info: SKIP };
    }
    const token = String(channelCfg.botToken ?? '').trim();
    const chatId = String(channelCfg.chatId ?? '').trim();
    if (esPlaceholder(token) || token.length < 20) return { sent: false, skipped: true, info: SKIP };
    if (esPlaceholder(chatId)) return { sent: false, skipped: true, info: SKIP };

    // ---- 1) sendMessage (texto del boletín, HTML) ----
    const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: String(message ?? '').slice(0, 4000), // límite Bot API: 4096
        parse_mode: 'HTML',
        disable_web_page_preview: false,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || data.ok !== true) {
      return { sent: false, error: `telegram sendMessage falló (HTTP ${res.status}): ${data.description || 'sin detalle'}` };
    }

    // ---- 2) sendDocument (video bulletin.mp4) si existe ----
    let extra = '';
    if (documentPath) {
      try {
        if (!fs.existsSync(documentPath)) {
          extra = ' (documento omitido: no existe)';
        } else {
          const size = fs.statSync(documentPath).size;
          if (size >= MAX_DOC) {
            extra = ` (documento omitido: pesa ${(size / MB).toFixed(1)} MB ≥ 50 MB)`;
          } else {
            // FormData + Blob nativos de Node (sin dependencias externas)
            const buf = fs.readFileSync(documentPath);
            const fd = new FormData();
            fd.append('chat_id', chatId);
            fd.append('caption', 'ZOLO Noticias · video del día');
            fd.append('document', new Blob([buf], { type: 'video/mp4' }), documentName);
            const res2 = await fetch(`https://api.telegram.org/bot${token}/sendDocument`, {
              method: 'POST',
              body: fd, // fetch añade el multipart boundary automáticamente
            });
            const data2 = await res2.json().catch(() => ({}));
            extra = (res2.ok && data2.ok === true)
              ? ' + video entregado'
              : ` (video NO enviado: ${data2.description || `HTTP ${res2.status}`})`;
          }
        }
      } catch (e) {
        extra = ` (video falló: ${e?.message || e})`; // el texto ya fue entregado; no marca fallo total
      }
    }

    return { sent: true, info: `mensaje entregado a chat ${chatId}${extra}` };
  } catch (e) {
    return { sent: false, error: `telegram: ${e?.message || e}` };
  }
}

export default sendTelegram;
