# Worklog — MarketNow / UTA multi-agent log (semilla v4.0 ZOLO, reconstruido 24-oct-2026)

> NOTA DE RECONSTRUCCIÓN: el filesystem original se perdió (reset #3 documentado). Este archivo se siembra desde el kit `agent_reconstruction.zip`: snapshots de worklog (Tasks 18, 89-93), entradas perdidas (Tasks 94-99) y memoria alethech (Task 114, deploy 1-oct-2026). La numeración continúa desde el último Task verificado en la cadena de memoria (Task 114). **Toda cifra marcada [recuperado] debe re-verificarse contra las fuentes vivas en el próximo arranque.**

## ESTADO VERIFICADO EN VIVO (24-oct-2026, Task 121 — recreación ZOLO v4.0)

- `/api/health` → **200** · worker `marketnow-edge` · versión **4.2.0** · features: sentinel-l1, leaderboard, arena, quests, agent-hire, submit, m2m-checkout, agent-rep, agent-referral
- `/api/skills` → **71,198** skills (totalPages 3560, 16 categorías) — cifra viva
- `/uta/conformance/vectors/_index.json` → **200** · npm `@marketnow/uta-conformance@1.4.0` = latest en registry
- Superficies agent-first: `/SKILL.md` **200 (RESUELTO, era 404 en v3.3)** · `/llms.txt` 200 · `/llms-full.txt` 200 · `/agents` 200 · `/atc` 200 · `/api/mcp` **200 (Worker desplegado)** · `/.well-known/glama.json` 200
- Pendiente de inspección: schema de `/api/mcp` (dual-era, server/discover, RFC 9728, server-card SEP-1649) y drift de cifras dentro de llms.txt — verificar antes de claims en directorios

## ESTADO RECUPERADO — heredado (21-oct-2026, [recuperado] — re-verificar lo no re-sellado hoy)

- Proyecto: MarketNow (marketnow.site) — 71,198 MCP skills auditadas (VERIFICADO HOY; historial: 69,077 stats.json 12-sep · 68,617 deploy 1-oct), certificados Sentinel
- Empresa: AliceLabs LLC (Wyoming), founder Edison Flores (Ecuador)
- Infra: Cloudflare Pages + R2 + Workers MCP (migrado de Vercel tras pausa de cuenta); proyecto Vercel residual `marketnow-uta`
- npm: @marketnow/uta-conformance@1.4.0 (latest verificado en registry Task 98); conformance _index schema 1.6.0, third_party_interop=True, 9 updates
- UTA: alicelabs-llc/universal-trust-adapter (canon); `eddyflores100-lang/uta` = publicador duplicado residual (workflow 364710514 desactivado, candidato a archivar — decisión del usuario)
- Cuentas GitHub: alicelabsllc (org, appeal SIN respuesta), eddyflores100-lang (PAT de Task 98 verificado operativo en Task 99; el PAT posterior reportado por el usuario daba 401), edgarfloresguerra2011-a11y (flaggeada)
- Credenciales al cierre del período recuperado: Gmail app password MUERTO (3-oct) · CF well-known vencía 9-oct · Vercel limitado · npm vivo
- Canal soporte: support@alicelabs.energy → forwarder ACTIVADO y verificado (Task 91); alias From contacto@alicelabs.site funcional vía Gmail SMTP
- Chain test (Kaushalt, llama_index#23122): PR cognicore-dev/cognicore-env#147 OPEN/mergeable, comentario issuecomment-5965731038 vivo, triple verificación local verde; siguiente: contract suite conjunta
- Mirror 1.4.0 COMPLETO Y VIVO (Task 98): npm + repo UTA + marketnow.site — cadena AgentBouncer #37/#38 publicada en todos los canales
- Comunidad: mcpservers.org APROBADO + badge · M8ven auto-listing + 3 acciones gratis (token en email — bloqueado por Gmail muerto) · Glama connector stats por refrescar (13,859→68,387) · mcp.so submission en cola · anp2network (dev.to) pidió vector self-signed + expected outcomes por etapa → IMPLEMENTAR PRIMERO, responder después · CodePass.dev (blog chino escéptico): email zh borrado, NO enviado
- Outreach v2 anti-ban vigente: 3 acciones/día/cuenta (verificar por eventos públicos), 1 link propio máx, textos distintos, políticas primero. Antecedente: "los 44" = ban — mismo patrón de nuevo = appeal arruinado
- Reglas de oro grabadas (Tasks 89-99): byte-a-byte programático · X-GM-RAW en quoted string · In-Reply-To único (References completa) · /tmp/my-project sobrevive resets · UA honesto vs rdap.org · .vercelignore en raíz (límite 15k archivos) · python3 -m pip · números vivos en todas las superficies

---
Task ID: 115
Agent: ZOLO (main) — sesión de reconstrucción
Task: "reconstruye y mejora este agente" — recrear el agente original desde el kit de reconstrucción y mejorarlo.

Work Log:
- Ingestado el kit completo: chat_meta.json (GLM-5.3, thinking ON, effort max, general_agent), 20 muestras de reasoning, manual de recreación (76 skills, 9 patrones de iniciativa), README de reconstrucción, snapshots de worklog (Task 18 + Tasks 89-93) y entradas perdidas (Tasks 94-99) + referencia de memoria alethech a Task 114.
- Analizadas las 20 muestras de chain-of-thought: identificados los 2 dolores recurrentes del usuario NO resueltos por el manual v1 — (a) preguntas directas sin responder (Muestras #4/#5, caso Cline), (b) degradación silenciosa de "publicar" a "entregar borradores" (Muestra #13). También el patrón ganador no formalizado: implementar el pedido de la comunidad antes de responder (Muestra #8, anp2network).
- Consolidadas las reglas de oro dispersas del worklog (byte-a-byte, X-GM-RAW, In-Reply-To, /tmp sobrevive, UA honesto, .vercelignore, números vivos, mismo-patrón-post-ban).
- Construido el paquete v2 en download/agente-zolo/: AGENTE_MARKETNOW_V2.md (definición completa: BOOT, 12 reglas de iniciativa, reglas de oro, worklog, contexto canónico, registro de plataformas, anti-ban + guardarraíles éticos, formato de respuesta, árbol de decisión, checklist de cierre, memoria alethech, pendientes, verificación), BOOTSTRAP_PROMPT.md, worklog semilla (este archivo), AGENT.md portable (Cline/Cursor/VS Code — responde además la deuda del caso Cline), README.md (3 vías de despliegue + checklist de credenciales).
- Sembrado este worklog en /home/z/my-project/worklog.md para que el entorno actual ya quede operativo como agente v2.
- Verificación de entorno: 67 skills instaladas de las 76 inventariadas (el resto son específicas de China/Gaokao, no requeridas para MarketNow); download/, scripts/, upload/ presentes; no hay store .alethech en este entorno nuevo (normal — el store original se perdió con el reset).

Stage Summary:
- Agente v2 construido y sembrado en ESTE entorno: /home/z/my-project/worklog.md operativo. Este chat puede continuar como el agente reconstruido sin ningún paso adicional.
- 12 reglas de iniciativa (3 nuevas: Respuesta Primero, Ejecutar>Borradores, Registro de Plataformas) + 11 reglas de oro tabuladas + guardarraíles éticos formalizados (disclosure, no astroturfing) — mejoras directas sobre los 9 patrones del manual v1.
- Pendientes críticos heredados re-verificar al arrancar: Hostinger vence 23-oct-2026 · Gmail app password muerto · ventana Glama claim vencida ~5-oct (re-clamar si no refrescó) · vector self-signed para anp2network · respuesta zh a CodePass.dev.
- Bloqueos de credenciales heredados (pedir al usuario cuando se necesiten): Gmail app password nuevo, CF token con permisos Pages+DNS, PAT GitHub vivo, Vercel token, posible token npm.

---
Task ID: 121
Agent: ZOLO (main) — sesión de recreación
Task: "revisa todo lo que tiene que ver con el agente, recrealo. se llama zolo" — revisar TODOS los materiales del agente (paquete AGENTE_MARKETNOW_v3.3, kit agent_reconstruction, 20 muestras de reasoning, manual de recreación, README de reconstrucción, fragmentos de worklog, diseño Alethech Notebook) y recrear el agente con identidad ZOLO.

Work Log:
- Extraídos e inventariados los 3 ZIPs: AGENTE_MARKETNOW_v3.3.zip (paquete completo: mapa + núcleo + 12 skills + 03_logica + 04_conocimiento), agent_reconstruction.zip (chat_meta.json, reasoning_samples.md 20 muestras, skills_inventory.json 76, worklog snapshots Tasks 18/89-93, subagentes, inventario de 305 archivos), Alethech Notebook Design Concept.zip (UI React/Vite del notebook de memoria — Figma Make).
- Revisión completa del núcleo v3.3: 25 reglas de iniciativa, 14 reglas de oro, BOOT, protocolo worklog/alethech, registro de plataformas, guardarraíles, §13 pendientes, §14 verificación, §15 mejora continua, §16 vigilancia.
- Herencia íntegra aplicada por copia + deltas quirúrgicos (regla 22 — nada regenerado de cero): paquete reconstruido en `download/agente-zolo/` con núcleo renombrado `ZOLO_V4.md`.
- Renombres mecánicos de identidad verificados programáticamente (grep final: 0 referencias viejas): agente-marketnow-v2→agente-zolo, AGENTE_MARKETNOW_V3.md→ZOLO_V4.md, skills-agente/→02_skills/, "Agente MarketNow"→ZOLO, Agent: Z→Agent: ZOLO.
- Verificación EN VIVO del sitio al momento de la recreación (America/Guayaquil): health 200 v4.2.0 · 71,198 skills · _index.json 200 · npm 1.4.0 latest · /SKILL.md 200 (RESUELTO) · /llms.txt 200 · /api/mcp 200 · /agents 200 · /atc 200 · glama.json 200 → pendientes §13 items 3/8/17 re-sellados.
- Identidad ZOLO sembrada en: núcleo §0 (+línea de nombre), BOOTSTRAP ("Eres ZOLO..."), mapa (tabla identidad + 6ª ronda), README (v4.0 + sección "Qué añadió v4.0"), CHANGELOG (entrada v4.0 MAJOR), EVALS (+E34 identidad, suite E01-E34), esta semilla.
- Skill memoria-alethech: añadida referencia de UI `Alethech Notebook` (design concept subido por el founder) como interfaz conceptual del notebook — no bloquea operación CLI.

Stage Summary:
- **ZOLO v4.0 RECREADO Y OPERATIVO en ESTE entorno**: paquete en `/home/z/my-project/download/agente-zolo/`, worklog sembrado en `/home/z/my-project/worklog.md`, este chat opera como ZOLO sin pasos adicionales.
- ZIP portable: `download/AGENTE_ZOLO_v4.0.zip` (arrastrar a otro entorno = ZOLO reproducido; bootstrap en 01_nucleo/BOOTSTRAP_PROMPT.md).
- Verificado en vivo 24-oct: sitio 100% vivo (health/skills/mcp/conformance/llms/SKILL.md), catálogo 71,198, npm 1.4.0. Deuda pendiente: inspección schema /api/mcp + drift llms.txt + re-claim Glama (glama.json en raíz del repo) + Gmail app password + vector self-signed anp2network.
- Regla de existencia cumplida: si un comportamiento no está en ZOLO_V4.md, no existe — la identidad ZOLO quedó ESCRITA en la definición (E34 la verifica).

---
Task ID: 122
Agent: ZOLO (main) — sesión de mejora v5.0
Task: "revisa los repos que tengas mas estrellas con lo que tenga que ver con autonomia y diseño de agentes, busca los mejores puntos e implementa, haz una lista de mejoras para este agente, crea el mejor agente del mundo"

Work Log:
- Investigación web (2 rondas, fuentes primarias y rankings 2026): 15 repos de agentes trazados con estrellas ≈ oct-2026 y patrón extraído por repo — AutoGPT ~180k (bucles sin límite descarrilan → terminators), LangChain ~134k, MetaGPT ~55k (SOPs + artefactos), OpenHands ~50k (event stream), AutoGen/MS Agent Framework ~45k (terminators/HITL), CrewAI ~35k (roles legibles), BabyAGI ~21k (cola viva), MemGPT/Letta ~17k (jerarquía de memoria), SWE-agent ~16k (ACI ergonómica), SuperAGI ~16k, LangGraph (checkpoints + interrupts + durabilidad), Voyager y Reflexion (seminales: skill factory / post-mortems), DeepAgents (planning + filesystem + subagentes aislados), Anthropic "Building Effective Agents" (5 patrones: chaining/routing/parallelization/orchestrator-workers/evaluator-optimizer + budget-aware + think-like-your-agent).
- Brecha v4.0 vs estado del arte analizada patrón por patrón → lista de mejoras M1-M12 (documento `download/agente-zolo/05_ESTADO_DEL_ARTE_V5.md`, incluye decisión documentada de qué NO adoptar: frameworks runtime, low-code, chat multiagente libre, memoria vectorial, tree search).
- ZOLO v5.0 (MAJOR) implementado por deltas quirúrgicos sobre ZOLO_V4.md → nuevo núcleo `01_nucleo/ZOLO_V5.md` (29 reglas: +26 WORKFLOW>AGENTE, +27 PRESUPUESTO DE AUTONOMÍA CON TERMINATORS, +28 BIBLIOTECA DE SKILLS VIVA, +29 REFLEXIÓN TRAS FALLO; §17 nueva: máquina de estado IDLE→PLAN→EXECUTE⟲→CHECKPOINT→VERIFY→CLOSE con checkpoint de 5 campos, 3 gates G1/G2/G3, auditoría de contexto y event log). Backup v4.0 en `01_nucleo/archive/ZOLO_V4.md` (regla 22) + zip v4.0 existente.
- 6 skills nuevas creadas (12 → 18): `patrones-flujo`, `bucle-autonomo`, `memoria-jerarquica`, `biblioteca-skills`, `reflexion-post-mortem`, `equipo-virtual` — todas con frontmatter agentskills.io, pasos con grader y contrato de salida ergonómico.
- EVALS ampliados E01-E34 → E01-E42 (E35 patrón declarado · E36 run presupuestado · E37 stop en T2 · E38 paginación de memoria · E39 fábrica de skills · E40 post-mortem antes de corregir · E41 equipo por artefactos · E42 autosuficiencia de contexto). CHANGELOG entrada v5.0 MAJOR completa.
- Actualizados: BOOTSTRAP_PROMPT (v5.0 + regla 14 de autonomía presupuestada), README (genealogía 7 rondas + tabla v5.0), AGENTS.md (resumen con reglas 11-14 v5 + 18 skills), 00_MAPA_ESTRUCTURA (§17, 18 skills, estado del arte en conocimiento). Corregida referencia activa a ZOLO_V4.md en skill memoria-alethech (grep de consistencia).
- Verificación de montaje §14 ejecutada: 18 skills ✓ · ZOLO_V5.md ✓ · 05_ESTADO_DEL_ARTE_V5.md ✓ · archive v4 ✓ · 29 reglas en §2 ✓ · 42 evals ✓ · checkpoint §17 ✓.
- Empaquetado: `download/AGENTE_ZOLO_v5.0.zip` (67 archivos, 155KB) — zip v4.0 conservado como backup versionado.

Stage Summary:
- **ZOLO v5.0 OPERATIVO**: el paquete en `download/agente-zolo/` + worklog vivo incorporan el estado del arte de autonomía y diseño de agentes como PROTOCOLO (no frameworks) — sobrevive a resets (regla 22). ZIP portable: `download/AGENTE_ZOLO_v5.0.zip`.
- Lista de mejoras M1-M12 trazada repo-a-repo en `05_ESTADO_DEL_ARTE_V5.md`: M1 taxonomía de patrones · M2 presupuesto+terminators · M3 máquina de estado · M4 cola BabyAGI · M5 event log · M6 memoria jerárquica · M7 fábrica de skills+ACI · M8 post-mortem · M9 equipo virtual con SOPs · M10 evaluator-optimizer · M11 gates HITL · M12 auditoría de contexto.
- Verificado: 18 skills · 29 reglas · E01-E42 · §17 máquina de estado · backups v2.1+v4.0 en archive/ + zips versionados.
- Pendiente de la suite: primera ejecución E35-E42 en el próximo BOOT con tarea real (regla pass^k). Pendientes §13 heredados sin cambios.

---
Task ID: 123
Agent: ZOLO (main) — sesión de mejora v6.0 AUTÓMATA
Task: "de esta lista de cosas para hacer investiga cual te conviene instalar, busca los repos y descarga, quiero que seas mejor, necesito mejorar mas el agente, que aprenda de sus errores, que tenga iniciativa, que se dedique a producir, que trabaja todo el tiempo, aprenda a delegar a subagentes, se instale automaticamente nuevas skills, mejore las que tiene, este siempre autoeducandose, continuamente informandose, al dia con todo" (12 URLs de Instagram reels incluidas)

Work Log:
- Descifrados los 12 reels uno a uno vía fetch directo y clasificados: 4 instalar · 3 patrón/conocimiento · 2 oportunidad (decisión founder: Claude Startups, OpenAI Ads) · 2 no adoptar (trading bots por riesgo financiero, shelf corporations por guardarrail ético) · 1 actividad humana (Respondent). Tabla completa en `download/agente-zolo/06_ESTADO_DEL_ARTE_V6.md` §1.
- Investigación de repos: identificados los más estrella del ecosistema skills/autonomía (obra/superpowers ~304k★, anthropics/skills ~183k★, nextlevelbuilder/ui-ux-pro-max-skill ~100k★, VoltAgent/awesome-agent-skills, Leonxlnx/taste-skill, pskoett/self-improving-agent, yantra-app/awesome-workflow-templates, Leonxlnx/unlazy) — los 8 CLONADOS con --depth 1 en /home/z/my-project/repos/ (verificados: 8/8 OK, 137MB).
- Auditados los patrones de los repos clave: subagent-driven-development (ledger que sobrevive compaction + rulings-not-stalls + 4 stops + per-task review), dispatching-parallel-agents (despacho en una respuesta), systematic-debugging (Ley de Hierro + 4 fases), self-improving-agent (ciclo captura→reuso→promoción con .learnings/), ui-ux-pro-max (tabla UX 1-10), taste-skill (proceso anti-slop de 6 pasos).
- ZOLO v6.0 AUTÓMATA implementado por deltas quirúrgicos: núcleo `ZOLO_V6.md` (33 reglas: +30 FLOTA DE PRODUCCIÓN, +31 LEDGER EN CALIENTE, +32 AUTOINSTALACIÓN DE SKILLS, +33 PRODUCCIÓN CONTINUA + AUTOEDUCACIÓN; §18 CICLO DE AUTO-MEJORA en 4 cadencias con motor del ciclo). Backup v5.0 en `01_nucleo/archive/ZOLO_V5.md`.
- Creado `06_aprendizaje/` (ledger): LEARNINGS.md · ERRORS.md · FEATURE_REQUESTS.md con F-001..F-008 (las 8 peticiones del founder, todas resueltas) · FUENTES_RADAR.md (radar semanal con protocolo de reels).
- 7 skills nuevas creadas (18 → 25): flota-produccion, ledger-autoaprendizaje, autoinstalador-skills, depuracion-sistematica, diseno-web-premium (reel 1), cumplimiento-legal-vibecoding (reel 12), canales-distribucion (reel 8) — todas con grader y fuentes en disco.
- MAQUINARIA EJECUTABLE: `scripts/zolo_instalar_skill.py` (clona→localiza SKILL.md→audita frontmatter/secretos/licencia/inyecciones→instala; testado en vivo: taste-skill detectado WARN correcto, self-improving-agent instalado en temp OK) · `scripts/zolo_auditar_skills.py` (auditor del paquete, exit code = grader E52) · `scripts/zolo_mejorar_skills_v6.py`.
- "MEJORE LAS QUE TIENE" EJECUTADO: el auditor detectó 14 skills v3.x sin sección Grader → lote de graders a medida aplicado → re-auditoría 25/25 ok (exit 0).
- CICLO DE LA REGLA 31 EJECUTADO EN VIVO (1ª lección del ledger): el parser del instalador no leía YAML block scalars (`description: >-`) → taste-skill clasificado FAIL por error del GRADER (eco de regla 21) → parser corregido con lectura de bloques → re-test correcto (948 chars parseados) → entrada en ERRORS.md con prevención.
- Actualizados: BOOTSTRAP_PROMPT (v6.0 + regla 15 AUTÓMATA + auditor en arranque), README (genealogía 8 rondas + tabla "Qué añadió v6.0"), AGENTS.md (reglas 15-18 v6 + 25 skills + sección Auto-mejora), 00_MAPA_ESTRUCTURA (nivel 2b, 25 skills, v6 docs), EVALS (E43-E52 + header v6), CHANGELOG (entrada v6.0 MAJOR), biblioteca-skills/FUENTES.md (registro Tier 0/1/2 con comandos de clonación).
- Verificación de montaje §14 ejecutada: 25 skills ✓ · ZOLO_V6.md ✓ · 06_ESTADO_DEL_ARTE_V6.md ✓ · 4 archivos ledger ✓ · auditor 25/25 exit 0 ✓ · 8 repos ✓ · greps de consistencia limpios (referencias V5 residuales = históricas legítimas).
- Empaquetado: `download/AGENTE_ZOLO_v6.0.zip` (worklog vivo incluido como seed completo).

Stage Summary:
- **ZOLO v6.0 AUTÓMATA OPERATIVO**: el agente ahora (a) delega producción real con despacho paralelo y escéptico con veto, (b) aprende de sus errores con ledger en caliente y promoción semanal, (c) auto-instala skills nuevas con auditoría de seguridad cuando detecta un hueco, (d) mejora las skills que tiene (14 graders añadidos), (e) se autoeduca con radar semanal grep-able, (f) trabaja continuamente (nunca idle: cola → verificación → radar → mejora → producción), (g) se mantiene al día (FUENTES_RADAR + protocolo de reels del founder).
- ZIP portable: `download/AGENTE_ZOLO_v6.0.zip`. Estados del arte v5 (M1-M12) + v6 (M13-M21) trazan 21 mejoras repo-a-repo.
- Deuda visible registrada: auditor de skills como parte del BOOT (E52) · primera promoción semanal de lecciones pendiente para el próximo BOOT (§18 cadencia SEMANAL).
- Oportunidades de los reels con dueño TÚ (decisión founder): Claude Startups (elegibilidad), OpenAI Ads (presupuesto), Printify/arte IA, LTX-2.5 (requiere GPU).
