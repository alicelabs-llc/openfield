"""PriceWatch — FastAPI server."""
from __future__ import annotations
import asyncio
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from pricewatch import __version__
from pricewatch.core.config import get_settings
from pricewatch.core.models import TrackRequest
from pricewatch.tracker import Tracker

app = FastAPI(
    title="PriceWatch",
    description="Monitor de precios en MercadoLibre y Amazon. Alertas por email/Telegram/Discord.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"

tracker = Tracker()
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def _start_scheduler():
    s = get_settings()
    scheduler.add_job(tracker.check_all, "interval", minutes=s.check_interval_minutes, id="check_prices")
    scheduler.start()


@app.on_event("shutdown")
async def _stop_scheduler():
    scheduler.shutdown(wait=False)


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>PriceWatch v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "version": __version__,
        "products_tracked": len(tracker.products),
        "check_interval_minutes": get_settings().check_interval_minutes,
    }


@app.post("/v1/track")
async def track_product(req: TrackRequest):
    """Add a product to track."""
    p = tracker.add(req)
    return p.model_dump()


@app.get("/v1/products")
async def list_products():
    return [p.model_dump() for p in tracker.list_all()]


@app.get("/v1/products/{pid}")
async def get_product(pid: str):
    p = tracker.get(pid)
    if not p:
        raise HTTPException(404, f"Product {pid} not found")
    return p.model_dump()


@app.delete("/v1/products/{pid}")
async def delete_product(pid: str):
    if not tracker.remove(pid):
        raise HTTPException(404, f"Product {pid} not found")
    return {"deleted": pid}


@app.post("/v1/products/{pid}/check")
async def check_now(pid: str):
    """Force a price check for one product."""
    alert = await tracker.check_one(pid)
    if alert:
        return {"alert_fired": True, "alert": alert.model_dump()}
    p = tracker.get(pid)
    return {"alert_fired": False, "last_price": p.last_price if p else None}


@app.post("/v1/check-all")
async def check_all(bg: BackgroundTasks):
    """Force check all products (async)."""
    bg.add_task(tracker.check_all)
    return {"status": "scheduled", "products": len(tracker.products)}


@app.get("/v1/products/{pid}/history")
async def price_history(pid: str, limit: int = 100):
    p = tracker.get(pid)
    if not p:
        raise HTTPException(404, f"Product {pid} not found")
    history = p.price_history[-limit:]
    return [
        {
            "price": pp.price,
            "currency": pp.currency,
            "captured_at": pp.captured_at.isoformat(),
            "discount_percent": pp.discount_percent,
        }
        for pp in history
    ]
