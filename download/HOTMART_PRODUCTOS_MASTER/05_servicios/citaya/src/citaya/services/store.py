"""CitaYa — JSON-backed store for professionals, services, customers, appointments."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from citaya.core.config import get_settings
from citaya.core.models import Professional, Service, Customer, Appointment, AppointmentStatus


class DataStore:
    """JSON file-based persistence."""

    def __init__(self):
        self.s = get_settings()

    @property
    def base_path(self) -> Path:
        return self.s.data_path

    def _file(self, name: str) -> Path:
        p = self.base_path / f"{name}.json"
        if not p.exists():
            p.write_text("[]", encoding="utf-8")
        return p

    def _load(self, name: str) -> list[dict]:
        return json.loads(self._file(name).read_text(encoding="utf-8"))

    def _save(self, name: str, data: list[dict]):
        self._file(name).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    # === Professionals ===
    def list_professionals(self) -> list[Professional]:
        return [Professional(**d) for d in self._load("professionals")]

    def get_professional(self, pid: str) -> Professional | None:
        for p in self.list_professionals():
            if p.id == pid:
                return p
        return None

    def save_professional(self, p: Professional) -> Professional:
        items = self._load("professionals")
        items = [i for i in items if i["id"] != p.id]
        items.append(p.model_dump())
        self._save("professionals", items)
        return p

    def delete_professional(self, pid: str) -> bool:
        items = self._load("professionals")
        before = len(items)
        items = [i for i in items if i["id"] != pid]
        if len(items) < before:
            self._save("professionals", items)
            return True
        return False

    # === Services ===
    def list_services(self) -> list[Service]:
        return [Service(**d) for d in self._load("services")]

    def get_service(self, sid: str) -> Service | None:
        for s in self.list_services():
            if s.id == sid:
                return s
        return None

    def save_service(self, s: Service) -> Service:
        items = self._load("services")
        items = [i for i in items if i["id"] != s.id]
        items.append(s.model_dump())
        self._save("services", items)
        return s

    # === Customers ===
    def list_customers(self) -> list[Customer]:
        return [Customer(**d) for d in self._load("customers")]

    def get_or_create_customer(self, name: str, phone: str = "", email: str = "") -> Customer:
        items = self._load("customers")
        # Find by phone (most unique)
        if phone:
            for c in items:
                if c.get("phone") == phone:
                    c["name"] = name
                    c["email"] = email or c.get("email", "")
                    self._save("customers", items)
                    return Customer(**c)
        # Create new
        new_id = f"CUST-{len(items) + 1:04d}"
        customer = Customer(id=new_id, name=name, phone=phone, email=email)
        items.append(customer.model_dump())
        self._save("customers", items)
        return customer

    # === Appointments ===
    def list_appointments(self, professional_id: str = None, date_from: datetime = None, date_to: datetime = None) -> list[Appointment]:
        items = self._load("appointments")
        appts = []
        for d in items:
            d["start_at"] = datetime.fromisoformat(d["start_at"]) if isinstance(d.get("start_at"), str) else d.get("start_at")
            d["end_at"] = datetime.fromisoformat(d["end_at"]) if isinstance(d.get("end_at"), str) else d.get("end_at")
            d["created_at"] = datetime.fromisoformat(d["created_at"]) if isinstance(d.get("created_at"), str) else d.get("created_at")
            d["status"] = AppointmentStatus(d.get("status", "pending"))
            appts.append(Appointment(**d))
        if professional_id:
            appts = [a for a in appts if a.professional_id == professional_id]
        if date_from:
            appts = [a for a in appts if a.start_at >= date_from]
        if date_to:
            appts = [a for a in appts if a.start_at <= date_to]
        return appts

    def get_appointment(self, aid: str) -> Appointment | None:
        for a in self.list_appointments():
            if a.id == aid:
                return a
        return None

    def save_appointment(self, a: Appointment) -> Appointment:
        items = self._load("appointments")
        items = [i for i in items if i["id"] != a.id]
        items.append(a.model_dump())
        self._save("appointments", items)
        return a

    def delete_appointment(self, aid: str) -> bool:
        items = self._load("appointments")
        before = len(items)
        items = [i for i in items if i["id"] != aid]
        if len(items) < before:
            self._save("appointments", items)
            return True
        return False

    def has_conflict(self, professional_id: str, start_at: datetime, end_at: datetime, exclude_id: str = None) -> bool:
        """Check if professional has any overlapping appointment."""
        for a in self.list_appointments(professional_id=professional_id):
            if a.id == exclude_id:
                continue
            if a.status in (AppointmentStatus.CANCELLED,):
                continue
            if start_at < a.end_at and end_at > a.start_at:
                return True
        return False
