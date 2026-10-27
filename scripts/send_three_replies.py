#!/usr/bin/env python3
"""
send_three_replies.py — Sends three emails via Hostinger SMTP:

1. Reply to Ryan Gillespie <sec@optitransfer.ch> (x402 conformance — YES)
   Threaded: In-Reply-To + References point to original msg-id.

2. Reply to WWF-Indonesia <procurement.WWF@wwf.id> (consortium question)
   Threaded: In-Reply-To + References point to original msg-id.

3. New outbound email to witmer960@gmail.com (Airtasker client):
   - Capabilities presentation PDF attached
   - Asks for project specs
"""
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
from pathlib import Path

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SENDER = "contacto@alicelabs.site"
PASSWORD = "Emm@darla201500"

DRAFTS_DIR = Path("/home/z/my-project/download/email_campaigns/drafts")
PRESENTATION_PDF = Path("/home/z/my-project/download/presentation/AliceLabs_Capabilities.pdf")


def parse_draft(path: Path):
    """Parse a draft file with From:/To:/Subject: headers + blank line + body."""
    text = path.read_text(encoding="utf-8")
    # Split headers from body on first blank line
    parts = text.split("\n\n", 1)
    if len(parts) != 2:
        raise ValueError(f"Draft {path} missing header/body separator")
    header_block, body = parts
    headers = {}
    for line in header_block.split("\n"):
        if ":" in line:
            k, _, v = line.partition(":")
            headers[k.strip().lower()] = v.strip()
    return headers, body


def send_one(to_addr, subject, body_text, in_reply_to=None, attachment=None,
             attachment_name=None):
    """Send an email via Hostinger SMTP. Supports threading + one attachment."""
    msg = MIMEMultipart("mixed")
    msg["From"] = f"AliceLabs LLC <{SENDER}>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Reply-To"] = SENDER
    new_msgid = make_msgid(domain="alicelabs.site")
    msg["Message-ID"] = new_msgid

    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        # References is a space-separated list of msg-ids; include the original
        msg["References"] = in_reply_to

    # Body — text/plain version (HTML wrapper would be nice but not strictly needed)
    # Wrap as multipart/alternative so Outlook doesn't strip the body
    alt = MIMEMultipart("alternative")
    # Plain text version
    alt.attach(MIMEText(body_text, "plain", "utf-8"))
    # Simple HTML version (so spam filters see both)
    html_body = (
        "<!DOCTYPE html><html><body style=\"font-family:-apple-system,Segoe UI,Roboto,sans-serif;"
        "line-height:1.55;color:#1a1a2e;font-size:14px;\">"
        + body_text.replace("\n", "<br>")
        + "</body></html>"
    )
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt)

    if attachment:
        part = MIMEApplication(attachment, Name=attachment_name)
        part["Content-Disposition"] = f'attachment; filename="{attachment_name}"'
        msg.attach(part)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=60) as s:
        s.login(SENDER, PASSWORD)
        s.sendmail(SENDER, [to_addr], msg.as_string())
    return new_msgid


def main():
    print("=" * 72)
    print("📤 AliceLabs — sending 3 emails via Hostinger SMTP")
    print("=" * 72)

    # ---- 1. Ryan Gillespie reply ------------------------------------------------
    print("\n[1/3] Reply to Ryan Gillespie <sec@optitransfer.ch>...")
    headers, body = parse_draft(DRAFTS_DIR / "reply_ryan_gillespie.txt")
    ryan_msgid = "<179288285056.3250222.4244974722028637885@optitransfer.ch>"
    mid = send_one(
        to_addr=headers["to"],
        subject=headers["subject"],
        body_text=body,
        in_reply_to=ryan_msgid,
    )
    print(f"    ✅ Sent. New Message-ID: {mid}")

    # ---- 2. WWF-Indonesia reply -------------------------------------------------
    print("\n[2/3] Reply to WWF-Indonesia <procurement.WWF@wwf.id>...")
    headers, body = parse_draft(DRAFTS_DIR / "reply_wwf_indonesia.txt")
    wwf_msgid = "<TY0PR03MB6726BB3D0A0F40EA2DB52E2A89612@TY0PR03MB6726.apcprd03.prod.outlook.com>"
    mid = send_one(
        to_addr=headers["to"],
        subject=headers["subject"],
        body_text=body,
        in_reply_to=wwf_msgid,
    )
    print(f"    ✅ Sent. New Message-ID: {mid}")

    # ---- 3. witmer960@gmail.com — capabilities packet + project discovery ------
    print("\n[3/3] Outbound to witmer960@gmail.com (capabilities + discovery)...")
    witmer_body = """Hi,

Thanks for reaching out via Airtasker — happy to send over our capabilities packet.

AliceLabs LLC is a Wyoming-registered web development and design company. We build websites, web applications, content management systems, and visual identity systems for government, institutional, and commercial clients across the US, Canada, and Latin America.

A few things to know about us up front, so you can decide if we're the right fit:

- We are a senior-only team. The person who writes your proposal is the same person who writes your code. No hand-offs, no offshore staffing, no sub-contractors.
- We work fixed-fee by milestone. No hourly billing. You see what you're paying for before you pay for it.
- We deliver WCAG 2.1/2.2 AA on every public-facing site we build, and we document our accessibility testing in the acceptance report.
- We are E-Verify compliant, can provide a W-9 and Certificate of Insurance, and have three client references available on request.
- We work in English and Spanish. Spanish-language and bilingual EN/ES implementations are part of our normal practice.

I have attached our Capabilities & Discovery Packet as a PDF. It covers who we are, what we build, how we work, five selected case studies, and a company snapshot.

The packet also includes Section 4 — a list of project discovery questions. Those are the same questions we ask every client before quoting a fixed fee. If you can answer as many as you can in writing, I will send you a fixed-fee proposal within 48 hours.

If you'd rather have a 30-minute call instead of writing, send me two or three times that work for you and I'll confirm one by reply. Either path is free.

Quick context so I don't waste your time on the wrong quote:

1. What is the one-sentence goal of the project? (e.g. "launch a paid course platform", "migrate a 12-year-old Drupal site to a modern CMS", "build a customer portal that integrates with our CRM")
2. Is there a fixed deadline driving this, or is the timeline flexible?
3. Do you have a budget range already? I'll tell you honestly what we can deliver inside that range and what we can't.
4. Is this for yourself, your business, or a client of yours?

Looking forward to your reply.

Best,
Edison Flores Guerra
AliceLabs LLC
Wyoming, USA
contacto@alicelabs.site · alicelabs.site
"""
    witmer_subject = "AliceLabs LLC — Capabilities Packet + Project Discovery Questions"
    pdf_bytes = PRESENTATION_PDF.read_bytes()
    mid = send_one(
        to_addr="witmer960@gmail.com",
        subject=witmer_subject,
        body_text=witmer_body,
        attachment=pdf_bytes,
        attachment_name="AliceLabs_Capabilities.pdf",
    )
    print(f"    ✅ Sent. New Message-ID: {mid}")
    print(f"    📎 Attachment: AliceLabs_Capabilities.pdf ({len(pdf_bytes)} bytes)")

    print("\n" + "=" * 72)
    print("📊 All three emails sent. Copies will appear in Sent folder shortly.")
    print("=" * 72)


if __name__ == "__main__":
    main()
