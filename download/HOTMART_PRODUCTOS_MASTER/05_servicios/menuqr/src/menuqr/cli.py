"""MenuQR Pro — CLI."""
from __future__ import annotations
from decimal import Decimal
import click
from rich.console import Console
from rich.table import Table
from rich import box

from menuqr import __version__
from menuqr.core.config import get_settings
from menuqr.core.models import Category, MenuItem, MenuItemCreate, Table, TableCreate
from menuqr.core.store import MenuStore
from menuqr.core.qr_generator import generate_table_qr, generate_menu_qr

console = Console()


@click.group()
@click.version_option(__version__, prog_name="menuqr")
def main():
    """MenuQR Pro — Menús digitales con QR."""


@main.command()
def version():
    click.echo(f"MenuQR Pro v{__version__}")


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8008, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server."""
    import uvicorn
    uvicorn.run("menuqr.server:app", host=host, port=port, reload=reload)


@main.command(name="add-category")
@click.option("--id", prompt="ID (ej. entradas)")
@click.option("--name", prompt="Nombre")
@click.option("--sort", type=int, default=0, prompt="Orden (0=primero)")
def add_category(id, name, sort):
    """Add a menu category."""
    c = Category(id=id.lower().replace(" ", "_"), name=name, sort_order=sort)
    MenuStore().save_category(c)
    console.print(f"[green]✓ Categoría:[/green] {c.name}")


@main.command(name="add-item")
@click.option("--category", prompt="Categoría ID")
@click.option("--name", prompt="Nombre")
@click.option("--price", type=float, prompt="Precio")
@click.option("--desc", default="", prompt="Descripción")
@click.option("--veg", is_flag=True, help="Vegetariano")
@click.option("--vegan", is_flag=True, help="Vegano")
@click.option("--gluten-free", "gf", is_flag=True, help="Gluten-free")
@click.option("--spicy", is_flag=True, help="Picante")
def add_item(category, name, price, desc, veg, vegan, gf, spicy):
    """Add a menu item."""
    item = MenuItem(
        id=f"ITM-{__import__('uuid').uuid4().hex[:8].upper()}",
        category_id=category,
        name=name,
        description=desc,
        price=Decimal(str(price)),
        is_vegetarian=veg,
        is_vegan=vegan,
        is_gluten_free=gf,
        is_spicy=spicy,
    )
    MenuStore().save_item(item)
    console.print(f"[green]✓ Item:[/green] {item.name} — ${item.price}")


@main.command(name="add-table")
@click.option("--number", type=int, prompt="Número de mesa")
@click.option("--name", default="", prompt="Nombre (opcional)")
@click.option("--capacity", type=int, default=4, prompt="Capacidad")
@click.option("--location", default="interior", prompt="Ubicación (interior/terraza/bar)")
def add_table(number, name, capacity, location):
    """Add a restaurant table."""
    import uuid
    t = Table(
        id=f"TBL-{uuid.uuid4().hex[:8].upper()}",
        number=number, name=name, capacity=capacity, location=location,
    )
    MenuStore().save_table(t)
    console.print(f"[green]✓ Mesa {t.number}:[/green] {t.id}")


@main.command()
@click.argument("table_id")
@click.option("--out", "-o", type=click.Path(), default=None, help="Output file (default: stdout)")
def qr(table_id, out):
    """Generate QR code for a table."""
    if out:
        from pathlib import Path
        generate_table_qr(table_id)
        # Save to file via generator's output_path
        from menuqr.core.qr_generator import generate_qr
        s = get_settings()
        url = f"{s.qr_base_url}/m/{table_id}"
        path = generate_qr(url, output_path=out, color=s.qr_color, bg_color=s.qr_bg_color)
        console.print(f"[green]✓ QR saved to {path}[/green]")
    else:
        # Print URL
        s = get_settings()
        url = f"{s.qr_base_url}/m/{table_id}"
        console.print(f"[cyan]URL:[/cyan] {url}")
        console.print(f"[dim](Use --out file.png to save image)[/dim]")


@main.command(name="list-items")
def list_items():
    """List menu items."""
    items = MenuStore().list_items()
    if not items:
        console.print("[yellow]No hay items[/yellow]")
        return
    table = Table(title=f"Items ({len(items)})", box=box.ROUNDED)
    table.add_column("ID", style="dim")
    table.add_column("Categoría")
    table.add_column("Nombre")
    table.add_column("Precio", justify="right")
    table.add_column("Tags")
    for i in items:
        tags = []
        if i.is_vegetarian: tags.append("🌿")
        if i.is_vegan: tags.append("🌱")
        if i.is_gluten_free: tags.append("🌾")
        if i.is_spicy: tags.append("🌶️")
        table.add_row(i.id[:12], i.category_id, i.name, f"${i.price}", " ".join(tags))
    console.print(table)


@main.command(name="list-orders")
def list_orders():
    """List orders."""
    orders = MenuStore().list_orders()
    if not orders:
        console.print("[yellow]No hay pedidos[/yellow]")
        return
    table = Table(title=f"Pedidos ({len(orders)})", box=box.ROUNDED)
    table.add_column("ID", style="bold")
    table.add_column("Mesa")
    table.add_column("Items", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Estado")
    table.add_column("Hora")
    for o in sorted(orders, key=lambda x: x.created_at, reverse=True):
        table.add_row(
            o.id[:12], str(o.table_number), str(len(o.items)),
            f"${o.total}", o.status, o.created_at.strftime("%H:%M"),
        )
    console.print(table)


if __name__ == "__main__":
    main()
