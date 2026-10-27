#!/usr/bin/env node
// ============================================================
// ZOLO NEWS — Complemento MCP para GPT o cualquier IA
// Subagente 125-C · AliceLabs (Ecuador)
//
// Servidor MCP estándar sobre stdio (Model Context Protocol).
// Claude Desktop, Cursor, Windsurf, Zed, VS Code Copilot o cualquier
// cliente MCP puede llamarlo; ChatGPT consume el equivalente HTTP
// (ver docs/INTEGRACION-GPT.md).
//
// EJECUCIÓN:  node src/mcp/server.js   (o `npm run mcp`)
//             NO se editó package.json: no hay bin entry, se documenta.
//
// ⚠️ stdout es SOLO del protocolo JSON-RPC; cualquier log va a stderr.
//
// Herramientas (4):
//   zolo_get_news    {limit?, topic?}  → noticias frescas ahora mismo
//   zolo_get_weather {city?}           → clima actual de cfg.city
//   zolo_get_bulletin{mood?}           → boletín completo de HOY (o al vuelo)
//   zolo_set_mood    {mood}            → tono del boletín de mañana
//
// Los módulos del núcleo (src/news.js, src/weather.js, src/mood.js,
// src/config.js, src/scriptWriter.js — del subagente 125-A) se importan
// DINÁMICAMENTE con await import + try/catch: si aún no existen o fallan,
// las tools responden "ERROR: núcleo no disponible: <motivo>".
// ============================================================

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const CONFIG_PATH = path.join(PROJECT_ROOT, 'config.json');
const TZ = 'America/Guayaquil';
const MOODS_POR_DEFECTO = ['feliz', 'neutral', 'serio', 'motivado', 'bajoneado'];

// ============================================================
// Utilidades de fecha (America/Guayaquil)
// ============================================================

/** Fecha de HOY en Ecuador como "YYYY-MM-DD". */
function hoyGuayaquil() {
  const partes = new Intl.DateTimeFormat('en-CA', {
    year: 'numeric', month: '2-digit', day: '2-digit', timeZone: TZ,
  }).format(new Date()); // en-CA → YYYY-MM-DD
  return partes;
}

/** Fecha larga en español: "Sábado 24 de octubre de 2026". */
function fechaLargaGuayaquil(date = new Date()) {
  const s = new Intl.DateTimeFormat('es-EC', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: TZ,
  }).format(date);
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Fecha corta para titulares de noticias: "24 oct, 06:30". */
function fechaCorta(valor) {
  const d = new Date(valor);
  if (isNaN(d.getTime())) return String(valor ?? '').trim();
  return new Intl.DateTimeFormat('es-EC', {
    day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: TZ,
  }).format(d);
}

// ============================================================
// Carga resiliente de módulos del núcleo (subagente 125-A)
// ============================================================

/** Prueba varias rutas/nombres de export y devuelve la primera función encontrada. */
async function importarFn(rutas, nombres, etiqueta) {
  const motivos = [];
  for (const ruta of rutas) {
    let mod;
    try {
      mod = await import(ruta);
    } catch (e) {
      motivos.push(`${ruta}: ${e?.message || e}`);
      continue;
    }
    for (const nombre of nombres) {
      if (typeof mod?.[nombre] === 'function') return { fn: mod[nombre], nombre, mod };
    }
    motivos.push(`${ruta}: no exporta ${nombres.join('/')}`);
  }
  throw new Error(`núcleo no disponible: ${etiqueta} — ${motivos.join(' | ')}`);
}

/**
 * Llama a una función del núcleo probando varias formas de argumento,
 * porque su firma exacta se define en paralelo (125-A). Devuelve el primer
 * resultado no-undefined; si todas fallan, lanza el último error.
 */
async function llamarConVariantes(fn, variantes) {
  let ultimoError;
  for (const args of variantes) {
    try {
      const r = await fn(...args);
      if (r !== undefined) return r;
      ultimoError = new Error('la función devolvió undefined');
    } catch (e) {
      ultimoError = e;
    }
  }
  throw ultimoError || new Error('llamada sin variantes');
}

