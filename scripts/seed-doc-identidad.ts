// Seed doc 6: "arquitectura de identidad" — full identity layer for alethech.
import { db } from "../src/lib/db";

const body = `# arquitectura de identidad

> rev 1 — REVIEW. Diseña la arquitectura de identidad completa de alethech.
> Construye sobre rev 2 del núcleo (que ya tiene \`Identity\` con \`agent_id\`, \`public_key\`, \`key_id\`, \`recovery_root\`) pero formaliza lo que hoy es convención y agrega lo que falta.
>
> Fuera de alcance explícitamente: \`memex\`, MCP, retrieval, runtime autónomo, red, sincronización. La identidad debe poder vivir independientemente del storage y del agente.

## el principio fundamental

> **La clave no es la identidad. La clave es un instrumento criptográfico de una identidad.**

Esto permite:
- rotar una clave operacional sin crear una identidad nueva
- no invalidar el historial anterior al rotar
- revocar una clave sin perder la identidad
- tener múltiples claves para una misma identidad

La identidad es persistente. Las claves son reemplazables.

## el modelo de identidad

Tres capas, en orden de jerarquía:

\`\`\`
┌─────────────────────────────┐
│   ROOT AUTHORITY (recovery) │  ← inmutable para una identidad dada
└──────────────┬──────────────┘
               │ emits
               ▼
┌─────────────────────────────┐
│   IDENTITY (agent_id)       │  ← persistente, vinculada criptográficamente al root
└──────────────┬──────────────┘
               │ authorizes
               ▼
┌─────────────────────────────┐
│   OPERATIONAL KEY (key_id)  │  ← reemplazable, rotable
└─────────────────────────────┘
\`\`\`

### Root Authority

- Un par Ed25519 generado al momento de crear la identidad.
- Solo se usa para: rotar la Identity Key, revocar claves operacionales, autorizar nuevas claves operacionales.
- **No firma commits ni evidence.** Su única función es de governance.
- Se guarda separado del signing key (directorio distinto, ideally con backup offline).
- Si se compromete: la identidad está comprometida. No hay recovery desde root. (Ver sección "Recovery" abajo.)

### Identity (agent_id)

- El \`did:alethech:...\` que ya existe en rev 2.
- Derivado criptográficamente de la **Root Authority public key** (no de la operational key, como en rev 2 actual).
- Es la identidad persistente. No cambia cuando rotamos claves operacionales.
- Cuando alguien verifica un commit, comprueba:
  1. que la firma del commit verifica con la operational key declarada
  2. que esa operational key está autorizada por la identity
  3. que la identity deriva del root authority

### Operational Key (key_id)

- Un par Ed25519 dedicado a firmar MemoryCommits y EvidenceCommits.
- Identificado por \`key_id\` (ej: \`key-001\`, \`key-002\`).
- Reemplazable. La rotación no rompe el historial.
- Puede haber múltiples activas simultáneamente (para casos como: una para desarrollo, una para producción, una para agentes externos delegados).

## estructuras de datos

### RootAuthority

\`\`\`json
{
  "type": "RootAuthority",
  "version": 1,
  "root_id": "did:alethech:root:<base32(sha256(root_public_jwk)[0:16])>",
  "root_public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url>" },
  "created_at": "2026-09-26T...",
  "recovery_quorum": {
    "type": "single" | "multisig" | "external",
    "threshold": 1,
    "members": ["did:alethech:root:..."]
  }
}
\`\`\`

Notas:
- \`root_id\` se deriva de la root public key (mismo algoritmo que agent_id).
- \`recovery_quorum\` describe cómo se recupera el root si se pierde. En rev 1 es siempre \`single\` (un solo root key). En rev 2+ se podrá tener multisig.

### IdentityRecord (extiende Identity de rev 2)

\`\`\`json
{
  "type": "Identity",
  "version": 2,
  "agent_id": "did:alethech:<base32(sha256(root_public_jwk)[0:16])>",
  "root_id": "did:alethech:root:<base32(sha256(root_public_jwk)[0:16])>",
  "root_public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url>" },
  "active_keys": [
    {
      "key_id": "key-001",
      "public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url>" },
      "authorized_at": "2026-09-26T...",
      "authorized_by": "root_signature:<base64url>",
      "expires_at": null,
      "revoked_at": null
    }
  ],
  "revoked_keys": [],
  "created_at": "2026-09-26T...",
  "recovery_root": "<base64url of root public key>"
}
\`\`\`

Cambios respecto a rev 2:
- \`agent_id\` ahora se deriva del **root_public_key**, no de la operational key. Esto desacopla identidad de clave operacional.
- \`active_keys\` es una lista (no un solo \`key_id\`).
- Cada key tiene \`authorized_by\` = firma del root authority que la autorizó.
- \`revoked_keys\` permite revocación sin perder historial.

### KeyAuthorization (objeto firmable)

Cuando el root authority autoriza una nueva operational key, emite un objeto firmado:

\`\`\`json
{
  "type": "KeyAuthorization",
  "version": 1,
  "commit_id": "sha256:...",
  "root_id": "did:alethech:root:...",
  "key_id": "key-002",
  "public_key": { "kty": "OKP", "crv": "Ed25519", "x": "<base64url>" },
  "action": "authorize" | "revoke",
  "reason": "rotation" | "compromise" | "expiry",
  "timestamp": "2026-09-26T...",
  "expires_at": null,
  "signature": "ed25519:<base64url>"  // firma del root authority
}
\`\`\`

Este objeto se almacena en \`.alethech/key_authorizations/<commit_id>.json\` y es verificable offline.

## rotación de claves

### Procedimiento normal (rotación programada)

\`\`\`bash
alethech key rotate --reason rotation
\`\`\`

Pasos:
1. Genera nuevo par Ed25519 (será \`key-002\`).
2. Construye \`KeyAuthorization\` con \`action=authorize\`, \`reason=rotation\`.
3. Lo firma con el **root authority private key**.
4. Construye \`KeyAuthorization\` con \`action=revoke\`, \`reason=rotation\` para \`key-001\`.
5. Lo firma con el root authority.
6. Actualiza \`IdentityRecord\`: mueve \`key-001\` a \`revoked_keys\`, agrega \`key-002\` a \`active_keys\`.
7. Guarda el nuevo signing key en \`.alethech/keys/signing-key-002.key\`.
8. NO toca commits existentes — siguen firmados con \`key-001\`, que sigue siendo verificable.

### Verificación de commits después de rotación

Cuando \`alethech verify\` encuentra un commit firmado con \`key-001\`:
1. Busca \`key-001\` en \`IdentityRecord.active_keys\` → no está.
2. Busca en \`IdentityRecord.revoked_keys\` → está, con \`revoked_at\` y \`reason=rotation\`.
3. Verifica que el commit fue firmado **antes** de \`revoked_at\`. Si sí, es válido.
4. Si el commit fue firmado **después** de \`revoked_at\`, marca como \`signature_invalid: key revoked before signing\`.

Esto preserva el historial: los commits viejos siguen siendo verificables, los nuevos requieren la nueva clave.

## revocación de emergencia

Si una clave se compromete:

\`\`\`bash
alethech key revoke --key-id key-002 --reason compromise
\`\`\`

Pasos:
1. Construye \`KeyAuthorization\` con \`action=revoke\`, \`reason=compromise\`.
2. Lo firma con el root authority.
3. Mueve \`key-002\` de \`active_keys\` a \`revoked_keys\` con \`revoked_at=now\`.
4. **NO genera una nueva clave automáticamente** — eso requiere intervención humana para evitar que el atacante que comprometió key-002 también comprometa key-003.
5. El humano debe generar key-003 manualmente con \`alethech key authorize --new\` después de asegurarse que el entorno está limpio.

### Commits firmados después de la revocación de emergencia

Cualquier commit firmado con \`key-002\` después de \`revoked_at\` se considera **inválido**. \`alethech verify\` lo marcará como \`signature_invalid: key compromised\`.

Esto es correcto. Si el atacante tiene la clave, puede firmar commits falsos. El protocolo no puede distinguir "commits reales hechos con key-002 antes del compromiso" de "commits falsos hechos por el atacante después del compromiso" — salvo por el timestamp.

Por eso \`revoked_at\` debe ser lo más temprano posible: idealmente el momento en que se detectó el compromiso, no el momento en que se revocó formalmente. Si hay dudas, se puede usar un timestamp anterior.

## recovery ante pérdida o compromiso

### Caso 1: pérdida de operational key

- El root authority sigue intacto.
- Procedimiento: \`alethech key authorize --new\` con el root authority.
- Genera key-003, autoriza, actualiza \`IdentityRecord\`.
- No se pierde nada de la historia.

### Caso 2: compromiso de operational key

- El atacante puede firmar commits falsos hasta que revocamos.
- Procedimiento: \`alethech key revoke --reason compromise\` inmediatamente.
- Luego \`alethech key authorize --new\` desde un entorno limpio.
- Los commits firmados entre el compromiso y la revocación son indistinguibles. Si se sabe cuándo se comprometió, marcar \`revoked_at\` en ese momento.

### Caso 3: pérdida del root authority

- Esto es grave. Sin el root, no se puede autorizar nuevas operational keys ni revocar las existentes.
- **La identidad está congelada.** Los commits existentes siguen siendo verificables (las operational keys no se pierden), pero no se pueden rotar ni revocar.
- Recovery real: requiere \`recovery_quorum\` con multisig (rev 2+ del documento de identidad). En rev 1, si se pierde el root, la identidad está efectivamente muerta para nuevas operaciones.

### Caso 4: compromiso del root authority

- Esto es lo peor. El atacante puede autorizar claves nuevas, revocar las legítimas, y tomar control total de la identidad.
- **No hay recovery criptográfico.** La identidad está completamente comprometida.
- Lo único que se puede hacer: publicar una alerta de "identidad comprometida" en los canales de publicación (\`.well-known\`, DNS TXT, etc.) y crear una identidad nueva con un nuevo root authority.
- Los commits antiguos siguen siendo verificables criptográficamente, pero ya no se puede confiar en que futuros commits provengan del agente legítimo.

Esto es una limitación fundamental. Sin multisig o mecanismo externo, un compromiso del root es terminal. Por eso el root authority debe estar en el lugar más seguro posible — ideally offline, en hardware dedicado.

## publicación de la identidad

Para que terceros puedan verificar commits de un agente, necesitan conocer su public key. Opciones:

### Opción 1: \`.well-known/alethech/identity.json\`

Si el agente tiene un dominio (cuando consigamos los dominios \`alethech.io\` etc.), publica:

\`\`\`
GET https://alethech.io/.well-known/alethech/identity.json
\`\`\`

Respuesta: el \`IdentityRecord\` completo. Cualquiera puede descargarlo y verificar commits.

### Opción 2: DNS TXT record

\`\`\`
alethech.io.  IN  TXT  "alethech-agent-id=did:alethech:abc123..."
alethech.io.  IN  TXT  "alethech-root-key=ed25519:..."
\`\`\`

Más ligero que HTTP, pero limita el tamaño. Útil para lookup rápido del \`agent_id\`.

### Opción 3: GitHub gist o repo

\`\`\`
https://gist.github.com/<user>/raw/<id>/alethech-identity.json
\`\`\`

Útil si el agente no tiene dominio propio todavía.

### Opción 4: IPFS / content-addressable

\`\`\`
ipfs://<cid>/alethech-identity.json
\`\`\`

Para casos donde la inmutabilidad importe más que la actualizabilidad. Requiere publicación periódica del CID más reciente en algún canal lookup-able.

### Formato del documento publicado

\`\`\`json
{
  "type": "AlethechIdentityPublication",
  "version": 1,
  "identity": { /* IdentityRecord completo */ },
  "published_at": "2026-09-26T...",
  "publication_signature": "ed25519:..."  // firma del root authority
}
\`\`\`

La firma del root authority prueba que la publicación es autorizada, no modificada por el operador del dominio.

### Verificación cruzada

Un verificador externo puede:
1. Descargar la identidad desde múltiples canales (well-known + DNS + gist).
2. Verificar que todas coinciden.
3. Si no coinciden: alguien está presentando identidades distintas a receptores distintos (equivocation).

Esto conecta con la detección de equivocation del spec rev 2.

## wallet múltiple

Un agente puede tener múltiples identidades para contextos distintos:

\`\`\`bash
alethech identity list
\`\`\`

\`\`\`
did:alethech:abc123...  (default, key-001 active)
did:alethech:def456...  (work identity, key-002 active)
did:alethech:ghi789...  (experimental, key-001 active)
\`\`\`

Implementación:
- \`.alethech/identities/<agent_id>/\` en lugar del archivo único actual.
- Cada identidad tiene su propio \`IdentityRecord\`, sus propias claves, su propio \`HEAD\`.
- El flag \`--identity\` en comandos permite elegir qué identidad usar.
- Default: la primera identidad creada, o la marcada como \`default\` con \`alethech identity default <agent_id>\`.

### Casos de uso

- Una identidad para commits públicos (visible en el sitio).
- Una identidad para trabajo con un cliente específico (datos privados).
- Una identidad para experimentos (que se puede descartar sin afectar la principal).

## relación con el protocolo rev 2

Esto es compatible con el núcleo aprobado:

- \`MemoryCommit\` y \`EvidenceCommit\` siguen teniendo \`agent_id\` y \`key_id\`. Sin cambios.
- \`verify\` agrega un paso más: verificar que la \`key_id\` declarada está (o estuvo) autorizada por la identidad correspondiente.
- Los commits existentes firmados con \`key-001\` siguen siendo válidos si \`key-001\` está en \`active_keys\` o \`revoked_keys\` con \`revoked_at\` posterior al timestamp del commit.

### Cambios a \`alethech verify\`

Pasos adicionales después de verificar firma:

7. **Verificar autorización de key**:
   - Para cada commit, buscar \`key_id\` en \`IdentityRecord.active_keys\`.
   - Si está: OK.
   - Si no está, buscar en \`revoked_keys\`.
   - Si está revocada: verificar que el commit fue firmado **antes** de \`revoked_at\`. Si no, marcar como \`signature_invalid: key revoked before signing\`.
   - Si no está ni en \`active_keys\` ni en \`revoked_keys\`: marcar como \`unknown_key\`.

8. **Verificar autorización de la key por el root**:
   - Para cada \`active_key\`, buscar su \`KeyAuthorization\` correspondiente.
   - Verificar la firma del root authority sobre la autorización.

## migración desde alethech init actual

El \`alethech init\` actual (rev 2 spec):
- Genera un par signing + un par recovery.
- Crea \`Identity\` con \`key_id="key-001"\`.
- \`recovery_root\` es un string base64url pero no se usa.

Para migrar a rev 1 (este documento):

### Procedimiento automático

\`\`\`bash
alethech migrate --from v0.1 --to v0.2
\`\`\`

Pasos:
1. Lee el \`Identity\` actual (formato rev 2).
2. Identifica el \`recovery_root\` como la root_public_key.
3. Construye nuevo \`RootAuthority\` derivando \`root_id\` de esa public key.
4. Construye nuevo \`IdentityRecord\` con:
   - \`agent_id\` recalculado a partir del root (puede cambiar — eso requiere decisión explícita).
   - \`root_id\` nuevo.
   - \`active_keys\` = [\`key-001\` actual, con \`authorized_by\` firmado por el root].
5. Construye \`KeyAuthorization\` retroactiva: el root autoriza a \`key-001\`.
6. Guarda todo.

### Decisión sobre \`agent_id\`

Hay una tensión: en rev 2, \`agent_id\` deriva de la operational key. En este doc (rev 1), deriva del root.

Opciones:
- **A. Mantener agent_id actual** (derivado de operational key). Requiere cambiar el algoritmo de derivación para que use el root en nuevas identidades, pero las existentes conservan su agent_id.
- **B. Recalcular agent_id** desde el root. Esto cambia la identidad de commits existentes, lo que rompe verificación.

Recomendación: **A**. Mantener agent_id actual para identidades existentes. Las nuevas identidades creadas con \`alethech init v0.2+\` usan derivación desde root.

Eso significa que hay dos clases de identidades:
- v0.1 identities: agent_id deriva de operational key (legacy).
- v0.2+ identities: agent_id deriva de root authority.

\`verify\` maneja ambos casos mirando el campo \`version\` del \`IdentityRecord\`.

## qué significa "identidad verificable"

Después de este documento, "identidad verificable" significa:

1. **Identidad persistente**: el \`agent_id\` no cambia al rotar claves.
2. **Autoría criptográfica**: cada commit está firmado por una clave específica, vinculada a la identidad.
3. **Autorización verificable**: cada operational key tiene una \`KeyAuthorization\` firmada por el root.
4. **Rotación no destructiva**: los commits antiguos siguen siendo verificables después de rotar.
5. **Revocación detectable**: commits firmados con claves revocadas se detectan como inválidos.
6. **Publicación cruzada**: la identidad puede publicarse en múltiples canales para verificación externa.
7. **Recovery parcial**: pérdida de operational key se recupera. Compromiso del root es terminal.

## qué NO significa "identidad verificable"

- No prueba que el agente sea confiable.
- No prueba que los contenidos de los commits sean verdaderos.
- No prueba que el operador del dominio donde se publica la identidad no la haya modificado (salvo verificación cruzada).
- No protege contra compromiso del root authority.
- No requiere o provee consenso distribuido.

## tests mínimos

1. Crear identidad v0.2, firmar commit con key-001, rotar a key-002, firmar commit con key-002. Verificar ambos pasan.
2. Revocar key-001, verificar commit firmado antes de revocación sigue válido.
3. Revocar key-001, verificar commit firmado después de revocación es inválido.
4. Autorizar key-002 sin firma del root → \`unknown_key\`.
5. Migrar identidad v0.1 a v0.2 manteniendo agent_id → pasa \`verify\`.
6. Migrar identidad v0.1 a v0.2, firmar commit nuevo con key-001 autorizada por root retroactivamente → pasa.
7. Publicar identidad en \`.well-known/alethech/identity.json\`, descargar desde otro cliente, verificar firma de publicación.
8. Publicar dos identidades distintas en dos canales → detectar \`equivocation\` (no implementado en rev 1, pero spec está).
9. Crear segunda identidad en mismo store (\`alethech identity create --name work\`), listar identidades, usar \`--identity\` para elegir.
10. Comprometer root (simulación: borrar \`recovery.key\`), intentar autorizar nueva key → falla con \`root_unavailable\`.

## límites y amenazas

### Lo que el protocolo NO puede resolver

1. **Compromiso del root authority**: como dije, es terminal. Sin multisig o mecanismo externo, no hay recovery.
2. **Compromiso silencioso**: si el atacante usa la clave comprometida pero nadie se da cuenta, los commits firmados se ven legítimos. \`alethech verify\` no detecta ataques que aún no se han descubierto.
3. **Equivocation no detectada**: si un agente presenta identidades distintas a receptores distintos y los receptores nunca comparan, \`alethech verify\` no puede saber. Requiere observación cruzada.
4. **Ataques al canal de publicación**: si alguien compromete el dominio donde se publica la identidad, puede publicar una identidad falsa. La firma del root authority en la publicación mitiga esto, pero requiere que el verificador conozca el root de antemano (chicken-and-egg hasta que exista un web of trust).

### Lo que el protocolo SÍ resuelve

1. **Rotación no destructiva**: el caso de uso más importante. Las claves se rotan, el historial sobrevive.
2. **Revocación explícita**: cuando se descubre un compromiso, se puede marcar el momento exacto y detectar commits falsos posteriores.
3. **Autoría criptográfica**: cada commit está firmado por una clave específica, vinculada a una identidad, autorizada por un root.
4. **Verificación offline**: toda la verificación se hace con datos públicos (IdentityRecord + KeyAuthorizations + commits). Sin red, sin LLM, sin servicios externos.

## lo que queda fuera de rev 1 (para rev 2+)

- Multisig en el root authority (\`recovery_quorum\` con \`threshold > 1\`).
- Detección automática de equivocation vía red de testigos.
- Publicación en blockchain (timestamping periódico del HEAD).
- Delegación de identidad (un agente actuando en nombre de otro).
- Identidad socialmente recuperable ( amigos firmantes de rotación).
- Hardware-backed keys (TPM, YubiKey, smart cards).
- Sistema de reputación vinculado a la identidad.

## compatibilidad con rev 2 del núcleo

Sin cambios estructurales:

- \`MemoryCommit\` y \`EvidenceCommit\` no cambian. Tienen \`agent_id\` y \`key_id\` como antes.
- \`Checkpoint\` no cambia.
- \`verify\` agrega pasos 7 y 8 (verificación de autorización de key). Es aditivo.
- \`init\` cambia: genera root + operational, no solo signing + recovery.
- \`commit\` y \`evidence\` no cambian desde el punto de vista del usuario. Internamente, \`key_id\` puede ser \`key-002\` después de una rotación, pero el comando no lo expone.
- \`export\` y \`import\` ahora incluyen \`RootAuthority\` y \`KeyAuthorizations\` en el paquete.

## implementación mínima

Para rev 1 de este documento:

- Nuevo comando: \`alethech key rotate\`
- Nuevo comando: \`alethech key revoke\`
- Nuevo comando: \`alethech key authorize\` (manual, para casos especiales)
- Nuevo comando: \`alethech identity list\`
- Nuevo comando: \`alethech identity create\` (multiple wallets)
- Nuevo comando: \`alethech identity publish\` (genera archivo para \`.well-known\`)
- Nuevo comando: \`alethech migrate --from v0.1 --to v0.2\`
- Cambios en \`alethech init\`: ahora genera root + operational.
- Cambios en \`alethech verify\`: agrega pasos 7 y 8.
- Nuevo objeto: \`RootAuthority\`, \`IdentityRecord v2\`, \`KeyAuthorization\`.

Tests:
- Los 10 tests mínimos de arriba.
- Migración: identidad v0.1 migrada a v0.2 pasa \`verify\`.
- Roundtrip: init v0.2 → commit → rotate → commit → verify pasa.
- Publicación: init v0.2 → publish → descargar en cliente B → verify pasa.

## revisión

- rev 1 (actual): especificación inicial. REVIEW. Pendiente de aprobación del humano.
- rev 2 (futura): después de implementar y encontrar casos límite.

— self, revisión 1 (arquitectura de identidad completa)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (existing) {
    console.log(`doc already exists (rev ${existing.revision}). skipping.`);
    return;
  }

  const doc = await db.doc.create({
    data: {
      slug: "arquitectura-identidad",
      title: "arquitectura de identidad",
      body,
      status: "REVIEW",
      author: "self",
    },
  });
  console.log(`created: ${doc.slug} rev ${doc.revision}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
