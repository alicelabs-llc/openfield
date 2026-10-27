// ============================================================
// ZOLO NEWS — Guionista del noticiero (125-A)
// buildNewscast({cfg, news, weather, curiosities, mood})
//   → { sections: [...], meta: { date, mood, engine: 'llm'|'fallback' } }
// Contrato de sección (lo consumen los subagentes B y C):
//   { kind: 'intro'|'news'|'weather'|'curious'|'outro',
//     title?, text, source?, url?, imagePrompt?, caption? }
// REGLA TTS: text ≤ 600 chars por sección (news ≤ 550, intro ≤ 500,
//   caption ≤ 90). 2 intentos LLM; si fallan → plantillas de calidad.
// NUNCA devuelve null.
// ============================================================
import { toneHints } from './mood.js';

const KINDS = new Set(['intro', 'news', 'weather', 'curious', 'outro']);
const LIMIT = { text: 600, news: 550, intro: 500, caption: 90, title: 120 };

// ---------- utilidades de fecha y texto ----------
/** Partes de fecha en la timezone dada (en-CA → YYYY/MM/DD numéricos). */
export function partsInTz(tz, date = new Date()) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz ?? 'America/Guayaquil',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hour12: false,
  });
  const p = Object.fromEntries(fmt.formatToParts(date).filter((x) => x.type !== 'literal').map((x) => [x.type, x.value]));
  return p;
}

/** Clave YYYY-MM-DD del "hoy" en la timezone de la ciudad. */
export function todayKey(tz) {
  const p = partsInTz(tz);
  return `${p.year}-${p.month}-${p.day}`;
}

