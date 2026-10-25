# 🚀 HOTMART PRODUCTOS — Master Bundle

> **10 productos digitales self-hosted para LatAm** — código fuente completo, tests, landing HTML, diagramas y docs. Listos para subir a Hotmart.

---

## 📦 Productos incluidos

| # | Producto | ZIP | Categoría | Precio | Tests | Stack |
|---|----------|-----|-----------|--------|-------|-------|
| 1 | **ScamShield Pro** | `scamshield-pro.zip` | Seguridad | $47–$197 | 30 ✓ | Python, FastAPI |
| 2 | **FacturaPro** | `facturapro.zip` | Fintech | $97–$297 | 15 ✓ | Python, FastAPI, lxml |
| 3 | **LeadHarvester** | `leadharvester.zip` | Marketing | $97–$297 | 24 ✓ | Python, Playwright |
| 4 | **PriceWatch** | `pricewatch.zip` | Ecommerce | $47–$197 | 18 ✓ | Python, APScheduler |
| 5 | **WhatsAppBot Pro** | `wabotpro.zip` | Ecommerce | $97–$297 | 24 ✓ | Python, FastAPI |
| 6 | **CitaYa** | `citaya.zip` | Reservas | $97–$297 | 18 ✓ | Python, APScheduler |
| 7 | **ReviewReply AI** | `reviewreply.zip` | Marketing | $47–$197 | 21 ✓ | Python, Z.ai |
| 8 | **PostFactory** | `postfactory.zip` | Marketing | $47–$197 | 25 ✓ | Python, Z.ai |
| 9 | **MenuQR Pro** | `menuqr.zip` | Restaurantes | $47–$197 | 18 ✓ | Python, QR |
| 10 | **LicitAlert** | `licitalert.zip` | B2B Gov | $97–$297 | 16 ✓ | Python, Scrapers |

**Total:** 209 tests pasando · 10 landings HTML · 20+ diagramas PNG · 10 docs de competidores · 10 pricings

---

## 🗂️ Estructura del bundle

```
HOTMART_PRODUCTOS_MASTER/
├── README.md                          ← Este archivo (índice maestro)
├── CATALOGO.md                        ← Catálogo extendido con características
├── ESTRATEGIA_VENTA.md                ← Plan de monetización
├── 01_seguridad/
│   └── scamshield-pro/                ← Producto 1 (código fuente)
├── 02_fintech/
│   └── facturapro/                    ← Producto 2
├── 03_marketing/
│   ├── leadharvester/                 ← Producto 3
│   ├── reviewreply/                   ← Producto 7
│   └── postfactory/                   ← Producto 8
├── 04_ecommerce/
│   ├── pricewatch/                    ← Producto 4
│   └── wabotpro/                      ← Producto 5
├── 05_servicios/
│   ├── citaya/                        ← Producto 6
│   └── menuqr/                        ← Producto 9
├── 06_government/
│   └── licitalert/                    ← Producto 10
└── zips/                              ← Todos los ZIPs individuales
    ├── scamshield-pro.zip
    ├── facturapro.zip
    ├── leadharvester.zip
    ├── pricewatch.zip
    ├── wabotpro.zip
    ├── citaya.zip
    ├── reviewreply.zip
    ├── postfactory.zip
    ├── menuqr.zip
    └── licitalert.zip
```

---

## 🚀 Quick Start — Cómo usar este bundle

### Opción 1: Instalar un producto individual
```bash
cd 01_seguridad/scamshield-pro
cp .env.example .env
pip install -e .
scamshield serve
# → Abre http://localhost:8000
```

### Opción 2: Levantar todos con Docker
Cada producto tiene su `docker-compose.yml`:
```bash
cd 01_seguridad/scamshield-pro && docker compose up -d
cd ../../02_fintech/facturapro && docker compose up -d
# ... etc.
```

### Opción 3: Subir a Hotmart
1. Toma el ZIP del producto (de `zips/`)
2. En Hotmart: **Crear producto digital** → **Subir archivo**
3. Pega la descripción larga de `docs/LANDING_COPY.md` (en ScamShield) o del `README.md`
4. Configura los 3 tiers de pricing: Starter / Pro / Agency
5. Activa "7-day money back guarantee"

---

## 💰 Pricing sugerido (Hotmart)

Cada producto tiene 3 tiers. Resumen:

| Producto | Starter | Pro ⭐ | Agency |
|----------|---------|-------|--------|
| ScamShield Pro | $47 | $97 | $197 |
| FacturaPro | $97 | $197 | $297 |
| LeadHarvester | $97 | $197 | $297 |
| PriceWatch | $47 | $97 | $197 |
| WhatsAppBot Pro | $97 | $197 | $297 |
| CitaYa | $97 | $197 | $297 |
| ReviewReply AI | $47 | $97 | $197 |
| PostFactory | $47 | $97 | $197 |
| MenuQR Pro | $47 | $97 | $197 |
| LicitAlert | $97 | $197 | $297 |

**Bundle todo (10 productos): $497 USD** (ahorro 65% vs compra individual)

---

## 🎯 Quién es el cliente ideal

- 🇪🇨 Agencias de marketing LatAm (LeadHarvester, PostFactory, ReviewReply)
- 🇲🇽 Contadores y consultores fiscales (FacturaPro)
- 🇨🇴 Pymes que venden en MercadoLibre (PriceWatch)
- 🇵🇪 Restaurantes y cafeterías (MenuQR Pro, CitaYa)
- 🇪🇨 Startups bootstrapped que no quieren pagar mensualidades (todos)
- 🇲🇽 Proveedores B2B gobierno (LicitAlert)
- LatAm Devs freelance (ScamShield, WhatsAppBot)

---

## 📈 Proyección de revenue

Asumiendo 25 ventas/mes en mes 3, mezcla 60% Starter / 30% Pro / 10% Agency:

- **Mes 3**: $4,925 USD/mes (por producto)
- **10 productos**: $49,250 USD/mes potenciales
- **Realista (5 productos activos)**: $24,625 USD/mes
- **Año 1**: $200,000+ USD con 95% margen (digital, self-hosted)

---

## ⚙️ Stack técnico común

Todos los productos comparten:
- **Lenguaje**: Python 3.10+
- **Web framework**: FastAPI 0.115+
- **CLI**: Click + Rich
- **Validation**: Pydantic v2
- **HTTP**: httpx (async)
- **Cache**: diskcache
- **Tests**: pytest + pytest-asyncio
- **Container**: Docker + docker-compose
- **AI provider** (donde aplica): Z.ai GLM-4.6 (alternativa barata a OpenAI)

---

## 🛠️ Mantenimiento

Cada producto es **independiente y auto-contenido**:
- No comparten dependencias entre sí
- Cada uno tiene su propio `requirements.txt` y `pyproject.toml`
- Cada uno tiene su propia base de datos JSON (sin Postgres/Redis requerido)
- Cada uno tiene tests propios con su propio venv

**Actualizaciones**: idealmente 1 release/mes por producto. Hotmart notifica a los compradores automáticamente.

---

## 📞 Soporte

- **Email**: eddyflores100@gmail.com
- **GitHub**: github.com/eddyflores100-lang
- **DEV.to**: 100+ artículos (autoridad para marketing orgánico)
- **Garantía**: 7 días devolución sin preguntas

---

© 2026 Eddy Flores. Lifetime licenses. Todos los productos son self-hosted y pagan una sola vez.
