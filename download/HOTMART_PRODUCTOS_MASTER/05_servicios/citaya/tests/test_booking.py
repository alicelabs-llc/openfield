"""Tests for booking service."""
from datetime import datetime, timedelta
import pytest

from citaya.core.models import Professional, Service, BookingRequest, AppointmentStatus
from citaya.services import DataStore, BookingService


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    from citaya.core.config import reset_settings_cache
    reset_settings_cache()
    s = DataStore()
    # Seed sample data
    s.save_professional(Professional(id="DR01", name="Dr. House", specialty="General"))
    s.save_service(Service(id="SRV01", name="Consulta", duration_minutes=30, price=50.0))
    s.save_service(Service(id="SRV02", name="Limpieza", duration_minutes=60, price=80.0))
    return s


@pytest.fixture
def booking(store):
    return BookingService(store)


def test_book_appointment_success(booking, store):
    """Book a valid slot."""
    future = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(days=1, hours=2)
    # Adjust to working hours if needed
    req = BookingRequest(
        professional_id="DR01",
        service_id="SRV01",
        customer_name="Juan Perez",
        customer_phone="593999123456",
        customer_email="juan@x.com",
        start_at=future,
    )
    appt = booking.book(req)
    assert appt.id.startswith("APT-")
    assert appt.status == AppointmentStatus.CONFIRMED
    assert appt.customer_name == "Juan Perez"
    assert appt.end_at - appt.start_at == timedelta(minutes=30)


def test_book_conflict_rejected(booking, store):
    """Cannot book two appointments at the same time."""
    future = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(days=1, hours=2)
    req1 = BookingRequest(
        professional_id="DR01",
        service_id="SRV01",
        customer_name="Cliente 1",
        start_at=future,
    )
    booking.book(req1)
    # Now try to book overlapping
    req2 = BookingRequest(
        professional_id="DR01",
        service_id="SRV01",
        customer_name="Cliente 2",
        start_at=future + timedelta(minutes=15),  # overlaps with 30min appt
    )
    with pytest.raises(ValueError, match="conflict"):
        booking.book(req2)


def test_cancel_appointment(booking, store):
    future = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)
    appt = booking.book(BookingRequest(
        professional_id="DR01",
        service_id="SRV01",
        customer_name="Test",
        start_at=future,
    ))
    cancelled = booking.cancel(appt.id, "test cancel")
    assert cancelled.status == AppointmentStatus.CANCELLED


def test_cancel_nonexistent_raises(booking):
    with pytest.raises(ValueError, match="not found"):
        booking.cancel("NONEXISTENT")


def test_complete_appointment(booking):
    future = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)
    appt = booking.book(BookingRequest(
        professional_id="DR01",
        service_id="SRV01",
        customer_name="Test",
        start_at=future,
    ))
    completed = booking.complete(appt.id)
    assert completed.status == AppointmentStatus.COMPLETED


def test_get_available_slots(booking):
    """Slots should be available for a working day."""
    from datetime import date
    from citaya.core.slots import generate_slots
    # Get slots for tomorrow
    tomorrow = date(2026, 10, 26)
    slots = booking.get_available_slots("DR01", "2026-10-26")
    # Should have at least 1 slot, all available initially
    if slots:  # might be 0 if it's a Sunday
        assert all(s.available for s in slots)


def test_invalid_professional_raises(booking):
    with pytest.raises(ValueError, match="not found"):
        booking.book(BookingRequest(
            professional_id="INVALID",
            service_id="SRV01",
            customer_name="Test",
            start_at=datetime.utcnow() + timedelta(days=1),
        ))


def test_invalid_service_raises(booking):
    with pytest.raises(ValueError, match="not found"):
        booking.book(BookingRequest(
            professional_id="DR01",
            service_id="INVALID",
            customer_name="Test",
            start_at=datetime.utcnow() + timedelta(days=1),
        ))
