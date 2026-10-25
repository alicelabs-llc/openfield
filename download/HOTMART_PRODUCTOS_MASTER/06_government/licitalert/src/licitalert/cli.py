"""LicitAlert — CLI."""
from __future__ import annotations
import asyncio
from decimal import Decimal
import click
from rich.console import Console
from rich.table import Table
from rich import box

from licitalert import __version__
from licitalert.core.config import get_settings
from licitalert.core.models import AlertRule, AlertRequest, Country
from licitalert.core.store import AlertStore
from licitalert.services import LicitAlertService

console = Console()


@click.group()
@click.version_option(__version__, prog_name="licitalert")
def main():
    """LicitAlert — Alertas de licitaciones públicas."""


@main.command()
def version():
    click.echo(f"LicitAlert v{__version__}")


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8009, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server (with scheduler)."""
    import uvicorn
    uvicorn.run("licitalert.server:app", host=host, port=port, reload=reload)


@main.command()
@click.option("--name", prompt="Nombre de la alerta")
@click.option("--countries", default="co,ec,mx", prompt="Países (comma-sep)")
@click.option("--keywords", prompt="Keywords (comma-sep)")
@click.option("--min-budget", type=float, default=None, prompt="Presupuesto mín. (opcional)")
@click.option("--max-budget", type=float, default=None, prompt="Presupuesto máx. (opcional)")
@click.option("--email", default="", prompt="Email para alertas")
def add_alert(name, countries, keywords, min_budget, max_budget, email):
    """Add an alert rule."""
    import uuid
    rule = AlertRule(
        id=f"RULE-{uuid.uuid4().hex[:8].upper()}",
        name=name,
        countries=[Country(c.strip()) for c in countries.split(",") if c.strip()],
        keywords=[k.strip() for k in keywords.split(",") if k.strip()],
        min_budget=Decimal(str(min_budget)) if min_budget else None,
        max_budget=Decimal(str(max_budget)) if max_budget else None,
        alert_channels=["email"] if email else [],
        alert_recipient=email,
    )
    AlertStore().save_rule(rule)
    console.print(f"[green]✓ Alerta creada:[/green] {rule.id} - {rule.name}")
    console.print(f"  Países: {[c.value for c in rule.countries]}")
    console.print(f"  Keywords: {rule.keywords}")


@main.command(name="list-alerts")
def list_alerts():
    """List alert rules."""
    rules = AlertStore().list_rules()
    if not rules:
        console.print("[yellow]No hay alertas configuradas[/yellow]")
        return
    table = Table(title=f"Alertas ({len(rules)})", box=box.ROUNDED)
    table.add_column("ID", style="bold")
    table.add_column("Nombre")
    table.add_column("Países")
    table.add_column("Keywords")
    table.add_column("Destinatario")
    for r in rules:
        countries = ",".join([c.value for c in r.countries]) or "todos"
        keywords = ", ".join(r.keywords[:3]) + ("..." if len(r.keywords) > 3 else "")
        table.add_row(r.id, r.name, countries, keywords, r.alert_recipient)
    console.print(table)


@main.command()
@click.argument("rule_id")
def remove_alert(rule_id):
    """Remove an alert rule."""
    if AlertStore().delete_rule(rule_id):
        console.print(f"[green]✓ Eliminada: {rule_id}[/green]")
    else:
        console.print(f"[red]No encontrada: {rule_id}[/red]")


@main.command(name="check-now")
def check_now():
    """Force a check cycle now."""
    service = LicitAlertService()
    console.print("[cyan]Ejecutando ciclo de check...[/cyan]")
    result = asyncio.run(service.run_check_cycle())
    console.print(f"[green]✓ Done[/green]")
    console.print(f"  Nuevas licitaciones: {result.get('new_tenders', 0)}")
    console.print(f"  Matches: {result.get('matches', 0)}")
    console.print(f"  Notificaciones enviadas: {result.get('notified', 0)}")


@main.command(name="list-tenders")
@click.option("--country", default=None, help="co, ec, mx")
@click.option("--limit", type=int, default=20)
def list_tenders(country, limit):
    """List cached tenders."""
    tenders = AlertStore().list_tenders(country=country, limit=limit)
    if not tenders:
        console.print("[yellow]No hay licitaciones cacheadas. Ejecuta 'check-now' primero.[/yellow]")
        return
    table = Table(title=f"Licitaciones ({len(tenders)})", box=box.ROUNDED)
    table.add_column("País")
    table.add_column("Título")
    table.add_column("Entidad")
    table.add_column("Presupuesto", justify="right")
    table.add_column("Estado")
    for t in tenders:
        table.add_row(
            t.country.value.upper(),
            t.title[:40],
            t.entity[:30],
            f"${t.budget} {t.currency}" if t.budget else "N/A",
            t.status.value,
        )
    console.print(table)


if __name__ == "__main__":
    main()
