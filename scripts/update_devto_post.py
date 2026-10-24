#!/usr/bin/env python3
"""
Update the existing DEV.to post (ID 4908108) with the improved v2 content
that adds: explicit Demo section, Why Open Innovation Matters section,
and GitHub Copilot usage section (qualifies for $100 partner prize).
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

API_KEY = os.environ.get("DEVTO_API_KEY", "JKTqE35XNwxTtSihCddbdqym")
ARTICLE_ID = 4908108  # The published post ID
POST_PATH = "/home/z/my-project/download/devto_hf26_week3_post_v2.md"

with open(POST_PATH, 'r') as f:
    body_markdown = f.read()

# Strip front matter
fm_match = re.match(r'^---\n(.*?)\n---\n', body_markdown, re.DOTALL)
front_matter = {}
if fm_match:
    fm_text = fm_match.group(1)
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key == 'tags':
                front_matter[key] = [t.strip() for t in val.strip('[]').split(',') if t.strip()]
            else:
                front_matter[key] = val
    body_markdown = body_markdown[fm_match.end():]

print(f"✅ Post loaded: {len(body_markdown)} chars, {len(body_markdown.split())} words")
print(f"   Title: {front_matter.get('title', '?')[:80]}")
print(f"   Tags: {front_matter.get('tags', [])}")
print()

# Use PUT to update the existing article
payload = {
    "article": {
        "title": front_matter.get("title"),
        "published": True,
        "body_markdown": body_markdown,
        "tags": front_matter.get("tags", ["devchallenge", "hf26challenge", "hacktoberfest", "showdev"]),
        "description": front_matter.get("description"),
    }
}
if front_matter.get("canonical_url"):
    payload["article"]["canonical_url"] = front_matter["canonical_url"]

print(f"📤 Updating DEV.to post ID {ARTICLE_ID} via PUT /api/articles/{ARTICLE_ID}...")

req = urllib.request.Request(
    f"https://dev.to/api/articles/{ARTICLE_ID}",
    data=json.dumps(payload).encode(),
    method="PUT",
    headers={
        "Content-Type": "application/json",
        "api-key": API_KEY,
        "User-Agent": "eddyflores100-lang-bot/1.0",
    },
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        response = json.loads(r.read())
        print()
        print("🎉 UPDATED!")
        print(f"   URL: {response.get('url', '?')}")
        print(f"   ID: {response.get('id', '?')}")
        print(f"   Tags: {response.get('tag_list', '?')}")
        print(f"   Reading time: {response.get('reading_time_minutes', '?')} min")
        print(f"   Edited at: {response.get('edited_at', '?')}")
        print(f"   Body length: {len(body_markdown)} chars, {len(body_markdown.split())} words")
        print()
        print("✅ Done. The post has been updated with:")
        print("   - Explicit '## What I Built' section (per submission template)")
        print("   - Explicit '## What effort it saves' section")
        print("   - Explicit '## Demo' section with 5-step walkthrough")
        print("   - Explicit '## Why Open Innovation Matters' section (3 reasons)")
        print("   - Explicit '## Built with GitHub Copilot' section (qualifies for $100 partner prize)")
        print("   - Preserved all original architecture + containment matrix sections")
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f"❌ HTTP {e.code}: {e.reason}")
    print(f"   Response: {err_body[:500]}")
    sys.exit(2)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(3)
