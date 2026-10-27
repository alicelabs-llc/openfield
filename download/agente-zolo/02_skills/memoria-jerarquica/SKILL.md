---
name: memoria-jerarquica
description: Gestión de la memoria de TRABAJO (v5.0, jerarquía de MemGPT/Letta). Activar cuando una sesión lleva muchas tool calls, el contexto crece con resultados grandes (HTMLs, JSONs, logs), se relee lo mismo dos veces, o antes de entrar a una fase nueva de una tarea larga. No toca el largo plazo (worklog + alethech — regla 24): organiza lo que vive en la ventana AHORA.
---

# Memoria jerárquica — la ventana es un presupuesto, páginala (v5.0, M6)

Modelo MemGPT/Letta verificado en producción: el contexto principal es finito; el agente funciona bien cuando él MISMO pagina contenido entre la ventana (caliente) y el almacenamiento (frío), y edita su propia memoria de trabajo. En ZOLO las 4 capas ya existen — esta skill define CUÁNDO y CÓMO mover contenido entre ellas (regla 22 es el presupuesto; esta es la mecánica).

## 1. Las 4 capas (de más caliente a más fría)

| Capa | Qué vive ahí | Caducidad | Soporte |
|---|---|---|---|
| **L1 Ventana caliente** | objetivo del run, checkpoint vigente, datos del paso ACTUAL, índice de skills | la sesión | contexto del chat |
| **L2 Archivo de sesión** | resultados grandes (HTML, JSON, logs), hallazgos intermedios, drafts | el run | `download/research/`, `plans/`, `scripts/out/` |
| **L3 Worklog** | narrativa con evidencia: qué se hizo, hashes, HTTP, lecciones | permanente (append-only) | `/home/z/my-project/worklog.md` |
| **L4 Alethech** | estado comprometido con firma (qué/cuándo/evidencia/pendientes) | permanente (Ed25519) | `.alethech` |

Regla de tránsito: **todo lo que ocupe >~50 líneas o no se necesite en las próximas 2 acciones, baja a L2** y se reemplaza en la ventana por 1 línea de referencia (`ver download/research/X.json — resumen: <3 palabras>`).

## 2. Señales de paginación (actuar ANTES de saturar)

- Un output de tool ocupó la ventana con datos crudos → extraer lo útil (grep/parse) a 1-5 líneas + guardar el crudo en L2.
- Me pillé re-leyendo el mismo archivo por 2ª vez → su versión comprimida (resumen con cifras) va a L2 y releer queda prohibido salvo delta.
- Fase cerrada del run → checkpoint (§17) y bajar todo lo no-referenciado.
- Cambio de tema del usuario → resumen de estado actual (≤5 líneas) + offload del resto.

## 3. Memoria auto-editable (protocolo de resumen)

Al compactar el trabajo propio, escribir en el archivo de sesión un bloque ESTADO editable:

```markdown
## ESTADO <fecha-hora> (editado por el agente)
OBJETIVO: <...> · PATRÓN: <...> · PRESUPUESTO RESTANTE: <...>
HECHO: <bullets con evidencia — lo verificable, no la narrativa>
ABIERTO: <bullets con lo pendiente y su bloqueo>
```

En la acción siguiente se lee SOLO ese bloque (no el histórico): la memoria de trabajo se edita, no se acumula. Lo que se saca NUNCA se pierde: baja a L2/L3 (worklog si aporta evidencia).

## 4. Lo que JAMÁS se pagina fuera de la ventana

1. Las reglas del núcleo (viven siempre — es su definición).
2. El checkpoint vigente del run (§17).
3. El criterio de salida del objetivo actual.
4. Los gates pendientes (G1/G2/G3) alcanzados y sin resolver.

Si la ventana ya no alcanza para todo esto: sesión nueva con checkpoint como primer mensaje (es el mecanismo diseñado para ello, regla 27 reanudación).

## 5. Compactación y recall

- Recall programático antes que memoria: `grep` en L2/L3 antes de "creo que era...". El grep es determinista; el recuerdo no.
- Compactación mensual de worklog → skill `mantenimiento-mensual` (L3); linter de cadena → skill `memoria-alethech` (L4).
- Duplicados en L2: al cerrar el run, un solo archivo final (`download/research/<slug>-final.md`) con el ESTADO + índice de artefactos; los crudos quedan junto a él para auditoría.
## Grader (v6.0 — añadido por regla 32)

- Sesión larga → offload de crudos a L2 (download/research/) + bloque ESTADO editable → PASS.
- Ventana conservando solo objetivo + checkpoint + criterio + gates → PASS.
- Resultado grande re-leído íntegro de la transcripción en vez de su referencia L2 → FAIL.
