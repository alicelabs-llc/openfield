"""CitaYa — Models."""
from __future__ import annotations
from datetime import datetime, date, time, timedelta
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class Professional(BaseModel):
    id: str
    name: str
    specialty: str = ""
    email: str = ""
    phone: str = ""
    color: str = "#5d8bff"  # for calendar UI
    active: bool = True
    # Working hours per day (override defaults)
    work_schedule: dict[str, dict] = Field(default_factory=dict)  # {"mon": {"start":"09:00","end":"18:00"}}


class Service(BaseModel):
    id: str
    name: str
    description: str = ""
    duration_minutes: int = 30
    price: float = 0.0
    professional_id: str = ""  # if specific to a professional


class Customer(BaseModel):
    id: str
    name: str
    email: str = ""
    phone: str = ""
    notes: str = ""


class Appointment(BaseModel):
    id: str
    professional_id: str
    customer_id: str
    customer_name: str
    customer_phone: str = ""
    customer_email: str = ""
    service_id: str
    service_name: str
    start_at: datetime
    end_at: datetime
    status: AppointmentStatus = AppointmentStatus.PENDING
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    reminder_sent: bool = False

    @field_validator("end_at")
    @classmethod
    def end_after_start(cls, v, info):
        start = info.data.get("start_at")
        if start and v <= start:
            raise ValueError("end_at must be after start_at")
        return v


class Slot(BaseModel):
    """An available time slot for booking."""
    professional_id: str
    start_at: datetime
    end_at: datetime
    available: bool = True


class BookingRequest(BaseModel):
    """Public booking request (no auth required)."""
    professional_id: str
    service_id: str
    customer_name: str
    customer_phone: str = ""
    customer_email: str = ""
    start_at: datetime
    notes: str = ""
