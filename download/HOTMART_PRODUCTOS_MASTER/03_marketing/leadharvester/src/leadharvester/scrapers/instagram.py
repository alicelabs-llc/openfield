"""LeadHarvester — Instagram scraper using Playwright.

Note: Instagram aggressively blocks scraping. This module uses a real
logged-in session (saved via Playwright state) and respects delays
to avoid rate-limiting. For bulk scraping, use rotating proxies + multiple
sessions.
"""
from __future__ import annotations
import asyncio
import json
import random
from pathlib import Path
from typing import AsyncIterator
from urllib.parse import quote

from leadharvester.core.config import get_settings
from leadharvester.core.models import Lead, LeadSource, ScrapeRequest
from leadharvester.core.extractors import (
    extract_email, extract_phone, extract_website, is_business_bio, extract_category
)


class InstagramScraper:
    """Scraper for Instagram public profiles via Playwright."""

    BASE_URL = "https://www.instagram.com"

    def __init__(self):
        self.settings = get_settings()
        self._browser = None
        self._context = None
        self._page = None

    async def _ensure_session(self):
        """Initialize Playwright with saved session."""
        if self._page is not None:
            return self._page

        from playwright.async_api import async_playwright

        self._pw = await async_playwright().start()
        launch_args = {"headless": True}
        if self.settings.proxy_url:
            launch_args["proxy"] = {"server": self.settings.proxy_url}

        self._browser = await self._pw.chromium.launch(**launch_args)
        session_path = Path(self.settings.ig_session_file).expanduser()
        session_path.parent.mkdir(parents=True, exist_ok=True)

        if session_path.exists():
            self._context = await self._browser.new_context(
                storage_state=str(session_path),
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )
        else:
            self._context = await self._browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )

        self._page = await self._context.new_page()
        return self._page

    async def login(self, username: str, password: str) -> bool:
        """Login to Instagram and save session."""
        page = await self._ensure_session()
        await page.goto(f"{self.BASE_URL}/accounts/login/", wait_until="networkidle")
        await page.fill('input[name="username"]', username)
        await page.fill('input[name="password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000)
        if "login" in page.url:
            return False
        # Save session
        session_path = Path(self.settings.ig_session_file).expanduser()
        await self._context.storage_state(path=str(session_path))
        return True

    async def scrape_profile(self, username: str, extract_contact: bool = True) -> Lead:
        """Scrape a single Instagram profile (public data only)."""
        page = await self._ensure_session()
        url = f"{self.BASE_URL}/{username}/"
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(random.uniform(
            self.settings.delay_min_seconds * 1000,
            self.settings.delay_max_seconds * 1000,
        ))

        # Extract data from page
        # Try meta tags first (most stable)
        full_name = await page.evaluate("""() => {
            const el = document.querySelector('meta[property="og:title"]');
            return el ? el.getAttribute('content') : '';
        }""")

        bio = await page.evaluate("""() => {
            const el = document.querySelector('meta[property="og:description"]');
            return el ? el.getAttribute('content') : '';
        }""")

        avatar_url = await page.evaluate("""() => {
            const el = document.querySelector('meta[property="og:image"]');
            return el ? el.getAttribute('content') : '';
        }""")

        # Parse followers/following/posts from bio string
        followers = 0
        following = 0
        posts_count = 0
        if bio:
            import re
            # Pattern: "123 Followers, 45 Following, 67 Posts"
            m = re.search(r"([\d,]+)\s+Followers?,\s+([\d,]+)\s+Following?,\s+([\d,]+)\s+Posts?", bio, re.IGNORECASE)
            if m:
                followers = int(m.group(1).replace(",", ""))
                following = int(m.group(2).replace(",", ""))
                posts_count = int(m.group(3).replace(",", ""))

        # Verified status
        verified = await page.evaluate("""() => {
            return !!document.querySelector('svg[aria-label="Verified"]');
        }""")

        # Try to find contact info in bio + any visible text
        full_text = f"{bio} {full_name}"
        # Also try extracting from any link buttons (Link-in-bio)
        try:
            links = await page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href]')).map(a => a.href).filter(h => !h.includes('instagram.com'));
            }""")
            if links:
                full_text += " " + " ".join(links)
        except Exception:
            pass

        email = extract_email(full_text) if extract_contact else ""
        phone = extract_phone(full_text) if extract_contact else ""
        website = extract_website(full_text)

        is_biz = is_business_bio(bio)
        category = extract_category(bio) if is_biz else ""

        return Lead(
            username=username,
            full_name=full_name.replace(" (@{})".format(username), "").strip(),
            bio=bio[:500] if bio else "",
            profile_url=url,
            avatar_url=avatar_url,
            followers=followers,
            following=following,
            posts_count=posts_count,
            verified=verified,
            is_business=is_biz,
            category=category,
            email=email,
            phone=phone,
            website=website,
            source=LeadSource.INSTAGRAM,
        )

    async def scrape_hashtag(self, hashtag: str, max_results: int = 50, extract_contact: bool = True, only_business: bool = False) -> AsyncIterator[Lead]:
        """Scrape posts from a hashtag, extract unique usernames."""
        page = await self._ensure_session()
        url = f"{self.BASE_URL}/explore/tags/{quote(hashtag.lstrip('#'))}/"
        await page.goto(url, wait_until="networkidle")

        # Extract post URLs
        post_urls = await page.evaluate("""(max) => {
            const links = Array.from(document.querySelectorAll('a[href*="/p/"]'));
            return [...new Set(links.map(a => a.href))].slice(0, max);
        }""", max_results * 2)  # over-fetch to compensate for filter

        seen_users = set()
        for post_url in post_urls:
            if len(seen_users) >= max_results:
                break
            await page.goto(post_url, wait_until="networkidle")
            await page.wait_for_timeout(random.uniform(
                self.settings.delay_min_seconds * 1000,
                self.settings.delay_max_seconds * 1000,
            ))
            # Extract author username
            username = await page.evaluate("""() => {
                const el = document.querySelector('a[href^="/"][role="link"] span');
                // Fallback: extract from URL or header
                const header = document.querySelector('header a[href]');
                return header ? header.getAttribute('href').replace('/', '') : '';
            }""")
            if not username or username in seen_users:
                continue
            seen_users.add(username)
            try:
                lead = await self.scrape_profile(username, extract_contact=extract_contact)
                if only_business and not lead.is_business:
                    continue
                yield lead
            except Exception:
                continue

    async def scrape_followers_of(self, target_username: str, max_results: int = 50, extract_contact: bool = True, only_business: bool = False) -> AsyncIterator[Lead]:
        """Scrape followers of a target account. Requires login session."""
        page = await self._ensure_session()
        # Navigate to target profile
        await page.goto(f"{self.BASE_URL}/{target_username}/", wait_until="networkidle")

        # Click followers link
        try:
            await page.click('a[href*="/followers/"]')
            await page.wait_for_timeout(2000)
        except Exception:
            return

        seen_users = set()
        scroll_count = 0
        max_scrolls = max_results // 10 + 5

        while len(seen_users) < max_results and scroll_count < max_scrolls:
            # Extract visible usernames
            usernames = await page.evaluate("""() => {
                const links = document.querySelectorAll('div[role="dialog"] a[href^="/"]');
                return Array.from(links).map(a => a.getAttribute('href').replace('/', '')).filter(u => u && !u.includes('/'));
            }""")

            for username in usernames:
                if username in seen_users or len(seen_users) >= max_results:
                    continue
                seen_users.add(username)
                try:
                    lead = await self.scrape_profile(username, extract_contact=extract_contact)
                    if only_business and not lead.is_business:
                        continue
                    yield lead
                except Exception:
                    continue

            # Scroll the followers modal
            await page.evaluate("""() => {
                const dialog = document.querySelector('div[role="dialog"]');
                if (dialog) dialog.scrollTop = dialog.scrollHeight;
            }""")
            await page.wait_for_timeout(2000)
            scroll_count += 1

    async def close(self):
        if self._browser:
            await self._browser.close()
        if self._pw:
            await self._pw.stop()
        self._browser = None
        self._context = None
        self._page = None


async def scrape(req: ScrapeRequest) -> list[Lead]:
    """Main scrape entrypoint."""
    scraper = InstagramScraper()
    leads = []
    try:
        if req.target_type == "username":
            lead = await scraper.scrape_profile(req.target, extract_contact=req.extract_contact)
            if not req.only_business or lead.is_business:
                leads.append(lead)
        elif req.target_type == "hashtag":
            async for lead in scraper.scrape_hashtag(req.target, max_results=req.max_results, extract_contact=req.extract_contact, only_business=req.only_business):
                leads.append(lead)
        elif req.target_type == "followers_of":
            async for lead in scraper.scrape_followers_of(req.target, max_results=req.max_results, extract_contact=req.extract_contact, only_business=req.only_business):
                leads.append(lead)
        else:
            raise ValueError(f"Unknown target_type: {req.target_type}")
    finally:
        await scraper.close()
    return leads
