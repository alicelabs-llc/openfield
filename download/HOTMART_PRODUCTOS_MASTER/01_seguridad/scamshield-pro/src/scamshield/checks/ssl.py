"""ScamShield Pro — SSL/TLS certificate check."""
from __future__ import annotations

import socket
import ssl
from datetime import datetime

from scamshield.checks.base import BaseCheck, CheckContext


class SSLCheck(BaseCheck):
    """Verify SSL certificate validity and age."""

    name = "ssl_certificate"
    severity = "high"
    weight = 20
    requires_network = True

    async def run(self, ctx: CheckContext) -> object:
        if ctx.url.startswith("http://"):
            return self._fail(
                "Site served over plain HTTP — no SSL/TLS encryption",
                scheme="http",
            )

        host = ctx.domain
        port = 443

        ctx.ssl_valid = False
        try:
            ctx_copy = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=ctx.timeout) as sock:
                with ctx_copy.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    ctx.ssl_cert = cert
        except ssl.SSLCertVerificationError as e:
            return self._fail(
                f"SSL verification failed: {e.verify_message}",
                error_type=type(e).__name__,
            )
        except (socket.timeout, ConnectionError, OSError) as e:
            return self._fail(
                f"Cannot establish SSL connection: {type(e).__name__}",
                error=str(e),
            )

        if not cert:
            return self._fail("No SSL certificate returned", host=host)

        # Parse notAfter
        try:
            not_after_str = cert.get("notAfter", "")
            expiry = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
            days_until_expiry = (expiry - datetime.utcnow()).days

            if days_until_expiry < 0:
                return self._fail(
                    "SSL certificate EXPIRED",
                    expired_on=expiry.isoformat(),
                    days_since_expiry=-days_until_expiry,
                )
            if days_until_expiry < 7:
                return self._fail(
                    f"SSL certificate expires in {days_until_expiry} days",
                    expires_on=expiry.isoformat(),
                )
        except (ValueError, TypeError):
            pass

        # Check issuer — free CAs are fine but DV-only certs get slight scrutiny
        issuer = dict(x[0] for x in cert.get("issuer", []))
        issuer_name = issuer.get("organizationName", "Unknown")

        ctx.ssl_valid = True
        return self._pass(
            f"Valid SSL certificate issued by {issuer_name}",
            issuer=issuer_name,
            subject=dict(x[0] for x in cert.get("subject", [])),
            expires_on=not_after_str if not_after_str else None,
            version=cert.get("version"),
        )
