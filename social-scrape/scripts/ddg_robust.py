#!/usr/bin/env python3
"""
Robust DDG HTML search with retries + polite delay.
Usage: python3 ddg_robust.py 'query1' 'query2' ... > output.json
"""
import re, html, time, sys, json, urllib.parse, urllib.request
from urllib.parse import unquote

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def ddg_search(query, max_results=20, retries=3, delay=8):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    last_err = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=25) as r:
                h = r.read().decode("utf-8", errors="replace")
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
                real = unquote(m2.group(1)) if m2 else u
                title = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
                snip = html.unescape(re.sub(r'<[^>]+>', '', m.group(3))).strip()
                out.append({"title": title, "url": real, "snippet": snip})
                if len(out) >= max_results:
                    break
            if out:
                return out
            # Sometimes DDG returns 200 with empty results block (rate-limit indicator)
            last_err = "empty_results"
        except Exception as e:
            last_err = str(e)[:200]
        time.sleep(delay * (attempt + 1))
    return [{"error": last_err}]

if __name__ == "__main__":
    queries = sys.argv[1:]
    all_results = {}
    for q in queries:
        print(f"[DDG] {q}", file=sys.stderr)
        all_results[q] = ddg_search(q)
        time.sleep(6)
    print(json.dumps(all_results, ensure_ascii=False, indent=2))
