#!/usr/bin/env node
// ============================================================
// ZOLO NEWS — CLI del agente (125-A)
//   node agent.js run     [--dry-run] [--no-video] [--no-deliver]
//   node agent.js mood    <feliz|neutral|serio|motivado|bajoneado>
//   node agent.js schedule          (daemon node-cron)
//   node agent.js status            (mood, última corrida, alarma)
// Pipeline del run:
//   banner → config → mood → noticias → clima → curiosidades →
//   guion → artefactos → (medios) → (entrega) → state/lastRun.json
// ============================================================
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { loadConfig } from './src/config.js';
import { getMood, setMood, readMoodState } from './src/mood.js';
import { fetchNews } from './src/news.js';
import { fetchWeather } from './src/weather.js';
import { getCuriosities } from './src/curiosities.js';
import { buildNewscast } from './src/scriptWriter.js';
import { buildReportMd, saveRunArtifacts } from './src/report.js';
import { startScheduler, nextRunInfo } from './src/scheduler.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_DIR = path.join(__dirname, 'state');
const LAST_RUN_PATH = path.join(STATE_DIR, 'lastRun.json');
const VERSION = '1.0.0';

// ---------------- helpers de consola ----------------
const fmtMs = (ms) => (ms >= 1000 ? `${(ms / 1000).toFixed(1)}s` : `${Math.round(ms)}ms`);
const line = () => console.log('─'.repeat(64));

function banner() {
  console.log(`
  ============================================================
     Z O L O   N O T I C I A S   📰   v${VERSION}
     tu noticiero matutino autónomo · AliceLabs / MarketNow
  ============================================================`);
}

function showHelp() {
  console.log(`
ZOLO NEWS — noticiero matutino autónomo (v${VERSION})

Comandos:
  run [--dry-run] [--no-video] [--no-deliver]   genera el boletín de hoy
      --dry-run     solo núcleo (RSS/clima/guion/artefactos), sin medios ni entrega
      --no-video    salta imágenes de noticias y ensamblado de video (ahorra tiempo/costo)
      --no-deliver  no entrega por canales (email/Telegram/WhatsApp)
  mood <estado>     fija el humor: feliz|neutral|serio|motivado|bajoneado
  schedule          daemon: despierta solo a la hora de config.json (wakeTime)
  status            humor actual, última corrida y próxima alarma
  help              esta ayuda

Ejemplos:
  node agent.js run --dry-run
  node agent.js mood motivado
  node agent.js schedule
`);
}

// ---------------- pipeline principal ----------------
/**
 * Ejecuta el pipeline completo del noticiero.
 * @param {{dryRun?:boolean, noVideo?:boolean, noDeliver?:boolean}} opts
 * @returns {Promise<{ok:boolean, outDir?:string, error?:string}>}
 */
