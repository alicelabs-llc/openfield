"""LicitAlert — Service orchestrator."""
from __future__ import annotations
import asyncio
from datetime import datetime
from licitalert.core.config import get_settings
from licitalert.core.models import Tender, AlertRule, TenderMatch
from licitalert.core.matcher import find_matches
from licitalert.core.store import AlertStore
from licitalert.scrapers import get_scraper
from licitalert.notifiers import send_matches_alert


class LicitAlertService:
    """Main service: scrape + match + notify."""

    def __init__(self):
        self.store = AlertStore()
        self.settings = get_settings()

    async def check_all_countries(self, since_hours: int = 24) -> list[Tender]:
        """Fetch tenders from all configured countries."""
        countries = [c.strip() for c in self.settings.countries.split(",") if c.strip()]
        all_tenders = []
        for country in countries:
            try:
                scraper = get_scraper(country)
                tenders = await scraper.fetch_tenders(since_hours=since_hours)
                # Save new ones
                for t in tenders:
                    if not self.store.is_seen(t.id, country):
                        self.store.save_tender(t)
                        all_tenders.append(t)
            except Exception as e:
                continue
        return all_tenders

    async def run_check_cycle(self) -> dict:
        """Run full check: scrape → match → notify."""
        new_tenders = await self.check_all_countries()
        if not new_tenders:
            return {"new_tenders": 0, "matches": 0, "notified": 0}

        rules = self.store.list_rules()
        if not rules:
            return {"new_tenders": len(new_tenders), "matches": 0, "notified": 0}

        matches = find_matches(new_tenders, rules)
        if not matches:
            return {"new_tenders": len(new_tenders), "matches": 0, "notified": 0}

        # Group matches by rule + recipient for batched notification
        grouped = {}
        for m in matches:
            rule = next((r for r in rules if r.id == m.rule_id), None)
            if not rule:
                continue
            key = (rule.id, rule.alert_recipient, tuple(sorted(rule.alert_channels)))
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(m)

        notified = 0
        for (rule_id, recipient, channels), ms in grouped.items():
            ch_list = list(channels)
            try:
                results = await send_matches_alert(ms, ch_list, recipient)
                if any(results.values()):
                    notified += 1
            except Exception:
                pass

        return {
            "new_tenders": len(new_tenders),
            "matches": len(matches),
            "notified": notified,
            "checked_at": datetime.utcnow().isoformat(),
        }
