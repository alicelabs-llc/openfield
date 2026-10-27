// ============================================================
// ZOLO NEWS — Estado de ánimo (humor) del presentador (125-A)
// Se persiste en state/mood.json: { mood, setAt }
// getMood(cfg) → mood actual (state > cfg.mood.current > default)
// setMood(mood, cfg) → valida y persiste
// toneHints(mood) → instrucciones de tono para el guionista
// ============================================================
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_DIR = path.resolve(__dirname, '..', 'state');
const MOOD_PATH = path.join(STATE_DIR, 'mood.json');

/**
 * Lee el humor persistido. Si no existe o está corrupto, cae a
 * cfg.mood.current y por último a cfg.mood.default. NUNCA lanza.
 */
export function getMood(cfg) {
  try {
    const raw = JSON.parse(readFileSync(MOOD_PATH, 'utf8'));
    const allowed = cfg?.mood?.allowed ?? [];
    if (raw && typeof raw.mood === 'string' && raw.mood.trim()) {
      const mood = raw.mood.trim().toLowerCase();
      // Si hay lista permitida y el estado no pertenece a ella, se ignora.
      if (allowed.length === 0 || allowed.includes(mood)) return mood;
    }
  } catch {
    /* sin estado previo: es normal la primera vez */
  }
  return cfg?.mood?.current || cfg?.mood?.default || 'neutral';
}

/**
 * Valida y persiste el humor con timestamp ISO.
 * @returns {{mood:string, setAt:string}} lo guardado
 * @throws Error si el mood no está en cfg.mood.allowed
 */
export function setMood(mood, cfg) {
  const valor = String(mood ?? '').trim().toLowerCase();
  const allowed = cfg?.mood?.allowed ?? ['feliz', 'neutral', 'serio', 'motivado', 'bajoneado'];
  if (!allowed.includes(valor)) {
    throw new Error(`humor inválido: "${valor}". Permitidos: ${allowed.join(', ')}`);
  }
  const payload = { mood: valor, setAt: new Date().toISOString() };
  mkdirSync(STATE_DIR, { recursive: true });
  writeFileSync(MOOD_PATH, JSON.stringify(payload, null, 2) + '\n', 'utf8');
  return payload;
}

/** Lee {mood, setAt} crudo del disco (para `status`). Devuelve null si no existe. */
export function readMoodState() {
  try {
    return JSON.parse(readFileSync(MOOD_PATH, 'utf8'));
  } catch {
    return null;
  }
}

/**
 * Pistas de tono por humor — alimentan el prompt del guionista y de curiosidades.
 * @returns {{estilo:string, instruccion:string}}
 */
export function toneHints(mood) {
  switch (mood) {
    case 'feliz':
      return {
        estilo: 'alegre y bromista',
        instruccion: 'Usa humor ligero, entusiasmo contagioso y alguna picardía suave. Puedes reírte contigo mismo.',
      };
    case 'serio':
      return {
        estilo: 'sobrio y directo',
        instruccion: 'Tono profesional, sin bromas ni exclamaciones; ve directo a la información con precisión.',
      };
    case 'motivado':
      return {
        estilo: 'energético y motivador',
        instruccion: 'Energía alta, frases que empujan a actuar, verbos de acción y cierre con un empujón motivacional.',
      };
    case 'bajoneado':
      return {
        estilo: 'tierno y reconfortante',
        instruccion: 'Máxima ternura y calma. PROHIBIDO el humor negro y los chistes forzados; reconforta con suavidad y cierra con algo esperanzador.',
      };
    case 'neutral':
    default:
      return {
        estilo: 'ligero y cordial',
        instruccion: 'Tono amable y claro, con toques de humor sutil sin exagerar.',
      };
  }
}
