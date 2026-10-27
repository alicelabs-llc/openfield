# ESTADO DEL ARTE v5.0 — Repos de agentes más estrella → lista de mejoras de ZOLO

> **Origen** (Task 122, 24-oct-2026): "revisa los repos que tengas mas estrellas con lo que tenga que ver con autonomia y diseño de agentes, busca los mejores puntos e implementa, haz una lista de mejoras para este agente, crea el mejor agente del mundo".
> Este documento ES la lista de mejoras: (1) qué repos dominan el diseño de agentes, (2) qué patrón se extrae de cada uno, (3) la brecha contra ZOLO v4.0, (4) cómo se implementa cada mejora (regla/skill/árbol). Nada se adopta por moda: solo patrones que sobreviven a un reset del entorno (regla 22) y caben en protocolo markdown.

---

## 1. Los repos de referencia (autonomía y diseño de agentes, oct-2026)

| Repo | Estrellas ≈ | Qué demostró | Patrón extraído |
|---|---|---|---|
| `Significant-Gravitas/AutoGPT` | ~180k | El primer bucle autónomo masivo (percibir→planear→actuar) y su plataforma de bloques | Lección central: **bucles sin límite descarrilan** — la plataforma maduró hacia workflows con terminators, presupuestos y pasos verificables |
| `langchain-ai/langchain` | ~134k | Componentes componibles (prompts, memoria, tools) como capa estándar | Composición de piezas pequeñas > monolitos; ya adoptado (arquitectura 2 niveles) |
| `langchain-ai/langgraph` | ~20k (runtime de producción de LangChain) | Grafo de **estado tipado + checkpoints + durabilidad + interrupts** (HITL) | Máquina de estado persistente: pausar, guardar, reanudar EXACTO; aprobación humana en nodos definidos |
| `FoundationAgents/MetaGPT` | ~55k | SOPs codificados en una "empresa virtual" (PRD→diseño→código) | Roles con **SOP explícito** y handoff de ARTEFACTOS estructurados, no conversación libre |
| `All-Hands-AI/OpenHands` | ~50k | Event stream: toda acción/observación es un evento estructurado rejugable | **Log de eventos** de sesión: una línea por acción con evidencia → replay y auditoría |
| `microsoft/autogen` → MS Agent Framework | ~45k | Conversación multiagente event-driven; condiciones de terminación explícitas; UserProxy como HITL | **Terminators y gates explícitos** en cualquier interacción multiagente |
| `crewAIInc/crewAI` | ~35k | Roles legibles (rol/meta/backstory) + delegación secuencial/jerárquica | Roles en lenguaje humano = iteración doble de velocidad; delegación con salida esperada |
| `yoheinakajima/babyagi` | ~21k | Cola de tareas viva: crear → priorizar → ejecutar → re-priorizar | **Backlog como bucle**, no lista estática |
| `princeton-nlp/SWE-agent` | ~16k | ACI (Agent-Computer Interface): la interfaz se DISEÑA para el agente | **Contrato de salida ergonómico**: outputs compactos, grep-ables, con linter de feedback |
| `TransformerOptimus/SuperAGI` | ~16k | Guardarraíles de ejecución + telemetría de cada run | (Ya v4.0 §7) + telemetría de presupuesto por run |
| `letta-ai/letta` (MemGPT) | ~17k | Jerarquía de memoria: contexto principal ↔ almacenamiento externo, **memoria auto-editable** | Paginación de contexto: lo frío sale a archivos; el agente EDITA su propia memoria de trabajo |
| `joaopn/voyager`-style (Voyager, seminal) | seminal (NeurIPS 2023) | **Biblioteca de skills auto-expandible**: cada experiencia exitosa se convierte en skill reusable | Fábrica de skills con criterio de incorporación y poda |
| `noahshinn/reflexion` (seminal) | seminal | Auto-reflexión verbal persistida tras fallo → memoria episódica de lecciones | **Post-mortem obligatorio** antes de corregir; la lección se reutiliza |
| LangChain **Deep Agents** (2026) | oficial | planning tool + filesystem como memoria + subagentes con contexto aislado + HITL | Valida lo ya adoptado (PLAN.md, subagentes-contrato) y añade offload sistemático a archivos |
| Anthropic **"Building Effective Agents"** | referencia de ingeniería | Workflows vs agents; 5 patrones: **chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer**; simplicidad; budget-aware; "think like your agent" | Taxonomía de decisión: elegir el patrón MÁS SIMPLE que resuelve la tarea |

