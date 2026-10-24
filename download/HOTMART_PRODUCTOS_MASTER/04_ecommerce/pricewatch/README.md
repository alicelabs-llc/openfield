# PriceWatch

> **Monitor de precios** en MercadoLibre y Amazon. Alertas por email/Telegram/Discord cuando el precio baja. Self-hosted.

## Features

- 🛒 **2 stores**: MercadoLibre (LatAm) + Amazon (global)
- 💰 **4 condiciones de alerta**: below target / above target / drop % / any change
- 📧 **3 canales**: Email (SMTP) / Telegram / Discord webhook
- ⏰ **Scheduler**: APScheduler, default 60 min entre checks
- 📊 **Historial**: guarda cada price point, hasta 1000 por producto
- 🐳 **Docker-ready**: deploy en cualquier VPS
- 🆓 **Sin mensualidad**: pago único $47

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/pricewatch.git
cd pricewatch
cp .env.example .env
# Edit .env: set SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
pip install -e .
pricewatch serve
```

Abre `http://localhost:8003`.

## Uso

### CLI

```bash
# Trackear producto
pricewatch add "https://www.mercadolibre.com.ec/ML-123456789-iphone-15-_JM" --target 700 --email yo@gmail.com

# Listar productos
pricewatch list

# Forzar check
pricewatch check-all

# Quitar
pricewatch remove amazon_B0CHX1W1XY
```

### API REST

```bash
# Trackear
curl -X POST http://localhost:8003/v1/track \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.amazon.com/dp/B0CHX1W1XY",
    "target_price": 79.99,
    "alert_channels": ["email"],
    "alert_recipient": "yo@example.com"
  }'

# Listar
curl http://localhost:8003/v1/products

# Forzar check de uno
curl -X POST http://localhost:8003/v1/products/{pid}/check

# Historial de precios
curl http://localhost:8003/v1/products/{pid}/history
```

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | 50 productos, email alerts |
| Pro | $97 | 500 productos, Telegram + Discord |
| Agency | $197 | unlimited, multi-user, API |

© 2026 Eddy Flores.
