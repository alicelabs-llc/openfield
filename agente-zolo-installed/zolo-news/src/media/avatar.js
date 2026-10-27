// ============================================================
// ZOLO NEWS — Avatar del presentador (imagen IA)
// Subagente 125-B · Pipeline de medios
// - ensureAvatar(cfg) → {path, cached}  (caché en assets/avatar.png)
// - makeAvatar: alias de contrato consumido por src/media/index.js
// API: z-ai-web-dev-sdk · zai.images.generations.create
// ============================================================

import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import ZAI from 'z-ai-web-dev-sdk';

const execFileAsync = promisify(execFile);

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

// Prompt EN INGLÉS para el ancla visual de la marca (reproducible corrida a corrida)
export const AVATAR_PROMPT =
  'Friendly futuristic robot TV news anchor named ZOLO, 3D pixar-like style, ' +
  'modern television studio with blue and teal screens lighting, professional ' +
  'broadcast look, looking at camera, upper body, high quality, detailed';

let _zai = null;
async function getZAI() {
  if (!_zai) _zai = await ZAI.create();
  return _zai;
}

/** Genera una imagen con el SDK y la escribe en outPath como PNG real. */
export async function generateImage(prompt, size, outPath) {
  const zai = await getZAI();
  const r = await zai.images.generations.create({ prompt, size });
  const b64 = r?.data?.[0]?.base64;
  if (!b64) throw new Error('la API no devolvió base64 para la imagen');
  const buf = Buffer.from(b64, 'base64');
  if (buf.length < 1024) throw new Error(`imagen inválida (${buf.length} bytes)`);

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const head = buf.subarray(0, 4).toString('hex');

  if (head === '89504e47') {
    // PNG nativo: escribir directo
    fs.writeFileSync(outPath, buf);
    return outPath;
  }
  if (head.startsWith('ffd8ff')) {
    // La API devuelve JPEG (JFIF) pese al contrato: normalizamos a PNG real con ffmpeg
    const src = `${outPath}.src.jpg`;
    fs.writeFileSync(src, buf);
    try {
      await execFileAsync('ffmpeg', ['-y', '-v', 'error', '-i', src, '-frames:v', '1', outPath],
        { maxBuffer: 16 * 1024 * 1024 });
    } finally {
      fs.rmSync(src, { force: true });
    }
    if (!fs.existsSync(outPath) || fs.statSync(outPath).size < 1024) {
      throw new Error('conversión JPEG→PNG falló');
    }
    return outPath;
  }
  throw new Error(`formato de imagen no reconocido (header=${head})`);
}

/**
 * Genera (o reutiliza desde caché) el avatar presentador de ZOLO Noticias.
 * @param {object} cfg - config.json cargado
 * @returns {Promise<{path: string, cached: boolean}>}
 */
export async function ensureAvatar(cfg) {
  const assetsDir = path.resolve(ROOT, 'assets');
  fs.mkdirSync(assetsDir, { recursive: true });
  const avatarPath = path.join(assetsDir, 'avatar.png');

  // Caché en disco: si ya existe y es un PNG razonable, reutilizar
  if (fs.existsSync(avatarPath)) {
    const size = fs.statSync(avatarPath).size;
    const head = fs.readFileSync(avatarPath).subarray(0, 4).toString('hex');
    if (size > 1024 && head === '89504e47') {
      console.log(`[MEDIA][AVATAR] Reutilizando caché: ${avatarPath} (${(size / 1024).toFixed(1)} KB)`);
      return { path: avatarPath, cached: true };
    }
    console.warn('[MEDIA][AVATAR] Caché corrupta, regenerando…');
  }

  try {
    await generateImage(AVATAR_PROMPT, '1024x1024', avatarPath);
  } catch (e) {
    throw new Error(`IMAGE_FAILED: no se pudo generar el avatar: ${e.message}`);
  }
  const kb = (fs.statSync(avatarPath).size / 1024).toFixed(1);
  console.log(`[MEDIA][AVATAR] Avatar generado: ${avatarPath} (${kb} KB)`);
  return { path: avatarPath, cached: false };
}

// Contrato del pipeline (el núcleo consume makeAvatar)
export const makeAvatar = ensureAvatar;