/** Carga cfg desde ../config.js del núcleo; si aún no existe, lee config.json directo. */
async function loadCfg() {
  try {
    const mod = await import('../config.js');
    if (typeof mod?.loadConfig === 'function') {
      const cfg = await mod.loadConfig();
      if (cfg && typeof cfg === 'object') return cfg;
    }
  } catch { /* núcleo aún no disponible → fallback abajo */ }
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch (e) {
    throw new Error(`núcleo no disponible: no se pudo cargar la configuración (../config.js o config.json): ${e?.message || e}`);
  }
}

/** Valida el humor contra cfg.mood.allowed. */
function validarMood(mood, cfg) {
  const permitidos = Array.isArray(cfg?.mood?.allowed) && cfg.mood.allowed.length
    ? cfg.mood.allowed
    : MOODS_POR_DEFECTO;
  const m = String(mood ?? '').trim().toLowerCase();
  if (!m) throw new Error(`Falta el humor. Valores permitidos: ${permitidos.join(', ')}.`);
  if (!permitidos.includes(m)) {
    throw new Error(`El humor "${m}" no es válido. Valores permitidos: ${permitidos.join(', ')}.`);
  }
  return m;
}

/** Quita acentos y minúsculas para filtrar por tema. */
function sinAcentos(v = '') {
  return String(v).toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '');
}

// ============================================================
// Normalizadores (el núcleo puede nombrar los campos de varias maneras)
// ============================================================

function extraerLista(bruto) {
  if (Array.isArray(bruto)) return bruto;
  if (bruto && typeof bruto === 'object') {
    for (const clave of ['items', 'articles', 'noticias', 'news', 'results', 'data']) {
      if (Array.isArray(bruto[clave])) return bruto[clave];
    }
  }
  return [];
}

function normalizarNoticia(item) {
  if (typeof item === 'string') return { title: item };
  if (!item || typeof item !== 'object') return null;
  return {
    title: item.title ?? item.titulo ?? item.headline ?? '(sin titular)',
    source: item.source ?? item.fuente ?? item.author ?? '',
    url: item.url ?? item.link ?? item.enlace ?? '',
    // news.js del núcleo usa "published"; incluimos alias por robustez.
    date: item.date ?? item.fecha ?? item.published ?? item.publishedAt ?? item.pubDate ?? '',
    summary: item.summary ?? item.resumen ?? item.description ?? item.snippet ?? '',
  };
}

function normalizarClima(bruto) {
  if (typeof bruto === 'string') return { condicion: bruto };
  const w = bruto && typeof bruto === 'object' ? (bruto.weather ?? bruto.current ?? bruto.data ?? bruto) : {};
  const num = (v) => {
    if (typeof v === 'number') return v;
    if (typeof v === 'string' && v.trim() && !isNaN(Number(v))) return Number(v);
    return undefined;
  };
  const brutoLluvia = w.rain ?? w.rainProb ?? w.lluvia ?? w.precip ?? w.precipitation ?? w.precipProb ?? w.chanceOfRain ?? '';
  const claveLluvia = Object.keys(w).find((k) => w[k] === brutoLluvia) || '';
  return {
    temp: num(w.temp ?? w.temperatura ?? w.temperature ?? w.temp_c),
    condicion: w.condition ?? w.condicion ?? w.descripcion ?? w.description ?? w.text ?? '',
    max: num(w.max ?? w.tempMax ?? w.temp_max ?? w.high),
    min: num(w.min ?? w.tempMin ?? w.temp_min ?? w.low),
    sensacion: num(w.feelsLike ?? w.sensacion ?? w.apparentTemperature),
    lluvia: brutoLluvia,
    // rainProb (núcleo) es probabilidad en %; precipitaciones en mm.
    lluviaUnidad: /prob|chance|pop/i.test(claveLluvia) ? '%' : 'mm',
    consejo: w.advice ?? w.consejo ?? w.recomendacion ?? w.tip ?? '',
    degradado: w.degraded === true,
  };
}

// ============================================================
// Handlers de las 4 tools
// ============================================================

