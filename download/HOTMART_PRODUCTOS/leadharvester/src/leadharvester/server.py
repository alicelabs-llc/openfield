"""LeadHarvester — FastAPI server."""
from __future__ import annotations
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from leadharvester import __version__
from leadharvester.core.config import get_settings
from leadharvester.core.models import ScrapeRequest, ScrapeJob, LeadList
from leadharvester.scrapers import scrape
from leadharvester.export import to_json, to_csv, to_excel

app = FastAPI(
    title="LeadHarvester",
    description="Scraper de leads Instagram para agencias. Extrae emails, teléfonos y datos de perfiles públicos.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"

# In-memory job store (production: use SQLite/Postgres)
JOBS: dict[str, ScrapeJob] = {}


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>LeadHarvester v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "ig_session_configured": bool(s.ig_username and s.ig_password),
        "max_per_run": s.max_profiles_per_run,
    }


@app.post("/v1/scrape")
async def start_scrape(req: ScrapeRequest, bg: BackgroundTasks):
    """Start async scrape job."""
    job_id = str(uuid.uuid4())[:8]
    job = ScrapeJob(job_id=job_id, status="pending", request=req)
    JOBS[job_id] = job
    bg.add_task(_run_scrape, job_id, req)
    return {"job_id": job_id, "status": "pending", "poll_url": f"/v1/scrape/{job_id}"}


async def _run_scrape(job_id: str, req: ScrapeRequest):
    job = JOBS[job_id]
    job.status = "running"
    job.started_at = datetime.utcnow()
    try:
        leads = await scrape(req)
        job.leads = leads
        job.progress = 100
        job.status = "completed"
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
    finally:
        job.completed_at = datetime.utcnow()


@app.get("/v1/scrape/{job_id}")
async def get_scrape(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(404, "Job not found")
    return JOBS[job_id].model_dump()


@app.post("/v1/scrape/{job_id}/export")
async def export_scrape(job_id: str, format: str = "csv"):
    """Export job results to CSV/JSON/Excel."""
    if job_id not in JOBS:
        raise HTTPException(404, "Job not found")
    job = JOBS[job_id]
    if job.status != "completed":
        raise HTTPException(400, f"Job not completed (status: {job.status})")
    s = get_settings()
    lead_list = LeadList(
        name=f"leads_{job_id}",
        query=job.request.target,
        leads=job.leads,
    )
    if format == "csv":
        path = to_csv(lead_list, s.export_path / f"leads_{job_id}.csv")
    elif format == "json":
        path = to_json(lead_list, s.export_path / f"leads_{job_id}.json")
    elif format == "excel":
        path = to_excel(lead_list, s.export_path / f"leads_{job_id}.xlsx")
    else:
        raise HTTPException(400, f"Unknown format: {format}")
    return FileResponse(str(path), filename=path.name)
