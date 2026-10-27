#!/usr/bin/env python3
"""
Bing search parser for site:x.com / site:reddit.com queries.
Decodes Bing's 'ck/a' redirect URLs (u=a1<base64url>) to real URLs.

Bing indexes Twitter/X content reasonably well, and unlike DDG, doesn't
rate-limit as aggressively when called with browser-like headers.
"""
import re, html, time, sys, json, base64, urllib.parse, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def decode_bing_u(u_param):
    """Bing encodes target URL as 'a1' + base64url."""
    if u_param.startswith("a1"):
        u_param = u_param[2:]
    # base64url -> base64
    s = u_param.replace("-", "+").replace("_", "/")
    # pad
    pad = len(s) % 4
    if pad:
        s += "=" * (4 - pad)
    try:
        return base64.b64decode(s).decode("utf-8", errors="replace")
    except Exception:
        return None

def bing_search(query, max_results=15, retries=2):
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&count=30"
    last_err = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml",
            })
            with urllib.request.urlopen(req, timeout=20) as r:
                h = r.read().decode("utf-8", errors="replace")
            out = []
            # Bing's algo result pattern: <li class="b_algo"> ... <h2><a href="...">title</a></h2> ... <p>snippet</p>
            for m in re.finditer(r'<li class="b_algo".*?<h2><a[^>]*href="([^"]+)"[^>]*>(.+?)</a></h2>(.*?)(?=<li class="b_algo"|$)', h, re.S):
                href = m.group(1)
                title = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
                body = m.group(3)
                # decode Bing redirect URL if present
                real = href
                um = re.search(r'[?&]u=a1([^&]+)', href)
                if um:
                    decoded = decode_bing_u("a1" + um.group(1))
                    if decoded:
                        real = decoded
                # try to grab snippet from <p> in body
                snip_match = re.search(r'<p[^>]*>(.+?)</p>', body, re.S)
                snip = ""
                if snip_match:
                    snip = html.unescape(re.sub(r'<[^>]+>', '', snip_match.group(1))).strip()
                out.append({"title": title, "url": real, "snippet": snip})
                if len(out) >= max_results:
                    break
            if out:
                return out
            last_err = "empty_results"
        except Exception as e:
            last_err = str(e)[:200]
        time.sleep(5 * (attempt + 1))
    return [{"error": last_err}]

if __name__ == "__main__":
    queries = sys.argv[1:]
    all_results = {}
    for q in queries:
        print(f"[Bing] {q}", file=sys.stderr)
        all_results[q] = bing_search(q)
        time.sleep(3)
    print(json.dumps(all_results, ensure_ascii=False, indent=2))
