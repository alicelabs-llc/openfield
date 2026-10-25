# WhatsAppBot Pro

> **Bot de WhatsApp** para negocios LATAM. Catálogo de productos, pedidos automáticos, flujos conversacionales. Self-hosted vía WhatsApp Cloud API oficial.

## Features

- 💬 **Flujos conversacionales** sin programar: catálogo, carrito, checkout
- 🛒 **Catálogo gestionable**: agrega/quita productos vía CLI o API
- 📦 **Pedidos automáticos**: el cliente compra sin abandonar WhatsApp
- 🔍 **Búsqueda**: "buscar camiseta" → resultados relevantes
- 📊 **API admin**: gestión de catálogo + pedidos via REST
- ✅ **WhatsApp Cloud API oficial** (no librería no-oficial de ban riesgo)
- 🐳 **Docker-ready**
- 🆓 **Sin mensualidad**: pago único $97

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/wabotpro.git
cd wabotpro
cp .env.example .env
# Edit .env: set WA_VERIFY_TOKEN, WA_ACCESS_TOKEN, WA_PHONE_NUMBER_ID from Meta
pip install -e .
wabotpro serve
```

Configura el webhook en Meta dashboard:
- URL: `https://tu-dominio.com/webhook`
- Verify token: el mismo que pusiste en `WA_VERIFY_TOKEN`
- Subscribed fields: `messages`

## Uso

### Agregar productos al catálogo

```bash
wabotpro add-product --id P001 --name "Camiseta" --price 15.00 --stock 10
wabotpro add-product --id P002 --name "Pantalón" --price 35.00 --stock 5
wabotpro catalog
```

### Probar flujos sin WhatsApp

```bash
wabotpro simulate --from-number 593999123456 --text "hola"
wabotpro simulate --text "catálogo"
wabotpro simulate --text "agregar P001 2"
wabotpro simulate --text "carrito"
wabotpro simulate --text "confirmar"
```

### Ver pedidos

```bash
wabotpro orders
```

### API REST

```bash
# Gestión de catálogo
curl http://localhost:8004/v1/catalog
curl -X POST http://localhost:8004/v1/catalog -d '{"id":"P001","name":"Camiseta","price":15.00}'

# Ver pedidos
curl http://localhost:8004/v1/orders

# Enviar mensaje directo
curl -X POST "http://localhost:8004/v1/send?to=593999123456&text=Hola%20cliente"

# Simular mensaje entrante (para testing)
curl -X POST "http://localhost:8004/v1/simulate?from_number=593999123456&text=catálogo"
```

## Comandos que entiende el bot

| Comando | Descripción |
|---------|-------------|
| `hola` / `menu` / `inicio` | Ver menú principal |
| `catálogo` / `productos` | Ver productos disponibles |
| `agregar P001 2` | Agregar 2 unidades del P001 al carrito |
| `quitar P001` | Quitar P001 del carrito |
| `carrito` | Ver contenido del carrito |
| `buscar camiseta` | Buscar "camiseta" en catálogo |
| `confirmar` / `pedido` | Finalizar pedido |
| `ayuda` / `help` | Ver todos los comandos |

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 negocio, 50 productos, 100 pedidos/mes |
| Business | $197 | 3 negocios, 500 productos, unlimited pedidos |
| Agency | $297 | unlimited negocios, marca blanca |

© 2026 Eddy Flores.
