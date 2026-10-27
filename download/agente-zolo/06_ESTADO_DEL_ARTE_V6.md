# ESTADO DEL ARTE v6.0 — Ronda 2: reels del founder + repos de auto-mejora (Task 123)

> Origen: el founder entregó una lista de 12 URLs de Instagram reels + el mandato: "investiga cual te conviene instalar, busca los repos y descarga… necesito mejorar mas el agente, que aprenda de sus errores, que tenga iniciativa, que se dedique a producir, que trabaje todo el tiempo, aprenda a delegar a subagentes, se instale automaticamente nuevas skills, mejore las que tiene, este siempre autoeducandose, continuamente informandose, al dia con todo".
> Método: (1) descifrado de los 12 reels vía fetch directo; (2) búsqueda de los repos mencionados + los repos MÁS ESTRELLA del ecosistema de skills/autonomía; (3) clonación y auditoría de 8 repos en `repos/`; (4) extracción de patrones → implementación como protocolo (reglas 30-33 + §18 + 7 skills + 3 scripts). Complementa a `05_ESTADO_DEL_ARTE_V5.md` (ronda 1: 15 repos de autonomía).

## 1. Los 12 reels descifrados y su clasificación

| # | Reel | Tema | Decisión |
|---|---|---|---|
| 1 | DegSH0wymBj | 5 herramientas contra el "AI-slop": taste-skill, ui-ux-pro-max, references, impeccable, subagentes build+audit | **INSTALAR** → repos clonados + skill `diseno-web-premium` |
| 2 | DeTmiIRNIdO | Mesa de trading con 6 bots en grupo (uno escéptico que tumba operaciones flojas, 24/7) | **PATRÓN** (no trading): escéptico con veto + trabajo 24/7 → regla 30 + regla 33. Los bots de trading NO se instalan (riesgo financiero fuera del alcance) |
| 3 | DebO8GQsIPQ | Store de plugins ChatGPT = App Store 2008 (caso $500K ARR semana 1) | **CONOCIMIENTO** → canal de distribución: skill `canales-distribucion` §3 |
| 4 | DeAZpJsBT3i | Respondent (user research pagado $150-600/session) | **NO ADOPTAR**: actividad humana (el founder puede hacerlo; el agente no cobra entrevistas) |
| 5 | De0wmPPoUYw | LTX-2.5 video local (open source) | **CONOCIMIENTO**: sin GPU NVIDIA en el entorno; no instalable aquí. Re-clonable si hay hardware |
| 6 | DeaG4dZAl10 | Printify + arte IA (print-on-demand) | **OPORTUNIDAD DE NEGOCIO** anotada — requiere cuenta del founder; sin Skill |
| 7 | DePYpL0uLSo | Claude Startups (1 año Claude Team + $1k API + $45k descuentos) | **DECISIÓN DEL FOUNDER** (elegibilidad de AliceLabs; ventana: fundada <5 años) |
| 8 | De1aXzyjR-1 | 5 sitios para lanzar apps: r/SideProject, HN, Product Hunt (mar-mié-jue), Indie Hackers, Uneed | **INSTALAR** → skill `canales-distribucion` |
| 9 | DekY0_Ly6f9 | Repos gratis que sustituyen herramientas de pago + yantra-app/awesome-workflow-templates (365 workflows n8n) | **INSTALAR** → repos clonados + FUENTES.md (Tier 1) |
| 10 | Dez8oF2hIFH | OpenAI Ads dentro de ChatGPT (ads manager, primeros en LATAM) | **OPORTUNIDAD** anotada — requiere presupuesto del founder (G1 del núcleo: gasto = mandato) |
| 11 | DcTdpM8toN7 | Shelf corporations (crédito instantáneo) | **NO ADOPTAR**: zona ética gris (guardarraíles §7 — nada que huele a esquema de crédito) |
| 12 | Dd8YqaajpGR | Riesgos legales del vibe coding: 6 fixes (COPPA, fonts, session recording, unsubscribe, renewal terms, DMCA) | **INSTALAR** → skill `cumplimiento-legal-vibecoding` |

Balance: **4 instalar · 3 patrón/conocimiento · 2 oportunidad (decisión founder) · 2 no adoptar · 1 decisión del founder**. Nada se ignoró (regla 13 — parseo multi-parte).

## 2. Los 8 repos clonados (en `repos/`, re-clonables — ver FUENTES.md)