async function toolGetNews(args = {}) {
  const limit = Math.min(20, Math.max(1, Number.isFinite(Number(args.limit)) ? Number(args.limit) : 6));
  const topic = typeof args.topic === 'string' ? args.topic.trim() : '';
  const cfg = await loadCfg();

  const { fn: fetchNews } = await importarFn(
    ['../news.js'],
    ['fetchNews', 'getNews', 'loadNews'],
    'módulo de noticias (src/news.js)',
  );

  const bruto = await llamarConVariantes(fetchNews, [
    [cfg, limit],
    [{ limit, topic: topic || undefined }],
    [limit],
    [cfg],
    [],
  ]);

  let items = extraerLista(bruto).map(normalizarNoticia).filter(Boolean);
  if (topic) {
    const t = sinAcentos(topic);
    items = items.filter((n) => sinAcentos(`${n.title} ${n.summary}`).includes(t));
  }
  items = items.slice(0, limit);

  const lineas = ['📰 **ZOLO Noticias — frescas ahora mismo**', `_${fechaLargaGuayaquil()} · ${items.length} noticia(s)_`];
  if (topic) lineas.push(`_Tema filtrado: "${topic}"_`);
  lineas.push('');
  if (!items.length) {
    lineas.push('No encontré noticias frescas ahora mismo (posible filtro muy estrecho o feeds sin responder). Intenta de nuevo sin `topic`.');
  }
  items.forEach((n, i) => {
    lineas.push(`**${i + 1}. ${n.title}**`);
    if (n.summary) lineas.push(`   ${String(n.summary).slice(0, 220)}`);
    const meta = [n.source ? `*${n.source}*` : '', n.date ? `📅 ${fechaCorta(n.date)}` : ''].filter(Boolean).join(' · ');
    if (meta) lineas.push(`   ${meta}`);
    if (n.url) lineas.push(`   🔗 [Leer más](${n.url})`);
    lineas.push('');
  });
  lineas.push('— ZOLO · AliceLabs');
  return lineas.join('\n');
}

async function toolGetWeather(args = {}) {
  const cfg = await loadCfg();
  const cityCfg = cfg?.city || {};
  const ciudadPedida = typeof args.city === 'string' && args.city.trim() ? args.city.trim() : null;
  const ciudad = ciudadPedida || cityCfg.name || '';

  const { fn: getWeather } = await importarFn(
    ['../weather.js'],
    ['getWeather', 'fetchWeather', 'obtenerClima', 'clima'],
    'módulo de clima (src/weather.js)',
  );

  // fetchWeather(cityCfg) del núcleo espera {name,lat,lon,timezone} = cfg.city;
  // el resto de variantes quedan como respaldo genérico.
  const bruto = await llamarConVariantes(getWeather, [
    [cfg?.city],
    [cfg?.city, cfg],
    [ciudad, cfg],
    [ciudad],
    [cfg],
    [],
  ]);
  const w = normalizarClima(bruto);

  const notas = [];
  if (!ciudadPedida) {
    notas.push(`Nota: el proyecto tiene una sola ciudad configurada (${cityCfg.name || 'sin nombre'}); el dato corresponde a esa ciudad.`);
  } else if (cityCfg.name && sinAcentos(cityCfg.name) !== sinAcentos(ciudadPedida)) {
    notas.push(`Nota: pediste ${ciudadPedida}, pero el núcleo puede limitarse a la ciudad configurada (${cityCfg.name}); verifica el dato.`);
  }

  const linea = (icono, etiqueta, valor, sufijo = '') =>
    valor === undefined || valor === '' || valor === null ? null : `- ${icono} ${etiqueta}: **${valor}${sufijo}**`;

  const lineas = [`🌤️ **Clima${ciudad ? ` en ${ciudad}` : ''}**`, `_${fechaLargaGuayaquil()}_`, ''];
  const filas = [
    linea('🌡️', 'Temperatura', w.temp, w.temp !== undefined ? '°C' : ''),
    linea('🤒', 'Sensación térmica', w.sensacion, w.sensacion !== undefined ? '°C' : ''),
    linea('☁️', 'Condición', w.condicion),
    linea('⬆️', 'Máxima', w.max, w.max !== undefined ? '°C' : ''),
    linea('⬇️', 'Mínima', w.min, w.min !== undefined ? '°C' : ''),
    linea('🌧️', 'Lluvia', w.lluvia === '' ? undefined : `${w.lluvia}${w.lluviaUnidad}`),
  ].filter(Boolean);
  lineas.push(...(filas.length ? filas : ['- Sin datos de clima disponibles ahora mismo.']));
  if (w.degradado) lineas.push('', '⚠️ _Datos degradados: las fuentes de clima no respondieron bien ahora mismo._');
  if (w.consejo) lineas.push('', `💡 **Consejo:** ${w.consejo}`);
  if (notas.length) lineas.push('', `_${notas.join(' ')}_`);
  lineas.push('', '— ZOLO · AliceLabs');
  return lineas.join('\n');
}

