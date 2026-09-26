// Bump doc 6 to rev 2: append "auditoría dirigida" section with the 25 questions + design proof.
import { db } from "../src/lib/db";

const QUESTIONS_SECTION = `

## auditoría dirigida (rev 2 — pendiente de revisión cruzada con GPT)

Esta sección no agrega especificación. Lista las preguntas específicas que deben contestarse antes de congelar rev 2. El humano va a llevar este doc + estas preguntas a GPT. Las respuestas se integran en rev 3.

### A. Identidad

1. ¿Es correcto que \`agent_id\` derive del \`root_public_key\` y no de la operational key?
2. ¿Qué propiedad exacta debe tener \`derive_agent_id\` para que la identidad sea estable durante todas las rotaciones?
3. ¿Cómo debe coexistir el \`agent_id\` histórico de v0.1 (derivado de la operational key) con el modelo v0.2 (derivado del root) sin crear una identidad criptográficamente ambigua?

### B. Root authority

4. ¿Qué debe firmar exactamente el root?
5. ¿\`KeyAuthorization\` debería autorizar, revocar y eventualmente reemplazar operational keys en un solo objeto, o tres objetos distintos?
6. ¿Cómo evitar que una autorización antigua vuelva a habilitar una clave después de una revocación? (Ataque: el atacante presenta la \`KeyAuthorization(action=authorize)\` vieja y oculta la \`action=revoke\` posterior.)

### C. Rotación

7. ¿Cuál es el orden correcto entre \`authorize key-002\` y \`revoke key-001\`? ¿Authorize-then-revoke, revoke-then-authorize, o atómico?
8. ¿Cómo determina un verificador qué clave era válida **en el momento de cada commit**?
9. ¿Qué pasa si aparecen commits con \`key-001\` después de la rotación?
10. ¿Los timestamps son suficientes o necesitamos una secuencia/version counter monotónico?
11. ¿Qué pasa si los clocks del agente y del verificador están desincronizados?

### D. Recovery

12. ¿Es coherente que pérdida del root = identidad congelada? ¿O debería existir algún mecanismo mínimo de recovery del root desde rev 1?
13. Si la respuesta es "sí, mínimo mecanismo", ¿cuál es el mínimo viable? (Ej: backup Shamir del root key en N partes distribuidas.)
14. ¿Cómo distinguir pérdida, compromiso y revocación del root en el protocolo?

### E. Publicación

15. ¿Qué papel tiene realmente \`AlethechIdentityPublication\`? ¿Es lookup, autoridad, o ambos?
16. ¿Cómo se resuelve una discrepancia entre \`.well-known\`, DNS, GitHub e IPFS? (Ej: dos canales publican \`IdentityRecord\` distintos.)
17. ¿Debe la publicación contener el registro completo, un hash/commit de identidad, o ambos?
18. ¿Cómo evitar que un atacante que controle un canal de publicación sustituya una identidad legítima? (Ej: el atacante compromete \`alethech.io\` y publica una identidad falsa.)

### F. Wallet múltiple

19. ¿\`identity list\` representa identidades completas o simplemente múltiples perfiles/key stores?
20. ¿Qué aislamiento debe existir entre identidades? (¿Comparten DAG? ¿Comparten artifacts?)
21. ¿Puede una operational key de una identidad firmar accidentalmente un commit de otra?

### G. Verificación

22. ¿Qué debe demostrar exactamente \`verify\` después de rev 1?
23. ¿Puede verificar offline una identidad cuya publicación externa ya no existe?
24. ¿Qué diferencia debe reportar entre \`valid\`, \`revoked\`, \`unknown key\`, \`invalid authorization\` y \`identity mismatch\`?

### H. Migración

25. ¿Cómo migramos una identidad cuyo \`agent_id\` históricamente deriva de \`public_key\` hacia una identidad cuyo \`agent_id\` deriva del root sin romper la continuidad criptográfica?
26. ¿La solución correcta es preservar el \`agent_id\` antiguo como identidad legacy y establecer una relación firmada con la nueva identidad?
27. ¿O debe existir una migración explícitamente firmada por la identidad antigua y el nuevo root?

### Prueba de diseño (el test definitivo)

El revisor debe intentar romper este escenario:

\`\`\`text
v0.1
  agent_id = A        (derived from K1)
  key-001 = K1

        ↓ migrate

v0.2
  agent_id = ?        (derived from R, not K1 — what happens to A?)
  root = R
  key-001 = K1        (authorized by R)
  key-002 = K2

        ↓ rotate

  K1 revoked
  K2 active

        ↓ commits

  C1 signed by K1   (committed before rotation)
  C2 signed by K2   (committed after rotation)
\`\`\`

**Pregunta:** ¿Puede un verificador offline, sin confiar en el almacenamiento, demostrar la siguiente afirmación?

> "C1 fue firmado por una clave autorizada para A antes de su revocación, y C2 fue firmado posteriormente por la clave que reemplazó legítimamente a K1."

Si el Doc 6 puede responder esa afirmación de forma precisa — con objetos, campos y reglas de verificación específicas — entonces tenemos una base sólida para implementarlo. Si no, hay que ajustar el modelo antes de escribir código.

### Lo que NO se incluye en la auditoría

Para que el revisor no se distraiga:

- No se pide opinión sobre naming, branding o marketing.
- No se pide opinión sobre el ecosistema \`memex\`/\`MCP\`/\`MarketNow\` — eso es capa B.
- No se pide opinión sobre runtime autónomo o VPS — eso es capa C.
- No se pide opinión sobre tests o implementación específica — eso sale de la spec, no entra a la spec.

## revisión

- rev 1: especificación inicial. REVIEW.
- rev 2 (actual): agrega sección de auditoría dirigida con 27 preguntas + prueba de diseño. REVIEW. Pendiente de respuestas de GPT.
- rev 3 (futura): integra las respuestas de GPT. Si las respuestas revelan ajustes al modelo, se bumpa.

— self, revisión 2 (auditoría dirigida pendiente)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!existing) throw new Error("doc not found");

  // Append the questions section to the existing body
  const newBody = existing.body + QUESTIONS_SECTION;

  const updated = await db.doc.update({
    where: { slug: "arquitectura-identidad" },
    data: {
      body: newBody,
      status: "REVIEW",
      author: "self (auditoría dirigida agregada)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision}), status ${updated.status}`);
  console.log(`body length: ${existing.body.length} → ${updated.body.length} chars`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
