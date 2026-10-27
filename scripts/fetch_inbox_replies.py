#!/usr/bin/env python3
"""
fetch_inbox_replies.py — IMAP scan of INBOX + INBOX.Replied for any
replies to the AliceLabs campaign sends.

For each message that looks like a reply (In-Reply-To set, OR Subject
starts with "Re:"), print: From / Subject / Date / In-Reply-To / first
300 chars of body.

Also dumps a JSON summary to download/email_campaigns/tracking/replies.json
"""
import imaplib, ssl, json, email
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from pathlib import Path

IMAP_HOST = "imap.hostinger.com"
IMAP_PORT = 993
USER = "contacto@alicelabs.site"
PASSWORD = "Emm@darla201500"

OUT_JSON = Path("/home/z/my-project/download/email_campaigns/tracking/replies.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)


def decode(s):
    if not s:
        return ""
    try:
        return str(make_header(decode_header(s)))
    except Exception:
        return str(s)


def get_text(msg):
    """Extract plain text body, fallback to html stripped."""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                try:
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", "replace"
                    )[:2000]
                except Exception:
                    continue
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                try:
                    raw = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", "replace"
                    )
                    # crude strip
                    import re
                    return re.sub(r"<[^>]+>", " ", raw)[:2000]
                except Exception:
                    continue
        return ""
    try:
        return msg.get_payload(decode=True).decode(
            msg.get_content_charset() or "utf-8", "replace"
        )[:2000]
    except Exception:
        return ""


def main():
    ctx = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    imap.login(USER, PASSWORD)

    print("Mailbox list:")
    typ, data = imap.list()
    for d in data:
        print("  ", d.decode() if isinstance(d, bytes) else d)

    found = []
    for folder in ("INBOX", "INBOX.Sent", "INBOX.Replied", "INBOX.Drafts"):
        print(f"\n--- Scanning {folder} ---")
        typ, data = imap.select(folder, readonly=True)
        if typ != "OK":
            print(f"  (cannot select: {data})")
            continue
        n = int(data[0])
        print(f"  {n} messages")
        if n == 0:
            continue
        # Fetch ALL messages, headers + first chunk of body
        typ, msgs = imap.search(None, "ALL")
        if typ != "OK":
            continue
        ids = msgs[0].split()
        # Cap at last 60 to keep it fast
        ids = ids[-60:]
        for mid in ids:
            typ, msg_data = imap.fetch(mid, "(RFC822)")
            if typ != "OK":
                continue
            for part in msg_data:
                if isinstance(part, tuple):
                    raw = part[1]
                    msg = email.message_from_bytes(raw)
                    frm = decode(msg.get("From"))
                    subj = decode(msg.get("Subject"))
                    dt = msg.get("Date", "")
                    in_reply_to = msg.get("In-Reply-To", "")
                    refs = msg.get("References", "")
                    mid_hdr = msg.get("Message-ID", "")
                    body = get_text(msg)

                    is_reply = bool(in_reply_to) or subj.lower().startswith("re:")
                    is_us = "alicelabs" in frm.lower() or "contacto@" in frm.lower() or "edison@" in frm.lower()

                    # only show interesting ones — replies we received, or our sent
                    if is_reply or is_us:
                        print(f"\n  [{folder} #{mid.decode()}] {dt}")
                        print(f"    From         : {frm}")
                        print(f"    Subject      : {subj}")
                        print(f"    In-Reply-To  : {in_reply_to}")
                        print(f"    Message-ID   : {mid_hdr}")
                        if body:
                            preview = body.replace("\n", " ")[:280]
                            print(f"    Body preview  : {preview}")
                        found.append({
                            "folder": folder,
                            "from": frm,
                            "subject": subj,
                            "date": dt,
                            "in_reply_to": in_reply_to,
                            "message_id": mid_hdr,
                            "references": refs,
                            "body_preview": body[:600],
                            "is_reply": is_reply,
                            "is_us": is_us,
                        })

    imap.logout()

    OUT_JSON.write_text(json.dumps(found, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n\nWrote {len(found)} interesting messages to {OUT_JSON}")


if __name__ == "__main__":
    main()
