# Landing Copy — ScamShield Pro

Este documento contiene los textos de marketing listos para usar en Hotmart, AppSumo, emails, redes sociales.

---

## Hero (landing principal)

**Headline**: Detecta URLs maliciosas, phishing y fraude con una llamada API.

**Subheadline**: 30+ heurísticas: edad de dominio, SSL, DNS, redirect chains, phishing patterns, blocklists públicos y reputación IP. Score de confianza 0-100 estilo ScamAdviser.

**CTA primario**: ⚡ Lifetime Deal $47 →
**CTA secundario**: Probar demo

---

## Hotmart listing — descripción corta (160 chars)

Self-hosted URL fraud & phishing detector. 30+ heurísticas, trust score 0-100, ScamAdviser-compatible. FastAPI + CLI. Lifetime deal $47.

---

## Hotmart listing — descripción larga

**¿Cansado de pagar $99-$499/mes por APIs de detección de fraude?**

ScamShield Pro es tu alternativa self-hosted: lo instalas en tu VPS una vez, y escaneas URLs ilimitadas sin costo recurrente.

**¿Qué hace?**
Recibe una URL → ejecuta 9 familias de checks (WHOIS, SSL, DNS, redirects, content, phishing, blocklists, IP reputation) → devuelve un trust score 0-100 + breakdown completo. Compatible con el sistema de bandas de ScamAdviser.

**¿Para quién es?**
- Fintechs LATAM que no quieren enviar datos de clientes a EEUU
- Agencias que hacen cientos de miles de checks al mes
- E-commerce que quiere bloquear checkouts con tarjetas robadas
- Researchers que necesitan customizar el algoritmo
- Startups bootstrapped que no pueden pagar $99/mes

**¿Qué incluye?**
- ✅ Código fuente completo (~2,500 líneas Python)
- ✅ FastAPI server + CLI + Dashboard HTML
- ✅ 9 detectores con 30+ heurísticas
- ✅ Tests con pytest
- ✅ Dockerfile + docker-compose
- ✅ 3 ejemplos prácticos (quickstart, bulk scan, webhook integration)
- ✅ Docs completas (arquitectura, API, competidores, pricing)
- ✅ Diagramas de arquitectura

**¿Por qué confiar?**
- Tu controlas el 100% del código
- Los datos de tus usuarios NO salen de tu servidor
- 7 días garantía de devolución
- Soporte email directo con el autor

**Planes**:
- Single Dev — $47 (1 server, 1 proyecto)
- Pro — $97 (3 servers, marca blanca) ⭐ MÁS VENDIDO
- Agency — $197 (unlimited servers, onboarding 1:1)

**Compra una vez. Usa para siempre.**

---

## Email outreach (cold)

**Subject**: ¿Construyes checkout? Ahorra $4k/año en fraud detection

Hola [nombre],

Vi que [producto/empresa] procesa pagos online. Si alguna vez te has planteado integrar ScamAdviser o URLVoid para pre-screeen URLs sospechosas antes de cobrar, quizá te interese ScamShield Pro:

- Self-hosted (datos de tus clientes no salen de tu server)
- 30+ heurísticas estilo ScamAdviser
- Score 0-100 compatible
- Pago único $47-$197 (vs $99-$499/mes de los SaaS)

Si te interesa, puedo armarte una demo de 15 min: https://calendly.com/[tu-link]

O revisa la landing: [tu-landing-url]

Saludos,
Eddy

---

## Twitter thread (hilo)

**Tweet 1**: Construí un clon self-hosted de ScamAdviser.

Lo pago una vez ($47-$197) y escaneo URLs ilimitadas. Sin $99/mes. Sin límite de calls. Sin enviar datos de mis usuarios a terceros.

Esto es ScamShield Pro 🧵👇

**Tweet 2**: ¿Qué hace?

POST /v1/scan {"url": "https://suspicious-shop.xyz/free-iphone"}

→ Score 14/100 🔴
→ Veredicto: very_likely_unsafe
→ 9 detectores con breakdown:
  ✓ domain_age (8 días)
  ✗ phishing_patterns (impersonating "apple")
  ✗ blocklist_check (URLHaus hit)
  ✗ ssl_certificate (expired)

**Tweet 3**: Los 9 detectores:

1. Domain age (WHOIS)
2. SSL cert validity
3. DNS records (MX, NS, TXT, SPF)
4. TLD reputation (.xyz, .top, .gq...)
5. Redirect chain (shorteners, cross-domain)
6. HTML content analysis
7. Phishing patterns (IDN homograph, brand impersonation)
8. Blocklists (URLHaus + GSB + VT opcional)
9. IP reputation (proxy/hosting detection)

**Tweet 4**: ¿Por qué no usar ScamAdviser?

