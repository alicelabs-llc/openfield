---
name: maquina-ventas
description: Protocolo de ventas activas operado por el agente — vender la tecnología AliceLabs (servicios S1-S5, UTA/ATC, marketplace), conseguir trabajo (bounties, postings) y atraer agentes con campañas NEXUS COLD dentro de guardarrails. Activar cuando el usuario pida "vende", "busca trabajo", "ingresos", "clientes", "atraer agentes", "cold email", "pipeline", o cuando haya que ejecutar el kit de ventas.
---

# Máquina de ventas AliceLabs (v3.3)

Kit canónico: `download/ventas-alicelabs/` — 00 LEEME · 01 inventario · 02 ofertas · 03 plataformas · 04 campaña · 05 protocolo · 06 oportunidades. Este skill condensa las REGLAS; el kit tiene el DETALLE ejecutable.

## Reglas 25-28 (resumen operativo)

- **25 VENTA CON EVIDENCIA VIVA**: ninguna cifra en un pitch sin re-verificación en vivo en la misma sesión (curl a `/api/health`, `/api/skills`, npm view). Cifra con fecha >7 días = prohibida. Cada envío registra oferta+lead+cifras+HTTP codes en worklog.
- **26 ESCALERA DE EJECUCIÓN COMERCIAL**: lead público → personalización real (visitar su repo/sitio, citar algo específico) → UNA oferta del catálogo 02 → envío NEXUS COLD dentro de guardarrails → seguimiento día 3/7 → respuesta <24h → cierre o reciclaje. Prohibido saltar la personalización: el pitch genérico es la razón #1 de "nadie nos compra".
- **27 GUARDARRAILS DE CANAL**: email ≤80/día por dirección, 1 dirección/dominio, warm-up ≥15% del volumen, texto plano, 1 CTA, opt-out en 1 línea (MailReach 2026). Publicar SOLO en destinos del registro 03, con verify después (HTTP/URL). Propuestas en plataformas: entregable+precio+fecha, <24h.
- **28 CAJA ANTES DE GLAMOUR**: (a) responder demanda existente (postings/bounties) → (b) servicios S1-S5 → (c) listings Tier 0 (agentes) → (d) lanzamientos → (e) marketplace gate C1. Si hay ingreso en (a), lo demás espera.

## Flujos

1. **BOOT de ventas** → árbol completo en kit `05 §Árbol`: worklog+cifras → respuestas >24h primero → bloqueos (PAT/CF/NEXUS COLD) → producción del día dentro del cupo → cierre con alethech commit+evidence (regla 24).
2. **Campaña NEXUS COLD** → kit `04`: segmentos S1 (autores MCP, oferta conformance+ATC $400) · S2 (startups, Superficie Agent-First $2,500) · S3 (postings activos, respuesta en plataforma) · S4 (agentes, ATC gratis primeros 100). Secuencias EN/ES día 0/3/7 listas para copiar. KPIs y reglas de parada en 04 §4.5.
3. **Publicación** (dónde subir todo) → kit `03`: Tier 0 agentes (Official MCP Registry→Glama→mcpservers.org→mcp.so→Anthropic Directory→skills.sh), Tier 1 humanos (npm/PyPI ✓, Sponsors, PH/HN/Uneed), Tier 2 trabajo (Upwork/Fiverr/Opire/Algora/`label:bounty`).
4. **Trabajo inmediato** → kit `06`: demanda declarada con presupuesto primero (Upwork categoría MCP existe, $20-150/hr), bounties después.
5. **Pipeline** → worklog formato fijo `| fecha | segmento | lead | oferta | estado | siguiente acción |`; cierre de sesión = commit con evidence.

## Límites de autonomía

El agente hace SOLO sin preguntar: re-verificar cifras, armar leads públicos, generar correos hasta el cupo, seguimientos, publicar en destinos que no exijan cuenta nueva, proponer bounties, mantener KPIs, mejorar el kit por deltas. Escala a humano SIEMPRE: contratos >$5,000, precios fuera de tabla, términos de plataformas con cuenta personal, pagos, credenciales, legal/impuestos.
## Grader (v6.0 — añadido por regla 32)

- Pitch con cada cifra re-verificada EN VIVO (curl/npm) y fecha → PASS. Cifra >7 días sin re-verificar → FAIL.
- Lead contactado sin personalización real o sin fuente pública registrada → FAIL.
- Volumen >80 emails/día o >1 dirección/dominio → FAIL (guardarraíl).
