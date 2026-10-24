# LicitAlert

> **Alertas de licitaciones públicas**. Monitorea SECOP (Colombia), SERCOP (Ecuador), CompraNet (México). Self-hosted.

## Features

- 🌎 **3 países**: Colombia (SECOP II), Ecuador (SERCOP), México (CompraNet)
- 🔔 **Alertas multi-canal**: email + Telegram
- 🎯 **Filtros avanzados**: keywords, país, rango de presupuesto, categoría, exclusión
- 📊 **Scoring de relevancia**: 0-100 basado en matches de keywords
- 🤖 **Scheduler automático**: APScheduler check cada N horas (default 6)
- 💾 **Cache persistente**: hasta 1000 licitaciones en disco
- 🐳 **Docker-ready**

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/licitalert.git
cd licitalert
cp .env.example .env
# Edit .env: set SMTP_* for email alerts, TELEGRAM_BOT_TOKEN for telegram
pip install -e .
licitalert serve
```

## Uso

### CLI

```bash
# Crear alerta
licitalert add-alert --name "Software Colombia" \
  --countries co \
  --keywords "software,desarrollo,sistemas" \
  --email yo@empresa.com

# Listar alertas
licitalert list-alerts

# Force check ahora
licitalert check-now

# Ver licitaciones cacheadas
licitalert list-tenders --country co --limit 20

# Eliminar alerta
licitalert remove-alert RULE-ABC12345
```

### API REST

```bash
# Crear regla de alerta
curl -X POST http://localhost:8009/v1/rules -d '{
  "name": "Construcción LatAm",
  "countries": ["co", "mx"],
  "keywords": ["construccion", "obra", "infraestructura"],
  "min_budget": 1000000,
  "alert_channels": ["email"],
  "alert_recipient": "yo@empresa.com"
}'

# Listar reglas
curl http://localhost:8009/v1/rules

# Ver licitaciones cacheadas
curl http://localhost:8009/v1/tenders?country=co&limit=50

# Forzar check async
curl -X POST http://localhost:8009/v1/check
```

## Cómo funciona

1. **Cada 6 horas** (configurable), APScheduler dispara `run_check_cycle()`
2. Service llama a scrapers de Colombia/Ecuador/México en paralelo
3. Tenders nuevos se guardan en `~/.licitalert/data/tenders.json`
4. Engine de matching compara tenders vs todas las reglas activas
5. Agrupa matches por regla + destinatario
6. Envía alertas por email/Telegram con tabla HTML

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 país, 5 alertas, email |
| Pro | $197 | 3 países, 50 alertas, Telegram |
| Agency | $297 | unlimited países, multi-user, API |

© 2026 Eddy Flores.