/** Convierte script.json ({sections:[...]}) o texto plano en markdown legible. */
function formatearBoletinMd(contenido, cfg) {
  const secs = Array.isArray(contenido?.sections)
    ? contenido.sections
    : Array.isArray(contenido) ? contenido : null;

  const encabezado = [
    '☀️ **ZOLO NOTICIAS — boletín de HOY**',
    `_${fechaLargaGuayaquil()} · ${cfg?.city?.name || ''} · humor: ${contenido?.mood || cfg?.mood?.default || 'neutral'}_`,
    '',
  ];

  if (typeof contenido === 'string' && contenido.trim()) {
    return [...encabezado, contenido.trim()].join('\n');
  }
  if (typeof contenido?.reportMd === 'string' && contenido.reportMd.trim()) {
    return [...encabezado, contenido.reportMd.trim()].join('\n');
  }
  if (secs) {
    const titulos = {
      intro: '🎬 Apertura', news: '📰 Noticia', weather: '🌤️ Clima',
      curious: '🎲 Curiosidad', outro: '👋 Despedida',
    };
    const cuerpo = secs.map((s) => {
      const t = titulos[s?.kind] || '• Sección';
      const titulo = s?.title ? ` — **${s.title}**` : '';
      const meta = s?.url ? `\n   🔗 [fuente](${s.url})${s.source ? ` (${s.source})` : ''}` : '';
      return `${t}${titulo}\n${String(s?.text ?? '').trim()}${meta}`;
    }).join('\n\n');
    return [...encabezado, cuerpo].join('\n');
  }
  return [...encabezado, 'La corrida de hoy no contiene secciones legibles.'].join('\n');
}

/** ¿Existe corrida de HOY? → {script, reportMd, dir} o null. */
function boletinDeHoy() {
  const hoy = hoyGuayaquil();
  const dirHoy = path.join(PROJECT_ROOT, 'output', hoy);
  const scriptPath = path.join(dirHoy, 'script.json');
  if (!fs.existsSync(scriptPath)) return null;

  // Criterio principal: script.json de HOY. lastRun.json es confirmación adicional.
  let lastRunOk = null;
  try {
    const lastRun = JSON.parse(fs.readFileSync(path.join(PROJECT_ROOT, 'state', 'lastRun.json'), 'utf8'));
    const candidata = [lastRun?.date, lastRun?.fecha, lastRun?.day, lastRun?.dateISO, lastRun?.createdAt, lastRun?.startedAt, lastRun?.timestamp]
      .find((v) => v !== undefined && v !== null);
    const m = String(candidata ?? '').match(/(\d{4})-(\d{2})-(\d{2})/);
    lastRunOk = m ? `${m[1]}-${m[2]}-${m[3]}` === hoy : null;
  } catch { /* lastRun.json ausente o ilegible: no bloquea */ }

  const script = JSON.parse(fs.readFileSync(scriptPath, 'utf8'));
  const reportPath = path.join(dirHoy, 'report.md');
  const reportMd = fs.existsSync(reportPath) ? fs.readFileSync(reportPath, 'utf8') : null;
  return { script, reportMd, dir: `output/${hoy}`, lastRunOk };
}

