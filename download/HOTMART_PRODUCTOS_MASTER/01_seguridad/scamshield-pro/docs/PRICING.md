# Pricing Strategy — ScamShield Pro

## Estrategia: Lifetime Deal en 3 tiers

### Tier 1: Single Dev — $47 USD

**Target**: freelance developers, security researchers, indie hackers.

**Incluye**:
- 1 servidor / 1 proyecto propio
- API REST + CLI + Dashboard
- 30+ heurísticas
- Código fuente
- 6 meses soporte email
- Actualizaciones 6 meses

**NO incluye**:
- Multi-instancia
- Marca blanca
- Soporte prioritario

**Justificación**: Punto de entrada psicológico <$50. 3 meses más barato que URLVoid Lite ($19/mes). Recupera en 3 meses.

---

### Tier 2: Pro — $97 USD  ⭐ MÁS POPULAR

**Target**: agencias pequeñas, SaaS B2B, fintech startups.

**Incluye**:
- 3 servidores, multi-proyecto
- API REST + CLI + Dashboard
- 30+ heurísticas
- **Marca blanca** (tu logo, tu dominio)
- 12 meses soporte email
- Actualizaciones 12 meses
- Bulk scan hasta 100 URLs

**Justificación**: Tier de conversión principal. 1 mes más barato que ScamAdviser básico estimado. Marca blanca es killer feature para agencias.

---

### Tier 3: Agency — $197 USD

**Target**: agencias que revenden, consultoras, system integrators.

**Incluye**:
- Servidores ilimitados
- API REST + CLI + Dashboard
- 30+ heurísticas + integraciones
- Marca blanca completa
- **24 meses soporte prioritario**
- Actualizaciones 24 meses
- Onboarding 1:1 (2 horas video call)

**Justificación**: < 50% de urlscan.io Automate ($416/mes). Recupera en 2 semanas. Para agencias con 10+ clientes es trivial venderlo a $20/mes por cliente.

---

## Reglas de pricing (Hotmart)

1. **Lifetime deal, sin suscripción**: alineado con audiencia de Hotmart que odia recurrente.
2. **3 tiers, no más**: parafrilla. 3 opciones es óptimo para conversión.
3. **Tier medio destacado**: el "Pro" es el más vendido (bandera "MÁS POPULAR").
4. **Sin trial free**: producto es código, el repo público en GitHub funciona como trial implícito (con features reducidas).
5. **Garantía 7 días**: reduce fricción de compra.
6. **6/12/24 meses soporte**: escalonado para que el upgrade valga la pena.

## Cálculo de revenue

| Plan        | Precio | Ventas/mes (mes 3) | Revenue |
|-------------|--------|---------------------|---------|
| Single Dev  | $47    | 18                  | $846    |
| Pro         | $97    | 5                   | $485    |
| Agency      | $197   | 2                   | $394    |
| **Total**   |        | **25 ventas**       | **$1,725/mes** |

Año 1: $1,725 × 9 meses activos = **$15,525** (asumiendo ramp-up 3 meses).

Margen: 95%+ (copia digital). Solo Hotmart commission (~9.9%) + PayPal/Stripe fees (~3%).

## Comparativa directa con competidores

| Plan ScamShield | Pago único | Equivalente mensual (12 meses) | Equivalente mensual (24 meses) |
|-----------------|------------|--------------------------------|--------------------------------|
| Single Dev $47  | $47        | $3.92/mes                      | $1.96/mes                      |
| Pro $97         | $97        | $8.08/mes                      | $4.04/mes                      |
| Agency $197     | $197       | $16.42/mes                     | $8.21/mes                      |

vs competidores:
- URLVoid Lite: $19/mes → ScamShield Pro = 5-10x más barato
- ScamAdviser básico: ~$49/mes → ScamShield Pro = 6-12x más barato
- urlscan.io Automate: $416/mes → ScamShield Pro = 25-50x más barato
- IPQS Starter: $29.95/mes → ScamShield Pro = 4-7x más barato

## Upsells potenciales (post-compra)

1. **Setup + onboarding remoto** ($97 add-on): 1 hora video call + deploy asistido.
2. **Custom heuristics** ($197 add-on): 1 detector nuevo desarrollado a medida.
3. **SLA + support** ($49/mes): response time 24h, 1 llamada/mes.
4. **Custom integrations** ($297): webhook to Slack/Discord/Jira/PagerDuty.

## Pricing A/B tests para iterar

- **Test A**: $47 / $97 / $197 (actual)
- **Test B**: $39 / $89 / $179 (más agresivo, +conversion)
- **Test C**: $59 / $129 / $249 (más premium, -conversion pero +ARPU)

Medir: conversión a landing visit, conversión a checkout, ARPU.

## Proyección de revenue 12 meses

Mes 1: setup + lanzamiento, 5 ventas = $565
Mes 2: 12 ventas = $1,156
Mes 3-6: 25 ventas/mes = $1,725/mes × 4 = $6,900
Mes 7-12: 35 ventas/mes = $2,500/mes × 6 = $15,000

**Total año 1**: $565 + $1,156 + $6,900 + $15,000 = **$23,621 USD**

Con ~95% de margen = **$22,440 USD netos año 1**.

Año 2 (sin re-acquisition cost): $30,000+ esperado con upsells y renewals de soporte.
