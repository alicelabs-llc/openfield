# Arquitectura — LeadHarvester

## Componentes

```
Client → FastAPI server → InstagramScraper (Playwright) → Lead extraction → Export
```

### InstagramScraper (scrapers/instagram.py)
- Usa Playwright + Chromium headless
- Sesión persistente en `~/.leadharvester/ig_session.json`
- 3 modos: profile / hashtag / followers_of
- Delays aleatorios 2-5s entre requests

### Extractors (core/extractors.py)
- Regex para email (con obfuscaciones [at]/[dot]/[ar])
- Phone con country code
- Website (filtra social media URLs)
- is_business_bio (heurística: venta, tienda, DM, etc.)
- extract_category (9 categorías predefinidas)

### Export (export/exporters.py)
- to_json: serializa LeadList
- to_csv: archivo plano con todos los campos
- to_excel: 2 hojas (Leads + Summary con métricas)

### API (server.py)
- POST /v1/scrape → inicia job async
- GET /v1/scrape/{job_id} → poll status
- POST /v1/scrape/{job_id}/export → descarga CSV/JSON/Excel

## Limitaciones técnicas

- **Sin login IG**: solo data pública (meta tags + bio)
- **Con login**: full data + followers list (requiere IG_USERNAME/IG_PASSWORD)
- **Rate limiting**: delays configurables; IG bloquea tras ~200 req/hora sin sesión
- **Proxy**: opcional para rotar IPs y evitar bloqueos
