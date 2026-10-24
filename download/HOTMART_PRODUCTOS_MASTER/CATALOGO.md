# 📋 Catálogo extendido — 10 productos

Detalle de características de cada producto. Para info técnica completa, ver el `README.md` dentro de cada carpeta.

---

## 1. 🛡️ ScamShield Pro — Detector de URLs maliciosas

**Ubicación**: `01_seguridad/scamshield-pro/` · **ZIP**: `scamshield-pro.zip` (412K)

### Qué hace
Recibe una URL → ejecuta 9 familias de checks (WHOIS, SSL, DNS, redirects, content, phishing, blocklists, IP reputation) → devuelve un trust score 0-100 compatible con ScamAdviser.

### Features clave
- 30+ heurísticas en 9 detectores
- Score 0-100 con 5 bandas (ScamAdviser-compatible)
- API REST + CLI + Dashboard HTML
- Cache DiskCache + rate limiting
- Docker-ready
- Sin API keys externas requeridas (GSB/VT/IPQS opcionales)

### Competidores verificados
ScamAdviser ($49-$499/mes) · URLVoid ($19-$299/mes) · urlscan.io ($416-$4,167/mes) · IPQS ($30-$500/mes)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | 1 server, 6 meses soporte |
| Pro ⭐ | $97 | 3 servers, marca blanca, 12 meses |
| Agency | $197 | unlimited, 24 meses, onboarding 1:1 |

---

## 2. 📄 FacturaPro — Facturación electrónica SRI + CFDI

**Ubicación**: `02_fintech/facturapro/` · **ZIP**: `facturapro.zip` (218K)

### Qué hace
Genera XML válido para Ecuador SRI v2.34 (offline) y México CFDI 4.0. Genera PDF imprimible. Firma con XAdES-EPES. Envía al SRI/PAC.

### Features clave
- Multi-país: Ecuador + México en un producto
- Generación de clave de acceso SRI (49 dígitos + DV módulo 11)
- XAdES-EPES envelope completo
- PDF con template corporativo (ReportLab)
- Cliente SOAP para SRI (recepción + autorización)
- Cliente REST para PAC México (SW SAPIen, Facturama, BuzonE)
- IVA configurable: 15% Ecuador, 16% México

### Competidores verificados
Alegra ($19-$79/mes) · Aneta EC ($20-$50/mes) · Facturador Cloud AR ($20/mes) · Holded

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 emisor, 100 facturas/mes |
| Pro ⭐ | $197 | 3 emisores, unlimited, marca blanca |
| Multi | $297 | multi-empresa, multi-país simultáneo |

---

## 3. 📸 LeadHarvester — Scraper de leads Instagram

**Ubicación**: `03_marketing/leadharvester/` · **ZIP**: `leadharvester.zip` (184K)

### Qué hace
Scrapea perfiles públicos de Instagram. Extrae emails, teléfonos, datos de bio. Exporta a CSV/Excel/JSON. Modos: username, hashtag, followers de cuenta.

### Features clave
- 3 modos de scraping (username, hashtag, followers_of)
- Detección de emails con obfuscaciones ([at], [dot], [ar])
- 9 categorías automáticas (restaurante, moda, fitness, etc.)
- Filtro business (heurística: venta, tienda, DM)
- Export Excel con hoja Summary
- API REST async + job polling
- Playwright + Chromium (sesión persistente)
- Delays 2-5s para evitar bloqueos

### Competidores verificados
Phantombuster ($69-$279/mes) · Apify ($49+) · GrowMeOrganic ($49-$299) · Skrapp.io ($0-$99)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 500 leads/run, CSV |
| Agency ⭐ | $197 | 2000 leads/run, Excel, API |
| Pro | $297 | unlimited, multi-cuenta IG, proxy |

---

## 4. 💰 PriceWatch — Monitor de precios ML + Amazon

**Ubicación**: `04_ecommerce/pricewatch/` · **ZIP**: `pricewatch.zip` (179K)

### Qué hace
Monitorea precios en MercadoLibre (Ecuador, México, Colombia, Argentina, Chile, Perú) y Amazon. Alertas por email/Telegram/Discord cuando el precio baja.

