#!/usr/bin/env python3
"""
agent-bridge-client.py — Signs and sends commands to the agent-bridge
running on the user's PC via Cloudflare Tunnel.

Usage:
  python agent-bridge-client.py --url https://xyz.trycloudflare.com \\
      --secret-file /path/to/SHARED_SECRET.txt \\
      --command "git status"

  python agent-bridge-client.py --url ... --secret ... --command "ls"

Exit codes:
  0 — command executed successfully (exit_code 0)
  1 — command executed but exit_code != 0
  2 — request rejected (auth, rate limit, blocklist, etc.)
  3 — network/connection error
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path


def sign_payload(secret: bytes, timestamp: str, nonce: str,
                 body: bytes) -> str:
    """Compute HMAC-SHA256(secret, timestamp + '.' + nonce + '.' + body)."""
    payload = timestamp.encode("utf-8") + b"." + nonce.encode("utf-8") + b"." + body
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def normalize_secret(raw: str) -> bytes:
    """Accept base64url with or without padding, or plain hex."""
    raw = raw.strip()
    # Try base64url
    padded = raw + "=" * (-len(raw) % 4)
    try:
        return base64.urlsafe_b64decode(padded.encode())
    except Exception:
        pass
    # Try hex
    try:
        return bytes.fromhex(raw)
    except Exception:
        raise ValueError(f"Cannot decode secret (neither base64url nor hex): {raw[:20]}...")


def call_bridge(url: str, secret: bytes, command: str,
                timeout: int = 60) -> tuple[int, dict]:
    """Send a signed command to the bridge. Returns (http_status, response)."""
    nonce = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    body = json.dumps({"command": command}, ensure_ascii=False).encode("utf-8")
    signature = sign_payload(secret, timestamp, nonce, body)

    req = urllib.request.Request(
        url.rstrip("/") + "/run",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Bridge-Timestamp": timestamp,
            "X-Bridge-Nonce": nonce,
            "X-Bridge-Signature": signature,
            "User-Agent": "agent-bridge-client/1.0.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            data = json.loads(resp.read().decode("utf-8"))
            return status, data
    except urllib.error.HTTPError as e:
        try:
            data = json.loads(e.read().decode("utf-8"))
        except Exception:
            data = {"error": f"HTTP {e.code}", "body": e.read().decode("utf-8", errors="replace")[:500]}
        return e.code, data
    except (urllib.error.URLError, ConnectionError, OSError) as e:
        return 0, {"error": f"Connection error: {type(e).__name__}: {e}"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Signs and sends commands to agent-bridge"
    )
    parser.add_argument("--url", required=True,
                        help="Tunnel URL, e.g. https://xyz.trycloudflare.com")
    parser.add_argument("--secret", help="Shared secret (base64url)")
    parser.add_argument("--secret-file", type=Path,
                        help="Path to file containing the secret")
    parser.add_argument("--command", required=True,
                        help="Command to execute on the remote PC")
    parser.add_argument("--timeout", type=int, default=60,
                        help="HTTP request timeout in seconds (default 60)")
    args = parser.parse_args()

    if args.secret_file:
        secret = normalize_secret(args.secret_file.read_text())
    elif args.secret:
        secret = normalize_secret(args.secret)
    else:
        print("❌ Provide --secret or --secret-file", file=sys.stderr)
        return 2

    status, data = call_bridge(args.url, secret, args.command, args.timeout)

    if status == 0:
        print(f"❌ Network error: {data.get('error')}", file=sys.stderr)
        return 3

    print(f"HTTP {status}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if status == 200 and data.get("exit_code") == 0:
        return 0
    elif status == 200:
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
