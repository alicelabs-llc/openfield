"""WhatsAppBot Pro — FastAPI server + webhook receiver."""
from __future__ import annotations
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from wabotpro import __version__
from wabotpro.core.config import get_settings
from wabotpro.core.models import Message, MessageType, Product, Order
from wabotpro.core.store import Store
from wabotpro.flows import FlowEngine
from wabotpro.handlers import WhatsAppCloudClient

app = FastAPI(
    title="WhatsAppBot Pro",
    description="Bot de WhatsApp para negocios LATAM. Catálogo, pedidos, flujos conversacionales.",
    version=__version__,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = Path(__file__).parent.parent.parent / "web"
store = Store()
flow = FlowEngine(store)
wa_client = WhatsAppCloudClient()


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>WhatsAppBot Pro v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "business_name": s.business_name,
        "catalog_size": len(store.get_catalog()),
        "orders_total": len(store.get_orders()),
        "wa_configured": bool(s.wa_access_token and s.wa_phone_number_id),
    }


# === WhatsApp Webhook ===

@app.get("/webhook")
async def webhook_verify(
    hub_mode: str = Query("", alias="hub.mode"),
    hub_challenge: str = Query("", alias="hub.challenge"),
    hub_verify_token: str = Query("", alias="hub.verify_token"),
):
    """Meta webhook verification."""
    s = get_settings()
    if hub_mode == "subscribe" and hub_verify_token == s.wa_verify_token:
        return int(hub_challenge)
    raise HTTPException(403, "Invalid verify token")


@app.post("/webhook")
async def webhook_receive(req: Request, bg: BackgroundTasks):
    """Receive incoming WhatsApp messages."""
    payload = await req.json()
    bg.add_task(_process_incoming, payload)
    return {"status": "received"}


async def _process_incoming(payload: dict):
    """Parse Meta webhook and respond."""
    try:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" not in value:
                    continue
                for msg in value["messages"]:
                    if msg.get("type") != "text":
                        continue
                    from_number = msg.get("from", "")
                    text = msg.get("text", {}).get("body", "")
                    incoming = Message(
                        from_number=from_number,
                        to_number=value.get("metadata", {}).get("phone_number_id", ""),
                        text=text,
                        type=MessageType.TEXT,
                        raw=msg,
                    )
                    responses = flow.process(incoming)
                    for r in responses:
                        await wa_client.send_text(from_number, r)
    except Exception:
        pass


# === Catalog API ===

@app.get("/v1/catalog")
async def list_catalog():
    return [p.model_dump() for p in store.get_catalog()]


@app.post("/v1/catalog")
async def add_product(product: Product):
    store.add_product(product)
    return {"added": product.id}


@app.delete("/v1/catalog/{product_id}")
async def remove_product(product_id: str):
    if not store.remove_product(product_id):
        raise HTTPException(404, "Product not found")
    return {"removed": product_id}


# === Orders API ===

@app.get("/v1/orders")
async def list_orders():
    return [o.model_dump() for o in store.get_orders()]


@app.get("/v1/orders/{order_id}")
async def get_order(order_id: str):
    o = store.get_order(order_id)
    if not o:
        raise HTTPException(404, "Order not found")
    return o.model_dump()


# === Send message API ===

@app.post("/v1/send")
async def send_message(to: str, text: str):
    """Send a message to a WhatsApp number."""
    return await wa_client.send_text(to, text)


# === Simulate message (for testing without WA) ===

@app.post("/v1/simulate")
async def simulate_message(from_number: str, text: str):
    """Simulate an incoming message (for testing flows without WhatsApp)."""
    incoming = Message(from_number=from_number, to_number="bot", text=text)
    responses = flow.process(incoming)
    return {"responses": responses}
