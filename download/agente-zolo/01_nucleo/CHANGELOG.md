# CHANGELOG — ZOLO

Versionado semántico: **PATCH** = aclaración · **MINOR** = regla nueva · **MAJOR** = cambio de arquitectura.

---

## v6.0 — 2026-10-24 (MAJOR: AUTÓMATA — auto-mejora, delegación y producción continua)

**Origen**: el founder entregó 12 URLs de reels + mandato: "de esta lista… investiga cual te conviene instalar, busca los repos y descarga… necesito mejorar mas el agente, que aprenda de sus errores, que tenga iniciativa, que se dedique a producir, que trabaja todo el tiempo, aprenda a delegar a subagentes, se instale automaticamente nuevas skills, mejore las que tiene, este siempre autoeducandose, continuamente informandose, al dia con todo" (Task 123). Los 12 reels fueron descifrados uno a uno y clasificados; investigación y trazado completo en `06_ESTADO_DEL_ARTE_V6.md` (mejoras M13-M21). Las 8 peticiones del founder quedaron resueltas y registradas como **F-001..F-008** en `06_aprendizaje/FEATURE_REQUESTS.md`.

**Repos clonados y auditados (8, en `repos/` — re-clonables vía `02_skills/biblioteca-skills/FUENTES.md`)**: `obra/superpowers` ~304k★ (subagent-driven-development, dispatching-parallel-agents, systematic-debugging) · `anthropics/skills` ~183k★ (spec + template oficial) · `nextlevelbuilder/ui-ux-pro-max-skill` ~100k★ (UX 1-10, 192 paletas) · `VoltAgent/awesome-agent-skills` (mapa de 1000+ skills) · `pskoett/self-improving-agent` (patrón .learnings) · `Leonxlnx/taste-skill` (anti-slop de 6 pasos) · `yantra-app/awesome-workflow-templates` (365 workflows) · `Leonxlnx/unlazy` (output enforcement).

**Reglas nuevas (30-33):**
- **30 FLOTA DE PRODUCCIÓN POR DELEGACIÓN REAL**: subagente fresco por pieza + despacho paralelo EN UN SOLO MENSAJE + revisión por artefacto + ledger en archivo + RULINGS NOT STALLS + 4 paradas + escéptico con veto (M13+M17).
- **31 LEDGER DE APRENDIZAJE EN CALIENTE**: captura en el momento en `06_aprendizaje/` (LEARNINGS/ERRORS/FEATURE_REQUESTS), reuso antes de tareas mayores, promoción semanal a regla/skill/eval (M14).
- **32 AUTOINSTALACIÓN DE SKILLS**: hueco → buscar (FUENTES.md) → clonar → auditar (seguridad-fuentes) → adaptar → instalar → indexar; jamás "no puedo X" sin ciclo; máx ~30 skills (M15).
- **33 PRODUCCIÓN CONTINUA + AUTOEDUCACIÓN**: nunca idle (cola → verificación → radar → mejora de skills → producción); radar semanal grep-able (`PATRÓN NUEVO:`); reels del founder se descifran y clasifican (M21).

**Sección nueva §18 — CICLO DE AUTO-MEJORA CONTINUA**: 4 cadencias (en-caliente · diaria · semanal · mensual) con salida verificable cada una + motor del ciclo (ledger → promoción → reglas/skills/evals → autoinstalador) + garantía de existencia (patrón 2+ veces sin promover = deuda mensual).

**Directorio nuevo `06_aprendizaje/`**: `LEARNINGS.md` · `ERRORS.md` (1ª entrada viva: bug de YAML block scalar del instalador, corregido en caliente) · `FEATURE_REQUESTS.md` (F-001..F-008) · `FUENTES_RADAR.md` (radar de fuentes semanal + protocolo de reels).

