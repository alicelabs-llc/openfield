# Análisis de competidores — ScamShield Pro

## 1. Mapa competitivo

| Competidor             | Modelo               | Precio base      | Target                  | Self-host? |
|------------------------|----------------------|------------------|-------------------------|------------|
| **ScamAdviser**        | SaaS API + Data feed | $49-$499/mes     | Agencias, KYC vendors   | No         |
| **URLVoid (APIVoid)**  | SaaS API             | $19-$299/mes     | SOC, threat intel teams | No         |
| **urlscan.io**         | SaaS API + Platform  | $416-$4,167/mes  | Threat hunters enterprise| No        |
| **IPQualityScore**     | SaaS API suite       | $30-$500/mes     | Fintechs, ad networks   | No         |
| **VirusTotal**         | SaaS (Google)        | Free + Premium   | General public + ent    | No         |
| **Google Safe Browsing**| API gratuito        | $0 (10k/day)     | Devs, browsers          | No         |
| **Cloudflare URL Scanner**| Built-in CF       | $0+$5-$200/mes CF| CF customers            | No         |

## 2. Precios reales (2026)

### ScamAdviser Trust Score API
- Pricing no público en su landing. Contacta sales.
- Estimaciones de partners: $49/mes para 5k calls, hasta $499/mes para 50k calls.
- White-label y data feed son enterprise-only (presumiblemente $2k+/mes).

### URLVoid / APIVoid
- Free: 250 req/month
- Lite: $19/mes — 5k req
- Pro: $99/mes — 50k req
- Business: $299/mes — 250k req
- Enterprise: Custom

### urlscan.io (tier más agresivo del mercado enterprise)
- Free: 50 private scans + 5k public scans/día
- Automate: $416/mes — 2,500 private scans/día
- Professional: $1,042/mes — 20k private + 10 seats Pro
- Enterprise: $2,084/mes — 100k private + 30 seats
- Ultimate: $4,167/mes — 200k private + 100 seats

### IPQualityScore
- Free: 5,000 lookups/mes
- Starter: $29.95/mes — 50k lookups
- Premium: $99/mes — 200k lookups
- Enterprise: Custom

## 3. Estilo de landing — referencias

### ScamAdviser
- **Tono**: consumer-friendly, enfoque educativo.
- **Headlines**: "Check Any Website for Scams & Fraud"
- **Estructura landing**:
  1. Search bar gigante arriba (URL input → resultado instantáneo)
  2. Trust score band system (5 niveles con emojis)
  3. "Why does a legitimate website sometimes score low?" (transparencia)
  4. Who Uses ScamAdviser's Trust Score Data? (logos)
  5. Ambassador program / Scam University (community)
- **Colores**: mucho blanco + verde/rojo + emoji coloridos
- **CTA**: "Try Now" (gratis, sin signup)

### URLVoid
- **Tono**: técnico, freemium developer-focused.
- **Headlines**: "Website Reputation Checker — 30+ blocklist engines"
- **Estructura**:
  1. Search bar arriba
  2. 3 features principales (Multiple Blocklists, Threat Analysis, Safety Report)
  3. Popular Windows software cross-sell (extraño pero efectivo)
- **Colores**: gris/azul, minimalista
- **CTA**: "Scan Website"

### urlscan.io
- **Tono**: enterprise, threat-hunting serio.
- **Headlines**: tabla de pricing muy detallada con quotas
- **Estructura**: pricing-first, features segundo
- **Colores**: negro/azul/verde, dashboard look
- **CTA**: "Start free trial"

### IPQualityScore
- **Tono**: B2B fintech, productos múltiples.
- **Estructura**: mega-menú con 30+ productos relacionados (proxy, email, phone, device fingerprint)
- **Colores**: rojo/azul, fintech look
- **CTA**: "Sign up free"

## 4. Estilo que ScamShield Pro copia

Mezclamos ScamAdviser (consumer-friendly trust bands) + URLVoid (developer focus + free scan) + urlscan.io (pricing transparente):

- **Hero**: headline gigante + search bar embebida en hero (como ScamAdviser).
- **Score bands**: idéntico sistema 5-tier con emojis (1-20 🔴 ... 81-100 ✅).
- **Comparison table**: contra ScamAdviser/URLVoid/IPQS directamente.
- **Pricing visible**: 3 tiers visibles sin "contact sales" (diferenciador vs ScamAdviser).
- **Code block**: como urlscan.io, snippet de curl + JSON response.
- **Dashboard**: minimalista, foco en el score gigante.
- **Color**: dark mode (#0a0e1a bg + accent verde #00d97e) — premium feel, distinto de ScamAdviser (claro).

## 5. Gap competitivo que ScamShield Pro llena

Ningún competidor ofrece las 4 cosas juntas:

1. **Self-hosted**: ScamAdviser, URLVoid, IPQS, urlscan.io son todos SaaS. ScamShield Pro va en tu VPS.
2. **Código fuente**: todos los competidores son cerrados. ScamShield Pro entrega el código.
3. **Lifetime deal**: todos son suscripción mensual. ScamShield Pro es pago único $47-$197.
4. **Sin límite de calls**: todos te cobran por call. ScamShield Pro es ilimitado (limitado solo por tu CPU).

Esto appeals a:
- Fintechs LATAM que no quieren enviar datos de clientes a EEUU
- Agencias que hacen cientos de miles de checks al mes y no quieren pagar $4k/mes
- Researchers que quieren customizar el algoritmo
- Startups bootstrapped que no pueden afrontar $99/mes por 50k calls

## 6. Pricing de ScamShield Pro — justificación

| Plan     | Precio | Justificación vs competidores                                  |
|----------|--------|----------------------------------------------------------------|
| Single Dev | $47  | < 1 mes de URLVoid Lite ($19×3). Recupera en 3 meses.        |
| Pro       | $97  | < 1 mes de ScamAdviser básico estimado. Recupera en 2 meses.  |
| Agency    | $197 | < 1 mes de urlscan.io Automate ($416). Recupera en 2 semanas.|

## 7. Tácticas de copy

Cada landing copia frases que han probado funcionar en los competidores:

- "Trust Score" (término de ScamAdviser) — usado literalmente.
- "Blocklist" (URLVoid usa "Multiple Blocklists") — usamos "30+ heurísticas".
- "Self-hosted" (diferenciador clave, repetido 6 veces en landing).
- "Lifetime license" (palabra mágica en Hotmart).
- "Sin costos recurrentes" (translate directo de "no recurring fees").
- "Score 0-100 compatible con ScamAdviser" (credibilidad por asociación).

## 8. Canales de distribución

| Canal              | Estrategia                                                |
|--------------------|-----------------------------------------------------------|
| Hotmart            | Listing oficial, 3 planes ($47/$97/$197)                  |
| AppSumo            | Lifetime deal $49 (similar a Hotmart Single Dev)           |
| DEV.to             | Artículo técnico "Cómo construí un clon self-hosted de ScamAdviser" → tráfico |
| GitHub             | Repo público con README de marketing + issues abiertos    |
| Reddit /r/netsec   | Show & tell con enfoque educativo                        |
| LinkedIn           | Post sobre "stop paying monthly fees for fraud detection"  |
| Twitter/X          | Hilos con screenshots del dashboard                       |

## 9. Métricas objetivo (3 meses)

- 50 ventas Single Dev ($2,350)
- 15 ventas Pro ($1,455)
- 5 ventas Agency ($985)
- **Total**: $4,790 en 3 meses
- Costo marginal: $0 (copia digital)
- Margen: 95%+ (solo comisiones Hotmart ~9.9% + fees)
