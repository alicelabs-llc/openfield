// ============================================================
// ZOLO NEWS — Clima vía Open-Meteo (125-A)  ·  sin API key
// fetchWeather(cityCfg) → { city, temp, feelsLike?, condition,
//   humidity?, wind?, max, min, rainProb, advice }
// RESILIENCIA: si Open-Meteo falla (ej. 429 límite diario) prueba wttr.in;
// si ambas fallan devuelve objeto degradado — NUNCA tumba el run.
// ============================================================

const TIMEOUT_MS = 10_000;
const UA = 'ZOLO-News/1.0 (agente personal; contacto: founder)';

/** WMO weather code → descripción en español. */
const WMO_ES = new Map([
  [0, 'despejado'],
  [1, 'mayormente despejado'],
  [2, 'parcialmente nublado'],
  [3, 'nublado'],
  [45, 'con neblina'],
  [48, 'con neblina helada'],
  [51, 'llovizna ligera'],
  [53, 'llovizna'],
  [55, 'llovizna intensa'],
  [56, 'llovizna helada ligera'],
  [57, 'llovizna helada intensa'],
  [61, 'lluvia ligera'],
  [63, 'lluvia moderada'],
  [65, 'lluvia fuerte'],
  [66, 'lluvia helada ligera'],
  [67, 'lluvia helada fuerte'],
  [71, 'nieve ligera'],
  [73, 'nieve'],
  [75, 'nieve fuerte'],
  [77, 'granizo menudo'],
  [80, 'chubascos ligeros'],
  [81, 'chubascos'],
  [82, 'chubascos violentos'],
  [85, 'chubascos de nieve ligeros'],
  [86, 'chubascos de nieve fuertes'],
  [95, 'tormenta eléctrica'],
  [96, 'tormenta con granizo ligero'],
  [99, 'tormenta con granizo fuerte'],
]);

function describeWmo(code) {
  if (code === null || code === undefined) return 'variable';
  return WMO_ES.get(Number(code)) ?? `condición ${code}`;
}

/** Construye un consejo práctico según lluvia y temperaturas. */
export function buildAdvice({ rainProb, max, min, condition }) {
  if (Number.isFinite(rainProb) && rainProb > 60) {
    return `Cielo con ${condition} y ${rainProb}% de probabilidad de lluvia: no salgas sin paraguas.`;
  }
  if (Number.isFinite(max) && max >= 30) {
    return `Día caluroso (máx ${Math.round(max)}°C): hidrátate bien, usa bloqueador y busca la sombra al mediodía.`;
  }
  if (Number.isFinite(rainProb) && rainProb > 30) {
    return `Hay ${rainProb}% de probabilidad de lluvia: un paraguas en la mochila no está de más.`;
  }
  if (Number.isFinite(min) && min < 15) {
    return `Mañana fresca (mín ${Math.round(min)}°C): lleva una casaca ligera para temprano.`;
  }
  return 'Clima estable: perfecto para salir a caminar un rato.';
}

/** Objeto degradado cuando la API no responde (el run continúa igual). */
function degraded(cityCfg, errorMsg) {
  return {
    city: cityCfg?.name ?? '—',
    temp: null,
    feelsLike: null,
    condition: 'No disponible',
    humidity: null,
    wind: null,
    max: null,
    min: null,
    rainProb: null,
    advice: 'No pude consultar el clima ahora mismo, pero que no te quite el ánimo: hidrátate y avanza.',
    degraded: true,
    error: errorMsg,
    source: 'ninguna',
  };
}

/** Traduce descripciones en inglés de wttr.in a español. */
export function translateWttr(desc) {
  const d = String(desc ?? '').toLowerCase();
  if (!d) return 'variable';
  if (d.includes('thunder')) return 'tormenta eléctrica';
  if (d.includes('snow') || d.includes('sleet') || d.includes('ice')) return 'nieve o aguanieve';
  if (d.includes('heavy') && (d.includes('rain') || d.includes('shower'))) return 'lluvia fuerte';
  if (d.includes('shower')) return 'chubascos';
  if (d.includes('drizzle')) return 'llovizna ligera';
  if (d.includes('rain')) return 'lluvia';
  if (d.includes('overcast')) return 'nublado';
  if (d.includes('partly')) return 'parcialmente nublado';
  if (d.includes('cloud')) return 'nublado';
  if (d.includes('mist') || d.includes('fog') || d.includes('haze')) return 'neblina';
  if (d.includes('sunny') || d.includes('clear')) return 'despejado';
  return d;
}

/**
 * Fuente secundaria sin API key: wttr.in (format=j1).
 * Misma forma de salida que el objeto de Open-Meteo (contract único).
 */