Lectura cruzada (LangChain blog "Building LangGraph", sep-2025; Anthropic "Building Effective Agents", dic-2024 + talk 2026; JetBrains framework comparison 2026; Taskade/Medium rankings 2026): el consenso de producción converge en 4 ideas — (1) **control explícito del flujo** por encima de autonomía improvisada, (2) **durabilidad** (checkpoints, reanudación, HITL), (3) **presupuestos** (latencia/coste/acciones medidos, no supuestos), (4) **aprendizaje persistente** (memoria jerárquica + skills que crecen).

---

## 2. Brecha: ZOLO v4.0 vs estado del arte

| # | Patrón de los repos | v4.0 tenía | Brecha |
|---|---|---|---|
| M1 | Taxonomía de 5 patrones de flujo + criterio workflow>agente (Anthropic) | best-of-n (evaluator-optimizer parcial) y subagentes (orchestrator-workers parcial), pero sin taxonomía ni criterio de elección | **SÍ** — improvisaba la forma de ejecutar cada tarea |
| M2 | Presupuesto de autonomía + terminators (AutoGPT, budget-aware) | grind loop de 5 iteraciones (regla 18) y presupuesto de atención (regla 22) | **PARCIAL** — faltaba presupuesto explícito de acciones/tiempo y stops formales por run |
| M3 | Máquina de estado con checkpoints reanudables (LangGraph) | PLAN.md persistido con criterios de salida | **PARCIAL** — plan sin estados tipados ni checkpoints de reanudación |
| M4 | Cola de tareas viva (BabyAGI) | §13 pendientes canónicos (estático) | **SÍ** — no había bucle de re-priorización al iniciar run autónomo |
| M5 | Event log de sesión (OpenHands) | worklog narrativo post-hoc | **SÍ** — sin registro en vivo por acción en tareas largas |
| M6 | Jerarquía de memoria (MemGPT/Letta) | worklog + alethech (largo plazo, excelente) + presupuesto de atención | **SÍ** — faltaba la capa de memoria DE TRABAJO: compactación y offload a archivos de sesión |
| M7 | Fábrica de skills (Voyager) + ACI ergonómica (SWE-agent) | §15 crea REGLAS nuevas por fricción; skills fijas en 12 | **SÍ** — un éxito repetido no se convertía automáticamente en skill reusable |
| M8 | Reflexión post-fallo persistida (Reflexion) | reglas de oro nacen de costes reales (reactivo, informal) | **SÍ** — no había protocolo post-mortem OBLIGATORIO antes de corregir |
| M9 | Equipo virtual con SOPs por rol (CrewAI/MetaGPT) | subagentes-contrato (brief de 6 líneas) | **SÍ** — sin roles fijos con SOPs para pipelines recurrentes |
| M10 | Evaluator-optimizer explícito para lo reversible (Anthropic) | best-of-n solo para lo irreversible | **SÍ** — falta loop generar→criticar→revisar barato |
| M11 | Gates HITL definidos en el flujo (LangGraph interrupts, AutoGen) | §9 decide preguntar vs actuar (reactivo) | **PARCIAL** — sin gates ANTES declarados en el plan |
| M12 | Auditoría de contexto "think like your agent" (Anthropic) | regla 22 (presupuesto de atención) | **SÍ** — sin checklist de coherencia de contexto al activar skills |

---

## 3. Lista de mejoras implementadas en v5.0 (M1→M12)

