#!/usr/bin/env python3
"""fetch_full_body.py — pull full bodies of specific Message-IDs from INBOX."""
import imaplib, ssl, email, json
from email.header import decode_header, make_header

IMAP_HOST = "imap.hostinger.com"
IMAP_PORT = 993
USER = "contacto@alicelabs.site"
PASSWORD = "Emm@darla201500"

TARGETS = [
    # Dan Coldiron / City of Loveland reply
    "From Dan Coldiron re Loveland",
    # Luz Granados / WVWD reply
    "From Luz Granados re WVWD",
    # WWF procurement reply (already handled, but pull for record)
    "From WWF Procurement",
]


def decode(s):
    if not s: return ""
    try: return str(make_header(decode_header(s)))
    except: return str(s)


def get_full_text(msg):
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct in ("text/plain", "text/html"):
                try:
                    raw = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", "replace"
                    )
                    if ct == "text/html":
                        import re
                        raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.DOTALL)
                        raw = re.sub(r"<[^>]+>", " ", raw)
                        raw = re.sub(r"\s+", " ", raw)
                    parts.append(raw.strip())
                except: continue
    else:
        try:
            parts.append(msg.get_payload(decode=True).decode(
                msg.get_content_charset() or "utf-8", "replace"
            ))
        except: pass
    return "\n---\n".join(p for p in parts if p)[:6000]


ctx = ssl.create_default_context()
imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
imap.login(USER, PASSWORD)
imap.select("INBOX", readonly=True)

typ, msgs = imap.search(None, "ALL")
ids = msgs[0].split()[-60:]

want_senders = ("cityofloveland", "wvwd.org", "wwf.id")
for mid in ids:
    typ, msg_data = imap.fetch(mid, "(RFC822)")
    if typ != "OK": continue
    for part in msg_data:
        if isinstance(part, tuple):
            msg = email.message_from_bytes(part[1])
            frm = decode(msg.get("From")).lower()
            if any(s in frm for s in want_senders):
                print("=" * 78)
                print(f"From: {decode(msg.get('From'))}")
                print(f"Subj: {decode(msg.get('Subject'))}")
                print(f"Date: {msg.get('Date')}")
                print(f"MsgID: {msg.get('Message-ID')}")
                print(f"In-Reply-To: {msg.get('In-Reply-To')}")
                print("-" * 78)
                print(get_full_text(msg))
                print("=" * 78 + "\n")

imap.logout()
