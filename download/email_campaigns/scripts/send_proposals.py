#!/usr/bin/env python3
"""
send_proposals.py — Envía los 8 emails HTML vía Hostinger SMTP

REQUIERE: contraseña SMTP de contact@alicelabs.site
Setear en variable de entorno: ALICELABS_SMTP_PASSWORD

Uso:
    export ALICELABS_SMTP_PASSWORD="tu_password_de_hostinger"
    python3 send_proposals.py --all              # envía los 8
    python3 send_proposals.py --only 1            # solo C&D Municipal
    python3 send_proposals.py --only 6            # solo Westside
    python3 send_proposals.py --dry-run --all     # simular sin enviar
"""
from __future__ import annotations
import os
import smtplib
import ssl
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# === Configuración ===
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SENDER_EMAIL = "contact@alicelabs.site"
SENDER_NAME = "AliceLabs LLC"

# === Prospects ===
PROSPECTS = [
    {
        "id": 1,
        "name": "C&D Municipal Sales",
        "to": "sales@c-dmunicipal.com",
        "subject": "Propuesta: Rediseño WordPress + Directorio Dinámico — AliceLabs",
        "html_file": "01_cd_municipal_sales.html",
    },
    {
        "id": 2,
        "name": "Small Business (Squarespace)",
        "to": None,  # Upwork — no email directo, responder por plataforma
        "subject": "Tu nuevo sitio Squarespace — Listo en 7 días por $500",
        "html_file": "02_squarespace_small_business.html",
        "note": "Responder vía Upwork — no hay email directo disponible",
    },
    {
        "id": 3,
        "name": "Food4Fitness (Australia)",
        "to": None,  # Upwork
        "subject": "Proposal: WooCommerce Migration + Monthly Design Retainer — AliceLabs",
        "html_file": "03_food4fitness_woocommerce.html",
        "note": "Responder vía Upwork — acepta proveedores internacionales",
    },
    {
        "id": 4,
        "name": "THE ARCANE (Shopify)",
        "to": None,  # Upwork
        "subject": "THE ARCANE × AliceLabs — Luxury Shopify Store",
        "html_file": "04_the_arcane_shopify.html",
        "note": "Responder vía Upwork — verificar si sigue abierto (18-26 oct)",
    },
    {
        "id": 5,
        "name": "Sola Coffee Bar",
        "to": None,  # Upwork
        "subject": "Propuesta: Diseño de Merchandising — Tote, Camiseta, Vaso",
        "html_file": "05_sola_coffee_bar_merch.html",
        "note": "Responder vía Upwork",
    },
    {
        "id": 6,
        "name": "Westside Regional Center",
        "to": None,  # RFP — buscar email de compras
        "subject": "Proposal: WordPress Redesign, Accessibility & UX — AliceLabs LLC",
        "html_file": "06_westside_regional_center.html",
        "note": "RFP en Upscale Method — buscar contacto de compras en el documento original",
    },
    {
        "id": 7,
        "name": "Newton County Commission",
        "to": None,  # RFP — buscar email
        "subject": "Proposal: Government Website Migration & Security — AliceLabs LLC",
        "html_file": "07_newton_county_commission.html",
        "note": "RFP en Upscale Method — buscar contacto de compras",
    },
    {
        "id": 8,
        "name": "Visit Columbia",
        "to": None,  # RFP — buscar email
        "subject": "Proposal: Tourism Website + CRM + Destination Directory — AliceLabs",
        "html_file": "08_visit_columbia_tourism.html",
        "note": "RFP — deadline 29 oct, urgente. Buscar email de turismo/IT",
    },
]

HTML_DIR = Path("/home/z/my-project/download/email_campaigns/html")


def log(level: str, msg: str) -> None:
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "FAIL": "❌", "SEND": "📤", "SKIP": "⏭️"}
    print(f"{icons.get(level, '•')} [{level}] {msg}")


def send_email(to: str, subject: str, html_content: str, dry_run: bool = False) -> bool:
    """Send HTML email via Hostinger SMTP."""
    if dry_run:
        log("SKIP", f"[DRY RUN] Email a: {to} | Asunto: {subject}")
        return True

    password = os.environ.get("ALICELABS_SMTP_PASSWORD", "")
    if not password:
        log("FAIL", "ALICELABS_SMTP_PASSWORD no configurada. Ejecuta: export ALICELABS_SMTP_PASSWORD='tu_password'")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as server:
            server.login(SENDER_EMAIL, password)
            server.sendmail(SENDER_EMAIL, [to], msg.as_string())
        log("SEND", f"✅ Enviado a: {to} | Asunto: {subject}")
        return True
    except smtplib.SMTPAuthenticationError:
        log("FAIL", f"Auth falló para {SENDER_EMAIL} — verifica la contraseña")
        return False
    except Exception as e:
        log("FAIL", f"Error enviando a {to}: {type(e).__name__}: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enviar propuestas AliceLabs vía Hostinger SMTP")
    parser.add_argument("--all", action="store_true", help="Enviar todos los que tengan email")
    parser.add_argument("--only", type=int, help="Enviar solo un prospecto por ID")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin enviar")
    args = parser.parse_args()

    log("INFO", "=== AliceLabs Proposal Sender ===")
    log("INFO", f"SMTP: {SMTP_HOST}:{SMTP_PORT} | From: {SENDER_EMAIL}")
    log("INFO", f"Dry run: {args.dry_run}")
    print()

    # Password check
    if not args.dry_run:
        password = os.environ.get("ALICELABS_SMTP_PASSWORD", "")
        if not password:
            log("FAIL", "ALICELABS_SMTP_PASSWORD no configurada.")
            log("INFO", "Ejecuta: export ALICELABS_SMTP_PASSWORD='tu_password_de_hostinger'")
            log("INFO", "O usa --dry-run para simular")
            return 1

    # Filter prospects
    if args.only:
        prospects = [p for p in PROSPECTS if p["id"] == args.only]
    elif args.all:
        prospects = PROSPECTS
    else:
        log("WARN", "Especifica --all o --only N")
        return 1

    sent = 0
    skipped = 0
    failed = 0

    for p in prospects:
        html_path = HTML_DIR / p["html_file"]
        if not html_path.exists():
            log("FAIL", f"#{p['id']} {p['name']}: HTML no encontrado: {html_path}")
            failed += 1
            continue

        html_content = html_path.read_text(encoding="utf-8")

        if p["to"]:
            log("INFO", f"#{p['id']} {p['name']} → {p['to']}")
            if send_email(p["to"], p["subject"], html_content, dry_run=args.dry_run):
                sent += 1
            else:
                failed += 1
            # 35s delay between sends (anti-spam)
            if not args.dry_run:
                time.sleep(35)
        else:
            log("SKIP", f"#{p['id']} {p['name']}: Sin email directo — {p.get('note', 'responder vía plataforma')}")
            log("INFO", f"   HTML listo en: {html_path}")
            skipped += 1

    print()
    log("OK", f"=== Resumen: {sent} enviados · {skipped} sin email (Upwork/RFP) · {failed} fallidos ===")

    if skipped > 0:
        log("INFO", "Los prospectos sin email directo requieren:")
        log("INFO", "  - Upwork: responder desde la plataforma con el HTML como mensaje")
        log("INFO", "  - RFPs: buscar contacto de compras en el documento original")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
