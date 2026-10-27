#!/usr/bin/env python3
"""
send_all_proposals_v2.py — Envía TODAS las propuestas vía Gmail SMTP
(usando eddyflores100@gmail.com con Reply-To contact@alicelabs.site)
"""
from __future__ import annotations
import smtplib, ssl, sys, time, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid
from pathlib import Path
from datetime import datetime

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "eddyflores100@gmail.com"
SENDER_NAME = "AliceLabs LLC"
REPLY_TO = "contact@alicelabs.site"
PASSWORD = "kbgnmxmcsemjolzz"

HTML_DIR = Path("/home/z/my-project/download/email_campaigns/html")

# 23 prospectos — solo los que tienen email directo
PROSPECTS = [
    # --- URGENTES (deadline esta semana) ---
    {"id": 1, "name": "City of Lake Oswego", "to": "tramirez@lakeoswego.city",
     "subject": "Proposal: Municipal Website Redesign, CMS & Migration — AliceLabs LLC",
     "html": "09_lake_oswego.html", "budget": "~$30k", "deadline": "28 oct URGENTE"},
    {"id": 2, "name": "CSKT Tribes", "to": "elizabeth.dempsey@cskt.org",
     "subject": "Proposal: Web Design, Digital Brand & GIS Integration — AliceLabs LLC",
     "html": "10_cskt_tribes.html", "budget": "~$50k", "deadline": "29 oct URGENTE"},
    {"id": 3, "name": "CAMWS", "to": "nominating@camws.org",
     "subject": "Proposal: Website Redesign & Development — AliceLabs LLC",
     "html": "14_camws.html", "budget": "~$18k", "deadline": "30 oct"},
    {"id": 4, "name": "CARFAC Alberta", "to": "communications@carfacalberta.com",
     "subject": "Proposal: Visual Identity, Brand Manual & Graphic Resources — AliceLabs LLC",
     "html": "15_carfac_alberta.html", "budget": "TBD", "deadline": "30 oct"},
    {"id": 5, "name": "City of Vancouver WA", "to": "procurement@cityofvancouver.us",
     "subject": "Proposal: Website Redesign, Migration & Support — AliceLabs LLC",
     "html": "16_vancouver_wa.html", "budget": "TBD", "deadline": "4 nov"},
    {"id": 6, "name": "HomeFront", "to": "info@homefrontnj.org",
     "subject": "Proposal: Website Redesign & Accessible CMS — AliceLabs LLC",
     "html": "17_homefront.html", "budget": "TBD", "deadline": "4 nov"},
    {"id": 7, "name": "Connecticut Agency (RFP SEO-0155)", "to": "rfp@ct.gov",
     "subject": "Proposal: Graphic Design, Digital Communications & Social Media — AliceLabs LLC",
     "html": "18_connecticut_rfp.html", "budget": "TBD", "deadline": "3 nov"},
    # --- Semana que viene ---
    {"id": 8, "name": "LA Cultural Affairs", "to": "lex.gelb@lacity.org",
     "subject": "Proposal: Visual Identity, Logo & Event Graphics — AliceLabs LLC",
     "html": "11_la_cultural_affairs.html", "budget": "up to $75k", "deadline": "5 nov"},
    {"id": 9, "name": "IPPF", "to": "jguiney@ippf.org",
     "subject": "Proposal: Software Development & OpenEMR Integration — AliceLabs LLC",
     "html": "19_ippf_openemr.html", "budget": "TBD", "deadline": "6 nov"},
    {"id": 10, "name": "City of Hampton GA", "to": "wmoore@hamptonga.gov",
     "subject": "Proposal: Logo, Visual Identity & Brand Manual — AliceLabs LLC",
     "html": "20_hampton_ga.html", "budget": "TBD", "deadline": "9 nov"},
    {"id": 11, "name": "Achievement First", "to": "rfp@achievementfirst.org",
     "subject": "Proposal: Website Ecosystem Redesign (42 sites) — AliceLabs LLC",
     "html": "21_achievement_first.html", "budget": "TBD", "deadline": "9 nov"},
    {"id": 12, "name": "Wave Transit", "to": "procurement@wavetransit.com",
     "subject": "Proposal: Website Redesign, Integrations, Hosting & Support — AliceLabs LLC",
     "html": "22_wave_transit.html", "budget": "TBD", "deadline": "10 nov"},
    {"id": 13, "name": "Missouri Agency (WDDS-0663)", "to": "rfp@missouri.gov",
     "subject": "Proposal: Website Design, Development & Implementation — AliceLabs LLC",
     "html": "23_missouri_rfp.html", "budget": "TBD", "deadline": "12 nov"},
    {"id": 14, "name": "Texas Agency (WDDS-0666)", "to": "rfp@texas.gov",
     "subject": "Proposal: Web Design, CMS, Migration, Hosting & Support — AliceLabs LLC",
     "html": "24_texas_rfp.html", "budget": "TBD", "deadline": "13 nov"},
    {"id": 15, "name": "City of Loveland CO", "to": "dan.coldiron@cityofloveland.org",
     "subject": "Proposal: Website Migration & Consolidation — AliceLabs LLC",
     "html": "12_loveland_co.html", "budget": "~$32k", "deadline": "19 nov"},
    {"id": 16, "name": "Moffat EDA", "to": "info@moffateda.org",
     "subject": "Proposal: Website, Landing Pages & Maintenance — AliceLabs LLC",
     "html": "25_moffat_eda.html", "budget": "TBD", "deadline": "19 nov"},
    {"id": 17, "name": "Colorado Agency (WDDS-0670)", "to": "rfp@colorado.gov",
     "subject": "Proposal: Web, Maintenance & Corporate Email — AliceLabs LLC",
     "html": "26_colorado_rfp.html", "budget": "TBD", "deadline": "19 nov"},
    {"id": 18, "name": "West Valley Water District", "to": "lgranados@wvwd.org",
     "subject": "Proposal: Website Redesign & Maintenance — AliceLabs LLC",
     "html": "13_west_valley_water.html", "budget": "~$25k", "deadline": "20 nov"},
    {"id": 19, "name": "Ohio Agency (WDDS-0671)", "to": "rfp@ohio.gov",
     "subject": "Proposal: Website Redesign & Intranet — AliceLabs LLC",
     "html": "27_ohio_rfp.html", "budget": "TBD", "deadline": "20 nov"},
    # --- Sin deadline confirmado ---
    {"id": 20, "name": "C&D Municipal Sales", "to": "sales@c-dmunicipal.com",
     "subject": "Propuesta: Rediseño WordPress + Directorio Dinámico — AliceLabs",
     "html": "01_cd_municipal_sales.html", "budget": "$5k", "deadline": "abierto"},
    {"id": 21, "name": "City of Highland Park IL", "to": "abennett@cityhpil.com",
     "subject": "Proposal: Brand Identity, Logo & Visual System — AliceLabs LLC",
     "html": "28_highland_park.html", "budget": "TBD", "deadline": "5 nov*"},
    {"id": 22, "name": "Brooksville Main Street", "to": "chairman@welovebvl.org",
     "subject": "Proposal: Graphic Design & Wayfinding Signage System — AliceLabs LLC",
     "html": "29_brooksville.html", "budget": "TBD", "deadline": "consultar"},
    {"id": 23, "name": "Federation of American Scientists", "to": "info@fas.org",
     "subject": "Proposal: Website Improvements & Technical Maintenance — AliceLabs LLC",
     "html": "30_fas.html", "budget": "TBD", "deadline": "30 oct"},
]


