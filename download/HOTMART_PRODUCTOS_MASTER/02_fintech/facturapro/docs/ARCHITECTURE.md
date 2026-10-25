# Arquitectura — FacturaPro

## Componentes

```
Client → FastAPI server → {XML generator, PDF generator, Signer, SRI/PAC client}
```

### XML Generator (xml/generator.py)
- `generate_factura_xml_sri()`: Ecuador SRI v2.34
- `generate_cfdi_xml_4_0()`: Mexico CFDI 4.0
- Dispatch via country setting

### Signer (xml/signer.py)
- `wrap_with_xades_envelope()`: estructura XAdES-EPES
- `sign_xml()`: usa xmlsig + .p12 cert (dev mode si no hay cert)

### PDF Generator (pdf/generator.py)
- ReportLab con template corporativo
- Incluye emisor, cliente, detalles, totales, clave de acceso

### SRI Client (api/sri_client.py)
- SOAP envelopes para RecepcionComprobantesOffline + AutorizacionComprobantesOffline
- tenacity retries (3 intentos recepción, 5 para autorización)

### PAC Client (api/pac_client.py)
- REST genérico compatible con SW SAPIen, Facturama, BuzonE
- Basic auth con credenciales del PAC

## Clave de acceso (Ecuador)

49 dígitos:
- 8: fecha (ddmmyyyy)
- 2: tipo comprobante
- 2: tipo identificación
- 13: RUC
- 1: ambiente
- 3: establecimiento
- 3: punto emisión
- 9: secuencial
- 8: código numérico random
- 1: DV módulo 11

## Flujo completo

1. Cliente POST /v1/factura/create
2. Server genera clave + XML + PDF
3. Server guarda en data/facturas/{clave}/
4. Cliente POST /v1/factura/sign → envelope XAdES + firma
5. Cliente POST /v1/factura/send-sri → envío SOAP
6. SRI devuelve estado RECIBIDA o rechazada
7. Cliente poll /v1/factura/authorize/{clave} → estado AUTORIZADO
8. Cliente descarga PDF final
