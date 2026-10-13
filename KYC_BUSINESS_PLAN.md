# Plan A — Dashboard KYC Web (servicio SaaS)

## Qué necesitas

### Dominio
- Comprar: `kyc.ec` o `compliance.ec` o `verify.ec`
- Precio: ~$15-$50/año
- Dónde: Cloudflare Registrar (más barato) o Namecheap
- URL: https://dash.cloudflare.com/?to=/:domains/registrar

### Hosting
- Opción 1: Vercel (gratis para empezar, $20/mes Pro cuando tengas clientes)
  - URL: https://vercel.com
  - Conecta tu GitHub y deploy automático
- Opción 2: Railway.app (backend Python + DB)
  - URL: https://railway.app
  - Plan gratis: $5 crédito/mes

### Stack técnico
```
Frontend:  React + Next.js + Tailwind CSS
Backend:   Python FastAPI
Database:  PostgreSQL (Supabase gratis hasta 500MB)
Auth:      Clerk (gratis hasta 10K usuarios) o Supabase Auth
PDF gen:   WeasyPrint (Python) o React-PDF
Deploy:    Vercel (frontend) + Railway (backend)
```

### Servicios externos
- OpenSanctions API (ya tienes key) — 25K req/mes gratis
- Supabase (DB + Auth) — https://supabase.com — gratis
- Stripe (cobros) — https://stripe.com — 2.9% + $0.30 por transacción
  - Necesitas cuenta de Stripe conectada a tu banco USA

### Páginas del sitio
```
/ (landing page — diseño de portada, pricing, features)
/login
/dashboard (búsqueda de personas/empresas)
/dashboard/results (resultados del screening)
/dashboard/history (historial de búsquedas)
/dashboard/billing (facturación)
/api/check (endpoint API para clientes)
/pricing
/about
```

### Pricing
```
Free:     5 búsquedas/mes, resultados básicos
Pro:      $99/mes — 100 búsquedas, reportes PDF, API access
Business: $299/mes — 500 búsquedas, multi-usuario, API, soporte
```

### Diseño
- Landing page: usar tu skill de diseño gráfico para crear la identidad
- Logo: nombre + ícono (escudo/check)
- Colores: azul oscuro (confianza) + verde (verificado)
- Tipografía: Inter (gratis de Google Fonts)

### Lo que yo construyo
1. Backend Python FastAPI con endpoints /api/check
2. Frontend React con dashboard
3. Integración con OpenSanctions API
4. Generador de reportes PDF
5. Sistema de autenticación

### Lo que tú haces
1. Comprar dominio
2. Crear cuenta en Vercel + Railway + Supabase + Stripe
3. Diseñar logo y branding
4. Contactar clientes potenciales

### Clientes objetivo
- Notarías de Quito (buscar en Google "notaría Quito")
- Abogados de compliance (buscar "compliance Ecuador")
- Casas de cambio (reguladas por Superintendencia)
- Empresas de importación (aduanas)
- Cooperativas de crédito pequeñas

---

# Plan B — API Wrapper Simple (producto para desarrolladores)

## Qué necesitas

### Dominio
- Comprar: `sanctions-api.com` o `kyc-api.dev` o `verify-api.com`
- Precio: ~$12-$20/año
- Dónde: Cloudflare o Namecheap

### Hosting
- Railway.app (backend Python)
  - URL: https://railway.app
  - Plan: $5/mes

### Stack técnico
```
Backend:   Python FastAPI
Deploy:    Railway
Docs:      FastAPI auto-genera docs en /docs
Auth:      API keys simples (generadas con Python)
```

### Endpoints
```
GET  /api/v1/check?name=Juan+Perez&country=EC
GET  /api/v1/check/company?name=Empresa+S.A.
POST /api/v1/batch (array de nombres)
GET  /docs (documentación automática)
```

### Pricing
```
Free:    50 requests/mes
Dev:     $29/mes — 1,000 requests
Pro:     $99/mes — 10,000 requests
```

### Lo que yo construyo
1. Wrapper Python sobre OpenSanctions API
2. Sistema de API keys
3. Documentación en español
4. Landing page simple

### Lo que tú haces
1. Comprar dominio
2. Crear cuenta en Railway
3. Postear en r/Python, r/devsecops, foros de compliance
4. Contactar desarrolladores en LinkedIn

---

# Plan C — Generador de Reportes PDF (producto inmediato)

## Qué necesitas

### Dominio
- Usar subdominio gratis: `kyc.alicelabs.site` o `verify.marketnow.site`
- Precio: $0 (ya tienes el dominio)

### Hosting
- Tu propio servidor/VPS o Railway
- URL: https://railway.app — $5/mes

### Stack técnico
```
Backend:   Python (script CLI + web)
PDF gen:   WeasyPrint o ReportLab
Web:       FastAPI + Jinja2 templates
```

### Cómo funciona
1. Cliente te manda nombre/empresa por email o WhatsApp
2. Tú corres el script: `python3 generate_report.py --name "Juan Perez" --country EC`
3. Script consulta OpenSanctions API
4. Genera PDF profesional con branding AliceLabs
5. Envías el PDF al cliente
6. Facturas $50-$150 via AliceLabs LLC

### Estructura del reporte PDF
```
Página 1:
- Logo AliceLabs
- "Reporte de Screening KYC/AML"
- Fecha, cliente, referencia
- Nombre buscado
- Resultado: ✅ No encontrado / ⚠️ Match encontrado

Página 2 (si hay match):
- Detalles del match
- Listas donde aparece (OFAC, EU, UN)
- Score de coincidencia
- Datos de la entidad (nacionalidad, fecha nacimiento)
- Recomendación

Página 3:
- Metodología
- Fuentes consultadas (490 datasets)
- Disclaimer legal
- Contacto: eddyflores100@gmail.com
```

### Pricing
```
Reporte individual: $50 c/u
Paquete 5 reportes: $200 ($40 c/u)
Paquete 20 reportes: $600 ($30 c/u)
Suscripción mensual: $300/mes (reportes ilimitados)
```

### Lo que yo construyo
1. Script Python que genera el PDF
2. Template HTML/CSS para el PDF (diseño profesional)
3. Landing page simple para vender el servicio
4. Sistema de pago básico

### Lo que tú haces
1. Diseñar el logo de AliceLabs para el PDF
2. Contactar 10 notarías/abogados en Ecuador
3. Vender el primer reporte

---

# Resumen — qué comprar para cada plan

| Item | Plan A (Dashboard) | Plan B (API) | Plan C (PDF) |
|------|-------------------|--------------|--------------|
| Dominio | $15/año (kyc.ec) | $12/año (sanctions-api.com) | $0 (subdominio) |
| Hosting | $0-$20/mes (Vercel) | $5/mes (Railway) | $5/mes (Railway) |
| Database | $0 (Supabase gratis) | $0 (SQLite) | $0 |
| Auth | $0 (Clerk/Supabase) | $0 (API keys) | N/A |
| Stripe | 2.9% por transacción | 2.9% | N/A (factura manual) |
| API OpenSanctions | $0 (25K req/mes) | $0 | $0 |
| **Total inicial** | **$15** | **$12** | **$0** |
| **Total mensual** | **$0-$20** | **$5** | **$0-$5** |

### Orden recomendado de ejecución

1. **HOY:** Plan C (PDF generator) — $0 inicial, vende primer reporte mañana
2. **SEMANA 1:** Con dinero del primer reporte, Plan B (API wrapper)
3. **SEMANA 2-3:** Plan A (Dashboard completo)
