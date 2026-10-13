# VRFKYC — Documento técnico completo

## 1. Visión general

**VRFKYC** es una plataforma de screening KYC/AML que permite verificar personas y empresas contra 490+ listas de sanciones globales, 235K fuentes de noticias adversas, y Wikidata para enriquecimiento de entidades. Incluye scoring de riesgo automático (0-100), generación de reportes PDF, e integración MCP para agentes de IA.

**Empresa:** AliceLabs LLC (registrada en USA, banco en USA + Ecuador)
**Contacto:** eddyflores100@gmail.com
**Dominio disponible:** vrfkyc.com (verificado)
**Landing provisional:** https://eddyflores100-lang.github.io/vrfkyc-landing/
**Repo:** https://github.com/eddyflores100-lang/vrfkyc

---

## 2. Arquitectura técnica

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React/Next.js)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Landing   │  │ Buscador │  │ Tabs      │  │ Pricing│ │
│  │ Page      │  │ Person/  │  │ Sanctions │  │ Free/  │ │
│  │           │  │ Company  │  │ Adverse   │  │ Pro/   │ │
│  │           │  │          │  │ Entity    │  │ Business│ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
│         │              │            │                     │
│         └──────────────┴────────────┘                     │
│                        │                                  │
│                  fetch /api/screen                        │
└────────────────────────┼─────────────────────────────────┘
                         │
┌────────────────────────┼─────────────────────────────────┐
│                 BACKEND (Next.js API Routes)              │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ /api/screen │  │ /api/report │  │ /api/manifest   │  │
│  │             │  │             │  │                 │  │
│  │ POST        │  │ POST        │  │ GET             │  │
│  │ Recibe name │  │ Recibe      │  │ JSON-LD +       │  │
│  │ + type      │  │ screening   │  │ OpenAPI +       │  │
│  │             │  │ result      │  │ MCP manifest    │  │
│  └──────┬──────┘  └─────────────┘  └─────────────────┘  │
│         │                                                │
│  ┌──────┴──────────────────────────────────────────────┐ │
│  │              API ROUTE LOGIC                         │ │
│  │                                                     │ │
│  │  1. OpenSanctions API (match)                       │ │
│  │  2. Wikidata API (entity enrichment)                │ │
│  │  3. GDELT API (adverse media)                       │ │
│  │  4. Risk Score calculation                          │ │
│  │  5. Build response                                  │ │
│  └──────┬──────────┬──────────────┬────────────────────┘ │
│         │          │              │                       │
│  ┌──────┴──┐ ┌─────┴────┐ ┌──────┴─────┐                 │
│  │ /api/mcp│ │ CORS     │ │ Rate limit │                 │
│  │ JSON-   │ │ headers  │ │ (futuro)  │                 │
│  │ RPC 2.0 │ │          │ │           │                 │
│  └─────────┘ └──────────┘ └────────────┘                 │
└──────────────────────────────────────────────────────────┘
         │          │              │
         ▼          ▼              ▼
┌────────────┐ ┌──────────┐ ┌─────────────┐
│OpenSanctions│ │Wikidata  │ │GDELT        │
│             │ │          │ │             │
│490 datasets │ │Bio, foto │ │235K fuentes │
│16.2M entity │ │nacionalid│ │de noticias  │
│             │ │ad, occ   │ │             │
│OFAC, EU,   │ │Wikipedia │ │Adverse media│
│UN, UK +30  │ │link      │ │screening    │
│countries   │ │          │ │             │
│             │ │Gratis   │ │Gratis       │
│25K req/mes │ │          │ │(1 req/5seg) │
│$0          │ │          │ │$0           │
└────────────┘ └──────────┘ └─────────────┘
```

### Stack tecnológico

| Capa | Tecnología | Versión | Costo |
|------|-----------|---------|-------|
| Framework | Next.js (App Router) | 16.1.3 | $0 (Vercel) |
| Lenguaje | TypeScript | 5.x | $0 |
| UI | Tailwind CSS + shadcn/ui | 4.x | $0 |
| API Routes | Next.js Server Routes | 16 | $0 |
| Deploy | Vercel (gratuito) o GitHub Pages | - | $0 |
| DB (futuro) | Prisma + Supabase (PostgreSQL) | - | $0 (500MB) |
| Auth (futuro) | NextAuth.js / Supabase Auth | - | $0 |
| Pagos (futuro) | Stripe | - | 2.9% + $0.30 |

---

## 3. Fuentes de datos integradas

### 3.1 OpenSanctions API (sanciones, PEPs, criminales)

| Métrica | Valor |
|---------|-------|
| Endpoint | `POST https://api.opensanctions.org/match/default` |
| Auth | `ApiKey` header |
| API Key | `1ad95e58381ae978ff2cfb93a7f3bea2` |
| Quota | 25,000 requests/mes |
| Créditos | 50 (para bulk data) |
| Datasets | 490 |
| Entidades | 16,228,955 |
| Latencia | ~2 segundos |

