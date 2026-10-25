# API Reference — ScamShield Pro

Base URL: `http://localhost:8000` (cambia según tu deployment)

## Autenticación

Si `API_KEY` está configurado en `.env` (recomendado en producción), todas las rutas `/v1/*` requieren el header:

```
X-API-Key: <tu-api-key>
```

Si no está configurado o es `changeme-please-replace-this`, el servidor opera en modo dev sin auth.

---

## Endpoints

### `GET /`

Landing page HTML (interactiva, con demo en vivo).

### `GET /dashboard`

Dashboard HTML para escanear URLs desde el navegador.

### `GET /healthz`

Health check para Docker / Kubernetes / monitoring.

**Response 200:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "checks_enabled": [
    "domain_age", "ssl_certificate", "dns_records", "tld_reputation",
    "redirect_chain", "content_analysis", "phishing_patterns",
    "blocklist_check", "ip_reputation"
  ]
}
```

### `POST /v1/scan`

Escanea una URL y devuelve el trust score + breakdown completo.

**Request body:**

| Field             | Type    | Required | Default | Description                              |
|-------------------|---------|----------|---------|------------------------------------------|
| `url`             | string  | ✓        | —       | URL a analizar                          |
| `follow_redirects`| bool    | ✗        | `true`  | Seguir redirects                         |
| `fetch_content`   | bool    | ✗        | `true`  | Fetch & analizar HTML                    |
| `timeout`         | float   | ✗        | `10.0`  | Timeout por request (1-60s)              |

**Response 200 — `ScanResult`:**
```json
{
  "url": "https://example.com",
  "normalized_url": "https://example.com",
  "final_url": "https://example.com",
  "domain": "example.com",
  "tld": ".com",
  "scanned_at": "2026-10-24T15:30:00",
  "duration_ms": 823,
  "trust_score": {
    "value": 92,
    "verdict": "very_likely_safe",
    "positive_signals": 6,
    "negative_signals": 0,
    "confidence": 90
  },
  "checks": [
    {
      "name": "domain_age",
      "passed": true,
      "severity": "high",
      "weight": 25,
      "message": "Domain age: 10592 days (29 years) — well established",
      "details": { "age_days": 10592 }
    },
    {
      "name": "ssl_certificate",
      "passed": true,
      "severity": "high",
      "weight": 20,
      "message": "Valid SSL certificate issued by DigiCert Inc",
      "details": { "issuer": "DigiCert Inc", "expires_on": "Mar 14 23:59:59 2027 GMT" }
    }
  ],
  "ip_address": "93.184.216.34",
  "server_country": "United States",
  "domain_age_days": 10592,
  "ssl_valid": true,
  "redirect_count": 0
}
```

**Response 400** — URL inválida:
```json
{ "detail": "URL must be a non-empty string" }
```

**Response 429** — Rate limit excedido:
```json
{ "detail": "Rate limit exceeded (60/min)" }
```

### `POST /v1/scan/bulk`

Escanea hasta 100 URLs en secuencia. Útil para batch processing nocturno.

**Request body:**
```json
{
  "urls": [
    "https://a.com",
    "https://b.com",
    "https://c.com"
  ]
}
```

**Response 200** — Array de `ScanResult` (mismo schema que `/v1/scan`).

### `GET /v1/checks`

Lista todos los detectores habilitados con su metadata.

**Response 200:**
```json
[
  {
    "name": "domain_age",
    "severity": "high",
    "weight": 25,
    "requires_network": true,
    "requires_content": false,
    "description": "Domain age check — newer domains are riskier."
  },
  ...
]
```

---

## Ejemplos

### cURL

```bash
# Scan simple
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}' | jq '.trust_score'

# Con API key
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"url": "https://suspicious-site.xyz/free-iphone"}'

# Filtro solo del score
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq '{score: .trust_score.value, verdict: .trust_score.verdict}'
```

### Python (requests)

```python
import requests

r = requests.post(
    "http://localhost:8000/v1/scan",
    json={"url": "https://example.com", "fetch_content": False},
    headers={"X-API-Key": "your-key"},
)
data = r.json()
print(f"Score: {data['trust_score']['value']}/100")
print(f"Verdict: {data['trust_score']['verdict']}")
for c in data["checks"]:
    icon = "✓" if c["passed"] else "✗"
    print(f"  {icon} {c['name']}: {c['message']}")
```

### JavaScript (fetch)

```javascript
const res = await fetch('/v1/scan', {
  method: 'POST',
  headers: {'Content-Type': 'application/json', 'X-API-Key': apiKey},
  body: JSON.stringify({url: 'https://example.com', fetch_content: false})
});
const data = await res.json();
console.log(`Score: ${data.trust_score.value}/100`);
```

---

## Rate limits

| Plan (Hotmart)        | Rate limit                 | Notes                                |
|-----------------------|----------------------------|--------------------------------------|
| Single Dev ($47)      | 60 req/min por IP (default)| Single instance                     |
| Pro ($97)             | 60 req/min por IP          | Multi-instance compartido via Redis  |
| Agency ($197)         | Customizable               | Override `RATE_LIMIT_PER_MINUTE`     |

El rate limit se aplica por IP del cliente, no por API key. Si necesitas rate limiting por key,es un customization request.

---

## Errores comunes

| HTTP | Causa                                    | Solución                                   |
|------|------------------------------------------|--------------------------------------------|
| 400  | URL vacía o scheme inválido              | Verifica que sea `http://` o `https://`    |
| 401  | Falta `X-API-Key` o es incorrecta        | Revisa `.env` y header                     |
| 422  | JSON mal formado o schema incorrecto    | Verifica el body                           |
| 429  | Rate limit excedido                       | Espera 60s o sube el límite en `.env`      |
| 500  | Scan fallido (normalmente red)            | Revisa logs del servidor                   |
| 502  | No llega al servidor                     | Verifica que `uvicorn` esté corriendo       |