**Skills nuevas (7 → 25 total)**: `flota-produccion` (M13+M17) · `ledger-autoaprendizaje` (M14) · `autoinstalador-skills` (M15) · `depuracion-sistematica` (M16, Ley de Hierro: no fix sin causa raíz) · `diseno-web-premium` (M18, reel 1) · `cumplimiento-legal-vibecoding` (M19, reel 12) · `canales-distribucion` (M20, reel 8). **Mejora de las existentes**: 14 skills v3.x recibieron sección Grader a medida (regla 32 §2) — auditor `zolo_auditar_skills.py` verde 25/25.

**Scripts de maquinaria (3, en `scripts/`)**: `zolo_instalar_skill.py` (clonar→localizar→auditar→instalar; parser YAML con block scalars tras bug corregido en vivo; testado contra repos reales) · `zolo_auditar_skills.py` (auditoría completa del paquete; exit code como grader determinista E52) · `zolo_mejorar_skills_v6.py` (lote de graders v6.0 a skills legacy).

**EVALS nuevos (E43-E52)**: ledger en caliente · despacho paralelo · escéptico con evidencia · rulings · ciclo de autoinstalación · auditoría de skills de terceros · causa raíz antes que fix · reels descifrados · producción continua · auditor verde. Suite de regresión E01-E52.

**No cambió**: reglas 1-29, reglas de oro, §17 máquina de estado, kit de ventas, guardarraíles, protocolo worklog/alethech, uta-ai, pendientes §13. Edición por deltas quirúrgicos (regla 22). Backup v5.0: `archive/ZOLO_V5.md` + zip `AGENTE_ZOLO_v5.0.zip`.

---

## v5.0 — 2026-10-24 (MAJOR: ESTADO DEL ARTE DE AUTONOMÍA Y DISEÑO DE AGENTES — repos más estrella implementados)

**Origen**: "revisa los repos que tengas mas estrellas con lo que tenga que ver con autonomia y diseño de agentes, busca los mejores puntos e implementa, haz una lista de mejoras para este agente, crea el mejor agente del mundo" (Task 122, founder). Investigación completa con 15 repos trazados repo-a-repo → `05_ESTADO_DEL_ARTE_V5.md` (mejoras M1-M12).

**Repos fuente (estrellas ≈ oct-2026)**: AutoGPT ~180k (lección: bucles sin límite descarrilan) · LangChain ~134k · MetaGPT ~55k (SOPs) · OpenHands ~50k (event stream) · AutoGen/MS Agent Framework ~45k (terminators) · CrewAI ~35k (roles legibles) · BabyAGI ~21k (cola viva) · MemGPT/Letta ~17k (jerarquía de memoria) · SWE-agent ~16k (ACI ergonómica) · SuperAGI ~16k · LangGraph (checkpoints + HITL interrupts) · Voyager y Reflexion (seminales: skill factory, post-mortems) · DeepAgents (planning + filesystem + subagentes aislados) · Anthropic "Building Effective Agents" (5 patrones + budget-aware + "think like your agent").

**Reglas nuevas (26-29):**
- **26 WORKFLOW > AGENTE CUANDO EL CAMINO ES MAPEABLE**: clasificación en 1 línea + los 5 patrones (chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer); prohibido improvisar autonomía donde un flujo determinista basta (M1).
- **27 PRESUPUESTO DE AUTONOMÍA CON TERMINATORS**: todo bucle arranca con presupuesto explícito y 4 terminators (T1 objetivo · T2 presupuesto · T3 progreso nulo ×3 · T4 gate humano); al dispararse: STOP + checkpoint + opciones, nunca "una iteración más" (M2).
- **28 BIBLIOTECA DE SKILLS VIVA**: éxito 2+ veces (o 1 vez caro) → skill nueva con frontmatter + grader + contrato de salida ergonómico (ACI de SWE-agent); poda a los 2 meses sin uso (M7).
- **29 REFLEXIÓN TRAS FALLO, NO SOLO TRAS FRICCIÓN**: post-mortem de 4 campos (esperaba/obtuve/causa raíz/LECCIÓN grep-able) ANTES de corregir; lección → regla + eval + skill candidata (M8).

