// ============================================================
// ZOLO NEWS — Reporte markdown + artefactos del run (125-A)
// buildReportMd({cfg, sections, news, weather, curiosities, mood, meta})
//   → string markdown en español
// saveRunArtifacts({cfg, newscast, reportMd, data})
//   → crea output/<YYYY-MM-DD>/ (America/Guayaquil) y escribe
//     script.json, script.md y report.md
//   → { outDir, scriptPath, reportPath }
// ============================================================
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { fechaLarga, todayKey, truncate } from './scriptWriter.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUTPUT_DIR = path.join(ROOT, 'output');

const MOOD_EMOJI = {
  feliz: '😄', neutral: '🙂', serio: '🧐', motivado: '💪', bajoneado: '🤍',
};

function esc(s) {
  return String(s ?? '').replace(/\[/g, '\\[').replace(/\]/g, '\\]');
}

/** Hora legible "HH:MM" en la timezone de la ciudad. */
function horaActual(tz) {
  const p = new Intl.DateTimeFormat('en-CA', { timeZone: tz, hour: '2-digit', minute: '2-digit', hour12: false })
    .formatToParts(new Date())
    .filter((x) => x.type !== 'literal')
    .reduce((acc, x) => ((acc[x.type] = x.value), acc), {});
  return `${p.hour}:${p.minute}`;
}

/**
 * Construye el reporte markdown bonito del boletín.
 */
export function buildReportMd({ cfg, sections, news, weather, curiosities, mood, meta }) {
  const fecha = fechaLarga(cfg.city.timezone);
  const emo = MOOD_EMOJI[mood] ?? '🙂';
  const items = news?.items ?? [];
  const lines = [];

  lines.push(`# 📰 ZOLO Noticias — ${fecha}`);
  lines.push('');
  lines.push(
    `> 🌍 ${weather?.city ?? cfg.city.name} · 🕒 ${horaActual(cfg.city.timezone)} (${cfg.city.timezone}) · ${emo} humor: **${mood}** · ⚙️ motor: **${meta?.engine ?? 'n/d'}**`
  );
  lines.push('');

  // ---- TL;DR (3 bullets)
  lines.push('## ⚡ TL;DR');
  lines.push('');
  const tldr = items.slice(0, 3);
  if (tldr.length === 0) {
    lines.push('- Hoy no hubo noticias disponibles de los feeds; revisa los errores del run.');
  } else {
    for (const it of tldr) lines.push(`- ${esc(truncate(it.title, 140))}`);
  }
  lines.push('');

  // ---- Noticias
  lines.push('## 🗞️ Noticias');
  lines.push('');
  const newsSections = sections.filter((s) => s.kind === 'news');
  if (newsSections.length === 0) {
    lines.push('_(sin noticias en esta emisión)_');
    lines.push('');
  } else {
    newsSections.forEach((s, i) => {
      lines.push(`### ${i + 1}. ${esc(s.title ?? 'Noticia')}`);
      lines.push('');
      lines.push(s.text);
      lines.push('');
      const linkParts = [];
      if (s.url) linkParts.push(`🔗 [${esc(s.source ?? 'fuente')}](${s.url})`);
      else if (s.source) linkParts.push(`🔗 ${esc(s.source)}`);
      if (s.caption) linkParts.push(`🎬 _caption:_ "${esc(s.caption)}"`);
      if (linkParts.length) {
        lines.push(linkParts.join(' · '));
        lines.push('');
      }
    });
  }

  // ---- Clima
  lines.push(`## 🌤️ Clima en ${weather?.city ?? cfg.city.name}`);
  lines.push('');
  if (weather?.degraded) {
    lines.push(`⚠️ Consulta fallida (${weather.error ?? 'error desconocido'}). ${weather.advice ?? ''}`);
  } else {
    const parts = [];
    if (Number.isFinite(weather?.temp)) {
      parts.push(`Ahora: **${weather.temp}°C**${Number.isFinite(weather.feelsLike) ? ` (sensación ${weather.feelsLike}°C)` : ''} — ${weather.condition}`);
    }
    if (Number.isFinite(weather?.max) || Number.isFinite(weather?.min)) {
      parts.push(`Máx **${weather.max ?? '—'}°C** / Mín **${weather.min ?? '—'}°C**`);
    }
    if (Number.isFinite(weather?.rainProb)) parts.push(`💧 lluvia: **${weather.rainProb}%**`);
    if (Number.isFinite(weather?.humidity)) parts.push(`humedad: ${weather.humidity}%`);
    if (Number.isFinite(weather?.wind)) parts.push(`💨 viento: ${weather.wind} km/h`);
    for (const p of parts) lines.push(`- ${p}`);
  }
  if (weather?.advice) {
    lines.push('');
    lines.push(`💡 **Consejo:** ${weather.advice}`);
  }
  lines.push('');

  // ---- Curiosidades
  lines.push('## 🧠 Curiosidades');
  lines.push('');
  const otd = curiosities?.onThisDay ?? [];
  if (otd.length) {
    lines.push('**Tal día como hoy**');
    lines.push('');
    for (const ev of otd) lines.push(`- **${ev.year}** — ${ev.text}`);
    lines.push('');
  }
  if (curiosities?.joke) {
    lines.push(`😄 **Dato/chiste:** ${curiosities.joke}`);
    lines.push('');
  }
  if (curiosities?.quote) {
    lines.push(`📜 **Frase del día:** ${curiosities.quote}`);
    lines.push('');
  }
  if (Array.isArray(curiosities?.crypto) && curiosities.crypto.length) {
    lines.push(`🪙 **Cripto (USD):** ${curiosities.crypto.map((c) => `${c.symbol} $${c.price_usd.toLocaleString('es-EC')}`).join(' · ')}`);
    lines.push('');
  }
  if (!otd.length && !curiosities?.joke && !curiosities?.quote && !curiosities?.crypto) {
    lines.push('_(sin curiosidades esta mañana — las fuentes no respondieron)_');
    lines.push('');
  }

  // ---- Firma
  lines.push('---');
  lines.push('');
  lines.push(`_ZOLO Noticias · tu noticiero matutino autónomo · preparado con 🤖 para **${cfg.user.name}** · ${fecha}_`);
  lines.push('');

  return lines.join('\n');
}

