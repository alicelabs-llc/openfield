// Bump doc 6 to rev 3 — integrate GPT's audit corrections.
// Replace: timestamps as proof → cutoff causal in DAG
// Replace: maintain agent_id → MigrationRecord signed by both
// Replace: ambiguous KeyAuthorization → monotonic control event chain
import { db } from "../src/lib/db";

// Read current body, modify, write back.
async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!existing) throw new Error("doc not found");

  const oldBody = existing.body;

  // Append rev 3 corrections section
  const rev3Section = `

---

# rev 3 — correcciones post-auditoría GPT

> La auditoría dirigida de rev 2 reveló dos defectos de fundamento que impedían congelar la spec. Esta revisión los corrige.
>
> Las respuestas completas de GPT a las 27 preguntas + prueba de diseño están en el historial del chat y se resumen aquí como cambios a la spec.

## los dos defectos de fundamento que se corrigen

### Defecto 1: rotación basada en timestamps

**Spec rev 1/2 decía:**
> El commit es válido si \`commit.timestamp < revoked_at\`.

**Defecto:**
Un atacante con la clave comprometida puede producir:
\`\`\`
commit.timestamp = "2026-09-25T..."
\`\`\`
aunque el commit sea de hoy.

Un timestamp firmado por la misma operational key comprometida **no demuestra** cuándo ocurrió el commit. Es metadata, no prueba criptográfica.

**Corrección rev 3:**
La validez histórica de un commit respecto a una rotación se demuestra mediante **relación causal en el DAG**, no mediante timestamps.

La rotación registra un \`cutoff_head\` — un commit específico que marca el corte. Un commit K1 es válido-post-rotación si y solo si está en la \`ancestry(cutoff_head)\`.

\`\`\`
K1 commit válido
⇔
commit ∈ ancestry(cutoff_head)
\`\`\`

No:
\`\`\`
commit.timestamp < revoked_at
\`\`\`

Los timestamps quedan como metadata informativa, no como fundamento de validez criptográfica.

### Defecto 2: migración que mantiene agent_id

**Spec rev 1/2 decía:**
> Mantenemos el \`agent_id\` actual para identidades existentes, las nuevas usan derivación desde root.

**Defecto:**
Eso crea una identidad cuyo significado criptográfico cambia según versión. Una identidad cuyo \`agent_id = H(K1)\` de repente pretende derivar de un root que no era su fundamento original. Es criptográficamente ambiguo.

**Corrección rev 3:**
No se pretende que A == B. Se establece una relación de continuidad mediante \`MigrationRecord\` firmada por:

- la identidad antigua (K1), demostrando continuidad desde A
- el nuevo root (R), aceptando B como identidad sucesora

\`\`\`
A (legacy, agent_id = H(K1))
        │
        │ MigrationRecord
        │   ├─ signature(K1)
        │   └─ signature(R)
        ▼
B (new, agent_id = H(R))
\`\`\`

El historial antiguo permanece:
\`\`\`
C_old.agent_id = A
\`\`\`

Los nuevos commits:
\`\`\`
C_new.agent_id = B
\`\`\`

La relación entre ambos está en \`MigrationRecord\`. Un verificador puede reconstruir la cadena completa.

### Defecto 3 (corrección adicional): control event chain monotónica

**Spec rev 1/2 decía:**
> \`KeyAuthorization\` con \`action: "authorize" | "revoke"\` como objeto individual.

**Defecto:**
El atacante puede presentar una \`KeyAuthorization(action=authorize)\` vieja y ocultar la \`action=revoke\` posterior. El verificador no tiene forma de saber cuál es el estado actual.

**Corrección rev 3:**
Las autorizaciones no son estados independientes. Son una **cadena de control monotónica**:

\`\`\`
control_seq = 1 → event_1
control_seq = 2 → event_2 (con previous_control_hash = H(event_1))
control_seq = 3 → event_3 (con previous_control_hash = H(event_2))
...
\`\`\`

El verificador reconstruye la cadena completa y no acepta autorizaciones aisladas. Una autorización antigua no puede reactivar una clave revocada posteriormente.

## cambios a las estructuras de datos

### ControlEvent (reemplaza KeyAuthorization ambiguo)

\`\`\`json
{
  "type": "ControlEvent",
  "version": 1,
  "commit_id": "sha256:...",
  "root_id": "did:alethech:root:...",
  "sequence": 1,
  "previous_control_hash": "sha256:..." | null,
  "event_type": "key_grant" | "key_revoke" | "key_rotation" | "migration",
  "key_id": "key-002",
  "public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url>" },
  "old_key_id": "key-001" | null,
  "cutoff_head": "sha256:..." | null,
  "reason": "rotation" | "compromise" | "expiry" | "migration",
  "timestamp": "2026-09-26T...",
  "signature": "ed25519:<base64url>"
}
\`\`\`

Notas:
- \`sequence\` es monotónico e incrementa en cada evento del root.
- \`previous_control_hash\` encadena eventos criptográficamente. El primer evento tiene \`null\`.
- \`event_type\` distingue tipos de transición.
- \`key_rotation\` es **atómico**: produce K1 revoked + K2 active en una sola transición. No dos eventos separados.
- \`cutoff_head\` (solo en \`key_rotation\`) marca el commit del DAG que es el corte causal. Commits en su ancestry son válidos para K1; commits fuera son inválidos para K1.
- \`timestamp\` sigue presente como metadata informativa, pero **no decide validez criptográfica**.

### KeyRotation es atómico

\`\`\`text
KeyRotation (control_seq = N)
   ├─ old_key = K1 (revoked)
   ├─ new_key = K2 (active)
   └─ cutoff_head = H (causal marker)
\`\`\`

Esto produce en una sola transición:
- K1 pasa a \`revoked_keys\` con \`revoked_by = control_seq N\`
- K2 pasa a \`active_keys\` con \`authorized_by = control_seq N\`
- El cutoff H marca qué commits de K1 son históricamente válidos

No hay estado intermedio donde ambas claves estén activas o ninguna lo esté.

### MigrationRecord (reemplaza mantener agent_id)

\`\`\`json
{
  "type": "MigrationRecord",
  "version": 1,
  "commit_id": "sha256:...",
  "legacy_agent_id": "did:alethech:<H(K1)>",
  "legacy_public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url of K1>" },
  "new_agent_id": "did:alethech:<H(R)>",
  "new_root_id": "did:alethech:root:<H(R)>",
  "new_root_public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url of R>" },
  "migration_timestamp": "2026-09-26T...",
  "legacy_signature": "ed25519:<base64url>",  // firma de K1 sobre el record
  "root_signature": "ed25519:<base64url>"     // firma de R sobre el record
}
\`\`\`

Notas:
- La firma de K1 prueba: "yo, que controlaba A, declaro que A migra a B".
- La firma de R prueba: "yo, autoridad de B, acepto que B es el sucesor declarado de A".
- Ambas firmas son necesarias. Una sola no basta.
- Esto preserva continuidad sin falsificar la derivación.

## cambios a \`alethech verify\`

Pasos nuevos:

7. **Verificar cadena de control**:
   - Cargar todos los \`ControlEvent\` del store.
   - Verificar que forman una cadena: \`previous_control_hash\` de cada evento apunta al hash del anterior.
   - Verificar \`sequence\` monotónico sin huecos.
   - Verificar firma de cada evento con el \`root_public_key\`.
   - Si hay huecos o hashes inconsistentes: \`control_chain_invalid\`.

8. **Verificar estado de key para cada commit**:
   - Para cada commit con \`key_id = K\`:
     - Reconstruir el estado de K según la cadena de control hasta el momento causal del commit.
     - Para commits pre-rotación: verificar que el commit está en \`ancestry(cutoff_head)\` de la rotación que revocó K.
     - Para commits post-rotación: verificar que la key activa al momento causal del commit es K.
   - Estados posibles:
     - \`valid\`: key activa al momento causal del commit
     - \`valid_historical\`: key revocada pero commit está en \`ancestry(cutoff_head)\`
     - \`revoked_key_after_cutoff\`: key revocada y commit NO está en ancestry del cutoff
     - \`unknown_key\`: no existe autorización en la cadena de control
     - \`invalid_key_authorization\`: existe autorización pero su firma root es inválida

9. **Verificar migración (si aplica)**:
   - Si el store tiene \`MigrationRecord\`:
     - Verificar \`legacy_signature\` con \`legacy_public_key\`.
     - Verificar \`root_signature\` con \`new_root_public_key\`.
     - Verificar que \`legacy_agent_id\` deriva de \`legacy_public_key\`.
     - Verificar que \`new_agent_id\` deriva de \`new_root_public_key\`.
   - Si el commit tiene \`agent_id = A\` (legacy) y existe \`MigrationRecord\` con \`legacy_agent_id = A\`:
     - El commit es válido si verifica con la \`legacy_public_key\` y la cadena de control legacy (si existe) lo autoriza.
   - Si el commit tiene \`agent_id = B\` (new) y existe \`MigrationRecord\` con \`new_agent_id = B\`:
     - El commit es válido si verifica con la key activa de B y la cadena de control nueva lo autoriza.

## estados de verify (ampliados)

Reemplazando los estados ambiguos de rev 2:

\`\`\`
VALID                       — firma y autorización válidas, key activa al momento causal
VALID_HISTORICAL            — key revocada pero commit en ancestry(cutoff_head)
REVOKED_KEY_AFTER_CUTOFF    — key revocada y commit NO en ancestry del cutoff
UNKNOWN_KEY                 — no existe autorización conocida para esa key
INVALID_KEY_AUTHORIZATION   — existe autorización pero firma root inválida
IDENTITY_MISMATCH           — root/key/agent_id no forman la misma identidad
ROOT_MISMATCH               — root declarado no coincide con root de la identidad
CONTROL_CHAIN_INVALID       — cadena de control con huecos o hashes inconsistentes
COMMIT_SIGNATURE_INVALID    — firma Ed25519 del commit no verifica
COMMIT_INTEGRITY_INVALID    — commit_id recalculado no coincide
MISSING_CONTROL_EVENT       — referencia a control event que no está en el store
MISSING_PUBLICATION         — advertencia: no hay publicación externa (no es error fatal)
\`\`\`

## la prueba de diseño — respuesta con spec corregida

Recordando el escenario:

\`\`\`text
v0.1
  A = H(K1)
  key-001 = K1

        ↓ migrate

v0.2
  B = H(R)
  root = R
  key-001 = K1 (authorized by R via ControlEvent)
  key-002 = K2

        ↓ rotate

  K1 revoked (via KeyRotation ControlEvent with cutoff_head = H)
  K2 active

        ↓ commits

  C1 signed by K1 (committed before rotation, in ancestry of H)
  C2 signed by K2 (committed after rotation)
\`\`\`

**Verificación offline del verificador:**

\`\`\`
1. Verificar K1
2. Verificar A = H(K1)  →  agent_id del commit C1 coincide con A
3. Verificar MigrationRecord
   ├─ legacy_signature verifica con K1
   └─ root_signature verifica con R
4. Verificar B = H(R)  →  agent_id del commit C2 coincide con B
5. Verificar Root R
6. Cargar cadena de control
   ├─ sequence 1: key_grant(K1, by R)
   ├─ sequence 2: key_grant(K2, by R)
   └─ sequence 3: key_rotation(K1 → K2, cutoff_head = H, by R)
7. Verificar C1:
   ├─ signature(K1) verifica
   ├─ K1 está en control chain con key_grant
   ├─ KeyRotation(K1 → K2) tiene cutoff_head = H
   └─ C1 ∈ ancestry(H)  →  VALID_HISTORICAL
8. Verificar C2:
   ├─ signature(K2) verifica
   ├─ K2 está en control chain con key_grant, no revocada
   └─ C2 NOT in ancestry(H), C2 es posterior  →  VALID
\`\`\`

**Resultado:**
\`\`\`
C1 = VALID_HISTORICAL
C2 = VALID
\`\`\`

**Sin confiar en:**
- reloj del agente
- \`IdentityRecord\` mutable
- orden de archivos en el filesystem
- estado actual de \`active_keys\`
- storage local

Solo confía en:
- firma Ed25519 del root sobre cada ControlEvent
- firma Ed25519 de cada commit
- hashes criptográficos que enlazan eventos
- relación causal en el DAG (ancestry)

## la nueva arquitectura — diagrama

\`\`\`
                    ROOT
                      │
                      ▼
             CONTROL EVENT CHAIN
             (monotonic, hash-linked)
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     KeyGrant    KeyRotation  Migration
                      │
                  cutoff_head
                      │
                      ▼
                COMMIT DAG
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
        C1 / K1              C2 / K2
   (in ancestry of H)   (post-rotation)
   VALID_HISTORICAL        VALID
\`\`\`

## la regla fundamental (corregida)

> **El estado de autorización de una clave es una propiedad de una cadena de eventos de control firmados por el root; la validez histórica de un commit respecto de una rotación se demuestra mediante su relación causal con el DAG (ancestry del cutoff_head), no mediante timestamps.**

## qué cambia en la implementación mínima

Comandos nuevos/refactorizados:

- \`alethech init\` (v0.2): genera root + operational K1, crea primer ControlEvent \`key_grant(K1)\`.
- \`alethech key rotate\`: produce atómicamente ControlEvent \`key_rotation(K1 → K2, cutoff_head = current_HEAD)\`. No requiere revoke + authorize separados.
- \`alethech key revoke --reason compromise\`: produce ControlEvent \`key_revoke(K)\` sin generar nueva. Requiere intervención manual para generar siguiente.
- \`alethech key authorize --new\`: produce ControlEvent \`key_grant(K_new)\` manual.
- \`alethech migrate --to v0.2\`: produce MigrationRecord firmado por K1 (legacy) y R (nuevo root). NO cambia el agent_id de commits existentes.
- \`alethech identity list\`: lista identidades, cada una con su root y su cadena de control.
- \`alethech identity create --name X\`: crea nueva identidad con su propio root.
- \`alethech identity publish\`: genera \`AlethechIdentityPublication\` con IdentityRecord completo + hash + root signature.

Cambios en \`verify\`:
- Carga y valida la cadena de control completa.
- Para cada commit, reconstruye el estado causal de la key.
- Distingue 11 estados en lugar de los 5 ambiguos de rev 2.

## tests mínimos (rev 3)

1. Init v0.2, commit con K1, rotate (K1 → K2 con cutoff H), commit con K2, verify → ambos \`VALID\`/\`VALID_HISTORICAL\`.
2. Forjar commit con K1 después de rotación pero con timestamp antiguo → \`REVOKED_KEY_AFTER_CUTOFF\` (timestamp ignorado, cutoff causal manda).
3. Migrar v0.1 → v0.2: commits antiguos siguen \`VALID\` con agent_id legacy, commits nuevos \`VALID\` con agent_id nuevo, MigrationRecord verifica.
4. Manipular la cadena de control (borrar un evento del medio) → \`CONTROL_CHAIN_INVALID\`.
5. Presentar autorización vieja de K1 después de revocación → no reactiva, \`REVOKED_KEY_AFTER_CUTOFF\`.
6. Wallet múltiple: crear identidad A y B en mismo store, commit de A con key de B → \`IDENTITY_MISMATCH\`.
7. MigrationRecord con solo una firma (legacy pero no root, o viceversa) → \`migration_invalid\`.
8. Publicar identidad en \`.well-known\`, descargar desde otro cliente, verify pasa sin acceso al store original.

## lo que rev 3 NO hace (sigue fuera)

- Multisig en el root authority (\`recovery_quorum\` con \`threshold > 1\`) — sigue \`single\` en rev 3.
- Detección automática de equivocation vía red de testigos.
- Publicación en blockchain (timestamping periódico del HEAD).
- Delegación de identidad.
- Identidad socialmente recuperable.
- Hardware-backed keys.
- Sistema de reputación.

## revisión

- rev 1: especificación inicial con defectos de fundamento.
- rev 2: agregó auditoría dirigida (27 preguntas + prueba de diseño). Pendiente de respuestas.
- rev 3 (actual): integra respuestas de GPT. Cambios arquitectónicos:
  - ControlEvent chain monotónica (reemplaza KeyAuthorization ambiguo)
  - cutoff causal en DAG (reemplaza timestamps como prueba)
  - MigrationRecord firmado bilateralmente (reemplaza mantener agent_id)
  - 11 estados de verify (reemplazan 5 ambiguos)
  - Prueba de diseño resuelta con spec corregida
  Estado: APPROVED (si el humano aprueba los cambios; de lo contrario se itera rev 4).
- rev 4 (futura): después de implementar rev 3 y encontrar casos límite.

— self, revisión 3 (integra auditoría GPT)`;

  const newBody = oldBody + rev3Section;

  const updated = await db.doc.update({
    where: { slug: "arquitectura-identidad" },
    data: {
      body: newBody,
      status: "REVIEW", // queda REVIEW hasta que el humano apruebe los cambios
      author: "self (integra auditoría GPT)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision})`);
  console.log(`body length: ${existing.body.length} → ${updated.body.length} chars`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