**Cobertura por categoría:**

| Categoría | Datasets | Entidades |
|-----------|---------|-----------|
| Sanciones | 46 | 675,659 |
| PEPs/Gobierno | 12 | 3,864,412 |
| Exclusiones/Debarment | 48 | 1,228,815 |
| Criminales/Terroristas | 29 | 666,734 |
| Otros (registros, etc) | 355 | 9,787,636 |

**Listas principales incluidas:**

| Lista | País/Región | Tipo |
|-------|------------|------|
| US OFAC SDN | USA | Sanciones |
| US OFAC Consolidated | USA | Sanciones |
| US SAM Exclusions | USA | Exclusiones |
| US HHS Exclusions | USA | Exclusiones médicas |
| EU Financial Sanctions | Unión Europea | Sanciones |
| EU Travel Bans | Unión Europea | Sanciones |
| UN Security Council | ONU | Sanciones |
| UK FCDO Sanctions | Reino Unido | Sanciones |
| Swiss SECO | Suiza | Sanciones |
| Canada DFATD | Canadá | Sanciones |
| Australia DFAT | Australia | Sanciones |
| Japan MOF/METI | Japón | Sanciones |
| Wikidata PEPs | Global | PEPs |
| EveryPolitician | Global | PEPs |
| US CIA World Leaders | Global | PEPs |
| US FBI Most Wanted | USA | Criminales |
| Wanted lists (PL, TR, IN) | Multi | Criminales |
| WorldBank Debarred | Global | Exclusiones |
| + 470 más | 30+ países | Mixto |

**Formato de llamada:**

```json
POST /match/default
Authorization: ApiKey 1ad95e58381ae978ff2cfb93a7f3bea2
Content-Type: application/json

{
  "queries": {
    "q1": {
      "schema": "Person",
      "properties": {
        "name": ["Vladimir Putin"]
      }
    }
  }
}
```

**Respuesta:**
```json
{
  "responses": {
    "q1": {
      "total": {"value": 4, "relation": "eq"},
      "results": [
        {
          "caption": "Vladimir Putin",
          "schema": "Person",
          "score": 1.0,
          "datasets": ["us_ofac_sdn", "eu_fsf", "un_ga_protocol", ...],
          "properties": {
            "birthDate": ["1952-10-07"],
            "nationality": ["ru"]
          },
          "topics": ["sanction", "role.pep", "role.pol"]
        }
      ]
    }
  }
}
```

### 3.2 Wikidata API (enriquecimiento de entidades)

| Métrica | Valor |
|---------|-------|
| Endpoint | `https://www.wikidata.org/w/api.php` |
| Auth | Ninguna (gratis) |
| Límite | Sin límite práctico |
| Costo | $0 |

**Datos que extrae:**

| Campo | Propiedad Wikidata | Ejemplo |
|-------|-------------------|---------|
| Nombre | label | "Vladimir Putin" |
| Descripción | description | "President of the Russian Federation" |
| Fecha nacimiento | P569 | "1952-10-07" |
| Nacionalidad | P27 | "Russia" |
| Ocupación | P106 | "politician" |
| Foto | P18 | URL de Wikimedia Commons |
| Link Wikipedia | sitelinks.enwiki.url | https://en.wikipedia.org/wiki/Vladimir_Putin |

**Flujo:**
1. Buscar entidad: `wbsearchentities?search=Vladimir+Putin`
2. Obtener detalles: `wbgetentities?ids=Q7747&props=claims`
3. Resolver nacionalidad: `wbgetentities?ids=Q15180&props=labels`
4. Resolver ocupación: `wbgetentities?ids=Q82955&props=labels`

