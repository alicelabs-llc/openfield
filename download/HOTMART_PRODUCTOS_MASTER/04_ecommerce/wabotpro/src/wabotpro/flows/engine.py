"""WhatsAppBot Pro — Conversation flow engine.

State machine: start → browsing → cart → checkout → confirming → done
Each state has handlers that produce outgoing messages.
"""
from __future__ import annotations
import re
from wabotpro.core.models import ConversationState, Message, Product
from wabotpro.core.store import Store


class FlowEngine:
    """Process incoming messages and produce outgoing responses."""

    def __init__(self, store: Store):
        self.store = store
        self.states: dict[str, ConversationState] = {}

    def get_state(self, customer_number: str) -> ConversationState:
        if customer_number not in self.states:
            self.states[customer_number] = ConversationState(customer_number=customer_number)
        return self.states[customer_number]

    def reset(self, customer_number: str):
        self.states[customer_number] = ConversationState(customer_number=customer_number)

    def process(self, message: Message) -> list[str]:
        """Returns list of outgoing message texts to send."""
        state = self.get_state(message.from_number)
        text = message.text.strip()
        text_lower = text.lower()

        # Global commands
        if text_lower in ("menu", "inicio", "hola", "start", "hi"):
            self.reset(message.from_number)
            return self._render_menu()

        if text_lower in ("catalogo", "catálogo", "productos", "productos"):
            return self._render_catalog()

        if text_lower in ("carrito", "cart", "ver carrito"):
            return self._render_cart(state)

        if text_lower in ("confirmar", "checkout", "pedido"):
            return self._checkout(state)

        if text_lower in ("ayuda", "help"):
            return [
                "🛒 *Comandos disponibles*\n\n"
                "• `menu` — ver menú principal\n"
                "• `catálogo` — ver productos\n"
                "• `carrito` — ver tu carrito\n"
                "• `agregar <id> <qty>` — agregar al carrito\n"
                "• `quitar <id>` — quitar del carrito\n"
                "• `confirmar` — finalizar pedido\n"
                "• `ayuda` — esta lista"
            ]

        # Add to cart: "agregar P001 2"
        m = re.match(r"(?:agregar|add|comprar)\s+(\w+)\s*(\d+)?", text_lower)
        if m:
            product_id = m.group(1).upper()
            qty = int(m.group(2)) if m.group(2) else 1
            return self._add_to_cart(state, product_id, qty)

        # Remove from cart
        m = re.match(r"(?:quitar|remove|eliminar)\s+(\w+)", text_lower)
        if m:
            return self._remove_from_cart(state, m.group(1).upper())

        # Search
        m = re.match(r"(?:buscar|search)\s+(.+)", text_lower)
        if m:
            return self._search_products(m.group(1))

        # Default: echo help
        return [
            f"Hola 👋 No entendí tu mensaje.\n\n"
            f"Escribe `menu` para ver opciones, `catálogo` para ver productos, "
            f"o `ayuda` para ver todos los comandos."
        ]

    def _render_menu(self) -> list[str]:
        return [
            f"🛒 *{self.store.settings.business_name}*\n\n"
            f"Horario: {self.store.settings.business_hours}\n\n"
            f"¿Qué deseas hacer?\n\n"
            f"• Escribe `catálogo` para ver productos\n"
            f"• Escribe `ayuda` para ver todos los comandos"
        ]

    def _render_catalog(self) -> list[str]:
        catalog = self.store.get_catalog()
        if not catalog:
            return ["📂 El catálogo está vacío. El administrador debe agregar productos."]
        lines = ["📂 *Catálogo*\n"]
        for p in catalog[:20]:
            stock_str = f" (stock: {p.stock})" if p.stock > 0 else " (sin stock)"
            lines.append(f"• *{p.id}* — {p.name}\n  ${p.price} {p.currency}{stock_str}")
        lines.append(f"\n_Para comprar: `agregar <ID> <cantidad>`_")
        return ["\n".join(lines)]

    def _add_to_cart(self, state: ConversationState, product_id: str, qty: int) -> list[str]:
        product = self.store.find_product(product_id)
        if not product:
            return [f"❌ Producto '{product_id}' no encontrado. Escribe `catálogo` para ver disponibles."]
        if product.stock > 0 and product.stock < qty:
            return [f"⚠️ Solo hay {product.stock} unidades disponibles de '{product.name}'."]
        from wabotpro.core.models import CartItem
        # Check if already in cart
        for item in state.cart:
            if item.product_id == product_id:
                item.quantity += qty
                return [
                    f"✅ Actualizado: {product.name} x{item.quantity}\n"
                    f"Subtotal: ${item.subtotal:.2f}\n\n"
                    f"Escribe `carrito` para ver todo, `confirmar` para pedir."
                ]
        state.cart.append(CartItem(
            product_id=product.id,
            product_name=product.name,
            quantity=qty,
            unit_price=product.price,
        ))
        state.state = "cart"
        return [
            f"✅ Agregado: {product.name} x{qty}\n"
            f"Subtotal: ${product.price * qty:.2f} {product.currency}\n\n"
            f"Escribe `catálogo` para seguir comprando, `confirmar` para pedir."
        ]

    def _remove_from_cart(self, state: ConversationState, product_id: str) -> list[str]:
        before = len(state.cart)
        state.cart = [i for i in state.cart if i.product_id != product_id]
        if len(state.cart) < before:
            return [f"🗑️ Producto {product_id} quitado del carrito."]
        return [f"❌ Producto {product_id} no estaba en tu carrito."]

    def _render_cart(self, state: ConversationState) -> list[str]:
        if not state.cart:
            return ["🛒 Tu carrito está vacío.\nEscribe `catálogo` para ver productos."]
        lines = ["🛒 *Tu carrito*\n"]
        total = sum((i.subtotal for i in state.cart), 0)
        for i in state.cart:
            lines.append(f"• {i.product_name} x{i.quantity} = ${i.subtotal:.2f}")
        lines.append(f"\n*Total: ${total:.2f}*")
        lines.append(f"\nEscribe `confirmar` para finalizar el pedido.")
        return ["\n".join(lines)]

    def _checkout(self, state: ConversationState) -> list[str]:
        if not state.cart:
            return ["🛒 Tu carrito está vacío."]
        from wabotpro.core.models import Order
        import uuid
        order = Order(
            id=f"ORD-{str(uuid.uuid4())[:8].upper()}",
            customer_number=state.customer_number,
            items=list(state.cart),
            status="confirmed",
        )
        self.store.save_order(order)
        total = sum((i.subtotal for i in state.cart), 0)
        lines = [
            "✅ *Pedido confirmado*\n",
            f"Orden: *{order.id}*",
            f"\nDetalle:",
        ]
        for i in state.cart:
            lines.append(f"• {i.product_name} x{i.quantity} = ${i.subtotal:.2f}")
        lines.append(f"\n*Total: ${total:.2f}*")
        lines.append(f"\nRecibirás una notificación cuando tu pedido esté listo. 🙏")
        self.reset(state.customer_number)
        return ["\n".join(lines)]

    def _search_products(self, query: str) -> list[str]:
        catalog = self.store.get_catalog()
        matches = [p for p in catalog if query.lower() in p.name.lower() or query.lower() in (p.description or "").lower()]
        if not matches:
            return [f"🔍 No encontré productos para '{query}'."]
        lines = [f"🔍 *Resultados para '{query}'*\n"]
        for p in matches[:10]:
            lines.append(f"• *{p.id}* — {p.name} — ${p.price}")
        return ["\n".join(lines)]
