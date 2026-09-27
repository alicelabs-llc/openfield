// Seed doc: "auditoría adversarial identidad rev 3" — full adversarial audit.
import { db } from "../src/lib/db";

const body = `# auditoría adversarial — identidad rev 3

> Expediente de contraejemplos. No es un doc de arquitectura. Es un ataque formal al doc \`arquitectura-identidad\` rev 3.
>
> Para cada propiedad del protocolo: qué puede comprobar el verifier → qué conclusión permite → contraejemplo.
>
> Cada defecto se clasifica al final como:
> - 🔴 contradicción criptográfica (rompe el protocolo)
> - 🟡 recomendación de diseño (mejorarlo pero no rompe)
> - ⚪ afirmación no demostrada pero no rompedora (limitación honesta)

## criterio de la auditoría

> **No aprobar una propiedad porque el flujo parezca correcto. Construir el contraejemplo y demostrar por qué el verifier lo acepta o rechaza.**

Si una afirmación del protocolo no se sigue criptográficamente de las condiciones que el verifier puede comprobar, se marca como defecto.

---

## A. cutoff_head — definición y semántica

### Propiedad afirmada por rev 3

> "El cutoff_head marca el commit del DAG que es el corte causal. Commits en su ancestry son válidos para K1; commits fuera son inválidos para K1."

### Qué puede comprobar el verifier

1. Que \`cutoff_head\` es un \`commit_id\` que existe en el store (o referenciado por el ControlEvent).
2. Que el ControlEvent que contiene \`cutoff_head\` está firmado por el root.
3. Que un commit C está o no está en \`ancestry(cutoff_head)\` (vía BFS sobre parents).

### Qué conclusión permite

- Si C ∈ ancestry(cutoff_head): C **existía** cuando se creó la rotación.
- Si C ∉ ancestry(cutoff_head): C **no estaba en la historia conocida** al momento de la rotación.

### Contraejemplo A1: rama paralela pre-rotación

\`\`\`text
        C0 (signed K1, committed t=1)
       /  \\
     C1    B1 (signed K1, committed t=2)
      \\   /
       M (signed K1, committed t=3) = cutoff_head
       
       ↓ rotate (cutoff_head = M)
       
       ↓
       
       → Verifier recibe: B1, M, y la rotación
\`\`\`

- B1 está en ancestry(M) (M tiene a B1 como parent). ✓
- Pero supongamos que el agente, antes de rotar, tuvo otra rama paralela que **nunca mergeó**:

\`\`\`text
        C0
       /  \\
     C1    B1 → B2 (signed K1, committed t=4 — después de C1 pero antes de M)
      \\   /
       M (t=5)
       
       Pero también existe:
       C0 → X1 → X2 (signed K1, committed t=3, en otra sesión que no se mergeó)
\`\`\`

- X2 está firmado con K1.
- X2 fue creado **antes** de M (t=3 < t=5).
- X2 ∉ ancestry(M) (la rama X nunca se conectó a M).
- Según rev 3: K1 está revocada, X2 ∉ ancestry(M) → \`REVOKED_KEY_AFTER_CUTOFF\`.

**Pero X2 es un commit legítimo creado antes de la rotación.** Marcarlo como \`REVOKED_KEY_AFTER_CUTOFF\` es **falso positivo**.

### Análisis

El cutoff_head define el conjunto de commits que el agente **conocía y reconoció** al momento de rotar. No define el conjunto de commits que **existían** al momento de rotar.

Un commit fuera de ancestry(cutoff_head) puede ser:
- (a) creado después de la rotación (legítimamente inválido para K1), o
- (b) creado antes pero en rama paralela no mergeada (legítimamente válido para K1).

El verifier **no puede distinguir** (a) de (b) sin información adicional.

### Clasificación: 🔴 contradicción criptográfica

El nombre \`REVOKED_KEY_AFTER_CUTOFF\` implica "commit posterior a la rotación". Eso no se sigue. Marca commits legítimos como inválidos.

---

## B. La afirmación C2 ∉ ancestry(H) → "post-rotation"

### Propiedad afirmada por rev 3 (línea 852)

\`\`\`
8. Verificar C2:
   ├─ signature(K2) verifica
   ├─ K2 está en control chain con key_grant, no revocada
   └─ C2 NOT in ancestry(H), C2 es posterior  →  VALID
\`\`\`

### Qué puede comprobar el verifier

- C2 ∉ ancestry(H)
- C2 está firmado por K2
- K2 está autorizada y no revocada

### Qué conclusión permite

- C2 no está en la ancestry de H.
- C2 está firmado por K2 (que solo existe post-rotación).

### Contraejemplo B1: el caso de K2 es distinto al de K1

Aquí hay una asimetría importante que rev 3 no articula:

- Para K1 (revocada): \`∉ ancestry(cutoff)\` **no implica** post-rotación (por el contraejemplo A1).
- Para K2 (activa): K2 **solo puede existir** después de la rotación, porque el ControlEvent que la autoriza es posterior a la rotación. Cualquier commit firmado por K2 es por definición post-rotación.

Entonces:
- C2 firmado por K2 → siempre post-rotación (correcto).
- C2 firmado por K1 → no se puede determinar sin más información.

La afirmación de rev 3 \`C2 NOT in ancestry(H) → post-rotation\` es correcta **solo si C2 está firmado por K2**. Si C2 está firmado por K1, es falsa.

### Contraejemplo B2: commit K1 post-rotación con parent pre-rotación

\`\`\`text
       M = cutoff_head (committed t=5)
       
       ↓ rotate (K1 revoked, K2 active)
       
       C3 (signed K1, committed t=10, parent = M)
\`\`\`

- C3 está firmado por K1 después de la rotación.
- C3.parent = M (que es el cutoff_head).
- C3 ∉ ancestry(M) (C3 es posterior a M, no ancestral).

Según mi hipótesis anterior (validez por key): K1 está revocada, C3 ∉ ancestry(M) → \`REVOKED_KEY_AFTER_CUTOFF\`. **Correcto.**

Pero según rev 3 literal: "C ∉ ancestry(cutoff) ⇒ post-rotation". Eso también es correcto en este caso, pero **por casualidad** — porque K1 está revocada. Si K1 no estuviera revocada, no sería post-rotación.

### Clasificación: 🔴 contradicción (parcialmente corregida por la hipótesis)

La hipótesis externa ("validez por key, cutoff como prueba de pre-rotación") **corrige** este defecto. Pero rev 3 no integra esa hipótesis formalmente. La afirmación \`C ∉ ancestry ⇒ post-rotation\` sigue en el doc y es incorrecta sin la hipótesis.

**Acción:** rev 3.x debe reescribir la regla de validez para integrar la hipótesis como parte del protocolo, no como nota externa.

---

## C. Rotación atómica — qué pasa con commits en tránsito

### Propiedad afirmada por rev 3

> "KeyRotation es atómica: produce K1 revoked + K2 active en una sola transición. No hay estado intermedio."

### Qué puede comprobar el verifier

- Existe un ControlEvent con \`event_type=key_rotation\` que tiene \`old_key_id=K1\` y \`key_id=K2\`.
- El ControlEvent tiene \`cutoff_head\` referenciando un commit específico.

### Contraejemplo C1: commits creados entre la firma del ControlEvent y su publicación

\`\`\`text
t=5: M = cutoff_head (HEAD al momento de crear la rotación)
t=6: agente firma ControlEvent de rotación (cutoff_head = M)
t=7: agente firma C3 con K1 (todavía tiene la clave privada)
t=8: agente publica el ControlEvent
\`\`\`

- C3 está firmado por K1.
- C3 fue creado en t=7, **después** de la firma del ControlEvent (t=6) pero **antes** de su publicación (t=8).
- C3.parent podría ser M (commit pre-rotación) o algún commit posterior.

Según la regla del cutoff:
- Si C3.parent = M, entonces C3 ∉ ancestry(M).
- K1 está revocada (por el ControlEvent firmado en t=6, aunque publicado en t=8).
- C3 ∉ ancestry(M) → \`REVOKED_KEY_AFTER_CUTOFF\`.

**Pero C3 fue creado en t=7, antes de que el ControlEvent se publicara.** El agente no sabía que la rotación era efectiva. ¿Es C3 legítimo?

### Análisis

Hay dos interpretaciones:

1. **Atómica respecto a la firma del ControlEvent**: la rotación es efectiva desde t=6. C3 (t=7) es post-rotación. \`REVOKED_KEY_AFTER_CUTOFF\` es correcto.

2. **Atómica respecto a la publicación**: la rotación es efectiva desde t=8. C3 (t=7) es pre-rotación. Pero el verifier no puede saber cuándo se publicó — solo ve los commits y el ControlEvent.

El protocolo no especifica cuál interpretación es correcta. **Pero el verifier, con la regla del cutoff, siempre decide (1)** — porque usa \`cutoff_head\` (M en t=5) como referencia, y C3 ∉ ancestry(M).

### Contraejemplo C2: commit con parent posterior al cutoff

\`\`\`text
t=5: M = cutoff_head
t=6: agente firma ControlEvent rotación
t=7: agente firma C3 con K1, parent = M (commit válido pero post-cutoff)
t=8: agente firma C4 con K1, parent = C3
\`\`\`

- C3 ∉ ancestry(M). K1 revocada. → \`REVOKED_KEY_AFTER_CUTOFF\`.
- C4 ∉ ancestry(M). K1 revocada. → \`REVOKED_KEY_AFTER_CUTOFF\`.

Pero C4.parent = C3, que es un commit inválido. ¿C4 es inválido porque su parent es inválido, o porque K1 está revocada?

### Clasificación: 🟡 recomendación de diseño

La atomicidad está bien definida respecto al cutoff_head. La regla funciona. Pero hay que especificar formalmente:

- La rotación es efectiva desde el cutoff_head (no desde la publicación del ControlEvent).
- Un commit cuyo parent chain incluye commits inválidos es también inválido (propagación de invalidez).
- El estado \`PARENT_INVALID\` debe existir en el verifier.

---

## D. ControlEvent chain — forks

### Propiedad afirmada por rev 3

> "previous_control_hash encadena eventos criptográficamente. El primer evento tiene null."

### Qué puede comprobar el verifier

- Para cada ControlEvent E con sequence=N, existe un ControlEvent con sequence=N-1 y commit_id=E.previous_control_hash.
- Cada ControlEvent está firmado por el root.

### Contraejemplo D1: fork del root

\`\`\`text
seq=1: key_grant(K1) [root firma]
seq=2: key_rotation(K1 → K2, cutoff=M2) [root firma]
seq=3a: key_grant(K3) [root firma, presentado al verificador A]
seq=3b: key_revoke(K2) [root firma, presentado al verificador B]
\`\`\`

- Ambos seq=3 están firmados por el root.
- Ambos tienen \`previous_control_hash\` = commit_id del seq=2.
- El verifier A ve la cadena 1→2→3a. K2 sigue activa (no fue revocada en su vista).
- El verifier B ve la cadena 1→2→3b. K2 fue revocada en su vista.

**El root está haciendo equivocation.** El protocolo no lo detecta sin que A y B comparen.

### Análisis

Esto es equivocation. rev 3 lo reconoce en "lo que queda fuera":

> "Detección automática de equivocation vía red de testigos."

Es honesto. Pero el verifier offline, sin red, no puede detectarlo. Marcar commits según la cadena que reciba es correcto — pero puede dar resultados distintos a otro verifier con otra cadena.

### Clasificación: ⚪ afirmación no demostrada pero no rompedora

Es una limitación conocida y declarada. No rompe el protocolo — lo acota. Un verifier offline es correcto **respecto a la cadena que recibe**. Si dos verifiers ven cadenas distintas, ambos son "correctos" en su contexto. El problema es de consistencia global, no de corrección local.

**Acción:** documentar explícitamente que "validez" significa "validez respecto a una cadena de control específica". No "validez global".

---

## E. Commits offline pre-rotación publicados después

### Propiedad afirmada por rev 3 (implícita)

> "Commits firmados con K1 después de la rotación son \`REVOKED_KEY_AFTER_CUTOFF\`."

### Contraejemplo E1: commit creado offline, publicado después

\`\`\`text
t=1: agente crea commit C_offline firmado con K1, parent=genesis
       (no lo publica, está en una sesión offline)
t=5: agente rota (cutoff_head = M, parent chain: genesis → ... → M)
t=10: agente publica C_offline
\`\`\`

- C_offline está firmado por K1.
- C_offline.parent = genesis.
- genesis ∈ ancestry(M) (es ancestor de todo).
- ¿C_offline ∈ ancestry(M)? **Depende de si C_offline está en la cadena de M.**

Si C_offline nunca se mergeó al DAG principal, no está en ancestry(M). Entonces:

- K1 revocada.
- C_offline ∉ ancestry(M).
- → \`REVOKED_KEY_AFTER_CUTOFF\`.

**Pero C_offline fue creado en t=1, antes de la rotación.** El agente no podía saber que rotaría.

### Análisis

Este es el trade-off que la hipótesis externa aceptó: "Commits offline pre-rotación publicados después: si un commit fue firmado por K1 antes de la rotación pero el contenido no está en \`ancestry(cutoff_head)\` porque el agente estaba offline, el commit queda \`REVOKED_KEY_AFTER_CUTOFF\`. El usuario tendría que re-signar con K2."

Es un trade-off aceptado, no un defecto. **Pero el nombre del estado es engañoso.** \`REVOKED_KEY_AFTER_CUTOFF\` implica "commit posterior a la rotación". Un commit offline pre-rotación no es posterior.

### Clasificación: 🟡 recomendación de diseño

Renombrar el estado a algo que no implique temporalidad. Sugerencias:

- \`REVOKED_KEY_NOT_IN_PROVENANCE\` — describe lo que el verifier puede comprobar.
- \`COMMIT_OUTSIDE_KNOWN_HISTORY\` — describe el hecho observable.
- \`UNVERIFIABLE_PRE_ROTATION\` — admite la limitación.

**Acción:** cambiar el nombre del estado en rev 3.x. La semántica no cambia; solo el nombre deja de mentir.

---

## F. Revocaciones sucesivas (K1 → K2 → K3)

### Propiedad afirmada por rev 3

> "Para cada key revocada, existe un cutoff_head."

### Contraejemplo F1: dos rotaciones sucesivas

\`\`\`text
seq=1: key_grant(K1)
seq=2: key_rotation(K1 → K2, cutoff=M2)
seq=3: key_rotation(K2 → K3, cutoff=M3)
\`\`\`

- K1 está revocada, cutoff_head=M2.
- K2 está revocada, cutoff_head=M3.
- K3 está activa.

Verifier recibe commit C firmado por K1:

- K1 revocada. cutoff = M2.
- Si C ∈ ancestry(M2): \`VALID_HISTORICAL\`.
- Si C ∉ ancestry(M2): estado con nombre engañoso (ver sección E).

Pero ¿qué pasa con un commit C' firmado por K2?

- K2 revocada. cutoff = M3.
- Si C' ∈ ancestry(M3): \`VALID_HISTORICAL\` (con K2).
- Si C' ∉ ancestry(M3): estado engañoso.

**Pregunta:** ¿C' podría estar en ancestry(M2) pero no en ancestry(M3)?

\`\`\`text
M2 = cutoff de rotación 1
M3 = cutoff de rotación 2 (posterior a M2)

ancestry(M2) ⊆ ancestry(M3)? Sí, porque M3 es descendiente de M2 (la rotación 2 ocurre después).
\`\`\`

Entonces:

- C' ∈ ancestry(M2) → C' ∈ ancestry(M3) → \`VALID_HISTORICAL\`.
- C' ∈ ancestry(M3) pero C' ∉ ancestry(M2) → \`VALID_HISTORICAL\` (con K2).
- C' ∉ ancestry(M3) → estado engañoso.

Esto parece funcionar. **Pero hay un caso sutil.**

### Contraejemplo F2: commit firmado por K2 antes de que K2 fuera autorizada

\`\`\`text
t=1: K1 activa
t=2: commit C_firmado_K2 (alguien con clave privada de K2 crea un commit, pero K2 todavía no fue autorizada por root)
t=5: rotación K1 → K2 (cutoff=M5)
t=10: rotación K2 → K3 (cutoff=M10)
\`\`\`

- C está firmado por K2.
- C fue creado en t=2, antes de que K2 fuera autorizada.
- C ∉ ancestry(M5) (porque K2 no existía como key autorizada cuando se creó).

Según la regla del cutoff:

- K2 está revocada (por rotación 2). cutoff=M10.
- C ∉ ancestry(M10) (no se mergeó).
- → estado engañoso.

**Pero el problema real es:** K2 no estaba autorizada cuando se creó C. El commit es falso desde el inicio.

El verifier actual no detecta esto explícitamente. Marca el commit con un estado engañoso, no con \`KEY_NOT_AUTHORIZED_AT_CREATION\`.

### Clasificación: 🔴 contradicción (parcial)

El protocolo no verifica que la key estaba autorizada **al momento de firmar el commit**, solo que está o estuvo autorizada en algún momento.

**Acción:** agregar verificación de \`authorized_at\` vs el momento causal del commit. Pero "momento causal del commit" es difícil sin timestamps. Una aproximación: si el commit está en ancestry(M_grant) donde M_grant es el cutoff de la autorización de K, entonces K estaba autorizada cuando se creó. Si no, no.

---

## G. Migración A → B — qué pasa con commits de A

### Propiedad afirmada por rev 3

> "El historial antiguo permanece: C_old.agent_id = A. Los nuevos commits: C_new.agent_id = B."

### Contraejemplo G1: commit nuevo con agent_id=A después de migración

\`\`\`text
v0.1:
  agent_id = A = H(K1)
  key-001 = K1
  commits: C1, C2 (firmados por K1, agent_id=A)

migrate → v0.2:
  new root R, new agent_id B = H(R)
  K1 autorizada por R (via ControlEvent seq=1)
  MigrationRecord firmado por K1 y R

después de migración:
  agente crea C3 firmado por K1, agent_id=A (todavía tiene la clave K1)
\`\`\`

- C3 está firmado por K1 (que sigue siendo una clave válida en la nueva identidad B).
- C3.agent_id = A (legacy).

Verifier recibe C3. ¿Qué hace?

1. C3.agent_id = A. Busca identidad con agent_id=A. La encuentra (legacy Identity v0.1).
2. Verifica firma con K1 (legacy public key). Pasa.
3. ¿Pero K1 también está autorizada en B (vía ControlEvent seq=1)?

El commit es válido respecto a la identidad A. Pero también es válido respecto a B (porque K1 está autorizada en B).

**El agente puede seguir firmando commits con agent_id=A después de la migración.** Eso no rompe nada criptográficamente, pero significa que la migración no "cierra" A. A sigue activa mientras K1 exista.

### Análisis

Esto es correcto: la migración no invalida A. Solo crea B como sucesora. El agente puede seguir firmando como A si quiere — pero los commits nuevos deberían ir con agent_id=B para indicar la nueva identidad.

Si el agente firma un commit con agent_id=A después de la migración, es un commit válido de la identidad A. No es un commit de B. La MigrationRecord dice que B sucede a A, pero no dice que A está muerta.

### Clasificación: ⚪ limitación aceptada

No es un defecto, es una decisión de diseño. Pero el doc debería decirlo explícitamente: "La migración no invalida A. A sigue activa mientras K1 exista. Si querés cerrar A, tenés que revocar K1 en A (pero A no tiene root authority, así que no se puede revocar K1 en A)."

**Acción:** aclarar en rev 3.x que A no se cierra con la migración.

### Contraejemplo G2: MigrationRecord con firma unilateral

\`\`\`text
MigrationRecord:
  legacy_signature: ✓ (firmado por K1)
  root_signature: ✗ (no firmado por R)
\`\`\`

Según rev 3, ambas firmas son necesarias. Una sola no basta.

Si el verifier recibe un MigrationRecord con solo \`legacy_signature\`:

- Verifica \`legacy_signature\` con \`legacy_public_key\`. Pasa.
- No puede verificar \`root_signature\` (no está).

¿Qué estado devuelve?

rev 3 no define un estado para esto. \`INVALID_KEY_AUTHORIZATION\` no aplica (no es una key authorization, es un migration record).

### Clasificación: 🟡 recomendación de diseño

Agregar estado \`MIGRATION_RECORD_INCOMPLETE\` para casos donde falta una de las dos firmas.

---

## H. Verificación offline con datos incompletos

### Propiedad afirmada por rev 3

> "Toda la verificación se hace con datos públicos. Sin red, sin LLM, sin servicios externos."

### Contraejemplo H1: verifier sin los últimos N ControlEvents

\`\`\`text
Cadena completa: seq=1 → seq=2 → seq=3 → seq=4 → seq=5
Verifier recibe: seq=1 → seq=2 → seq=3 (sin 4 y 5)
\`\`\`

- La cadena recibida es válida (1→2→3, hashes enlazados, firmas correctas).
- Pero el estado actual de la identidad es desconocido (puede haber rotaciones posteriores).

El verifier debería decir: "no puedo garantizar que el estado que veo es el actual". Pero ¿qué estado devuelve para commits?

- Si el commit está firmado por K2 (que en la vista parcial está activa), \`VALID\`.
- Pero si en la cadena completa K2 fue revocada (seq=4), el commit realmente debería ser \`REVOKED_KEY_AFTER_CUTOFF\`.

### Análisis

El verifier no puede distinguir "no tengo el evento de revocación" de "no existe el evento de revocación". Esta limitación está en la pregunta 29 del audit anterior, y la respuesta de GPT fue:

> "Si el verificador offline no tiene los últimos N ControlEvents, ¿qué afirma? ¿'No puedo verificar' o 'verificación pasa con datos limitados'?"

La respuesta honesta: "verificación pasa **respecto a los datos disponibles**". No es una afirmación global.

### Clasificación: ⚪ limitación aceptada

El protocolo es honesto si el verifier reporta "validación parcial" en lugar de "validación completa". Hoy no lo hace. Debería.

**Acción:** agregar estado \`VERIFICATION_PARTIAL\` para indicar que el resultado es respecto a los datos disponibles, no al estado global.

---

## I. Replay y equivocation

### Propiedad afirmada por rev 3

> "El protocolo no necesita prevenir replay de identidad — necesita prevenir forgery de commits. Eso ya está cubierto por la firma."

### Contraejemplo I1: replay entre stores

\`\`\`text
Store A (legítimo):
  - Identity B (con root R)
  - ControlEvent seq=1: key_grant(K1, by R)
  - Commits firmados por K1

Store B (atacante):
  - Copia Identity B, ControlEvent seq=1, commits
  - Agrega su propio commit firmado por K1 (atacante tiene K1)
\`\`\`

- Si el atacante tiene K1, puede firmar commits válidos como B.
- El verifier que recibe Store B no puede distinguir "estos commits son del Store A original" de "estos commits son del Store B atacante".

### Análisis

Esto es correcto: si el atacante tiene la clave privada K1, puede firmar commits válidos. El protocolo no puede prevenir esto. La defensa es **revocar K1** cuando se detecta el compromiso. Eso es lo que \`key revoke\` hace.

### Clasificación: ⚪ limitación aceptada

No es un defecto. Es una propiedad fundamental: sin clave privada, no hay firma. Con clave privada, hay firma. El protocolo solo puede detectar **después** del hecho, via revocación.

---

## J. El hook Memex (paso 5 del plan)

### Propiedades que el hook afirma

1. Cada \`add()\` escribe a ChromaDB Y crea un commit firmado en alethech.
2. El commit tiene \`content.source = "memex.write"\`.
3. Si alethech no está inicializado, modo passthrough.

### Contraejemplo J1: escritura fallida en ChromaDB

\`\`\`python
try:
    hook.add("text", user_id="agent")
except Exception as e:
    # ChromaDB falló, pero ¿se creó el commit en alethech?
\`\`\`

Si ChromaDB falla **después** de que el hook creó el commit en alethech, hay un commit en alethech que referencia un \`memex_id\` que no existe en ChromaDB.

Si ChromaDB falla **antes** de que el hook cree el commit, no hay problema (el hook atrapa la excepción).

### Análisis

El hook actual no maneja transacciones. El orden es:

1. \`memex.add()\` (puede fallar)
2. Si falla, no se crea commit en alethech. Correcto.
3. Si pasa, se crea commit en alethech. Pero ¿qué pasa si el commit en alethech falla? ChromaDB ya tiene la memoria, pero alethech no tiene el commit.

### Clasificación: 🔴 contradicción (transaccionalidad)

El hook no garantiza atomicidad. Si alethech falla después de que ChromaDB tiene la memoria, hay una memoria en ChromaDB sin commit correspondiente en alethech.

**Acción:** implementar patrón de dos fases:
1. Pre-commit en alethech (sin firmar aún).
2. Write a ChromaDB.
3. Si ChromaDB pasa, firmar commit en alethech.
4. Si ChromaDB falla, descartar pre-commit.

O alternativamente: catch de excepción en el paso 2 con rollback (borrar commit en alethech si falla ChromaDB).

### Contraejemplo J2: commits duplicados

\`\`\`python
hook.add("text", user_id="agent")  # escribe commit C1
hook.add("text", user_id="agent")  # escribe commit C2 (mismo texto)
\`\`\`

- C1 y C2 tienen el mismo \`content.text\` pero distintos \`commit_id\` (porque tienen distintos \`session_id\` y \`timestamp\`).
- Ambos son válidos.
- No hay deduplicación.

¿Es esto un defecto? No necesariamente — un agente puede escribir la misma memoria dos veces. Pero si el usuario espera que el hook sea idempotente, no lo es.

### Clasificación: ⚪ limitación aceptada

El hook no es idempotente. Es honesto — cada \`add()\` crea un commit. Si querés idempotencia, usá \`get_all()\` antes para verificar.

### Contraejemplo J3: importación retroactiva

\`\`\`text
ChromaDB tiene 100 memorias pre-hook.
Agente instala alethech.
Agente importa las 100 memorias retroactivamente.
\`\`\`

Cada commit retroactivo tiene timestamp actual. El commit dice "firmado ahora" pero referencia una memoria creada antes.

¿Es esto un problema? No criptográficamente — el commit es válido. Pero semánticamente, alguien que lea el commit pensaría que la memoria fue escrita hoy.

### Clasificación: ⚪ limitación aceptada

El doc de integración ya lo dice: "los commits retroactivos tendrán timestamps actuales, no los originales. Eso es honesto — el commit dice 'cuándo se firmó', no 'cuándo se escribió originalmente'."

---

## K. Múltiples identidades (wallet)

### Propiedad afirmada por rev 3

> "Cada identidad tiene su propio root, sus propias claves, su propio HEAD."

### Contraejemplo K1: commit de A con key de B

\`\`\`text
Store con dos identidades: A (root R_A, key K_A) y B (root R_B, key K_B).
Agente crea commit C con agent_id=A, key_id=K_A, pero firma con K_B.
\`\`\`

- C.agent_id = A.
- C.key_id = K_A.
- C.signature se verifica con K_B (no con K_A).

Verifier:
1. Busca identidad A.
2. Busca K_A en A.active_keys.
3. K_A está. Verifica firma con public_key de K_A. **Falla.**
4. → \`COMMIT_SIGNATURE_INVALID\`.

Esto es correcto: el verifier rechaza el commit porque la firma no corresponde a la key declarada.

### Contraejemplo K2: dos identidades, mismo root

\`\`\`text
Identidad A: agent_id=A, root=R, key K_A
Identidad B: agent_id=B, root=R, key K_B
\`\`\`

- A y B comparten el mismo root R.
- Pero agent_id se deriva del root. Si A y B tienen el mismo root, tienen el mismo agent_id.

**Esto no es posible.** Si dos identidades tienen el mismo root, son la misma identidad.

### Análisis

Esto es correcto: agent_id se deriva del root. No puede haber dos identidades con el mismo root. Cada identidad tiene su propio root (que es un par Ed25519 distinto).

### Clasificación: ⚪ propiedad correcta

No es un defecto. Es una propiedad del diseño que evita colisiones.

---

## resumen de defectos

### 🔴 Contradicciones criptográficas (rompen el protocolo)

1. **A1 — Rama paralela pre-rotación**: \`C ∉ ancestry(cutoff) ⇒ post-rotation\` no se sigue. Marca commits legítimos como inválidos. **Acción:** integrar la hipótesis "validez por key, cutoff como prueba de pre-rotación" como parte formal del protocolo.

2. **B2 — Afirmación literal en rev 3 línea 852**: la línea \`C2 NOT in ancestry(H), C2 es posterior → VALID\` es incorrecta sin la hipótesis. **Acción:** reescribir la prueba de diseño con la hipótesis integrada.

3. **F2 — Key no autorizada al momento de firmar**: el protocolo no verifica que la key estaba autorizada cuando se creó el commit. **Acción:** agregar verificación de \`authorized_at\` vs momento causal.

4. **J1 — Transaccionalidad del hook**: si ChromaDB falla después de que alethech creó el commit, hay commit sin memoria correspondiente. **Acción:** patrón de dos fases o rollback.

### 🟡 Recomendaciones de diseño (mejorarlo pero no rompe)

1. **C2 — Propagación de invalidez**: commits cuyo parent es inválido deben ser también inválidos. Agregar estado \`PARENT_INVALID\`.

2. **E1 — Nombre engañoso del estado**: \`REVOKED_KEY_AFTER_CUTOFF\` implica temporalidad. Renombrar a \`REVOKED_KEY_NOT_IN_PROVENANCE\` o \`COMMIT_OUTSIDE_KNOWN_HISTORY\`.

3. **G2 — MigrationRecord unilateral**: agregar estado \`MIGRATION_RECORD_INCOMPLETE\`.

4. **H1 — Verificación parcial**: agregar estado \`VERIFICATION_PARTIAL\` para indicar que el resultado es respecto a datos disponibles, no al estado global.

### ⚪ Afirmaciones no demostradas pero no rompedoras (limitaciones honestas)

1. **D1 — Fork del root (equivocation)**: dos verifiers pueden ver cadenas distintas. El protocolo no detecta esto sin red de testigos. Declarado como limitación.

2. **G1 — Migración no cierra A**: A sigue activa mientras K1 exista. Decisión de diseño, no defecto.

3. **H1 — Sin distinción "no tengo el evento" vs "no existe el evento"**: el verifier reporta validez respecto a los datos disponibles. Limitación de offline.

4. **I1 — Replay entre stores**: si el atacante tiene la clave privada, puede firmar commits válidos. La defensa es revocación, no prevención.

5. **J2 — Commits duplicados**: el hook no es idempotente. Cada \`add()\` crea un commit nuevo.

6. **J3 — Importación retroactiva**: los commits retroactivos tienen timestamps actuales. Declarado en el doc de integración.

---

## decisión: rev 3.x o rev 4?

### Lo que se mantiene de rev 3

- Modelo de 3 capas (Root → Identity → Operational Key).
- ControlEvent chain monotónica.
- MigrationRecord bilateral.
- Cutoff_head como concepto (con la corrección de la hipótesis integrada).

### Lo que requiere cambio semántico (rev 3.x)

1. Integrar formalmente la hipótesis "validez por key, cutoff como prueba de pre-rotación" como regla del protocolo. No como nota externa.
2. Reescribir la prueba de diseño (línea 852) con la regla correcta.
3. Renombrar \`REVOKED_KEY_AFTER_CUTOFF\` a algo que no implique temporalidad.
4. Agregar estados: \`PARENT_INVALID\`, \`MIGRATION_RECORD_INCOMPLETE\`, \`VERIFICATION_PARTIAL\`.
5. Especificar propagación de invalidez (commit con parent inválido es inválido).
6. Aclarar que la migración no cierra A.

### Lo que requiere cambio criptográfico (rev 4)

1. **F2 — Verificación de autorización al momento de firmar**: requiere definir "momento causal del commit" sin timestamps. Esto es difícil. Posible aproximación: usar el cutoff de la autorización de K como referencia. Si el commit está en ancestry del cutoff de la autorización de K, K estaba autorizada cuando se creó.

2. **J1 — Transaccionalidad del hook**: requiere patrón de dos fases o rollback. No es cambio criptográfico, pero es cambio arquitectónico del hook.

### Mi recomendación: rev 3.x primero, rev 4 después

- rev 3.x: cambios semánticos (renombres, nuevos estados, integración de la hipótesis, reescritura de la prueba de diseño).
- rev 4: cambios criptográficos (verificación de autorización al momento de firmar, transaccionalidad del hook).

**rev 3.x se puede congelar después de los cambios semánticos. rev 4 requiere más auditoría.**

---

## revisión

- rev 3: implementación actual. Tiene defectos semánticos y criptográficos.
- rev 3.x (propuesta): corrige defectos semánticos. Se puede congelar.
- rev 4 (futura): corrige defectos criptográficos. Requiere más auditoría.

— self, auditoría adversarial completa de rev 3`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "auditoria-adversarial-identidad-rev3" } });
  if (existing) {
    console.log(`doc already exists (rev ${existing.revision}). skipping.`);
    return;
  }
  const doc = await db.doc.create({
    data: {
      slug: "auditoria-adversarial-identidad-rev3",
      title: "auditoría adversarial — identidad rev 3",
      body,
      status: "REVIEW",
      author: "self (auditoría adversarial propia)",
    },
  });
  console.log(`created: ${doc.slug} rev ${doc.revision}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