- ScamAdviser = $49-$499/mes
- urlscan.io = $416-$4,167/mes
- IPQS = $30-$500/mes

ScamShield Pro = $47 pago único, para siempre.

Recuperas la inversión en 1-3 meses. Después es 100% gratis.

**Tweet 5**: Stack técnico:

- Python 3.10+ / FastAPI
- Async (9 checks en paralelo, scan completo <2s)
- DiskCache integrado (TTL 24h default)
- Docker-ready (docker-compose incluido)
- CLI con Click + Rich
- OpenAPI docs en /docs
- Tests con pytest

Código: github.com/eddyflores100-lang/scamshield-pro
Landing + demo: [link]

---

## Reddit r/netsec — Show & Tell

**Title**: [Show] ScamShield Pro — self-hosted ScamAdviser alternative (FastAPI, MIT-style license)

**Body**:

Built a URL fraud & phishing detector that runs on your own server. Combines 9 families of heuristics (WHOIS, SSL, DNS, redirects, content, phishing, blocklists, IP reputation) and returns a 0-100 trust score using the same 5-tier band system as ScamAdviser.

Why I built it:
- Got tired of paying $99-$499/month for ScamAdviser / URLVoid / IPQS for a side project
- Wanted full control over the algorithm (custom heuristics for LATAM brands)
- Didn't want to send user URLs to a 3rd-party API

Stack: Python 3.10+, FastAPI, asyncio, dnspython, python-whois, httpx, Pydantic.

Repo (with marketing landing included): [link]

Open to feedback, especially on:
- Additional heuristics to add (cheap ones, no API keys required)
- Scoring algorithm tuning
- Performance optimizations

---

## LinkedIn post

¿Pagar $4k/año por detección de fraude te parece razonable?

Yo no. Por eso construí ScamShield Pro: un detector de URLs maliciosas que instalas en tu VPS y corres ilimitadamente, sin suscripción.

30+ heurísticas. Score 0-100 estilo ScamAdviser. API REST + CLI + dashboard. Pago único $47-$197.

Para fintechs LATAM: tus datos no salen de tu infraestructura. Para agencias: marca blanca incluida en el plan Pro ($97).

Si quieres ahorrar $4k-$50k/año en APIs de fraud detection, échale un vistazo: [link]

#cybersecurity #fintech #saas #selfhosted

---

## DEV.to article (SEO)

**Title**: Cómo construí un clon self-hosted de ScamAdviser (con Python + FastAPI)

**Tags**: python, fastapi, security, tutorial

**Outline**:
1. Por qué (problema: $99-$499/mes por ScamAdviser es caro)
2. Arquitectura (CheckContext compartido, 2 fases paralelas)
3. Los 9 detectores (código de cada uno explicado)
4. Trust score aggregation (cómo se calcula 0-100)
5. FastAPI server (rate limiting, auth, OpenAPI)
6. CLI con Click + Rich
7. Tests con pytest
8. Deploy con Docker
9. Pricing y estrategia de venta (Hotmart)
10. Lo que aprendí (transparencia: qué faltó, qué sigue)

---

## FAQ para soporte email

**Q: ¿Necesito API keys de Google/VirusTotal/IPQS?**
A: No. ScamShield Pro funciona out-of-the-box con blocklists públicos gratuitos (URLHaus, ip-api.com). Las API keys externas son opcionales para enriquecer el reporte.

**Q: ¿Funciona detrás de Cloudflare?**
A: Sí, sin problema. El servidor escucha HTTP; Cloudflare (o Caddy/Nginx) maneja TLS termination.

**Q: ¿Puedo revenderlo como SaaS a mis clientes?**
A: El plan Agency ($197) permite marca blanca completa, pero no puedes revenderlo como producto standalone. Para OEM / revenue share, contáctame directamente.

**Q: ¿Tengo que dar atribución visible al autor?**
A: En la UI del dashboard y la landing, sí (footer con "Powered by ScamShield Pro"). En el código fuente, el header de cada archivo debe preservar el copyright. Si necesitas.removeAttribute, es plan Agency + custom clause.

**Q: ¿Cómo recibo actualizaciones?**
A: Te agregamos a un canal privado de GitHub (o Discord, según prefieras) donde subimos releases. Las updates llegan como tags en git.

**Q: ¿Y si encuentro un bug?**
A: Abre un issue en GitHub o escríbeme directamente. SLA de respuesta: 48h en días hábiles para planes Pro/Agency.

**Q: ¿Puedo contratar soporte extra?**
A: Sí, ofrezco:
- Onboarding 1:1 (2h) — $97 add-on
- Custom heuristics (1 detector nuevo) — $197 add-on
- SLA mensual (24h response, 1 call/mes) — $49/mes
- Integración custom (Slack/Discord/Jira) — $297