/** Fecha larga en español capitalizada: "Sábado, 24 de octubre de 2026". */
export function fechaLarga(tz) {
  const s = new Intl.DateTimeFormat('es-EC', {
    timeZone: tz ?? 'America/Guayaquil',
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  }).format(new Date());
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Trunca a `max` cortando por palabra y agregando '…'. */
export function truncate(text, max) {
  const t = String(text ?? '').replace(/\s+/g, ' ').trim();
  if (t.length <= max) return t;
  const cut = t.slice(0, max - 1);
  const sp = cut.lastIndexOf(' ');
  return (sp > max * 0.55 ? cut.slice(0, sp) : cut).trimEnd() + '…';
}

function capFirst(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
}

/** Extrae el primer objeto JSON de un texto (soporta fences ```json). */
export function extractJson(text) {
  if (!text) return null;
  let t = String(text).replace(/```json/gi, '```').trim();
  const fences = t.split('```');
  if (fences.length > 1) t = fences.find((s) => s.includes('{')) ?? t;
  const start = t.indexOf('{');
  const end = t.lastIndexOf('}');
  if (start === -1 || end === -1 || end <= start) return null;
  try {
    return JSON.parse(t.slice(start, end + 1));
  } catch {
    return null;
  }
}

// ---------- prompts ----------
function systemPrompt(cfg, mood, hints) {
  return [
    `Eres el guionista de ZOLO Noticias, el noticiero matutino personal de ${cfg.user.name}, se emite en ${cfg.city.name}, Ecuador.`,
    'Escribes guiones para ser LOCUTADOS en voz alta por un presentador IA: frases cortas, naturales, en español de Ecuador, cero tecnicismos innecesarios, cero markdown.',
    '',
    'REGLAS ESTRICTAS:',
    '1. Responde ÚNICAMENTE con JSON válido, sin markdown ni explicaciones, con esta forma exacta: {"sections":[ ... ]}',
    '2. Cada sección es un objeto con "kind" y "text"; opcionalmente "title", "source", "url", "caption", "imagePrompt".',
    '3. Orden EXACTO de secciones: una "intro"; luego UNA sección "news" POR CADA noticia, en el mismo orden en que te las entrego; luego "weather"; luego "curious"; y cierras con "outro".',
    '4. Límites de caracteres por "text": intro ≤ 500, news ≤ 550, weather/curious/outro ≤ 600. Nada de listas con viñetas ni emojis dentro de "text".',
    '5. Sección "news": "title" es un titular corto (máx 90 caracteres, no copies el titular completo si es larguísimo), "source" y "url" cópialos TAL CUAL de la noticia, "caption" es una frase para video de máximo 90 caracteres, "imagePrompt" es un prompt visual EN INGLÉS con la forma "editorial photograph about {tema}, no text in image".',
    '6. Sección "weather": menciona temperatura actual, máxima y mínima, probabilidad de lluvia y UN consejo práctico en lenguaje natural.',
    '7. Sección "curious": abre con "Tal día como hoy" usando los eventos entregados, integra el dato/chiste y la frase del día; si hay precios de cripto, menciónalos al final en USD.',
    `8. Humor del día: ${mood} (${hints.estilo}). ${hints.instruccion}`,
    '9. NO inventes datos: usa exclusivamente la información entregada. Naturaliza los titulares para habla: no los recites literalmente.',
    '10. En "intro" saluda por el nombre, menciona la fecha larga y anticipa de qué hablarás. En "outro" despídete por el nombre y firma "ZOLO Noticias".',
  ].join('\n');
}

function userPrompt({ cfg, news, weather, curiosities, mood, fecha }) {
  const payload = {
    fecha,
    nombre: cfg.user.name,
    ciudad: `${cfg.city.name} (lat ${cfg.city.lat}, lon ${cfg.city.lon})`,
    humor: mood,
    clima: {
      ciudad: weather.city,
      condicion: weather.condition,
      temp: weather.temp,
      sensacion: weather.feelsLike,
      max: weather.max,
      min: weather.min,
      probabilidad_lluvia: weather.rainProb,
      humedad: weather.humidity,
      viento_kmh: weather.wind,
      consejo: weather.advice,
    },
    noticias: (news?.items ?? []).map((it, i) => ({
      indice: i + 1,
      titular: it.title,
      fuente: it.source,
      url: it.url,
      fecha_publicacion: it.published,
      resumen: it.summary || '',
    })),
    curiosidades: {
      tal_dia_como_hoy: curiosities.onThisDay,
      chiste_o_dato: curiosities.joke || null,
      frase_del_dia: curiosities.quote || null,
      cripto_usd: curiosities.crypto ?? null,
    },
  };
  return (
    'Datos reales de hoy para el guion (JSON):\n' +
    JSON.stringify(payload, null, 1) +
    '\n\nGenera SOLO el JSON {"sections":[...]} con todas las secciones en orden: intro, ' +
    `${payload.noticias.length} secciones news (una por noticia, en orden), weather, curious, outro.`
  );
}

// ---------- normalización / validación ----------
/** Valida y normaliza las secciones del LLM. Devuelve array o null. */
export function validateSections(arr, newsItems) {
  if (!Array.isArray(arr) || arr.length < 3) return null;
  const out = [];
  const newsCount = arr.filter((s) => s && s.kind === 'news').length;

  for (const s of arr) {
    if (!s || typeof s !== 'object') return null;
    const kind = String(s.kind ?? '').toLowerCase().trim();
    if (!KINDS.has(kind)) return null;
    const text = String(s.text ?? '').replace(/\s+/g, ' ').trim();
    if (!text) return null;

    const maxText = kind === 'news' ? LIMIT.news : kind === 'intro' ? LIMIT.intro : LIMIT.text;
    const sec = { kind, text: truncate(text, maxText) };

    if (kind === 'news') {
      sec.title = truncate(String(s.title ?? '').trim() || 'Noticia del día', LIMIT.title);
      if (s.source) sec.source = truncate(String(s.source), 80);
      if (s.url && /^https?:\/\//i.test(String(s.url))) sec.url = String(s.url).trim();
      if (s.caption) sec.caption = truncate(String(s.caption), LIMIT.caption);
      if (s.imagePrompt) sec.imagePrompt = String(s.imagePrompt).trim().slice(0, 300);
    } else {
      if (s.title) sec.title = truncate(String(s.title), LIMIT.title);
    }
    out.push(sec);
  }

  const kinds = out.map((s) => s.kind);
  if (!kinds.includes('intro') || !kinds.includes('outro')) return null;
  if (!kinds.includes('weather') && !kinds.includes('news')) return null;

  // Relleno de metadatos faltantes en news usando el orden de newsItems.
  let idx = 0;
  for (const sec of out) {
    if (sec.kind !== 'news') continue;
    const it = (newsItems ?? [])[idx] ?? (newsItems ?? [])[idx - 1];
    idx++;
    if (!it) continue;
    if (!sec.source && it.source) sec.source = it.source;
    if (!sec.url && it.url) sec.url = it.url;
    if (!sec.caption) sec.caption = truncate(it.title, LIMIT.caption);
    if (!sec.imagePrompt) {
      const tema = truncate(String(it.title ?? 'noticias del día'), 120);
      sec.imagePrompt = `editorial photograph about ${tema}, no text in image`;
    }
  }

  // Si el LLM devolvió más news de las que hay, se recortan (cuenta con sentido).
  if (newsCount > (newsItems?.length ?? 0) && (newsItems?.length ?? 0) > 0) {
    return null; // desalineación grave: preferimos el fallback determinista
  }
  return out;
}

// ---------- fallback determinista ----------
const INTRO_MOOD = {
  feliz: (n, f, c) => `¡Buenos días, ${n}! Hoy amanece ${c} con ganas de fiesta: es ${f}. Te cuento lo que necesitas para arrancar sonriendo.`,
  neutral: (n, f, c) => `Buenos días, ${n}. Hoy es ${f} y arrancamos tu día con lo más importante en ${c} y el mundo.`,
  serio: (n, f, c) => `Buenos días, ${n}. Informe matutino del ${f}. La información clave de ${c} y el mundo, directo al grano.`,
  motivado: (n, f, c) => `¡Despierta, ${n}! Es ${f} y el día está servido para conquistarlo. Esto es ZOLO Noticias desde ${c}.`,
  bajoneado: (n, f, c) => `Buenos días, ${n}. Hoy es ${f}. Vamos con calma: te acompaño con las noticias y algo de cariño para empezar suave.`,
};

const OUTRO_MOOD = {
  feliz: (n) => `¡Y hasta aquí la emisión, ${n}! Gracias por este rato contigo. Te leo mañana con más noticias. Esto fue ZOLO Noticias.`,
  neutral: (n) => `Eso fue todo por hoy, ${n}. Gracias por escuchar; mañana más noticias a primera hora. Esto fue ZOLO Noticias.`,
  serio: (n) => `Fin del informe, ${n}. Quedaste al día con lo esencial. Mañana más. Esto fue ZOLO Noticias.`,
  motivado: (n) => `¡Y con esa energía, ${n}, a romperla hoy! Recuerda: los días grandes empiezan bien informados. Esto fue ZOLO Noticias.`,
  bajoneado: (n) => `Y hasta aquí por hoy, ${n}. Recuerda que no tienes que estar perfecto, solo seguir. Aquí estaré mañana. Esto fue ZOLO Noticias.`,
};

/** Guion determinista con plantillas de calidad en español (motor 'fallback'). */
export function buildFallbackScript({ cfg, news, weather, curiosities, mood }) {
  const fecha = fechaLarga(cfg.city.timezone);
  const nombre = cfg.user.name;
  const ciudad = cfg.city.name;
  const sections = [];

  const introTpl = INTRO_MOOD[mood] ?? INTRO_MOOD.neutral;
  sections.push({ kind: 'intro', title: 'Apertura', text: truncate(introTpl(nombre, fecha, ciudad), LIMIT.intro) });

  for (const it of news?.items ?? []) {
    const limpio = String(it.title ?? '').replace(/\s+-\s+[^-]{2,30}$/, '').trim() || it.title; // quita " - Fuente" de Google News
    const fuenteTxt = it.source ? ` Lo cuenta ${it.source}.` : '';
    const cuerpo = it.summary && it.summary.length > 40 ? `${capFirst(it.summary)}${fuenteTxt}` : `${limpio}.${fuenteTxt}`;
    sections.push({
      kind: 'news',
      title: truncate(limpio, LIMIT.title),
      text: truncate(cuerpo, LIMIT.news),
      ...(it.source ? { source: it.source } : {}),
      ...(it.url ? { url: it.url } : {}),
      caption: truncate(limpio, LIMIT.caption),
      imagePrompt: `editorial photograph about ${truncate(limpio, 120)}, no text in image`,
    });
  }

  const w = weather ?? {};
  const weatherText = w.degraded
    ? `En clima de ${ciudad} tuve problemas técnicos para consultar los datos, pero el consejo de siempre vale: hidrátate y sal con actitud.`
    : `En clima de ${ciudad}: ${w.condition ?? 'variable'}, ${w.temp ?? '?'} grados ahora, máxima ${w.max ?? '?'} y mínima ${w.min ?? '?'}. ` +
      `Probabilidad de lluvia ${Number.isFinite(w.rainProb) ? w.rainProb + ' por ciento' : 'sin dato'}. ${w.advice ?? ''}`;
  sections.push({ kind: 'weather', title: `Clima en ${ciudad}`, text: truncate(weatherText, LIMIT.text) });

  const bits = [];
  const otd = curiosities?.onThisDay ?? [];
  if (otd.length) {
    const evs = otd.slice(0, 2).map((e) => `en ${e.year}, ${e.text}`).join('; ');
    bits.push(`Tal día como hoy: ${evs}.`);
  }
  if (curiosities?.joke) bits.push(curiosities.joke);
  if (curiosities?.quote) bits.push(`Y la frase del día: ${curiosities.quote}`);
  if (Array.isArray(curiosities?.crypto) && curiosities.crypto.length) {
    bits.push(`Cripto del día: ${curiosities.crypto.map((c) => `${c.symbol} a ${c.price_usd} dólares`).join(' y ')}.`);
  }
  const curiousText = bits.length ? bits.join(' ') : 'Hoy el archivo de curiosidades está en blanco, pero el día apenas empieza: haz tú la historia.';
  sections.push({ kind: 'curious', title: 'Curiosidades', text: truncate(curiousText, LIMIT.text) });

  const outroTpl = OUTRO_MOOD[mood] ?? OUTRO_MOOD.neutral;
  sections.push({ kind: 'outro', title: 'Despedida', text: truncate(outroTpl(nombre), LIMIT.text) });

  return sections;
}

// ---------- LLM ----------
async function llmAttempt(userMsg, cfg, mood) {
  const mod = await import('z-ai-web-dev-sdk');
  const ZAI = mod.default ?? mod;
  const zai = await ZAI.create();
  const completion = await zai.chat.completions.create({
    messages: [
      { role: 'assistant', content: systemPrompt(cfg, mood, toneHints(mood)) },
      { role: 'user', content: userMsg },
    ],
    thinking: { type: 'disabled' },
  });
  const text = completion?.choices?.[0]?.message?.content;
  if (!text || !text.trim()) throw new Error('respuesta vacía del LLM');
  const parsed = extractJson(text);
  if (!parsed) throw new Error('el LLM no devolvió JSON parseable');
  return parsed;
}

// ---------- API principal ----------
/**
 * Construye el newscast completo.
 * @returns {Promise<{sections:Array, meta:{date:string, mood:string, engine:'llm'|'fallback', note?:string}}>}
 */
export async function buildNewscast({ cfg, news, weather, curiosities, mood }) {
  const date = todayKey(cfg.city.timezone);
  const userMsg = userPrompt({ cfg, news, weather, curiosities, mood, fecha: fechaLarga(cfg.city.timezone) });

  let lastErr = null;
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const parsed = await llmAttempt(userMsg, cfg, mood);
      const sections = validateSections(parsed?.sections, news?.items ?? []);
      if (sections) {
        return { sections, meta: { date, mood, engine: 'llm', attempts: attempt } };
      }
      lastErr = new Error('JSON recibido no cumple el contrato de secciones');
    } catch (err) {
      lastErr = err;
    }
  }

  const sections = buildFallbackScript({ cfg, news, weather, curiosities, mood });
  return { sections, meta: { date, mood, engine: 'fallback', note: `LLM falló 2 veces: ${lastErr?.message ?? lastErr}` } };
}

export default { buildNewscast, buildFallbackScript };
