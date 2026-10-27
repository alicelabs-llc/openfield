"""CitaYa — Slot generation logic."""
from __future__ import annotations
from datetime import datetime, date, time, timedelta
from citaya.core.config import get_settings
from citaya.core.models import Slot, Professional


WEEKDAY_MAP = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


def _parse_work_days(s: str) -> set[int]:
    return {WEEKDAY_MAP[d.strip().lower()] for d in s.split(",") if d.strip()}


def _get_working_hours(professional: Professional, day: date) -> tuple[time, time] | None:
    """Returns (start, end) for the given day, or None if not working."""
    s = get_settings()
    weekday_name = list(WEEKDAY_MAP.keys())[day.weekday()]

    # Check professional override
    if weekday_name in professional.work_schedule:
        ws = professional.work_schedule[weekday_name]
        if not ws.get("active", True):
            return None
        start = time.fromisoformat(ws["start"])
        end = time.fromisoformat(ws["end"])
        return (start, end)

    # Default business hours
    work_days = _parse_work_days(s.work_days)
    if day.weekday() not in work_days:
        return None
    start = time(s.default_open_hour, 0)
    end = time(s.default_close_hour, 0)
    return (start, end)


def generate_slots(
    professional: Professional,
    target_date: date,
    slot_duration_minutes: int | None = None,
) -> list[Slot]:
    """Generate all bookable slots for a professional on a given date."""
    s = get_settings()
    duration = slot_duration_minutes or s.slot_duration_minutes

    hours = _get_working_hours(professional, target_date)
    if not hours:
        return []

    start_time, end_time = hours
    start_dt = datetime.combine(target_date, start_time)
    end_dt = datetime.combine(target_date, end_time)

    slots: list[Slot] = []
    current = start_dt
    while current + timedelta(minutes=duration) <= end_dt:
        slot_end = current + timedelta(minutes=duration)
        slots.append(Slot(
            professional_id=professional.id,
            start_at=current,
            end_at=slot_end,
        ))
        current = slot_end

    return slots


def generate_slots_range(
    professional: Professional,
    start_date: date,
    days: int = 7,
    slot_duration_minutes: int | None = None,
) -> list[Slot]:
    """Generate slots for a range of days (default: next 7 days)."""
    all_slots: list[Slot] = []
    for i in range(days):
        target = start_date + timedelta(days=i)
        all_slots.extend(generate_slots(professional, target, slot_duration_minutes))
    return all_slots
