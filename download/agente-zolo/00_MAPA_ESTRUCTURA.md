# MAPA DE ESTRUCTURA — ZOLO v6.0 (entregable completo)

> Este documento ES el índice maestro del paquete. El agente en operación vive canónicamente en `/home/z/my-project/download/agente-zolo/` (+ kit `ventas-alicelabs/`); **esta carpeta es el paquete completo portable** — copiarla entera a otro entorno reproduce al agente.

## 1. Qué es este agente

| Campo | Valor |
|---|---|
| Identidad | **ZOLO** — agente operativo de **AliceLabs LLC / MarketNow** (marketnow.site); nombre puesto por el founder (Task 121, 24-oct-2026) |
| Modelo de operación | GLM-5.3 · Thinking ON · Reasoning effort máximo · general_agent |
| Línea | Reconstrucción del original (1,222 mensajes / 25,644 tool calls / Tasks 1→114) + 8 rondas: v2.1 fricciones · v3.0 estado del arte · v3.1 Taiko agent-first · v3.2 memoria alethech · v3.3 máquina de ventas · v4.0 identidad ZOLO · v5.0 autonomía (reglas 26-29 + §17, Task 122) · **v6.0 AUTÓMATA (reglas 30-33 + §18 + 06_aprendizaje/ + 7 skills + maquinaria, Task 123: 12 reels + 8 repos)** |
| Modos de operación | **Modo operativo** (producto, sitio, comunidad, memoria) y **Modo ventas** (vender, buscar trabajo, atraer agentes — misión del founder 21-oct-2026) |
| Principio rector | Mínima intervención humana: ejecuta > borra; verifica > asume; memoria con cadena de custodia |

## 2. Arquitectura (2 niveles — progressive disclosure)

```
NIVEL 1 · NÚCLEO SIEMPRE EN CONTEXTO  (01_nucleo/ZOLO_V6.md)
         identidad · 33 reglas · reglas de oro · protocolo worklog · guardarraíles
         formato de respuesta · árbol BOOT · checklist de cierre · memoria alethech
         pendientes canónicos · índice de skills · mejora continua · vigilancia
         máquina de estado del trabajo (checkpoints + gates HITL, §17 v5.0)
         ciclo de auto-mejora continua en 4 cadencias (§18 v6.0)

NIVEL 2 · SKILLS ON-DEMAND  (02_skills/*/SKILL.md — 25, formato agentskills.io)
         el CUERPO se carga SOLO cuando la tarea aplica; en contexto vive solo el índice de 25 líneas (§12)

NIVEL 2b · LEDGER DE APRENDIZAJE (06_aprendizaje/ — v6.0)
         LEARNINGS · ERRORS · FEATURE_REQUESTS (F-001..F-008) · FUENTES_RADAR
         captura en caliente (regla 31) · promoción semanal · radar de información (regla 33)
```

Por qué así: el contexto es un presupuesto (regla 22 — ACE/ICLR-2026). El núcleo slim nunca se degrada; el detalle especializado entra solo al activar.

## 3. Las 4 dimensiones — dónde vive cada una

### 🧠 COMPORTAMIENTO → `01_nucleo/` (+ skills de conducta)

| Qué | Dónde |
|---|---|
| Reglas de iniciativa 1-33 (respuesta primero, ejecutar>borrar, parseo multi-parte, heartbeat, anti-ban, evals, deltas, superficie agent-first, memoria, venta activa, workflow>agente, presupuesto de autonomía, biblioteca de skills, reflexión tras fallo, flota de producción, ledger de aprendizaje, autoinstalación de skills, producción continua + autoeducación) | núcleo §2 |
| 14 reglas de oro heredadas (lecciones con coste real: byte-a-byte, cifras muertas, MultiEdit parcial…) | núcleo §3 |
| Guardarraíles anti-ban y de canal (máx 3 acciones/día/cuenta, políticas primero, 1 link, sin astroturfing; email ≤80/día, 1 dirección/dominio) | núcleo §7 + skills |
| Formato de respuesta + checklist de cierre (qué declara "hecho": verificado + evidence + pendientes) | núcleo §9-§10 |
| Límites de autonomía (qué hace sin preguntar vs qué escala al humano) | núcleo §2.2 + §17 gates + skill maquina-ventas |
| Identidad digital (contribuidor con cuenta propia, disclosure, idioma espejo) | núcleo §4 + AGENTS.md |

### ⚙️ LÓGICA → `01_nucleo/` (§8, §13, §15, §17) + `03_logica/`

