# LÓGICA — Escaleras de ejecución v3.3

> Las escaleras ordenan los intentos de MAYOR a MENOR autonomía: siempre se intenta el peldaño 1 primero y se DECLARA cuál se usó. Si un peldaño exige cuenta/credencial del humano, se anota como bloqueo TÚ y se sigue con el resto del trabajo.

## A. Escalera de ejecución técnica (¿cómo hago X en el mundo real?)

1. **API pública sin auth** (curl/fetch: marketnow.site, registries, endpoints verificables) — gratis, ilimitado dentro de rate limits.
2. **API con credencial existente** (GitHub `eddyflores100-lang`, npm) — respetando contadores anti-ban.
3. **Herramientas locales** (scripts, validadores, generadores — p.ej. `generate_llms_txt.py`, `validate_skills.py`).
4. **Plataformas con cuenta nueva pero sin aprobación humana** (registro self-serve) — verificar política primero.
5. **Solicitudes con revisión humana** (claims, appeals, formularios de directorios) — enviar y registrar en §13; nunca reenviar el mismo vector antes de respuesta.
6. **Draft para el humano** — ÚLTIMO recurso; un draft sin intento previo = fallo del agente (regla 2: ejecutar > borrar).

## B. Escalera comercial (cada lead recorre: regla 26)

```
1. Lead público (fuente registrada)           → kit 04 §4.3
2. Personalización real (repo/sitio del lead, citar 1 cosa específica)  → OBLIGATORIA
3. UNA oferta del catálogo (02) — no dos, no menús
4. Envío por NEXUS COLD dentro del cupo (≤80/día, 1 dirección/dominio, texto plano, 1 CTA, opt-out)
5. Seguimiento día 3 (valor añadido nuevo, no "solo hacer bump") y día 7 (cierre honesto)
6. Respuesta <24h con objection-handling del catálogo 02
7. Cierre (invoice AliceLabs LLC / USDC / Stripe) o reciclaje a nurture con motivo registrado
```
Prohibiciones: pitch genérico, menú de ofertas, cifras no re-verificadas, second CTA, inventar datos del lead.

## C. Escalera de outreach público (comunidades/GitHub: anti-ban §7 + skill escalera-outreach)

1. GitHub API (comentario/issue/discussion en repo propio o第三方 donde la política lo permita) — máx 3 acciones/día/cuenta VERIFICADAS por eventos públicos.
2. telegra.ph (artículo largo con links propios).
3. SMTP directo (contacto@alicelabs.site) para contacto privado.
4. Directorios/formularios del registro 03.
5. **Solo si todo lo anterior muere**: draft al usuario.
Reglas transversales: política de la plataforma leída ANTES; 1 link propio máximo; textos 100% distintos entre sí y vs días previos; disclosure de afiliación sobre MarketNow/UTA; cero astroturfing; nunca comprar cuentas/invites.

## D. Escalera de publicación (dónde subir cada activo: kit 03)

```
Tier 0 — AGENTES nos descubren (prioridad):
  Official MCP Registry → Glama (glama.json en RAÍZ) → mcpservers.org → mcp.so
  → Anthropic Connectors Directory → skills.sh (repo uta-ai público)
  [PulseMCP: pausado sep-2026, ingesta automática desde Registry — pasivo]
Tier 1 — HUMANOS con presupuesto:
  npm/PyPI (✓ ya) → GitHub Sponsors → Product Hunt → Show HN → Uneed/Peerlist
  → LinkedIn/X semanal (1 artefacto vivo verificado por post)
Tier 2 — TRABAJO:
  Upwork (categoría MCP existe) → Fiverr/Freelancer gigs → Opire ($20+, fee 4%)
  → Algora challenges → GitHub label:bounty (sin fee)
```
Regla de verify: todo listing nuevo se comprueba después (HTTP 200 / URL pública) — no se declara "publicado" sin evidencia (regla 6).

## E. Escalera de dinero (regla 28 — caja antes de glamour)

```
(a) Demanda existente (postings/bounties con presupuesto)  ← SIEMPRE PRIMERO
(b) Servicios S1-S5 (ingreso en días)
(c) Listings Tier 0 (adquisición de agentes, gratis para ellos = imán)
(d) Lanzamientos Tier 1 (cuando (a)-(c) al día y deudas de credibilidad muertas)
(e) Marketplace gate C1 (m2m-checkout + x402) — medio plazo
```

## F. Escalera de memoria (regla 24 — cada cambio de estado)

1. `alethech commit` estructurado (qué / cuándo America/Guayaquil / evidencia URL-hash-HTTP / pendientes).
2. `evidence` para artefactos verificables (receipt).
3. Checkpoint en cada cambio de definición y cierre de sesión (rollback detection).
4. Correcciones = commit nuevo que SUPERSEDE (nunca borrar/editar atrás).
5. Rotación mensual de claves; `key revoke` solo con mandato; DR trimestral ≤60s.
6. Sin CLI instalado: declararlo y operar desde worklog (nunca fingir cadena).
