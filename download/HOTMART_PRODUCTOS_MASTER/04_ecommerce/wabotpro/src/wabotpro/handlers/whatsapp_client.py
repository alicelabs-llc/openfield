"""WhatsAppBot Pro — WhatsApp Cloud API client (Meta official)."""
from __future__ import annotations
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from wabotpro.core.config import get_settings


class WhatsAppCloudClient:
    """Client for Meta WhatsApp Cloud API (v21.0)."""

    BASE_URL = "https://graph.facebook.com"

    def __init__(self):
        self.s = get_settings()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_text(self, to: str, text: str) -> dict:
        """Send a text message."""
        if not self.s.wa_access_token or not self.s.wa_phone_number_id:
            return {"success": False, "error": "WA_ACCESS_TOKEN or WA_PHONE_NUMBER_ID not set"}

        url = f"{self.BASE_URL}/{self.s.wa_api_version}/{self.s.wa_phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text, "preview_url": False},
        }
        headers = {
            "Authorization": f"Bearer {self.s.wa_access_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            return r.json()
        return {"success": False, "error": f"HTTP {r.status_code}: {r.text}"}

    async def send_button(self, to: str, text: str, buttons: list[dict]) -> dict:
        """Send interactive button message."""
        url = f"{self.BASE_URL}/{self.s.wa_api_version}/{self.s.wa_phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": b["id"], "title": b["title"][:20]},
                        } for b in buttons
                    ]
                },
            },
        }
        headers = {
            "Authorization": f"Bearer {self.s.wa_access_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(url, json=payload, headers=headers)
        return r.json() if r.status_code == 200 else {"error": r.text}

    async def send_image(self, to: str, image_url: str, caption: str = "") -> dict:
        """Send an image message."""
        url = f"{self.BASE_URL}/{self.s.wa_api_version}/{self.s.wa_phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {"link": image_url, "caption": caption},
        }
        headers = {"Authorization": f"Bearer {self.s.wa_access_token}"}
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(url, json=payload, headers=headers)
        return r.json() if r.status_code == 200 else {"error": r.text}
