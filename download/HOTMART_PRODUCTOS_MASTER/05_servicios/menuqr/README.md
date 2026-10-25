# MenuQR Pro

> **Menús digitales con QR** para restaurantes. Self-hosted, multi-idioma, pedidos por mesa.

## Features

- 📱 **QR por mesa**: cada mesa tiene su QR único → menú + pedidos
- 📋 **Multi-categoría**: entradas, principales, postres, bebidas — ordena como quieras
- 🌍 **Multi-idioma**: español/inglés/portugués — toggle en tiempo real
- 🥗 **Tags dietarios**: vegetariano, vegano, gluten-free, picante
- 💰 **Moneda configurable**: USD, MXN, ARS, BRL, etc.
- 📦 **Pedidos desde QR**: cliente escanea → ve menú → pide → llega a cocina
- 🔄 **5 estados de orden**: pending → preparing → served → paid → cancelled
- 🎨 **QR personalizable**: color, fondo, logo opcional
- 🐳 **Docker-ready**

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/menuqr.git
cd menuqr
cp .env.example .env
pip install -e .
menuqr serve
```

## Uso

### CLI

```bash
# Agregar categorías
menuqr add-category --id entradas --name "Entradas" --sort 0
menuqr add-category --id principales --name "Platos Principales" --sort 1

# Agregar items
menuqr add-item --category entradas --name "Ceviche" --price 8.50 --desc "Pescado fresco, limón, cebolla"
menuqr add-item --category principales --name "Lomo Saltado" --price 14.00 --veggie

# Agregar mesas
menuqr add-table --number 1 --capacity 4 --location interior
menuqr add-table --number 2 --capacity 2 --location terraza

# Generar QR para una mesa
menuqr qr TBL-12345678 --out mesa1.png

# Listar items
menuqr list-items

# Ver pedidos
menuqr list-orders
```

### API REST

```bash
# Crear categoría
curl -X POST http://localhost:8008/admin/categories -d '{"id":"postres","name":"Postres"}'

# Crear item
curl -X POST http://localhost:8008/admin/items -d '{
  "category_id": "postres",
  "name": "Tiramisú",
  "price": 6.50,
  "is_vegetarian": true
}'

# Crear mesa
curl -X POST http://localhost:8008/admin/tables -d '{"number":1,"capacity":4}'

# Descargar QR de la mesa
curl -o mesa1.png http://localhost:8008/admin/tables/TBL-XXX/qr

# QR del menú general
curl -o menu.png http://localhost:8008/admin/menu/qr

# Cliente escanea QR → ve menú → hace pedido
curl -X POST "http://localhost:8008/public/order?table_id=TBL-XXX&notes=sin cebolla" \
  -d '[{"item_id":"ITM-001","qty":2},{"item_id":"ITM-002","qty":1}]'

# Ver pedidos
curl http://localhost:8008/admin/orders

# Actualizar estado
curl -X POST http://localhost:8008/admin/orders/ORD-XXX/status?status=preparing
```

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $47 | 1 local, 20 mesas, menú básico |
| Pro | $97 | 50 mesas, multi-idioma, pedidos |
| Premium | $197 | multi-local, marca blanca, integración POS |

© 2026 Eddy Flores.
