// ============================================================
// ZOLO NEWS — Ensamblador de video del noticiero (MP4 1280x720)
// Subagente 125-B · Pipeline de medios
// - makeVideo({sections, audio, avatar, images}, cfg) → {videoPath} | {videoPath:null, reason}
// Estrategia:
//   1. bulletin.wav  = concat demuxer de los WAV por sección (-c copy, fallback re-encode)
//   2. slide PNGs    = un slide por sección, cada uno dura audio[i].seconds
//                      · intro:  fondo oscuro + avatar + "ZOLO NOTICIAS" + fecha en español
//                      · news:   imagen a 1280x720 (scale+crop) + banda inferior con caption
//                                (drawtext textfile=, fontsize 40, box black@0.55, 2 líneas máx)
//                      · weather/curious: fondo studio + título (textfile)
//                      · outro:  avatar + "ZOLO Noticias · <fecha>" + "Tu resumen diario está listo"
//   3. slides.txt    = concat demuxer de imágenes con duration por slide (última repetida)
//   4. mux final     = libx264 + yuv420p + r 30 + aac 192k + -shortest
// Reglas: NUNCA lanza; ante fallo → {videoPath:null, reason:'FFMPEG_FAILED: …'}
// ============================================================

import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';

const execFileAsync = promisify(execFile);
const FFMPEG_OPTS = { maxBuffer: 32 * 1024 * 1024 };
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

async function ff(args) {
  await execFileAsync('ffmpeg', args, FFMPEG_OPTS);
}

async function probeDuration(file) {
  const { stdout } = await execFileAsync('ffprobe', [
    '-v', 'error', '-show_entries', 'format=duration',
    '-of', 'default=noprint_wrappers=1:nokey=1', file,
  ], FFMPEG_OPTS);
  const s = parseFloat(String(stdout).trim());
  return Number.isFinite(s) ? s : NaN;
}

// ---------- Helpers de presentación ----------

/** Fuente TTF para drawtext: cfg.video.font con fallback DejaVu. */
function resolveFont(cfg) {
  const candidates = [
    cfg?.video?.font,
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
  ].filter(Boolean);
  for (const f of candidates) {
    if (fs.existsSync(f)) return f;
  }
  throw new Error('no se encontró fuente TTF (revisa cfg.video.font / fc-list DejaVu)');
}

/** Fecha en español (capitalizada) en la zona de la ciudad: "Viernes, 24 de octubre de 2026". */
function fechaBonita(cfg) {
  const tz = cfg?.city?.timezone || 'America/Guayaquil';
  const s = new Intl.DateTimeFormat('es-EC', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: tz,
  }).format(new Date());
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Envuelve texto en ≤ maxLines líneas de ≤ maxChars (con elipsis si sobra). */
function wrapText(text, maxChars, maxLines) {
  const words = String(text ?? '').replace(/\s+/g, ' ').trim().split(' ').filter(Boolean);
  if (!words.length) return [];
  const lines = [];
  let cur = '';
  for (const w of words) {
    const cand = cur ? `${cur} ${w}` : w;
    if (cand.length <= maxChars) { cur = cand; continue; }
    lines.push(cur);
    cur = w;
    if (lines.length >= maxLines) break;
  }
  if (lines.length < maxLines && cur) lines.push(cur);
  if (lines.length === maxLines && lines.join(' ').length < words.join(' ').length) {
    let last = lines[maxLines - 1] ?? '';
    if (last.length > maxChars - 1) last = last.slice(0, maxChars - 1);
    last = last.replace(/\s+\S*$/, '');
    lines[maxLines - 1] = `${last}…`;
  }
  return lines;
}

/** Escribe un archivo de texto temporal para drawtext (evita escapado de tildes/comillas). */
function tmpText(dir, name, content) {
  const p = path.join(dir, name);
  fs.writeFileSync(p, content, 'utf8');
  return p;
}

