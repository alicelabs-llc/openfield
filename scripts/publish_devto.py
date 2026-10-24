#!/usr/bin/env python3
"""
Publish the DEV.to HF26 Week 3 post directly via the Forem API.

Usage:
  python3 publish_devto.py

Requires:
  - DEVTO_API_KEY env var OR replace the placeholder below with the key
  - The post content at /home/z/my-project/download/devto_hf26_week3_post.md

API docs: https://developers.forem.com/api/v0#tag/articles/operation/createArticle
Endpoint: POST https://dev.to/api/articles
Headers: api-key: <KEY>, Content-Type: application/json
"""
import json
import os
import sys
import urllib.request
import urllib.error

# === REPLACE THIS WITH THE ACTUAL DEV.TO API KEY ===
# User can generate one at https://dev.to/settings/account
# (scroll down to "DEV Community API Keys" → "Generate API Key")
API_KEY = os.environ.get("DEVTO_API_KEY", "PASTE_KEY_HERE")

POST_PATH = "/home/z/my-project/download/devto_hf26_week3_post.md"

if API_KEY == "PASTE_KEY_HERE":
    print("❌ ERROR: DEVTO_API_KEY env var not set and no key in script.")
    print("   Generate one at: https://dev.to/settings/account")
    print("   (Scroll down to 'DEV Community API Keys' → click 'Generate API Key')")
    print()
    print("   Then run with:")
    print("   DEVTO_API_KEY='your_key_here' python3 publish_devto.py")
    sys.exit(1)

# Read the markdown file
with open(POST_PATH, 'r') as f:
    body_markdown = f.read()

# Strip the front matter since we'll pass it as separate fields
# (DEV.to accepts front matter in body_markdown, but cleaner to pass as fields)
import re
front_matter_match = re.match(r'^---\n(.*?)\n---\n', body_markdown, re.DOTALL)
front_matter = {}
if front_matter_match:
    fm_text = front_matter_match.group(1)
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key in ('tags',):
                front_matter[key] = [t.strip() for t in val.strip('[]').split(',') if t.strip()]
            else:
                front_matter[key] = val
    body_markdown = body_markdown[front_matter_match.end():]

print(f"✅ Post loaded: {len(body_markdown)} chars, {len(body_markdown.split())} words")
print(f"   Title: {front_matter.get('title', '?')}")
print(f"   Tags: {front_matter.get('tags', [])}")
print(f"   Published: {front_matter.get('published', True)}")
print()

# Build API payload
payload = {
    "article": {
        "title": front_matter.get("title", "I let an AI agent do my overnight chores — but every step is signed"),
        "published": front_matter.get("published", "true") == "true",
        "body_markdown": body_markdown,
        "tags": front_matter.get("tags", ["devchallenge", "hf26challenge", "hacktoberfest", "ai"]),
        "description": front_matter.get("description", "Slow-and-steady agent execution with sandboxed blast radius + tamper-evident provenance"),
        "canonical_url": front_matter.get("canonical_url"),
    }
}
if front_matter.get("cover_image"):
    payload["article"]["main_image"] = front_matter["cover_image"]

print("📤 Publishing to DEV.to...")
print(f"   Endpoint: POST https://dev.to/api/articles")

req = urllib.request.Request(
    "https://dev.to/api/articles",
    data=json.dumps(payload).encode(),
    method="POST",
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
        print("🎉 PUBLISHED!")
        print(f"   URL: {response.get('url', '?')}")
        print(f"   Path: {response.get('path', '?')}")
        print(f"   ID: {response.get('id', '?')}")
        print(f"   Tags: {response.get('tag_list', '?')}")
        print(f"   Reading time: {response.get('reading_time_minutes', '?')} min")
        print(f"   Published at: {response.get('published_at', '?')}")
        print()
        print("✅ Done. The post is live.")
        
        # Save the URL to a file for tracking
        with open("/home/z/my-project/download/devto_posted_url.txt", 'w') as f:
            f.write(response.get('url', 'unknown') + '\n')
            f.write(f"ID: {response.get('id', 'unknown')}\n")
            f.write(f"Published: {response.get('published_at', 'unknown')}\n")
        
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f"❌ HTTP {e.code}: {e.reason}")
    print(f"   Response: {err_body[:500]}")
    sys.exit(2)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(3)
