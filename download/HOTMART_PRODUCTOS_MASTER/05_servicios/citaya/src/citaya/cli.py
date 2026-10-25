"""CitaYa — CLI."""
from __future__ import annotations
import asyncio
from datetime import datetime, date
import click
from rich.console import Console
from rich.table import Table
from rich import box

from citaya import __version__
from citaya.core.config import get_settings
from citaya.core.models import Professional, Service, BookingRequest, AppointmentStatus
from citaya.services import DataStore, BookingService
from citaya.notifiers import send_appointment_confirmation

console = Console()


@click.group()
@click.version_option(__version__, prog_name="citaya")
def main():
    """CitaYa — Sistema de reservas/citas."""


@main.command()
def version():
    click.echo(f"CitaYa v{__version__}")


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8005, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server."""
    import uvicorn
    uvicorn.run("citaya.server:app", host=host, port=port, reload=reload)


@main.command(name="add-professional")
@click.option("--id", prompt="ID (ej. DR01)")
@click.option("--name", prompt="Nombre")
@click.option("--specialty", default="", prompt="Especialidad")
@click.option("--email", default="", prompt="Email")
@click.option("--phone", default="", prompt="Teléfono")
def add_professional(id, name, specialty, email, phone):
    """Add a professional."""
    p = Professional(id=id.upper(), name=name, specialty=specialty, email=email, phone=phone)
    DataStore().save_professional(p)
    console.print(f"[green]✓ Profesional agregado:[/green] {p.id} - {p.name}")


@main.command(name="add-service")
@click.option("--id", prompt="ID (ej. SRV01)")
@click.option("--name", prompt="Nombre")
@click.option("--duration", type=int, default=30, prompt="Duración (minutos)")
@click.option("--price", type=float, default=0.0, prompt="Precio")
def add_service(id, name, duration, price):
    """Add a service."""
    s = Service(id=id.upper(), name=name, duration_minutes=duration, price=price)
    DataStore().save_service(s)
    console.print(f"[green]✓ Servicio agregado:[/green] {s.id} - {s.name} ({s.duration_minutes}min)")


@main.command(name="list-professionals")
def list_professionals():
    """List professionals."""
    pros = DataStore().list_professionals()
    table = Table(title=f"Profesionales ({len(pros)})", box=box.ROUNDED)
    table.add_column("ID", style="bold")
    table.add_column("Nombre")
    table.add_column("Especialidad")
    table.add_column("Email")
    for p in pros:
        table.add_row(p.id, p.name, p.specialty, p.email)
    console.print(table)


@main.command(name="list-appointments")
@click.option("--date-from", default=None, help="YYYY-MM-DD")
def list_appointments_cmd(date_from):
    """List appointments."""
    s = DataStore()
    df = datetime.fromisoformat(date_from) if date_from else None
    appts = s.list_appointments(date_from=df)
    if not appts:
        console.print("[yellow]No hay citas[/yellow]")
        return
    table = Table(title=f"Citas ({len(appts)})", box=box.ROUNDED)
    table.add_column("ID", style="bold")
    table.add_column("Fecha")
    table.add_column("Hora")
    table.add_column("Profesional")
    table.add_column("Cliente")
    table.add_column("Servicio")
    table.add_column("Estado")
    pros = {p.id: p for p in s.list_professionals()}
    for a in sorted(appts, key=lambda x: x.start_at):
        pro_name = pros.get(a.professional_id, Professional(id="", name="??")).name
        table.add_row(
            a.id[:12],
            a.start_at.strftime("%d/%m/%Y"),
            a.start_at.strftime("%H:%M"),
            pro_name,
            a.customer_name,
            a.service_name,
            a.status.value,
        )
    console.print(table)


@main.command(name="list-slots")
@click.option("--professional-id", prompt="ID profesional")
@click.option("--date", "date_str", default=None, help="YYYY-MM-DD (default: hoy)")
def list_slots(professional_id, date_str):
    """List available slots."""
    s = DataStore()
    booking = BookingService(s)
    target = date.fromisoformat(date_str) if date_str else None
    slots = booking.get_available_slots(professional_id, date_str)
    if not slots:
        console.print("[yellow]No hay slots disponibles[/yellow]")
        return
    available = [s for s in slots if s.available]
    table = Table(title=f"Slots disponibles ({len(available)}/{len(slots)})", box=box.ROUNDED)
    table.add_column("Hora")
    table.add_column("Disponible")
    for s in slots:
        icon = "[green]✓[/green]" if s.available else "[red]✗[/red]"
        table.add_row(s.start_at.strftime("%H:%M"), icon)
    console.print(table)


@main.command()
@click.option("--professional-id", prompt="ID profesional")
@click.option("--service-id", prompt="ID servicio")
@click.option("--start", prompt="Inicio (YYYY-MM-DDTHH:MM)")
@click.option("--name", prompt="Nombre cliente")
@click.option("--phone", default="", prompt="Teléfono")
@click.option("--email", default="", prompt="Email")
def book(professional_id, service_id, start, name, phone, email):
    """Book an appointment."""
    s = DataStore()
    booking = BookingService(s)
    try:
        req = BookingRequest(
            professional_id=professional_id.upper(),
            service_id=service_id.upper(),
            customer_name=name,
            customer_phone=phone,
            customer_email=email,
            start_at=datetime.fromisoformat(start),
        )
        appt = booking.book(req)
        console.print(f"[green]✓ Cita reservada:[/green] {appt.id}")
        console.print(f"  Cliente: {appt.customer_name}")
        console.print(f"  Fecha: {appt.start_at.strftime('%d/%m/%Y %H:%M')}")
    except ValueError as e:
        console.print(f"[red]✗ {e}[/red]")


@main.command()
@click.argument("appointment_id")
def cancel(appointment_id):
    """Cancel an appointment."""
    s = DataStore()
    booking = BookingService(s)
    try:
        appt = booking.cancel(appointment_id)
        console.print(f"[yellow]✗ Cancelada: {appt.id}[/yellow]")
    except ValueError as e:
        console.print(f"[red]✗ {e}[/red]")


if __name__ == "__main__":
    main()
