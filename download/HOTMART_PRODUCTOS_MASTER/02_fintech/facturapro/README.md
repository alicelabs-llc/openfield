# FacturaPro

> **Facturación electrónica self-hosted** para Ecuador (SRI v2.34) y México (CFDI 4.0). Genera XML firmado, PDF imprimible, envía al SRI/PAC.

## Por qué FacturaPro

- ✅ **Multi-país**: Ecuador (SRI esquema offline v2.34) + México (CFDI 4.0 SAT)
- ✅ **Self-hosted**: tus facturas nunca salen de tu servidor
- ✅ **Sin suscripción mensual**: pago único $97-$297
- ✅ **Código fuente incluido**: customiza si necesitas
- ✅ **API REST + CLI + Dashboard**: integra con tu ERP/CRM en minutos
- ✅ **PDF imprimible**: reportlab, template personalizable
- ✅ **XAdES-EPES signing**: listo para certificado .p12/.pfx

## Quick Start

```bash
git clone https://github.com/eddyflores100-lang/facturapro.git
cd facturapro
cp .env.example .env
pip install -e .
facturapro serve
```

Abre `http://localhost:8001`.

## Uso

### CLI

```bash
# Crear factura interactiva
facturapro create

# Ver configuración
facturapro config

# Validar clave de acceso
facturapro validate-clave 251020240101001234567001200100100123456780000016

# Firmar XML
facturapro sign factura.xml --out factura_signed.xml
```

### API REST

```bash
# Crear factura
curl -X POST http://localhost:8001/v1/factura/create \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": {"ruc_cedula":"1712345670001","razon_social":"CLIENTE SAC","tipo_identificacion":"04"},
    "detalles": [{"codigo_principal":"P001","descripcion":"Servicio","cantidad":2,"precio_unitario":100,"iva_tarifa":15}]
  }'

# Firmar (devuelve XML con envelope XAdES)
curl -X POST http://localhost:8001/v1/factura/sign \
  -H "Content-Type: application/json" \
  -d '{"xml":"<factura>...</factura>"}'

# Enviar al SRI (Ecuador)
curl -X POST http://localhost:8001/v1/factura/send-sri \
  -H "Content-Type: application/json" \
  -d '{"xml_signed_b64":"..."}'

# Stamp con PAC (México)
curl -X POST http://localhost:8001/v1/factura/stamp-pac \
  -d '{"xml_b64":"..."}'

# Consultar autorización
curl http://localhost:8001/v1/factura/authorize/CLAVE_ACCESO

# Descargar PDF
curl -o factura.pdf http://localhost:8001/v1/factura/pdf/CLAVE_ACCESO
```

## Flujo

```
1. POST /v1/factura/create → genera XML + PDF + clave acceso
2. POST /v1/factura/sign → envuelve XML en XAdES-EPES + firma con .p12
3. POST /v1/factura/send-sri → envía al SRI (Ecuador) o stamp-pac (México)
4. GET  /v1/factura/authorize/{clave} → poll por autorización
5. GET  /v1/factura/pdf/{clave} → descarga PDF
```

## Detectores / Características

| Feature | Ecuador SRI | México CFDI 4.0 |
|---------|-------------|-----------------|
| XML schema | v2.34 offline | CFDI 4.0 |
| IVA default | 15% | 16% |
| Identificación | RUC/cedula | RFC |
| Firma | XAdES-EPES | Sello digital |
| Envío | SOAP SRI | PAC REST |
| Clave | 49 dígitos + DV mod 11 | UUID PAC |

## Pricing

| Plan | Precio | Incluye |
|------|--------|---------|
| Starter | $97 | 1 emisor, ambiente pruebas, 100 facturas/mes |
| Business | $197 | 3 emisores, ambiente producción, unlimited |
| Multi | $297 | unlimited emisores, multi-empresa, API |

## License

Single-User Lifetime License. © 2026 Eddy Flores.