| Repo | ≈Estrellas | Qué se extrajo → dónde quedó |
|---|---|---|
| `obra/superpowers` | ~304k | subagent-driven-development (subagente fresco por tarea + revisión por artefacto + LEDGER que sobrevive compaction + rulings-not-stalls + 4 paradas) y dispatching-parallel-agents (dominios independientes + despacho en UNA respuesta) → regla 30 + skill `flota-produccion`. systematic-debugging (Ley de Hierro: no fix sin causa raíz; 4 fases) → skill `depuracion-sistematica`. 15 skills de disciplina como referencia permanente |
| `anthropics/skills` | ~183k | spec agentskills.io + template oficial + skills de referencia (frontend-design, skill-creator) → estándar de las skills v6.0 + FUENTES Tier 0 |
| `nextlevelbuilder/ui-ux-pro-max-skill` | ~100k | tabla de prioridad UX 1-10 (accesibilidad CRÍTICA primero), 79 estilos/192 paletas/74 pares tipográficos/119 guías, anti-patrones explícitos → skill `diseno-web-premium` §3-§4 |
| `VoltAgent/awesome-agent-skills` | top del tema | el MAPA de 1000+ skills curadas → motor de búsqueda del autoinstalador (regla 32 paso 2) |
| `pskoett/self-improving-agent` | ~777 | patrón `.learnings/` (LEARNINGS/ERRORS/FEATURE_REQUESTS + captura→revisión→reuso→promoción, categorías, formato grep-able) → regla 31 + `06_aprendizaje/` + skill `ledger-autoaprendizaje` |
| `Leonxlnx/taste-skill` | top del tema | proceso de 6 pasos anti-slop (brief → direcciones → idea → build con fotos reales → check en navegador a 3 anchos → look-and-fix ×3) + bans + motion → skill `diseno-web-premium` |
| `yantra-app/awesome-workflow-templates` | — | 365 workflows tipo n8n (Slack, Gmail, Notion, agentes, RAG) → FUENTES Tier 1 como recetario de automatización |
| `Leonxlnx/unlazy` | — | full-output-enforcement (cero placeholders/trabajo a medias) → FUENTES Tier 1 + refuerzo de regla 2 |

## 3. Mejoras M13-M21 (trazadas fuente→implementación)

| ID | Mejora | Fuente | Implementación |
|---|---|---|---|
| M13 | Delegación real de producción (subagente fresco por pieza + paralelo en 1 mensaje + revisión por artefacto) | superpowers | regla 30 + skill `flota-produccion` |
| M14 | Ledger de aprendizaje en caliente con promoción (errores → lecciones → reglas/skills) | self-improving-agent | regla 31 + `06_aprendizaje/` + skill `ledger-autoaprendizaje` + §18 |
| M15 | Autoinstalación de skills con auditoría de seguridad | Voyager (ronda 1) + skills CLI + FUENTES | regla 32 + skill `autoinstalador-skills` + `zolo_instalar_skill.py` |
| M16 | Causa raíz obligatoria antes de cualquier fix | superpowers systematic-debugging | skill `depuracion-sistematica` (refuerza regla 29) |
| M17 | Escéptico con veto + rulings-not-stalls + 4 paradas | mesa de 6 bots (reel 2) + superpowers | regla 30 §4-§6 + skill `flota-produccion` |
| M18 | Diseño anti-slop verificable (sistema de diseño + auditoría en navegador a 3 anchos) | taste-skill + ui-ux-pro-max + impeccable (reel 1) | skill `diseno-web-premium` |
| M19 | Checklist legal pre-lanzamiento de apps | reel 12 | skill `cumplimiento-legal-vibecoding` |
| M20 | Distribución ordenada por canal | reel 8 + reel 3 | skill `canales-distribucion` |
| M21 | Producción continua 24/7 con autoeducación (nunca idle) | reel 2 + mandato del founder | regla 33 + §18 ciclo de 4 cadencias + `FUENTES_RADAR.md` |

## 4. Qué NO se adoptó (y por qué)

- **Frameworks runtime de skills** (plugin marketplaces, harnesses): ZOLO consume PATRONES en protocolo markdown — sobreviven a resets (regla 22). Los repos quedan como biblioteca de consulta, no como dependencias.
- **Bots de trading** (reel 2): riesgo financiero real; el patrón organizativo sí se adoptó.
- **Shelf corporations** (reel 11): zona ética gris — guardarrail §7.
- **Respondent / user research pagado** (reel 4): actividad humana; el agente la prepara, no la ejecuta.
- **LTX-2.5** (reel 5): sin GPU en el entorno; documentado para re-clonar cuando exista hardware.
- **OpenAI Ads / Printify / Claude Startups** (reels 6, 7, 10): requieren gasto, cuentas o decisiones del founder — anotadas como oportunidades con dueño TÚ (regla 2).

## 5. Resultado neto de la ronda

**8 peticiones del founder → 8 resueltas** (F-001..F-008 en `06_aprendizaje/FEATURE_REQUESTS.md`): aprender de errores (regla 31) · iniciativa (reglas heredadas + 33) · producir (regla 30) · trabajar todo el tiempo (regla 33) · delegar a subagentes (regla 30 + flota) · autoinstalar skills (regla 32) · mejorar las existentes (14 skills con grader nuevo + auditor 25/25 verde) · autoeducarse y estar al día (radar + §18).

Estado final: **33 reglas · 25 skills (25/25 en auditoría) · E01-E52 · §17 máquina de estado · §18 ciclo de auto-mejora · 06_aprendizaje/ operativo · 3 scripts de maquinaria · 8 repos de referencia**.
