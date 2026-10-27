#!/usr/bin/env python3
"""
DuckDuckGo HTML search for site:reddit.com / site:x.com queries.
No API key required. Returns list of dicts: {title,url,snippet,query,engine}.
"""
import re, html, time, sys, json, urllib.parse
from urllib.parse import unquote
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def ddg_search(query, max_results=15):
    """Return list of {title,url,snippet} from DuckDuckGo HTML."""
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            h = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return [{"error": str(e)[:200]}]
    out = []
    pattern = re.compile(
        r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.+?)</a>.*?'
        r'<a[^>]+class="result__snippet"[^>]*>(.+?)</a>',
        re.S
    )
    for m in pattern.finditer(h):
        raw_url = m.group(1)
        u = unquote(raw_url)
        m2 = re.search(r'uddg=([^&]+)', u)
        if m2:
            real = unquote(m2.group(1))
        else:
            real = u
        title = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        snip = html.unescape(re.sub(r'<[^>]+>', '', m.group(3))).strip()
        out.append({"title": title, "url": real, "snippet": snip})
        if len(out) >= max_results:
            break
    return out

if __name__ == "__main__":
    queries = sys.argv[1:]
    all_results = {}
    for q in queries:
        print(f"[DDG] {q}", file=sys.stderr)
        results = ddg_search(q)
        all_results[q] = results
        time.sleep(2)
    print(json.dumps(all_results, ensure_ascii=False, indent=2))
