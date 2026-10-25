"""MenuQR Pro — FastAPI server."""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from menuqr import __version__
from menuqr.core.config import get_settings
from menuqr.core.models import (
    Category, MenuItem, MenuItemCreate, Table, TableCreate, Order,
)
from menuqr.core.store import MenuStore
from menuqr.core.qr_generator import generate_qr, generate_table_qr, generate_menu_qr

app = FastAPI(
    title="MenuQR Pro",
    description="Menús digitales con QR para restaurantes. Self-hosted, multi-idioma.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"

store = MenuStore()


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>MenuQR Pro v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "restaurant": s.restaurant_name,
        "categories": len(store.list_categories()),
        "items": len(store.list_items()),
        "tables": len(store.list_tables()),
        "orders_today": len([o for o in store.list_orders() if o.created_at.date() == datetime.utcnow().date()]),
    }


# === Public menu endpoints (no auth, scanned from QR) ===

@app.get("/menu/{menu_id}", response_class=HTMLResponse)
async def view_menu(menu_id: str, lang: str = "es"):
    """Public menu view (scanned from QR code)."""
    menu = store.get_full_menu()
    # Render simple HTML menu (in production: Jinja2 template)
    html = _render_menu_html(menu, lang)
    return HTMLResponse(html)


@app.get("/m/{table_id}", response_class=HTMLResponse)
async def view_menu_for_table(table_id: str, lang: str = "es"):
    """Public menu view tied to a specific table (for ordering)."""
    table = store.get_table(table_id)
    if not table:
        raise HTTPException(404, "Table not found")
    menu = store.get_full_menu()
    html = _render_menu_html(menu, lang, table=table)
    return HTMLResponse(html)


def _render_menu_html(menu, lang: str = "es", table: Table = None) -> str:
    """Render a simple HTML menu."""
    s = get_settings()
    rows = []
    for cat in menu.categories:
        rows.append(f'<h2>{cat.name}</h2>')
        for item in menu.get_by_category(cat.id):
            tags = []
            if item.is_vegetarian: tags.append("🌿 Veg")
            if item.is_vegan: tags.append("🌱 Vegan")
            if item.is_gluten_free: tags.append("🌾 GF")
            if item.is_spicy: tags.append("🌶️ Spicy")
            tags_str = " ".join(tags)
            rows.append(f"""
            <div class="item">
                <div class="item-name">{item.name} <span class="price">${item.price}</span></div>
                <div class="item-desc">{item.description}</div>
                <div class="tags">{tags_str}</div>
            </div>
            """)
    table_html = f"<p>Mesa {table.number}</p>" if table else ""
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s.restaurant_name} — Menú</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 700px; margin: 0 auto; padding: 24px; background: #f8f9fa; }}
h1 {{ color: #2d3748; }}
h2 {{ color: #4a5568; border-bottom: 2px solid #cbd5e0; padding-bottom: 8px; margin-top: 32px; }}
.item {{ padding: 12px 0; border-bottom: 1px solid #e2e8f0; }}
.item-name {{ font-weight: bold; font-size: 16px; }}
.price {{ color: #38a169; float: right; }}
.item-desc {{ color: #718096; font-size: 14px; margin-top: 4px; }}
.tags {{ margin-top: 6px; font-size: 12px; color: #4a5568; }}
</style></head><body>
<h1>{s.restaurant_name}</h1>
{table_html}
{''.join(rows)}
</body></html>"""


# === Admin endpoints ===

@app.get("/admin/menu")
async def get_full_menu():
    """Get full menu structure (categories + items)."""
    return store.get_full_menu().model_dump()


@app.post("/admin/categories")
async def create_category(cat: Category):
    store.save_category(cat)
    return cat


@app.post("/admin/items")
async def create_item(item: MenuItemCreate):
    """Add a menu item."""
    new = MenuItem(
        id=f"ITM-{str(uuid.uuid4())[:8].upper()}",
        **item.model_dump(),
    )
    store.save_item(new)
    return new


@app.delete("/admin/items/{item_id}")
async def delete_item(item_id: str):
    if not store.delete_item(item_id):
        raise HTTPException(404, "Item not found")
    return {"deleted": item_id}


@app.get("/admin/items")
async def list_items(category_id: str = None, available_only: bool = False):
    items = store.list_items(category_id=category_id, available_only=available_only)
    return [i.model_dump() for i in items]


# Tables
@app.get("/admin/tables")
async def list_tables():
    return [t.model_dump() for t in store.list_tables()]


@app.post("/admin/tables")
async def create_table(table: TableCreate):
    new = Table(
        id=f"TBL-{str(uuid.uuid4())[:8].upper()}",
        **table.model_dump(),
    )
    store.save_table(new)
    return new


@app.get("/admin/tables/{table_id}/qr")
async def get_table_qr(table_id: str):
    """Get QR code image for a table."""
    if not store.get_table(table_id):
        raise HTTPException(404, "Table not found")
    img_bytes = generate_table_qr(table_id)
    return Response(content=img_bytes, media_type="image/png")


@app.get("/admin/menu/qr")
async def get_menu_qr():
    """Get QR code for the general menu."""
    img_bytes = generate_menu_qr()
    return Response(content=img_bytes, media_type="image/png")


# Orders
@app.post("/public/order")
async def place_order(table_id: str, items: list[dict], notes: str = ""):
    """Customer places an order via QR."""
    table = store.get_table(table_id)
    if not table:
        raise HTTPException(404, "Table not found")

    total = Decimal("0")
    for order_item in items:
        item = store.get_item(order_item.get("item_id"))
        if item and item.available:
            qty = order_item.get("qty", 1)
            total += item.price * qty

    order = Order(
        id=f"ORD-{str(uuid.uuid4())[:8].upper()}",
        table_id=table_id,
        table_number=table.number,
        items=items,
        total=total,
        customer_notes=notes,
        status="pending",
    )
    store.save_order(order)
    return order


@app.get("/admin/orders")
async def list_orders(status: str = None):
    orders = store.list_orders(status=status)
    return [o.model_dump() for o in orders]


@app.post("/admin/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    order = store.get_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    order.status = status
    if status == "served" and not order.served_at:
        order.served_at = datetime.utcnow()
    store.save_order(order)
    return order