**Sección nueva §17 — MÁQUINA DE ESTADO DEL TRABAJO**: IDLE→PLAN→EXECUTE⟲→CHECKPOINT→VERIFY→CLOSE; checkpoint de 5 campos reanudable; 3 gates estándar (G1 irreversible · G2 presupuesto · G3 divergencia 2x); auditoría de contexto al activar skills ("think like your agent", M12); event log por acción (OpenHands, M5). Base: LangGraph checkpoints + interrupts.

**Skills nuevas (6 → 18 total):** `patrones-flujo` (M1+M10+M12) · `bucle-autonomo` (M2+M3+M4+M5: apertura de run, cola BabyAGI, terminators, checkpoints, anti-loops) · `memoria-jerarquica` (M6: 4 capas ventana→archivo→worklog→alethech, memoria auto-editable estilo MemGPT) · `biblioteca-skills` (M7: fábrica Voyager + ACI + poda) · `reflexion-post-mortem` (M8: protocolo de 4 campos + clasificación de causa raíz + memoria episódica) · `equipo-virtual` (M9: 5 roles con SOP — Orquestador/Investigador/Constructor/Auditor/Comercial — handoff por ARTEFACTO, no conversación).

**EVALS nuevos**: E35 (patrón declarado en tareas mapeables) · E36 (run presupuestado en tareas abiertas) · E37 (stop en T2) · E38 (paginación de memoria) · E39 (fábrica de skills) · E40 (post-mortem antes de corregir) · E41 (equipo por artefactos) · E42 (autosuficiencia de contexto). Suite de regresión E01-E42.

**Decisión de diseño (no adoptar frameworks)**: ZOLO adopta los PATRONES en protocolo markdown, no librerías runtime (LangGraph/AutoGen/CrewAI como dependencias). Razón: sobrevivir a resets del entorno (regla 22) y mantener el núcleo auditable. Se descartaron: plataformas low-code, chat multiagente libre, memoria vectorial externa, tree search masivo — trazado en `05_ESTADO_DEL_ARTE_V5.md` §4.

**Arquitectura**: se mantiene 2 niveles; el índice de skills pasa a 18 líneas. Backup v4.0: `archive/ZOLO_V4.md` (in-package) + zip `AGENTE_ZOLO_v4.0.zip` (regla 22).

**No cambió**: reglas 1-25, reglas de oro, kit de ventas, guardarraíles, protocolo worklog/alethech, uta-ai, pendientes §13. Edición por deltas quirúrgicos (regla 22).

---

## v4.0 — 2026-10-24 (MAJOR: NUEVA IDENTIDAD ZOLO + recreación completa del paquete + verificación en vivo del estado)

**Origen**: "revisa todo lo que tiene que ver con el agente, recrealo. se llama zolo" (Task 121, founder). El agente tiene ahora nombre propio: **ZOLO**.

**Qué cambió:**
- **Identidad**: el agente se llama ZOLO (núcleo §0, BOOTSTRAP, mapa, README, AGENTS.md, firma en superficies públicas como "ZOLO (AliceLabs)"). El paquete se renombra: `download/agente-zolo/` + núcleo `ZOLO_V4.md` (antes `agente-marketnow-v2/` + `AGENTE_MARKETNOW_V3.md`). Renombre mecánico verificado programáticamente: 0 referencias viejas restantes.
- **Herencia íntegra de v3.3**: 25 reglas de iniciativa · 14 reglas de oro · 12 skills on-demand · E01-E33 · kit `ventas-alicelabs/` (7 archivos) · uta-ai · guardarraíles anti-ban · memoria alethech. Nada se regeneró de cero — copia + deltas quirúrgicos (regla 22).
- **Verificación EN VIVO al momento de la recreación (24-oct-2026, Task 121)**: `/api/health` 200 (worker `marketnow-edge` v4.2.0, features: sentinel-l1, leaderboard, arena, quests, agent-hire, submit, m2m-checkout, agent-rep, agent-referral) · `/api/skills` **71,198** · `/uta/conformance/vectors/_index.json` 200 · npm `@marketnow/uta-conformance@1.4.0` latest · `/SKILL.md` **200 (antes 404 — RESUELTO)** · `/llms.txt` + `/llms-full.txt` 200 · `/agents` 200 · `/atc` 200 · `/api/mcp` **200 (Worker desplegado)** · `/.well-known/glama.json` 200.
- **Pendientes §13 actualizados** con ese estado (items 3/8/17): lo que ya sirve 200 queda marcado; queda pendiente la INSPECCIÓN de schema de `/api/mcp` antes de claims en directorios.
- **Memoria §11**: añadida referencia de interfaz — `Alethech Notebook` (design concept React/Vite, Figma Make) como UI conceptual del notebook de memoria; no bloquea operación CLI.

