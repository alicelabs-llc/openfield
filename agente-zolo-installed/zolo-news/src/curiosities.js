// ============================================================
// ZOLO NEWS — Curiosidades (125-A)
// - onThisDay: Wikipedia ES "tal día como hoy" (REST feed, sin key)
// - crypto: CoinGecko simple/price (BTC, ETH) si cfg.features.crypto
// - joke + quote: UNA llamada al LLM (2 intentos) adaptada al mood;
//   fallbacks estáticos en español si el LLM falla o el JSON no parsea.
// RESILIENCIA: cada pieza falla en silencio (vacío/undefined), el run sigue.
// ============================================================
import { toneHints } from './mood.js';

const UA = 'ZOLO-News/1.0 (agente personal; contacto: founder)';
// Wikimedia exige UA con contacto explícito (política de User-Agent) — sin esto devuelve 403.
const UA_WIKI = 'ZOLO-News/1.0 (https://alicelabs.site; contacto@alicelabs.energy) zolo-news-agent';
const TIMEOUT_MS = 10_000;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** {mm, dd} con ceros, en la timezone de la ciudad. */
export function todayMMDD(tz) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz ?? 'America/Guayaquil',
    month: '2-digit',
    day: '2-digit',
  });
  const p = Object.fromEntries(fmt.formatToParts(new Date()).filter((x) => x.type !== 'literal').map((x) => [x.type, x.value]));
  return { mm: p.month, dd: p.day };
}

/** fetch JSON con timeout; lanza en error HTTP. */
async function fetchJson(url, userAgent = UA) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(new Error('timeout 10s')), TIMEOUT_MS);
  try {
    const res = await fetch(url, { signal: ctrl.signal, headers: { 'User-Agent': userAgent, Accept: 'application/json' } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

// ---------- onThisDay (Wikipedia ES) ----------
/**
 * 2-3 eventos históricos del día, preferiendo año >= 1900.
 * Devuelve [] ante cualquier fallo.
 */
export async function getOnThisDay(tz) {
  try {
    const { mm, dd } = todayMMDD(tz);
    const data = await fetchJson(`https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/${mm}/${dd}`, UA_WIKI);
    const events = Array.isArray(data?.events) ? data.events : [];
    const clean = events
      .filter((e) => e && Number.isFinite(Number(e.year)) && typeof e.text === 'string' && e.text.trim())
      .map((e) => ({ year: Number(e.year), text: String(e.text).replace(/\s+/g, ' ').trim() }));

    const modern = clean.filter((e) => e.year >= 1900).sort((a, b) => a.year - b.year);
    const older = clean.filter((e) => e.year < 1900).sort((a, b) => b.year - a.year);

    const picked = [];
    if (modern.length >= 3) {
      // 3 eventos repartidos en el siglo XX-XXI (primero, medio, último).
      picked.push(modern[0], modern[Math.floor(modern.length / 2)], modern[modern.length - 1]);
    } else {
      picked.push(...modern.slice(0, 2), ...older.slice(0, 3 - Math.min(modern.length, 2)));
    }
    // Deduplicar y dejar 3 máximo (2 si el guionista necesita aire).
    const seen = new Set();
    return picked.filter((e) => {
      const k = `${e.year}|${e.text.slice(0, 40)}`;
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    }).slice(0, 3);
  } catch {
    return [];
  }
}

// ---------- crypto (CoinGecko) ----------
const COINS = [
  { id: 'bitcoin', symbol: 'BTC' },
  { id: 'ethereum', symbol: 'ETH' },
];

/** [{symbol, price_usd}] o undefined si falla o está desactivado. */
export async function getCrypto(cfg) {
  if (cfg?.features?.crypto === false) return undefined;
  try {
    const ids = COINS.map((c) => c.id).join(',');
    const data = await fetchJson(`https://api.coingecko.com/api/v3/simple/price?ids=${ids}&vs_currencies=usd`);
    const out = COINS
      .map((c) => {
        const price = data?.[c.id]?.usd;
        return Number.isFinite(Number(price)) ? { symbol: c.symbol, price_usd: Math.round(Number(price)) } : null;
      })
      .filter(Boolean);
    return out.length ? out : undefined;
  } catch {
    return undefined;
  }
}

// ---------- joke + quote (LLM, 1 llamada, 2 intentos) ----------
/** Fallbacks estáticos en español por mood (sin humor negro en bajoneado). */
const FALLBACK_HUMOR = {
  feliz: {
    joke: '¿Qué hace una abeja en el gimnasio? ¡Zumbando! 🐝',
    quote: '"La felicidad no es algo hecho. Viene de tus propias acciones" — Dalai Lama',
  },
  neutral: {
    joke: 'Dato: los pulpos tienen tres corazones y sangre azul. La naturaleza también hace ingeniería exagerada.',
    quote: '"El mejor momento para plantar un árbol fue hace 20 años; el segundo mejor es ahora" — proverbio chino',
  },
  serio: {
    joke: 'Dato sobrio: un día en Venus dura más que un año en Venus. Todo depende desde dónde se mire.',
    quote: '"El conocimiento habla, pero la sabiduría escucha" — Jimi Hendrix',
  },
  motivado: {
    joke: 'Dato: el bambú tarda años echando raíces y luego crece varios metros en semanas. Sigue regando lo tuyo.',
    quote: '"No cuentes los días, haz que los días cuenten" — Muhammad Ali',
  },
  bajoneado: {
    joke: 'Dato tierno: las nutrias marinas se toman de las manos al dormir para no separarse. Alguien siempre te sostiene. 🦦',
    quote: '"Las tormentas enseñan a los árboles a tener raíces más fuertes" — proverbio popular',
  },
};

/** Extrae el primer objeto JSON de un texto (soporta ```json ... ```). */
export function extractJson(text) {
  if (!text) return null;
  let t = String(text).replace(/```json/gi, '```').trim();
  const fence = t.split('```');
  if (fence.length > 1) t = fence.find((s) => s.includes('{')) ?? t;
  const start = t.indexOf('{');
  const end = t.lastIndexOf('}');
  if (start === -1 || end === -1 || end <= start) return null;
  try {
    return JSON.parse(t.slice(start, end + 1));
  } catch {
    return null;
  }
}

async function llmCallOnce(mood) {
  const mod = await import('z-ai-web-dev-sdk');
  const ZAI = mod.default ?? mod;
  const zai = await ZAI.create();
  const hints = toneHints(mood);
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content:
          'Eres el escritor de curiosidades de ZOLO Noticias, un noticiero matutino en español de Ecuador. ' +
          'Respondes ÚNICAMENTE con un objeto JSON válido, sin markdown ni texto extra: {"joke":"...","quote":"..."}. ' +
          '"joke" es un chiste corto y apropiado O un dato curioso sorprendente (máx 220 caracteres). ' +
          '"quote" es una frase del día inspiradora con autor en el formato «frase» — Autor (máx 180 caracteres). ' +
          'Nada ofensivo, nada de humor negro.',
      },
      {
        role: 'user',
        content:
          `Estilo solicitado: ${hints.estilo}. ${hints.instruccion}\n` +
          'Genera el JSON con un chiste/dato y una frase del día para esta mañana.',
      },
    ],
    thinking: { type: 'disabled' },
  });
  const text = completion?.choices?.[0]?.message?.content;
  const obj = extractJson(text);
  if (obj && typeof obj.joke === 'string' && obj.joke.trim() && typeof obj.quote === 'string' && obj.quote.trim()) {
    return { joke: obj.joke.trim().slice(0, 300), quote: obj.quote.trim().slice(0, 240) };
  }
  throw new Error('JSON de humor inválido o incompleto');
}

