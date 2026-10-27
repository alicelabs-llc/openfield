"""LicitAlert — FastAPI server."""
from __future__ import annotations
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from licitalert import __version__
from licitalert.core.config import get_settings
from licitalert.core.models import AlertRule, AlertRequest, Country
from licitalert.core.store import AlertStore
from licitalert.services import LicitAlertService

app = FastAPI(
    title="LicitAlert",
    description="Alertas de licitaciones públicas. Monitorea SECOP, SERCOP, CompraNet.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"
service = LicitAlertService()
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def _start_scheduler():
    s = get_settings()
    scheduler.add_job(service.run_check_cycle, "interval", hours=s.check_interval_hours, id="check_tenders")
    scheduler.start()


@app.on_event("shutdown")
async def _stop_scheduler():
    scheduler.shutdown(wait=False)


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>LicitAlert v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    store = AlertStore()
    return {
        "status": "ok",
        "version": __version__,
        "countries": s.countries,
        "check_interval_hours": s.check_interval_hours,
        "rules_count": len(store.list_rules()),
        "tenders_cached": len(store.list_tenders(limit=1000)),
    }


@app.post("/v1/rules")
async def create_rule(req: AlertRequest):
    """Create a new alert rule."""
    rule = AlertRule(
        id=f"RULE-{str(uuid.uuid4())[:8].upper()}",
        **req.model_dump(),
    )
    AlertStore().save_rule(rule)
    return rule


@app.get("/v1/rules")
async def list_rules():
    return [r.model_dump() for r in AlertStore().list_rules()]


@app.delete("/v1/rules/{rule_id}")
async def delete_rule(rule_id: str):
    if not AlertStore().delete_rule(rule_id):
        raise HTTPException(404, "Rule not found")
    return {"deleted": rule_id}


@app.get("/v1/tenders")
async def list_tenders(country: str = None, limit: int = 100):
    tenders = AlertStore().list_tenders(country=country, limit=limit)
    return [t.model_dump() for t in tenders]


@app.post("/v1/check")
async def force_check(bg: BackgroundTasks):
    """Force a check cycle (async)."""
    bg.add_task(service.run_check_cycle)
    return {"status": "scheduled"}


@app.post("/v1/check-sync")
async def force_check_sync():
    """Force a check cycle and wait for result."""
    return await service.run_check_cycle()
