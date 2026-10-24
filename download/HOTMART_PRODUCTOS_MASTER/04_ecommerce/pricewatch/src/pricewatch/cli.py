"""PriceWatch — CLI."""
from __future__ import annotations
import asyncio
import json
from rich.console import Console
from rich.table import Table
from rich import box
import click

from pricewatch import __version__
from pricewatch.core.config import get_settings
from pricewatch.core.models import TrackRequest, AlertChannel, AlertCondition
from pricewatch.tracker import Tracker

console = Console()


@click.group()
@click.version_option(__version__, prog_name="pricewatch")
def main():
    """PriceWatch — Monitor de precios."""


@main.command()
def version():
    click.echo(f"PriceWatch v{__version__}")


@main.command()
@click.argument("url")
@click.option("--target", type=float, help="Target price (alerts when price drops below)")
@click.option("--email", help="Email to notify")
@click.option("--telegram", help="Telegram chat ID to notify")
@click.option("--discord", help="Discord webhook URL")
def add(url, target, email, telegram, discord):
    """Add a product URL to track."""
    channels = []
    recipient = ""
    if email:
        channels.append(AlertChannel.EMAIL)
        recipient = email
    elif telegram:
        channels.append(AlertChannel.TELEGRAM)
        recipient = telegram
    elif discord:
        channels.append(AlertChannel.DISCORD)
        recipient = discord
    else:
        channels.append(AlertChannel.EMAIL)

    req = TrackRequest(
        url=url,
        target_price=target,
        alert_channels=channels,
        alert_recipient=recipient,
    )
    t = Tracker()
    p = t.add(req)
    console.print(f"[green]✓ Producto agregado:[/green] {p.id}")
    console.print(f"  URL: {p.url}")
    console.print(f"  Store: {p.store.value}")
    console.print(f"  Target: ${target or '—'}")

    # Force initial check
    console.print("\n[cyan]Haciendo check inicial...[/cyan]")
    alert = asyncio.run(t.check_one(p.id))
    p = t.get(p.id)
    if p and p.last_price:
        console.print(f"  Precio actual: [bold]${p.last_price}[/bold] {p.price_history[-1].currency if p.price_history else ''}")
    if alert:
        console.print(f"[yellow]⚠ Alerta: bajó de ${alert.old_price} a ${alert.new_price}[/yellow]")


@main.command(name="list")
def list_cmd():
    """List tracked products."""
    t = Tracker()
    products = t.list_all()
    if not products:
        console.print("[yellow]No hay productos trackeados[/yellow]")
        return
    table = Table(title="Productos trackeados", box=box.ROUNDED)
    table.add_column("ID", style="dim")
    table.add_column("Nombre")
    table.add_column("Store")
    table.add_column("Precio actual", justify="right")
    table.add_column("Target", justify="right")
    for p in products:
        table.add_row(
            p.id[:20],
            (p.name or "(sin nombre)")[:40],
            p.store.value,
            f"${p.last_price}" if p.last_price else "—",
            f"${p.target_price}" if p.target_price else "—",
        )
    console.print(table)


@main.command()
@click.argument("pid")
def check(pid):
    """Force check one product."""
    t = Tracker()
    alert = asyncio.run(t.check_one(pid))
    p = t.get(pid)
    if not p:
        console.print(f"[red]Producto no encontrado: {pid}[/red]")
        return
    if p.last_price:
        console.print(f"[green]✓ Precio actualizado:[/green] ${p.last_price}")
    if alert:
        console.print(f"[yellow]⚠ ALERTA: ${alert.old_price} → ${alert.new_price} (-{alert.price_diff_percent}%)[/yellow]")


@main.command(name="check-all")
def check_all():
    """Check all tracked products."""
    t = Tracker()
    console.print(f"[cyan]Checkeando {len(t.products)} productos...[/cyan]")
    alerts = asyncio.run(t.check_all())
    console.print(f"[green]✓ Done. {len(alerts)} alertas disparadas.[/green]")


@main.command()
@click.argument("pid")
def remove(pid):
    """Stop tracking a product."""
    t = Tracker()
    if t.remove(pid):
        console.print(f"[green]✓ Removido: {pid}[/green]")
    else:
        console.print(f"[red]No encontrado: {pid}[/red]")


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8003, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server (with scheduler)."""
    import uvicorn
    uvicorn.run("pricewatch.server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