/**
 * Versión "legible" del guion (para locución o revisión rápida).
 */
function buildScriptMd(newscast, cfg) {
  const fecha = fechaLarga(cfg.city.timezone);
  const lines = [];
  lines.push(`# 🎙️ Guion — ZOLO Noticias · ${fecha}`);
  lines.push('');
  lines.push(`> humor: ${newscast.meta.mood} · motor: ${newscast.meta.engine} · secciones: ${newscast.sections.length}`);
  lines.push('');
  newscast.sections.forEach((s, i) => {
    const titulos = {
      intro: 'INTRO', news: `NOTICIA ${s.title ?? ''}`.trim(), weather: 'CLIMA', curious: 'CURIOSIDADES', outro: 'DESPEDIDA',
    };
    lines.push(`## [${i + 1}] ${titulos[s.kind] ?? s.kind.toUpperCase()}`);
    if (s.kind !== 'news' && s.title) lines.push(`**${s.title}**`);
    lines.push('');
    lines.push(`> ${s.text}`);
    lines.push('');
    if (s.kind === 'news') {
      if (s.source) lines.push(`- Fuente: ${s.source}`);
      if (s.url) lines.push(`- URL: ${s.url}`);
      if (s.caption) lines.push(`- Caption video: "${s.caption}"`);
      if (s.imagePrompt) lines.push(`- ImagePrompt: ${s.imagePrompt}`);
      lines.push('');
    }
  });
  lines.push('---');
  lines.push('_ZOLO Noticias · fin del guion_');
  lines.push('');
  return lines.join('\n');
}

/** Directorio de salida del día: output/YYYY-MM-DD (America/Guayaquil). */
export function outDirForDay(cfg) {
  const day = todayKey(cfg.city.timezone);
  return path.join(OUTPUT_DIR, day);
}

/**
 * Persiste los 3 artefactos del run.
 * @param {{cfg:object, newscast:object, reportMd:string, data?:object}} args
 * @returns {{outDir:string, scriptPath:string, reportPath:string, scriptMdPath:string}}
 */
export function saveRunArtifacts({ cfg, newscast, reportMd, data }) {
  if (!newscast || !Array.isArray(newscast.sections)) {
    throw new Error('saveRunArtifacts: newscast inválido (sin sections)');
  }
  const outDir = outDirForDay(cfg);
  mkdirSync(outDir, { recursive: true });

  const scriptPath = path.join(outDir, 'script.json');
  const scriptMdPath = path.join(outDir, 'script.md');
  const reportPath = path.join(outDir, 'report.md');

  writeFileSync(scriptPath, JSON.stringify(newscast, null, 2) + '\n', 'utf8');
  writeFileSync(scriptMdPath, buildScriptMd(newscast, cfg), 'utf8');
  writeFileSync(reportPath, reportMd ?? '', 'utf8');

  return { outDir, scriptPath, reportPath, scriptMdPath };
}

export default { buildReportMd, saveRunArtifacts };