/** Filtro drawtext con textfile (contenido nunca viaja inline en el filtro). */
function drawtext(font, textfile, { size, color = 'white', x = '(w-text_w)/2', y, box = true, spacing = 0 }) {
  const opts = [
    `fontfile=${font}`,
    `textfile=${textfile}`,
    `expansion=none`, // el contenido del textfile es literal (tildes, %, comillas)
    `fontsize=${size}`,
    `fontcolor=${color}`,
    `x=${x}`,
    `y=${y}`,
  ];
  if (spacing) opts.push(`line_spacing=${spacing}`);
  if (box) opts.push('box=1', 'boxcolor=black@0.55', 'boxborderw=18');
  return `drawtext=${opts.join(':')}`;
}

/** Escala+recorte centrado de cualquier imagen a WxH. */
const COVER = (W, H) => `scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H}`;

// ---------- Constructores de slides ----------

/** Slide intro: fondo oscuro + avatar + "ZOLO NOTICIAS" + fecha en español. */
async function slideIntro(outPath, avatarPath, font, tmpDir, dateStr, W, H) {
  const tTitle = tmpText(tmpDir, 'tmp_intro_title.txt', 'ZOLO NOTICIAS');
  const tDate = tmpText(tmpDir, 'tmp_intro_date.txt', dateStr);
  const avH = 400;
  const fc = [
    `[1:v]scale=-2:${avH}[av]`,
    `[0:v][av]overlay=(W-w)/2:${H - avH - 30}`,
    drawtext(font, tTitle, { size: 76, y: '56' }),
    drawtext(font, tDate, { size: 34, y: '196', color: '0xBBD9EE' }),
  ].join(',');
  await ff(['-y', '-v', 'error',
    '-f', 'lavfi', '-i', `color=c=0x0A1A2F:s=${W}x${H}`,
    '-i', avatarPath,
    '-filter_complex', fc,
    '-frames:v', '1', outPath]);
}

/** Slide noticia: imagen a pantalla + banda inferior con caption (2 líneas máx). */
async function slideNews(outPath, imgPath, font, tmpDir, caption, W, H) {
  const lines = wrapText(caption, 46, 2);
  let dt = '';
  if (lines.length > 0) {
    const tCap = tmpText(tmpDir, 'tmp_caption.txt', lines.join('\n'));
    dt = `,${drawtext(font, tCap, { size: 40, y: 'h-text_h-52', spacing: 10 })}`;
  }
  const fc = `[0:v]${COVER(W, H)}${dt}`;
  await ff(['-y', '-v', 'error', '-i', imgPath, '-filter_complex', fc, '-frames:v', '1', outPath]);
}

/** Slide clima / curioso / otros: fondo de estudio + etiqueta + título. */
async function slideStudio(outPath, bgPath, font, tmpDir, label, title, W, H) {
  const tLbl = tmpText(tmpDir, 'tmp_label.txt', label);
  const tTit = tmpText(tmpDir, 'tmp_studio_title.txt', wrapText(title, 40, 2).join('\n') || label);
  const fc = [
    `[0:v]${COVER(W, H)}`,
    drawtext(font, tLbl, { size: 30, y: 'h/2-140', color: '0x7FD1D8' }),
    drawtext(font, tTit, { size: 48, y: 'h/2-60', spacing: 12 }),
  ].join(',');
  await ff(['-y', '-v', 'error', '-i', bgPath, '-filter_complex', fc, '-frames:v', '1', outPath]);
}

/** Slide de cierre: avatar + "ZOLO Noticias · <fecha>" + "Tu resumen diario está listo". */
async function slideOutro(outPath, avatarPath, font, tmpDir, dateStr, W, H) {
  const tLine1 = tmpText(tmpDir, 'tmp_outro1.txt', `ZOLO Noticias · ${dateStr}`);
  const tLine2 = tmpText(tmpDir, 'tmp_outro2.txt', 'Tu resumen diario está listo');
  const avH = 380;
  const fc = [
    `[1:v]scale=-2:${avH}[av]`,
    `[0:v][av]overlay=(W-w)/2:${H - avH - 40}`,
    drawtext(font, tLine1, { size: 44, y: '70' }),
    drawtext(font, tLine2, { size: 32, y: '150', color: '0xBBD9EE' }),
  ].join(',');
  await ff(['-y', '-v', 'error',
    '-f', 'lavfi', '-i', `color=c=0x0A1A2F:s=${W}x${H}`,
    '-i', avatarPath,
    '-filter_complex', fc,
    '-frames:v', '1', outPath]);
}

