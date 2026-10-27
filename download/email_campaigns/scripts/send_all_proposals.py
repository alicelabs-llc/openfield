#!/usr/bin/env python3
"""
send_all_proposals.py — Envía TODAS las propuestas con email directo vía Hostinger SMTP
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

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SENDER_EMAIL = "contact@alicelabs.site"
SENDER_NAME = "AliceLabs LLC"
PASSWORD = os.environ.get("ALICELABS_SMTP_PASSWORD", "Emm@darla201500")

HTML_DIR = Path("/home/z/my-project/download/email_campaigns/html")

# 7 prospectos con email directo directo — ordenados por urgencia de deadline
PROSPECTS = [
    {"id": 1, "name": "C&D Municipal Sales", "to": "sales@c-dmunicipal.com",
     "subject": "Propuesta: Rediseño WordPress + Directorio Dinámico — AliceLabs",
     "html": "01_cd_municipal_sales.html", "budget": "$5,000", "deadline": "abiierto"},
    {"id": 9, "name": "City of Lake Oswego, OR", "to": "tramirez@lakeoswego.city",
     "subject": "Proposal: Municipal Website Redesign, CMS & Migration — AliceLabs LLC",
     "html": "09_lake_oswego.html", "budget": "~$30k", "deadline": "28 oct URGENTE"},
    {"id": 10, "name": "CSKT Tribes", "to": "elizabeth.dempsey@cskt.org",
     "subject": "Proposal: Web Design, Digital Brand & GIS Integration — AliceLabs LLC",
     "html": "10_cskt_tribes.html", "budget": "~$50k", "deadline": "29 oct URGENTE"},
    {"id": 14, "name": "CAMWS", "to": "nominating@camws.org",
     "subject": "Proposal: Website Redesign & Development — AliceLabs LLC",
     "html": "14_camws.html", "budget": "~$18k", "deadline": "30 oct"},
    {"id": 11, "name": "LA Cultural Affairs", "to": "lex.gelb@lacity.org",
     "subject": "Proposal: Visual Identity, Logo & Event Graphics — AliceLabs LLC",
     "html": "11_la_cultural_affairs.html", "budget": "up to $75k", "deadline": "5 nov"},
    {"id": 12, "name": "City of Loveland, CO", "to": "dan.coldiron@cityofloveland.org",
     "subject": "Proposal: Website Migration & Consolidation — AliceLabs LLC",
     "html": "12_loveland_co.html", "budget": "~$32k", "deadline": "19 nov"},
    {"id": 13, "name": "West Valley Water District", "to": "lgranados@wvwd.org",
     "subject": "Proposal: Website Redesign & Maintenance — AliceLabs LLC",
     "html": "13_west_valley_water.html", "budget": "~$25k", "deadline": "20 nov"},
]

def send_email(to: str, subject: str, html_content: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg["Reply-To"] = SENDER_EMAIL
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, [to], msg.as_string())
        return True
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {e}")
        return False

def main():
    dry_run = "--dry-run" in sys.argv

    print(f"📤 AliceLabs Proposal Sender — {len(PROSPECTS)} prospectos")
    print(f"   SMTP: {SMTP_HOST}:{SMTP_PORT}")
    print(f"   From: {SENDER_EMAIL}")
    print(f"   Dry run: {dry_run}")
    print()

    sent = 0
    failed = 0

    for p in PROSPECTS:
        html_path = HTML_DIR / p["html"]
        if not html_path.exists():
            print(f"  ❌ #{p['id']} {p['name']}: HTML no encontrado")
            failed += 1
            continue

        html = html_path.read_text(encoding="utf-8")

        if dry_run:
            print(f"  ⏭️  [DRY] #{p['id']} {p['name']} → {p['to']} | {p['budget']} | {p['deadline']}")
            sent += 1
            continue

        print(f"  📤 #{p['id']} {p['name']} → {p['to']} ({p['budget']} | {p['deadline']})...")

        if send_email(p["to"], p["subject"], html):
            print(f"  ✅ Enviado!")
            sent += 1
        else:
            print(f"  ❌ Falló")
            failed += 1

        if p != PROSPECTS[-1]:
            print(f"  ⏳ Esperando 35s (anti-spam)...")
            time.sleep(35)

    print()
    print(f"📊 Resumen: {sent} enviados · {failed} fallidos")

    if not dry_run and sent > 0:
        # Log
        log_path = Path("/home/z/my-project/download/email_campaigns/tracking/sent_log.json")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        import json
        from datetime import datetime
        log = {
            "sent_at": datetime.utcnow().isoformat(),
            "from": SENDER_EMAIL,
            "total_sent": sent,
            "total_failed": failed,
            "prospects": [{"to": p["to"], "subject": p["subject"], "budget": p["budget"]} for p in PROSPECTS]
        }
        log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print(f"📝 Log guardado: {log_path}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
