#!/usr/bin/env python3
"""
Generates AliceLabs LLC capabilities presentation as a professional PDF.
Output: /home/z/my-project/download/presentation/AliceLabs_Capabilities.pdf
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from datetime import date

OUT = "/home/z/my-project/download/presentation/AliceLabs_Capabilities.pdf"
DARK = HexColor("#0a1a3a")
DARKER = HexColor("#050a20")
ACCENT = HexColor("#0e3a8a")
LIGHT = HexColor("#f0f4fa")
GREY = HexColor("#666666")
BODY = HexColor("#1a1a2e")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="HeroTitle", fontName="Helvetica-Bold",
                          fontSize=28, textColor=white, alignment=TA_LEFT,
                          leading=34, spaceAfter=8))
styles.add(ParagraphStyle(name="HeroSub", fontName="Helvetica",
                          fontSize=14, textColor=HexColor("#a8c5ff"),
                          alignment=TA_LEFT, leading=18))
styles.add(ParagraphStyle(name="HeroMeta", fontName="Helvetica-Bold",
                          fontSize=10, textColor=HexColor("#6080b0"),
                          alignment=TA_LEFT, leading=14, spaceBefore=10))
styles.add(ParagraphStyle(name="H2", fontName="Helvetica-Bold",
                          fontSize=18, textColor=DARK, leading=22,
                          spaceBefore=18, spaceAfter=8))
styles.add(ParagraphStyle(name="H3", fontName="Helvetica-Bold",
                          fontSize=13, textColor=ACCENT, leading=17,
                          spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle(name="Body", fontName="Helvetica",
                          fontSize=10.5, textColor=BODY, leading=15,
                          alignment=TA_JUSTIFY, spaceAfter=8))
styles.add(ParagraphStyle(name="BulletItem", fontName="Helvetica",
                          fontSize=10.5, textColor=BODY, leading=14,
                          alignment=TA_LEFT, spaceAfter=4, leftIndent=12))
styles.add(ParagraphStyle(name="Small", fontName="Helvetica",
                          fontSize=9, textColor=GREY, leading=12))
styles.add(ParagraphStyle(name="QuoteBig", fontName="Helvetica-Bold",
                          fontSize=16, textColor=ACCENT, leading=22,
                          alignment=TA_LEFT, spaceBefore=10, spaceAfter=10))
styles.add(ParagraphStyle(name="Footer", fontName="Helvetica",
                          fontSize=8, textColor=GREY, alignment=TA_CENTER))


def page_template(canvas_obj, doc):
    """Header strip and footer on every page after cover."""
    canvas_obj.saveState()
    page_num = canvas_obj.getPageNumber()
    if page_num > 1:
        # Top header strip
        canvas_obj.setFillColor(DARK)
        canvas_obj.rect(0, letter[1] - 0.45 * inch, letter[0], 0.45 * inch, fill=1, stroke=0)
        canvas_obj.setFillColor(white)
        canvas_obj.setFont("Helvetica-Bold", 10)
        canvas_obj.drawString(0.6 * inch, letter[1] - 0.3 * inch, "AliceLabs LLC")
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(HexColor("#a8c5ff"))
        canvas_obj.drawRightString(letter[0] - 0.6 * inch, letter[1] - 0.3 * inch,
                                    "Capabilities & Discovery Packet")
        # Bottom footer
        canvas_obj.setFillColor(GREY)
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawCentredString(letter[0] / 2, 0.35 * inch,
                                     f"AliceLabs LLC · Wyoming, USA · alicelabs.site · Page {page_num}")
    canvas_obj.restoreState()


def cover_page(canvas_obj, doc):
    """Full-bleed dark cover page."""
    canvas_obj.saveState()
    # Dark gradient-like background (solid dark navy)
    canvas_obj.setFillColor(DARKER)
    canvas_obj.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    # Accent band
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, letter[1] - 0.18 * inch, letter[0], 0.18 * inch, fill=1, stroke=0)
    # Logo block (top left)
    canvas_obj.setFillColor(white)
    canvas_obj.setFont("Helvetica-Bold", 18)
    canvas_obj.drawString(0.8 * inch, letter[1] - 1.5 * inch, "AliceLabs LLC")
    canvas_obj.setFont("Helvetica", 11)
    canvas_obj.setFillColor(HexColor("#a8c5ff"))
    canvas_obj.drawString(0.8 * inch, letter[1] - 1.8 * inch, "Web Development & Design")
    canvas_obj.drawString(0.8 * inch, letter[1] - 2.0 * inch, "Wyoming, USA")
    # Headline (vertical center)
    canvas_obj.setFillColor(white)
    canvas_obj.setFont("Helvetica-Bold", 32)
    canvas_obj.drawString(0.8 * inch, letter[1] / 2 + 0.8 * inch, "Capabilities &")
    canvas_obj.drawString(0.8 * inch, letter[1] / 2 + 0.3 * inch, "Discovery Packet")
    canvas_obj.setFillColor(HexColor("#a8c5ff"))
    canvas_obj.setFont("Helvetica", 13)
    canvas_obj.drawString(0.8 * inch, letter[1] / 2 - 0.1 * inch,
                          "Who we are, what we build, and the questions we ask")
    canvas_obj.drawString(0.8 * inch, letter[1] / 2 - 0.3 * inch,
                          "before sending you a fixed-price proposal.")
    # Bottom band
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, 0.6 * inch, letter[0], 0.04 * inch, fill=1, stroke=0)
    canvas_obj.setFillColor(white)
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawString(0.8 * inch, 0.4 * inch,
                          f"contacto@alicelabs.site   ·   alicelabs.site   ·   {date.today().strftime('%B %Y')}")
    canvas_obj.restoreState()


# ---------------------- Document content ----------------------
doc = SimpleDocTemplate(
    OUT, pagesize=letter,
    leftMargin=0.7 * inch, rightMargin=0.7 * inch,
    topMargin=0.8 * inch, bottomMargin=0.7 * inch,
    title="AliceLabs LLC — Capabilities & Discovery Packet",
    author="AliceLabs LLC",
)

story = []

# Cover (page 1) — handled by cover_page; we still need to push a PageBreak
# so the next content starts on page 2.
story.append(PageBreak())

# Section 1: Who we are
story.append(Paragraph("1. Who we are", styles["H2"]))
story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=10))
story.append(Paragraph(
    "AliceLabs LLC is a Wyoming-registered web development and design company "
    "specializing in government, institutional, and commercial projects. We build "
    "websites, web applications, content management systems, visual identity systems, "
    "and accessibility-compliant digital products for clients across the United States, "
    "Canada, Latin America, and Europe.",
    styles["Body"]))
story.append(Paragraph(
    "We are a small, senior-only team. That means no hand-offs to junior developers, "
    "no offshore staffing, and no sub-contractors. The person who writes the proposal "
    "is the same person who writes the code and answers your calls. Every engagement "
    "is led end-to-end by a senior engineer with at least ten years of professional "
    "experience in their discipline.",
    styles["Body"]))
story.append(Paragraph(
    "AliceLabs LLC is registered in the State of Wyoming. We provide a W-9, Certificate "
    "of Insurance, E-Verify compliance, and three client references on request. We sign "
    "fixed-fee contracts by milestone, never hourly, and we honour the milestones we "
    "quote or we refund the unused portion. We work in English and Spanish, with formal "
    "experience delivering bilingual EN/ES sites for US and Latin American clients.",
    styles["Body"]))

# Section 2: What we build
story.append(Paragraph("2. What we build", styles["H2"]))
story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=10))

story.append(Paragraph("2.1  Websites and web applications", styles["H3"]))
story.append(ListFlowable([
    ListItem(Paragraph("Custom WordPress and Drupal sites, multisite networks, "
                        "and headless CMS implementations (Strapi, Sanity, Contentful).",
                        styles["BulletItem"])),
    ListItem(Paragraph("Next.js / React single-page applications and server-rendered "
                        "sites with TypeScript, Prisma, PostgreSQL, and Tailwind CSS.",
                        styles["BulletItem"])),
    ListItem(Paragraph("Laravel/PHP backends with REST and GraphQL APIs, including "
                        "OAuth2 and Microsoft Entra ID single sign-on integrations.",
                        styles["BulletItem"])),
    ListItem(Paragraph("Content migration from legacy CMS, including 301 redirect "
                        "mapping, URL canonicalization, and SEO preservation.",
                        styles["BulletItem"])),
], bulletType="bullet", start="square"))

story.append(Paragraph("2.2  Visual identity and design systems", styles["H3"]))
story.append(ListFlowable([
    ListItem(Paragraph("Logo systems, sub-brand identities, and complete brand "
                        "guidelines (40+ pages, multilingual).", styles["BulletItem"])),
    ListItem(Paragraph("Template systems for in-house non-technical staff: flyers, "
                        "programs, banners, social cards, letterhead, business cards.",
                        styles["BulletItem"])),
    ListItem(Paragraph("Wayfinding signage systems for downtown districts, transit "
                        "hubs, and municipal facilities, including ADA-compliant variants.",
                        styles["BulletItem"])),
    ListItem(Paragraph("Accessible digital document design: WCAG 2.1/2.2 AA PDF, "
                        "HTML, and EPUB output from a single source.", styles["BulletItem"])),
], bulletType="bullet", start="square"))

story.append(Paragraph("2.3  Specialist integrations", styles["H3"]))
story.append(ListFlowable([
    ListItem(Paragraph("Payment processing: Stripe, PayPal, PCI-compliant flows, "
                        "recurring billing, and donation systems for nonprofit clients.",
                        styles["BulletItem"])),
    ListItem(Paragraph("GIS and spatial data: PostgreSQL/PostGIS, GDAL, GeoServer, "
                        "OpenLayers, and OGC WMS/WFS integration for environmental "
                        "and municipal monitoring platforms.", styles["BulletItem"])),
    ListItem(Paragraph("AI and automation: chatbots, document extraction, workflow "
                        "automation, MCP integrations, and trust-card verification systems.",
                        styles["BulletItem"])),
    ListItem(Paragraph("Identity and access: Microsoft Entra ID (formerly Azure AD) "
                        "SSO, OAuth2, SAML, RBAC, and audit-trail implementations.",
                        styles["BulletItem"])),
], bulletType="bullet", start="square"))

# Section 3: How we work
story.append(Paragraph("3. How we work", styles["H2"]))
story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=10))

story.append(Paragraph("3.1  Engagement model", styles["H3"]))
story.append(Paragraph(
    "Every engagement starts with a free 30-minute discovery call. From there we issue "
    "a fixed-fee proposal within 48 hours, broken down by milestone. We do not bid hourly "
    "and we do not invoice for time we did not spend on your deliverables. Each milestone "
    "has a defined acceptance criterion, a defined deliverable, and a defined payment. "
    "You see exactly what you are paying for before you pay for it.",
    styles["Body"]))

story.append(Paragraph("3.2  Project management and communication", styles["H3"]))
story.append(Paragraph(
    "We use a shared Trello or Notion board for every project, updated at the end of each "
    "working day. You receive a written status update every Friday, and we hold a 30-minute "
    "sprint review every two weeks over Zoom. We respond to email and Slack within one "
    "business day. There is no project manager buffer between you and the engineer doing "
    "the work — you talk directly to the person writing your code.",
    styles["Body"]))

story.append(Paragraph("3.3  Accessibility and compliance", styles["H3"]))
story.append(Paragraph(
    "We deliver every public-facing site to WCAG 2.1 AA or WCAG 2.2 AA, verified with "
    "automated tools (axe-core, Lighthouse, WAVE) and a manual screen-reader pass using "
    "NVDA and VoiceOver. We document our accessibility testing in the acceptance report. "
    "For US federal clients, we can document Section 508 conformance. For Canadian "
    "clients, we can document AODA and ACA conformance.",
    styles["Body"]))

story.append(Paragraph("3.4  Hosting, support, and warranty", styles["H3"]))
story.append(Paragraph(
    "We do not own hosting. We deploy to your infrastructure of choice (AWS, Google Cloud, "
    "Azure, Vultr, Hostinger, Netlify, Vercel) and hand over all credentials and access "
    "logs at acceptance. We offer optional monthly maintenance contracts starting at "
    "$500/month for security patches, dependency updates, and bug fixes. Every contract "
    "includes a 90-day post-launch warranty during which we fix any defect attributed to "
    "our own code at no additional cost.",
    styles["Body"]))

# Section 4: Project discovery questions (the ask)
story.append(PageBreak())
story.append(Paragraph("4. Project discovery — questions for you", styles["H2"]))
story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=10))

story.append(Paragraph(
    "To send you a fixed-fee proposal that we can actually honour, we need to understand "
    "the project before we quote it. The questions below are the same ones we ask every "
    "client at the start of an engagement. Answer what you can in writing, and we will "
    "follow up by email or in a 30-minute call on anything that needs more context.",
    styles["Body"]))

story.append(Paragraph("4.1  Business context", styles["H3"]))
discovery_business = [
    "What is the one-sentence goal of this project? (e.g. \"reduce support calls by 30%\", "
    "\"launch a new paid product line\", \"modernize our brand for a 2027 rebrand\")",
    "Who is the primary user of what we will build, and what is the single most important "
    "task they need to complete on their first visit?",
    "What does success look like six months after launch? Be specific: numbers, behaviours, "
    "or milestones — not adjectives.",
    "Who are your top three competitors or peer organizations, and what specifically do you "
    "want to do better than each one?",
]
for q in discovery_business:
    story.append(Paragraph(f"• {q}", styles["BulletItem"]))

story.append(Paragraph("4.2  Scope and deliverables", styles["H3"]))
discovery_scope = [
    "What pages, sections, or features must be present at launch? A sitemap, even rough, "
    "is enough to start.",
    "Are there third-party systems we must integrate with (CRM, ERP, payment, identity, "
    "GIS, marketing automation, learning management)? Please list each one with the vendor "
    "name and whether you have API access already.",
    "Do you have an existing brand book, logo, color palette, typography, or content style "
    "guide we must follow? If yes, please share.",
    "Do you have existing content (copy, photography, video) that we are responsible for "
    "migrating, or will we be responsible for creating it? Content production is a separate "
    "scope from design and development.",
    "What languages must the site support at launch, and which languages might be added "
    "within the first 12 months?",
]
for q in discovery_scope:
    story.append(Paragraph(f"• {q}", styles["BulletItem"]))

story.append(Paragraph("4.3  Technical and compliance", styles["H3"]))
discovery_tech = [
    "Do you have an existing hosting provider, or should we propose one? If existing, "
    "please share the platform (AWS, Azure, GCP, Vercel, Netlify, Vultr, etc.) and the "
    "instance size you currently run.",
    "What CMS (if any) does your team use today, and how comfortable is your staff with "
    " editing content without developer support?",
    "Are there regulatory compliance requirements we must document? (WCAG 2.1/2.2 AA, "
    "Section 508, AODA, HIPAA, PCI-DSS, GDPR, CCPA, FERPA, ADA, etc.)",
    "Do you require single sign-on (Microsoft Entra ID, Okta, Google Workspace) or any "
    "role-based access control matrix?",
    "Are there data residency requirements (data must physically reside in a specific "
    "country or region)?",
]
for q in discovery_tech:
    story.append(Paragraph(f"• {q}", styles["BulletItem"]))

story.append(Paragraph("4.4  Timeline, budget, and procurement", styles["H3"]))
discovery_commercial = [
    "When do you need this live in production? Please give us the actual date, not a wish. "
    "We will tell you honestly whether it is achievable.",
    "What is your budget range? We will tell you honestly what we can deliver inside that "
    "range, and what we cannot. We never pad a quote to fit a budget.",
    "Is this a fixed-fee contract or a time-and-materials engagement? We strongly prefer "
    "fixed-fee because it puts the delivery risk on us, not on you.",
    "Are you a government, institutional, or commercial buyer? Procurement rules differ "
    "between the three, and they affect how we structure the contract.",
    "Do you have a standard contract template you want us to use, or should we send ours? "
    "We have a Wyoming-governing master services agreement we can share.",
]
for q in discovery_commercial:
    story.append(Paragraph(f"• {q}", styles["BulletItem"]))

story.append(Paragraph("4.5  Next step", styles["H3"]))
story.append(Paragraph(
    "Reply with as much as you can in writing. We will issue a fixed-fee proposal within "
    "48 hours of receiving your answers. If you prefer a 30-minute call instead, send us "
    "two or three times that work for you and we will confirm one by return email. There "
    "is no cost for either step.",
    styles["Body"]))

# Section 5: Selected case studies
story.append(PageBreak())
story.append(Paragraph("5. Selected case studies", styles["H2"]))
story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=10))

story.append(Paragraph(
    "Below is a representative selection of past and current work. Detailed portfolio, "
    "client references, and live URLs are shared on request under NDA where applicable.",
    styles["Body"]))

cases = [
    ("WebGIS & spatial data platforms",
     "Design and development of integrated spatial-data repositories with PostGIS, "
     "GDAL, OpenLayers, and S3-compatible storage, including OGC WMS/WFS consumption, "
     "metadata catalogues (ISO 19115), RBAC, SSO Microsoft Entra ID, and public map "
     "dashboards. Bilingual (EN/ES) implementations and audit-trail logging."),
    ("Compliance screening SaaS",
     "Stripe-powered compliance screening application for AML, sanctions, and PEP checks, "
     "with batch upload, certified PDF reports, API documentation, and a Stripe checkout "
     "flow. React + TypeScript + Tailwind frontend, Node.js serverless backend."),
    ("Municipal website consolidations",
     "Migration and consolidation of multiple departmental sites into a unified WordPress "
     "Multisite or Drupal installation, including 301 redirect mapping, content audit, "
     "WCAG 2.1 AA conformance, and staff training for non-technical content editors."),
    ("x402 payment protocol & trust cards",
     "Universal Trust Adapter (ATC/1.0): Ed25519-signed trust cards, RFC 8785 JCS "
     "canonicalization, ten verification controls, and a live x402 endpoint selling "
     "per-call trust verification in USDC on Base. Open-source at "
     "github.com/alicelabs-llc/universal-trust-adapter."),
    ("Bilingual education ecosystem",
     "WordPress Multisite network of 43 sites (1 network site + 3 regional hubs + 41 "
     "school microsites) with role-based editorial workflows, content syndication, "
     "and integrations to SchoolMint, HubSpot, and Greenhouse. WCAG 2.2 AA, EN/ES."),
]
for title, body in cases:
    story.append(Paragraph(f"<b>{title}</b>", styles["H3"]))
    story.append(Paragraph(body, styles["Body"]))

# Section 6: Company snapshot
story.append(PageBreak())
story.append(Paragraph("6. Company snapshot", styles["H2"]))
story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=10))

snapshot_data = [
    ["Legal name", "AliceLabs LLC"],
    ["Entity type", "Limited Liability Company (LLC)"],
    ["State of registration", "Wyoming, USA"],
    ["Year founded", "2024"],
    ["Principal contact", "Edison Flores Guerra, Founder"],
    ["Email", "contacto@alicelabs.site"],
    ["Website", "alicelabs.site"],
    ["Languages", "English, Spanish"],
    ["Compliance", "W-9, E-Verify, COI on request"],
    ["Contract type", "Fixed-fee by milestone (preferred)"],
    ["References", "Three on request, with contact email + phone"],
]
t = Table(snapshot_data, colWidths=[1.8 * inch, 4.5 * inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), LIGHT),
    ("TEXTCOLOR", (0, 0), (0, -1), DARK),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (1, 0), (1, -1), [white, HexColor("#fafbff")]),
    ("LINEBELOW", (0, 0), (-1, -1), 0.3, HexColor("#d0d4dc")),
]))
story.append(t)
story.append(Spacer(1, 0.3 * inch))

story.append(Paragraph(
    "This document is provided for procurement evaluation purposes. It is not a "
    "contract, proposal, or offer to perform services. Any fixed-fee proposal we issue "
    "is delivered separately in writing and is valid for 30 days from the date of issue.",
    styles["Small"]))

# Build with custom first page (cover) and subsequent page template
doc.build(story, onFirstPage=cover_page, onLaterPages=page_template)
print(f"✅ PDF generated: {OUT}")

import os
print(f"   Size: {os.path.getsize(OUT)} bytes")