| Mejora | Implementación | Dónde quedó |
|---|---|---|
| **M1** Taxonomía de patrones de flujo | Regla 26 WORKFLOW > AGENTE + skill `patrones-flujo` (los 5 patrones con árbol de elección + criterio de salida) | Núcleo §2.26 + `02_skills/patrones-flujo/` |
| **M2** Presupuesto de autonomía | Regla 27: presupuesto (acciones · tiempo · subagentes) + terminators ANTES de arrancar | Núcleo §2.27 + skill `bucle-autonomo` |
| **M3** Máquina de estado + checkpoints | §17 del núcleo: IDLE→PLAN→EXECUTE→CHECKPOINT→VERIFY→CLOSE + formato de checkpoint de 5 campos | Núcleo §17 + skill `bucle-autonomo` |
| **M4** Cola de tareas viva | Paso 0 del bucle autónomo: priorizar desde §13 (cola BabyAGI) cada vez que se abre un run | Skill `bucle-autonomo` §2 |
| **M5** Event log de sesión | Una línea por acción con evidencia dentro del PLAN.md (estilo OpenHands) | Skill `bucle-autonomo` §4 |
| **M6** Jerarquía de memoria de trabajo | 4 capas: contexto vivo → archivo de sesión (offload) → worklog → alethech; compactación con reglas explícitas | Skill `memoria-jerarquica` |
| **M7** Fábrica de skills + ACI | Regla 28: éxito 2+ veces (o 1 si fue caro) → skill nueva con contrato de salida ergonómico y grader; poda mensual | Núcleo §2.28 + skill `biblioteca-skills` |
| **M8** Post-mortem obligatorio | Regla 29: fallo verificado → 4 campos (esperaba/obtuve/causa raíz/lección) ANTES de corregir; lección → regla + eval + skill candidata | Núcleo §2.29 + skill `reflexion-post-mortem` |
| **M9** Equipo virtual con SOPs | 5 roles fijos (Orquestador, Investigador, Constructor, Auditor, Comercial) con SOP y handoff de artefactos | Skill `equipo-virtual` |
| **M10** Evaluator-optimizer barato | Patrón 5 de `patrones-flujo`: loop generar→criticar→revisar para lo reversible (≤2 iteraciones) | Skill `patrones-flujo` §5 |
| **M11** Gates HITL en el plan | 3 gates estándar (G1 irreversible · G2 presupuesto agotado · G3 divergencia 2x) declarados al abrir el plan | Núcleo §17.3 |
| **M12** Auditoría de contexto | Checklist de 4 preguntas al activar cada skill: ¿el cuerpo trae TODO lo que la ventana necesita? | Skill `patrones-flujo` §7 + núcleo §17.4 |

## 4. Qué NO se adoptó (y por qué)

1. **Frameworks runtime (LangGraph/AutoGen/CrewAI como librerías)** — ZOLO opera como protocolo markdown sobre GLM: adopta los PATRONES (estados, terminators, roles) sin dependencia de runtime; así sobrevive a resets (regla 22).
2. **Plataformas low-code (bloques de AutoGPT, GUIs)** — el valor para ZOLO es la lección de terminators/presupuestos, no la GUI.
3. **Multiagente conversacional libre (AutoGen chat infinito)** — se adopta la versión con SOPs y handoffs de artefactos (MetaGPT): la conversación libre quema contexto sin evidencia.
4. **Memoria vectorial externa** — el binomio worklog (narrativa) + alethech (integridad criptográfica) ya cubre el largo plazo con verificación; añadir vectores rompería la cadena de custodia sin ganar recall a esta escala.
5. **Tree search masivo (LATS/ToT)** — el coste de inferencia no justifica a esta escala; best-of-N de 3 (regla 20) cubre el mismo riesgo.

## 5. Cómo se verifica esta adopción

Nuevos escenarios de regresión **E35-E42** en `EVALS.md` (uno por patrón crítico: M1, M2/M3, M2-stop, M6, M7, M8, M9, M12). Criterio de éxito de la versión: la próxima tarea grande de ZOLO abre con (a) patrón declarado en 1 línea, (b) presupuesto explícito, (c) gates identificados, (d) checkpoints durante la ejecución — y cierra con post-mortem si hubo fallo + skill candidata si hubo éxito repetible.
