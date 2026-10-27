// ============================================================
// ZOLO NEWS — Scheduler node-cron (125-A)
// - startScheduler(cfg, runFn): despierta el noticiero a cfg.wakeTime
//   en cfg.city.timezone; flag anti-solape; devuelvo el task.
// - cronExprFromWake("HH:MM") → "MM HH * * *"
// - nextRunInfo(cfg) → { iso, label } de la próxima ejecución.
// ============================================================
import cron from 'node-cron';

/** "06:30" → "30 6 * * *" (valida formato). Lanza si es inválido. */
export function cronExprFromWake(wakeTime) {
  const m = /^([01]\d|2[0-3]):([0-5]\d)$/.exec(String(wakeTime ?? '').trim());
  if (!m) throw new Error(`wakeTime inválido: "${wakeTime}" (se espera HH:MM, ej. 06:30)`);
  const hh = String(Number(m[1])); // sin cero inicial para cron
  const mm = String(Number(m[2]));
  return `${mm} ${hh} * * *`;
}

/** Partes numéricas de "ahora" en una timezone. */
function nowInTz(tz) {
  const p = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hour12: false,
  })
    .formatToParts(new Date())
    .filter((x) => x.type !== 'literal')
    .reduce((acc, x) => ((acc[x.type] = x.value), acc), {});
  return { y: +p.year, mo: +p.month, d: +p.day, h: +p.hour, mi: +p.minute };
}

/**
 * Próxima ejecución de la alarma diaria en la timezone de la ciudad.
 * @returns {{iso: string, label: string}}
 */
export function nextRunInfo(cfg) {
  const tz = cfg.city.timezone;
  const [hh, mm] = String(cfg.wakeTime).split(':').map(Number);
  const now = nowInTz(tz);

  const pad = (n) => String(n).padStart(2, '0');
  let y = now.y, mo = now.mo, d = now.d;
  if (hh * 60 + mm <= now.h * 60 + now.mi) {
    // ya pasó hoy → mañana (aritmética UTC sobre reloj de pared; Guayaquil no tiene DST)
    const dt = new Date(Date.UTC(y, mo - 1, d) + 86_400_000);
    y = dt.getUTCFullYear(); mo = dt.getUTCMonth() + 1; d = dt.getUTCDate();
  }
  const iso = `${y}-${pad(mo)}-${pad(d)}T${pad(hh)}:${pad(mm)}:00`;
  return { iso, label: `${iso} (${tz})` };
}

/**
 * Programa el despertar diario del noticiero.
 * @param {object} cfg
 * @param {() => Promise<void>} runFn — pipeline a ejecutar en cada despertar
 * @returns {object} task de node-cron (con task.stop() para apagar)
 */
export function startScheduler(cfg, runFn) {
  const expr = cronExprFromWake(cfg.wakeTime);
  if (!cron.validate(expr)) {
    throw new Error(`expresión cron inválida generada desde wakeTime "${cfg.wakeTime}": ${expr}`);
  }

  let running = false; // flag anti-solape: si aún corre, se salta el disparo

  const task = cron.schedule(
    expr,
    async () => {
      if (running) {
        console.log('⏭️  Ya hay una ejecución en curso — se omite este disparo.');
        return;
      }
      running = true;
      const t0 = performance.now();
      try {
        console.log(`⏰ Despertar programado: ${new Date().toISOString()}`);
        await runFn();
        console.log(`✅ Ejecución programada terminada en ${Math.round(performance.now() - t0)} ms`);
      } catch (err) {
        console.error(`❌ Ejecución programada falló: ${err?.message ?? err}`);
      } finally {
        running = false;
      }
    },
    { timezone: cfg.city.timezone }
  );

  console.log(`⏰ ZOLO NEWS despierta programada a las ${cfg.wakeTime} (${cfg.city.timezone})`);
  console.log(`📅 Próxima ejecución: ${nextRunInfo(cfg).label}`);

  return task;
}

export default { startScheduler, nextRunInfo, cronExprFromWake };
