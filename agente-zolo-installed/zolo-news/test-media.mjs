// ============================================================
// ZOLO NEWS — Prueba standalone del pipeline de medios (Subagente 125-B)
// Genera en output/test/: avatar (o caché), 2 WAV (intro + noticia),
// imágenes por sección y bulletin.mp4/bulletin.wav de prueba.
// Ejecutar:  node test-media.mjs
// ============================================================

import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';
import { makeAvatar, makeAudio, makeNewsImages, makeVideo } from './src/media/index.js';

const execFileAsync = promisify(execFile);
const ROOT = path.dirname(fileURLToPath(import.meta.url));

// Config real del proyecto + overrides SOLO para esta prueba (→ output/test/)
const cfg = JSON.parse(readFileSync(path.join(ROOT, 'config.json'), 'utf8'));
cfg.outputDate = 'test'; // las funciones escriben en output/<outputDate || YYYY-MM-DD>/

const KB = (p) => (fs.statSync(p).size / 1024).toFixed(1);

async function probeDuration(file) {
  const { stdout } = await execFileAsync('ffprobe', [
    '-v', 'error', '-show_entries', 'format=duration',
    '-of', 'default=noprint_wrappers=1:nokey=1', file,
  ]);
  return parseFloat(String(stdout).trim());
}

// --- Guion de prueba (2 secciones, español) ---
const sections = [
  {
    kind: 'intro',
    title: 'ZOLO NOTICIAS',
    text: 'Buenos días Edison, soy ZOLO, tu noticiero matutino autónomo. Hoy es un gran día para despertarse informado. Comenzamos con la noticia principal de la jornada.',
  },
  {
    kind: 'news',
    title: 'Pipeline de medios listo',
    text: 'ZOLO NEWS completa su primera prueba técnica de punta a punta. El pipeline de medios generó la voz del presentador, las imágenes de cada sección y el video final del noticiero sin intervención humana. Así, Edison Flores, founder de AliceLabs, podrá recibir cada mañana su resumen informativo listo para ver y escuchar.',
    source: 'Prueba técnica',
    url: 'https://example.com/zolo-news',
    imagePrompt: 'sunrise over Guayaquil Ecuador skyline with the Guayas river, modern city buildings, warm morning light, clouds',
    caption: 'Prueba de video del noticiero',
  },
];

let ok = true;
try {
  console.log('=== ZOLO NEWS · test de pipeline de medios (subagente 125-B) ===\n');

  // 1) Avatar
  const avatar = await makeAvatar(cfg);
  console.log(`[1] Avatar: ${avatar.path} (cached=${avatar.cached}, ${KB(avatar.path)} KB)\n`);

  // 2) Audio TTS por sección
  const audio = await makeAudio(sections, cfg);
  const totalAudio = audio.reduce((s, a) => s + a.seconds, 0);
  for (const a of audio) console.log(`[2] Audio seg_${String(a.index).padStart(2, '0')}.wav: ${a.seconds.toFixed(2)}s (${KB(a.path)} KB)`);
  console.log(`[2] Audio total: ${totalAudio.toFixed(2)}s\n`);

  // 3) Imágenes por sección
  const images = await makeNewsImages(sections, cfg);
  for (const im of images) console.log(`[3] Imagen img_${im.index}.png: ${KB(im.path)} KB → ${im.path}`);
  console.log('');

  // 4) Video
  const { videoPath, reason } = await makeVideo({ sections, audio, avatar, images }, cfg);
  if (!videoPath) throw new Error(`makeVideo devolvió null: ${reason}`);
  console.log(`[4] Video: ${videoPath} (${KB(videoPath)} KB)`);

  // --- Verificación dura (evidencia) ---
  const dur = await probeDuration(videoPath);
  const sizeKB = parseFloat(KB(videoPath));
  console.log(`\nDuración del MP4: ${dur.toFixed(2)}s | Tamaño: ${sizeKB.toFixed(1)} KB`);

  if (!(sizeKB > 100)) throw new Error(`el MP4 pesa ${sizeKB} KB (se esperaba > 100 KB)`);
  if (!(dur > 5)) throw new Error(`el MP4 dura ${dur.toFixed(2)}s (se esperaba > 5s)`);
  const wavOk = fs.existsSync(path.join(ROOT, 'output', 'test', 'bulletin.wav'));
  if (!wavOk) throw new Error('bulletin.wav no existe en output/test/');
  if (Math.abs(dur - totalAudio) > 3) throw new Error(`duración del video (${dur.toFixed(2)}s) difiere >3s del audio (${totalAudio.toFixed(2)}s)`);

  console.log('\n✅ TEST DE MEDIOS OK: avatar, 2 WAV, imágenes y bulletin de prueba generados.');
  console.log(`   Salida: ${path.join(ROOT, 'output', 'test')}`);
} catch (e) {
  ok = false;
  console.error(`\n❌ TEST DE MEDIOS FALLÓ: ${e.message}`);
  if (String(e.message).includes('TTS_FAILED') || String(e.message).includes('IMAGE_FAILED')) {
    console.error('   Posible bloqueo de auth/red del SDK z-ai-web-dev-sdk. Revisa logs/test-125B.txt');
  }
  process.exitCode = 1;
}