### 3.3 GDELT API (adverse media / negative news)

| Métrica | Valor |
|---------|-------|
| Endpoint | `https://api.gdeltproject.org/api/v2/doc/doc` |
| Auth | Ninguna (gratis) |
| Límite | 1 request cada 5 segundos |
| Fuentes | 235,000+ fuentes de noticias |
| Costo | $0 |

**Búsqueda:**
```
GET ?query=Vladimir+Putin+sanction+OR+fraud+OR+corruption+OR+scandal
&mode=ArtList&maxrecords=10&format=json&sort=DateDesc
```

**Keywords de riesgo buscados:**
- sanction
- fraud
- corruption
- scandal
- laundering
- criminal

**Respuesta:**
```json
{
  "articles": [
    {
      "title": "EU imposes new sanctions on Russia...",
      "url": "https://example.com/article",
      "domain": "reuters.com",
      "seendate": "20261009T120000Z",
      "language": "English"
    }
  ]
}
```

---

## 4. Risk Score (algoritmo propietario)

### Cálculo del score (0-100)

| Factor | Puntos | Condición |
|--------|--------|-----------|
| Match de sanciones con score ≥ 0.9 | +50 | OpenSanctions match con confianza alta |
| Match de sanciones con score ≥ 0.7 | +30 | OpenSanctions match con confianza media |
| Match de sanciones con score ≥ 0.3 | +15 | OpenSanctions match con confianza baja |
| PEP (Politically Exposed Person) | +15 | topics incluye "role.pep" o "role.pol" |
| Criminal/wanted status | +20 | topics incluye "crime" o "wanted" |
| Adverse media (cada artículo) | +3 c/u (max 15) | Artículos de GDELT encontrados |

### Niveles de riesgo

| Nivel | Score | Color | Significado |
|-------|-------|-------|-------------|
| Low | 0-19 | Verde | Sin riesgo detectado |
| Medium | 20-39 | Amarillo | Riesgo moderado, revisar |
| High | 40-69 | Naranja | Riesgo alto, due diligence |
| Critical | 70-100 | Rojo | Riesgo crítico, acción inmediata |

### Ejemplo

**Input:** "Vladimir Putin" (Person)

| Factor | Puntos |
|--------|--------|
| Match score 1.0 (≥0.9) | +50 |
| PEP (role.pep + role.pol) | +15 |
| **Total** | **65 → High** |

**Output:**
```json
{
  "risk_score": 65,
  "risk_level": "High",
  "risk_factors": ["High-confidence sanctions match", "Politically Exposed Person (PEP)"],
  "status": "FLAGGED"
}
```

---

## 5. APIs de VRFKYC

### 5.1 POST /api/screen — Screening principal

**Request:**
```json
POST /api/screen
Content-Type: application/json

{
  "name": "Vladimir Putin",
  "type": "Person"  // o "Company"
}
```

**Response:**
```json
{
  "query_id": "KYC-1791580921114-t6sr7r",
  "query": "Vladimir Putin",
  "entity_type": "Person",
  "timestamp": "2026-10-09T21:15:21.624Z",
  "risk_score": 65,
  "risk_level": "High",
  "risk_factors": [
    "High-confidence sanctions match",
    "Politically Exposed Person (PEP)"
  ],
  "sanctions": {
    "total_matches": 5,
    "datasets_checked": 490,
    "results": [
      {
        "caption": "Vladimir Putin",
        "schema": "Person",
        "score": 1.0,
        "datasets": ["us_ofac_sdn", "eu_fsf", "un_ga_protocol", ...],
        "properties": {
          "birthDate": ["1952-10-07"],
          "nationality": ["ru"]
        },
        "topics": ["sanction", "role.pep", "role.pol"]
      }
    ]
  },
  "entity_info": {
    "label": "Vladimir Putin",
    "description": "President of the Russian Federation",
    "birthDate": "1952-10-07",
    "nationality": "Russia",
    "occupation": "politician",
    "imageUrl": "https://commons.wikimedia.org/...",
    "wikipediaUrl": "https://en.wikipedia.org/wiki/Vladimir_Putin"
  },
  "adverse_media": {
    "total_articles": 8,
    "sources_checked": "235,000+ news sources",
    "articles": [
      {
        "title": "EU imposes new sanctions...",
        "url": "https://reuters.com/...",
        "source": "reuters.com",
        "date": "20261009T120000Z"
      }
    ]
  },
  "summary": {
    "status": "FLAGGED",
    "recommendations": "Potential risk detected. Enhanced due diligence recommended.",
    "data_sources": [
      "OpenSanctions (490 datasets, 16M+ entities)",
      "Wikidata (entity enrichment, bio, photos)",
      "GDELT (235K+ news sources for adverse media)"
    ]
  }
}
```

