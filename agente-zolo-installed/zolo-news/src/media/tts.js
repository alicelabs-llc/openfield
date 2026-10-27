// ============================================================
// ZOLO NEWS — TTS (voz del presentador)
// Subagente 125-B · Pipeline de medios
// - synthesizeSection(text, cfg, outPath): 1 sección → WAV en disco
// - makeAudio(sections, cfg): [{index, path, seconds}] en orden de sections
// API: z-ai-web-dev-sdk · zai.audio.tts.create (máx 1024 chars/llamada)
// ============================================================

import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import ZAI from 'z-ai-web-dev-sdk';

const execFileAsync = promisify(execFile);
const FFMPEG_OPTS = { maxBuffer: 16 * 1024 * 1024 };

// Raíz del proyecto (…/zolo-news) — independiente del cwd
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

// Instancia del SDK reutilizable
let _zai = null;
async function getZAI() {
  if (!_zai) _zai = await ZAI.create();
  return _zai;
}

// ---------- Utilidades ----------

/** Fecha local (YYYY-MM-DD) en la zona horaria de la ciudad (America/Guayaquil). */
export function todayLocal(cfg) {
  const tz = cfg?.city?.timezone || 'America/Guayaquil';
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date());
  const get = (t) => parts.find((p) => p.type === t)?.value ?? '00';
  return `${get('year')}-${get('month')}-${get('day')}`;
}

/** Directorio de salida del día. Soporta cfg.outputRoot / cfg.outputDate (usados por test-media). */
export function outputDayDir(cfg) {
  const base = path.resolve(ROOT, cfg?.outputRoot || 'output');
  const day = String(cfg?.outputDate || todayLocal(cfg));
  return path.join(base, day);
}

