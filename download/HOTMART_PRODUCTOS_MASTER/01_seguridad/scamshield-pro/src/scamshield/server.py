"""ScamShield Pro — FastAPI server."""
from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from scamshield import __version__
from scamshield.checks import ALL_CHECKS
from scamshield.core.config import get_settings
from scamshield.core.models import (
    BulkScanRequest,
    HealthResponse,
    ScanRequest,
    ScanResult,
)
from scamshield.scanner import Scanner

# --- Rate limiter (in-memory, per-IP) ---
RATE_BUCKETS: dict[str, deque] = defaultdict(deque)


def _check_rate_limit(client_ip: str, limit_per_min: int) -> None:
    now = time.time()
    bucket = RATE_BUCKETS[client_ip]
    # Drop entries older than 60s
    while bucket and bucket[0] < now - 60:
        bucket.popleft()
    if len(bucket) >= limit_per_min:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded ({limit_per_min}/min)",
        )
    bucket.append(now)


# --- App ---
app = FastAPI(
    title="ScamShield Pro",
    description=(
        "Self-hosted URL fraud & phishing detector. 30+ heuristics, "
        "0-100 trust score, ScamAdviser-compatible bands."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Optional: serve static assets (landing/dashboard)
WEB_DIR = Path(__file__).parent.parent.parent / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


# --- Auth ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _verify_api_key(provided: Optional[str]) -> None:
    s = get_settings()
    # If no key configured, allow all (local dev mode)
    if not s.api_key or s.api_key == "changeme-please-replace-this":
        return
    if provided != s.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )


# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the landing page (if available)."""
    index = WEB_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse(
        f"<h1>ScamShield Pro v{__version__}</h1>"
        "<p>API running. See <a href='/docs'>/docs</a> for OpenAPI.</p>"
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard."""
    dash = WEB_DIR / "dashboard.html"
    if dash.exists():
        return HTMLResponse(dash.read_text(encoding="utf-8"))
    raise HTTPException(404, "dashboard.html not bundled")


@app.get("/healthz", response_model=HealthResponse)
async def healthz():
    return HealthResponse(
        status="ok",
        version=__version__,
        checks_enabled=[c.name for c in ALL_CHECKS],
    )


@app.post("/v1/scan", response_model=ScanResult)
async def scan(
    req: ScanRequest,
    request: Request,
    api_key: str = Depends(api_key_header),
):
    """Scan a single URL. Returns trust score + per-check breakdown."""
    s = get_settings()
    _check_rate_limit(request.client.host if request.client else "unknown", s.rate_limit_per_minute)
    _verify_api_key(api_key)

    scanner = Scanner()
    try:
        result = await scanner.scan(req)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Scan failed: {type(e).__name__}: {e}")
    return result


@app.post("/v1/scan/bulk", response_model=list[ScanResult])
async def scan_bulk(
    req: BulkScanRequest,
    request: Request,
    api_key: str = Depends(api_key_header),
):
    """Scan up to 100 URLs at once (sequential)."""
    s = get_settings()
    _check_rate_limit(request.client.host if request.client else "unknown", s.rate_limit_per_minute)
    _verify_api_key(api_key)

    scanner = Scanner(parallel=False)
    results = []
    for url in req.urls:
        try:
            r = await scanner.scan(ScanRequest(url=url))
            results.append(r)
        except Exception as e:
            # Include error result
            results.append(ScanResult(
                url=url,
                normalized_url=url,
                domain="error",
                tld="",
                trust_score=__import__("scamshield.core.models", fromlist=["TrustScore", "Verdict"]).TrustScore(
                    value=1,
                    verdict=__import__("scamshield.core.models", fromlist=["Verdict"]).Verdict.VERY_UNSAFE,
                ),
                checks=[],
            ))
    return results


@app.get("/v1/checks")
async def list_checks(api_key: str = Depends(api_key_header)):
    """List all detectors with their metadata."""
    _verify_api_key(api_key)
    return [
        {
            "name": c.name,
            "severity": c.severity,
            "weight": c.weight,
            "requires_network": c.requires_network,
            "requires_content": c.requires_content,
            "description": (c.__doc__ or "").strip().split("\n")[0],
        }
        for c in ALL_CHECKS
    ]