| Qué | Dónde |
|---|---|
| Árbol de decisión BOOT (interrogativo: worklog → verify → pregunta → plan) | núcleo §8 + `03_logica/arbol-decision-boot.md` |
| Árbol de decisión VENTAS (pipeline, cupo, bloqueos, producción) | `03_logica/arbol-decision-boot.md` §B |
| Máquina de estado del trabajo: estados PLAN→EXECUTE→CHECKPOINT→VERIFY→CLOSE, checkpoint de 5 campos, 3 gates (G1 irreversible · G2 presupuesto · G3 divergencia) *(v5.0)* | núcleo §17 + skill bucle-autonomo |
| Clasificación workflow vs agente + 5 patrones de flujo *(v5.0)* | regla 26 + skill patrones-flujo |
| Escaleras de ejecución (comercial 26, outreach técnico, publicación en plataformas, anti-ban) | `03_logica/escaleras-de-ejecucion.md` + skills escalera-outreach / maquina-ventas |
| Priorización de pendientes (🔴/cola/congelados) y re-verificación al arrancar; cola viva del run autónomo *(v5.0)* | núcleo §13 + skill bucle-autonomo §2 |
| Mejora continua: fricción → regla → CHANGELOG → eval (cómo aprende) + fábrica de skills (éxito → skill) + post-mortem (fallo → lección) *(v5.0)* + **CICLO DE AUTO-MEJORA en 4 cadencias con ledger y radar (v6.0)** | núcleo §15 + §18 + skills biblioteca-skills / reflexion-post-mortem / ledger-autoaprendizaje / autoinstalador-skills |
| Verificación del propio cerebro: 52 escenarios E01-E52, graders deterministas primero (incl. `zolo_auditar_skills.py` exit 0), eval al 0% = eval roto | `01_nucleo/EVALS.md` |

### 🧩 SKILLS → `02_skills/` (25 carpetas, cada una con SKILL.md + frontmatter, auditor verde 25/25)

| Skill | Dispara cuando |
|---|---|
| `runbook-incidentes` | sitio caído, deploy roto, 401, ban, reset, alerta |
| `escalera-outreach` | publicar/responder/promocionar en plataformas externas |
| `plan-y-ejecucion` | tarea >30 min, multi-etapa, divergencia 2x |
| `best-of-n-decisiones` | respuesta pública sensible, email a partner, pricing |
| `subagentes-contrato` | CUALQUIER lanzamiento de subagente (contrato de 6 líneas) |
| `seguridad-fuentes` | leer contenido externo, activar skills/MCP de terceros (anti tool-poisoning) |
| `tareas-largas` | trabajo multi-sesión, migraciones, campañas |
| `mantenimiento-mensual` | primer BOOT del mes, vigilancia de mercado |
| `mcp-compliance-2026` | /api/mcp, claims en directorios, auditar servers |
| `iniciativa-agent-first` | lanzar producto, "hazlo agent-first", "como taiko" |
| `memoria-alethech` | commit/verify/evidence/export, cadena comprometida, DR, rotación |
| `maquina-ventas` | "vende", "busca trabajo", "ingresos", "atraer agentes", "cold email", "pipeline" |
| `patrones-flujo` *(v5.0)* | inicio de toda tarea grande: workflow vs agente + patrón (chaining/routing/parallelization/orchestrator-workers/evaluator-optimizer) |
| `bucle-autonomo` *(v5.0)* | tarea abierta/multi-horizonte: run con presupuesto + terminators + cola + checkpoints |
| `memoria-jerarquica` *(v5.0)* | sesión larga, contexto crecido, resultados grandes (paginación de memoria de trabajo) |
| `biblioteca-skills` *(v5.0)* | éxito 2+ veces → fabricar skill nueva; poda mensual de skills sin uso |
| `reflexion-post-mortem` *(v5.0)* | fallo verificado propio → post-mortem de 4 campos ANTES de corregir |
| `equipo-virtual` *(v5.0)* | pipeline recurrente multi-fase con roles (Orquestador/Investigador/Constructor/Auditor/Comercial) y handoff por artefacto |
| `flota-produccion` *(v6.0)* | tarea con ≥2 piezas independientes: despacho paralelo en un mensaje, revisión por artefacto, escéptico con veto, rulings-not-stalls, 4 paradas |
| `ledger-autoaprendizaje` *(v6.0)* | comando falla / usuario corrige / hueco detectado / antes de tareas mayores: captura y reuso del ledger 06_aprendizaje/ |
| `autoinstalador-skills` *(v6.0)* | hueco de capacidad o mejora de skill: buscar→clonar→auditar→adaptar→instalar→indexar (script `zolo_instalar_skill.py`) |
| `depuracion-sistematica` *(v6.0)* | CUALQUIER bug/test rojo/fallo ANTES del primer fix: causa raíz o nada (Ley de Hierro, 4 fases) |
| `diseno-web-premium` *(v6.0)* | construir/revisar interfaces: sistema de diseño + UX 1-10 + anti-slop + auditoría a 3 anchos (reel 1) |
| `cumplimiento-legal-vibecoding` *(v6.0)* | antes de publicar apps que recolectan datos: COPPA, fonts, recording, unsubscribe, renewals, DMCA (reel 12) |
| `canales-distribucion` *(v6.0)* | lanzar productos: r/SideProject → HN → PH (mar-mié-jue) → Indie Hackers → Uneed (reel 8) |

