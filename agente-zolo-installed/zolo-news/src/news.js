// ============================================================
// ZOLO NEWS — Recolector de noticias RSS (125-A)
// - Parsea cada feed de cfg.news.feeds con fast-xml-parser.
// - fetch con AbortController (timeout 10s) y User-Agent honesto.
// - Deduplica por título normalizado (lowercase, sin tildes, 10 palabras).
// - Ordena por fecha desc (sin fecha al final), limita a cfg.news.maxItems.
// - RESILIENCIA: un feed caído va a `errors` y el run continúa SIEMPRE.
// ============================================================
import { XMLParser } from 'fast-xml-parser';

const UA = 'ZOLO-News/1.0 (agente personal; contacto: founder)';
const TIMEOUT_MS = 10_000;

const parser = new XMLParser({
  ignoreAttributes: false,
  attributeNamePrefix: '@_',
  trimValues: true,
  // CDATA y texto se fusionan tal cual; fast-xml-parser ya lo maneja.
});

/** Limpia HTML/entidades y colapsa espacios. */
export function stripHtml(input) {
  return String(input ?? '')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#0?39;|&apos;/gi, "'")
    .replace(/&#\d+;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Fecha arbitraria (RFC822/ISO) → ISO UTC o null. */
function toISO(value) {
  if (!value) return null;
  const t = Date.parse(String(value).trim());
  return Number.isFinite(t) ? new Date(t).toISOString() : null;
}

/** Clave de deduplicación: lowercase, sin tildes, primeras 10 palabras. */
export function dedupeKey(title) {
  const norm = String(title ?? '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // quita diacríticos
    .replace(/[^\w\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return norm.split(' ').slice(0, 10).join(' ');
}

/** Normaliza un item RSS 2.0 / RDF / Atom a nuestro formato. */
function normalizeItem(raw, feedName) {
  try {
    const title = stripHtml(
      typeof raw.title === 'string' ? raw.title : raw.title?.['#text'] ?? raw.title?.['@_href'] ?? ''
    );
    if (!title) return null;

    // <link> en RSS es texto; en Atom es <link href="...">; algunos usan guid.
    let link = '';
    if (typeof raw.link === 'string') link = raw.link.trim();
    else if (Array.isArray(raw.link)) {
      const alt = raw.link.find((l) => l?.['@_rel'] !== 'self');
      link = (alt?.['@_href'] ?? '').trim();
    } else if (raw.link && typeof raw.link === 'object') {
      link = (raw.link['@_href'] ?? raw.link['#text'] ?? '').trim();
    }
    if (!link && raw.guid) link = String(typeof raw.guid === 'string' ? raw.guid : raw.guid['#text'] ?? '').trim();
    if (!link && raw['dc:identifier']) link = String(raw['dc:identifier']).trim();

    const published = toISO(raw.pubDate ?? raw.published ?? raw.updated ?? raw['dc:date']);
    const summary = stripHtml(raw.description ?? raw.summary ?? raw['content:encoded'] ?? raw.content).slice(0, 400);

    return { title, source: feedName, url: link || null, published, summary };
  } catch {
    return null; // un item raro nunca tumba el feed
  }
}

/** Descarga y parsea UN feed. Lanza si algo falla (el llamador decide). */
async function fetchFeed(feed) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(new Error(`timeout ${TIMEOUT_MS / 1000}s`)), TIMEOUT_MS);
  try {
    const res = await fetch(feed.url, {
      signal: ctrl.signal,
      redirect: 'follow',
      headers: {
        'User-Agent': UA,
        Accept: 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*',
        'Accept-Language': 'es-EC, es;q=0.9',
      },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText ?? ''}`.trim());
    const xml = await res.text();
    if (!xml || xml.length < 40) throw new Error('respuesta vacía o demasiado corta');

    const doc = parser.parse(xml);
    const rawItems =
      doc?.rss?.channel?.item ??       // RSS 2.0
      doc?.['rdf:RDF']?.item ??        // RSS 1.0 / RDF
      doc?.feed?.entry ??              // Atom
      [];
    const arr = Array.isArray(rawItems) ? rawItems : [rawItems];
    const items = arr.map((r) => normalizeItem(r, feed.name ?? feed.url)).filter(Boolean);
    if (items.length === 0) throw new Error('feed sin items parseables');
    return items;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Obtiene las noticias de todos los feeds configurados.
 * @param {object} cfg
 * @returns {Promise<{items: Array<{title,source,url,published,summary?}>, errors: Array<{feed,url,error}>, total: number, feedsOk: number}>}
 */
export async function fetchNews(cfg) {
  const feeds = cfg?.news?.feeds ?? [];
  const maxItems = Math.max(1, Number(cfg?.news?.maxItems) || 6);

  const results = await Promise.allSettled(feeds.map((f) => fetchFeed(f)));

  const all = [];
  const errors = [];
  let feedsOk = 0;
  results.forEach((r, i) => {
    const feed = feeds[i];
    if (r.status === 'fulfilled') {
      feedsOk++;
      all.push(...r.value);
    } else {
      const msg = r.reason?.name === 'AbortError' ? `timeout ${TIMEOUT_MS / 1000}s` : String(r.reason?.message ?? r.reason);
      errors.push({ feed: feed?.name ?? `feed#${i}`, url: feed?.url ?? '?', error: msg });
    }
  });

  // Deduplicación por título normalizado (conserva la primera aparición = feed priorizado por orden de config).
  const seen = new Set();
  const dedup = [];
  for (const it of all) {
    const key = dedupeKey(it.title);
    if (!key) continue;
    if (seen.has(key)) continue;
    seen.add(key);
    dedup.push(it);
  }

  // Orden por published desc; sin fecha al final (estable entre iguales).
  dedup.sort((a, b) => {
    const ta = a.published ? Date.parse(a.published) : Number.NEGATIVE_INFINITY;
    const tb = b.published ? Date.parse(b.published) : Number.NEGATIVE_INFINITY;
    return tb - ta;
  });

  return { items: dedup.slice(0, maxItems), errors, total: dedup.length, feedsOk };
}

export default { fetchNews };
