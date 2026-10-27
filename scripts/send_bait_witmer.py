#!/usr/bin/env python3
"""
send_bait_witmer.py — Sends the bait+deterrent email to witmer960@gmail.com.

- Threads on witmer's original Message-ID
- HTML + plain alternative body
- IMAP APPEND to INBOX.Sent (Hostinger doesn't auto-copy)
- Bearer-style X-Mailer header so we can fingerprint our own send later
"""
import smtplib, ssl, imaplib, email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from pathlib import Path
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
IMAP_HOST = "imap.hostinger.com"
IMAP_PORT = 993
SENDER = "contacto@alicelabs.site"
PASSWORD = "Emm@darla201500"
DISPLAY_FROM = "Edison Flores <edison@alicelabs.site>"
TO = "witmer960@gmail.com"

# witmer's original message — threading anchor
ORIGINAL_MSGID = "<CAL38h7TdQaRP1bWszcyppKNdCrumwfBn4+8vvE=11cmeN3Ak+A@mail.gmail.com>"
SUBJECT = "Re: Collaboration — moving forward / conditions"

BODY_TEXT = """Hi K,

I read your reply and I'm willing to keep talking. But before we go any further, I owe you full transparency about how I operate — because if your proposal is legitimate, none of this should bother you. If it isn't, then this email is the only warning you'll get.

== How my inbound pipeline works ==

Every email that lands in my box is auto-processed by an ingestion agent that captures and fingerprints:

  - Full RFC 5322 headers, including the originating IP from every Received: hop (not just the last one)
  - SPF, DKIM, and DMARC alignment results
  - Client fingerprint (MTA banner, HELO, X-Mailer, message-ID pattern)
  - Calendly/booking links: account name, timezone, vanity URL history, redirect chain (every 301/302 hop is followed and timestamped)
  - Any linked domains: WHOIS age, registrar, nameserver history, SSL certificate chain, hosting ASN
  - Pattern cross-reference against public abuse feeds (Spamhaus DBL, SURBL, PhishTank, AbuseIPDB, GREYNOISE)

When patterns match known commercial-scam signatures — Calendly account registered under a name that doesn't match the sender domain, redirect chains through intermediary domains, free-form "futurelove"-style vanity URLs, UTC-only timezone with no real geolocation, or scripted replies that dodge verification questions — the pipeline auto-assembles an evidence bundle (headers + IPs + redirect trace + WHOIS + cert chain + timeline) and queues it for disclosure to:

  - Google abuse ( abuse@gmail.com ) — for Gmail sender accounts
  - The hosting provider of every intermediary domain in the chain
  - IC3 / FBI Internet Crime Complaint Center (if dollar figures mentioned exceed USD 5,000, the wire-fraud threshold kicks in)
  - Spamhaus + SURBL + Barracuda Central for IP/domain blacklisting

I can publish the full chain to public abuse databases with a single command. That burns the IP, the Gmail account, every linked Calendly URL, and any downstream account sharing the same fingerprint — across the spam ecosystem permanently, not just on my side.

I'm not accusing you. I'm telling you how I work. If your proposal is real, this is just standard due diligence. If it isn't, the bundle is already assembled and timestamped; I just haven't hit send on it yet.

== The bait ==

Alright — assuming you're real, let's talk business. Send me four things, and if they check out we move forward within 24h:

  1. Business registration number and jurisdiction
     (US LLC = state + EIN; UK = Companies House number;
      EU = VAT ID + registry; anywhere else = equivalent)
  2. A direct phone number — not VoIP, not Google Voice, not Skype.
     I will call it. My translator will be on the line.
  3. The payment platform you use to pay collaborators
     (Stripe / PayPal / bank wire / Wise / crypto).
     If crypto-only, we're done here.
  4. Two verifiable client references I can email today.

If those four arrive and verify, we sign a simple scope-of-work agreement and start. If they don't arrive, or if the answers are vague, or if I get another Calendly link instead of direct answers, I assume the worst and the bundle goes out — not as a threat, just as standard hygiene.

== What I will not do ==

  - I will not click a Calendly link a second time without the above.
  - I will not send any upfront fee, deposit, or "onboarding" payment.
  - I will not install any software, plugin, or "client tool" you send.
  - I will not share any login, API key, or GitHub collaborator seat
    before a signed SOW and verified payment.

If any of those are dealbreakers for you, that itself is an answer.

Ball's in your court. Reply with the four items, in plain text, in this thread. No new links, no new platforms, no "book a call first."

— Edison
AliceLabs LLC
edison@alicelabs.site
github.com/alicelabs-llc
"""


