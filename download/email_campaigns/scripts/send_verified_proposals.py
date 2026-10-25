#!/usr/bin/env python3
"""
send_verified_proposals.py — Sends personalized English proposals
from contacto@alicelabs.site via Hostinger SMTP
in batches of 5 with 35s delays
"""
import smtplib, ssl, sys, time, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime, timezone

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SENDER = "contacto@alicelabs.site"
PASSWORD = "Emm@darla201500"
HTML_DIR = Path("/home/z/my-project/download/email_campaigns/html_verified")
HTML_DIR.mkdir(parents=True, exist_ok=True)

PROSPECTS = [
    {"to": "nominating@camws.org", "name": "CAMWS",
     "subject": "CAMWS Website RFP — AliceLabs LLC",
     "need": "Website redesign for classical studies association (1,100 members). Member portal, conference registration with abstract submission and payment processing, CMS for small nonprofit staff, WCAG 2.2 AA, content migration with URL redirects, visual design system, staff training, post-launch support.",
     "budget": "$30,000-$40,000", "deadline": "October 30, 2026 11:59 PM PT",
     "contact_person": "Professor Victoria Pagan",
     "requirements": "Executive summary, team bios, portfolio of comparable work (nonprofit/academic), technical approach, milestone-based timeline, migration plan, 3 client references, itemized cost proposal",
     "our_proposal": "$35,000",
     "why_us": "Experience with nonprofit membership platforms, conference registration systems, PCI-compliant payment processing, and WCAG 2.2 AA accessibility. Small-team CMS implementation with non-technical staff in mind."},
    {"to": "communications@carfacalberta.com", "name": "CARFAC Alberta",
     "subject": "Proposal: Visual Identity & Brand Manual — AliceLabs LLC",
     "need": "Visual identity system, brand manual, and graphic resources for an Alberta-based arts organization advocating for visual artists.",
     "budget": "TBD", "deadline": "October 30, 2026",
     "contact_person": "Communications Team",
     "requirements": "Visual identity, brand guidelines, graphic resource templates",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with arts sector branding, understanding of CARFAC's advocacy role for visual artists in Canada, bilingual capability (English/French) if required."},
    {"to": "info@fas.org", "name": "Federation of American Scientists",
     "subject": "Proposal: Website Improvements & Technical Maintenance — AliceLabs LLC",
     "need": "Website improvements and ongoing technical maintenance for a science policy organization.",
     "budget": "TBD", "deadline": "October 30, 2026",
     "contact_person": "FAS Team",
     "requirements": "Website improvements, technical maintenance",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with science and policy organization websites, technical maintenance contracts, and content management systems for research organizations."},
    {"to": "procurement@ct.gov", "name": "Connecticut Agency (RFP SEO-0155)",
     "subject": "Proposal: Graphic Design & Digital Communications — AliceLabs LLC",
     "need": "Graphic design, digital communications, and social media for a Connecticut state agency.",
     "budget": "TBD", "deadline": "November 3, 2026",
     "contact_person": "Procurement Office",
     "requirements": "Graphic design, digital communications, social media management",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with government agency communications, social media design systems, and digital content creation for public sector clients."},
    {"to": "abennett@cityhpil.com", "name": "City of Highland Park, IL",
     "subject": "Proposal: Brand Identity, Logo & Visual System — AliceLabs LLC",
     "need": "New brand identity, logo, and visual system for a municipality in Illinois.",
     "budget": "TBD", "deadline": "November 5, 2026",
     "contact_person": "A. Bennett",
     "requirements": "Brand identity, logo design, visual system, brand guidelines",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with municipal branding, civic visual identity systems, and government brand guidelines that balance modernity with institutional credibility."},
    {"to": "lex.gelb@lacity.org", "name": "LA Department of Cultural Affairs",
     "subject": "Proposal: Visual Identity, Logo & Event Graphics — AliceLabs LLC",
     "need": "Visual identity system, logo design, templates, and event graphic materials for the LA Department of Cultural Affairs. Must serve a diverse, multilingual city.",
     "budget": "Up to $75,000", "deadline": "November 5, 2026",
     "contact_person": "Lex Gelb",
     "requirements": "Visual identity, logo, template system (flyers, programs, banners, social media, letterhead), event graphics, multilingual support (English, Spanish, Korean, Chinese, Tagalog), WCAG 2.1 AA, digital asset library, brand guidelines, staff training",
     "our_proposal": "$68,000",
     "why_us": "Experience with cultural arts organization branding, multilingual design systems, and government compliance. Understanding of LA's diverse cultural landscape."},
    {"to": "jguiney@ippf.org", "name": "IPPF",
     "subject": "Proposal: Software Development & OpenEMR Integration — AliceLabs LLC",
     "need": "Software development and OpenEMR integration for an international health organization.",
     "budget": "TBD", "deadline": "November 6, 2026",
     "contact_person": "J. Guiney",
     "requirements": "Software development, OpenEMR integration, international health systems",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with healthcare software integration, OpenEMR systems, and international NGO technical requirements."},
    {"to": "wmoore@hamptonga.gov", "name": "City of Hampton, GA",
     "subject": "Proposal: Logo, Visual Identity & Brand Manual — AliceLabs LLC",
     "need": "Logo design, visual identity, and brand manual for a municipality in Georgia.",
     "budget": "TBD", "deadline": "November 9, 2026",
     "contact_person": "W. Moore",
     "requirements": "Logo, visual identity, brand manual",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with municipal government branding, civic identity systems, and brand guideline documentation for government staff."},
    {"to": "jacquialessi@achievementfirst.org", "name": "Achievement First",
     "subject": "Proposal: Website Ecosystem Redesign — 43 Sites — AliceLabs LLC",
     "need": "Unified digital ecosystem: 1 network website + 3 regional hubs (CT, NY, RI) + 41 school microsites. WordPress or Drupal CMS, WCAG 2.2 AA, bilingual (EN/ES), role-based permissions, content syndication, third-party integrations (SchoolMint, HubSpot, Greenhouse). 5-year TCO required.",
     "budget": "Not specified (large project)", "deadline": "November 9, 2026",
     "contact_person": "Jacqui Alessi, Associate Chief of Marketing & Communications",
     "requirements": "Fixed-fee implementation by phase, itemized ongoing hosting/SLA/maintenance, 5-year TCO, portfolio of comparable multi-site work, team bios, technical approach, migration plan, 3 references",
     "our_proposal": "To be confirmed — large-scale project requiring detailed scoping",
     "why_us": "Experience with WordPress Multisite, school district websites, bilingual EN/ES implementations, WCAG 2.2 AA, role-based editorial workflows, and content syndication across multiple sites."},
    {"to": "procurement@wavetransit.com", "name": "Wave Transit",
     "subject": "Proposal: Website Redesign, Development, Hosting & Support — AliceLabs LLC",
     "need": "Website redesign, development, hosting, integration, training, maintenance, and support for a public transportation authority in Wilmington, NC.",
     "budget": "TBD", "deadline": "November 10, 2026 4:00 PM EST",
     "contact_person": "Procurement Office",
     "requirements": "Website redesign, development, hosting, integration, training, maintenance, support",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with transit authority websites, real-time route information integration, accessibility compliance, and public sector hosting/maintenance contracts."},
    {"to": "dan.coldiron@cityofloveland.org", "name": "City of Loveland, CO",
     "subject": "Proposal: Website Migration & Consolidation — AliceLabs LLC",
     "need": "Website migration and consolidation of multiple department sites into a unified CMS for a Colorado municipality.",
     "budget": "TBD", "deadline": "November 19, 2026",
     "contact_person": "Dan Coldiron",
     "requirements": "Multi-site consolidation, content migration with 301 redirects, unified CMS, WCAG 2.1 AA",
     "our_proposal": "$32,000",
     "why_us": "Experience with government website consolidation, 301 redirect mapping, citizen-centric information architecture, and unified CMS implementations for municipalities."},
    {"to": "lgranados@wvwd.org", "name": "West Valley Water District",
     "subject": "Proposal: Website Redesign & Maintenance — AliceLabs LLC",
     "need": "Website redesign, accessibility compliance, ongoing maintenance, and user-facing functionality for a California water district.",
     "budget": "TBD", "deadline": "November 20, 2026",
     "contact_person": "L. Granados",
     "requirements": "Website redesign, accessibility, maintenance, user functions (bill payment, usage dashboard, outage map)",
     "our_proposal": "$25,000",
     "why_us": "Experience with utility district websites, online bill payment integration, water usage dashboards, outage communication systems, and public sector accessibility compliance."},
    {"to": "sales@c-dmunicipal.com", "name": "C&D Municipal Sales",
     "subject": "Proposal: WordPress Redesign + Dynamic Directory — AliceLabs LLC",
     "need": "WordPress redesign with a dynamic manufacturer and team directory for a municipal sales company in Baltimore, MD.",
     "budget": "$5,000", "deadline": "Open",
     "contact_person": "Sales Team",
     "requirements": "WordPress redesign, dynamic directory of manufacturers and teams, CMS",
     "our_proposal": "$4,500",
     "why_us": "Experience with WordPress corporate sites, dynamic directory implementations with search and filter functionality, and CMS setups that non-technical staff can manage."},
    {"to": "chairman@welovebvl.org", "name": "Brooksville Main Street",
     "subject": "Proposal: Graphic Design & Wayfinding Signage System — AliceLabs LLC",
     "need": "Graphic design and visual wayfinding signage system for downtown Brooksville, FL revitalization.",
     "budget": "TBD", "deadline": "To be confirmed",
     "contact_person": "Chairman",
     "requirements": "Graphic design, wayfinding signage, downtown revitalization visual system",
     "our_proposal": "To be confirmed upon project review",
     "why_us": "Experience with downtown revitalization visual systems, wayfinding signage design, and Main Street program branding guidelines."},
    {"to": "info@moffateda.org", "name": "Moffat Economic Development Authority",
     "subject": "Proposal: Website, Landing Pages & Maintenance — AliceLabs LLC",
     "need": "Initial website, landing pages, and phased maintenance for an economic development authority.",
     "budget": "TBD", "deadline": "November 19, 2026",
     "contact_person": "Moffat EDA",
     "requirements": "Website, landing pages, hosting, maintenance (phased approach)",
     "our_proposal": "To be confirmed upon RFP review",
     "why_us": "Experience with economic development organization websites, business attraction landing pages, and phased website delivery for organizations with limited budgets."},
]


def generate_email_html(p):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Proposal for {p['name']} — AliceLabs LLC</title></head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f4f4f7;color:#1a1a2e;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#0a1a3a 0%,#050a20 100%);padding:40px 20px;">
<tr><td align="center"><table width="600" cellpadding="0" cellspacing="0"><tr><td style="color:#ffffff;text-align:center;">
<h1 style="margin:0 0 8px;font-size:26px;font-weight:800;">Proposal for {p['name']}</h1>
<p style="margin:0;color:#6080b0;font-size:16px;">AliceLabs LLC — Web Development & Design</p>
<p style="margin:8px 0 0;color:#6080b0;font-size:14px;font-weight:600;">Deadline: {p['deadline']} · Budget: {p['budget']}</p>
</td></tr></table></td></tr></table>
<table width="100%" cellpadding="0" cellspacing="0" style="padding:32px 20px;">
<tr><td align="center"><table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="padding:32px 32px 0;">
<p style="font-size:16px;line-height:1.6;color:#444;">Dear {p['contact_person']},</p>
<p style="font-size:16px;line-height:1.6;color:#444;">We are pleased to submit our proposal in response to your procurement notice. AliceLabs LLC is a Wyoming-registered web development and design company specializing in government, institutional, and commercial projects.</p>
</td></tr>
<tr><td style="padding:24px 32px 0;">
<h2 style="font-size:20px;font-weight:700;color:#0a1a3a;margin:0 0 16px;border-bottom:2px solid #0a1a3a;padding-bottom:8px;">Project Understanding</h2>
<p style="font-size:15px;line-height:1.6;color:#444;">{p['need']}</p>
</td></tr>
<tr><td style="padding:24px 32px 0;">
<h2 style="font-size:20px;font-weight:700;color:#0a1a3a;margin:0 0 16px;border-bottom:2px solid #0a1a3a;padding-bottom:8px;">Requirements We Can Meet</h2>
<p style="font-size:15px;line-height:1.6;color:#444;">{p['requirements']}</p>
</td></tr>
<tr><td style="padding:24px 32px 0;">
<h2 style="font-size:20px;font-weight:700;color:#0a1a3a;margin:0 0 16px;border-bottom:2px solid #0a1a3a;padding-bottom:8px;">Our Proposal</h2>
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4fa;border-radius:8px;"><tr><td style="padding:20px;">
<p style="margin:0 0 12px;font-size:20px;font-weight:700;color:#0a1a3a;">{p['our_proposal']}</p>
<p style="margin:0;font-size:14px;color:#666;">Timeline and detailed scope to be confirmed upon full RFP review.</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:24px 32px 0;">
<h2 style="font-size:20px;font-weight:700;color:#0a1a3a;margin:0 0 16px;border-bottom:2px solid #0a1a3a;padding-bottom:8px;">Why AliceLabs</h2>
<p style="font-size:15px;line-height:1.6;color:#444;">{p['why_us']}</p>
<p style="font-size:15px;line-height:1.6;color:#444;margin-top:12px;">AliceLabs LLC is registered in Wyoming, USA. We provide W-9, Certificate of Insurance, E-Verify compliance, and client references upon request.</p>
</td></tr>
<tr><td style="padding:24px 32px 32px;">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:12px;background:#e8f0ff;border-radius:8px;">
<p style="margin:0;font-size:15px;color:#0a1a3a;">
<strong>1.</strong> Reply to schedule a 30-minute consultation call<br>
<strong>2.</strong> We deliver a formal proposal with W-9, references, and portfolio within 48 hours<br>
<strong>3.</strong> Contact: <a href="mailto:contacto@alicelabs.site" style="color:#0a1a3a;">contacto@alicelabs.site</a> · marketnow.site<br>
<strong>4.</strong> Deadline: {p['deadline']}
</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:24px 32px;background:#050a20;">
<p style="margin:0 0 8px;color:#ffffff;font-size:16px;font-weight:700;">AliceLabs LLC</p>
<p style="margin:0 0 4px;color:#6080b0;font-size:13px;">Wyoming, USA · Government Contractor · E-Verify Compliant</p>
<p style="margin:0 0 4px;color:#6080b0;font-size:13px;">📧 contacto@alicelabs.site · 🌐 marketnow.site</p>
<p style="margin:8px 0 0;color:#444;font-size:12px;">Reply "unsubscribe" to stop receiving emails</p>
</td></tr>
</table></td></tr></table>
</body></html>"""


def send_email(to, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["From"] = f"AliceLabs LLC <{SENDER}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg["Reply-To"] = SENDER
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=30) as s:
            s.login(SENDER, PASSWORD)
            s.sendmail(SENDER, [to], msg.as_string())
        return True
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {e}")
        return False


def main():
    batch = 5
    delay = 35
    batch_pause = 60
    dry = "--dry-run" in sys.argv
    start = int(sys.argv[sys.argv.index("--from")+1]) if "--from" in sys.argv else 0
    cnt = int(sys.argv[sys.argv.index("--count")+1]) if "--count" in sys.argv else len(PROSPECTS)-start
    prospects = PROSPECTS[start:start+cnt]

    print(f"📤 AliceLabs Verified Proposal Sender")
    print(f"   From: {SENDER} via Hostinger SMTP")
    print(f"   Total: {len(prospects)} | Batch: {batch} | Delay: {delay}s | Dry: {dry}")
    print()

    sent = 0; failed = 0; results = []

    for i, p in enumerate(prospects):
        html = generate_email_html(p)
        # Save HTML
        fname = f"{i+1+start:02d}_{p['name'].lower().replace(' ','_').replace('/','_')}.html"
        (HTML_DIR / fname).write_text(html, encoding="utf-8")

        if dry:
            print(f"  ⏭️  [DRY] {p['name']} → {p['to']} | {p['deadline']}")
            sent += 1; results.append({"name":p["name"],"to":p["to"],"status":"dry_run"})
            continue

        print(f"  📤 [{i+1}/{len(prospects)}] {p['name']} → {p['to']}")
        if send_email(p["to"], p["subject"], html):
            print(f"  ✅ Sent!"); sent += 1
            results.append({"name":p["name"],"to":p["to"],"status":"sent"})
        else:
            failed += 1
            results.append({"name":p["name"],"to":p["to"],"status":"failed"})

        if i < len(prospects)-1:
            if (i+1) % batch == 0:
                print(f"  ⏳ Batch pause {batch_pause}s..."); time.sleep(batch_pause)
            else:
                print(f"  ⏳ {delay}s..."); time.sleep(delay)

    print(f"\n📊 {sent} sent · {failed} failed · From: {SENDER}")
    if not dry and sent > 0:
        log = Path("/home/z/my-project/download/email_campaigns/tracking/verified_sent_log.json")
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(json.dumps({"sent_at":datetime.now(timezone.utc).isoformat(),"from":SENDER,"total":sent,"failed":failed,"prospects":results}, indent=2), encoding="utf-8")
        print(f"📝 Log: {log}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
