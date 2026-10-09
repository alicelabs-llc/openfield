# Hacktoberfest 2026 Week 1: Touch Grass — Plan de batalla

**Tema:** Touch Grass — construir algo con AI open-source que saque a la gente de la pantalla
**Premio:** $2,450 USD / 17 ganadores
**Deadline:** 11 oct 2026, 11:59 PM PDT (= 12 oct 06:59 UTC = 12 oct 01:59 Ecuador)
**Tiempo restante:** ~7 horas desde Ecuador (18:55 ahora)

---

## Reglas oficiales (confirmadas en dev.to)

1. **Proyecto nuevo**, construido durante el challenge
2. **AI open-source en el core**: open-weight model, open-source agent harness/framework, local inference (o los 3)
3. **Tema "Touch Grass"**: sacar gente al exterior (caminar, jardinería, birding, run clubs, otoño)
4. **El write-up es lo más importante** — calidad de escritura tiene mayor peso en judging
5. **Explicar por qué open importa**: sin internet, datos locales, modelo intercambiable, gratis
6. **Una submission por challenge**
7. **NO contar PRs a existentes este año**

---

## Idea de proyecto para ti: "Alethech Field Notes"

Combina lo que ya tienes (alethech-publish-2) con el challenge.

### Concepto

CLI de Python/Rust que:
1. Tomas fotos durante una caminata (drop folder)
2. Vision model local (Gemma 4B open-weight) genera field notes
3. EXIF GPS → mapa con tu ruta
4. Field notes + GPS se guardan en contenedor `.aleth` (alethech-publish-2)
5. Verificación criptográfica del recorrido (nadie puede modificar "estuve ahí" después)

### Por qué encaja perfecto contigo

- ✅ Tienes alethech-publish-2 (310 commits, MIT, listo)
- ✅ Skills en Python/Rust
- ✅ Tema "Touch Grass" — caminatas al aire libre
- ✅ AI open-source en el core (Gemma open-weight + alethech open-source)
- ✅ "Why open matters" — tus fotos con GPS nunca salen de tu laptop
- ✅ Write-up: tienes experiencia escribiendo docs (alethech-publish-2 tiene 19 docs)

### Arquitectura mínima viable (MVP)

```
[photos/] → [exif_read.py] → GPS + timestamps
                ↓
        [gemma 4b vision] → "field notes" (qué hay en cada foto)
                ↓
        [alethech commit] → verificación criptográfica
                ↓
        [markdown report] → map + notes + verification proof
```

### Stack propuesto

- **Vision model:** Gemma 3n 4B (open-weight, corre en CPU/GPU modesta)
  - Alternative: LLaVA 7B (también open-weight)
- **EXIF:** Python `pillow` o `exifread`
- **Maps:** Leaflet + OpenStreetMap (no API key)
- **Storage:** alethech `.aleth` container
- **Frontend:** markdown estático (es lo que piden — write-up pesa más que UI)

### Tiempo realista

| Componente | Tiempo |
|-----------|--------|
| Setup: Gemma local + alethech | 1h |
| EXIF reader (Python) | 30 min |
| Vision → field notes | 2h |
| Alethech integration | 1h |
| Markdown report generator | 1h |
| **Demo + screenshots** | 1h |
| **Write-up para DEV** | 2h |
| **Total** | ~8.5 horas |

Tienes ~7 horas hasta deadline. Ajuste: simplificar MVP — saltar el mapa, solo field notes + verificación.

---

## Plan de ejecución HOY (8 oct, 19:00 Ecuador)

### Bloque 1 (19:00-21:00, 2h) — Setup

1. Instalar Gemma local (via Ollama o llama.cpp)
2. Verificar alethech-publish-2 funciona
3. Tomar 5-10 fotos de una caminata rápida (literalmente "touch grass")

### Bloque 2 (21:00-23:00, 2h) — MVP

1. Script Python: leer EXIF de fotos
2. Script Python: enviar foto a Gemma, pedir "what do you see in 1 sentence?"
3. Script Python: guardar field notes en .aleth container

### Bloque 3 (23:00-01:00, 2h) — Demo

1. Generar markdown report con photos + notes + verification
2. Subir repo a GitHub (con MIT license)
3. Tomar screenshots

### Bloque 4 (01:00-02:00, 1h) — Write-up

1. Post en DEV explicando proyecto
2. Tags: `#devchallenge #hf26challenge #hacktoberfest`
3. Explicar "why open matters": photos nunca salen de tu laptop
4. Submit

**Deadline real:** 12 oct 01:59 Ecuador. Tienes hasta la madrugada.

---

## Si no alcanzas para Week 1

**Está bien.** Quedan 3 semanas más:

| Semana | Tema se revela | Deadline |
|--------|----------------|----------|
| Week 2 | 12 oct | 18 oct |
| Week 3 | 19 oct | 25 oct |
| Week 4 | 26 oct | 1 nov |

Cada semana = $2,450 USD / 17 ganadores. Si participas en 1 sola y ganas, son $2,450 USD.

---

## ¿Por qué esto es MEJOR que los PRs que estábamos haciendo

| Antes (PRs a OSS) | Ahora (DEV Challenges) |
|-------------------|------------------------|
| 6 PRs merged → 0 USD | 1 submission aceptada → $2,450 USD |
| Track record (largo plazo) | Premio inmediato (corto plazo) |
| Requiere maintainer approve | Solo judges + write-up |
| Sin tema específico | Tema claro ("Touch Grass") |

**Combinar ambos:**
- PRs merged → portfolio para Outreachy/DoraHacks (largo plazo)
- DEV Challenges → premio inmediato + write-up cuenta como portfolio (corto plazo)

---

## Acción inmediata

### Decisión

**Opción A (recomendada):** Empezar Touch Grass HOY. Tienes 7 horas. Posibilidad real de $2,450 USD.

**Opción B:** Esperar a Week 2 (12 oct). Más tiempo, pero pierdes oportunidad.

**Opción C:** Solo PRs a OSS (no DEV Challenges). Track record, sin premio Hacktoberfest.

¿Cuál eliges? Si A, empiezo a preparar el repo + scripts ahora.