export async function runPipeline({ dryRun = false, noVideo = false, noDeliver = false } = {}) {
  const T0 = performance.now();

  // ---- 1) Config (esencial: aquí sí puede abortar el run)
  let tStage = performance.now();
  const cfg = loadConfig();
  console.log(`⚙️  Config lista: ${cfg.city.name} (${cfg.city.timezone}) · despertar ${cfg.wakeTime} · para ${cfg.user.name} (${fmtMs(performance.now() - tStage)})`);

  // ---- 2) Mood
  tStage = performance.now();
  const mood = getMood(cfg);
  console.log(`🎭 Humor del día: ${mood} (${fmtMs(performance.now() - tStage)})`);

  // ---- 3) Noticias (resiliente: feeds caídos → errors[])
  tStage = performance.now();
  const news = await fetchNews(cfg);
  console.log(`📰 Noticias: ${news.items.length} ítems de ${news.feedsOk}/${cfg.news.feeds.length} feeds OK${news.errors.length ? ` · ⚠️ caídos: ${news.errors.map((e) => e.feed).join(', ')}` : ''} (${fmtMs(performance.now() - tStage)})`);
  for (const err of news.errors) console.log(`   ⚠️  ${err.feed}: ${err.error}`);

  // ---- 4) Clima (Open-Meteo; degrada sin tumbar el run)
  tStage = performance.now();
  const weather = await fetchWeather(cfg.city);
  console.log(
    weather.degraded
      ? `🌤️  Clima: no disponible (${weather.error}) (${fmtMs(performance.now() - tStage)})`
      : `🌤️  Clima: ${weather.temp}°C · ${weather.condition} · máx ${weather.max}° / mín ${weather.min}° · lluvia ${weather.rainProb}% (${fmtMs(performance.now() - tStage)})`
  );

  // ---- 5) Curiosidades (Wikipedia + CoinGecko + humor LLM)
  tStage = performance.now();
  const curiosities = await getCuriosities(cfg, mood);
  const cBits = [];
  cBits.push(`${curiosities.onThisDay.length} eventos "tal día como hoy"`);
  cBits.push(curiosities.joke ? 'dato/chiste ✓' : 'sin dato/chiste');
  cBits.push(curiosities.quote ? 'frase ✓' : 'sin frase');
  if (curiosities.crypto) cBits.push(curiosities.crypto.map((c) => `${c.symbol} $${c.price_usd}`).join(' · '));
  console.log(`🧠 Curiosidades: ${cBits.join(' · ')} (${fmtMs(performance.now() - tStage)})`);

  // ---- 6) Guion (LLM ×2 → fallback determinista)
  tStage = performance.now();
  const newscast = await buildNewscast({ cfg, news, weather, curiosities, mood });
  const chars = newscast.sections.map((s) => s.text.length);
  const maxChars = Math.max(...chars, 0);
  console.log(`🎬 Guion: motor ${newscast.meta.engine} · ${newscast.sections.length} secciones · text máx ${maxChars} chars${maxChars > 600 ? ' ⚠️' : ''} (${fmtMs(performance.now() - tStage)})`);
  if (newscast.meta.note) console.log(`   ℹ️  ${newscast.meta.note}`);

  // ---- 7) Reporte markdown
  tStage = performance.now();
  const reportMd = buildReportMd({ cfg, sections: newscast.sections, news, weather, curiosities, mood, meta: newscast.meta });

  // ---- 8) Artefactos (output/<fecha>/)
  tStage = performance.now();
  const artifacts = saveRunArtifacts({ cfg, newscast, reportMd, data: { news, weather, curiosities } });
  console.log(`💾 Artefactos guardados: ${artifacts.outDir} (${fmtMs(performance.now() - tStage)})`);

  // ---- 9) Medios (solo fuera de dry-run; stubs → aviso y seguimos)
  let avatar = null;
  let audio = null;
  let images = null;
  let videoPath = null;
  let audioPath = null;
  const mediaNotes = [];

  if (!dryRun) {
    tStage = performance.now();
    try {
      const media = await import('./src/media/index.js');
      try {
        avatar = await media.makeAvatar(cfg);
        console.log(`🧑‍💼 Avatar: ${avatar?.path ?? '?'}`);
      } catch (err) {
        mediaNotes.push(`avatar (${err?.message ?? err})`);
      }
      try {
        audio = await media.makeAudio(newscast.sections, cfg);
        // audioPath informativo para entrega: primer fragmento (125-B puede devolver un track único más adelante)
        audioPath = Array.isArray(audio) && audio[0]?.path ? audio[0].path : null;
        console.log(`🔊 Audio: ${Array.isArray(audio) ? audio.length : 0} fragmentos${audioPath ? ` · ${audioPath}` : ''}`);
      } catch (err) {
        mediaNotes.push(`audio (${err?.message ?? err})`);
      }
      if (!noVideo) {
        try {
          images = await media.makeNewsImages(newscast.sections, cfg);
          console.log(`🖼️  Imágenes: ${Array.isArray(images) ? images.length : 0}`);
        } catch (err) {
          mediaNotes.push(`imágenes (${err?.message ?? err})`);
        }
        try {
          const video = await media.makeVideo({ sections: newscast.sections, audio, avatar, images }, cfg);
          videoPath = video?.videoPath ?? null;
          if (video?.reason) mediaNotes.push(`video (${video.reason})`);
          if (videoPath) console.log(`🎥 Video: ${videoPath}`);
        } catch (err) {
          mediaNotes.push(`video (${err?.message ?? err})`);
        }
      } else {
        mediaNotes.push('video omitido por --no-video');
      }
    } catch (err) {
      mediaNotes.push(`módulo de medios (${err?.message ?? err})`);
    }
    if (mediaNotes.length) console.log(`⚠️  medios no disponibles: ${mediaNotes.join('; ')}`);
    console.log(`🎞️  Etapa de medios terminada (${fmtMs(performance.now() - tStage)})`);
  } else {
    console.log('🏃 dry-run: se omiten medios y entrega');
  }

  // ---- 10) Entrega multicanal (NUNCA tumba el run)
  let delivery = null;
  if (!dryRun && !noDeliver) {
    tStage = performance.now();
    try {
      const deliveryMod = await import('./src/delivery/index.js');
      delivery = await deliveryMod.deliverAll({ reportMd, videoPath, audioPath, sections: newscast.sections, cfg });
      console.log(`📨 Entrega (${fmtMs(performance.now() - tStage)}):`);
      for (const canal of ['email', 'telegram', 'whatsapp']) {
        const r = delivery?.[canal];
        if (!r) continue;
        const estado = r.sent ? '✅ enviado' : r.skipped ? '⏭️  omitido' : '❌ falló';
        const extra = r.info ?? r.error ?? '';
        console.log(`   ${canal}: ${estado}${extra ? ` — ${extra}` : ''}`);
      }
      for (const s of delivery?.social ?? []) {
        console.log(`   ${s.channel}: ${s.status}${s.note ? ` — ${s.note}` : ''}`);
      }
    } catch (err) {
      console.log(`⚠️  entrega falló (el run continúa): ${err?.message ?? err}`);
    }
  }

  // ---- 11) state/lastRun.json
  tStage = performance.now();
  const lastRun = {
    date: newscast.meta.date,
    mood,
    engine: newscast.meta.engine,
    counts: { news: (news.items ?? []).length, sections: newscast.sections.length },
    artifacts: {
      outDir: artifacts.outDir,
      scriptPath: artifacts.scriptPath,
      scriptMdPath: artifacts.scriptMdPath,
      reportPath: artifacts.reportPath,
      audioPath,
      videoPath,
    },
    newsErrors: news.errors,
    delivery,
    flags: { dryRun, noVideo, noDeliver },
    finishedAt: new Date().toISOString(),
  };
  mkdirSync(STATE_DIR, { recursive: true });
  writeFileSync(LAST_RUN_PATH, JSON.stringify(lastRun, null, 2) + '\n', 'utf8');
  console.log(`📌 Estado del run guardado en state/lastRun.json (${fmtMs(performance.now() - tStage)})`);

  // ---- Resumen final
  line();
  console.log(`✅ Boletín listo: ${artifacts.outDir}`);
  console.log(`   🗞️  ${news.items.length} noticias · ⚙️ motor ${newscast.meta.engine} · 🎭 humor ${mood}`);
  if (dryRun) console.log('   🏃 modo dry-run (sin video ni entrega)');
  console.log(`⏱️  Pipeline completo: ${fmtMs(performance.now() - T0)}`);
  line();

  return { ok: true, outDir: artifacts.outDir };
}

