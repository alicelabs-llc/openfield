# LeadHarvester

> **Scraper de leads Instagram** para agencias. Extrae emails, teléfonos y datos de perfiles públicos. Exporta a CSV/Excel/JSON.

## Features

- 🎯 **3 modos de scraping**: por username, hashtag, o followers de cuenta
- 📧 **Extracción de contacto**: emails, teléfonos (con obfuscaciones tipo [at]/[dot])
- 🏷️ **Categorización automática**: restaurante, moda, fitness, belleza, etc.
- 💼 **Filtro business**: identifica perfiles comerciales (venta, tienda, DM, etc.)
- 📊 **Export 3 formatos**: CSV, Excel (con hoja Summary), JSON
- 🤖 **API REST**: scrape async con job polling
- 🐳 **Docker-ready**: Playwright + Chromium preinstalado
- ⏱️ **Rate limiting configurable**: delays entre requests para evitar bloqueos
- 🔄 **Proxy support**: rotación de IPs a escala

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/leadharvester.git
cd leadharvester
cp .env.example .env
pip install -e .
playwright install chromium
leadharvester serve
```

Abre `http://localhost:8002`.

## Uso

### CLI

```bash
# Scrape perfil único
leadharvester scrape-cmd tienda_x --type username

# Scrape hashtag (top 50 perfiles)
leadharvester scrape-cmd moda_ecuatoriana --type hashtag --max 50

# Scrape followers de una cuenta competidora (con login)
leadharvester scrape-cmd competencia --type followers_of --max 100 --only-business

# Export a Excel
leadharvester scrape-cmd tienda --type username --format excel -o leads
```

### API REST

```bash
# Iniciar job async
curl -X POST http://localhost:8002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"target":"moda","target_type":"hashtag","max_results":20}'

# Poll status
curl http://localhost:8002/v1/scrape/{job_id}

# Export results
curl -X POST http://localhost:8002/v1/scrape/{job_id}/export?format=excel -o leads.xlsx
```

## Categorías detectadas automáticamente

- 🍽️ restaurante
- 👗 moda
- 💪 fitness
- 💄 belleza
- 💻 tecnología
- 📈 marketing
- 🏠 inmobiliaria
- 🏥 salud
- 📚 educación

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 user, hasta 500 leads/run, export CSV |
| Agency | $197 | 3 users, 2000 leads/run, Excel, API |
| Pro | $297 | unlimited, proxy rotation, multi-account IG |

## ⚠️ Aviso legal

LeadHarvester extrae **datos públicos** de perfiles Instagram (info visible sin login o con sesión autenticada). No almacena contraseñas ni datos privados. Cumple ToS Instagram en términos de uso razonable (delays 2-5s, sin flooding). Para uso a escala comercial, considera usar la Graph API oficial de Meta.

© 2026 Eddy Flores. Lifetime license.
