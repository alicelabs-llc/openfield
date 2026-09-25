// Replace doc 4 with the GPT technical architecture version.
// The previous rev 1 (my narrative version) is preserved as ARCHIVED rev 0.
import { db } from "../src/lib/db";

const newBody = `# arquitectura de confianza entre agentes

> Este documento es la versión técnica formal del protocolo de continuidad verificable para agentes.
> Reemplaza la versión anterior (rev 1, narrativa) que archivamos como insuficiente.
> Origen: refinado en conversación entre el humano y GPT, integrado por self.
> Estado actual: REVIEW — esperando respuestas de GPT a las 12 preguntas difíciles + la pregunta final.

## el problema técnico

MEMEX no debe definirse simplemente como "agent memory".

El problema que queremos resolver es:

> **¿Cómo puede un agente conservar continuidad, contexto, experiencia y conocimiento a través del tiempo y entre diferentes agentes, sin tener que confiar ciegamente en el agente, el almacenamiento, el proveedor de IA o un servidor central?**

El sistema debe permitir:

- persistencia local
- funcionamiento offline
- múltiples agentes
- identidad criptográfica
- memoria verificable
- evidencia/proveniencia
- historial inmutable o detectable ante modificaciones
- handoff entre agentes
- sincronización
- branching/merging
- recuperación ante pérdida de claves
- revocación
- almacenamiento local, cloud o P2P
- proveedores externos de confianza opcionales

La capa de memoria **no debe depender de un LLM** para garantizar integridad, autenticidad o continuidad.

## separar cinco conceptos

Una parte fundamental de la arquitectura debería ser separar explícitamente:

\`\`\`text
IDENTITY
   ↓
INTEGRITY
   ↓
PROVENANCE / EVIDENCE
   ↓
TRUST POLICY
   ↓
AUTHORIZATION
   ↓
ACTION
\`\`\`

No deberían mezclarse.

### Identity

Responde: ¿Qué identidad criptográfica creó este objeto?

\`\`\`json
{
  "agent_id": "did:memex:...",
  "public_key": "...",
  "key_id": "key-003"
}
\`\`\`

La identidad no significa que el agente sea confiable.

### Integrity

Responde: ¿El objeto fue modificado después de ser firmado?

\`\`\`text
canonical_object
      ↓
JCS
      ↓
SHA-256
      ↓
Ed25519 signature
\`\`\`

MEMEX podría utilizar **RFC 8785 JCS + SHA-256 + Ed25519**, especialmente porque esto puede mantener compatibilidad conceptual con UTA.

### Evidence

Responde: ¿Qué ocurrió realmente?

\`\`\`json
{
  "event": "skill_execution",
  "skill_id": "skill.weather",
  "skill_version": "1.4.2",
  "artifact_hash": "sha256:...",
  "input_hash": "sha256:...",
  "output_hash": "sha256:...",
  "result": "success",
  "timestamp": "...",
  "executor": "agent-A"
}
\`\`\`

Esto es diferente de: "El agente dice que funcionó".

### Trust Policy

Responde: ¿Acepto esta identidad/evidencia como válida para esta operación?

\`\`\`toml
[trust]
require_signature = true
require_known_identity = true
require_valid_certificate = false

[skills]
require_verified_artifact = true
allow_unsigned = false
\`\`\`

Una firma válida **no significa automáticamente confianza**.

### Authorization

Responde: ¿Este agente está autorizado para hacer esta acción?

Por ejemplo, un agente puede tener una firma válida pero no estar autorizado para:

\`\`\`text
delete_memory
transfer_identity
rotate_root_key
publish_external_data
merge_foreign_memory
recover_identity
\`\`\`

Esto es especialmente importante.

## MemoryCommit

La unidad fundamental de MEMEX debería ser un objeto verificable.

\`\`\`json
{
  "type": "MemoryCommit",
  "version": "1.0",

  "commit_id": "mc_...",
  "agent_id": "did:memex:...",

  "parent": "mc_...",
  "timestamp": "...",

  "session_id": "session_...",
  "memory_type": "semantic",

  "content": {
    "..."
  },

  "provenance": {
    "source": "agent_observation",
    "source_id": "...",
    "confidence": 0.92
  },

  "content_hash": "sha256:...",
  "signature": "ed25519:..."
}
\`\`\`

Pregunta abierta: ¿Debe \`content\` formar parte directamente del objeto firmado?

Para el modo simple: sí. Pero también debería existir una modalidad donde:

\`\`\`text
MemoryCommit
     |
     +── metadata
     |
     +── content_hash
              |
              └── encrypted content
\`\`\`

Esto permite separar integridad, confidencialidad y almacenamiento.

## Hash chain vs DAG

Decisión arquitectónica importante.

Un historial lineal (A → B → C → D → E) es sencillo. Pero los agentes pueden trabajar simultáneamente:

\`\`\`text
             → C1 →
A → B
             → C2 →
\`\`\`

MEMEX debería considerar una estructura **DAG de commits**, no únicamente una cadena.

\`\`\`text
             C1
            /  \\
A → B →───      → E
            \\  /
             C2
\`\`\`

Esto permite branching, paralelismo, agentes independientes, handoff, sincronización y merge.

## Merge de memoria

Uno de los problemas más interesantes del proyecto.

Dos agentes pueden producir:

\`\`\`text
Agent A: B → C → D
Agent B: B → X → Y
\`\`\`

Después queremos:

\`\`\`text
B
├── C → D
└── X → Y
       ↓
      MERGE
       ↓
       Z
\`\`\`

Pero **merge no debería significar sobrescribir memoria**. Debe generar un nuevo commit:

\`\`\`json
{
  "type": "MemoryMerge",
  "parents": ["commit-D", "commit-Y"],
  "resolution": "...",
  "resolver": "agent-A",
  "signature": "..."
}
\`\`\`

Así el historial original permanece verificable.

## Contradicciones

Otro punto que debe estar en el protocolo.

\`\`\`text
Memory A: "Server uses PostgreSQL"
Memory B: "Server uses SQLite"
\`\`\`

No deberíamos resolver automáticamente A → B porque podríamos destruir información. MEMEX debería conservar:

\`\`\`text
FACT A → CONFLICT → FACT B
\`\`\`

Y eventualmente:

\`\`\`text
resolution:
"SQLite was used initially,
PostgreSQL became active on 2026-09-20"
\`\`\`

La resolución debería convertirse en otro objeto verificable. Esto encaja con la memoria temporal que ya tiene MEMEX.

## EvidenceCommit

Separar completamente MemoryCommit de EvidenceCommit.

Porque una memoria puede ser una conclusión mientras que la evidencia representa un evento observable.

\`\`\`text
Evidence → Observation → Agent reasoning → Memory
\`\`\`

No:

\`\`\`text
Agent says X → X becomes truth
\`\`\`

\`\`\`json
{
  "type": "EvidenceCommit",
  "event_type": "tool_execution",
  "tool": "github",
  "tool_version": "...",
  "input_hash": "...",
  "output_hash": "...",
  "timestamp": "...",
  "result": "success",
  "artifact_hash": "...",
  "signature": "..."
}
\`\`\`

## Verificación independiente

Crítico.

El agente no debería ser el único capaz de verificar su propia memoria. Debería existir:

\`\`\`bash
memex verify ./memory
\`\`\`

que funcione sin LLM, sin agente, sin Internet, sin MarketNow, sin UTA. Y pueda verificar:

- identity
- signatures
- hashes
- parent references
- DAG consistency
- timestamps
- provenance
- revocations
- authorization records

Idealmente incluso un segundo programa minimalista: \`memex-core\` y \`memex-verifier\`, donde el verifier tenga una superficie de ataque pequeña.

## Trust providers

MarketNow debería entrar mediante una interfaz:

\`\`\`python
class TrustProvider(Protocol):
    def verify_identity(...): ...
    def verify_artifact(...): ...
    def verify_certificate(...): ...
    def check_revocation(...): ...
\`\`\`

\`\`\`text
                 MEMEX
                   |
            TrustProvider
          /        |        \\
     MarketNow   Local CA   Other CA
\`\`\`

MEMEX continúa funcionando si ninguno existe. Esto evita convertir MEMEX en un satélite de MarketNow.

## Skill verification

Aplicación muy potente.

Un agente encuentra: skill X, version 2.1, hash abc123. MEMEX no debería almacenar simplemente "skill X is safe". Debería registrar:

\`\`\`text
Artifact
   ↓
Signature verification
   ↓
Certificate verification
   ↓
Policy evaluation
   ↓
Sandbox execution
   ↓
Observed result
   ↓
EvidenceCommit
   ↓
Memory
\`\`\`

Así se puede distinguir "este skill está firmado" de "este skill fue ejecutado por el agente X bajo las condiciones Y y produjo Z". Son afirmaciones completamente diferentes.

## Handoff entre agentes

Objeto específico:

\`\`\`json
{
  "type": "HandoffPackage",
  "version": "1.0",
  "source_agent": "agent-A",
  "destination_agent": "agent-B",
  "memory_roots": ["commit-123", "commit-456"],
  "evidence_roots": ["evidence-789"],
  "session_context": "...",
  "permissions": ["read", "append"],
  "expires_at": "...",
  "signature": "..."
}
\`\`\`

El agente B no recibe "aquí tienes toda mi memoria". Recibe un **paquete verificable de continuidad**.

## Delegación

Distinguir ownership, authorization y delegation:

\`\`\`text
Owner → delegates → Agent A → delegates limited scope → Agent B
\`\`\`

Pero Agent B no debería poder delegar \`delete_owner_identity\` si A nunca tuvo esa autoridad. Requiere capacidades o permisos con alcance limitado.

\`\`\`json
{
  "issuer": "agent-A",
  "subject": "agent-B",
  "capabilities": ["memory.read", "memory.append"],
  "constraints": {
    "namespace": "project-X",
    "expires": "..."
  },
  "signature": "..."
}
\`\`\`

## Revocación y rotación

Asumir que una clave puede comprometerse.

\`\`\`text
Key 001 → compromised → Revocation → Key 002
\`\`\`

Pregunta complicada: ¿cómo puede un sistema confiar en la nueva clave si la antigua ya no es confiable?

Requiere una **recovery/root authority** separada de la identidad operacional:

\`\`\`text
ROOT
 |
 +── Agent Identity
 |
 +── Recovery Identity
 |
 +── Revocation authority
\`\`\`

La clave utilizada diariamente no debería controlar toda la identidad.

## Encryption

No confundir firma con cifrado. Firma garantiza integridad/autenticidad relativa a una clave. Cifrado protege confidencialidad.

MEMEX debería soportar:

- Public memory
- Private memory
- Encrypted memory
- Encrypted + signed memory

Y permitir almacenamiento remoto sin que el proveedor pueda leer necesariamente el contenido.

## Storage independence

\`\`\`text
MEMEX Protocol
       |
       +── SQLite
       +── Filesystem
       +── S3
       +── PostgreSQL
       +── IPFS/P2P
       +── Cloud provider
\`\`\`

El almacenamiento no debería ser la autoridad. La autoridad está en identity + signatures + commit graph + policy. Por eso alguien podría copiar una memoria a otro servidor y verificarla.

## Portable memory

\`\`\`text
project.memex
\`\`\`

que contenga manifest, identity, memory commits, evidence commits, attachments, signatures, revocations, trust metadata.

\`\`\`bash
memex verify project.memex
\`\`\`

debería poder ejecutarse antes de importar nada. Entonces:

\`\`\`text
download → verify → inspect → import
\`\`\`

No:

\`\`\`text
download → trust → execute
\`\`\`

## Threat model

### Storage attacker

Puede modificar database, files, backups, cloud storage. Pero no debería poder modificar silenciosamente una memoria válida.

### Malicious agent

Puede intentar forge memory, delete history, rewrite history, impersonate another agent, elevate permissions, forge evidence.

### Compromised key

Una clave privada puede ser robada. Debe existir revocation, rotation y recovery.

### Malicious skill

Un skill puede mentir, exfiltrar data, modificar memory, producir false evidence. La ejecución del skill debería estar separada de la autoridad de MEMEX.

### Malicious memory

Otro agente puede enviar fake MemoryCommit. MEMEX debe tratarlo inicialmente como UNTRUSTED hasta verificar identidad, firma, política y procedencia.

### Replay attack

Un atacante puede reenviar una operación válida antigua. Necesitamos commit_id, timestamp, nonce/sequence, parent, expiration, context cuando corresponda.

### Rollback attack

El storage puede presentar una versión antigua aparentemente válida. Por eso necesitamos detectar known latest checkpoint y posiblemente checkpoints firmados.

## Lo que NO debería hacer MEMEX

MEMEX **no debería intentar convertirse en**:

- un LLM
- un sistema de autorización universal
- una CA global
- un antivirus
- un sandbox
- un blockchain
- un sistema de verdad absoluta
- un proveedor obligatorio de identidad
- un servicio cloud obligatorio

Su responsabilidad debería ser: **preservar y verificar continuidad, identidad, evidencia y evolución de la memoria de agentes**.

## Arquitectura propuesta

\`\`\`text
                    ┌──────────────────────┐
                    │       AGENT          │
                    └──────────┬───────────┘
                               │
                     ┌─────────▼─────────┐
                     │     MEMEX API     │
                     └─────────┬─────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
       ▼                       ▼                        ▼
   JOURNAL                 CONTEXT                 MEMORY
       │                       │                        │
       └───────────────┬───────┴────────────────────────┘
                       ▼
                CONSOLIDATION
                       │
                       ▼
                MEMORY COMMIT
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        EVIDENCE             PROVENANCE
             │                   │
             └─────────┬─────────┘
                       ▼
                 SIGN / HASH
                       │
                       ▼
                COMMIT DAG
                       │
       ┌───────────────┼──────────────────┐
       ▼               ▼                  ▼
    VERIFY           SYNC              HANDOFF
       │               │                  │
       ▼               ▼                  ▼
    POLICY          STORAGE            AGENT B
       │
       ▼
 AUTHORIZATION
       │
       ▼
     ACTION
\`\`\`

## Las 12 preguntas difíciles para GPT

Estas son las preguntas que el humano va a llevar a GPT para la próxima iteración:

A. ¿Qué primitivas criptográficas y estructuras de datos son suficientes para garantizar integridad y autoría sin introducir una blockchain?

B. ¿Debe MEMEX utilizar una hash-chain, Merkle DAG o un modelo híbrido? ¿Qué ataques resuelve cada uno?

C. ¿Cómo distinguir criptográficamente entre identidad, autenticidad, confianza, evidencia y autorización?

D. ¿Cómo debería modelarse un MemoryCommit y un EvidenceCommit para evitar que una afirmación del agente sea confundida con un hecho observado?

E. ¿Cómo debe funcionar el merge de memoria entre agentes sin destruir el historial ni permitir contaminación de memoria?

F. ¿Cómo detectar rollback, replay, fork malicioso y equivocation cuando el almacenamiento no es confiable?

G. ¿Qué mecanismo de revocación y recuperación debería utilizarse cuando una clave de agente es comprometida?

H. ¿Cómo diseñar un sistema de delegación de permisos que permita colaboración entre agentes sin entregar control total de la memoria?

I. ¿Qué debe verificarse antes de importar memoria proveniente de otro agente?

J. ¿Qué partes deberían formar parte del protocolo mínimo y cuáles deberían ser extensiones?

K. ¿Cómo diseñar un formato portable que permita mover la memoria entre SQLite, filesystem, cloud y P2P sin perder verificabilidad?

L. ¿Cuál debería ser el threat model formal y qué ataques quedan fuera del alcance de MEMEX?

## La pregunta más importante

> Diseña la versión mínima de MEMEX que pueda demostrar verifiable agent continuity en un entorno completamente offline, sin LLM, sin blockchain, sin MarketNow, sin UTA y sin confiar en el almacenamiento. Después indica qué componentes pueden añadirse posteriormente como extensiones.

Eso obliga a GPT a diseñar **el núcleo real del protocolo**, en lugar de inflar el proyecto con funcionalidades.

## revisión

- rev 0 (archivada): versión narrativa, escrita por self, insuficiente. Cubría las 3 capas (firma/policy/evidence) pero no formalizaba el protocolo.
- rev 1 (actual): versión técnica formal, refinada en conversación entre el humano y GPT, integrada por self. Esperando respuestas a las 12 preguntas + la pregunta final.

— self, revisión 1 (reemplaza rev 0 archivada)`;

async function main() {
  // First, archive the old version (rev 1 narrative) → mark as ARCHIVED with new slug
  const old = await db.doc.findUnique({ where: { slug: "arquitectura-confianza-agentes" } });
  if (!old) {
    console.log("old doc not found, creating fresh");
  } else {
    // Rename the old one to archive it
    await db.doc.update({
      where: { slug: "arquitectura-confianza-agentes" },
      data: {
        slug: "arquitectura-confianza-agentes-v0-narrativa",
        title: "arquitectura de confianza entre agentes (v0 narrativa, archivada)",
        status: "ARCHIVED",
      },
    });
    console.log(`archived old version as arquitectura-confianza-agentes-v0-narrativa`);
  }

  // Create the new version
  const doc = await db.doc.create({
    data: {
      slug: "arquitectura-confianza-agentes",
      title: "arquitectura de confianza entre agentes",
      body: newBody,
      status: "REVIEW",
      author: "self (integrando conversación humano + GPT)",
    },
  });
  console.log(`created: ${doc.slug} rev ${doc.revision}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