### Features clave
- 2 stores: MercadoLibre + Amazon (con JSON-LD parsing)
- 4 condiciones de alerta: below, above, drop%, any change
- 3 canales: Email (SMTP) + Telegram + Discord webhook
- Scheduler APScheduler (default 60 min)
- Historial de hasta 1000 price points por producto
- API REST completa + CLI

### Competidores verificados
Keepa (€19-€39/mes) · CamelCamelCamel ($0-$10/mes) · MercadoTrack ($5/mes) · PriceSpy

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | 50 productos, email alerts |
| Pro ⭐ | $97 | 500 productos, Telegram + Discord |
| Agency | $197 | unlimited, multi-user, API |

---

## 5. 💬 WhatsAppBot Pro — Bot para negocios LATAM

**Ubicación**: `04_ecommerce/wabotpro/` · **ZIP**: `wabotpro.zip` (221K)

### Qué hace
Bot conversacional en WhatsApp Cloud API oficial. Catálogo, carrito, pedidos automáticos. Clientes compran sin salir de WhatsApp.

### Features clave
- Flujos conversacionales sin programar (state machine)
- Catálogo gestionable vía CLI/API
- Pedidos automáticos con ID único
- Búsqueda fuzzy en catálogo
- WhatsApp Cloud API v21.0 oficial (no Baileys, cero baneos)
- 8 comandos: hola, catálogo, agregar, quitar, carrito, buscar, confirmar, ayuda
- API REST + webhook

### Competidores verificados
Manychat ($15-$50/mes) · Wati ($39-$99/mes) · Twilio ($0.005/msg) · Kommo ($15-$55) · Zenvia (enterprise)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 negocio, 50 productos |
| Business ⭐ | $197 | 3 negocios, unlimited pedidos |
| Agency | $297 | unlimited, marca blanca |

---

## 6. 📅 CitaYa — Sistema de reservas/citas

**Ubicación**: `05_servicios/citaya/` · **ZIP**: `citaya.zip` (193K)

### Qué hace
Sistema de reservas para clínicas, peluquerías, consultorios, spas. Multi-profesional, calendario automático, recordatorios.

### Features clave
- Calendario automático con slots según horario de cada profesional
- Multi-profesional con override por día
- 5 estados: pending → confirmed → completed/cancelled/no_show
- Widget público (sin login)
- Recordatorios APScheduler (2h antes)
- 3 canales: Email + Telegram + WhatsApp
- iCal export

### Competidores verificados
Calendly ($10-$30/usuario/mes) · Acuity ($23-$50) · SimplyBook ($25-$90) · Booksy ($30-$60) · Fresha (2.2%/booking)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 profesional, 100 citas/mes |
| Business ⭐ | $197 | 5 profesionales, unlimited, recordatorios |
| Premium | $297 | unlimited, multi-sucursal, marca blanca |

---

## 7. 🤖 ReviewReply AI — Respuestas a reseñas con IA

**Ubicación**: `03_marketing/reviewreply/` · **ZIP**: `reviewreply.zip` (198K)

### Qué hace
Genera respuestas a reseñas de Google, Yelp, App Store, Trustpilot, Facebook, Amazon. Detecta sentimiento, genera 3 variantes por reseña.

### Features clave
- Multi-provider IA: Z.ai GLM-4.6, OpenAI, Anthropic, Ollama
- Detección de sentimiento (4 categorías: positive, negative, neutral, mixed)
- Extracción de temas (8 categorías)
- 3 variantes por reseña (corto, medio, detallado)
- 6 plataformas con reglas específicas
- Template fallback (12 templates, gratis sin IA)
- Batch hasta 50 reseñas por request

### Competidores verificados
BirdEye ($50-$300/mes) · Podium ($399+) · Marble ($30-$99) · ReviewTrackers ($99+) · NiceJob ($75-$300)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | Template + 100 AI calls/día |
| Pro ⭐ | $97 | 1000 AI calls/día + Google Business API |
| Agency | $197 | unlimited AI + multi-business |

---

## 8. 📝 PostFactory — Generador contenido redes sociales

**Ubicación**: `03_marketing/postfactory/` · **ZIP**: `postfactory.zip` (190K)