// ---------------- comandos ----------------
async function cmdMood(moodArg) {
  const cfg = loadConfig();
  if (!moodArg) {
    console.log(`Uso: node agent.js mood <estado>\nPermitidos: ${cfg.mood.allowed.join(', ')}`);
    process.exitCode = 1;
    return;
  }
  try {
    const saved = setMood(moodArg, cfg);
    console.log(`🎭 Humor actualizado a "${saved.mood}" (${saved.setAt})`);
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exitCode = 1;
  }
}

async function cmdStatus() {
  const cfg = loadConfig();
  line();
  console.log(`📰 ZOLO NEWS · estado`);
  line();
  console.log(`👤 Usuario: ${cfg.user.name} · Ciudad: ${cfg.city.name} (${cfg.city.timezone})`);
  console.log(`⏰ Despertar configurado: ${cfg.wakeTime}`);

  const moodState = readMoodState();
  const mood = getMood(cfg);
  console.log(`🎭 Humor actual: ${mood}${moodState?.setAt ? ` (desde ${moodState.setAt})` : ' (por defecto)'}`);

  const next = nextRunInfo(cfg);
  console.log(`📅 Próxima alarma: ${next.label}`);

  if (existsSync(LAST_RUN_PATH)) {
    try {
      const last = JSON.parse(readFileSync(LAST_RUN_PATH, 'utf8'));
      console.log(`🔎 Última corrida: ${last.date ?? '?'} · humor ${last.mood ?? '?'} · motor ${last.engine ?? '?'} · ${last.counts?.news ?? 0} noticias`);
      if (last.artifacts?.outDir) console.log(`📂 Artefactos: ${last.artifacts.outDir}`);
      if (last.artifacts?.videoPath) console.log(`🎥 Video: ${last.artifacts.videoPath}`);
      if (Array.isArray(last.newsErrors) && last.newsErrors.length) {
        console.log(`⚠️  Feeds caídos esa corrida: ${last.newsErrors.map((e) => e.feed).join(', ')}`);
      }
      console.log(`🕒 Terminó: ${last.finishedAt ?? '?'}`);
    } catch (err) {
      console.log(`⚠️  lastRun.json ilegible: ${err.message}`);
    }
  } else {
    console.log('🔎 Última corrida: (ninguna todavía — corre `node agent.js run`)');
  }
  line();
}

