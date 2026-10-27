# Errors — ZOLO

Fallos de comando, integración y deploy con su corrección exacta (regla 31, v6.0). Regla de entrada: todo comando que falla deja aquí el error, la causa y el comando que funcionó. Solo append.

---

### parser-yaml-block-scalar — 24-oct-2026
- CONTEXTO: primer test del instalador `zolo_instalar_skill.py` contra `Leonxlnx/taste-skill` (regla 32, Task 123)
- PASÓ: SKILL.md válido clasificado FAIL por "description ausente" — el frontmatter usa YAML block scalar `description: >-` multi-línea y el parser solo leía `key: value` de una línea
- LECCIÓN: LECCIÓN: parsers de frontmatter deben manejar block scalars (`>-`, `>`, `|`, `|-`, `|+`) — un FAIL de auditoría puede ser un bug del GRADER, no de la skill auditada (eco de la regla 21: eval al 0% = eval roto)
- CORRECCIÓN: parser reescrito con lectura de bloques (zolo_instalar_skill.py); re-test: taste-skill ahora WARN correcto (948 chars de descripción)
- PREVENCIÓN: grader determinista instalado — el auditor `zolo_auditar_skills.py` se corre tras editar scripts de skills

### sandbox-403-caida-cierre — 25-oct-2026
- CONTEXTO: cierre del Task 125 (flota de subagentes + integración del noticiero)
- PASÓ: el sandbox devolvió 403 Forbidden en Bash/Write al CERRAR la sesión (golpeó también al subagente 125-C tras completar su trabajo); el append final del worklog quedó pendiente
- LECCIÓN: LECCIÓN: la caída del entorno puede llegar al cierre — lo único que se pierde es el registro, nunca el trabajo (todo estaba en disco); el append pendiente se ejecuta en el siguiente turno, no se rehace
- CORRECCIÓN: entrada Task 125 apendada al reabrir la sesión (Task 126)
- PREVENCIÓN: la cadencia DIARIA (§18) termina con verificación de que el worklog quedó apendado ANTES de cerrar

### sandbox-mata-background — 25-oct-2026
- CONTEXTO: run completo del noticiero lanzado con nohup & (Task 125)
- PASÓ: el sandbox mata los procesos hijos al terminar la llamada de shell (PID vivo → muerto, log 0 bytes)
- LECCIÓN: LECCIÓN: en este entorno el progreso vive en ARTEFACTOS, no en procesos — nunca depender de un proceso background entre llamadas
- CORRECCIÓN: scripts/ensamblar.mjs ejecuta el pipeline por etapas reanudables (audio→images→video) con estado en output/<fecha>/audio.json + images.json
- PREVENCIÓN: cualquier pipeline >5 min se divide en etapas con checkpoint §17 (eval E53)

### auditor-grader-demasiado-estricto — 25-oct-2026 (Task 124 — instalación ZOLO v6.1)
- CONTEXTO: reinstalación de ZOLO v6.1 en sandbox nuevo, primer run de `zolo_auditar_skills.py` (script recreado de cero)
- PASÓ: 26/26 skills clasificadas FAIL por: (a) frontmatter sin campo `trigger` (no es spec agentskills.io), (b) falta sección `## Cuándo`/`## Pasos` (nomenclatura flexible, no requerida), (c) false positive de "base64 token" en cualquier string >40 chars
- LECCIÓN: un auditor demasiado estricto produce 0% verde = auditor ROTO (eco regla 21: eval al 0% = eval roto). El grader determinista debe fallar solo por issues REALES (secretos, missing SKILL.md, frontmatter inválido), no por preferencias de estilo
- CORRECCIÓN: relajado a criterios alineados con agentskills.io spec v1: BLOCKING = sin SKILL.md / sin frontmatter / sin name+description / secretos; NON-BLOCKING = sin sección Grader (warn). Re-test: 26/26 verde
- PREVENCIÓN: el grader documenta en su docstring qué es BLOCKING vs NON-BLOCKING; cualquier cambio a estos criterios se versionaquea en CHANGELOG

### auditor-cuenta-directorio-archive — 25-oct-2026 (Task 128 — auto-curación)
- CONTEXTO: primera corrida de zolo_auto_curacion_semanal.sh, auditoría final报告ó 33/34 (1 FAIL)
- PASÓ: el curador creó `02_skills/.archive/` (vacío, placeholder) y el auditor lo contó como skill a auditar → FAIL por no tener SKILL.md
- LECCIÓN: el auditor debe excluir directorios ocultos (que empiezan con `.`) — `.archive/` es infraestructura, no una skill
- CORRECCIÓN: `if d.is_dir() and not d.name.startswith(".")` en zolo_auditar_skills.py
- PREVENCIÓN: cualquier directorio con prefijo `.` en 02_skills/ se trata como infraestructura, no skill
