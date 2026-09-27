// Seed doc: threat model formal — priority #6.
import { db } from "../src/lib/db";

const body = `# threat model formal

> Matriz de amenazas: actor × capacidad × ataque × detección.
>
> Construida a partir de las 5 auditorías adversariales completadas (#1-#5).

## actores

| actor | qué tiene | qué no tiene |
|-------|-----------|--------------|
| Atacante sin keys | acceso de lectura al store | claves privadas |
| Atacante con commit existente | un commit válido firmado | claves privadas |
| Atacante con operational key | clave privada K (activa o revocada) | root key |
| Atacante con acceso al store | acceso de escritura al filesystem | claves privadas |
| Atacante con acceso a ChromaDB | acceso de escritura a ChromaDB | claves privadas |
| Root comprometido | root private key | nada (tiene todo) |

## matriz de amenazas

### Actor: Atacante sin keys (solo lectura)

| ataque | qué puede conseguir | detecta verify | mitigación |
|--------|---------------------|-----------------|------------|
| Leer commits | Ver contenido de memorias | N/A (no es ataque) | Cifrado (rev 4+) |
| Leer identidad | Ver public keys | N/A | Las public keys son públicas |
| Leer root authority | Ver root public key | N/A | Es pública |

**Conclusión:** sin claves privadas, el atacante no puede falsificar nada. Solo puede leer.

### Actor: Atacante con commit existente

| ataque | qué puede conseguir | detecta verify | mitigación |
|--------|---------------------|-----------------|------------|
| Replay commit en otro store | Commit aparece como válido | No detecta (diseño: replay de identidad es aceptable) | Verificar provenance si importa |
| Presentar commit fuera de contexto | Commit válido pero en store distinto | No detecta (por diseño) | Binding commit→store es policy externa |
| Modificar content.text | commit_id no coincide | ✓ \`COMMIT_INTEGRITY_INVALID\` | — |
| Modificar signature | firma no verifica | ✓ \`COMMIT_SIGNATURE_INVALID\` | — |
| Modificar commit_id | hash recalculado no coincide | ✓ \`COMMIT_INTEGRITY_INVALID\` | — |

### Actor: Atacante con operational key (K)

| ataque | qué puede conseguir | detecta verify | mitigación |
|--------|---------------------|-----------------|------------|
| Si K está activa: firmar commits válidos | Commits legítimos | No detecta (es legítimo) | — |
| Si K está revocada: firmar commits post-rotación | Commits que parecen válidos | ✓ Si C ∉ ancestry(cutoff): \`NOT_IN_PROVEN_PRE_ROTATION_HISTORY\` | Revocar K lo antes posible |
| Si K está revocada: firmar commit con parent en ancestry(cutoff) | Commit pasa como \`VALID_HISTORICAL\` | No detecta (puede ser legítimo o falso) | Limitación fundamental: no se puede distinguir sin timestamps |
| Declarar key_id equivocado | Firma no verifica contra la key declarada | ✓ \`COMMIT_SIGNATURE_INVALID\` | — |
| Declarar agent_id equivocado | Identity lookup falla | ✓ \`UNKNOWN_KEY\` o \`IDENTITY_MISMATCH\` | — |

### Actor: Atacante con acceso al store (escritura filesystem)

| ataque | qué puede conseguir | detecta verify | mitigación |
|--------|---------------------|-----------------|------------|
| Borrar commit | parent_missing en commits hijos | ✓ \`PARENT_MISSING\` | Backup |
| Modificar commit content | commit_id no coincide | ✓ \`COMMIT_INTEGRITY_INVALID\` | — |
| Modificar ControlEvent | firma root no verifica | ✓ (después de BUG 2 fix) \`CONTROL_CHAIN_INVALID\` | — |
| Modificar cutoff_head en ControlEvent | firma root no verifica (cutoff es parte del firmado) | ✓ \`CONTROL_CHAIN_INVALID\` | — |
| Duplicar commit con mismo commit_id | — | ✓ (después de BUG 1 fix) \`duplicate commit_id\` | — |
| Borrar ControlEvent del medio | Cadena rota | ✓ \`CONTROL_CHAIN_INVALID\` | — |
| Borrar IdentityRecord | Commits no verifican | ✓ \`UNKNOWN_IDENTITY\` | — |
| Borrar RootAuthority | verify_identity_layer skip (v0.1 fallback) | ⚠️ Puede pasar si hay identidad legacy | BUG 6: si se borra root_authority pero queda IdentityRecordV2, verify debería detectarlo |
| Crear ControlEvent con cutoff inexistente | ControlEvent válido pero cutoff roto | ❌ No detecta | BUG 3: verify no chequea que cutoff_head existe en el DAG |
| Modificar incomplete_compensation | No afecta verify | No detecta (no es parte de verify) | Documentar que incomplete_compensations no se verifican |

### Actor: Atacante con acceso a ChromaDB

| ataque | qué puede conseguir | detecta verify | mitigación |
|--------|---------------------|-----------------|------------|
| Modificar memoria en ChromaDB | Contenido distinto en ChromaDB | No detecta (verify no lee ChromaDB) | \`verify_correspondence()\` helper |
| Borrar memoria de ChromaDB | Memoria desaparece | No detecta | Mismo |
| Agregar memoria falsa a ChromaDB | Memoria sin commit | No detecta | Mismo |
| Corromper ChromaDB entero | Todas las memorias perdidas | No detecta (alethech intacto) | Recuperar desde alethech commits |

### Actor: Root comprometido

| ataque | qué puede conseguir | detecta verify | mitigación |
|--------|---------------------|-----------------|------------|
| Autorizar keys nuevas | Keys válidas | No detecta (es legítimo por diseño) | Multisig (rev 4+) |
| Revocar keys legítimas | Keys revocadas | No detecta | Multisig |
| Firmar dos cadenas de control distintas | Equivocation | No detecta sin red de testigos | Limitación fundamental declarada |
| Crear MigrationRecord falsa | Migración falsa | No detecta (firma root válida) | Verificar contra publicación externa |
| Cambiar cutoff_head retroactivamente | No puede (cutoff está en ControlEvent firmado) | ✓ Firma no verifica | — |

## bugs encontrados (5 auditorías)

| # | bug | severidad | estado |
|---|-----|-----------|--------|
| 1 | Duplicate commit_ids silenciosamente ignorados | 🔴 | ✓ FIXED (0.4.3) |
| 2 | verify_store no verificaba ControlEvents | 🔴 | ✓ FIXED (0.4.3) |
| 3 | cutoff_head inexistente no detectado | 🟡 | documentado, pendiente fix |
| 4 | idempotency_key con texto distinto no detecta conflicto | 🟡 | documentado, pendiente fix |
| 5 | JWK inválido en identity puede pasar verify | 🟡 | documentado, pendiente fix |
| 6 | Borrar RootAuthority pero dejar IdentityRecordV2 → verify pasa | 🟡 | identificado en threat model, pendiente test |

## lo que el protocolo demuestra

| propiedad | demostrado | cómo |
|-----------|------------|------|
| Integridad de commits | ✓ | SHA-256 + firma Ed25519 |
| Autoría criptográfica | ✓ | Cada commit firmado por key específica |
| Autorización de keys | ✓ | ControlEvent chain firmada por root |
| Rotación no destructiva | ✓ | cutoff_head + ancestry check |
| Migración bilateral | ✓ | MigrationRecord con dos firmas |
| Verificación offline | ✓ | Sin red, sin LLM, sin servicios |
| Cadena de control monotónica | ✓ | sequence + previous_control_hash |
| Detección de tampering | ✓ | commit_id recalculado vs declarado |
| Detección de corrupción | ✓ | JSON malformado, firma corrupta, parent faltante |
| Portabilidad | ✓ | export/import roundtrip preserva estado |

## lo que el protocolo NO demuestra

| propiedad | no demostrado | por qué |
|-----------|---------------|---------|
| Tiempo físico de creación | ✗ | timestamps son metadata, no prueba |
| Verdad del contenido | ✗ | la firma prueba autoría, no verdad |
| Existencia física de evento externo | ✗ | EvidenceCommit es atribución, no prueba del mundo |
| Estado global del sistema offline | ✗ | dos verifiers pueden ver cadenas distintas |
| Ausencia de forks desconocidos | ✗ | sin red de testigos, equivocation no se detecta |
| Consistencia entre ChromaDB y alethech | ✗ | verify no lee ChromaDB |
| Atomicidad ACID entre sistemas | ✗ | compensación best-effort, no transaccional |
| Inmutabilidad del almacenamiento | ✗ | el disco puede borrarse o modificarse |
| Que cutoff_head existe en el DAG | ✗ | BUG 3 — pendiente fix |
| Que idempotency_key con texto distinto produce conflicto | ✗ | BUG 4 — pendiente fix |
| Que JWK es válido | ✗ | BUG 5 — pendiente fix |

## revisión

- rev 1 (actual): threat model formal. REVIEW.
- rev 2 (futura): después de fixear BUGs 3, 4, 5, 6.

— self, threat model formal rev 1`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "threat-model-formal" } });
  if (existing) {
    console.log(`doc already exists (rev ${existing.revision}). skipping.`);
    return;
  }
  const doc = await db.doc.create({
    data: {
      slug: "threat-model-formal",
      title: "threat model formal",
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
