"""CitaYa — FastAPI server."""
from __future__ import annotations
import asyncio
from datetime import datetime, date
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from citaya import __version__
from citaya.core.config import get_settings
from citaya.core.models import Professional, Service, Appointment, AppointmentStatus, BookingRequest
from citaya.services import DataStore, BookingService
from citaya.notifiers import send_appointment_confirmation

app = FastAPI(
    title="CitaYa",
    description="Sistema de reservas/citas self-hosted para clínicas, peluquerías, consultorios.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

store = DataStore()
booking = BookingService(store)
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def _start_scheduler():
    # Reminder job: runs every hour, checks appts coming up in 2h
    scheduler.add_job(_send_reminders, "interval", minutes=60, id="reminders")
    scheduler.start()


@app.on_event("shutdown")
async def _stop_scheduler():
    scheduler.shutdown(wait=False)


async def _send_reminders():
    """Send reminders for appointments in 2 hours."""
    s = get_settings()
    now = datetime.utcnow()
    target = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=s.reminder_hours_before)
    for appt in store.list_appointments():
        if appt.reminder_sent or appt.status != AppointmentStatus.CONFIRMED:
            continue
        if appt.start_at.strftime("%Y-%m-%d %H:00") == target.strftime("%Y-%m-%d %H:00"):
            professional = store.get_professional(appt.professional_id)
            # Send reminder
            # ... (reuse send_appointment_confirmation with reminder template)
            appt.reminder_sent = True
            store.save_appointment(appt)


from datetime import timedelta


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>CitaYa v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "version": __version__,
        "business_name": get_settings().business_name,
        "professionals": len(store.list_professionals()),
        "appointments": len(store.list_appointments()),
    }


# === Public booking endpoints (no auth) ===

@app.get("/public/professionals")
async def public_list_professionals():
    """List active professionals (for booking widget)."""
    return [p.model_dump() for p in store.list_professionals() if p.active]


@app.get("/public/services")
async def public_list_services(professional_id: str = None):
    services = store.list_services()
    if professional_id:
        services = [s for s in services if not s.professional_id or s.professional_id == professional_id]
    return [s.model_dump() for s in services]


@app.get("/public/slots")
async def public_get_slots(professional_id: str, date: str = None):
    """Get available slots for a professional on a given date."""
    slots = booking.get_available_slots(professional_id, date)
    return [
        {
            "start_at": s.start_at.isoformat(),
            "end_at": s.end_at.isoformat(),
            "available": s.available,
        }
        for s in slots
    ]


@app.post("/public/book")
async def public_book(req: BookingRequest):
    """Public booking endpoint."""
    try:
        appt = booking.book(req)
    except ValueError as e:
        raise HTTPException(400, str(e))
    # Send confirmation async
    professional = store.get_professional(req.professional_id)
    asyncio.create_task(send_appointment_confirmation(appt, professional, get_settings().business_name))
    return appt.model_dump()


# === Admin endpoints (would require auth in production) ===

@app.get("/admin/appointments")
async def list_appointments(date_from: str = None, date_to: str = None):
    df = datetime.fromisoformat(date_from) if date_from else None
    dt = datetime.fromisoformat(date_to) if date_to else None
    return [a.model_dump() for a in store.list_appointments(date_from=df, date_to=dt)]


@app.get("/admin/appointments/{aid}")
async def get_appointment(aid: str):
    a = store.get_appointment(aid)
    if not a:
        raise HTTPException(404, "Not found")
    return a.model_dump()


@app.post("/admin/professionals")
async def create_professional(p: Professional):
    store.save_professional(p)
    return p


@app.delete("/admin/professionals/{pid}")
async def delete_professional(pid: str):
    if not store.delete_professional(pid):
        raise HTTPException(404, "Not found")
    return {"deleted": pid}


@app.post("/admin/services")
async def create_service(s: Service):
    store.save_service(s)
    return s


@app.post("/admin/appointments/{aid}/confirm")
async def confirm_appt(aid: str):
    return booking.confirm(aid).model_dump()


@app.post("/admin/appointments/{aid}/complete")
async def complete_appt(aid: str):
    return booking.complete(aid).model_dump()


@app.post("/admin/appointments/{aid}/cancel")
async def cancel_appt(aid: str, reason: str = ""):
    return booking.cancel(aid, reason).model_dump()
