// ============================================================
// ZOLO NEWS — Canal WHATSAPP (CallMeBot API gratuita)
// Subagente 125-C · AliceLabs
//
// sendWhatsApp(channelCfg, {message})
// → {sent, skipped?, info?, error?} — NUNCA lanza excepciones.
//
// GET https://api.callmebot.com/whatsapp.php?phone=<phone>&text=<encodeURIComponent(text)>&apikey=<key>
// - El mensaje llega como texto plano corto (≤ 800 chars, lo arma deliverAll).
// - Regla de skip: enabled !== true o phone/apikey placeholder.
// - Proceso de activación: docs/CANALES.md §WhatsApp.
// ============================================================

const SKIP = 'whatsapp no configurado — ver docs/CANALES.md';

/**
 * Envía el mensaje por WhatsApp vía CallMeBot.
 * @param {object} channelCfg - cfg.channels.whatsapp ({enabled, phone, apikey})
 * @param {{message:string}} opts - texto plano corto (≤ 800 chars recomendado)
 * @returns {Promise<{sent:boolean, skipped?:boolean, info?:string, error?:string}>}
 */
export async function sendWhatsApp(channelCfg, { message = '' } = {}) {
  try {
    if (!channelCfg || channelCfg.enabled !== true) {
      return { sent: false, skipped: true, info: SKIP };
    }
    const phone = String(channelCfg.phone ?? '').trim();
    const apikey = String(channelCfg.apikey ?? '').trim();

    // phone debe ser internacional solo dígitos (p.ej. 593999123456); el placeholder
    // "5939XXXXXXXX" contiene letras → inválido.
    const phoneValido = /^\d{10,15}$/.test(phone);
    const keyValida = apikey && !/CLAVE_CALLMEBOT/i.test(apikey) && apikey.length >= 4;
    if (!phoneValido || !keyValida) return { sent: false, skipped: true, info: SKIP };

    // CallMeBot recomienda ≤ 800 chars; entregamos recortado por seguridad.
    const texto = String(message).slice(0, 800);
    const url = `https://api.callmebot.com/whatsapp.php?phone=${encodeURIComponent(phone)}&text=${encodeURIComponent(texto)}&apikey=${encodeURIComponent(apikey)}`;

    const res = await fetch(url);
    const cuerpo = (await res.text()).slice(0, 300);
    if (!res.ok || /ERROR/i.test(cuerpo)) {
      return { sent: false, error: `whatsapp: CallMeBot respondió HTTP ${res.status}: ${cuerpo || 'sin cuerpo'}` };
    }
    return { sent: true, info: `mensaje entregado a +${phone} vía CallMeBot` };
  } catch (e) {
    return { sent: false, error: `whatsapp: ${e?.message || e}` };
  }
}

export default sendWhatsApp;
