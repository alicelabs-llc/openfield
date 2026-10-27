// ============================================================
// ZOLO NEWS — Imágenes por noticia + fondo de estudio
// Subagente 125-B · Pipeline de medios
// - makeNewsImages(sections, cfg) → [{index, path}]
// - Fondo genérico cacheado en assets/background-studio.png (1 sola generación)
// Reglas: noticia con imagePrompt → 1344x768; resto → fondo de estudio.
// Si falla UNA imagen de noticia → fondo genérico + aviso (no lanza error).
// ============================================================

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { generateImage } from './avatar.js'; // helper compartido (misma zona de medios)

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

// Fondo de estudio cacheado (promedio 1344x768, recortable a 1280x720)
export const STUDIO_PROMPT =
  'modern TV newsroom studio background, blue and teal lighting, wide shot, no people, no text';

const NEWS_SUFFIX = ', editorial photography, dramatic lighting, no text, no watermark, high quality';

function studioPath() {
  return path.join(path.resolve(ROOT, 'assets'), 'background-studio.png');
}

/** Asegura el fondo de estudio en assets/ (lo genera UNA vez). Devuelve su ruta. */
export async function ensureBackground(cfg) {
  const p = studioPath();
  if (fs.existsSync(p)) {
    const head = fs.readFileSync(p).subarray(0, 4).toString('hex');
    if (fs.statSync(p).size > 1024 && head === '89504e47') return p;
    console.warn('[MEDIA][IMG] Fondo de estudio corrupto, regenerando…');
  }
  try {
    await generateImage(STUDIO_PROMPT, '1344x768', p);
    console.log(`[MEDIA][IMG] Fondo de estudio generado: ${p}`);
  } catch (e) {
    throw new Error(`IMAGE_FAILED: no se pudo generar el fondo de estudio: ${e.message}`);
  }
  return p;
}

/**
 * Genera imágenes por sección: noticia con imagePrompt → imagen dedicada;
 * intro/weather/curious/outro (o noticia sin imagePrompt) → fondo de estudio copiado.
 * @param {Array<{kind:string,imagePrompt?:string,title?:string,caption?:string}>} sections
 * @param {object} cfg
 * @returns {Promise<Array<{index:number, path:string}>>}
 */
export async function makeNewsImages(sections, cfg) {
  if (!Array.isArray(sections)) sections = [];

  const dayDir = path.join(path.resolve(ROOT, cfg?.outputRoot || 'output'), cfg?.outputDate || todayLocal(cfg));
  const imgDir = path.join(dayDir, 'images');
  fs.mkdirSync(imgDir, { recursive: true });

  // Fondo de estudio (obligatorio para uniformidad y fallback)
  const bg = await ensureBackground(cfg);

  const results = [];
  for (let i = 0; i < sections.length; i++) {
    const s = sections[i] ?? {};
    const outPath = path.join(imgDir, `img_${i}.png`);
    const wantsOwn = s.kind === 'news' && typeof s.imagePrompt === 'string' && s.imagePrompt.trim().length > 0;

    if (wantsOwn) {
      try {
        const prompt = `${s.imagePrompt.trim()}${NEWS_SUFFIX}`;
        await generateImage(prompt, '1344x768', outPath);
        console.log(`[MEDIA][IMG] img_${i}.png generada (noticia, ${(fs.statSync(outPath).size / 1024).toFixed(1)} KB)`);
        results.push({ index: i, path: outPath });
        continue;
      } catch (e) {
        // Una imagen fallida no debe tumbar el noticiero: fallback a fondo + aviso
        console.warn(`[MEDIA][IMG] Aviso: imagen ${i} falló (${e.message}); se usa el fondo de estudio`);
      }
    }

    fs.copyFileSync(bg, outPath); // copia al output para uniformidad del día
    results.push({ index: i, path: outPath });
  }
  return results;
}

// Fecha local YYYY-MM-DD (duplicado mínimo para mantener módulos autocontenidos)
function todayLocal(cfg) {
  const tz = cfg?.city?.timezone || 'America/Guayaquil';
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date());
  const get = (t) => parts.find((p) => p.type === t)?.value ?? '00';
  return `${get('year')}-${get('month')}-${get('day')}`;
}
