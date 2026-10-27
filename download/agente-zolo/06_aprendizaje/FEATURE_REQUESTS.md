# Feature Requests — ZOLO

Capacidades pedidas por el founder o detectadas por el agente (regla 31, v6.0). Estado: pendiente | en_curso | resuelto (versión). Esta sección ES el contrato de mejora continua con el founder — cada pedido entra, ninguno se pierde.

---

### F-001 — aprender de sus errores — 24-oct-2026
- PEDIDO: "que aprenda de sus errores" (founder, carta v6.0)
- ESTADO: **resuelto (v6.0)** — regla 29 (post-mortem) + regla 31 (ledger en caliente) + skills `reflexion-post-mortem` + `ledger-autoaprendizaje` + `depuracion-sistematica`

### F-002 — iniciativa — 24-oct-2026
- PEDIDO: "que tenga iniciativa"
- ESTADO: **resuelto (heredado)** — reglas 1-25 (v2-v5) + regla 33 v6.0 (sin tarea → cola → autoeducación → producción)

### F-003 — dedicarse a producir — 24-oct-2026
- PEDIDO: "que se dedique a producir"
- ESTADO: **resuelto (v6.0)** — regla 30 (flota de producción) + skill `flota-produccion` + regla 33 (producción continua)

### F-004 — trabajar todo el tiempo — 24-oct-2026
- PEDIDO: "que trabaje todo el tiempo"
- ESTADO: **resuelto (v6.0)** — regla 33 (nunca idle: cola §13 → verificación → autoeducación → mejora de skills) + `bucle-autonomo` (runs presupuestados) + heartbeat

### F-005 — aprender a delegar a subagentes — 24-oct-2026
- PEDIDO: "que aprenda a delegar a subagentes"
- ESTADO: **resuelto (v6.0)** — regla 30 + skill `flota-produccion` (despacho paralelo en un mensaje, brief exacto, revisión por artefacto, rulings-not-stalls) + escéptico con veto

### F-006 — autoinstalación de skills nuevas — 24-oct-2026
- PEDIDO: "que se instale automáticamente nuevas skills"
- ESTADO: **resuelto (v6.0)** — regla 32 + skill `autoinstalador-skills` + script `scripts/zolo_instalar_skill.py` + registro FUENTES.md

### F-007 — mejorar las skills que tiene — 24-oct-2026
- PEDIDO: "mejore las que tiene"
- ESTADO: **resuelto (v6.0)** — skill `autoinstalador-skills` §2 (re-clonar fuente, extraer delta, editar por deltas) + regla 28 (poda) + mantenimiento-mensual

### F-008 — autoeducación continua y siempre al día — 24-oct-2026
- PEDIDO: "que esté siempre autoeducándose, continuamente informándose, al día con todo"
- ESTADO: **resuelto (v6.0)** — regla 33 + `06_aprendizaje/FUENTES_RADAR.md` (radar semanal: HN, GitHub trending, awesome lists, contenido del founder) + §16 vigilancia + hueco_conocimiento → misión con fecha

### F-009 — noticiero matutino con avatar y humor adaptativo — 24-oct-2026
- PEDIDO: "complemento para GPT o cualquier IA que lea las noticias más frescas al despertar, que envíe al correo o recordatorio a FB/IG/TikTok, que cree los videos de las noticias más importantes del día, que scrapee la red; que se despierte a la hora programada; un avatar que lea las noticias como un noticiero; reportes del clima, cosas curiosas y cómicas dependiendo del humor del usuario" (founder, Task 125)
- ESTADO: **resuelto (Task 125, maquinaria viva)** — `zolo-news/` (núcleo RSS+clima+curiosidades+guion LLM, medios TTS+avatar+MP4, entrega email/Telegram/WhatsApp + stubs sociales, MCP de 4 tools) + skill `noticiero-matutino` + `docs/INTEGRACION-GPT.md` + `docs/CANALES.md`. Pendiente de credenciales del founder: SMTP, bot Telegram, CallMeBot, tokens Meta/TikTok.
