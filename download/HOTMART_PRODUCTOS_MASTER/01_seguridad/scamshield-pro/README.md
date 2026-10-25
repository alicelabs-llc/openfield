# 🛡️ ScamShield Pro

> **Self-hosted URL fraud & phishing detector.** 30+ heuristics. 0-100 trust score. ScamAdviser-compatible bands. FastAPI + CLI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: Commercial](https://img.shields.io/badge/license-single--user--lifetime-orange.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-success.svg)](#)

ScamShield Pro es un detector de URLs maliciosas que puedes instalar en tu propio servidor. Combina 9 familias de heurísticas (edad de dominio, SSL, DNS, redirect chains, análisis de contenido, patrones de phishing, blocklists, reputación IP) en un único producto que devuelve un score de confianza 0-100 compatible con ScamAdviser.

**Diferencia frente a ScamAdviser/URLVoid/IPQS**: pagas una vez ($47-$197), controlas el 100% del código, los datos de tus usuarios no salen de tu infraestructura, y no hay límites de llamadas.

---

## 🚀 Quick Start (5 minutos)

### Opción A — Instalador automático (Linux/macOS)

```bash
git clone https://github.com/eddyflores100-lang/scamshield-pro.git
cd scamshield-pro
bash scripts/install.sh
scamshield serve
```

Abre `http://localhost:8000` → landing interactiva con demo en vivo.
Abre `http://localhost:8000/dashboard` → dashboard de escaneo.

### Opción B — Docker

```bash
git clone https://github.com/eddyflores100-lang/scamshield-pro.git
cd scamshield-pro
cp .env.example .env
docker compose up --build -d
curl http://localhost:8000/healthz
```

### Opción C — Python directo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

scamshield serve
```

---

## 📋 Uso

### CLI

```bash
# Scan simple
scamshield scan https://example.com

# Output JSON
scamshield scan https://suspicious-site.xyz --json

# Skip HTML content analysis
scamshield scan https://example.com --no-content

# Scan desde archivo
scamshield scan-file urls.txt

# Listar detectores
scamshield checks
```

### API REST

```bash
# Scan simple
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Con API key (si configuraste .env)
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"url": "https://example.com"}'

# Bulk scan (hasta 100 URLs)
curl -X POST http://localhost:8000/v1/scan/bulk \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://a.com", "https://b.com"]}'

# Listar detectores habilitados
curl http://localhost:8000/v1/checks

# Health check
curl http://localhost:8000/healthz
```

### Python SDK

```python
import asyncio
from scamshield.core.models import ScanRequest
from scamshield.scanner import Scanner

async def main():
    scanner = Scanner()
    result = await scanner.scan(ScanRequest(url="https://github.com"))
    print(result.summary())  # "✅ Score 95/100 (very_likely_safe) — github.com"
    for c in result.checks:
        print(f"  {'✓' if c.passed else '✗'} {c.name}: {c.message}")

asyncio.run(main())
```

### Integración en checkout / webhook

```python
from scamshield.examples.webhook_integration import pre_charge_check
import asyncio

decision = asyncio.run(pre_charge_check("https://sketchy-store.xyz/free-iphone"))
# → {"decision": "block", "reason": "Trust score 8/100 — likely scam", ...}
```

---

## 🎯 Score bands (compatible con ScamAdviser)

| Score    | Verdict               | Recomendación                                                   |
|----------|-----------------------|-----------------------------------------------------------------|
| 1-20 🔴  | Very Likely Unsafe    | No visites. No ingreses datos personales o tarjetas.           |
| 21-40 🟠 | Likely Unsafe         | Evita transacciones. Busca reseñas independientes.             |
| 41-60 🟡 | Caution Recommended   | Verifica dirección física, redes, reseñas.                     |
| 61-80 🟢 | Likely Safe           | Razonable proceder. Usa tarjeta para protección de compra.     |
| 81-100 ✅| Very Likely Safe      | Alta confianza. Aplica buenas prácticas estándar.              |

---

## 🔍 Detectores incluidos

| # | Detector            | Severidad  | Peso | Descripción                                                  |
|---|----------------------|------------|------|--------------------------------------------------------------|
| 1 | `domain_age`         | high       | 25   | Edad del dominio via WHOIS (< 90 días = penalty)             |
| 2 | `ssl_certificate`    | high       | 20   | Validación de certificado SSL/TLS, expiración, emisor        |
| 3 | `dns_records`        | medium     | 15   | A, AAAA, MX, NS, TXT, SPF — configuración saludable          |
| 4 | `tld_reputation`     | medium     | 15   | TLDs estadísticamente abusivos (.xyz, .top, .gq, .cf, etc.) |
| 5 | `redirect_chain`     | medium     | 18   | Hop count, URL shorteners, cross-domain, HTTPS→HTTP downgrade|
| 6 | `content_analysis`   | medium     | 12   | HTML: password fields, hidden iframes, external scripts, idioma |
| 7 | `phishing_patterns`  | critical   | 35   | IDN homograph, brand impersonation, typosquatting, subdomain |
| 8 | `blocklist_check`    | critical   | 40   | URLHaus + Google Safe Browsing + VirusTotal (opcional)       |
| 9 | `ip_reputation`     | medium     | 12   | ip-api.com: país, ISP, hosting/proxy flag                   |

Total: 9 detectores · peso máximo acumulado: 192 (suficiente para llevar cualquier sitio a score 1 si todos fallan).

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT                                      │
│   Browser / curl / Python SDK / webhook integration                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP POST /v1/scan
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FastAPI Server (server.py)                     │
│                                                                       │
│   • CORS middleware                                                   │
│   • Rate limiter (in-memory, 60/min default)                         │
│   • API key auth (optional)                                          │
│   • Serves landing (/) + dashboard (/dashboard)                     │
│   • OpenAPI docs at /docs                                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Scanner (scanner.py)                            │
│                                                                       │
│   1. normalize_url()  →  URL canonicalization                        │
│   2. parse_domain()   →  extract registered domain + TLD             │
│   3. Phase 1 (parallel) → run all non-content checks                 │
│   4. Phase 2 (sequential) → run content checks (need final URL)     │
│   5. compute_score() → aggregate to 0-100 + verdict + confidence    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
  ┌──────────┐         ┌──────────┐         ┌──────────┐
  │ DomainAge│         │   SSL    │         │   DNS    │ ... (9 total)
  │  Check   │         │  Check   │         │  Check   │
  └────┬─────┘         └────┬─────┘         └────┬─────┘
       │                    │                    │
       ▼                    ▼                    ▼
   WHOIS lookup        socket + SSL        dnspython
   (python-whois)      context             Resolver

  Shared context (CheckContext) accumulates:
   • ip_address      • html_content   • ssl_cert
   • final_url       • whois_info     • dns_records
   • redirect_chain  • http_headers   • server_country

  Each detector:
   1. Reads what it needs from ctx
   2. Does its check (network or heuristic)
   3. Writes back to ctx (for downstream checks)
   4. Returns CheckResult(passed, severity, weight, message, details)

  Cache layer: DiskCache (~/.scamshield/cache) wraps expensive lookups
  (WHOIS, DNS). Configurable TTL.
```

