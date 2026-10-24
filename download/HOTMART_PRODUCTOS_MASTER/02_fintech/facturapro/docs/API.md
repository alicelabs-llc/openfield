# API Reference — FacturaPro

Base URL: `http://localhost:8001`

## Endpoints

### `GET /`
Landing HTML.

### `GET /healthz`
```json
{"status":"ok","version":"1.0.0","country":"ecuador","ambiente":"producción","emisor_ruc":"0992345678001"}
```

### `POST /v1/factura/create`
Request body:
```json
{
  "cliente": {
    "ruc_cedula": "1712345670001",
    "razon_social": "CLIENTE SAC",
    "tipo_identificacion": "04",
    "email": "cliente@example.com"
  },
  "detalles": [
    {
      "codigo_principal": "P001",
      "descripcion": "Servicio consultoría",
      "cantidad": 10,
      "precio_unitario": 50.00,
      "iva_tarifa": 15
    }
  ],
  "tipo_comprobante": "01"
}
```

Response 200:
```json
{
  "clave_acceso": "251020240101001234567001200100100123456780000016",
  "secuencial": "001001000000001",
  "totales": {
    "subtotal_sin_impuestos": "500.00",
    "iva_total": "75.00",
    "importe_total": "575.00"
  },
  "xml_path": "/home/user/.facturapro/data/facturas/.../factura.xml",
  "pdf_path": "/home/user/.facturapro/data/facturas/.../factura.pdf",
  "estado": "borrador"
}
```

### `POST /v1/factura/sign`
Body: `{"xml": "<factura>..."}`
Response: `{"signed_xml": "...", "ambiente": "2"}`

### `POST /v1/factura/send-sri`
Body: `{"xml_signed_b64": "..."}`
Response: `{"success": true, "estado": "RECIBIDA", "mensajes": []}`

### `GET /v1/factura/authorize/{clave}`
Response: `{"success": true, "estado": "AUTORIZADO", "numero_autorizacion": "...", "fecha_autorizacion": "..."}`

### `POST /v1/factura/stamp-pac`
Body: `{"xml_b64": "..."}`
Response: `{"success": true, "uuid": "...", "sat_seal": "...", "fecha_timbrado": "..."}`

### `GET /v1/factura/pdf/{clave}`
Returns PDF binary (application/pdf).
