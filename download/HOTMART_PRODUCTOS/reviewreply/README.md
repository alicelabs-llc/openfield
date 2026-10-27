# ReviewReply AI

> **Generador de respuestas a reseñas con IA.** Google Reviews, Yelp, App Store, Trustpilot, Facebook. Self-hosted, con fallback a templates sin IA.

## Features

- 🤖 **IA multi-provider**: Z.ai (GLM), OpenAI, Anthropic, o templates locales
- 🎭 **Detección de sentimiento**: positive / negative / neutral / mixed
- 🏷️ **Extracción de temas**: servicio, producto, comida, precio, entrega, limpieza, ambiente
- 📝 **3 variantes por reseña**: corto / medio / detallado
- 🌐 **Multi-plataforma**: Google Reviews, Yelp, App Store, Trustpilot, Facebook, Amazon
- 🆓 **Modo template**: funciona sin IA (gratis forever)
- 🔄 **Modo batch**: hasta 50 reseñas por request
- 🇪🇸 **Español primero** + soporte multi-idioma

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/reviewreply.git
cd reviewreply
cp .env.example .env
# Edit .env: set AI_API_KEY for AI mode (optional — template mode works free)
pip install -e .
reviewreply serve
```

## Uso

### CLI

```bash
# Generar respuestas (modo AI)
reviewreply generate --rating 5 --text "Excelente servicio" --author "Juan"

# Generar respuestas (modo template, sin IA)
reviewreply generate --rating 1 --text "Pésimo" --author "Pedro" --mode template

# Ver configuración
reviewreply config
```

### API REST

```bash
# Generar respuestas (AI mode)
curl -X POST http://localhost:8006/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "google_reviews",
    "rating": 1,
    "text": "Servicio lento, comida fría",
    "author_name": "Pedro"
  }'

# Generar respuestas (template mode, gratis)
curl -X POST "http://localhost:8006/v1/generate?mode=template" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "text": "Excelente", "author_name": "Maria"}'

# Batch (hasta 50)
curl -X POST http://localhost:8006/v1/generate/batch \
  -d '{"reviews": [{"rating":1,"text":"malo"},{"rating":5,"text":"bueno"}]}'
```

### Response structure

```json
{
  "review_summary": "Cliente menciona servicio lento y comida fría",
  "detected_sentiment": "negative",
  "suggestions": [
    {"text": "Hola Pedro. Lamentamos tu experiencia...", "tone": "corto", "word_count": 12},
    {"text": "Hola Pedro. Lamentamos mucho que...", "tone": "medio", "word_count": 65},
    {"text": "Hola Pedro. Leímos tu reseña y sentimos mucho...", "tone": "detallado", "word_count": 150}
  ],
  "model_used": "glm-4.6"
}
```

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | Template mode + 100 AI calls/día |
| Pro | $97 | 1000 AI calls/día + Google Business API connector |
| Agency | $197 | unlimited AI + multi-business + marca blanca |

© 2026 Eddy Flores.
