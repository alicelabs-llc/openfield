// Bump doc 6 to rev 3.1 — AUDIT_PENDING (administrative, no architectural changes).
import { db } from "../src/lib/db";

const NOTE = `

---

# rev 3.1 — estado: auditoría adversarial pendiente

> Revisión administrativa. No introduce cambios arquitectónicos. Solo registra que la cuestión permanece abierta.

Rev 3 incorporó las correcciones estructurales identificadas en la auditoría de rev 2: cadena monotónica de ControlEvents, cutoff causal en lugar de timestamps, y migración bilateral.

Antes de congelar la arquitectura queda pendiente una auditoría adversarial específica sobre:

- semántica temporal/causal de commits en DAGs con ramas
- concurrencia de commits
- commits offline y publicación diferida
- relación entre governance state y commit validity
- definición formal de "pertenencia a una época de autorización"

Esta revisión no introduce una solución al problema del cutoff en DAGs con ramas. Únicamente registra que la cuestión permanece abierta.

## propuesta de regla central (pendiente de auditoría GPT)

La propuesta que se enviará a GPT para auditoría adversarial:

> **La validez de un commit se determina por la key que lo firmó, no por su posición en el DAG. La posición en el DAG solo importa cuando la key está revocada — ahí, ancestry(cutoff_head) es la prueba criptográfica de pre-rotación.**

Reglas concretas:

Para un commit C firmado por key K:

- **K activa** → \`VALID\` (si firma verifica y parents válidos)
- **K revocada con cutoff M**:
  - C ∈ ancestry(M) → \`VALID_HISTORICAL\`
  - C ∉ ancestry(M) → \`REVOKED_KEY_AFTER_CUTOFF\`
- **K desconocida** → \`UNKNOWN_KEY\`

Esta propuesta fue revisada por el humano antes de enviarla a GPT. Sobrevivió a la crítica preliminar. Si GPT la confirma o la refina, se integra en rev 4. Si la rompe, se itera.

## lo que la propuesta NO resuelve todavía (trade-offs aceptados)

1. **Multiple rotaciones**: K1 revocada en rotación 1 (cutoff M1), K2 revocada en rotación 2 (cutoff M2). Commit firmado por K1 debe verificarse contra M1, no M2. Requiere que el verificador mapee cada key a su cutoff. Especificar.
2. **Replay entre stores**: ControlEvents firmados por root son válidos en cualquier store que tenga ese root. Si el atacante copia la chain completa, puede presentar la identidad. Pero no puede firmar commits nuevos sin una key activa. El protocolo no necesita prevenir replay de identidad — necesita prevenir forgery de commits. Eso ya está cubierto.
3. **Branches offline**: si una rama paralela firmada con K1 no estaba mergeada al HEAD cuando se rotó, esa rama queda inválida. Solución: el usuario debe merge todas las branches conocidas antes de rotar, o re-signarlas con K2 cuando vuelvan online. Trade-off: seguridad sobre conveniencia.
4. **Commits offline pre-rotación publicados después**: si un commit fue firmado por K1 antes de la rotación pero el contenido no está en ancestry(cutoff_head) porque el agente estaba offline, el commit queda \`REVOKED_KEY_AFTER_CUTOFF\`. El usuario tendría que re-signar con K2. Trade-off aceptado: honestidad sobre conveniencia.

## estados adicionales propuestos

- \`ORPHAN_COMMIT\` — commit sin conexión causal al genesis
- \`PARENT_INVALID\` — commit cuyo parent fue marcado como inválido

## revisión

- rev 1: especificación inicial con defectos de fundamento.
- rev 2: agregó auditoría dirigida (27 preguntas + prueba de diseño).
- rev 3: integra correcciones de GPT (ControlEvent chain, cutoff causal, MigrationRecord bilateral, 11 estados de verify).
- rev 3.1 (actual): estado \`AUDIT_PENDING\`. Registra que auditoría adversarial está pendiente. No toca arquitectura.
- rev 4 (futura): integra resultados de auditoría adversarial. Si la propuesta de regla central sobrevive, se congelará la spec.

— self, revisión 3.1 (AUDIT_PENDING)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!existing) throw new Error("doc not found");

  const updated = await db.doc.update({
    where: { slug: "arquitectura-identidad" },
    data: {
      body: existing.body + NOTE,
      status: "REVIEW", // mantenemos REVIEW porque AUDIT_PENDING no es un estado del enum
      author: "self (AUDIT_PENDING — auditoría adversarial pendiente)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision})`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