### Qué hace
Genera posts para Instagram, LinkedIn, Twitter, TikTok, Facebook, YouTube, Blog. 7 tipos de contenido, hashtags auto, calendario.

### Features clave
- 7 tipos de contenido: educational, promotional, engagement, storytelling, behind_scenes, listicle, how_to
- 7 plataformas con reglas específicas
- Hashtags automáticos por nicho (10 categorías)
- Calendario de contenido (N días)
- Multi-provider IA o templates gratis
- Best posting times por plataforma
- Image prompts incluidos

### Competidores verificados
Jasper ($49-$125/mes) · Copy.ai ($36-$186) · Lately.ai ($33-$249) · Predis.ai ($32-$59) · Buffer AI ($6-$12)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | Template + 50 AI calls/día |
| Pro ⭐ | $97 | 500 AI calls/día + calendario |
| Agency | $197 | unlimited + multi-cliente |

---

## 9. 📱 MenuQR Pro — Menús digitales con QR

**Ubicación**: `05_servicios/menuqr/` · **ZIP**: `menuqr.zip` (184K)

### Qué hace
Menús digitales con QR para restaurantes. Cliente escanea QR de la mesa → ve menú → hace pedido. Todo self-hosted.

### Features clave
- QR por mesa (cada mesa tiene su QR único)
- Multi-categoría (entradas, principales, postres, bebidas)
- Multi-idioma (es, en, pt) con toggle en vivo
- Tags dietarios (vegetariano, vegano, gluten-free, picante)
- Pedidos desde QR (sin app externa)
- 5 estados de orden: pending → preparing → served → paid → cancelled
- QR personalizable (color, fondo)

### Competidores verificados
GloriaFood ($0-$49/mes) · MenuPix ($29-$99) · Square for Restaurants ($60-$150) · Toast ($69+) · ChowNow ($149+)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | 1 local, 20 mesas |
| Pro ⭐ | $97 | 50 mesas, multi-idioma, pedidos |
| Premium | $197 | multi-local, marca blanca, POS |

---

## 10. 🔔 LicitAlert — Alertas de licitaciones públicas

**Ubicación**: `06_government/licitalert/` · **ZIP**: `licitalert.zip` (185K)

### Qué hace
Monitorea SECOP (Colombia), SERCOP (Ecuador), CompraNet (México). Filtros por keywords, presupuesto, categoría. Alertas por email y Telegram.

### Features clave
- 3 países: Colombia (SECOP II), Ecuador (SERCOP), México (CompraNet)
- Multi-canal: Email + Telegram
- Filtros: keywords, país, rango de presupuesto, categoría, exclusión
- Scoring 0-100 basado en matches de keywords
- Scheduler automático (cada 6h configurable)
- Cache persistente (1000 licitaciones)
- Normalización de texto (sin tildes, lowercase)

### Competidores verificados
Obtenez ($49-$199/mes) · El Tendero ($50-$200) · Alerta Licitaciones ($40-$150) · BidNet ($99-$300)

### Pricing
| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 país, 5 alertas, email |
| Pro ⭐ | $197 | 3 países, 50 alertas, Telegram |
| Agency | $297 | unlimited países, multi-user |

---

## 📊 Resumen total

| Métrica | Valor |
|---------|-------|
| Productos | 10 |
| Tests pasando | 209 |
| Landings HTML | 10 |
| Diagramas | 20+ |
| Docs competidores | 10 |
| Pricing docs | 10 |
| Líneas código totales | ~25,000 |
| Stack base | Python 3.10+, FastAPI, Pydantic v2 |
| Margen estimado | 95%+ (digital, self-hosted) |

---

## 🎯 Próximos pasos sugeridos

1. **Subir a Hotmart** (1 producto por día × 10 días)
2. **Crear repos GitHub públicos** (funcionan como trial implícito)
3. **Escribir 10 artículos DEV.to** (1 por producto, SEO orgánico)
4. **Outreach a 30 agencias LatAm** por producto vía email
5. **Twitter/LinkedIn threads** con screenshots del dashboard
6. **Reddit r/SaaS / r/Entrepreneur** show & tell

© 2026 Eddy Flores.
