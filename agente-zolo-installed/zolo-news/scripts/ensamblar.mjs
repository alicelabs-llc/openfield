#!/usr/bin/env node
// ============================================================
// ZOLO NEWS — Ensamblaje por etapas (integración, Task 125 main)
// Usa el código REAL del pipeline de medios (125-B):
//   node scripts/ensamblar.mjs audio    → avatar + TTS de las secciones
//   node scripts/ensamblar.mjs images   → imágenes de noticias
//   node scripts/ensamblar.mjs video    → MP4 final con las etapas previas
// Se apoya en state/lastRun.json (outDir) y output/<fecha>/script.json
// ============================================================
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { loadConfig } from '../src/config.js';
import * as media from '../src/media/index.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const mode = process.argv[2] || 'audio';

function cargarContexto() {
  const lastRun = JSON.parse(readFileSync(path.join(root, 'state', 'lastRun.json'), 'utf8'));
  const outDir = lastRun.artifacts?.outDir;
  if (!outDir || !existsSync(outDir)) throw new Error('outDir no existe: ' + outDir);
  const doc = JSON.parse(readFileSync(path.join(outDir, 'script.json'), 'utf8'));
  const sections = doc.sections ?? doc.newscast?.sections;
  if (!Array.isArray(sections) || !sections.length) throw new Error('script.json sin secciones');
  return { cfg: loadConfig(), sections, outDir };
}

function leerJSON(p) {
  return existsSync(p) ? JSON.parse(readFileSync(p, 'utf8')) : null;
}

const stage = async () => {
  const { cfg, sections, outDir } = cargarContexto();
  console.log(`🎬 Ensamblaje [${mode}] · ${sections.length} secciones · ${outDir}`);

  if (mode === 'audio') {
    const avatar = await media.makeAvatar(cfg);
    console.log('🧑‍💼 Avatar:', avatar);
    const audio = await media.makeAudio(sections, cfg);
    const total = audio.reduce((a, s) => a + (s.seconds || 0), 0);
    console.log(`🔊 Fragmentos: ${audio.length} · duración total ${total.toFixed(1)}s`);
    writeFileSync(path.join(outDir, 'audio.json'), JSON.stringify({ avatar, audio }, null, 2));
    console.log('💾 audio.json guardado');
    return;
  }

  if (mode === 'images') {
    const images = await media.makeNewsImages(sections, cfg);
    console.log(`🖼️  Imágenes: ${images.length}`);
    writeFileSync(path.join(outDir, 'images.json'), JSON.stringify({ images }, null, 2));
    console.log('💾 images.json guardado');
    return;
  }

  if (mode === 'video') {
    const saved = leerJSON(path.join(outDir, 'audio.json'));
    const savedImgs = leerJSON(path.join(outDir, 'images.json'));
    if (!saved?.audio?.length) throw new Error('audio.json falta — corre `ensamblar.mjs audio` primero');
    const avatar = saved.avatar ?? (await media.makeAvatar(cfg));
    const images = savedImgs?.images ?? (await media.makeNewsImages(sections, cfg));
    const video = await media.makeVideo({ sections, audio: saved.audio, avatar, images }, cfg);
    console.log('🎥 Resultado:', JSON.stringify(video, null, 2));
    return;
  }

  throw new Error('Modo desconocido: ' + mode);
};

const T0 = performance.now();
stage()
  .then(() => console.log(`✅ Etapa [${mode}] OK en ${((performance.now() - T0) / 1000).toFixed(1)}s`))
  .catch((err) => {
    console.error(`❌ Etapa [${mode}] falló: ${err?.message ?? err}`);
    process.exitCode = 1;
  });
