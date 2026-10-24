"""ReviewReply AI — Platform connectors (Google Business, Yelp, etc.)."""
from __future__ import annotations
from reviewreply.core.models import Review, Platform
import httpx


class GoogleBusinessConnector:
    """Google Business Profile API connector (read reviews + post replies).

    Requires OAuth2 token with https://www.googleapis.com/auth/business.manage scope.
    """

    BASE_URL = "https://mybusiness.googleapis.com/v4"

    def __init__(self, access_token: str, account_id: str, location_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.location_id = location_id

    async def list_reviews(self, page_size: int = 50) -> list[Review]:
        """Fetch recent reviews for the location."""
        url = f"{self.BASE_URL}/accounts/{self.account_id}/locations/{self.location_id}/reviews"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers, params={"pageSize": page_size})
        if r.status_code != 200:
            return []
        data = r.json()
        reviews = []
        for item in data.get("reviews", []):
            reviews.append(Review(
                id=item.get("reviewId", ""),
                platform=Platform.GOOGLE_REVIEWS,
                author_name=item.get("reviewer", {}).get("displayName", ""),
                author_avatar=item.get("reviewer", {}).get("profilePhotoUrl", ""),
                rating=int(item.get("starRating", 5) if item.get("starRating") else 5),
                title="",
                text=item.get("comment", ""),
                business_response=item.get("reviewReply", {}).get("comment", ""),
            ))
        return reviews

    async def post_reply(self, review_id: str, reply_text: str) -> bool:
        """Post a reply to a review."""
        url = f"{self.BASE_URL}/accounts/{self.account_id}/locations/{self.location_id}/reviews/{review_id}/reply"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.put(url, headers=headers, json={"comment": reply_text})
        return r.status_code == 200


class YelpConnector:
    """Yelp Fusion API connector (read-only, replies via business dashboard)."""

    BASE_URL = "https://api.yelp.com/v3"

    def __init__(self, api_key: str, business_id: str):
        self.api_key = api_key
        self.business_id = business_id

    async def list_reviews(self) -> list[Review]:
        url = f"{self.BASE_URL}/businesses/{self.business_id}/reviews"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=headers)
        if r.status_code != 200:
            return []
        data = r.json()
        reviews = []
        for item in data.get("reviews", []):
            reviews.append(Review(
                id=item.get("id", ""),
                platform=Platform.YELP,
                author_name=item.get("user", {}).get("name", ""),
                author_avatar=item.get("user", {}).get("image_url", ""),
                rating=int(item.get("rating", 5)),
                text=item.get("text", ""),
            ))
        return reviews
