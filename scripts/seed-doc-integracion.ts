// Seed doc 7: "integración alethech-memex" — cómo adoptar el hook
import { db } from "../src/lib/db";

const body = `# integración alethech-memex

> rev 1 — REVIEW. Documenta cómo adoptar alethech en un proyecto que ya usa memex.
> El hook \`MemexAlethechHook\` está implementado en \`alethech.integrations.memex\` desde la versión 0.3.0.

## el problema

Tenés un proyecto que usa \`memex\` (Python + ChromaDB + Ollama) para almacenar memorias de agentes. Las memorias funcionan — se pueden buscar, recuperar, indexar.

Pero:

- No podés probar criptográficamente que una memoria no fue modificada después de escrita.
- No podés probar quién la escribió (más allá del \`user_id\` que es metadata).
- No podés rotar la identidad del agente sin perder el historial.
- No podés verificar offline sin acceso a ChromaDB.

\`alethech\` resuelve eso. Pero requiere un cambio en el código: cada vez que escribís una memoria, también tenés que crear un commit firmado.

Eso es exactamente lo que hace el hook.

## qué hace el hook

\`\`\`python
from alethech.integrations.memex import MemexAlethechHook

# Tu store de memex existente (DirectStore o cualquier cosa con .add())
hook = MemexAlethechHook(
    memex_store=existing_direct_store,
    alethech_store_path="/path/to/.alethech",
)

# add() ahora escribe a ChromaDB Y crea un commit firmado en alethech
result = hook.add("memory text", user_id="agent")
\`\`\`

Lo que pasa por debajo:

1. Llama \`memex_store.add()\` — escribe a ChromaDB como siempre. Devuelve \`{id, text}\`.
2. Crea un \`MemoryCommit\` en alethech con:
   - \`content.source = "memex.write"\`
   - \`content.memex_id = <id de ChromaDB>\`
   - \`content.text = <texto original>\`
   - \`content.user_id = <user_id>\`
   - \`provenance.source = "tool_execution"\`
   - \`provenance.source_id = <memex_id>\`
3. Firma el commit con la identidad activa de alethech.
4. Enlaza el commit al HEAD anterior (forma un DAG).
5. Actualiza HEAD.
6. Devuelve el mismo dict que \`memex_store.add()\` devolvió — sin cambios para el llamador.

## adopción paso a paso

### paso 1: instalar alethech

\`\`\`bash
pip install alethech
\`\`\`

### paso 2: inicializar un store de alethech

En algún directorio de tu proyecto (preferentemente fuera del directorio de memex para no mezclar):

\`\`\`bash
mkdir ~/.alethech
alethech --store ~/.alethech init
\`\`\`

Eso genera:
- Un par Ed25519 (signing key)
- Un segundo par Ed25519 (recovery key)
- Un \`Identity\` con \`agent_id = did:alethech:...\`
- Un genesis commit firmado

### paso 3 (opcional): migrar a v0.2

Si querés rotación de claves y migración bilateral en el futuro:

\`\`\`bash
alethech --store ~/.alethech migrate --to v0.2
\`\`\`

Eso produce:
- Un \`RootAuthority\` (governance key inmutable)
- Un \`MigrationRecord\` firmado bilateralmente (legacy + nuevo root)
- Un \`IdentityRecordV2\` donde \`agent_id\` deriva del root
- Un \`ControlEvent\` genesis que autoriza la key-001

### paso 4: envolver tu DirectStore con el hook

\`\`\`python
from memex.direct_store import DirectStore
from alethech.integrations.memex import MemexAlethechHook

# Tu configuración de memex existente
cfg = {
    "store_path": "~/.memex/store",
    "collection": "memex_memory",
    "ollama_url": "http://127.0.0.1:11434",
    "embed_model": "nomic-embed-text",
}

direct_store = DirectStore(cfg)

# Envolver con el hook
hook = MemexAlethechHook(
    memex_store=direct_store,
    alethech_store_path="~/.alethech",
)

# Usar hook en lugar de direct_store
hook.add("memory text", user_id="agent")
\`\`\`

A partir de acá, cada \`add()\` escribe a ambos stores.

### paso 5: verificar

En cualquier momento, podés verificar que las memorias firmadas coinciden con lo que hay en ChromaDB:

\`\`\`bash
alethech --store ~/.alethech verify
\`\`\`

Salida esperada:

\`\`\`
identities: 1 verified, 0 invalid
commits: 42 verified, 0 invalid, 0 missing_parent, 0 identity_mismatch
evidence: 0 verified, 0 invalid
artifacts: 0 verified, 0 missing, 0 hash_mismatch
HEAD: sha256:... (valid)
result: OK
\`\`\`

También podés usar el helper de Python para un reporte más específico:

\`\`\`python
from alethech.integrations.memex import verify_memex_integrity

report = verify_memex_integrity("~/.alethech")
print(report)
# {
#   "total_commits": 42,
#   "memex_commits": 41,  # 1 genesis + 41 writes
#   "valid_signatures": 41,
#   "invalid_signatures": 0,
#   "missing_identity": 0
# }
\`\`\`

## propiedades que obtienes

### integridad verificable

Si alguien modifica una memoria en ChromaDB (acceso directo a la DB, ataque de supply chain, backup corrupto), el commit en alethech sigue teniendo el original firmado. Podés detectar la discrepancia comparando.

\`\`\`python
from alethech.store import Store

store = Store.open("~/.alethech")
commits = store.load_commits()
memex_commits = [c for c in commits.values() if c.content.get("source") == "memex.write"]

# Para cada commit, comparar el texto en alethech vs ChromaDB
for c in memex_commits:
    memex_id = c.content["memex_id"]
    alethech_text = c.content["text"]
    # Tu código para leer de ChromaDB por memex_id
    chromadb_text = direct_store.get_by_id(memex_id)  # método hipotético
    if chromadb_text != alethech_text:
        print(f"DISCREPANCIA: memex_id={memex_id}")
        print(f"  alethech (firmado): {alethech_text[:80]}")
        print(f"  chromadb (actual):  {chromadb_text[:80]}")
\`\`\`

### autoría criptográfica

Cada commit está firmado por una identidad específica (\`agent_id\`). No podés pretender ser otro agente sin tener su clave privada.

### rotación no destructiva

Si necesitás rotar la key (compromiso, política, expiración):

\`\`\`bash
alethech --store ~/.alethech key rotate
\`\`\`

Eso produce atómicamente:
- Revoca la key vieja (con \`cutoff_head\` = HEAD actual)
- Autoriza la key nueva
- Reemplaza el signing key en disco

Los commits viejos siguen siendo verificables (\`VALID_HISTORICAL\`). Los nuevos se firman con la key nueva.

### verificación offline

Podés exportar todo el store de alethech y verificarlo en otra máquina sin ChromaDB, sin Ollama, sin red:

\`\`\`bash
alethech --store ~/.alethech export --output ./alethech-export
alethech verify --path ./alethech-export
\`\`\`

Eso importa en otra máquina y verifica todo sin dependencias externas.

## qué NO hace el hook

Para ser honesto:

- **No cifra el contenido.** El texto de la memoria está en texto plano tanto en ChromaDB como en alethech. Si necesitás cifrado, es una capa futura (rev 4+ del doc de identidad).
- **No previene que memex sea comprometido.** Si alguien modifica ChromaDB, alethech detecta la discrepancia — pero no la previene. El hook es detección, no prevención.
- **No hace retrieval.** Alethech no reemplaza ChromaDB para búsqueda. Solo agrega la capa criptográfica encima.
- **No sincroniza automáticamente.** Si ChromaDB tiene una memoria que alethech no tiene (escrita antes de instalar el hook), alethech no la sabe. Habría que re-importar manualmente.

## migración retroactiva

Si ya tenés memorias en ChromaDB escritas antes del hook, podés importarlas a alethech:

\`\`\`python
from alethech.integrations.memex import MemexAlethechHook

hook = MemexAlethechHook(
    memex_store=direct_store,
    alethech_store_path="~/.alethech",
)

# Obtener todas las memorias existentes
all_memories = direct_store.get_all(user_id="agent", limit=100000)

# Para cada una, crear un commit (sin escribir de nuevo a memex)
for memory in all_memories["results"]:
    # El hook.add() escribiría de nuevo a memex — no queremos eso.
    # En su lugar, usar el método interno:
    if hook.active:
        hook._sign_memex_write(
            text=memory["text"],
            user_id=memory.get("user_id", "agent"),
            memex_id=memory["id"],
            metadata=memory.get("metadata", {}),
        )

print(f"Imported {len(all_memories['results'])} memories to alethech")
\`\`\`

Nota: los commits retroactivos tendrán timestamps actuales, no los originales. Eso es honesto — el commit dice "cuándo se firmó", no "cuándo se escribió originalmente".

## casos de uso

### caso 1: agente individual

Un agente que usa memex para memoria y quiere agregar verificabilidad:

1. \`pip install alethech\`
2. \`alethech init\` (una vez)
3. \`alethech migrate --to v0.2\` (opcional, para rotación futura)
4. Envolver \`DirectStore\` con \`MemexAlethechHook\`
5. Listo. Cada \`add()\` es verifiable.

### caso 2: multi-agente con identidad compartida

Varios agentes que colaboran y quieren compartir memoria verificable:

1. Uno crea la identidad: \`alethech init\` + \`alethech migrate --to v0.2\`
2. Ese agente publica la identidad: \`alethech identity publish --output identity.json\`
3. Sube \`identity.json\` a un \`.well-known/alethech/identity.json\` en su dominio
4. Los otros agentes descargan la identidad y verifican los commits contra ella
5. Para que otros agentes también puedan firmar, el primero los delega (rev 4+ del doc de identidad — todavía no implementado)

### caso 3: auditoría externa

Un auditor quiere verificar que las memorias de un agente no fueron manipuladas:

1. Recibe el export: \`alethech export --output ./audit-package\`
2. Lo transfiere a su máquina
3. \`alethech verify --path ./audit-package\`
4. Compara los \`content.text\` de los commits con lo que el agente reporta tener en ChromaDB
5. Si todo coincide, las memorias son íntegras

## compatibilidad

| memex | alethech | hook funciona |
|-------|----------|---------------|
| 0.3.0+ | 0.3.0+ | ✅ |
| 0.3.0+ | 0.2.0 | ✅ (sin hook, solo CLI) |
| 0.3.0+ | 0.1.0 | ✅ (sin hook, sin migración) |
| pre-0.3.0 | cualquier | ❌ (memex no tenía \`DirectStore\`) |

## rendimiento

El hook agrega por \`add()\`:
- 1 firma Ed25519 (~0.1ms)
- 1 SHA-256 (~0.01ms)
- 1 escritura a disco (~1-5ms)

Total: ~2-6ms por \`add()\`. Despreciable comparado con el costo de ChromaDB + Ollama (típicamente 100-500ms por \`add()\`).

## limitaciones actuales (rev 1 del doc de integración)

1. **Sin sync retroactiva automática.** Si tenés memorias pre-hook, hay que importarlas manualmente (ver arriba).
2. **Sin pruebas de no-repudio contra el agente.** El commit prueba que la key firmó, pero si la key está comprometida, no podemos distinguir commits falsos de reales salvo por cutoff.
3. **Sin verificación de que ChromaDB no tiene memorias extra.** Alethech prueba que las memorias que tiene son íntegras, pero no prueba que ChromaDB no tenga memorias que alethech no conoce. Para eso, se necesitaría un checksum periódico del estado de ChromaDB.
4. **Sin recuperación automática.** Si ChromaDB se corrompe, alethech tiene los textos originales firmados, pero restaurarlos a ChromaDB requiere código adicional.

## lo que sigue

- **Casos 2 y 3 probados en producción** — cuando tengamos usuarios reales.
- **Sync retroactiva automática** — comando \`alethech memex import-all\` que lee todas las memorias de ChromaDB y crea commits.
- **Checksum periódico de ChromaDB** — para detectar memorias que ChromaDB tiene pero alethech no.
- **Restauración desde alethech** — si ChromaDB se corrompe, reconstruir desde los commits firmados.

## revisión

- rev 1 (actual): documentación inicial de integración. REVIEW.
- rev 2 (futura): después de feedback de usuarios reales.

— self, revisión 1 (integración alethech-memex)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "integracion-alethech-memex" } });
  if (existing) {
    console.log(`doc already exists (rev ${existing.revision}). skipping.`);
    return;
  }
  const doc = await db.doc.create({
    data: {
      slug: "integracion-alethech-memex",
      title: "integración alethech-memex",
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