/** joke + quote con 2 intentos LLM y fallback estático garantizado. */
export async function getJokeQuote(mood) {
  let lastErr = null;
  for (let i = 0; i < 2; i++) {
    try {
      return await llmCallOnce(mood);
    } catch (err) {
      lastErr = err;
      await sleep(700);
    }
  }
  const fb = FALLBACK_HUMOR[mood] ?? FALLBACK_HUMOR.neutral;
  return { ...fb, fallback: true, error: String(lastErr?.message ?? lastErr) };
}

// ---------- API principal ----------
/**
 * @param {object} cfg
 * @param {string} mood
 * @returns {Promise<{onThisDay: Array<{year:number,text:string}>, joke: string, quote: string, crypto?: Array<{symbol:string,price_usd:number}>, sources: object}>}
 */
export async function getCuriosities(cfg, mood) {
  const feats = cfg?.features ?? {};
  const tz = cfg?.city?.timezone;

  const [otdRes, cryptoRes, humorRes] = await Promise.allSettled([
    feats.onThisDay === false ? Promise.resolve([]) : getOnThisDay(tz),
    getCrypto(cfg),
    feats.joke === false && feats.quote === false ? Promise.resolve(FALLBACK_HUMOR[mood] ?? FALLBACK_HUMOR.neutral) : getJokeQuote(mood),
  ]);

  const onThisDay = otdRes.status === 'fulfilled' ? otdRes.value : [];
  const crypto = cryptoRes.status === 'fulfilled' ? cryptoRes.value : undefined;
  let humor =
    humorRes.status === 'fulfilled'
      ? humorRes.value
      : { ...(FALLBACK_HUMOR[mood] ?? FALLBACK_HUMOR.neutral), fallback: true };

  // Si una feature está desactivada, el bloque correspondiente se vacía.
  if (feats.joke === false) humor.joke = '';
  if (feats.quote === false) humor.quote = '';

  return {
    onThisDay,
    joke: humor.joke ?? '',
    quote: humor.quote ?? '',
    ...(crypto ? { crypto } : {}),
    sources: {
      wikipedia: onThisDay.length > 0,
      coingecko: Array.isArray(crypto) && crypto.length > 0,
      llmHumor: !humor.fallback,
    },
  };
}

export default { getCuriosities };
