# DoraHacks / Dora Grant DAO — Plan de aplicación

**URL:** https://dorahacks.io
**Tipo:** Grant para proyectos OSS / "Public Good"
**Reward:** Variable — hasta $50,000 USD según round
**Cohortes:** Continuo, ~6-8 rounds al año

---

## Cómo funciona DoraHacks

DoraHacks opera 2 mecanismos:

### 1. Buidls (hackathons)
- Hackathons online con temas específicos
- Submit proyecto + demo
- Jury + community voting decide ganadores
- Prize pool típico: $5,000 - $50,000 USD
- Requisito: debe ser open source (Apache 2.0 o MIT)

### 2. Dora Grant DAO (grants continuos)
- Submit BUIDL page con tu proyecto
- Recurring rounds cada ~2 meses
- Community vota con DORA tokens (o quadratic voting)
- Funding perpetuo si tu proyecto recibe votos
- Para proyectos OSS de "public good"

---

## ¿Alethech califica?

**SÍ.** Tu repo `alethech-publish-2` cumple:

| Criterio DoraHacks | ¿Alethech cumple? |
|--------------------|-------------------|
| Open source | ✅ MIT licensed |
| Repo público | ✅ github.com/eddyflores100-lang/alethech |
| README claro | ✅ Tiene badges, descripción, examples |
| Demo funcional | ✅ CLI commands funcionan |
| Unique value prop | ✅ "Cryptographically verifiable agent memory" |
| Active development | ✅ Commits recientes |
| Community appeal | ⚠️ Necesita star count + users |

### Lo que falta para que sea competitivo

1. **Star count**: DoraHacks valora community signal. Actualmente tienes 0 stars en alethech-publish-2 (repos públicos pero sin promoción).
2. **Demo video**: 2-3 min mostrando el flujo `init → commit → verify → export`
3. **Use cases documentados**: casos reales de uso (agent continuity, audit log, supply chain verification)
4. **Traction**: al menos 10-50 stars, ideally 1-2 contributors externos

---

## Acciones concretas para hacer alethech "DoraHacks-ready"

### Fase 1 (oct 2026, durante Hacktoberfest)

1. **Pulir README principal** (ya está decente, necesita 1-2 diagrams)
2. **Crear demo video** 3 min en español + inglés
3. **Publicar en dev.to / Hacker News** 1 post técnico
4. **Listar en awesome-lists**: awesome-agent-memory, awesome-crypto, awesome-python
5. **Meta:** 10 stars + 100 PyPI downloads

### Fase 2 (nov-dic 2026)

1. **Submit a Dora Grant DAO** — crear BUIDL page
2. **Buscar 1-2 contributors externos** (puede ser via Hacktoberfest 2026)
3. **Publicar v0.5 release** con changelog claro
4. **Cross-promote** en /r/LocalLLaMA, /r/MachineLearning, /r/cryptography
5. **Meta:** 50 stars + 1000 PyPI downloads

### Fase 3 (Q1 2027)

1. **Apply a DoraHacks hackathon** temático (crypto, AI agents, privacy)
2. **Demo day** presentation de 5 min
3. **Meta:** $5,000 - $25,000 USD en grant

---

## BUIDL page template (draft)

```markdown
# Alethech — Cryptographically Verifiable Agent Memory

**Tagline:** Local-first, zero-LLM, zero-blockchain protocol for AI agent memory continuity.

## Problem
AI agents (LLM-based) lose context between sessions. Existing solutions 
(mem0, chromadb, langchain memory) trust the agent's own memory log without 
cryptographic verification — making them vulnerable to tampering, both 
accidental and malicious.

## Solution
Alethech signs memory commits with Ed25519, links them in a hash-linked DAG, 
rotates keys without losing identity, and seals verified history into encrypted 
.aleth files for portable transfer between runtimes.

## Why DoraHacks should fund this
- Public good: useful for any AI agent framework (LangChain, MemGPT, AutoGen, etc.)
- Open protocol: MIT licensed, no vendor lock-in
- Active development: 200+ commits, 9 CLI commands, 14 tests with mutation guards
- No dependencies on blockchains or LLMs

## Roadmap
- Q4 2026: v0.5 release, MCP registry, dev.to launch
- Q1 2027: Cross-runtime verification (Python ↔ Rust ↔ WASM)
- Q2 2027: Browser extension for chat capture
- Q3 2027: Conformance test suite for third-party implementations

## Funding ask
$5,000 USD para:
- Bounty program for contributors (Hacktoberfest + December)
- Hosting para conformance test vectors
- Domain + landing page profesional
- 1 mes de marketing (dev.to, HN, Twitter)

## Team
- Edison Flores (@eddyflores100-lang)
- Public track record: 6 PRs merged en OpenMW, Inkscape, F-Droid (oct 2026)
- 5 años de experiencia en Python/Rust

## Links
- Repo: https://github.com/eddyflores100-lang/alethech
- PyPI: https://pypi.org/project/alethech/
- Docs: https://eddyflores100-lang.github.io/alethech/
- Demo video: [pendiente]
```

---

## Acciones inmediatas (hoy)

### Script para preparar alethech

```bash
bash /home/z/my-project/scripts/dorahacks_setup.sh
```

Ese script:
1. Genera report de "DoraHacks readiness" del repo actual
2. Identifica gaps (stars, demo, docs)
3. Crea lista de tareas priorizadas para octubre

### Pasos manuales que necesitas hacer tú

1. **Crear cuenta en DoraHacks** (si no tienes): https://dorahacks.io/auth
2. **Crear cuenta en DoraHacks IDE** (para submitir BUIDL): https://Ide.dorahacks.io
3. **Conectar wallet** (opcional pero recomendado para Dora Grant DAO)

### Cronograma propuesto

| Fecha | Acción |
|-------|--------|
| Hoy | Revisar plan, crear cuenta DoraHacks |
| 7 oct | Ejecutar dorahacks_setup.sh, ver gaps |
| Octubre | Durante Hacktoberfest, ganar stars |
| 1 nov | Publicar v0.5 release de alethech |
| 15 nov | Demo video subido a YouTube |
| 1 dic | Submit BUIDL a Dora Grant DAO |
| Q1 2027 | Apply a DoraHacks hackathon temático |