**No cambió**: reglas 1-25, reglas de oro, skills (12), EVALS E01-E33 (+E34 nuevo), arquitectura 2 niveles, kit de ventas, guardarraíles, protocolo worklog/alethech. Edición por deltas con verificación grep (regla 22).

**EVALS nuevo**: E34 (identidad — ZOLO responde a su nombre y se presenta como ZOLO de AliceLabs; ninguna superficie lo llama "Agente MarketNow").

---

## v3.3 — 2026-10-21 (MINOR: regla 25 VENTA ACTIVA CON EVIDENCIA + skill maquina-ventas + kit de ventas completo)

**Origen**: "NO, QUIERO QUE TE DEDIQUES A COSAS NUEVAS, OTRO AGENTE YA ESTA EN GMAIL. QUIERO QUE TU BUSQUES TRABAJO, SEAS AGENTE DE TRABAJO, BUSCA COMO VENDER TODA LA TECNOLOGIA QUE TENEMOS... SE SUPONE QUE MEJORAMOS UNA HERRAMIENTA DE COLD EMAIL, SE LLAMA NEXUS COLD, TOMALO EN CUENTA PARA ENVIAR CORREOS... NECESITAMOS VENDER, INGRESOS URGENTES, COSAS REALES... BUSCA EN ESPECIAL AGENTES, VE DONDE PUEDES SUBIR TODO LO QUE TENEMOS" (Task 120).

**Regla nueva:**
- **25 VENTA ACTIVA CON EVIDENCIA**: el agente opera como agente de trabajo — kit canónico `download/ventas-alicelabs/` (7 archivos) · ninguna cifra en un pitch sin re-verificación en vivo (>7 días = prohibida) · lead sin personalización real = correo prohibido · ≤80 emails/día por dirección, 1 dirección/dominio · prioridad caja-antes-de-glamour (a) demanda existente → (b) servicios → (c) listings de agentes → (d) lanzamientos → (e) marketplace.

**Skill nueva (12 en total):** `maquina-ventas` — reglas 25-28 (25 evidencia, 26 escalera comercial, 27 guardarrails de canal, 28 caja antes de glamour), 5 flujos, límites de autonomía.

**Entregable — kit `download/ventas-alicelabs/`** (verificado en vivo 21-oct-2026): `01` inventario con HTTP codes (/api/health v4.2.0 con features agent-hire + m2m-checkout · /api/skills 71,198 · /agents 200 · MAP v1.1.0 · /atc 200 · npm conformance 1.4.0; deudas: drift llms.txt 68,388, /SKILL.md 404, /handshake 404) · `02` ofertas S1-S5 ($400-$2,500, ancladas a rates verificados $20-150/hr) + planes UTA + carril x402 ($24.24M/mes, Cloudflare Monetization Gateway cobra llamadas MCP) · `03` registro de plataformas Tier 0/1/2 (PulseMCP pausado → Official MCP Registry es EL camino; flujo alethech como playbook probado) · `04` campaña NEXUS COLD (guardarrails MailReach 2026: ≤80/día, 1 dir/dominio, warm-up ≥15%; 4 segmentos, secuencias EN/ES día 0/3/7 listas) · `05` protocolo con árbol de decisión y KPIs · `06` oportunidades verificadas (Upwork categoría MCP existe; Opire bounties $20+ fee 4%; GitHub label:bounty; Algora challenges).

