"""Quickstart — scan a URL in 5 lines of code.

Run with:
    python examples/quickstart.py
"""
import asyncio

from scamshield.core.models import ScanRequest
from scamshield.scanner import Scanner


async def main():
    scanner = Scanner()
    result = await scanner.scan(ScanRequest(url="https://github.com"))

    print(result.summary())
    print(f"  IP: {result.ip_address}")
    print(f"  Country: {result.server_country}")
    print(f"  SSL valid: {result.ssl_valid}")
    print(f"  Duration: {result.duration_ms} ms")
    print()
    for c in result.checks:
        icon = "✓" if c.passed else "✗"
        print(f"  {icon} [{c.severity:>8}] {c.name}: {c.message}")


if __name__ == "__main__":
    asyncio.run(main())