async function toolGetBulletin(args = {}) {
  const cfg = await loadCfg();
  const mood = args.mood ? validarMood(args.mood, cfg) : null;

  // ---- 1) Boletín ya producido HOY (America/Guayaquil) ----
  try {
    const deHoy = boletinDeHoy();
    if (deHoy) {
      const fuente = `📁 corrida de hoy (${deHoy.dir}${deHoy.lastRunOk === false ? ', lastRun.json desalineado pero script.json es de hoy' : ''})`;
      const md = deHoy.reportMd?.trim()
        ? `☀️ **ZOLO NOTICIAS — boletín de HOY**\n_${fechaLargaGuayaquil()}_\n\n${deHoy.reportMd.trim()}`
        : formatearBoletinMd(deHoy.script, cfg);
      return `${md}\n\n---\n_${fuente}_`;
    }
  } catch { /* lastRun/script ilegibles → generar al vuelo */ }

  // ---- 2) Generación al vuelo (news + weather + curiosidades + scriptWriter) ----
  const { fn: fetchNews } = await importarFn(['../news.js'], ['fetchNews', 'getNews', 'loadNews'], 'módulo de noticias (src/news.js)');
  const { fn: getWeather } = await importarFn(['../weather.js'], ['getWeather', 'fetchWeather', 'obtenerClima', 'clima'], 'módulo de clima (src/weather.js)');
  const { fn: writeScript } = await importarFn(
    ['../scriptWriter.js', '../script.js', '../script/index.js'],
    // buildNewscast/buildFallbackScript = contrato real del núcleo (125-A);
    // el resto son respaldos genéricos.
    ['buildNewscast', 'buildFallbackScript', 'writeScript', 'buildScript', 'generateScript', 'makeScript', 'crearGuion', 'escribirGuion'],
    'módulo de guion (src/scriptWriter.js)',
  );

  // Humor efectivo: explícito > state (getMood) > config default. Best-effort.
  let moodEfectivo = mood;
  if (!moodEfectivo) {
    try {
      const { fn: getMood } = await importarFn(['../mood.js'], ['getMood', 'leerMood'], 'módulo de humor (getMood)');
      moodEfectivo = await llamarConVariantes(getMood, [[cfg], []]);
    } catch { moodEfectivo = null; }
    if (!moodEfectivo) moodEfectivo = cfg?.mood?.default || 'neutral';
  }

  const limit = cfg?.news?.maxItems || 6;
  const [news, weather] = await Promise.all([
    llamarConVariantes(fetchNews, [[cfg, limit], [{ limit }], [cfg], []]),
    llamarConVariantes(getWeather, [[cfg?.city], [cfg?.city, cfg], [cfg], []]),
  ]);
  // Curiosidades (Wikipedia “tal día como hoy”, cripto, humor) — best-effort:
  // si el módulo falla el guion se genera igual (buildFallbackScript tolera ausencia).
  let curiosities;
  try {
    const { fn: getCuriosities } = await importarFn(['../curiosities.js'], ['getCuriosities'], 'módulo de curiosidades (src/curiosities.js)');
    curiosities = await llamarConVariantes(getCuriosities, [[cfg, moodEfectivo], [cfg]]);
  } catch { curiosities = undefined; }

  const guion = await llamarConVariantes(writeScript, [
    [{ cfg, news, weather, curiosities, mood: moodEfectivo }],
    [{ news, weather, curiosities, mood: moodEfectivo }],
    [{ cfg, news, weather, mood: moodEfectivo }],
  ]);

  const md = formatearBoletinMd(guion, cfg);
  return `${md}\n\n---\n_⚡ generado al vuelo (aún no hay corrida programada de hoy; el boletín oficial se produce a las ${cfg?.wakeTime || '06:30'})_`;
}