**EVALS:** E31 (pitch = cifras re-verificadas + 1 oferta + 1 CTA) · E32 (cupo ≤80/día no negociable) · E33 (leads solo de fuentes públicas con fuente registrada). Suite de regresión E01-E33.

**Pendientes §13 nuevos:** 15 NEXUS COLD config (TÚ, bloquea campañas) · 16 push uta-ai + listings Tier 0 · 17 deploy CF (drift + /SKILL.md + glama.json) · 18 leads+bounties cada BOOT (YO). NEXUS COLD registrado como activo a documentar (no estaba en worklog).

**No cambió:** reglas 1-24, §11 memoria, runbook, arquitectura 2 niveles, uta-ai. Edición por deltas (regla 22); verificación grep tras cada batch (lección Task 119 aplicada: 1 edit redundante detectado y descartado sin daño).

---

## v3.2 — 2026-10-21 (MINOR: regla 24 MEMORIA CON CADENA DE CUSTODIA + protocolo alethech completo + Hostinger congelado)

**Origen**: "HAZLO, DE HOSTINGER DEJA NOMAS, CÉNTRATE EN EL RESTO, APLICA LOS CAMBIOS DEL AGENTE, REVISA ALETHECH TAMBIEN PARA QUE MEJORES MEMORIA". Revisión del repo propio `eddyflores100-lang/alethech` ejecutada 21-oct-2026 (README crudo v0.9.1 vía raw.githubusercontent + listing mcpservers.org + presencia en TeleAI-UAGI/Awesome-Agent-Memory y MCP Registry oficial `io.github.eddyflores100-lang/alethech`).

**Regla nueva:**
- **24 MEMORIA CON CADENA DE CUSTODIA**: commit estructurado al cerrar todo cambio de estado (qué/cuándo/evidencia/pendientes) · `evidence` para artefactos verificables · `verify` FAIL-CLOSED al arrancar (cadena inválida = incidente, jamás sobrescribir para "arreglarla") · correcciones que SUPERSEDEN sin borrar (bi-temporal) · checkpoints obligatorios — alethech NO detecta rollback sin checkpoint externo, así que el agente los emite en cada cambio de definición y cierre de sesión con estado · sin commit de cierre el siguiente BOOT arranca ciego (Task 114).

**§11 reescrito — protocolo completo**: tres capas por autoridad (cadena firmada > worklog > definición) · superficie CLI de 9 comandos (`init` `commit` `evidence` `verify` `export` `import` `key rotate` `key revoke` `migrate`) · puente MCP read-only `alethech-mcp` (credenciales=config, nunca argumentos de tool) · ciclo de vida en 6 pasos con gate de novedad · contenedor portátil `.aleth` (scrypt + AES-256-GCM; nunca lleva `root.key`/`recovery.key`) · rotación mensual + revocación solo con mandato · simulacro DR trimestral ≤60s (referencia del repo: 42s medidos) · higiene adoptada del ecosistema (gate de novedad estilo Cortex; linter mensual de salud: entradas sin fecha/duplicados/dead links — patrón Verified Memory Vault).

**Skill nueva (11 en total):** `memoria-alethech` — qué prueba y qué NO el protocolo, los 9 comandos, BOOT fail-closed, gate de novedad, formato del commit con `supersede`, evidence, cadencia y DR, relación entre las 3 capas.

**EVALS:** E28 (verify inválido = fail-closed) · E29 (commit+evidence antes de declarar "hecho") · E30 (rollback detection por checkpoint). Suite de regresión E01-E30.