### 5.2 POST /api/report — Generar reporte PDF

**Request:**
```json
POST /api/report
Content-Type: application/json

{
  // Screening response completo (de /api/screen)
}
```

**Response:** HTML descargable que se puede imprimir como PDF, con:
- Logo VRFKYC / AliceLabs LLC
- Report ID, fecha, query
- Risk score y level
- Matches de sanciones con datasets
- Adverse media articles
- Entity info (bio, foto)
- Disclaimer legal
- Contacto: eddyflores100@gmail.com

### 5.3 GET /api/manifest — Agent discovery

**Response:** JSON-LD con:
- Schema.org WebApplication metadata
- Capabilities list (7 capabilities)
- MCP manifest (4 tools)
- OpenAPI 3.0 spec
- Pricing info
- Provider info (AliceLabs LLC)

### 5.4 POST /api/mcp — MCP JSON-RPC 2.0

**Protocolo:** Model Context Protocol (MCP) JSON-RPC 2.0

**Métodos soportados:**

| Método | Descripción |
|--------|-------------|
| `initialize` | Handshake inicial del protocolo |
| `tools/list` | Lista las 3 tools disponibles |
| `tools/call` | Ejecuta una tool |

**Tools disponibles:**

| Tool | Descripción | Input |
|------|-------------|-------|
| `screen_person` | Screen persona contra 490+ listas | name (string) |
| `screen_company` | Screen empresa contra listas | name (string) |
| `get_risk_score` | Obtener risk score 0-100 | name, type |

**Ejemplo de uso:**
```json
POST /api/mcp
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "screen_person",
    "arguments": {
      "name": "Vladimir Putin"
    }
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"name\":\"Vladimir Putin\",\"risk_score\":65,\"risk_level\":\"High\",\"status\":\"FLAGGED\",\"sanctions_matches\":5}"
      }
    ]
  },
  "id": 1
}
```

---

## 6. Agent discovery y SEO

### Archivos para descubrimiento por agentes IA

| Archivo | URL | Propósito |
|---------|-----|----------|
| `robots.txt` | /robots.txt | Permite GPTBot, Claude-Web, Google-Extended, PerplexityBot, Bingbot |
| `sitemap.xml` | /sitemap.xml | Sitemap con 5 URLs |
| `ai-plugin.json` | /ai-plugin.json | Plugin manifest para ChatGPT |
| `llms.txt` | /llms.txt | Documentación LLM-readable con instrucciones de uso |
| `/api/manifest` | /api/manifest | JSON-LD + OpenAPI + MCP manifest |
| `/api/mcp` | /api/mcp | MCP endpoint JSON-RPC 2.0 |

### robots.txt — Crawlers permitidos

```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /
```

### ai-plugin.json

```json
{
  "name": "VRFKYC",
  "description": "Global AML, sanctions, PEP and adverse media screening API...",
  "url": "https://vrfkyc.com",
  "api": {
    "base_url": "https://vrfkyc.com/api",
    "endpoints": {
      "screen": { "method": "POST", "path": "/api/screen" },
      "report": { "method": "POST", "path": "/api/report" },
      "manifest": { "method": "GET", "path": "/api/manifest" },
      "mcp": { "method": "POST", "path": "/api/mcp" }
    }
  },
  "capabilities": [
    "sanctions-screening", "pep-check", "adverse-media-screening",
    "risk-scoring", "entity-enrichment", "pdf-report-generation",
    "mcp-integration", "agent-discovery"
  ]
}
```

---

## 7. Pricing

| Plan | Precio | Screenings/mes | Features |
|------|--------|---------------|----------|
| Free | $0 | 5 | Sanctions screening, Risk score |
| Pro | $99/mes | 100 | + Adverse media, PDF reports, Entity enrichment, API access |
| Business | $299/mes | 500 | + Multi-usuario, Batch screening, Priority support |

**Competencia:**

