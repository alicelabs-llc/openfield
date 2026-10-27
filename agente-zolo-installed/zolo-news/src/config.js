// ============================================================
// ZOLO NEWS — Cargador de configuración (subagente 125-A)
// Lee config.json (ruta relativa a ESTE archivo), valida campos
// mínimos y aplica overrides por variables de entorno.
// ============================================================
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = path.resolve(__dirname, '..', 'config.json');

/** Expresión HH:MM válida de 24 horas (ej. "06:30"). */
const WAKE_RE = /^([01]\d|2[0-3]):([0-5]\d)$/;

/**
 * Devuelve la ruta absoluta del config.json (útil para diagnósticos).
 */
export function configPath() {
  return CONFIG_PATH;
}

/**
 * Carga y valida la configuración del noticiero.
 * - Lanza error claro si el archivo no existe o es JSON inválido (sin config no hay run).
 * - Los campos secundarios reciben valores por defecto (resiliencia).
 * - Overrides de entorno: ZOLO_USER_NAME, ZOLO_CITY_LAT, ZOLO_CITY_LON, ZOLO_WAKE_TIME.
 * @returns {object} cfg — configuración lista para todos los módulos.
 */
export function loadConfig() {
  let raw;
  try {
    raw = readFileSync(CONFIG_PATH, 'utf8');
  } catch (err) {
    throw new Error(`config.json no se pudo leer en ${CONFIG_PATH}: ${err.message}`);
  }

  let base;
  try {
    base = JSON.parse(raw);
  } catch (err) {
    throw new Error(`config.json es JSON inválido: ${err.message}`);
  }
  if (!base || typeof base !== 'object') {
    throw new Error('config.json inválido: el contenido no es un objeto');
  }

  // ---- Validación de campos mínimos (lo esencial; lo demás tiene defaults)
  const nombre = (base.user?.name ?? '').trim();
  if (!nombre) throw new Error('config.json inválido: falta user.name (¿a quién le hablamos?)');

  const lat = Number(base.city?.lat);
  const lon = Number(base.city?.lon);
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    throw new Error('config.json inválido: city.lat y city.lon deben ser números');
  }

  // ---- Defaults de secciones opcionales
  const cfg = {
    ...base,
    user: { language: 'es', ...(base.user ?? {}), name: nombre },
    city: {
      name: base.city?.name ?? 'Guayaquil',
      lat,
      lon,
      timezone: base.city?.timezone ?? 'America/Guayaquil',
    },
    wakeTime: base.wakeTime ?? '06:30',
    mood: {
      default: base.mood?.default ?? 'neutral',
      allowed: Array.isArray(base.mood?.allowed) && base.mood.allowed.length
        ? base.mood.allowed
        : ['feliz', 'neutral', 'serio', 'motivado', 'bajoneado'],
      ...(base.mood?.current ? { current: base.mood.current } : {}),
    },
    news: {
      maxItems: Math.max(1, Math.min(12, Number(base.news?.maxItems) || 6)),
      feeds: Array.isArray(base.news?.feeds) ? base.news.feeds.filter((f) => f?.url) : [],
    },
    tts: { voice: 'tongtong', speed: 1.0, ...(base.tts ?? {}) },
    video: { width: 1280, height: 720, ...(base.video ?? {}) },
    features: {
      onThisDay: true, joke: true, quote: true, crypto: true,
      ...(base.features ?? {}),
    },
    channels: base.channels ?? {},
  };

  if (!WAKE_RE.test(cfg.wakeTime)) {
    throw new Error(`config.json inválido: wakeTime "${cfg.wakeTime}" no es HH:MM válido (ej. 06:30)`);
  }
  if (cfg.news.feeds.length === 0) {
    throw new Error('config.json inválido: news.feeds está vacío (no hay de dónde sacar noticias)');
  }

  // ---- Overrides por entorno (para pruebas sin tocar config.json)
  if (process.env.ZOLO_USER_NAME && process.env.ZOLO_USER_NAME.trim()) {
    cfg.user.name = process.env.ZOLO_USER_NAME.trim();
  }
  if (process.env.ZOLO_CITY_LAT && Number.isFinite(Number(process.env.ZOLO_CITY_LAT))) {
    cfg.city.lat = Number(process.env.ZOLO_CITY_LAT);
  }
  if (process.env.ZOLO_CITY_LON && Number.isFinite(Number(process.env.ZOLO_CITY_LON))) {
    cfg.city.lon = Number(process.env.ZOLO_CITY_LON);
  }
  if (process.env.ZOLO_WAKE_TIME && WAKE_RE.test(process.env.ZOLO_WAKE_TIME)) {
    cfg.wakeTime = process.env.ZOLO_WAKE_TIME;
  }

  return cfg;
}

export default { loadConfig, configPath };
