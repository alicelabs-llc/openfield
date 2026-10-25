"""CitaYa — Booking service (orchestrator)."""
from __future__ import annotations
import uuid
from datetime import datetime
from citaya.core.config import get_settings
from citaya.core.models import Appointment, AppointmentStatus, BookingRequest, Slot
from citaya.core.slots import generate_slots, generate_slots_range
from citaya.services.store import DataStore


class BookingService:
    """High-level booking operations."""

    def __init__(self, store: DataStore):
        self.store = store
        self.settings = get_settings()

    def get_available_slots(self, professional_id: str, date_str: str = None, days: int = 1) -> list[Slot]:
        """Get available slots for a professional."""
        professional = self.store.get_professional(professional_id)
        if not professional or not professional.active:
            return []

        if date_str:
            target = datetime.fromisoformat(date_str).date()
            slots = generate_slots(professional, target)
        else:
            slots = generate_slots_range(professional, datetime.utcnow().date(), days=days)

        # Get existing appointments to filter out taken slots
        existing = self.store.list_appointments(professional_id=professional_id)
        for slot in slots:
            for appt in existing:
                if appt.status in (AppointmentStatus.CANCELLED,):
                    continue
                # If overlap, mark unavailable
                if slot.start_at < appt.end_at and slot.end_at > appt.start_at:
                    slot.available = False
                    break
        return slots

    def book(self, req: BookingRequest) -> Appointment:
        """Create a new appointment. Raises ValueError if conflict."""
        professional = self.store.get_professional(req.professional_id)
        if not professional:
            raise ValueError(f"Professional {req.professional_id} not found")
        service = self.store.get_service(req.service_id)
        if not service:
            raise ValueError(f"Service {req.service_id} not found")

        # Calculate end_at from service duration
        end_at = req.start_at + self._duration_timedelta(service.duration_minutes)

        if self.store.has_conflict(req.professional_id, req.start_at, end_at):
            raise ValueError("Time slot not available (conflict)")

        customer = self.store.get_or_create_customer(
            name=req.customer_name,
            phone=req.customer_phone,
            email=req.customer_email,
        )

        appointment = Appointment(
            id=f"APT-{str(uuid.uuid4())[:8].upper()}",
            professional_id=req.professional_id,
            customer_id=customer.id,
            customer_name=customer.name,
            customer_phone=customer.phone,
            customer_email=customer.email,
            service_id=req.service_id,
            service_name=service.name,
            start_at=req.start_at,
            end_at=end_at,
            status=AppointmentStatus.CONFIRMED,
            notes=req.notes,
        )
        self.store.save_appointment(appointment)
        return appointment

    def cancel(self, appointment_id: str, reason: str = "") -> Appointment:
        apt = self.store.get_appointment(appointment_id)
        if not apt:
            raise ValueError(f"Appointment {appointment_id} not found")
        apt.status = AppointmentStatus.CANCELLED
        apt.notes = f"{apt.notes}\nCancellation reason: {reason}".strip()
        self.store.save_appointment(apt)
        return apt

    def confirm(self, appointment_id: str) -> Appointment:
        return self._update_status(appointment_id, AppointmentStatus.CONFIRMED)

    def complete(self, appointment_id: str) -> Appointment:
        return self._update_status(appointment_id, AppointmentStatus.COMPLETED)

    def mark_no_show(self, appointment_id: str) -> Appointment:
        return self._update_status(appointment_id, AppointmentStatus.NO_SHOW)

    def _update_status(self, appointment_id: str, status: AppointmentStatus) -> Appointment:
        apt = self.store.get_appointment(appointment_id)
        if not apt:
            raise ValueError(f"Appointment {appointment_id} not found")
        apt.status = status
        self.store.save_appointment(apt)
        return apt

    def _duration_timedelta(self, minutes: int):
        from datetime import timedelta
        return timedelta(minutes=minutes)
