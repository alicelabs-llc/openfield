# Playbook: PB-001 — Verificar en vivo antes de consumir

## Patrón detectado
Cualquier archivo binario, feed, API o dato externo debe verificarse EN VIVO (magic bytes / HTTP code / parseable) ANTES de consumirlo — asumir que un caché o asunción es válido = FAIL.

## Evidencia (3 ocurrencias)

- **2026-10-25** — Task 125-B — `api-imagenes-devuelve-jpeg`: API devuelve JPEG aunque contrato decía PNG; sin verificación de magic bytes, el pipeline rompe.
- **2026-10-25** — Task 125-A — `fuentes-verificadas-antes-de-config`: 3 de 5 feeds RSS iniciales estaban muertos en vivo (Infobae 404, El Universo 404, El Comercio anti-bot) pese a ser feeds "conocidos".
- **2026-10-25** — Task 124 — `drift /api/mcp 200→400`: endpoint que era 200 en Task 121 pasó a 400 en Task 124. Sin verificación en vivo, se citaría cifra stale.

## Heurística portable

```
ANTES de consumir cualquier EXTERNO (archivo, feed, API, dato):
  1. Verificar existencia/availability (HTTP HEAD / file exists)
  2. Verificar tipo/formato (magic bytes / content-type header)
  3. Verificar parseabilidad (JSON válido / XML válido / imagen decodable)
  4. SI CUALQUIERA falla → no consumir, reportar drift, buscar alternativa
  5. NUNCA asumir "como funcionó antes, funcionará ahora"
```

Aplica a:
- **Archivos binarios** generados por APIs (imágenes, audio, video) — verificar magic bytes
- **Feeds/APIs externas** — verificar HTTP code + parseable antes de agregar a config
- **Endpoints propios** — verificar estado actual antes de citar cifras (regla 5)
- **Cachés** — verificar que el caché sigue siendo válido (TTL o re-fetch)

## Acción de promoción

- [x] **Promover a regla del núcleo** — propuesta regla 34 para ZOLO_V7.md
- [x] **Eval nuevo** — E56 propuesto: "archivo/feed/API externo se verifica en vivo antes de consumir"
- [ ] Solo playbook (mantener como referencia)

## Contexto de origen

Generado por **skill sueno-consolidacion** (primera ejecución, Task 125).
Inspirado por patrón "Anthropic dreaming" (Code with Claude, May 2026).
3 ocurrencias detectadas en ledger → umbral de promoción (mínimo 2).

## Referencias grep-able

- `grep "verificar" 06_aprendizaje/LEARNINGS.md` — muestra las 3 entradas
- `grep "regla 5\|regla 6" 01_nucleo/ZOLO_V6.md` — reglas relacionadas (estado ACTUAL, stale vs real)
- `grep "magic bytes\|HTTP code" worklog.md` — aplicaciones concretas

---

**Próxima revisión**: cuando se detecten 2+ ocurrencias más de este patrón (umbral 5 para auto-aplicación sin gate founder).
