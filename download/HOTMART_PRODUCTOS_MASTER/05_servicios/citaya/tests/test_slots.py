"""Tests for slot generation."""
from datetime import date, datetime, time
import pytest

from citaya.core.models import Professional
from citaya.core.slots import generate_slots, generate_slots_range, _get_working_hours


@pytest.fixture
def professional():
    return Professional(id="DR01", name="Dr. Test", specialty="General")


def test_slots_for_monday(professional):
    """Monday should produce slots based on default 9-18h."""
    monday = date(2026, 10, 26)  # Monday
    slots = generate_slots(professional, monday, slot_duration_minutes=60)
    assert len(slots) == 9  # 9:00 to 17:00 = 9 slots of 1h
    assert slots[0].start_at.time() == time(9, 0)
    assert slots[-1].end_at.time() == time(18, 0)


def test_slots_for_sunday_returns_empty(professional):
    """Sunday should produce no slots (default work_days exclude sun)."""
    sunday = date(2026, 10, 25)
    slots = generate_slots(professional, sunday)
    assert slots == []


def test_slots_30min_duration(professional):
    monday = date(2026, 10, 26)
    slots = generate_slots(professional, monday, slot_duration_minutes=30)
    assert len(slots) == 18  # 9 hours × 2 slots/hour


def test_professional_override_schedule():
    """Professional with custom hours on a specific day."""
    p = Professional(
        id="DR02", name="Dr. Custom",
        work_schedule={"mon": {"start": "10:00", "end": "14:00"}}
    )
    monday = date(2026, 10, 26)
    slots = generate_slots(p, monday, slot_duration_minutes=60)
    assert len(slots) == 4  # 4 hours from 10 to 14


def test_professional_inactive_day():
    """Professional explicitly inactive on a day."""
    p = Professional(
        id="DR03", name="Dr. TocoMartes",
        work_schedule={"tue": {"active": False, "start": "09:00", "end": "18:00"}}
    )
    tuesday = date(2026, 10, 27)
    slots = generate_slots(p, tuesday)
    assert slots == []


def test_generate_slots_range(professional):
    """Generate 7 days of slots."""
    slots = generate_slots_range(professional, date(2026, 10, 26), days=7, slot_duration_minutes=60)
    # Should have slots for working days only (mon-sat = 6 days)
    # 6 days × 9 slots = 54
    assert len(slots) == 54
