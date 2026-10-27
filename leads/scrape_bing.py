#!/usr/bin/env python3
"""Use Bing RSS/search to find X.com, LinkedIn, IndieHackers, Mastodon posts."""
import urllib.request, urllib.parse, json, time, re, sys
from html.parser import HTMLParser

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

QUERIES = [
    # X/Twitter posts
    ("x", 'site:x.com "looking for" "AI agent" developer'),
    ("x", 'site:x.com "hiring" "Python" "FastAPI" remote'),
    ("x", 'site:x.com "need someone" "GitLab" OR "GitHub" automation'),
    ("x", 'site:x.com "looking for" "security" "audit" python'),
    ("x", 'site:x.com "seeking" "freelance" "Docker" "LLM"'),
    ("x", 'site:x.com "any recommendations" developer python'),
    ("x", 'site:x.com "need to build" agent bot telegram'),
    ("x", 'site:x.com #buildinpublic "looking for" developer'),
    ("x", 'site:x.com #freelance "AI" "python"'),
    ("x", 'site:twitter.com "looking for" "AI agent" developer'),
    ("x", 'site:twitter.com "hiring" "Python" "FastAPI" remote'),
    ("x", 'site:twitter.com "need someone" "GitHub" automation'),
    # LinkedIn posts
    ("linkedin", 'site:linkedin.com/posts "hiring" "Python" "remote"'),
    ("linkedin", 'site:linkedin.com/posts "looking for" "freelance" "developer"'),
    ("linkedin", 'site:linkedin.com/posts "AI agent" "contract"'),
    ("linkedin", 'site:linkedin.com/jobs/view "AI agent" "contract"'),
    ("linkedin", 'site:linkedin.com/posts "FastAPI" "remote"'),
    ("linkedin", 'site:linkedin.com/posts "Docker" "LLM"'),
    # IndieHackers
    ("indiehackers", 'site:indiehackers.com "looking for developer"'),
    ("indiehackers", 'site:indiehackers.com "need help with"'),
    ("indiehackers", 'site:indiehackers.com "hiring contractor"'),
    ("indiehackers", 'site:indiehackers.com "looking for" "freelance"'),
    # Reddit fallback via Bing
    ("reddit", 'site:reddit.com/r/forhire "AI agent" "hiring"'),
    ("reddit", 'site:reddit.com/r/freelance "Wanted" "Python"'),
    ("reddit", 'site:reddit.com/r/SaaS "looking for" "developer"'),
    ("reddit", 'site:reddit.com/r/devops "freelance" "Docker"'),
    ("reddit", 'site:reddit.com/r/artificial "looking for" "developer"'),
    ("reddit", 'site:reddit.com/r/learnpython "help" "pay"'),
    # Mastodon
    ("mastodon", 'site:mastodon.social "looking for" "developer" "python"'),
    ("mastodon", 'site:mastodon.world "hiring" "python" "remote"'),
    ("mastodon", 'site:hachyderm.io "AI agent" "freelance"'),
    ("mastodon", 'site:fosstodon.org "python" "freelance"'),
    # Bluesky
    ("bluesky", 'site:bsky.app "looking for" "AI" "developer"'),
    ("bluesky", 'site:bsky.app "hiring" "python" "remote"'),
]

def bing_search(q, n=30):
    """Search Bing and parse HTML results."""
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": q, "count": n})
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"  err: {e}", file=sys.stderr)
        return ""

class BingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.in_li = False
        self.in_h2 = False
        self.in_a = False
        self.cur_url = None
        self.cur_title = ""
        self.cur_text = ""
        self.capture_link = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "li" and "b_algo" in a.get("class", ""):
            self.in_li = True
        if self.in_li and tag == "h2":
            self.in_h2 = True
        if self.in_li and self.in_h2 and tag == "a":
            self.in_a = True
            href = a.get("href", "")
            if href.startswith("http"):
                self.cur_url = href
        if self.in_li and tag == "p":
            self.capture_link = True

    def handle_data(self, data):
        if self.in_a and self.cur_url:
            self.cur_title += data
        if self.in_li and self.capture_link:
            self.cur_text += data + " "

    def handle_endtag(self, tag):
        if tag == "a" and self.in_a:
            self.in_a = False
        if tag == "h2" and self.in_h2:
            self.in_h2 = False
        if tag == "li" and self.in_li:
            if self.cur_url:
                self.results.append({
                    "url": self.cur_url,
                    "title": self.cur_title.strip(),
                    "snippet": self.cur_text.strip()[:500],
                })
            self.in_li = False
            self.cur_url = None
            self.cur_title = ""
            self.cur_text = ""
            self.capture_link = False

results = []
for i, (platform, q) in enumerate(QUERIES):
    print(f"[{i+1}/{len(QUERIES)}] {platform}: {q!r}", file=sys.stderr)
    html = bing_search(q)
    parser = BingParser()
    try:
        parser.feed(html)
    except Exception as e:
        print(f"  parse err: {e}", file=sys.stderr)
    print(f"  found {len(parser.results)} results", file=sys.stderr)
    for r in parser.results:
        r["platform"] = platform
        r["query"] = q
    results.extend(parser.results)
    time.sleep(3)

with open("/home/z/my-project/leads/bing_leads.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\nBing total: {len(results)} results", file=sys.stderr)
