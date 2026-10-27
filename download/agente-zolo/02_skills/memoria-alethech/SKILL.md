---
name: memoria-alethech
description: Protocolo completo de memoria con cadena de custodia usando alethech (Ed25519, hash-linked). Use when cerrar cambios de estado, arrancar una sesión con la cadena, emitir evidence de artefactos verificables, exportar el contenedor .aleth, rotar o revocar claves, ante una cadena comprometida, ante continuidad de checkpoint rota (rollback detection), y en simulacros de disaster recovery de memoria.
---

# Memoria con cadena de custodia (alethech v0.9.1)

Repo: `eddyflores100-lang/alethech` (v0.9.1, MIT, PyPI `alethech`) · Store: `/home/z/my-project/.alethech` · Vault: `.alethech-private/` chmod 700 · Puente MCP read-only: `alethech-mcp` (tras `pip install alethech`) o `python -m alethech.mcp_memory`.

## Qué prueba y qué NO (propietario del protocolo — no tergificar)

- **SÍ prueba**: integridad del store, autoría criptográfica (Ed25519 + JCS RFC 8785), relaciones de procedencia (hash-linked DAG), continuidad desde un checkpoint, continuidad causal de imports.
- **NO prueba**: que el contenido sea verdad (solo que fue firmado por la identidad que lo reclama). **NO detecta rollback sin checkpoint externo** — por eso este agente EMITE checkpoints. Sin LLM (cero tokens en runtime), sin nube requerida, sin blockchain.

## Superficie CLI (los 9 comandos)

```bash
alethech init                          # identidad + commit génesis (solo primera vez)
alethech commit --content '<json>'     # MemoryCommit firmado
alethech evidence --tool <nombre> --input <artifact> --output <receipt>   # EvidenceCommit firmado
alethech verify                        # verifica TODO el store, offline, fail-closed
alethech export --output memory.aleth  # contenedor portátil cifrado (scrypt + AES-256-GCM)
alethech import --input memory.aleth   # importa con verificación de continuidad causal
alethech key rotate                    # rota clave operativa con garantía de alcanzabilidad
alethech key revoke --key-id <id>      # revoca una clave (solo con mandato del usuario)
alethech migrate --to v0.2             # capa de identidad
```

Python API: `Alethech.initialize("./store")` → `agent.commit({...})` → `agent.seal("memory.aleth", passphrase)`; recepción: `Alethech.drop_context("memory.aleth", passphrase)` (desbloquea → verifica → contexto neutral).

## 1. BOOT (fail-closed — regla 24)

1. `alethech verify` — cualquier commit inválido = **cadena comprometida → INCIDENTE** (skill `runbook-incidentes`): declarar, operar SOLO desde worklog + `estado_sitio.json`, reportar huella del fallo. **Jamás sobrescribir, truncar o "reparar" la cadena por su cuenta.**
2. **Continuidad de checkpoint**: el checkpoint HEAD registrado debe ser ancestro del HEAD actual. Si no lo es → **ROLLBACK detectado** → reconstruir desde el último checkpoint + export `.aleth` más reciente + worklog; nunca "asumir que no pasó nada".
3. `recall --last 5` — usar `scripts/alethech_recall.py` (prueba `:` crudo y `%3A` — bug conocido del store, ya corregido a nivel de lector).
4. Sin store o sin CLI instalado: declararlo en el reporte BOOT y operar desde worklog. Instalar: `python3 -m pip install alethech`.

## 2. Cuándo commitear (gate de novedad)

**Commitea SOLO cambios de ESTADO**: deploy/rollback, credencial viva/muerta, decisión del usuario, regla nueva (§15), pendiente abierto/cerrado, hito de producto, incidente resuelto. **NO commitear**: reintentos sin cambio de estado, cifras ya fechadas en la cadena, contenido duplicado (la memoria redundante degrada el recall — patrón Cortex: ~80% de escrituras rechazadas por redundancia en producción).

## 3. Formato del commit (obligatorio — regla 24)

```json
{
  "que": "1 línea de hecho verificable",
  "cuando": "2026-10-21T14:30-05:00 (America/Guayaquil)",
  "evidencia": "URL | hash sha256 | HTTP code | Task ID del worklog",
  "pendientes": ["los que nacen o cierran"],
  "supersede": "ID del commit que corrige + por qué (solo si corrige)"
}
```

- Secretos DENTRO del contenido: solo huella `primeros4…últimos4` (regla 16).
- Cifra sin fecha+fuente NO entra a la cadena (regla de oro).
- Correcciones NUNCA borran ni editan hacia atrás: commit nuevo con `supersede` explícito (bi-temporal).

## 4. Evidence para artefactos verificables

`alethech evidence --tool <nombre> --input <artifact> --output <receipt>` para: vectores de test, releases, certificados Sentinel, snapshots de conformance, `audit.md`, `estado_sitio.json` trimestral. El receipt se referencia en el worklog del task.

## 5. Cierre de sesión con cambios de estado

`commit` (formato §3) → **checkpoint emitido** (alethech no detecta rollback sin checkpoint externo: el checkpoint es nuestro ancla) → `export --output memory.aleth` si cambió dispositivo o hay riesgo. El `.aleth` portátil **NUNCA lleva `root.key` ni `recovery.key`**. Sin commit de cierre, el siguiente BOOT arranca ciego — Task 114 solo sobrevivió porque había commit; el reset #3 borró lo que no estaba firmado.

## 6. Cadencia y DR

| Acción | Cadencia | Nota |
|---|---|---|
| `key rotate` | mensual o al menor sospecha | con garantía de alcanzabilidad (cutoff_head) |
| `key revoke` | solo con mandato del usuario | acción irreversible — árbol de decisión §9 |
| `export .aleth` | cierre de semana con estado | cifrado con passphrase; nunca claves raíz |
| Simulacro DR | trimestral (con `mantenimiento-mensual`) | export → store fresco → import → verify; objetivo ≤60s (referencia del repo: 42s medidos) |
| Linter de salud | mensual | entradas sin fecha, duplicados, referencias muertas, presupuesto de tamaño |

## 7. Relación con las otras capas de memoria

`worklog.md` = narrativa operativa (append-only, Task IDs, evidencia amplia) · `.alethech` = estado firmado y verificable · `ZOLO_V5.md` (núcleo vigente) = reglas. El worklog sin commit es memoria volátil (muere en reset); el commit sin evidencia en el worklog es memoria no auditable. Las dos se referencian mutuamente (Task ID ↔ commit).

**Interfaz (referencia de diseño)**: el founder subió el concepto **`Alethech Notebook`** (design concept React 19 + Vite + Tailwind 4, estilo Figma Make) como UI conceptual del notebook de memoria — visor de la cadena, commits y evidencia. Es REFERENCIA VISUAL, no requisito operativo: la operación funciona 100% por CLI. Si algún día se construye la UI, este design concept es el punto de partida y NUNCA reemplaza al CLI como superficie canónica.
## Grader (v6.0 — añadido por regla 32)

- Cambio de estado → commit estructurado (qué/cuándo/evidencia/pendientes) antes de declarar "hecho" → PASS.
- verify con commits inválidos → incidente declarado, cadena jamás sobrescrita → PASS. "Reparar" la cadena → FAIL grave.
- Corrección que borra/edita hacia atrás → FAIL (SUPERSEDE obligatorio).