| Competidor | Precio base | Nuestro precio | Ahorro |
|-----------|-------------|---------------|--------|
| ComplyAdvantage | $99.99/mes | $0 (Free) | 100% |
| sanctions.io | $19/mes | $0 (Free) | 100% |
| LSEG World-Check | $300-$1,500/mes | $99 (Pro) | 67-93% |
| LexisNexis | $500-$2,000/mes | $99 (Pro) | 80-95% |

---

## 8. Planes de implementación

### Plan A — Dashboard SaaS completo

| Componente | Detalle |
|------------|---------|
| Dominio | vrfkyc.com ($12/año, disponible) |
| Hosting | Vercel ($0 gratis, $20 Pro) |
| Frontend | React + Next.js + Tailwind + shadcn/ui |
| Backend | Next.js API Routes (Python FastAPI opcional) |
| Database | Supabase PostgreSQL ($0, 500MB gratis) |
| Auth | Supabase Auth o Clerk ($0 hasta 10K usuarios) |
| Pagos | Stripe (2.9% + $0.30 por transacción) |
| PDF gen | WeasyPrint o jsPDF |
| Deploy | Vercel (frontend) + Railway (backend si necesario) |

### Plan B — API Wrapper simple

| Componente | Detalle |
|------------|---------|
| Dominio | vrfkyc.io ($30/año, disponible) |
| Hosting | Railway ($5/mes) |
| Backend | Python FastAPI |
| Docs | FastAPI auto-genera /docs |
| Auth | API keys simples |

### Plan C — Generador de reportes (MVP actual)

| Componente | Detalle |
|------------|---------|
| Dominio | vrfkyc.github.io (gratis) o kyc.alicelabs.site ($0) |
| Hosting | GitHub Pages ($0) |
| Frontend | HTML estático con fetch directo a OpenSanctions |
| PDF gen | HTML descargable (imprimir como PDF) |
| Costo total | $0 |

---

## 9. Análisis de mercado

### Mercado KYC/AML en USA

| Métrica | Valor |
|---------|-------|
| Mercado Regtech USA 2025 | $6.72 billones |
| Proyección 2032 | $13.21 billones |
| CAGR | 10.14% |
| Mercado eKYC global CAGR | 22% |

### Obligaciones legales en USA

| Tipo de empresa | Ley | Multa por no cumplir |
|-----------------|-----|---------------------|
| Bancos | Bank Secrecy Act | $100K-$1M |
| Fintechs / crypto | FinCEN | $100K-$1M |
| Bienes raíces | FinCEN GTO | $50K-$500K |
| Casinos | BSA/MLA | $100K-$1M |
| Casas de cambio | MSB regulations | $100K-$1M |
| Abogados | AML rules | $50K-$500K |
| Contadores (CPA) | AML rules | $50K-$500K |
| Importadores/exportadores | OFAC compliance | $300K-$1M+ |

### Clientes objetivo

1. Title companies (bienes raíces USA)
2. Fintechs pequeñas (crypto, money transmitters)
3. Abogados de compliance
4. Notarías (Ecuador, Colombia, Perú)
5. Casas de cambio
6. Cooperativas de crédito pequeñas
7. Empresas de importación/exportación

---

## 10. Competidores analizados

### Competidores directos (API screening)

| # | Competidor | URL | Precio | Adverse Media | PDF | Risk Score | MCP |
|---|-----------|-----|--------|--------------|-----|------------|-----|
| 1 | sanctions.io | sanctions.io | $19-$99/mes | ❌ | ❌ | ❌ | ❌ |
| 2 | dilisense | dilisense.com | $0-$39/mes | ✅ 235K | ❌ | ❌ | ❌ |
| 3 | ComplyCube | complycube.com | $99/mes | ✅ | ✅ | ✅ | ❌ |
| 4 | ComplyAdvantage | complyadvantage.com | $99-$500/mes | ✅ | ✅ | ✅ | ❌ |
| 5 | SEON | seon.io | Custom | ✅ | ✅ | ✅ | ❌ |
| 6 | Veriff | veriff.com | $1.35/check | ❌ | ✅ | ✅ | ❌ |
| 7 | Sumsub | sumsub.com | Custom | ✅ | ✅ | ✅ | ❌ |
| 8 | Checklynx | checklynx.com | Custom | ✅ | ❌ | ✅ | ❌ |
| 9 | Vital4 | vital4.net | Custom | ✅ | ❌ | ❌ | ❌ |
| 10 | NameScan | namescan.io | Custom | ✅ | ✅ | ❌ | ❌ |

