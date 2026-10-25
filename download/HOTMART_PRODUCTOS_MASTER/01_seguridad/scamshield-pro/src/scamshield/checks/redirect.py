"""ScamShield Pro — Redirect chain analysis."""
from __future__ import annotations

from scamshield.checks.base import BaseCheck, CheckContext
from scamshield.utils.http_client import get_http_client
from scamshield.utils.url_parser import is_shortener


class RedirectChainCheck(BaseCheck):
    """Trace redirect chain — flag shorteners and excessive hops."""

    name = "redirect_chain"
    severity = "medium"
    weight = 18
    requires_network = True

    async def run(self, ctx: CheckContext) -> object:
        if not ctx.follow_redirects and not is_shortener(ctx.domain):
            return self._skip("follow_redirects disabled")

        # Already populated by an earlier HTTP fetch?
        if ctx.redirect_chain and ctx.final_url:
            chain = ctx.redirect_chain
            final = ctx.final_url
        else:
            chain = [ctx.url]
            try:
                async with get_http_client() as client:
                    # We disable auto-follow to capture the chain manually
                    async with client.stream(
                        "GET", ctx.url, follow_redirects=False
                    ) as r1:
                        current_url = ctx.url
                        next_loc = r1.headers.get("location")
                        # Re-enable follow to reach final URL
                    async with get_http_client(follow_redirects=True) as fc:
                        response = await fc.get(ctx.url)
                        ctx.http_status = response.status_code
                        ctx.http_headers = dict(response.headers)
                        final = str(response.url)
                        # Build the chain from response.history if present
                        for h in response.history:
                            chain.append(str(h.url))
                        if final not in chain:
                            chain.append(final)
            except Exception as e:
                return self._fail(
                    f"HTTP fetch failed: {type(e).__name__}",
                    error=str(e),
                )

        ctx.redirect_chain = chain
        ctx.final_url = chain[-1] if chain else ctx.url
        ctx.redirect_count = len(chain) - 1

        flags = []

        # 1. URL shortener
        if is_shortener(ctx.domain):
            flags.append("URL shortener in chain (obscures final destination)")

        # 2. Excessive redirects
        if ctx.redirect_count > 5:
            flags.append(f"Excessive redirects ({ctx.redirect_count} hops)")

        # 3. Cross-domain redirect (different registered domain)
        if len(chain) >= 2:
            from scamshield.utils.url_parser import parse_domain

            try:
                start_domain, _, _ = parse_domain(chain[0])
                end_domain, _, _ = parse_domain(chain[-1])
                if start_domain != end_domain:
                    flags.append(
                        f"Cross-domain redirect: {start_domain} → {end_domain}"
                    )
            except Exception:
                pass

        # 4. HTTPS to HTTP downgrade
        if chain[0].startswith("https://") and any(
            u.startswith("http://") for u in chain[1:]
        ):
            flags.append("HTTPS→HTTP downgrade in redirect chain")

        if flags:
            severity = "high" if ctx.redirect_count > 5 or any(
                "downgrade" in f for f in flags
            ) else "medium"
            self.severity = severity
            return self._fail(
                "Redirect chain issues: " + "; ".join(flags),
                chain=chain,
                hop_count=ctx.redirect_count,
                flags=flags,
            )

        return self._pass(
            f"Clean redirect chain ({ctx.redirect_count} hop(s))",
            chain=chain,
            hop_count=ctx.redirect_count,
        )
