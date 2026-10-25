# CitaYa

> **Sistema de reservas/citas self-hosted** para clínicas, peluquerías, consultorios, spas. Calendario, recordatorios, multi-profesional.

## Features

- 📅 **Calendario automático**: genera slots según horarios de cada profesional
- 👥 **Multi-profesional**: cada uno con su horario, servicios y color en calendario
- ⏰ **Recordatorios automáticos**: email/Telegram/WhatsApp X horas antes
- 🔄 **Estados de cita**: pending → confirmed → completed/cancelled/no_show
- 🌐 **Widget público**: tus clientes reservan sin login
- 📧 **Notificaciones**: email (SMTP), Telegram, WhatsApp Cloud API
- 🔌 **API REST completa**: pública para reservar, admin para gestionar
- 🐳 **Docker-ready**

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/citaya.git
cd citaya
cp .env.example .env
pip install -e .
citaya serve
```

Abre `http://localhost:8005`.

## Uso

### Configurar profesionales y servicios

```bash
citaya add-professional --id DR01 --name "Dra. García" --specialty "Dermatología"
citaya add-professional --id DR02 --name "Dr. Pérez" --specialty "Odontología"

citaya add-service --id SRV01 --name "Consulta general" --duration 30 --price 50
citaya add-service --id SRV02 --name "Limpieza dental" --duration 60 --price 80
```

### Ver slots disponibles

```bash
citaya list-slots --professional-id DR01 --date 2026-10-26
```

### Reservar (CLI)

```bash
citaya book --professional-id DR01 --service-id SRV01 --start "2026-10-26T10:00" --name "Juan Pérez" --phone 593999123456
```

### API pública (widget embebible)

```bash
# Ver profesionales
curl http://localhost:8005/public/professionals

# Ver slots disponibles
curl "http://localhost:8005/public/slots?professional_id=DR01&date=2026-10-26"

# Reservar
curl -X POST http://localhost:8005/public/book -d '{
  "professional_id": "DR01",
  "service_id": "SRV01",
  "customer_name": "Juan Pérez",
  "customer_phone": "593999123456",
  "customer_email": "juan@x.com",
  "start_at": "2026-10-26T10:00"
}'
```

### API admin

```bash
# Ver todas las citas
curl http://localhost:8005/admin/appointments

# Confirmar
curl -X POST http://localhost:8005/admin/appointments/APT-12345/confirm

# Cancelar
curl -X POST "http://localhost:8005/admin/appointments/APT-12345/cancel?reason=cliente"
```

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 profesional, 100 citas/mes, widget público |
| Business | $197 | 5 profesionales, unlimited citas, recordatorios email |
| Premium | $297 | unlimited profesionales, multi-sucursal, marca blanca |

© 2026 Eddy Flores.