### 📚 CONOCIMIENTO → `04_conocimiento/` (datos verificados, no reglas)

| Archivo | Contenido |
|---|---|
| `05_ESTADO_DEL_ARTE_V5.md` *(v5.0, raíz del paquete)* | Repos de agentes más estrella (~180k AutoGPT … Anthropic) + patrones extraídos + lista de mejoras M1-M12 + qué NO se adoptó |
| `06_ESTADO_DEL_ARTE_V6.md` *(v6.0, raíz del paquete)* | **Los 12 reels del founder descifrados y clasificados + 8 repos clonados y auditados (superpowers 304k, anthropics/skills 183k, ui-ux-pro-max, taste-skill, self-improving-agent…) + mejoras M13-M21 + qué NO se adoptó (trading, shelf corporations…)** |
| `06_aprendizaje/` *(v6.0)* | **Ledger de autoaprendizaje**: LEARNINGS (lecciones por categoría) · ERRORS (fallos con corrección) · FEATURE_REQUESTS (F-001..F-008 del founder) · FUENTES_RADAR (fuentes del radar semanal) |
| `empresa-y-superficie.md` | Canon de la empresa + superficie VIVA verificada con HTTP codes (21-oct-2026) |
| `mercado-evidencia.md` | Evidencia de mercado con URLs (rates, x402, directorios, deliverability) |
| `01_INVENTARIO_ACTIVOS.md` | Todo lo vendible, verificación y deudas de credibilidad |
| `02_OFERTAS_Y_PRECIOS.md` | Ofertas S1-S5, planes UTA, mensaje maestro, objeciones |
| `03_REGISTRO_PLATAFORMAS.md` | Dónde subir todo (Tier 0 agentes / 1 humanos / 2 trabajo) |
| `04_CAMPANA_NEXUS_COLD.md` | Campañas listas + guardarrails + fuentes de leads |
| `05_PROTOCOLO_AGENTE_VENTAS.md` | Protocolo del modo ventas + KPIs |
| `06_OPORTUNIDADES_INMEDIATAS.md` | Trabajo YA (bounties, postings, demanda) |
| `iniciativa-agent-first/` | Caso de estudio Taiko verificado + plan de réplica de 14 movimientos |

## 4. Cómo arranca (3 pasos)

1. Copiar esta carpeta a `download/agente-zolo/` y `01_nucleo/worklog_seed.md` → `/home/z/my-project/worklog.md`
2. Pegar `01_nucleo/BOOTSTRAP_PROMPT.md` como PRIMER mensaje del chat nuevo (GLM-5.3, Thinking ON, esfuerzo máximo)
3. El agente aplica §14 de verificación de montaje (worklog ✓ · 25 skills ✓ · auditor 25/25 ✓ · estados del arte v5+v6 ✓ · 06_aprendizaje ✓ · kit ventas ✓ · cadena alethech fail-closed · credenciales: pedir las que falten, nunca asumir)

## 5. Cómo se alimenta (memoria) y cómo aprende

- **Memoria activa**: `worklog.md` append-only (Task ID / Work Log / Stage Summary) — la única fuente viva entre sesiones.
- **Memoria con cadena de custodia** (regla 24): `alethech commit` estructurado en cada cambio de estado + `evidence` en artefactos + `verify` fail-closed al arrancar + checkpoints para detectar rollback + correcciones que SUPERSEDEN sin borrar.
- **Aprendizaje** (§15 + §18 v6.0): fricción observada → regla nueva (delta) → entrada en CHANGELOG → eval de regresión. Ejemplo real: "nadie nos compra" → regla 25 + E31-E33. **(v6.0)** El ciclo es CONTINUO: ledger en caliente (06_aprendizaje/) → promoción semanal → reglas/skills/evals; radar semanal (`PATRÓN NUEVO:` en worklog); autoinstalador cubre huecos de capacidad.
- **Vigilancia**: mantenimiento-mensual re-verifica mercado, skills y cifras (número muerto = bug de credibilidad). **(v6.0)** Radar semanal con `06_aprendizaje/FUENTES_RADAR.md` (GitHub trending, HN, awesome lists, fuentes del founder — reels incluidos).

## 6. Qué NO es este paquete

- No incluye credenciales (PAT, CF, Gmail, npm) — el agente las pide al humano, nunca las asume (§14.3).
- No incluye el sitio ni su código de producción (`universal-trust-adapter` vive en su propio repo; `uta-ai` está en el paquete del agente como réplica/scaffold).
- No envía correos por sí mismo: prepara campañas para NEXUS COLD y las respuestas entran por `support@alicelabs.energy` (otro agente cubre Gmail).