// ---------- Concatenación de audio ----------

/** Une los WAV por sección → bulletin.wav (concat demuxer; -c copy con fallback de re-encode). */
async function concatAudio(wavFiles, outWav, tmpDir) {
  if (wavFiles.length === 1) {
    fs.copyFileSync(wavFiles[0], outWav);
    return;
  }
  const list = path.join(tmpDir, 'tmp_audio_list.txt');
  fs.writeFileSync(list, wavFiles.map((p) => `file '${p}'`).join('\n') + '\n', 'utf8');
  try {
    try {
      await ff(['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', outWav]);
    } catch (e) {
      // Si algún WAV difiere en parámetros, normalizamos a pcm_s16le 24000 Hz
      console.warn(`[MEDIA][VIDEO] concat -c copy falló (${e.message}); re-codificando a pcm_s16le/24000…`);
      await ff(['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list,
        '-c:a', 'pcm_s16le', '-ar', '24000', outWav]);
    }
  } finally {
    fs.rmSync(list, { force: true });
  }
}

// ---------- API principal ----------

/**
 * Ensambla el video del noticiero. NUNCA lanza.
 * @param {{sections:Array, audio:Array<{index,path,seconds}>, avatar:{path:string}|string, images:Array<{index,path}>}} bundle
 * @param {object} cfg
 * @returns {Promise<{videoPath: string|null, reason?: string}>}
 */