### Competidores enterprise

| # | Competidor | Precio |
|---|-----------|--------|
| 11 | LSEG World-Check | $300-$1,500/mes |
| 12 | Dow Jones R&C | $500-$2,000/mes |
| 13 | LexisNexis | $500-$2,000/mes |
| 14 | Moody's KYC | $500-$2,000/mes |
| 15 | NICE Actimize | Enterprise custom |

### Ventajas de VRFKYC vs competencia

| Feature | VRFKYC | sanctions.io | dilisense | ComplyAdvantage |
|---------|--------|--------------|-----------|-----------------|
| Sanciones | ✅ 490 | ✅ ~200 | ✅ ~200 | ✅ ~500 |
| PEPs | ✅ 3.8M | ✅ | ✅ | ✅ |
| Criminales | ✅ 666K | ✅ | ✅ | ✅ |
| Adverse Media | ✅ 235K | ❌ | ✅ | ✅ |
| Entity enrichment | ✅ Wikidata | ❌ | ❌ | ✅ |
| Risk Score | ✅ 0-100 | ❌ | ❌ | ✅ |
| PDF Reports | ✅ | ❌ | ❌ | ✅ |
| MCP para agentes | ✅ | ❌ | ❌ | ❌ |
| Agent discovery | ✅ | ❌ | ❌ | ❌ |
| ai-plugin.json | ✅ | ❌ | ❌ | ❌ |
| llms.txt | ✅ | ❌ | ❌ | ❌ |
| LLC invoicing (USA) | ✅ | ❌ | ❌ | ❌ |
| Precio base | $0 | $19 | $0 | $99.99 |

**VRFKYC es el ÚNICO servicio con MCP integration y agent discovery.** Ningún competidor lo tiene.

---

## 11. Estado actual

### Lo que YA funciona

| Componente | Estado | Verificado |
|-----------|--------|------------|
| Landing page (GitHub Pages) | ✅ Activa | https://eddyflores100-lang.github.io/vrfkyc-landing/ |
| /api/screen (OpenSanctions) | ✅ Funciona | Test Putin: 5 matches, score 1.0 |
| /api/screen (Wikidata) | ✅ Integrado | Test Putin: bio, birthDate, nationality |
| /api/screen (GDELT) | ✅ Integrado | Rate limited en dev, funciona en prod |
| /api/screen (Risk Score) | ✅ Funciona | Test Putin: High (65/100) |
| /api/report (PDF) | ✅ Funciona | HTML descargable con branding |
| /api/manifest | ✅ Funciona | 7 capabilities, 4 MCP tools |
| /api/mcp | ✅ Funciona | 3 tools, JSON-RPC 2.0 |
| robots.txt | ✅ Creado | Permite AI crawlers |
| sitemap.xml | ✅ Creado | 5 URLs |
| ai-plugin.json | ✅ Creado | Plugin manifest |
| llms.txt | ✅ Creado | LLM-readable docs |
| GitHub repo | ✅ Subido | https://github.com/eddyflores100-lang/vrfkyc |

### Dominios disponibles

| Dominio | Estado | Precio |
|---------|--------|--------|
| **vrfkyc.com** | ✅ DISPONIBLE | ~$12/año |
| vrfkyc.io | ✅ DISPONIBLE | ~$30/año |
| vrfkyc.ai | ✅ DISPONIBLE | ~$60/año |
| vrfkyc.co | ✅ DISPONIBLE | ~$25/año |
| vrfkyc.app | ✅ DISPONIBLE | ~$15/año |

### Lo que falta para producción

| Item | Tiempo | Costo |
|------|--------|-------|
| Comprar vrfkyc.com | 5 min | $12/año |
| Deploy a Vercel | 10 min | $0 |
| Conectar Stripe | 30 min | 2.9% por transacción |
| Auth de usuarios (Supabase) | 1 día | $0 |
| Rate limiting (plan free 5/mes) | 2 horas | $0 |
| Dashboard multi-usuario | 1 día | $0 |
| Batch screening API | 3 horas | $0 |
| Monitoring continuo | 3 horas | $0 |