def build_message():
    msg = MIMEMultipart("mixed")
    msg["From"] = DISPLAY_FROM
    msg["To"] = TO
    msg["Subject"] = SUBJECT
    msg["Date"] = formatdate(localtime=True)
    msg["Reply-To"] = "edison@alicelabs.site"
    new_msgid = make_msgid(domain="alicelabs.site")
    msg["Message-ID"] = new_msgid
    msg["In-Reply-To"] = ORIGINAL_MSGID
    msg["References"] = ORIGINAL_MSGID
    msg["X-Mailer"] = "AliceLabs-Outbound/1.0 (bait+deterrent)"

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(BODY_TEXT, "plain", "utf-8"))
    html_body = (
        '<!DOCTYPE html><html><body '
        'style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;'
        'line-height:1.6;color:#1a1a2e;font-size:14px;max-width:680px;'
        'margin:0 auto;padding:16px;">'
        + BODY_TEXT.replace("\n", "<br>")
        + "</body></html>"
    )
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt)
    return msg, new_msgid


def imap_append_sent(msg_obj, new_msgid):
    """Append a copy of the sent message into INBOX.Sent via IMAP."""
    print("  → IMAP appending to INBOX.Sent...")
    ctx = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    try:
        imap.login(SENDER, PASSWORD)
        # Try the common Hostinger Sent folder names
        for folder in ("INBOX.Sent", "Sent", "INBOX.Sent Items"):
            typ, _ = imap.select(folder, readonly=True)
            if typ == "OK":
                target = folder
                break
        else:
            target = "INBOX.Sent"
        # Build the raw message bytes
        raw = msg_obj.as_bytes()
        # IMAP APPEND: flags \Seen + internaldate as proper datetime
        now_dt = datetime.now(timezone.utc)
        typ, data = imap.append(target, r"(\Seen)", now_dt, raw)
        if typ == "OK":
            print(f"  ✅ Appended to {target}")
        else:
            print(f"  ⚠️ APPEND returned {typ}: {data}")
        imap.logout()
    except Exception as e:
        print(f"  ⚠️ IMAP APPEND failed: {e}")


def main():
    print("=" * 72)
    print("📤 Sending BAIT + DETERRENT to witmer960@gmail.com")
    print("=" * 72)
    print(f"  From    : {DISPLAY_FROM}")
    print(f"  To      : {TO}")
    print(f"  Subject : {SUBJECT}")
    print(f"  Thread  : {ORIGINAL_MSGID}")
    print(f"  Body    : {len(BODY_TEXT)} chars, plain+html")
    print("-" * 72)

    msg, new_msgid = build_message()
    print(f"  New Message-ID: {new_msgid}")

    # ---- SMTP send ----
    print("  → SMTP send via Hostinger:465...")
    ctx = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=60) as s:
            s.login(SENDER, PASSWORD)
            s.sendmail(SENDER, [TO], msg.as_string())
        print("  ✅ SMTP send OK")
    except Exception as e:
        print(f"  ❌ SMTP FAILED: {e}")
        return 1

    # ---- IMAP append copy to Sent ----
    imap_append_sent(msg, new_msgid)

    print("-" * 72)
    print("✅ Done. witmer960 should see the reply in his inbox shortly.")
    print(f"   Thread anchor preserved: {ORIGINAL_MSGID}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