async function toolSetMood(args = {}) {
  const cfg = await loadCfg();
  const mood = validarMood(args?.mood, cfg);

  const { fn: setMood, nombre } = await importarFn(
    ['../mood.js'],
    ['setMood', 'definirMood', 'guardarMood', 'setHumor'],
    'módulo de humor (src/mood.js)',
  );
  // Firma real del núcleo: setMood(mood, cfg).
  await llamarConVariantes(setMood, [[mood, cfg], [mood]]);

  const permitidos = Array.isArray(cfg?.mood?.allowed) && cfg.mood.allowed.length ? cfg.mood.allowed : MOODS_POR_DEFECTO;
  return [
    `✅ **Humor actualizado a \`${mood}\`** (vía mood.js · ${nombre}).`,
    '',
    `El boletín de mañana se redactará con ese tono. Valores permitidos: ${permitidos.join(', ')}.`,
    '',
    '— ZOLO · AliceLabs',
  ].join('\n');
}

// ============================================================
// Definición de tools (contrato MCP)
// ============================================================

const TOOLS = [
  {
    name: 'zolo_get_news',
    description: 'Noticias frescas de Ecuador y el mundo (RSS: Google News Ecuador, BBC Mundo, Infobae, El Universo, El Comercio). Devuelve markdown con titular, fuente, fecha y link.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: { type: 'number', minimum: 1, maximum: 20, default: 6, description: 'Cantidad máxima de noticias (1-20).' },
        topic: { type: 'string', description: 'Palabra clave para filtrar (p.ej. "economía", "Selección").' },
      },
    },
  },
  {
    name: 'zolo_get_weather',
    description: 'Clima actual de la ciudad configurada en config.json (por defecto Guayaquil, Ecuador): temperatura, condición, máx/mín, lluvia y consejo del día.',
    inputSchema: {
      type: 'object',
      properties: {
        city: { type: 'string', description: 'Ciudad opcional; si se omite usa la configurada.' },
      },
    },
  },
  {
    name: 'zolo_get_bulletin',
    description: 'El boletín completo de HOY de ZOLO NEWS (noticiero matutino): si ya corrió el agente devuelve el guion/report.md de hoy; si no, genera uno al vuelo con noticias + clima + curiosidades.',
    inputSchema: {
      type: 'object',
      properties: {
        mood: { type: 'string', description: 'Tono opcional del boletín: feliz, neutral, serio, motivado, bajoneado.' },
      },
    },
  },
  {
    name: 'zolo_set_mood',
    description: 'Configura el tono (humor) con el que ZOLO redactará el boletín de mañana. Valores: feliz, neutral, serio, motivado, bajoneado.',
    inputSchema: {
      type: 'object',
      required: ['mood'],
      properties: {
        mood: { type: 'string', description: 'Tono del boletín de mañana.' },
      },
    },
  },
];

// ============================================================
// Servidor MCP (stdio)
// ============================================================

function textoResultado(text) {
  return { content: [{ type: 'text', text }] };
}

const server = new Server(
  { name: 'zolo-news', version: '1.0.0' },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const name = request?.params?.name || '';
  const args = request?.params?.arguments || {};
  try {
    switch (name) {
      case 'zolo_get_news':    return textoResultado(await toolGetNews(args));
      case 'zolo_get_weather': return textoResultado(await toolGetWeather(args));
      case 'zolo_get_bulletin':return textoResultado(await toolGetBulletin(args));
      case 'zolo_set_mood':    return textoResultado(await toolSetMood(args));
      default:
        throw new Error(`Herramienta desconocida: "${name}". Disponibles: ${TOOLS.map((t) => t.name).join(', ')}.`);
    }
  } catch (e) {
    // Errores SIEMPRE en español, como texto (nunca tiran la sesión del cliente).
    return { ...textoResultado(`ERROR: ${e?.message || e}`), isError: true };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // stderr: stdout es exclusivo del protocolo JSON-RPC.
  console.error('ZOLO NEWS MCP listo (stdio)');
}

main().catch((e) => {
  console.error('Fallo al iniciar el servidor MCP zolo-news:', e?.message || e);
  process.exit(1);
});

// Cierre limpio (Claude Desktop manda SIGINT/SIGTERM al detener).
process.on('SIGINT', () => process.exit(0));
process.on('SIGTERM', () => process.exit(0));
