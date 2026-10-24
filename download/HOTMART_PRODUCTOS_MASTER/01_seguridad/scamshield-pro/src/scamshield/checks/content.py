"""ScamShield Pro — HTML content analysis."""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from scamshield.checks.base import BaseCheck, CheckContext


class ContentCheck(BaseCheck):
    """Inspect on-page signals — forms, hidden elements, password fields."""

    name = "content_analysis"
    severity = "medium"
    weight = 12
    requires_content = True

    async def run(self, ctx: CheckContext) -> object:
        if not ctx.fetch_content:
            return self._skip("content fetch disabled")

        if not ctx.html_content:
            # Lazy-fetch if not yet present
            try:
                from scamshield.utils.http_client import get_http_client

                async with get_http_client() as client:
                    response = await client.get(ctx.final_url or ctx.url)
                    ctx.http_status = response.status_code
                    ctx.html_content = response.text[:200_000]  # cap
            except Exception as e:
                return self._fail(
                    f"Could not fetch HTML content: {type(e).__name__}",
                    error=str(e),
                )

        html = ctx.html_content or ""
        if not html:
            return self._fail("Empty response body")

        soup = BeautifulSoup(html, "lxml")
        flags: list[str] = []

        # 1. Password / credit card fields without HTTPS
        password_fields = soup.find_all("input", {"type": "password"})
        if password_fields and not (ctx.final_url or ctx.url).startswith("https://"):
            flags.append(
                f"Password field on HTTP page ({len(password_fields)} fields) — credentials exposed"
            )
        elif password_fields:
            # Check if action points to a different domain
            for form in soup.find_all("form"):
                action = form.get("action", "")
                if action.startswith("http://"):
                    flags.append("Form submits to HTTP endpoint")
                    break

        # 2. Hidden iframes
        hidden_iframes = [
            i for i in soup.find_all("iframe")
            if any(
                "hidden" in (i.get("style", "") + i.get("class", "")) or
                (i.get("width") == "0" and i.get("height") == "0")
                for _ in [None]
            )
        ]
        if hidden_iframes:
            flags.append(f"{len(hidden_iframes)} hidden iframe(s)")

        # 3. External script injection
        scripts = soup.find_all("script", src=True)
        external_scripts = []
        same_domain_count = 0
        for s in scripts:
            src = s.get("src", "")
            if src.startswith("http") and ctx.domain not in src:
                external_scripts.append(src)
            else:
                same_domain_count += 1
        if len(external_scripts) > 15 and same_domain_count < 3:
            flags.append(f"Excessive external scripts ({len(external_scripts)})")

        # 4. Excessive keywords spam
        text = soup.get_text(" ", strip=True).lower()
        spammy_keywords = ["free", "win", "winner", "congratulations", "limited time", "act now"]
        spam_count = sum(text.count(k) for k in spammy_keywords)
        if spam_count > 10:
            flags.append(f"Spammy keyword density ({spam_count} hits)")

        # 5. Title vs domain mismatch
        title = (soup.title.string or "").strip() if soup.title else ""
        if title and ctx.domain and len(title) > 5:
            # Check if domain appears in title (loose)
            domain_root = ctx.domain.split(".")[0]
            if domain_root.lower() not in title.lower() and len(title.split()) < 8:
                flags.append(f"Title/domain mismatch: '{title[:60]}'")

        # 6. Mismatched meta description language across page
        meta_lang = soup.find("html", attrs={"lang": True})
        if meta_lang:
            page_lang = meta_lang.get("lang", "").lower()
            # Heuristic: TLD suggests one country but page lang is another
            tld_country_hints = {".com.ec": "es", ".com.mx": "es", ".com.br": "pt", ".com.ar": "es"}
            expected = tld_country_hints.get(ctx.tld.lower())
            if expected and page_lang and expected not in page_lang:
                flags.append(f"Language mismatch: TLD expects {expected}, page is {page_lang}")

        if flags:
            severity = "high" if any("password" in f.lower() for f in flags) else "medium"
            self.severity = severity
            return self._fail(
                "Content issues: " + "; ".join(flags),
                flags=flags,
                title=title,
                has_password_field=bool(password_fields),
            )

        return self._pass(
            "Content analysis passed",
            title=title,
            script_count=len(scripts),
            external_scripts=len(external_scripts),
        )