export async function makeVideo(bundle, cfg) {
  const tmpDir = path.join(path.resolve(ROOT, cfg?.outputRoot || 'output'), cfg?.outputDate || todayLocal(cfg));
  const tmpFiles = [];
  try {
    const W = Number(cfg?.video?.width) || 1280;
    const H = Number(cfg?.video?.height) || 720;
    const font = resolveFont(cfg);
    fs.mkdirSync(tmpDir, { recursive: true });

    const sections = Array.isArray(bundle?.sections) ? bundle.sections : [];
    const audio = Array.isArray(bundle?.audio) ? [...bundle.audio].sort((a, b) => a.index - b.index) : [];
    const avatarPath = typeof bundle?.avatar === 'string' ? bundle.avatar : bundle?.avatar?.path;
    const imageByIndex = new Map((Array.isArray(bundle?.images) ? bundle.images : []).map((im) => [im.index, im.path]));

    if (!audio.length) return { videoPath: null, reason: 'FFMPEG_FAILED: no hay audio para el video' };
    if (!avatarPath || !fs.existsSync(avatarPath)) return { videoPath: null, reason: 'FFMPEG_FAILED: avatar no disponible' };
    const missing = audio.find((a) => !a.path || !fs.existsSync(a.path));
    if (missing) return { videoPath: null, reason: `FFMPEG_FAILED: falta el audio de la sección ${missing.index}` };

    const bg = imageByIndex.get(audio[0].index); // respaldo genérico si falta una imagen
    const dateStr = fechaBonita(cfg);

    // 1) bulletin.wav — concat de los WAV de secciones (mismo formato)
    const outWav = path.join(tmpDir, 'bulletin.wav');
    await concatAudio(audio.map((a) => a.path), outWav, tmpDir);
    const wavSeconds = await probeDuration(outWav);
    console.log(`[MEDIA][VIDEO] bulletin.wav listo (${wavSeconds.toFixed(2)}s)`);

    // 2) Un slide PNG 1280x720 por sección, alineado al audio
    const slides = [];
    for (let pos = 0; pos < audio.length; pos++) {
      const a = audio[pos];
      const s = sections[a.index] ?? {};
      const kind = String(s.kind ?? 'news');
      const slidePath = path.join(tmpDir, `slide_${pos}.png`);
      const img = imageByIndex.get(a.index) ?? bg;

      if (kind === 'intro') {
        await slideIntro(slidePath, avatarPath, font, tmpDir, dateStr, W, H);
      } else if (kind === 'outro') {
        await slideOutro(slidePath, avatarPath, font, tmpDir, dateStr, W, H);
      } else if (kind === 'news') {
        const caption = s.caption || s.title || '';
        await slideNews(slidePath, img, font, tmpDir, caption, W, H);
      } else {
        const label = kind === 'weather' ? 'EL CLIMA HOY' : kind === 'curious' ? 'DATO CURIOSO' : 'ZOLO NOTICIAS';
        const title = s.title || s.caption || 'ZOLO NOTICIAS';
        await slideStudio(slidePath, img, font, tmpDir, label, title, W, H);
      }
      slides.push({ file: `slide_${pos}.png`, duration: Math.max(0.5, Number(a.seconds) || 1) });
      console.log(`[MEDIA][VIDEO] slide_${pos}.png (${kind}, ${a.seconds.toFixed(2)}s)`);
    }

    // 3) slides.txt — concat demuxer de imágenes con duration por slide (última imagen repetida)
    const slidesTxt = path.join(tmpDir, 'slides.txt');
    const lines = ['ffconcat version 1.0'];
    slides.forEach((sl, i) => {
      lines.push(`file '${sl.file}'`);
      lines.push(`duration ${(i === slides.length - 1 ? sl.duration + 1.0 : sl.duration).toFixed(3)}`);
    });
    lines.push(`file '${slides[slides.length - 1].file}'`); // patrón del demuxer: repetir la última
    fs.writeFileSync(slidesTxt, lines.join('\n') + '\n', 'utf8');

    // 4) Mux final: video H.264 30fps + audio AAC (total ≈ suma de segundos de audio).
    //    Evidencia empírica (ffmpeg 7.1.5, demuxer concat de imágenes):
    //    · `-r 30` como opción de salida solo duplica la PRIMERA slide (21.87s de 49.7s);
    //      el filtro `fps=30` sí duplica el timeline completo → se usa fps=30.
    //    · `-shortest` es inestable aquí (una corrida sobrepasó a 77.3s, otra cortó a 21.87s
    //      por su lógica de buffer) → se elimina.
    //    · `-t` corta EXACTO a la duración del audio: el patrón "última imagen repetida"
    //      hereda la última duration y estiraría el video; -t lo garantiza preciso.
    const outMp4 = path.join(tmpDir, 'bulletin.mp4');
    await ff(['-y', '-v', 'error',
      '-f', 'concat', '-safe', '0', '-i', slidesTxt,
      '-i', outWav,
      '-vf', 'fps=30',
      '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
      '-c:a', 'aac', '-b:a', '192k',
      '-movflags', '+faststart',
      '-t', (wavSeconds + 0.05).toFixed(3),
      outMp4]);

    const dur = await probeDuration(outMp4);
    const kb = (fs.statSync(outMp4).size / 1024).toFixed(1);
    console.log(`[MEDIA][VIDEO] bulletin.mp4 listo (${kb} KB, ${dur.toFixed(2)}s) → ${outMp4}`);

    return { videoPath: outMp4 };
  } catch (e) {
    console.error(`[MEDIA][VIDEO] ERROR: ${e.message}`);
    return { videoPath: null, reason: `FFMPEG_FAILED: ${e.message}` };
  } finally {
    // Limpieza de textfiles temporales (los slides PNG y bulletin.* se conservan)
    try {
      for (const f of fs.readdirSync(tmpDir)) {
        if (f.startsWith('tmp_')) fs.rmSync(path.join(tmpDir, f), { force: true });
      }
    } catch { /* limpieza best-effort */ }
  }
}

// Fecha local YYYY-MM-DD (duplicado mínimo para mantener el módulo autocontenido)
function todayLocal(cfg) {
  const tz = cfg?.city?.timezone || 'America/Guayaquil';
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date());
  const get = (t) => parts.find((p) => p.type === t)?.value ?? '00';
  return `${get('year')}-${get('month')}-${get('day')}`;
}