def send_email(to: str, subject: str, html_content: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = to
    msg["Subject"] = subject
    msg["Reply-To"] = REPLY_TO
    msg["Message-ID"] = make_msgid(domain="alicelabs.site")
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
    only_urgent = "--urgent" in sys.argv

    if only_urgent:
        prospects = [p for p in PROSPECTS if "URGENTE" in p["deadline"] or "28 oct" in p["deadline"] or "29 oct" in p["deadline"]]
    else:
        prospects = PROSPECTS

    print(f"📤 AliceLabs Proposal Sender v2 (Gmail SMTP)")
    print(f"   From: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"   Reply-To: {REPLY_TO}")
    print(f"   Total prospectos: {len(prospects)}")
    print(f"   Dry run: {dry_run}")
    print()

    sent = 0
    failed = 0
    skipped = 0
    results = []

    for p in prospects:
        html_path = HTML_DIR / p["html"]

        # Si el HTML no existe, crear uno genérico rápido
        if not html_path.exists():
            print(f"  ⚠️  #{p['id']} {p['name']}: HTML no encontrado ({p['html']}) — creando...")
            # Crear email rápido genérico
            html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="font-family:sans-serif;color:#1a1a2e;">
<div style="max-width:600px;margin:0 auto;padding:20px;">
<h1 style="color:#1a2a4a;">Proposal for {p['name']}</h1>
<p>Dear {p['name']} team,</p>
<p>We are AliceLabs LLC, a Wyoming-registered web development company. We saw your RFP/procurement notice and would like to submit a proposal.</p>
<h2 style="color:#1a2a4a;">What we do</h2>
<ul>
<li>Website design & development (WordPress, custom)</li>
<li>Visual identity & branding</li>
<li>CMS implementation & migration</li>
<li>WCAG 2.1 AA accessibility compliance</li>
<li>Ongoing maintenance & support</li>
</ul>
<h2 style="color:#1a2a4a;">About AliceLabs</h2>
<p>AliceLabs LLC (Wyoming, USA) with team in Ecuador. We work with government, institutional, and commercial clients. W-9, insurance, E-Verify, and references available upon request.</p>
<h2 style="color:#1a2a4a;">Next Steps</h2>
<ol>
<li>Reply to schedule a 30-min consultation call</li>
<li>We deliver formal proposal + W-9 within 48 hours</li>
<li>Contact: <a href="mailto:contact@alicelabs.site">contact@alicelabs.site</a> · marketnow.site</li>
</ol>
<p style="margin-top:24px;color:#666;font-size:12px;">AliceLabs LLC · Wyoming, USA · Reply "unsubscribe" to stop</p>
</div>
</body></html>"""
            html_path.parent.mkdir(parents=True, exist_ok=True)
            html_path.write_text(html_content, encoding="utf-8")
            print(f"  ✅ HTML creado: {html_path.name}")

        html_content = html_path.read_text(encoding="utf-8")

        if dry_run:
            print(f"  ⏭️  [DRY] #{p['id']} {p['name']} → {p['to']} | {p['budget']} | {p['deadline']}")
            sent += 1
            results.append({"id": p["id"], "name": p["name"], "to": p["to"], "status": "dry_run"})
            continue

        print(f"  📤 #{p['id']} {p['name']} → {p['to']} ({p['budget']} | {p['deadline']})...")

        if send_email(p["to"], p["subject"], html_content):
            print(f"  ✅ Enviado!")
            sent += 1
            results.append({"id": p["id"], "name": p["name"], "to": p["to"], "status": "sent"})
        else:
            failed += 1
            results.append({"id": p["id"], "name": p["name"], "to": p["to"], "status": "failed"})

        # 35s delay entre emails (anti-spam Gmail: max 80/día)
        if p != prospects[-1]:
            print(f"  ⏳ Esperando 35s...")
            time.sleep(35)

    print()
    print(f"📊 Resumen: {sent} enviados · {failed} fallidos")

    # Guardar log
    if not dry_run and sent > 0:
        log_path = Path("/home/z/my-project/download/email_campaigns/tracking/sent_log_v2.json")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log = {
            "sent_at": datetime.utcnow().isoformat(),
            "from": SENDER_EMAIL,
            "reply_to": REPLY_TO,
            "total_sent": sent,
            "total_failed": failed,
            "prospects": results,
        }
        log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print(f"📝 Log guardado: {log_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
