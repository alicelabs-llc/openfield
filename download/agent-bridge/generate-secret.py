#!/usr/bin/env python3
"""
generate-secret.py — Generates a 32-byte random secret encoded as base64url.
Prints the secret to stdout. Save it to SHARED_SECRET.txt and put the same
value in config.json under "secret".
"""
import base64
import secrets
import sys

if __name__ == "__main__":
    secret = secrets.token_bytes(32)
    encoded = base64.urlsafe_b64encode(secret).decode().rstrip("=")
    print(encoded)
    if len(sys.argv) > 1:
        Path = sys.argv[1]
        with open(Path, "w") as f:
            f.write(encoded + "\n")
        print(f"Also wrote to {Path}", file=sys.stderr)