async function cmdSchedule() {
  const cfg = loadConfig();
  banner();
  console.log('Daemon activo: ZOLO NEWS despertará solo cada mañana.');
  console.log('Presiona Ctrl+C para apagarlo.');
  startScheduler(cfg, () => runPipeline({ dryRun: false, noVideo: false, noDeliver: false }));

  process.on('SIGINT', () => {
    console.log('\n👋 ZOLO NEWS daemon apagado. Hasta mañana.');
    process.exit(0);
  });
}

async function cmdRun(flagSet) {
  banner();
  return runPipeline({
    dryRun: flagSet.has('--dry-run'),
    noVideo: flagSet.has('--no-video'),
    noDeliver: flagSet.has('--no-deliver'),
  });
}

// ---------------- main ----------------
async function main() {
  const args = process.argv.slice(2);
  const command = (args[0] ?? 'help').toLowerCase();
  const flagSet = new Set(args.slice(1).filter((a) => a.startsWith('--')));

  try {
    switch (command) {
      case 'run':
        await cmdRun(flagSet);
        break;
      case 'mood':
        await cmdMood(args[1]);
        break;
      case 'schedule':
        await cmdSchedule();
        break;
      case 'status':
        await cmdStatus();
        break;
      case 'help':
      case '--help':
      case '-h':
      default:
        banner();
        showHelp();
        if (!['help', '--help', '-h'].includes(command)) {
          console.log(`⚠️  Comando desconocido: "${command}"`);
          process.exitCode = 1;
        }
        break;
    }
  } catch (err) {
    console.error(`❌ Error fatal: ${err?.message ?? err}`);
    if (err?.stack && process.env.ZOLO_DEBUG) console.error(err.stack);
    process.exitCode = 1;
  }
}

main();
