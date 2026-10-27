#!/usr/bin/env python3
"""
Fetch Reddit post body content via per-post RSS feed (.rss).
This endpoint is unblocked (unlike /search.json which requires login).
Returns the post body as plain text.
"""
import sys, json, urllib.request, urllib.parse, re, html as html_mod
import concurrent.futures, time

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_rss_body(url):
    """Given a Reddit post URL, fetch its RSS feed and extract body + author + date."""
    rss_url = url.rstrip('/') + '/.rss'
    try:
        req = urllib.request.Request(rss_url, headers={"User-Agent": UA, "Accept": "application/atom+xml"})
        with urllib.request.urlopen(req, timeout=15) as r:
            xml = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return {"url": url, "error": str(e)[:200], "ok": False}
    # Parse the first <entry>
    m = re.search(r'<entry>(.*?)</entry>', xml, re.S)
    if not m:
        # Try fallback: sometimes feed is empty (post deleted)
        return {"url": url, "ok": False, "error": "no_entry"}
    entry = m.group(1)
    # Extract author
    am = re.search(r'<author><name>([^<]+)</name>', entry)
    author = am.group(1) if am else ""
    # author format is "/u/<name>"
    author = author.replace("/u/", "").strip()
    # Extract content (HTML)
    cm = re.search(r'<content[^>]*>(.*?)</content>', entry, re.S)
    if not cm:
        return {"url": url, "ok": False, "error": "no_content"}
    content_html = cm.group(1)
    # Strip HTML tags
    text = html_mod.unescape(re.sub(r'<[^>]+>', ' ', content_html))
    text = re.sub(r'\s+', ' ', text).strip()
    # Look for [removed] / [deleted]
    if text.startswith('[removed]') or text.startswith('[deleted]'):
        return {"url": url, "ok": True, "body": text, "author": author, "removed": True}
    # Extract publish/update date
    pm = re.search(r'<updated>([^<]+)</updated>', xml)
    pub_date = pm.group(1) if pm else ""
    return {
        "url": url, "ok": True, "author": author, "body": text[:2000],
        "pub_date_iso": pub_date, "removed": False
    }

def fetch_many(urls, max_workers=2, delay=8):
    """Fetch with polite delays (Reddit rate-limits aggressive parallel access)."""
    out = []
    # Serial fetch with delay — Reddit 429s hard on parallel
    for u in urls:
        r = fetch_rss_body(u)
        out.append(r)
        print(f"[rss] {u[-60:]:60s} -> {'OK' if r.get('ok') else 'ERR:'+r.get('error','')[:50]}", file=sys.stderr)
        time.sleep(delay)
    return out

if __name__ == "__main__":
    urls = json.load(open(sys.argv[1] if len(sys.argv)>1 else '/dev/stdin'))
    print(f"[rss] fetching {len(urls)} post bodies", file=sys.stderr)
    results = fetch_many(urls)
    print(json.dumps(results, ensure_ascii=False, indent=2))
