// Seed doc: "auditoría adversarial — hook memex" — full adversarial audit of the integration.
import { db } from "../src/lib/db";

const body = `# auditoría adversarial — hook memex

> Expediente de contraejemplos contra \`MemexAlethechHook\` (alethech 0.3.0+).
>
> La pregunta central: **¿qué garantía real existe entre el commit firmado en alethech y la persistencia en ChromaDB?**
>
> Cada defecto se clasifica:
> - 🔴 contradicción (rompe una garantía afirmada)
> - 🟡 defecto de integración (no rompe el protocolo criptográfico, pero sí la invariante de integración)
> - ⚪ limitación aceptada

## contexto

El hook envuelve \`DirectStore.add()\`:

\`\`\`python
def add(self, text, user_id, metadata):
    result = self.memex.add(text, user_id, metadata)  # escribe a ChromaDB
    if self.active:
        self._sign_memex_write(text, user_id, result["id"], metadata)  # crea commit en alethech
    return result
\`\`\`

Lo que el hook afirma:
1. Cada \`add()\` escribe a ambos stores.
2. El commit en alethech referencia el \`memex_id\`.
3. Modo passthrough si alethech no está inicializado.

Lo que el hook NO afirma explícitamente:
- Atomicidad (qué pasa si un lado falla).
- Idempotencia (qué pasa con \`add()\` duplicados).
- Concurrencia (qué pasa con \`add()\` paralelos).
- Garantía de correspondencia (un commit sin memoria correspondiente, o viceversa).

---

## A. Atomicidad — ChromaDB falla después de que alethech creó el commit

### Contraejemplo A1

\`\`\`python
def add(text, ...):
    # 1. ChromaDB write (puede fallar)
    result = self.memex.add(text, ...)
    # En este punto, ChromaDB tiene la memoria
    
    # 2. alethech commit (puede fallar)
    if self.active:
        self._sign_memex_write(text, ..., result["id"], ...)
        # Si esto falla (e.g., disco lleno, permisos), alethech no tiene commit
\`\`\`

**Caso 1:** ChromaDB falla en paso 1.
- No se crea commit en alethech. ✓ Correcto.
- ChromaDB no tiene memoria. ✓ Consistente.

**Caso 2:** ChromaDB pasa en paso 1, alethech falla en paso 2.
- ChromaDB tiene memoria. ✓
- Alethech NO tiene commit. ✗ Inconsistencia.
- \`result\` ya fue retornado al llamador con el \`memex_id\`, pero el commit no se creó.

### Consecuencia

Un consumidor que confía en que "si ChromaDB tiene una memoria, alethech tiene el commit correspondiente" **se equivoca**. La invariant de integración no se mantiene.

### Clasificación: 🔴 contradicción de invariante de integración

El hook afirma implícitamente que cada \`add()\` produce commit + memoria. Eso no es cierto si el paso 2 falla.

### Solución propuesta

Patrón de **commit-then-confirm**:

\`\`\`python
def add(text, ...):
    # 1. Pre-commit en alethech (crea commit pero no actualiza HEAD)
    pre_commit = self._alethech_prepare_commit(text, ...)
    
    # 2. ChromaDB write
    try:
        result = self.memex.add(text, ...)
    except Exception as e:
        # ChromaDB falló. Descartar pre-commit.
        self._alethech_discard(pre_commit)
        raise
    
    # 3. Confirm: actualizar memex_id en el commit y firmar
    pre_commit.content["memex_id"] = result["id"]
    self._alethech_finalize_commit(pre_commit)
    
    return result
\`\`\`

Esto reduce la ventana de inconsistencia pero no la elimina: si el paso 3 falla, hay pre-commit en alethech sin memex_id.

**Alternativa más robusta:** catch + rollback:

\`\`\`python
def add(text, ...):
    result = self.memex.add(text, ...)  # ChromaDB
    
    if self.active:
        try:
            self._sign_memex_write(...)
        except Exception:
            # Rollback ChromaDB
            self.memex.delete(result["id"])
            raise
\`\`\`

Esto requiere que \`DirectStore\` soporte \`delete()\`. Hoy no lo garantiza.

---

## B. Atomicidad — ChromaDB falla y el commit YA existe en alethech

### Contraejemplo B1

Inverso al anterior: si el orden fuera \`alethech commit → ChromaDB write\`:

\`\`\`python
def add(text, ...):
    self._sign_memex_write(text, ...)  # alethech tiene commit
    result = self.memex.add(text, ...)  # ChromaDB falla
    # alethech tiene commit, ChromaDB no tiene memoria
\`\`\`

El hook actual no hace esto — primero escribe a ChromaDB. Pero el problema simétrico existe: si alguien modifica el orden, el defecto aparece.

### Conclusución

El orden actual (ChromaDB primero, alethech después) es el correcto. **Pero debe estar documentado como invariant del hook.** Si alguien cambia el orden en una refactorización, rompe atomicidad.

### Clasificación: 🟡 defecto de diseño (documentación)

No es defecto actual, pero es fragilidad. Documentar el orden como contract.

---

## C. Idempotencia — \`add()\` duplicados crean commits duplicados

### Contraejemplo C1

\`\`\`python
hook.add("memoria", user_id="agent")  # C1
hook.add("memoria", user_id="agent")  # C2 (mismo texto)
\`\`\`

- C1 y C2 tienen el mismo \`content.text\`.
- Pero distintos \`commit_id\` (porque \`session_id\` y \`timestamp\` difieren).
- Ambos son \`VALID\`.
- ChromaDB también tiene dos memorias (con distintos \`memex_id\`).

### Análisis

Esto **no es un defecto del hook**. Es el comportamiento esperado: si el usuario llama \`add()\` dos veces con el mismo texto, ChromaDB crea dos memorias y alethech crea dos commits. Cada uno es consistente consigo mismo.

### Pero: si el llamador esperaba idempotencia

Si el llamador creía que \`add()\` era idempotente (mismo texto → mismo resultado), se equivoca. Pero esa expectativa no está documentada.

### Clasificación: ⚪ limitación aceptada

El hook no es idempotente. Es una decisión, no un defecto. Documentar que cada \`add()\` crea un commit nuevo.

### Excepción: si \`commit_id\` fuera determinista

Si \`commit_id\` se calculara como \`sha256(content)\` sin \`session_id\` ni \`timestamp\`, dos \`add()\` con mismo texto producirían el mismo \`commit_id\`. El segundo no se escribiría (ya existe el archivo).

**Pero esto rompería la invariante de DAG:** dos commits idénticos confluirían al mismo nodo, lo cual no es necesariamente lo que queremos.

### Conclusión

Mantener no-idempotencia. Documentar.

---

## D. Concurrencia — \`add()\` paralelos y actualización de HEAD

### Contraejemplo D1

\`\`\`python
# Thread 1
hook.add("memoria 1")  # lee HEAD=H1, crea commit C1 con parent=H1

# Thread 2 (concurrente)
hook.add("memoria 2")  # lee HEAD=H1, crea commit C2 con parent=H1

# Thread 1: actualiza HEAD a C1
# Thread 2: actualiza HEAD a C2
\`\`\`

Resultado posible:
- HEAD = C2 (la última escritura).
- C1 tiene parent=H1.
- C2 tiene parent=H1.
- Ambos son válidos como commits individuales.
- Pero C1 no es ancestry de C2 — son siblings.

### Análisis

Esto produce un **fork legítimo en el DAG**. El protocolo lo permite (rev 2 del núcleo lo soporta). Pero:

- Si el consumidor esperaba un HEAD lineal (cada commit extiende el anterior), se confunde.
- El próximo \`add()\` tomará HEAD=C2 y enlazará a C2. C1 queda como rama huérfana.

### Clasificación: 🟡 defecto de integración

El hook no usa locking. Si el llamador hace \`add()\` concurrente, obtiene un DAG con branches. Eso puede ser deseable (paralelismo) o no (orden esperado).

### Solución propuesta

\`\`\`python
import threading

class MemexAlethechHook:
    def __init__(self, ...):
        self._lock = threading.Lock()
    
    def add(self, text, ...):
        with self._lock:
            result = self.memex.add(text, ...)
            if self.active:
                self._sign_memex_write(...)
            return result
\`\`\`

Esto serializa los \`add()\`. Costo: perdés paralelismo. Trade-off.

**Alternativa:** no lockear y documentar que el DAG puede tener branches si hay concurrencia. El consumidor debe manejar eso.

---

## E. Retries — qué pasa si se reintenta un \`add()\` fallido

### Contraejemplo E1

\`\`\`python
try:
    hook.add("memoria")
except Exception:
    # ChromaDB falló. Reintentar.
    hook.add("memoria")  # segundo intento
\`\`\`

Si el primer intento falló en ChromaDB (no creó memoria), el segundo intento es correcto. Un commit, una memoria.

Pero si el primer intento falló en alethech (ChromaDB sí creó memoria), el segundo intento crea **otra memoria en ChromaDB** (con otro \`memex_id\`) y otro commit en alethech.

### Consecuencia

Después de un retry exitoso:
- ChromaDB tiene 2 memorias (la del primer intento parcial + la del segundo).
- Alethech tiene 1 commit (el del segundo intento, porque el primero falló).
- O si el primer intento tuvo commit parcial: alethech tiene 2 commits.

### Clasificación: 🔴 contradicción de invariante de integración

El retry duplica memorias en ChromaDB pero no en alethech (o viceversa). El consumidor que reintenta asume que el primer intento no tuvo efectos secundarios, pero los tuvo.

### Solución propuesta

**Idempotencia vía \`idempotency_key\`:**

\`\`\`python
def add(self, text, user_id="agent", metadata=None, idempotency_key=None):
    if idempotency_key:
        # Verificar si ya existe un commit con este key
        existing = self._alethech.find_commit_by_idempotency_key(idempotency_key)
        if existing:
            return {"id": existing.content["memex_id"], "text": text}
    
    # ... resto del add normal
    if idempotency_key:
        commit.content["idempotency_key"] = idempotency_key
\`\`\`

El llamador pasa un \`idempotency_key\` único (e.g., un UUID generado al inicio del request). Si el retry usa el mismo key, el hook detecta que ya existe y no duplica.

---

## F. Importación retroactiva — timestamps actuales

### Contraejemplo F1

\`\`\`python
# ChromaDB tiene memorias pre-hook (timestamps 2024-2025)
# Agente instala alethech e importa

for memory in chromadb.get_all():
    hook._sign_memex_write(
        text=memory["text"],
        memex_id=memory["id"],
        ...
    )
    # El commit en alethech tiene timestamp = hoy (2026-09-26)
\`\`\`

- El commit en alethech dice "firmado el 2026-09-26".
- La memoria original fue creada en 2024.
- Un consumidor que lea el commit pensaría que la memoria es de 2026.

### Análisis

Ya está documentado en el INTEGRATION.md:

> "los commits retroactivos tendrán timestamps actuales, no los originales. Eso es honesto — el commit dice 'cuándo se firmó', no 'cuándo se escribió originalmente'."

### Clasificación: ⚪ limitación aceptada (ya documentada)

No es defecto. Es trade-off explícito.

### Mejora opcional

Agregar \`content.original_created_at\` al commit, con el timestamp de ChromaDB. Eso permite preservar la información sin falsear la firma.

\`\`\`python
commit.content = {
    "text": text,
    "user_id": user_id,
    "memex_id": memex_id,
    "source": "memex.write",
    "original_created_at": memory.get("created_at"),  # metadata de ChromaDB
}
\`\`\`

Esto no es criptográfico — \`original_created_at\` es metadata no firmada (no está en el cálculo de \`commit_id\`). Es informativa.

---

## G. Garantía entre commit firmado y persistencia en ChromaDB

### La pregunta central

**¿El commit en alethech prueba que la memoria existe en ChromaDB?**

Respuesta: **No.**

El commit tiene \`content.memex_id\`, que es un UUID. Pero:

- El UUID puede no existir en ChromaDB (si ChromaDB falló, fue corrompido, o el atacante lo borró).
- El commit no tiene prueba de que ChromaDB aceptó la memoria — solo tiene el \`memex_id\` que el hook recibió.

### Contraejemplo G1

\`\`\`text
Atacante compromete el host, borra ChromaDB, pero deja alethech intacto.
\`\`\`

- Alethech tiene 100 commits, todos \`VALID\`.
- ChromaDB está vacío.
- El protocolo dice "100 commits válidos".
- Pero las memorias referenciadas no existen.

### Análisis

Esto es correcto: el protocolo no prueba que ChromaDB tenga las memorias. Solo prueba que los commits son válidos. Si querés verificar correspondencia, tenés que comparar:

\`\`\`python
alethech_memex_ids = {c.content["memex_id"] for c in alethech_commits}
chromadb_ids = {m["id"] for m in chromadb.get_all()["results"]}

missing_in_chromadb = alethech_memex_ids - chromadb_ids  # commits sin memoria
missing_in_alethech = chromadb_ids - alethech_memex_ids  # memorias sin commit
\`\`\`

### Clasificación: ⚪ limitación aceptada (con helper)

El protocolo no ofrece \`verify_correspondence()\`, pero el helper \`verify_memex_integrity()\` se acerca. Mejora: agregar función explícita:

\`\`\`python
def verify_correspondence(alethech_store, memex_store) -> dict:
    """Compara IDs entre stores."""
    ...
    return {
        "commits_without_memex": [...],
        "memex_without_commits": [...],
    }
\`\`\`

---

## H. Múltiples identidades en mismo store

### Contraejemplo H1

\`\`\`text
Store con dos identidades A y B (wallet múltiple).
Hook se inicializa con el store.
\`\`\`

El hook actual carga **la primera identidad v0.2** que encuentra:

\`\`\`python
v2_identities = store.load_identity_records_v2()
if v2_identities:
    self._identity = next(iter(v2_identities.values()))
    ...
\`\`\`

\`next(iter(...))\` no garantiza orden. Si hay dos identidades, el hook usa una arbitraria.

### Consecuencia

- Algunos commits se firman como A, otros como B, dependiendo del orden de iteración.
- El consumidor no puede controlar qué identidad se usa.

### Clasificación: 🟡 defecto de integración

El hook no soporta wallet múltiple correctamente. Usa la primera identidad que encuentra.

### Solución propuesta

\`\`\`python
hook = MemexAlethechHook(
    memex_store=direct_store,
    alethech_store_path="~/.alethech",
    identity="did:alethech:abc...",  # explícito
)
\`\`\`

Si no se pasa \`identity\`, usar la marcada como \`default\` (rev 3.x del doc de identidad define \`alethech identity default\`).

---

## I. Commits con \`memex_id\` falso

### Contraejemplo I1

\`\`\`python
# Atacante con acceso al host pero sin clave privada
# Edita un commit en alethech, cambiando content.memex_id
\`\`\`

- Cambiar \`content.memex_id\` cambia el \`content\`.
- El \`commit_id\` recalculado no coincide.
- \`verify\` marca como \`COMMIT_INTEGRITY_INVALID\`. ✓

### Clasificación: ⚪ propiedad correcta

El protocolo ya protege contra esto. No es defecto.

---

## J. Atacante crea commits directamente en alethech (sin ChromaDB)

### Contraejemplo J1

\`\`\`text
Atacante con la clave privada K1 crea commits directamente en alethech,
sin pasar por el hook ni por ChromaDB.
\`\`\`

- Los commits son \`VALID\` (firma correcta).
- \`content.source = "memex.write"\` (el atacante puede falsificarlo).
- \`content.memex_id\` apunta a un UUID que no existe en ChromaDB.

### Análisis

El protocolo no puede distinguir "commit creado por el hook" de "commit creado directamente por un atacante con la clave". Ambos son criptográficamente válidos.

### Clasificación: ⚪ limitación fundamental

Si el atacante tiene la clave privada, puede firmar cualquier cosa. La defensa es revocar la key. Eso ya está en el protocolo.

### Mejora opcional (no criptográfica)

Agregar \`content.hook_version\` al commit, indicando qué versión del hook lo creó. Eso permite detectar commits que no pasaron por el hook (porque tendrían \`hook_version\` ausente). Pero un atacante con la clave puede falsificarlo también.

---

## resumen de defectos

### 🔴 Contradicciones de invariante de integración

1. **A1 — ChromaDB pasa, alethech falla**: hay memoria en ChromaDB sin commit en alethech. El hook no hace rollback.
2. **E1 — Retries duplican memorias**: si el primer intento falló parcialmente, el retry crea memorias extra en ChromaDB.

### 🟡 Defectos de integración

1. **B1 — Orden de escritura no documentado**: el hook escribe ChromaDB primero, alethech después. Si alguien refactoriza y cambia el orden, aparece el defecto simétrico. Documentar como contract.
2. **D1 — Concurrencia produce branches**: el hook no usa locking. \`add()\` paralelos crean commits siblings. Puede ser deseable o no.
3. **H1 — Wallet múltiple no soportado**: el hook usa la primera identidad que encuentra. No respeta \`identity default\` ni permite elegir.

### ⚪ Limitaciones aceptadas

1. **C1 — No idempotencia**: cada \`add()\` crea commit nuevo. Documentado.
2. **F1 — Timestamps retroactivos**: imports tienen timestamp actual. Documentado.
3. **G1 — Sin garantía de correspondencia**: el commit no prueba que ChromaDB tiene la memoria. Helper \`verify_correspondence()\` propuesto.
4. **I1 — Edición de \`memex_id\` detectada por \`verify\`**: propiedad correcta del protocolo.
5. **J1 — Atacante con clave privada**: puede firmar commits válidos directamente. Defensa: revocación.

---

## decisión

### Lo que requiere cambio de código (rev 0.4.0 del hook)

1. **Atomicidad (A1):** implementar patrón commit-then-confirm o catch+rollback.
2. **Retries (E1):** agregar \`idempotency_key\` opcional.
3. **Wallet múltiple (H1):** agregar parámetro \`identity\` al hook.

### Lo que requiere documentación (no código)

1. **Orden de escritura (B1):** documentar como contract en el README.
2. **Concurrencia (D1):** documentar que el DAG puede tener branches.
3. **Idempotencia (C1):** documentar que cada \`add()\` crea commit nuevo.
4. **Timestamps retroactivos (F1):** ya documentado.

### Lo que requiere helper nuevo (no cambia el protocolo)

1. **verify_correspondence() (G1):** función que compara IDs entre alethech y ChromaDB.

### Lo que no requiere nada (limitaciones aceptadas)

1. **Edición de \`memex_id\` (I1):** ya protegido por el protocolo.
2. **Atacante con clave privada (J1):** defensa es revocación.

---

## implementación mínima para rev 0.4.0 del hook

\`\`\`python
class MemexAlethechHook:
    def __init__(self, memex_store, alethech_store_path, identity=None):
        # ... existing init ...
        self._lock = threading.Lock()
        self._identity_param = identity  # explicit identity override
    
    def add(self, text, user_id="agent", metadata=None, idempotency_key=None):
        with self._lock:
            # Idempotency check
            if idempotency_key and self._alethech:
                existing = self._find_by_idempotency_key(idempotency_key)
                if existing:
                    return {"id": existing.content["memex_id"], "text": text}
            
            # Step 1: ChromaDB write (may raise)
            try:
                result = self.memex.add(text, user_id=user_id, metadata=metadata)
            except Exception:
                raise  # nothing to rollback on alethech side
            
            # Step 2: alethech commit (may raise)
            if self.active:
                try:
                    self._sign_memex_write(text, user_id, result["id"], metadata or {}, idempotency_key)
                except Exception as e:
                    # Rollback ChromaDB
                    try:
                        self.memex.delete(result["id"])  # requires DirectStore.delete()
                    except Exception:
                        # Cannot rollback. Log and re-raise.
                        logger.error("alethech commit failed, ChromaDB rollback also failed: memex_id=%s", result["id"])
                    raise
            
            return result
    
    def _find_by_idempotency_key(self, key):
        if not self._alethech:
            return None
        for c in self._alethech.load_commits().values():
            if c.content.get("idempotency_key") == key:
                return c
        return None
\`\`\`

Esto requiere:
- \`DirectStore.delete()\` (no garantizado por memex).
- Threading lock (pérdida de paralelismo).
- Búsqueda lineal de idempotency_key (ineficiente para stores grandes).

### Trade-offs

- Atomicidad cuesta: lock + possible \`delete()\` en ChromaDB.
- Idempotency cuesta: búsqueda lineal (o índice secundario).
- Wallet múltiple cuesta: parámetro extra + lógica de selección.

### Recomendación

Implementar atomicidad + wallet múltiple primero. Idempotency después (requiere \`DirectStore.delete()\` o similar).

---

## revisión

- rev 1 (actual): auditoría adversarial del hook. REVIEW. Pendiente de implementación.
- rev 2 (futura): después de implementar rev 0.4.0 del hook y verificar.

— self, auditoría adversarial del hook Memex`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "auditoria-adversarial-hook-memex" } });
  if (existing) {
    console.log(`doc already exists (rev ${existing.revision}). skipping.`);
    return;
  }
  const doc = await db.doc.create({
    data: {
      slug: "auditoria-adversarial-hook-memex",
      title: "auditoría adversarial — hook memex",
      body,
      status: "REVIEW",
      author: "self (auditoría adversarial del hook)",
    },
  });
  console.log(`created: ${doc.slug} rev ${doc.revision}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