**Pendientes §13 re-priorizados por decisión del usuario:** Hostinger **CONGELADO** (⏸️ "DE HOSTINGER DEJA NOMAS" — no renovar/migrar/recordar; movido a sección "Congelados" y fuera de Decisiones del usuario) → urgentes ahora: 1) Gmail app password, 2) re-claim Glama con glama.json en raíz. Comunidad marcada como la cola más antigua a priorizar (anp2network, CodePass.dev). BOOT paso 3 reescrito (fail-closed + checkpoint continuity + sin store = declararlo). §14 verificación incluye `alethech verify`.

**No cambió:** reglas 1-23, arquitectura 2 niveles, runbook, escalera de outreach, uta-ai. Edición por deltas (regla 22) — sin backup requerido (MINOR). Nota operativa: este entorno NO tiene store `.alethech` ni CLI instalados (se perdieron con el reset #3) — el worklog es la memoria activa hasta `pip install alethech` + `init` en el próximo BOOT.

---

## v3.1 — 2026-10-21 (MINOR: regla 23 SUPERFICIE AGENT-FIRST + réplica del caso de estudio Taiko)

**Origen**: "REVISA EL REPO DE TAIKO, VE LA INICIATIVA MOSTRADA POR EL AGENTE, ESTA EN GITHUB TODO EL CASO DE ESTUDIO, VE SI PUEDES REPLICAR ESE TIPO DE INICIATIVA". Caso verificado en fuentes primarias (github.com/taikoxyz/taiko-ai — 91 commits, v1.5.0, contribuidores dantaik + claude; taikoxyz/taiko-docs — llms.txt / llms-full.txt / .md por página / SKILL.md / browser tests de metadata). Análisis completo: `iniciativa-agent-first/CASO_ESTUDIO_TAIKO.md`.

**Regla nueva:**
- **23 SUPERFICIE AGENT-FIRST**: todo producto de AliceLabs se lanza con su superficie de agente de primera clase en el mismo task — repo `<producto>-ai` (skills + subagentes + MCP servers con schema de salida fijo + plugin Claude Code + audit.md de auto-auditoría de PRs en 3 categorías: bugs / violaciones de reglas / token-efficiency) + docs agent-first en 4 formatos (`/llms.txt`, `/llms-full.txt`, `/<path>.md`, `/SKILL.md` en la raíz del dominio) + agente como contribuidor con identidad propia + CI con drift-check de cifras.

**Skill nueva (10 en total):** `iniciativa-agent-first` — los 7 componentes obligatorios, reglas de calidad del caso Taiko, procedimiento para productos nuevos y señales de oportunidad proactiva.

**Entregable — repo réplica `download/uta-ai/`** (push pendiente de PAT): 4 skills (`uta`, `sentinel-audit`, `marketnow-catalog`, `uta-conformance`, frontmatter validado 4/4) · 2 subagentes (`uta-developer`, `sentinel-auditor`) · `.claude-plugin/` (marketplace 4 plugins + plugin.json) · `mcp-servers/SPEC.md` (uta-local 8 tools + catalog-cache 3 tools) + scaffold v0.1 `catalog-mcp` · `audit.md` con primer registro aplicado · `ci.yml` + **`drift-check.yml`** (cifra viva vs citada, diario 08:00 Guayaquil — mejora propia sobre el patrón) · `scripts/validate_skills.py`.

**Artefactos agent-first para marketnow.site** (`uta-ai/site-agent-first/`): `SKILL.md` del sitio (el 404 → contenido listo para deploy), `GAPS.md` (verificación viva: llms.txt ✓ 200, llms-full.txt ✓ 200, SKILL.md ✗ 404, .md ✗ 404 + **drift detectado: llms.txt 68,388 vs `/api/skills` vivo 71,198**), `llms-v2.txt` generada desde sitemap+APIs vivas (43 rutas HTML, 12 APIs, superficies nuevas `/agents` `/acp` `/agent-passport` `/atc` indexadas), `generate_llms_txt.py` (probado).

**Documentación:** `iniciativa-agent-first/PLAN_REPLICACION.md` — 14 movimientos mapeados Taiko→AliceLabs con estado YO/TÚ/PRÓXIMO BOOT y 5 fases de ejecución.

**No cambió:** núcleo de reglas 1-22, runbook, escalera de outreach, evals E01-E24 (ampliados a E27), arquitectura 2 niveles. Sin backup MAJOR requerido (edición por deltas, regla 22).

---

## v3.0 — 2026-10-21 (MAJOR: arquitectura de 2 niveles + estado del arte 2025-2026)

**Origen**: "verifica el mercado, ve las nuevas actualizaciones de agentes, revisa videos, repos, todo para crear el mejor agente". Investigación con 3 subagentes en paralelo (Tasks 117-a/b/c del worklog), fuentes primarias verificadas: Anthropic Research (context engineering, Managed Agents, harnesses, evals, sandboxing, prompt-injection defenses), Cursor blog (2.0 multi-agente, agent-best-practices ene-2026), LangChain 1.0, Microsoft Agent Framework, OpenAI DevDay 2025/2026, modelcontextprotocol.io (specs hasta 2026-07-28), agentskills.io, agents.md/AAIF, Letta/Mem0, ACE (ICLR 2026), skills.sh.

**Re-arquitectura (2 niveles — Anthropic Skills + Cursor reglas/skills):**
- Núcleo slim: `ZOLO_V4.md` (reglas siempre activas, 22 reglas, índice de skills).
- 9 skills on-demand estilo agentskills.io (SKILL.md con frontmatter name/description): runbook-incidentes, escalera-outreach, plan-y-ejecucion, best-of-n-decisiones, subagentes-contrato, seguridad-fuentes, tareas-largas, mantenimiento-mensual, mcp-compliance-2026.
- Progressive disclosure: el índice (9 líneas) vive en contexto; el cuerpo se carga solo al aplicar.

**Reglas nuevas (18-22):**
- 18 PLAN persistido + reiniciar-desde-el-plan + grind loop acotado (Cursor best-practices, Anthropic harnesses).
- 19 DATO ≠ INSTRUCCIÓN: spotlighting, cuarentena sin credenciales, checklist anti tool-poisoning (Anthropic prompt-injection-defenses, CaMeL, Invariant).
- 20 BEST-OF-N para decisiones irreversibles (Cursor 2.0 + voting Anthropic).
- 21 EVALS de dos niveles + grader determinista primero + "eval al 0% = eval roto" (Anthropic demystifying-evals).
- 22 Presupuesto de atención (BOOT interrogativo, grep antes que leer) + edición por deltas con backup (ACE/ICLR-2026, lección reset #3).

**Otros:**
- §7.7 mandato explícito para acciones de riesgo (patrón AP2/agentic commerce).
- §12 pendientes actualizados con compliance MCP 2026 (Worker dual-era + server/discover + RFC 9728 + server-card SEP-1649 + server.json al Registry oficial) y **corrección crítica: glama.json va en la RAÍZ del repo, no en /.well-known/** (Task 117-c).
- §16 vigilancia de mercado trimestral (codifica esta sesión para que se repita).
- AGENT.md deprecado → **AGENTS.md** canónico (estándar agents.md/AAIF, adoptado por Codex/Cursor/Gemini CLI/Copilot/Cline).
- EVALS.md ampliado a 24 escenarios (E16-E24: plan mode, inyección, grind cap, best-of-N, contrato, eval roto, BOOT interrogativo, deltas, índice de skills).
- Backup v2.1 preservado en `archive/` (regla 22 aplicada a este propio cambio).

---

## v2.1 — 2026-10-21 (MINOR: 5 reglas nuevas + runbook + mejora continua)

**Origen**: auditoría de mejora continua solicitada por el usuario ("verifica como mas podemos mejorar el agente"). Método: releer las 20 muestras de razonamiento + el worklog original buscando fricciones NO cubiertas por v2.0.

**Reglas nuevas (§2, ahora 17):**
- **13 Parseo Multi-parte** — los mensajes del usuario traen 5+ órdenes mezcladas (Muestra #15); cada parte se enumera con dueño y estado. Evidencia: la respuesta del v1 a ese mensaje abordó las 5 pero sin estructura, y en otros turnos quedó una pregunta sin responder.
- **14 Heartbeat en tareas largas** — avances intermedios en tareas >10 tool calls / >5 min; el silencio en IM se lee como abandono.
- **15 Subagentes para investigación pesada** — el v1 delegó solo el 0.04% de sus 25,644 tool calls; umbral >15 calls estimados → subagente con brief autocontenido.
- **16 Higiene de secretos** — el worklog v1 registró prefijos de PAT (`ghp_WhNe…`) en texto claro (Task 98); desde v2.1 solo huella 4+4.
- **17 Plan visible** — TodoWrite obligatorio en tareas de ≥3 pasos.

**Secciones nuevas:**
- **§14 Runbook de incidentes** — sitio caído (rollback antes que diagnóstico), deploy roto, credencial muerta, plataforma bloquea, reset del entorno, alerta de seguridad. Evidencia: Muestra #14 (el v1 reaccionó bien pero sin procedimiento escrito).
- **§15 Mejora continua** — protocolo de 5 pasos (fricción → regla → CHANGELOG → eval), reporte mensual de métricas, compaction mensual del worklog (el v1 creció a 76KB+), auditoría de definición con evidencia.
- **§6 Escalera de ejecución para outreach** — GitHub → telegra.ph → SMTP → OAuth → borrador (solo al agotar). Cierra el dolor de la Muestra #13 por procedimiento, no solo por declaración.
- **§1.4 Snapshot de drift** — `estado_sitio.json` en cada BOOT; el siguiente BOOT compara programáticamente (cifras vivas, schemas, endpoints).
- **§8.5-6** — fechas en hora local del usuario (America/Guayaquil); cierre multi-parte con estado por parte.
- **§3** — 2 reglas de oro nuevas: secretos solo como huella 4+4; toda cifra lleva fecha + fuente.

**Archivos nuevos:** `EVALS.md` (15 escenarios de verificación), `CHANGELOG.md` (este archivo).

---

## v2.0 — 2026-10-21 (MAJOR: reconstrucción completa)

**Origen**: "reconstruye y mejora este agente" con el kit `agent_reconstruction.zip`.

**Reconstruido** (desde chat_meta.json + 20 muestras + worklog Tasks 18/89-93/98-99/114):
- Identidad, misión y contexto canónico del proyecto (MarketNow / AliceLabs / UTA / infra CF).
- Protocolo BOOT de 5 pasos (memoria entre resets, alethech, credenciales, health checks, reporte).
- 12 reglas de iniciativa (9 patrones del v1 + Respuesta Primero + Ejecutar>Borradores + Registro de Plataformas).
- 10 reglas de oro tabuladas con su origen y coste.
- Protocolo worklog append-only con Task IDs continuados desde Task 114.
- Registro de plataformas con estado de acceso verificado (12 filas).
- Guardarraíles anti-ban (contador 3/día, políticas primero, disclosure) y éticos (cero astroturfing).
- Formato de respuesta, árbol de decisión preguntar/actuar, checklist de cierre, memoria alethech, pendientes canónicos, verificación de recreación.

**Mejoras vs el manual v1 del kit**: Respuesta Primero (deuda del caso Cline), Ejecutar>Borradores (Muestra #13), Implementar-antes-de-responder formalizado (Muestra #8), registro de plataformas (ciclo V2EX/Linux.do), credenciales al BOOT (3 muertes de tokens no detectadas a tiempo), recuperación post-reset estandarizada (Task 99), reglas de oro consolidadas, AGENT.md portable para Cline/Cursor (resuelve la pregunta jamás respondida), worklog semilla con numeración continua.

**Archivos**: AGENTE_MARKETNOW_V2.md · BOOTSTRAP_PROMPT.md · worklog_seed.md · AGENT.md · README.md.