Ver `docs/ARCHITECTURE.md` para más detalle.

---

## ⚙️ Configuración

Todas las opciones viven en `.env` (ver `.env.example`):

| Variable                  | Default             | Descripción                                  |
|---------------------------|---------------------|----------------------------------------------|
| `HOST`                    | `0.0.0.0`           | Bind address                                 |
| `PORT`                    | `8000`              | Bind port                                    |
| `DEBUG`                   | `false`             | Modo debug                                   |
| `API_KEY`                 | (auto-generado)     | Si está seteado, requiere header `X-API-Key` |
| `GSB_API_KEY`             | (vacío, opcional)   | Google Safe Browsing API key                 |
| `VT_API_KEY`              | (vacío, opcional)   | VirusTotal API key                           |
| `IPQS_API_KEY`            | (vacío, opcional)   | IPQualityScore API key                       |
| `CACHE_DIR`               | `~/.scamshield/cache` | DiskCache directory                         |
| `CACHE_TTL_SECONDS`       | `86400` (24h)       | Cache time-to-live                           |
| `RATE_LIMIT_PER_MINUTE`   | `60`                | Límite por IP                                |
| `HTTP_TIMEOUT_SECONDS`    | `10`                | Timeout HTTP por request                     |
| `DNS_TIMEOUT_SECONDS`     | `5`                 | Timeout DNS                                  |

---

## 🧪 Tests

```bash
pytest -v
```

Cobertura: `tests/test_url_parser.py`, `tests/test_scoring.py`, `tests/test_checks_phishing.py`, `tests/test_api.py`.

---

## 📦 Estructura del proyecto

```
scamshield-pro/
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── COMPETITORS.md
│   ├── PRICING.md
│   └── LANDING_COPY.md
├── diagrams/
│   ├── architecture.png       ← diagrama visual
│   └── flow.png               ← user flow
├── examples/
│   ├── quickstart.py
│   ├── bulk_scan.py
│   └── webhook_integration.py
├── scripts/
│   ├── install.sh
│   └── start.sh
├── src/
│   └── scamshield/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py             ← Click CLI
│       ├── scanner.py          ← Orquestador
│       ├── server.py          ← FastAPI app
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── models.py      ← Pydantic schemas
│       │   └── scoring.py     ← Trust score aggregation
│       ├── checks/            ← 9 detectores
│       │   ├── base.py
│       │   ├── domain.py
│       │   ├── ssl.py
│       │   ├── dns.py
│       │   ├── tld.py
│       │   ├── redirect.py
│       │   ├── content.py
│       │   ├── phishing.py
│       │   ├── blocklist.py
│       │   └── reputation.py
│       └── utils/
│           ├── url_parser.py
│           ├── http_client.py
│           └── cache.py
├── tests/
│   ├── conftest.py
│   ├── test_url_parser.py
│   ├── test_scoring.py
│   ├── test_checks_phishing.py
│   └── test_api.py
└── web/
    ├── index.html             ← Landing page
    └── dashboard.html         ← Dashboard
```

---

## 💰 Pricing (Hotmart)

| Plan         | Precio   | Target                          |
|--------------|----------|---------------------------------|
| Single Dev   | $47 USD  | Freelancers, 1 proyecto        |
| Pro          | $97 USD  | Agencias, multi-proyecto       |
| Agency       | $197 USD | Multi-server, marca blanca     |

Ver `docs/PRICING.md` para estrategia competitiva.

---

## 📞 Soporte

- Email: **eddyflores100@gmail.com**
- GitHub Issues: https://github.com/eddyflores100-lang/scamshield-pro/issues
- Garantía: 7 días devolución sin preguntas

---

## 📜 License

Single-User Lifetime License. Ver [LICENSE](LICENSE) para términos completos.

© 2026 Eddy Flores.
