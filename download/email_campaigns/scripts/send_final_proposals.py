#!/usr/bin/env python3
"""
send_final_proposals.py — Sends 14 personalized English proposals
from contacto@alicelabs.site via Hostinger SMTP (DKIM active)
with alicelabs.site as the ONLY website referenced (no marketnow)

14 emails with verified direct addresses, 35s delay, batches of 5
"""
import smtplib, ssl, sys, time, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SENDER = "contacto@alicelabs.site"
PASSWORD = "Emm@darla201500"
SITE = "alicelabs.site"

PROSPECTS = [
    # --- Batch 1: Oct 30 deadlines (3) ---
    {
        "to": "nominating@camws.org",
        "subject": "CAMWS Website RFP — AliceLabs LLC",
        "name": "CAMWS",
        "contact": "Professor Victoria Pagan",
        "need": "Full website redesign for a classical studies association with 1,100 members. Member portal with login, renewals, and directory. Conference registration with abstract submission and payment processing. Modern CMS for small nonprofit staff. WCAG 2.2 AA accessibility. Content migration with URL redirects. Visual design system. Staff training and documentation. Post-launch support.",
        "budget": "$30,000-$40,000",
        "deadline": "October 30, 2026 11:59 PM PT",
        "our_price": "$35,000",
        "why": "We have experience with nonprofit membership platforms, conference registration systems, PCI-compliant payment processing, and WCAG 2.2 AA accessibility. We build CMS implementations that non-technical staff can manage independently.",
        "requirements": "Executive summary, team bios, portfolio of comparable work (nonprofit/academic), technical approach, milestone-based timeline, migration plan, 3 client references, itemized cost proposal",
    },
    {
        "to": "communications@carfacalberta.com",
        "subject": "Proposal: Visual Identity & Brand Manual — AliceLabs LLC",
        "name": "CARFAC Alberta",
        "contact": "Communications Team",
        "need": "Visual identity system, brand manual, and graphic resources for an Alberta-based arts organization advocating for visual artists. Templates for digital and print use.",
        "budget": "To be confirmed upon RFP review",
        "deadline": "October 30, 2026",
        "our_price": "To be confirmed upon RFP review",
        "why": "We understand the arts sector and CARFAC's advocacy role for visual artists in Canada. We can deliver bilingual (English/French) brand systems if required.",
        "requirements": "Visual identity, brand guidelines, graphic resource templates, source files",
    },
    {
        "to": "mritchie@cityofgolden.gov",
        "subject": "Proposal: Graphic Design, Publications & Accessible Templates — AliceLabs LLC",
        "name": "City of Golden, Colorado",
        "contact": "M. Ritchie",
        "need": "Graphic design partner for recurring publications, brand guidance, staff-use templates, park map, and related graphics. Includes production management, accessible digital documents (WCAG 2.1 AA), and editable source files. Two annual water-quality reports beginning 2017. First design deadline December 15, 2026.",
        "budget": "$70,000 (not-to-exceed, 1 year)",
        "deadline": "November 3, 2026 5:00 PM MT",
        "our_price": "$65,000 (within $70,000 cap)",
        "why": "We specialize in accessible document design (WCAG 2.1 AA), reusable template systems that non-technical staff can manage, and recurring publication production. We understand municipal branding and publication workflows.",
        "requirements": "Portfolio, 3 references, team evidence, approach, fee schedule. Notarized Acceptance of Conditions Statement. Certificate of insurance after selection.",
    },
    # --- Batch 2: Nov 5-6 deadlines (4) ---
    {
        "to": "abennett@cityhpil.com",
        "subject": "Proposal: Municipal Brand Identity, Logo & Visual System — AliceLabs LLC",
        "name": "City of Highland Park, Illinois",
        "contact": "A. Bennett",
        "need": "New municipal brand identity including logo, sub-brands for departments, comprehensive design guides, and reusable templates for staff.",
        "budget": "To be confirmed upon RFP review",
        "deadline": "November 5, 2026",
        "our_price": "To be confirmed upon RFP review",
        "why": "We have experience with municipal branding that balances modernity with institutional credibility. Our civic identity systems include departmental sub-brands, staff-use templates, and comprehensive brand guidelines.",
        "requirements": "Brand identity, logo design, sub-brands, visual system, brand guidelines, templates",
    },
    {
        "to": "lex.gelb@lacity.org",
        "subject": "Proposal: Visual Identity, Logo & Event Graphics — AliceLabs LLC",
        "name": "LA Department of Cultural Affairs",
        "contact": "Lex Gelb",
        "need": "Comprehensive visual identity system including logo, template system (event flyers, programs, banners, social media, letterhead, business cards), event graphic materials for cultural events, multilingual support (English, Spanish, Korean, Chinese, Tagalog), WCAG 2.1 AA visual standards, digital asset library, 40+ page brand guidelines document, and staff training.",
        "budget": "Up to $75,000",
        "deadline": "November 5-6, 2026",
        "our_price": "$68,000",
        "why": "We have experience with cultural arts organization branding and multilingual design systems. We understand LA's diverse cultural landscape and the Department's role in serving all communities. All source files included (AI, PSD, PDF, SVG, PNG).",
        "requirements": "Visual identity, logo, templates, event graphics, multilingual, WCAG 2.1 AA, asset library, brand guidelines, staff training",
    },
    {
        "to": "jguiney@ippf.org",
        "subject": "Proposal: Software Development & OpenEMR Integration — AliceLabs LLC",
        "name": "IPPF",
        "contact": "J. Guiney",
        "need": "Software development and OpenEMR integration for an international health organization.",
        "budget": "To be confirmed upon RFP review",
        "deadline": "November 6, 2026",
        "our_price": "To be confirmed upon RFP review",
        "why": "We have experience with healthcare software integration, OpenEMR systems, and international NGO technical requirements.",
        "requirements": "Software development, OpenEMR integration",
    },
    {
        "to": "bettina@nafoa.org",
        "subject": "Proposal: Motif & Asset Designer for Branding Support — AliceLabs LLC",
        "name": "NAFOA",
        "contact": "Bettina Gonzalez, Director of Communications",
        "need": "Original visual motifs and branding assets reflecting Native American focus, finance, leadership, and economic themes. Motifs to differentiate work areas (general, policy/advocacy, education programs, Native Financial Advisor Program). Deliverables: patterns, icons, illustrations, backgrounds, overlays for print/digital, website/email/social templates. ADA accessibility compliance. File formats: AI, SVG, PNG with usage guidelines.",
        "budget": "Not specified",
        "deadline": "November 13, 2026 5:00 PM ET",
        "our_price": "To be proposed based on scope",
        "why": "We approach this with respect for Native American arts and cultures. Our design process includes cultural review checkpoints and collaborative feedback rounds. We deliver ADA-compliant assets in multiple formats with comprehensive usage guidelines.",
        "requirements": "Company profile, portfolio, project approach, pricing breakdown, references. Cultural knowledge. ADA accessibility. 6-8 week timeline. 3 rounds of revisions.",
    },
    # --- Batch 3: Nov 9-20 deadlines (5) ---
    {
        "to": "wmoore@hamptonga.gov",
        "subject": "Proposal: Logo, Visual Identity & Brand Manual — AliceLabs LLC",
        "name": "City of Hampton, Georgia",
        "contact": "W. Moore",
        "need": "Logo design, visual identity, and brand manual for a municipality in Georgia.",
        "budget": "To be confirmed upon RFP review",
        "deadline": "November 9, 2026",
        "our_price": "To be confirmed upon RFP review",
        "why": "We have experience with municipal government branding, civic identity systems, and brand guideline documentation designed for government staff use.",
        "requirements": "Logo, visual identity, brand manual",
    },
    {
        "to": "jacquialessi@achievementfirst.org",
        "subject": "Proposal: Website Ecosystem Redesign — 43 Sites — AliceLabs LLC",
        "name": "Achievement First",
        "contact": "Jacqui Alessi, Associate Chief of Marketing & Communications",
        "need": "Unified digital ecosystem: 1 network website + 3 regional hubs (CT, NY, RI) + 41 school microsites. WordPress Multisite or Drupal. WCAG 2.2 AA. Bilingual (EN/ES). Role-based permissions and editorial workflows. Content syndication. Third-party integrations (SchoolMint, HubSpot, Greenhouse). 5-year Total Cost of Ownership required.",
        "budget": "Not specified (large-scale project)",
        "deadline": "November 9, 2026",
        "our_price": "To be confirmed — requires detailed scoping",
        "why": "We have experience with WordPress Multisite, school district websites, bilingual EN/ES implementations, WCAG 2.2 AA, role-based editorial workflows, and content syndication across multiple sites. We understand charter school network requirements.",
        "requirements": "Fixed-fee by phase, itemized ongoing costs, 5-year TCO, portfolio of multi-site work, team bios, technical approach, migration plan, 3 references",
    },
    {
        "to": "kimberly@techequity.us",
        "subject": "Proposal: Website Redesign & Migration — AliceLabs LLC",
        "name": "TechEquity Collaborative",
        "contact": "Kimberly Davis-Wells",
        "need": "Redesign TechEquity Collaborative (c3) website to reflect new strategic plan. Discovery, IA, design, CMS development, content migration, QA, accessibility testing, staff training, post-launch support. Secondary: migrate TechEquity Action (c4) from splash page to manageable platform. WCAG 2.2 AA. SEO best practices.",
        "budget": "$80,000-$100,000 (both projects)",
        "deadline": "November 13, 2026",
        "our_price": "$85,000 (c3: $70,000 + c4: $15,000)",
        "why": "We have experience with nonprofit website redesigns, CMS implementations for non-technical staff, WCAG 2.2 AA compliance, and content migration with redirects. We understand tech policy organizations and can build on existing brand identity (launched July 2024).",
        "requirements": "Company overview, project team, proposed approach, timeline, detailed budget (separate c3/c4), portfolio, references, terms & conditions",
    },
    {
        "to": "dan.coldiron@cityofloveland.org",
        "subject": "Proposal: Website Migration & Consolidation — AliceLabs LLC",
        "name": "City of Loveland, Colorado",
        "contact": "Dan Coldiron",
        "need": "Website migration and consolidation of multiple department sites into a unified CMS. Content migration with 301 redirect mapping. WCAG 2.1 AA accessibility. Mobile-responsive. Staff training.",
        "budget": "To be confirmed upon RFP review",
        "deadline": "November 19, 2026",
        "our_price": "$32,000",
        "why": "We have experience with government website consolidation, 301 redirect mapping, citizen-centric information architecture, and unified CMS implementations for municipalities.",
        "requirements": "Multi-site consolidation, content migration, unified CMS, WCAG 2.1 AA, staff training",
    },
    {
        "to": "lgranados@wvwd.org",
        "subject": "Proposal: Website Redesign & Maintenance — AliceLabs LLC",
        "name": "West Valley Water District",
        "contact": "L. Granados",
        "need": "Website redesign, accessibility compliance, ongoing maintenance, and user-facing functionality (bill payment, usage dashboard, outage map) for a California water district.",
        "budget": "To be confirmed upon RFP review",
        "deadline": "November 20, 2026",
        "our_price": "$25,000",
        "why": "We have experience with utility district websites, online bill payment integration, water usage dashboards, outage communication systems, and public sector accessibility compliance.",
        "requirements": "Website redesign, accessibility, maintenance, user functions",
    },
    # --- Open deadline (2) ---
    {
        "to": "sales@c-dmunicipal.com",
        "subject": "Proposal: WordPress Redesign + Dynamic Directory — AliceLabs LLC",
        "name": "C&D Municipal Sales",
        "contact": "Sales Team",
        "need": "WordPress redesign with a dynamic manufacturer and team directory. Searchable, filterable, with individual profile pages. CMS that non-technical staff can manage.",
        "budget": "$5,000",
        "deadline": "Open",
        "our_price": "$4,500",
        "why": "We have experience with WordPress corporate sites, dynamic directory implementations with search and filter functionality, and CMS setups for non-technical staff.",
        "requirements": "WordPress redesign, dynamic directory, CMS",
    },
    {
        "to": "chairman@welovebvl.org",
        "subject": "Proposal: Graphic Design & Wayfinding Signage — AliceLabs LLC",
        "name": "Brooksville Main Street",
        "contact": "Chairman",
        "need": "Graphic design and visual wayfinding signage system for downtown Brooksville, FL revitalization. Historic preservation context.",
        "budget": "To be confirmed upon project review",
        "deadline": "To be confirmed",
        "our_price": "To be confirmed upon project review",
        "why": "We have experience with downtown revitalization visual systems, wayfinding signage design, and Main Street program branding guidelines.",
        "requirements": "Graphic design, wayfinding signage, downtown revitalization",
    },
]


