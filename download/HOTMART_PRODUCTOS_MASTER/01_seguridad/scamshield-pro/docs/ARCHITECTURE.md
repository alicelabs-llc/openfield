# Arquitectura — ScamShield Pro

## Visión general

ScamShield Pro es un servicio **self-hosted** monolítico: API REST + CLI + dashboard web embebido en un único binario Python. No requiere Redis, Postgres ni Kubernetes para empezar — solo Python 3.10+ y disco para el cache.

```
┌─────────────────────────────────────────────────────────────────┐
│   Browser / curl / Python client / webhook integration          │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│   FastAPI server  (scamshield/server.py)                         │
│   • CORS, rate limit, auth                                       │
│   • Routes: /, /dashboard, /healthz, /v1/scan, /v1/scan/bulk,   │
│             /v1/checks                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│   Scanner  (scamshield/scanner.py)                               │
│   • Normalizes URL                                                │
│   • Builds CheckContext                                           │
│   • Phase 1 (parallel): all checks not requiring HTML content     │
│   • Phase 2 (sequential): content-dependent checks                │
│   • Aggregates via compute_score() → TrustScore                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
       ┌─────────────────┼──────────────────────┐
       ▼                 ▼                      ▼
┌──────────────┐ ┌──────────────┐ ┌────────────────────┐
│ DomainAge    │ │ SSL Check    │ │ DNS Check          │ ...
│ (WHOIS)      │ │ (socket)     │ │ (dnspython)        │
└──────┬───────┘ └──────┬───────┘ └─────────┬──────────┘
       │                │                   │
       ▼                ▼                   ▼
   python-whois    ssl.create_default    dns.resolver
                   _context()            .Resolver()
```

## Componentes clave

### 1. CheckContext (estado compartido)

`scamshield/checks/base.py` define `CheckContext`, un dataclass que viaja a través de todos los checks:

```python
@dataclass
class CheckContext:
    url: str                     # URL original del request
    normalized_url: str          # URL canónica
    domain: str                  # e.g. "example.com"
    tld: str                     # e.g. ".com"
    follow_redirects: bool
    fetch_content: bool
    timeout: float

    # Populated progresivamente:
    ip_address: str | None
    final_url: str | None
    redirect_chain: list[str]
    http_status: int | None
    http_headers: dict[str, str]
    html_content: str | None
    ssl_cert: Any
    whois_info: dict[str, Any]
    dns_records: dict[str, list[str]]
    server_country: str | None
    domain_age_days: int | None
    ssl_valid: bool | None
    redirect_count: int | None
```

Los checks se ejecutan en orden, y cada uno puede leer lo que los anteriores escribieron. Por ejemplo, `ContentCheck` necesita `ctx.final_url` (escrito por `RedirectChainCheck`); `ReputationCheck` necesita `ctx.ip_address` (escrito por `DNSCheck`).

### 2. BaseCheck (interfaz común)

Todos los detectores heredan de `BaseCheck`:

```python
class BaseCheck(abc.ABC):
    name: str
    severity: str           # info|low|medium|high|critical
    weight: int             # 0-100, puntos restados al fallar
    requires_network: bool
    requires_content: bool

    async def run(self, ctx: CheckContext) -> CheckResult: ...
```

Cada check devuelve un `CheckResult` con `passed`, `severity`, `weight`, `message`, `details`.

### 3. Scanner (orquestador)

El motor (`scamshield/scanner.py`) ejecuta los checks en dos fases:

- **Fase 1 (paralela)**: todos los checks que no requieren HTML content. Usan `asyncio.gather()` para maximizar throughput.
- **Fase 2 (secuencial)**: checks que necesitan `ctx.html_content`. Se ejecutan uno a uno porque dependen del `final_url` resuelto en fase 1.

El `compute_score()` del módulo `scamshield/core/scoring.py` agrega todos los `CheckResult`:

```python
score = 75  # baseline neutral-leaning-safe
for check in checks:
    if check.passed:
        if check.weight >= 30:
            score += min(check.weight // 12, 5)  # bonus por pasar checks críticos
    else:
        penalty = check.weight
        if check.severity == "critical":
            penalty *= 1.5  # criticals pesan más
        score -= penalty
score = clamp(score, 1, 100)
```

### 4. Cache

`scamshield/utils/cache.py` envuelve `diskcache.Cache` con TTL configurable (default 24h). Reduce drásticamente la repetición de lookups WHOIS/DNS para los mismos dominios.

### 5. Rate limiting

In-memory, per-IP, usando un deque por IP con timestamps. Default 60 requests/minuto. Si se excede, devuelve HTTP 429.

## Decisiones de diseño

### ¿Por qué FastAPI y no Flask?

FastAPI tiene:
- Async nativo (crítico para hacer 9 checks paralelos)
- Pydantic schemas automáticos
- OpenAPI docs out-of-the-box
- Mejor rendimiento (Starlette underneath)

### ¿Por qué Python y no Go/Rust?

El usuario tiene 100+ artículos en DEV.to sobre Python, MCP servers y AI agents. El producto es vendible a devs Python que ya tienen ese stack. Rust/Go añadirían fricción sin valor para el ICP.

### ¿Por qué DiskCache y no Redis?

- 0 dependencias adicionales para empezar
- Funciona para single-instance
- Si necesitas multi-instance, hay docker-compose con Redis opcional (`--profile with-redis`)

### ¿Por qué 2 fases de checks?

Fase 1 corre todo en paralelo (~500ms con DNS+WHOIS+SSL+reputation en paralelo). Fase 2 necesita el HTML, que solo sabemos descargar después de fase 1 (porque necesitamos el `final_url` post-redirect). Hacerlo secuencialmente añadiría ~2s al tiempo total.

## Escalabilidad

| Escenario              | Estrategia                                          |
|------------------------|-----------------------------------------------------|
| 1-100 req/min          | 1 instancia, DiskCache                              |
| 100-1000 req/min       | 2-3 instancias + nginx upstream + Redis compartido  |
| 1000+ req/min          | Kubernetes + HPA + Redis cluster                    |

En escenarios altos, los externalíos a Google Safe Browsing y VirusTotal también deberían cachearse en Redis compartido.

## Extensibilidad

Añadir un nuevo detector es trivial:

1. Crea `scamshield/checks/mi_detector.py`
2. Hereda de `BaseCheck`, implementa `run()`
3. Añádelo a `ALL_CHECKS` en `scamshield/checks/__init__.py`

El motor automáticamente lo ejecutará y lo agregará al score.

## Seguridad operativa

- El servidor no requiere API key por defecto (modo dev local). En producción, setear `API_KEY` en `.env`.
- CORS abierto a `*` — recomendado restringir a dominios específicos en producción.
- TLS se asume detrás de un reverse proxy (Caddy/Nginx/Cloudflare). El servidor escucha HTTP.
- El User-Agent del HTTP client identifica como `ScamShieldPro/1.0` — no spoofea browsers.
- Rate limiting protege de abuso, pero no hay WAF integrado — detrás de Cloudflare u otro WAF es recomendado.
