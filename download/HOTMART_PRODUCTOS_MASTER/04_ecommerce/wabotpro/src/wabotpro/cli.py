"""WhatsAppBot Pro — CLI."""
from __future__ import annotations
import asyncio
from decimal import Decimal
import click
from rich.console import Console
from rich.table import Table
from rich import box

from wabotpro import __version__
from wabotpro.core.config import get_settings
from wabotpro.core.models import Product
from wabotpro.core.store import Store
from wabotpro.flows import FlowEngine
from wabotpro.handlers import WhatsAppCloudClient

console = Console()


@click.group()
@click.version_option(__version__, prog_name="wabotpro")
def main():
    """WhatsAppBot Pro — Bot de WhatsApp para negocios."""


@main.command()
def version():
    click.echo(f"WhatsAppBot Pro v{__version__}")


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8004, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server (webhook receiver + admin API)."""
    import uvicorn
    uvicorn.run("wabotpro.server:app", host=host, port=port, reload=reload)


@main.command()
def catalog():
    """Show current catalog."""
    s = Store()
    products = s.get_catalog()
    table = Table(title=f"Catálogo ({len(products)} productos)", box=box.ROUNDED)
    table.add_column("ID", style="bold")
    table.add_column("Nombre")
    table.add_column("Precio", justify="right")
    table.add_column("Stock", justify="right")
    for p in products:
        table.add_row(p.id, p.name, f"${p.price}", str(p.stock))
    console.print(table)


@main.command()
@click.option("--id", prompt="ID producto (ej. P001)")
@click.option("--name", prompt="Nombre")
@click.option("--price", type=float, prompt="Precio")
@click.option("--desc", default="", prompt="Descripción (opcional)")
@click.option("--stock", type=int, default=0, prompt="Stock")
@click.option("--category", default="", prompt="Categoría (opcional)")
def add_product(id, name, price, desc, stock, category):
    """Add product to catalog."""
    p = Product(
        id=id.upper(), name=name, description=desc, price=Decimal(str(price)),
        stock=stock, category=category,
    )
    Store().add_product(p)
    console.print(f"[green]✓ Producto agregado:[/green] {p.id} - {p.name} (${p.price})")


@main.command()
@click.argument("product_id")
def remove(product_id):
    """Remove product from catalog."""
    if Store().remove_product(product_id):
        console.print(f"[green]✓ Removido: {product_id}[/green]")
    else:
        console.print(f"[red]No encontrado: {product_id}[/red]")


@main.command()
def orders():
    """Show orders."""
    s = Store()
    all_orders = s.get_orders()
    if not all_orders:
        console.print("[yellow]No hay pedidos aún[/yellow]")
        return
    table = Table(title=f"Pedidos ({len(all_orders)})", box=box.ROUNDED)
    table.add_column("ID", style="bold")
    table.add_column("Cliente")
    table.add_column("Items", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Estado")
    for o in all_orders:
        table.add_row(o.id, o.customer_number, str(len(o.items)), f"${o.total}", o.status)
    console.print(table)


@main.command()
@click.option("--from-number", prompt="Tu número (ej. 593999123456)")
@click.option("--text", prompt="Mensaje")
def simulate(from_number, text):
    """Simulate an incoming message (for testing flows)."""
    from wabotpro.core.models import Message
    s = Store()
    flow = FlowEngine(s)
    msg = Message(from_number=from_number, to_number="bot", text=text)
    responses = flow.process(msg)
    for r in responses:
        console.print(f"\n[cyan]BOT →[/cyan] {r}")


@main.command()
@click.option("--to", prompt="Número destino")
@click.option("--text", prompt="Mensaje")
def send(to, text):
    """Send a real WhatsApp message (requires WA Cloud API configured)."""
    client = WhatsAppCloudClient()
    result = asyncio.run(client.send_text(to, text))
    console.print(result)


if __name__ == "__main__":
    main()