def make_html(p):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p['subject']}</title></head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f4f4f7;color:#1a1a2e;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#0a1a3a 0%,#050a20 100%);padding:40px 20px;">
<tr><td align="center"><table width="600" cellpadding="0" cellspacing="0"><tr><td style="color:#ffffff;text-align:center;">
<h1 style="margin:0 0 8px;font-size:26px;font-weight:800;">{p['name']}</h1>
<p style="margin:0;color:#6080b0;font-size:16px;">Proposal from AliceLabs LLC</p>
<p style="margin:8px 0 0;color:#6080b0;font-size:14px;font-weight:600;">Deadline: {p['deadline']} · Budget: {p['budget']}</p>
</td></tr></table></td></tr></table>
<table width="100%" cellpadding="0" cellspacing="0" style="padding:32px 20px;">
<tr><td align="center"><table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<tr><td style="padding:32px 32px 0;">
<p style="font-size:16px;line-height:1.6;color:#444;">Dear {p['contact']},</p>
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
<p style="margin:0 0 12px;font-size:20px;font-weight:700;color:#0a1a3a;">{p['our_price']}</p>
<p style="margin:0;font-size:14px;color:#666;">Timeline and detailed scope to be confirmed upon full RFP review.</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:24px 32px 0;">
<h2 style="font-size:20px;font-weight:700;color:#0a1a3a;margin:0 0 16px;border-bottom:2px solid #0a1a3a;padding-bottom:8px;">Why AliceLabs</h2>
<p style="font-size:15px;line-height:1.6;color:#444;">{p['why']}</p>
<p style="font-size:15px;line-height:1.6;color:#444;margin-top:12px;">AliceLabs LLC is registered in Wyoming, USA. We provide W-9, Certificate of Insurance, E-Verify compliance, and client references upon request.</p>
</td></tr>
<tr><td style="padding:24px 32px 32px;">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:12px;background:#e8f0ff;border-radius:8px;">
<p style="margin:0;font-size:15px;color:#0a1a3a;">
<strong>1.</strong> Reply to schedule a 30-minute consultation call<br>
<strong>2.</strong> We deliver a formal proposal with W-9, references, and portfolio within 48 hours<br>
<strong>3.</strong> Contact: <a href="mailto:contacto@alicelabs.site" style="color:#0a1a3a;">contacto@alicelabs.site</a> · <a href="https://{SITE}" style="color:#0a1a3a;">{SITE}</a><br>
<strong>4.</strong> Deadline: {p['deadline']}
</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:24px 32px;background:#050a20;">
<p style="margin:0 0 8px;color:#ffffff;font-size:16px;font-weight:700;">AliceLabs LLC</p>
<p style="margin:0 0 4px;color:#6080b0;font-size:13px;">Wyoming, USA · Government Contractor · E-Verify Compliant</p>
<p style="margin:0 0 4px;color:#6080b0;font-size:13px;">📧 contacto@alicelabs.site · 🌐 alicelabs.site</p>
<p style="margin:8px 0 0;color:#444;font-size:12px;">Reply "unsubscribe" to stop receiving emails</p>
</td></tr>
</table></td></tr></table>
</body></html>"""


def send(to, subject, html):
    msg = MIMEMultipart("alternative")
    msg["From"] = f"AliceLabs LLC <{SENDER}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg["Reply-To"] = SENDER
    msg.attach(MIMEText(html, "html", "utf-8"))
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
    dry = "--dry-run" in sys.argv
    batch_size = 5
    delay = 35
    batch_pause = 60

    print(f"📤 AliceLabs Final Proposal Sender")
    print(f"   From: {SENDER} via Hostinger SMTP (DKIM active)")
    print(f"   Website: {SITE} (NO marketnow)")
    print(f"   Total: {len(PROSPECTS)} | Language: ALL English")
    print(f"   Dry run: {dry}")
    print()

    sent = 0; failed = 0; results = []

    for i, p in enumerate(PROSPECTS):
        html = make_html(p)

        if dry:
            print(f"  ⏭️  [{i+1}/{len(PROSPECTS)}] {p['name']} → {p['to']} | {p['deadline']}")
            sent += 1; results.append({"name":p["name"],"to":p["to"],"status":"dry_run"})
            continue

        print(f"  📤 [{i+1}/{len(PROSPECTS)}] {p['name']} → {p['to']}")
        if send(p["to"], p["subject"], html):
            print(f"  ✅ Sent!")
            sent += 1; results.append({"name":p["name"],"to":p["to"],"status":"sent"})
        else:
            failed += 1; results.append({"name":p["name"],"to":p["to"],"status":"failed"})

        if i < len(PROSPECTS) - 1:
            if (i + 1) % batch_size == 0:
                print(f"  ⏳ Batch pause {batch_pause}s..."); time.sleep(batch_pause)
            else:
                print(f"  ⏳ {delay}s..."); time.sleep(delay)

    print(f"\n📊 {sent} sent · {failed} failed · From: {SENDER}")

    if not dry and sent > 0:
        log = {"sent_at":datetime.now(timezone.utc).isoformat(),"from":SENDER,"total":sent,"failed":failed,"prospects":results}
        from pathlib import Path
        log_path = Path("/home/z/my-project/download/email_campaigns/tracking/final_sent_log.json")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print(f"📝 Log: {log_path}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