/** Limpia el texto para TTS: quita markdown, emojis, URLs; colapsa espacios. ZOLO queda tal cual. */
export function cleanTextForTTS(text) {
  let t = String(text ?? '');
  t = t.replace(/```[\s\S]*?```/g, ' ');            // bloques de código
  t = t.replace(/`([^`]*)`/g, '$1');                // código inline
  t = t.replace(/!\[[^\]]*\]\([^)]*\)/g, ' ');      // imágenes markdown
  t = t.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');    // enlaces markdown → solo texto
  t = t.replace(/https?:\/\/\S+/g, ' ');            // URLs
  t = t.replace(/www\.\S+/g, ' ');
  t = t.replace(/^#{1,6}\s+/gm, '');                // encabezados markdown
  t = t.replace(/(\*\*|__)(.*?)\1/g, '$2');         // negrita
  t = t.replace(/(\*|_)(.*?)\1/g, '$2');            // cursiva
  t = t.replace(/^>\s?/gm, '');                     // citas
  // Emojis y símbolos decorativos (pictográficos, banderas, flechas, selectores, ZWJ)
  t = t.replace(/[\p{Extended_Pictographic}\u{1F1E6}-\u{1F1FF}\u{2190}-\u{2BFF}\u{FE00}-\u{FE0F}\u{200D}]/gu, ' ');
  t = t.replace(/[#*_~|>]+/g, ' ');                 // resto de símbolos markdown
  t = t.replace(/\s[-–—]\s/g, ', ');                // guiones sueltos → pausa natural
  t = t.replace(/[ \t]+/g, ' ');
  t = t.replace(/\s*\n\s*/g, ' ');
  return t.trim();
}

/**
 * Divide texto en trozos ≤ maxLen por oraciones (con fallback por palabras).
 * NUNCA concatena buffers crudos de WAV: cada trozo se sintetiza y se une con ffmpeg.
 */
export function splitIntoChunks(text, maxLen = 1000) {
  if (text.length <= maxLen) return [text];
  const sentences = text.match(/[^.!?…]+[.!?…]+["'”’»)\]]*\s*/gu) || [];
  const matched = sentences.join('');
  const tail = text.slice(matched.length).trim();
  const units = tail ? [...sentences.map((s) => s.trim()), tail] : sentences.map((s) => s.trim());

  const chunks = [];
  let cur = '';
  const pushWordSplit = (s) => {
    const words = s.split(/\s+/).filter(Boolean);
    let w = '';
    for (const word of words) {
      if ((w + ' ' + word).trim().length <= maxLen) w = (w + ' ' + word).trim();
      else { if (w) chunks.push(w); w = word.length > maxLen ? null : word; if (w === null) { /* palabra gigante: trocear duro */ for (let i = 0; i < word.length; i += maxLen) chunks.push(word.slice(i, i + maxLen)); w = ''; } }
    }
    if (w) chunks.push(w);
  };
  for (const s of units) {
    if (s.length > maxLen) { if (cur) { chunks.push(cur); cur = ''; } pushWordSplit(s); continue; }
    if ((cur + ' ' + s).trim().length <= maxLen) cur = (cur + ' ' + s).trim();
    else { if (cur) chunks.push(cur); cur = s; }
  }
  if (cur) chunks.push(cur);
  return chunks.filter((c) => c && c.trim().length > 0);
}

/** Duración real de un archivo de audio con ffprobe (segundos float). */
export async function probeDuration(file) {
  const { stdout } = await execFileAsync('ffprobe', [
    '-v', 'error',
    '-show_entries', 'format=duration',
    '-of', 'default=noprint_wrappers=1:nokey=1',
    file,
  ]);
  const s = parseFloat(String(stdout).trim());
  if (!Number.isFinite(s)) throw new Error(`ffprobe no devolvió duración válida para ${file}`);
  return s;
}

function clampSpeed(v) {
  const n = Number(v);
  if (!Number.isFinite(n)) return 1.0;
  return Math.min(2.0, Math.max(0.5, n));
}

function assertWav(buf) {
  if (!buf || buf.length < 128) throw new Error(`respuesta TTS vacía (${buf ? buf.length : 0} bytes)`);
  const head = buf.subarray(0, 4).toString('ascii');
  if (head !== 'RIFF') throw new Error(`respuesta TTS no es WAV válido (header=${JSON.stringify(head)})`);
}

/** Llamada TTS al SDK → Buffer WAV (pcm, 24000 Hz). */
async function ttsCall(text, cfg) {
  const zai = await getZAI();
  const voice = cfg?.tts?.voice || 'tongtong';
  const speed = clampSpeed(cfg?.tts?.speed ?? 1.0);
  const response = await zai.audio.tts.create({
    input: text,
    voice,
    speed,
    response_format: 'wav',
    stream: false,
  });
  const ab = await response.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(ab));
  assertWav(buffer);
  return buffer;
}

/** Une trozos WAV con ffmpeg concat demuxer → pcm_s16le 24000 Hz uniformes. */
async function joinWavParts(parts, outPath) {
  const listPath = `${outPath}.list.txt`;
  const lines = parts.map((p) => `file '${p.split("'").join("'\\''")}'`).join('\n');
  fs.writeFileSync(listPath, lines + '\n', 'utf8');
  try {
    await execFileAsync('ffmpeg', [
      '-y', '-v', 'error',
      '-f', 'concat', '-safe', '0', '-i', listPath,
      '-c:a', 'pcm_s16le', '-ar', '24000',
      outPath,
    ], FFMPEG_OPTS);
  } catch (e) {
    throw new Error(`ffmpeg no pudo unir ${parts.length} trozos: ${e.message}`);
  } finally {
    fs.rmSync(listPath, { force: true });
  }
}

// ---------- API principal ----------

/**
 * Sintetiza UNA sección → WAV en outPath. Devuelve duración real (segundos).
 * Si el texto > 1000 chars: divide por oraciones, genera WAV por trozo y los une con ffmpeg.
 * @param {string} text
 * @param {object} cfg
 * @param {string} outPath ruta destino del .wav
 * @returns {Promise<number>} segundos
 */
export async function synthesizeSection(text, cfg, outPath) {
  const clean = cleanTextForTTS(text);
  if (!clean || clean.length === 0) throw new Error('texto vacío tras limpieza para TTS');

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const chunks = splitIntoChunks(clean, 1000); // margen bajo el límite de 1024 del SDK

  if (chunks.length === 1) {
    const buf = await ttsCall(chunks[0], cfg);
    fs.writeFileSync(outPath, buf);
  } else {
    const parts = [];
    try {
      for (let c = 0; c < chunks.length; c++) {
        const partPath = `${outPath}.part_${c}.wav`;
        const buf = await ttsCall(chunks[c], cfg);
        fs.writeFileSync(partPath, buf);
        parts.push(partPath);
      }
      await joinWavParts(parts, outPath);
    } finally {
      for (const p of parts) fs.rmSync(p, { force: true });
    }
  }

  if (!fs.existsSync(outPath) || fs.statSync(outPath).size < 128) {
    throw new Error('el WAV final no se escribió correctamente');
  }
  const seconds = await probeDuration(outPath);
  if (seconds <= 0.05) throw new Error(`duración inválida (${seconds}s)`);
  return Math.round(seconds * 1000) / 1000;
}

/**
 * Sintetiza el audio de cada sección del guion.
 * WAVs en output/<YYYY-MM-DD>/audio/seg_00.wav, seg_01.wav, …
 * @param {Array<{kind:string,title?:string,text:string}>} sections
 * @param {object} cfg
 * @returns {Promise<Array<{index:number, path:string, seconds:number}>>}
 */
export async function makeAudio(sections, cfg) {
  if (!Array.isArray(sections) || sections.length === 0) {
    throw new Error('TTS_FAILED: no hay secciones para sintetizar');
  }
  const audioDir = path.join(outputDayDir(cfg), 'audio');
  fs.mkdirSync(audioDir, { recursive: true });

  const results = [];
  for (let i = 0; i < sections.length; i++) {
    const outPath = path.join(audioDir, `seg_${String(i).padStart(2, '0')}.wav`);
    const text = sections[i]?.text ?? '';
    let seconds = null;
    try {
      seconds = await synthesizeSection(text, cfg, outPath);
    } catch (first) {
      // Reintento único por sección (regla de resiliencia del pipeline)
      try {
        seconds = await synthesizeSection(text, cfg, outPath);
        console.log(`[MEDIA][TTS] Reintento OK para sección ${i} (${sections[i]?.kind})`);
      } catch (second) {
        throw new Error(`TTS_FAILED: sección ${i} (${sections[i]?.kind ?? 'desconocido'}): ${second.message}`);
      }
    }
    console.log(`[MEDIA][TTS] seg_${String(i).padStart(2, '0')}.wav → ${seconds.toFixed(2)}s (${sections[i]?.kind})`);
    results.push({ index: i, path: outPath, seconds });
  }
  return results;
}
