#!/usr/bin/env python3
"""Re-append only — rebuild the message and IMAP-APPEND into INBOX.Sent.
   Used because the SMTP send already succeeded in send_bait_witmer.py."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location(
    "sbw", "/home/z/my-project/scripts/send_bait_witmer.py"
)
sbw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbw)

msg, new_msgid = sbw.build_message()
print(f"Rebuilt message: {new_msgid}")
sbw.imap_append_sent(msg, new_msgid)
