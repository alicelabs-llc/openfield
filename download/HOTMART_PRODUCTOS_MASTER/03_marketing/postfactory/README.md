# PostFactory

> **Generador de contenido para redes sociales con IA.** 7 tipos de contenido, 7 plataformas, hashtags auto, calendario. Self-hosted.

## Features

- 📝 **7 tipos de contenido**: educational, promotional, engagement, storytelling, behind_scenes, listicle, how_to
- 🌐 **7 plataformas**: Instagram, LinkedIn, Twitter, TikTok, Facebook, YouTube, Blog
- 🎯 **Hashtags automáticos**: por nicho (10 categorías) + topic-derived + límites por plataforma
- 📅 **Calendario de contenido**: genera N días de posts con horarios óptimos por plataforma
- 🤖 **Multi-provider IA**: Z.ai (barato), OpenAI, Anthropic, o templates gratis
- 🆓 **Modo template**: funciona sin IA (gratis forever)
- ⏰ **Best posting times**: por plataforma (Instagram 7-9h, LinkedIn 8-10h, etc.)
- 🐳 **Docker-ready**

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/postfactory.git
cd postfactory
cp .env.example .env
pip install -e .
postfactory serve
```

## Uso

### CLI

```bash
# Generar posts (template mode, gratis)
postfactory generate "marketing digital" --platform instagram --type educational --mode template

# Generar con IA
postfactory generate "productividad" --platform linkedin --type how_to --variations 5

# Solo hashtags
postfactory hashtags "fitness motivation" --niche fitness --platform instagram

# Calendario de 7 días
postfactory calendar --days 7 --platforms "instagram,linkedin"
```

### API REST

```bash
# Generar (template mode)
curl -X POST "http://localhost:8007/v1/generate?mode=template" \
  -d '{"topic":"marketing","platform":"instagram","content_type":"educational","variations":3}'

# Hashtags
curl "http://localhost:8007/v1/hashtags?topic=marketing&niche=marketing&platform=instagram&count=10"

# Calendario
curl -X POST http://localhost:8007/v1/calendar \
  -d '{"days":7,"platforms":["instagram","linkedin"]}'
```

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | Template mode + 50 AI calls/día |
| Pro | $97 | 500 AI calls/día + calendario |
| Agency | $197 | unlimited + multi-client + marca blanca |

© 2026 Eddy Flores.
