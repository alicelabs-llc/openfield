# Learnings — ZOLO

Correcciones, insights, huecos de conocimiento y mejores prácticas capturados EN CALIENTE durante la operación (regla 31, v6.0 — patrón self-improving-agent).

**Categorías**: corrección | insight | hueco_conocimiento | mejor_práctica
**Formato**: entrada de 5 campos (CONTEXTO / PASÓ / LECCIÓN / CATEGORÍA / PROMOCIÓN) — ver skill `ledger-autoaprendizaje` §2. Solo append; las correcciones SUPERSEDEN (regla 24).

---

### api-imagenes-devuelve-jpeg — 25-oct-2026 (Task 125-B)
- CONTEXTO: pipeline de medios de ZOLO NEWS (generación de imágenes para el noticiero)
- PASÓ: la API de generación devuelve JPEG (JFIF) aunque el contrato del skill diga PNG
- LECCIÓN: verificar la FIRMA del archivo (magic bytes) antes de consumir cualquier binario generado por una API
- CATEGORÍA: corrección
- PROMOCIÓN: normalización automática por firma implementada en src/media/images.js (ffmpeg) + regla de oro §6.5 de skill noticiero-matutino + eval E54

### ffmpeg-concat-imagenes-duraciones — 25-oct-2026 (Task 125-B)
- CONTEXTO: ensamblado del MP4 del noticiero con concat demuxer
- PASÓ: la "última imagen repetida" hereda la última duration y estira el timeline; -r 30 como opción de salida duplica la primera slide; -shortest es inestable (77s vs 21s entre corridas)
- LECCIÓN: en concat de imágenes fijar fps como filtro de video (-vf fps=30) y capar con -t <duración_audio+0.05> — el resultado queda clavado al audio (Δ verificado 0.05s)
- CATEGORÍA: corrección
- PROMOCIÓN: implementado en src/media/video.js + regla de oro §6 de skill noticiero-matutino

### drawtext-solo-textfile — 25-oct-2026 (Task 125-B)
- CONTEXTO: captions en español (tildes, comas, comillas, %) sobre slides del noticiero
- PASÓ: texto inline en el filtro drawtext rompe con escapado de caracteres especiales
- LECCIÓN: drawtext SIEMPRE con textfile=<archivo temporal> + expansion=none — las tildes y comillas viajan seguras
- CATEGORÍA: mejor_práctica
- PROMOCIÓN: implementado en video.js + regla de oro §6.4 de skill noticiero-matutino

### fuentes-verificadas-antes-de-config — 25-oct-2026 (Task 125-A/integración)
- CONTEXTO: feeds RSS iniciales del noticiero (config.json)
- PASÓ: 3 de 5 feeds iniciales estaban muertos en vivo (Infobae 404, El Universo 404, El Comercio anti-bot) pese a ser feeds conocidos
- LECCIÓN: ninguna fuente (feed/API) entra a config sin verificación EN VIVO (código HTTP + contenido parseable); el sistema además debe saltar feeds caídos sin tumbar el run
- CATEGORÍA: mejor_práctica
- PROMOCIÓN: regla de oro §6.2 de skill noticiero-matutino + eval E55 + config.json reemplazada por 5 feeds verificados (Google News EC/Tec, BBC Mundo, France24 es, eJu.tv)

### radar-anthropic-dreaming-pattern — 25-oct-2026 (Task 125 — radar semanal)
- CONTEXTO: ciclo §18 auto-mejora, sesión de radar (FUENTES_RADAR)
- PASÓ: detectado patrón "dreaming" de Anthropic (May 2026) — agente revisa sesiones pasadas, extrae patrones, escribe playbooks. Harvey reportó 6x task completion rate. Es EXACTAMENTE lo que hace §18 pero sin sesión dedicada de consolidación.
- LECCIÓN: el ciclo §18 necesita una sesión dedicada que CONSOLIDE patrones cross-sesión (no solo capturar en caliente como hace regla 31). Sin consolidación, los learnings se acumulan pero no se promueven.
- CATEGORÍA: insight
- PROMOCIÓN: skill nueva `sueno-consolidacion` creada (27 skills total, auditor 27/27 verde). Cadencia SEMANAL §18 ahora incluye sesión de sueño. Eval E56 propuesto (verificar playbook output).

### patron-verificar-en-vivo-antes-de-usar — 25-oct-2026 (Task 125 — consolidación)
- CONTEXTO: sesión de sueño-consolidación (primera ejecución)
- PASÓ: patrón repetido 3 veces en el ledger: (1) api-imagenes-devuelve-jpeg → verificar magic bytes, (2) fuentes-verificadas-antes-de-config → verificar HTTP + parseable, (3) Task 124 drift /api/mcp 200→400 → verificar estado actual no stale. Los 3 casos comparten la misma heurística: NUNCA confiar en caché/asunción, SIEMPRE verificar en vivo antes de consumir.
- LECCIÓN: patrón cross-sesión detectado → merece ser regla del núcleo. "Verificar en vivo antes de usar" ya está implícito en regla 5 (estado ACTUAL) y regla 6 (stale vs real), pero la heurística específica para ARCHIVOS y FUENTES EXTERNAS no estaba formalizada.
- CATEGORÍA: insight (patrón cross-sesión)
- PROMOCIÓN: regla nueva propuesta para ZOLO_V7.md — regla 34: "VERIFICAR EN VIVO ANTES DE USAR: cualquier archivo binario, feed, API o dato externo se verifica en vivo (magic bytes / HTTP code / parseable) ANTES de consumirlo. Asumir que un caché es válido = FAIL. Eco de reglas 5 y 6, pero aplicado a consumibles externos." Pendiente gate G1 del founder.

### comparativa-12-repos-zolo-rank1-en-3-dimensiones — 25-oct-2026 (Task 129)
- CONTEXTO: founder pidió "busca otros agentes, busca repos y comparate" — cloné 12 repos top (LangGraph 37k★, CrewAI 35k★, OpenAI Agents SDK, Google ADK, Mastra, Letta 17k★, mem0, Hermes 257k★, ECC 288k★, Obra 304k★, Anthropic Skills 184k★, Awesome-Agent-Memory) y auditoría completa via subagente
- PASÓ: ZOLO v7.0 es #1 mundial en 3 dimensiones: (1) memoria criptográfica (único con Ed25519), (2) self-improvement más completo (5 mecanismos, nadie combina más de 2), (3) PreCompact hook crítico (único que documenta el failure mode). Pero #12 (último) en distribución/runtime y #8 en memoria retrieval (sin vector DB ni benchmarks).
- LECCIÓN: ZOLO es el protocolo más completo conceptualmente pero el menos distribuido prácticamente. El gap no es de calidad sino de runtime — sin código ejecutable, sin PyPI/npm, sin marketplace. El movimiento de mayor leverage: ship 1 script runnable + correr evals + publicar benchmarks.
- CATEGORÍA: insight
- PROMOCIÓN: reporte completo en 08_COMPARATIVA_12_REPOS.md. Gaps para cerrar en v7.1: (M28) memory benchmarks, (M26) vector retrieval, (M29) skill count growth, (M30) marketplace presence.
