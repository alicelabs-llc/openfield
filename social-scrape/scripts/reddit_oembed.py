#!/usr/bin/env python3
"""
Reddit oembed enrichment: fetches author + post title for each Reddit URL.
Works without auth (the /oembed endpoint is public for embed widgets).
"""
import sys, json, urllib.request, urllib.parse, time, re, concurrent.futures

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def enrich(url):
    """Return {author, title, subreddit, url} from oembed, or {error}."""
    api = "https://www.reddit.com/oembed?url=" + urllib.parse.quote(url, safe="")
    try:
        req = urllib.request.Request(api, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read().decode("utf-8", errors="replace"))
        author = d.get("author_name", "")
        html_ = d.get("html", "")
        # extract subreddit from html: 'in\n<a href="https://www.reddit.com/r/<sub>/">'
        m = re.search(r'reddit\.com/r/([^/]+)/', html_)
        sub = m.group(1) if m else ""
        # extract title from html: first <a>...</a> after blockquote
        m2 = re.search(r'reddit\.com/r/[^/]+/comments/[^"]+">([^<]+)</a>', html_)
        title = m2.group(1) if m2 else ""
        return {"author": author, "title": title, "subreddit": sub, "url": url, "ok": True}
    except Exception as e:
        return {"url": url, "error": str(e)[:200], "ok": False}

def enrich_many(urls, max_workers=4):
    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(enrich, u): u for u in urls}
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            out.append(r)
            print(f"[oembed] {r.get('url','')[:80]} -> {r.get('author','ERR:'+r.get('error',''))}", file=sys.stderr)
    return out

if __name__ == "__main__":
    # Reads URLs from stdin (one per line) OR from a JSON file passed as arg
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
        if isinstance(data, list):
            urls = data
        else:
            # dict of query -> list of results
            urls = []
            for q, results in data.items():
                for r in results:
                    if isinstance(r, dict) and r.get("url"):
                        urls.append(r["url"])
    else:
        urls = [l.strip() for l in sys.stdin if l.strip()]
    # dedupe
    seen = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]
    print(f"[oembed] enriching {len(urls)} unique URLs", file=sys.stderr)
    results = enrich_many(urls)
    print(json.dumps(results, ensure_ascii=False, indent=2))