async function fetchWttr(cityCfg, ctrl) {
  const url = `https://wttr.in/${encodeURIComponent(cityCfg.name)}?format=j1`;
  const res = await fetch(url, {
    signal: ctrl.signal,
    headers: { 'User-Agent': UA, Accept: 'application/json' },
  });
  if (!res.ok) throw new Error(`wttr.in HTTP ${res.status}`);
  const data = await res.json();
  const cc = data?.current_condition?.[0];
  const day = data?.weather?.[0];
  if (!cc) throw new Error('wttr.in sin current_condition');

  const hourly = Array.isArray(day?.hourly) ? day.hourly : [];
  const rainProb = hourly.length
    ? Math.max(...hourly.map((h) => Number(h.chanceofrain) || 0))
    : null;
  const condition = translateWttr(cc.weatherDesc?.[0]?.value);

  const temp = Number.isFinite(Number(cc.temp_C)) ? Math.round(Number(cc.temp_C)) : null;
  const max = Number.isFinite(Number(day?.maxtempC)) ? Math.round(Number(day.maxtempC)) : null;
  const min = Number.isFinite(Number(day?.mintempC)) ? Math.round(Number(day.mintempC)) : null;

  return {
    city: cityCfg.name ?? '—',
    temp,
    feelsLike: Number.isFinite(Number(cc.FeelsLikeC)) ? Math.round(Number(cc.FeelsLikeC)) : null,
    condition,
    humidity: Number.isFinite(Number(cc.humidity)) ? Math.round(Number(cc.humidity)) : null,
    wind: Number.isFinite(Number(cc.windspeedKmph)) ? Math.round(Number(cc.windspeedKmph)) : null,
    max,
    min,
    rainProb,
    advice: buildAdvice({ rainProb, max, min, condition }),
    degraded: false,
    source: 'wttr.in',
  };
}

/** Fuente principal según especificación: Open-Meteo (sin API key). */
async function fetchOpenMeteo(cityCfg, ctrl) {
  const url =
    'https://api.open-meteo.com/v1/forecast' +
    `?latitude=${encodeURIComponent(cityCfg.lat)}` +
    `&longitude=${encodeURIComponent(cityCfg.lon)}` +
    '&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m' +
    '&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code' +
    `&timezone=${encodeURIComponent(cityCfg.timezone ?? 'auto')}` +
    '&forecast_days=1';

  try {
    const res = await fetch(url, {
      signal: ctrl.signal,
      headers: { 'User-Agent': UA, Accept: 'application/json' },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (!data || !data.current || !data.daily) throw new Error('respuesta de Open-Meteo sin current/daily');

    const cur = data.current;
    const day = data.daily;
    const first = (arr) => (Array.isArray(arr) ? arr[0] : arr);

    const temp = Math.round(Number(cur.temperature_2m));
    const feelsLike = Number.isFinite(Number(cur.apparent_temperature)) ? Math.round(Number(cur.apparent_temperature)) : null;
    const condition = describeWmo(cur.weather_code);
    const max = Number.isFinite(Number(first(day.temperature_2m_max))) ? Math.round(Number(first(day.temperature_2m_max))) : null;
    const min = Number.isFinite(Number(first(day.temperature_2m_min))) ? Math.round(Number(first(day.temperature_2m_min))) : null;
    const rainProbRaw = first(day.precipitation_probability_max);
    const rainProb = rainProbRaw === null || rainProbRaw === undefined ? null : Math.round(Number(rainProbRaw));

    return {
      city: cityCfg.name ?? '—',
      temp: Number.isFinite(temp) ? temp : null,
      feelsLike,
      condition,
      humidity: Number.isFinite(Number(cur.relative_humidity_2m)) ? Math.round(Number(cur.relative_humidity_2m)) : null,
      wind: Number.isFinite(Number(cur.wind_speed_10m)) ? Math.round(Number(cur.wind_speed_10m)) : null,
      max,
      min,
      rainProb,
      advice: buildAdvice({ rainProb, max, min, condition }),
      degraded: false,
      source: 'open-meteo',
    };
  } catch (err) {
    const msg = err?.name === 'AbortError' ? 'timeout 10s' : String(err?.message ?? err);
    throw Object.assign(new Error(msg), { name: 'OpenMeteoError' });
  }
}

/**
 * Consulta el clima: Open-Meteo primero (según especificación) y
 * wttr.in como respaldo si la primera falla (ej. límite diario 429).
 * NUNCA lanza: ante fallo total devuelve objeto degradado.
 * @param {{name:string, lat:number, lon:number, timezone:string}} cityCfg
 */
export async function fetchWeather(cityCfg) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(new Error('timeout 10s')), TIMEOUT_MS);
  const errores = [];
  try {
    try {
      return await fetchOpenMeteo(cityCfg, ctrl);
    } catch (err) {
      errores.push(`open-meteo: ${err?.message ?? err}`);
    }
    try {
      return await fetchWttr(cityCfg, ctrl);
    } catch (err) {
      errores.push(`wttr.in: ${err?.message ?? err}`);
    }
    return degraded(cityCfg, errores.join(' | '));
  } finally {
    clearTimeout(timer);
  }
}

export default { fetchWeather };
