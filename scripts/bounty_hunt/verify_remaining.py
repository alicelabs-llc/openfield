"""Verify the rate-limited entries + upstream Parabola bounty."""
import json, re, ssl, time, urllib.request

with open('results_v3.json') as f:
    data = json.load(f)

ctx = ssl.create_default_context()
patterns = [
    (re.compile(r'\$\s?(\d{1,3}(?:[,\d]{0,9}))\b'), 'dollar'),
    (re.compile(r'(?<!EIP-)(?<!RFC-)\b(\d{2,6})\s?USDC\b', re.IGNORECASE), 'N USDC'),
    (re.compile(r'\b(\d{2,6})\s?USD\b', re.IGNORECASE), 'N USD'),
    (re.compile(r'\b(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|MATIC)\b', re.IGNORECASE), 'crypto'),
    (re.compile(r'\b(?:bounty|reward|payout|prize)[:\s]*\$?\s?(\d{2,6}(?:[,\d]{0,9}))', re.IGNORECASE), 'bounty kw'),
]
units = {'ETH':3000,'SOL':150,'BTC':65000,'DAI':1,'MATIC':0.7}

# Issues to verify (those that rate-limited before + Parabola upstream + lockpick)
to_verify = []
for e in data['top_20']:
    to_verify.append((e['repo'], e['number'], e['url'], e))
# Add upstream Parabola bounty
to_verify.append(('Parabola-org/parabola', 10, 'https://github.com/Parabola-org/parabola/issues/10', None))

results = []
for repo, num, url, orig in to_verify:
    api_url = url.replace('https://github.com/', 'https://api.github.com/repos/').replace('/issues/', '/issues/')
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent':'x','Accept':'application/vnd.github+json'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            full = json.loads(r.read().decode())
        body = full.get('body','') or ''
        title = full.get('title','')
        haystack = title + '\n' + body
        matches = []
        for p, name in patterns:
            for m in p.finditer(haystack):
                ctx_txt = haystack[max(0,m.start()-40):m.end()+20].replace('\n',' ')
                matches.append((name, m.group(0), m.group(1), ctx_txt))
        real = 0.0
        for name, full_m, val_str, ctx_txt in matches:
            try: v = float(val_str.replace(',',''))
            except: continue
            if not (25 <= v <= 100000): continue
            if name == 'dollar' and '$' in full_m:
                real = max(real, v)
            elif name == 'N USDC' and 'EIP' not in ctx_txt and 'BIP' not in ctx_txt:
                real = max(real, v)
            elif name == 'N USD':
                real = max(real, v)
            elif name == 'crypto':
                m2 = re.match(r'(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|MATIC)', full_m, re.IGNORECASE)
                if m2:
                    v2 = float(m2.group(1)) * units.get(m2.group(2).upper(), 1)
                    if 25 <= v2 <= 100000:
                        real = max(real, v2)
        results.append({'repo': repo, 'number': num, 'url': url,
                        'verified_reward_usd': real, 'title': title,
                        'state': full.get('state'),
                        'comments': full.get('comments'),
                        'assignee': (full.get('assignee') or {}).get('login') if full.get('assignee') else None,
                        'created_at': full.get('created_at'),
                        'top_match_evidence': matches[:3]})
        print(f'  {repo[:38]:<38} #{num:<6}  verified=${real:.2f}  title="{title[:60]}"')
        for name, full_m, val_str, ctx_txt in matches[:2]:
            print(f'      [{name}] {full_m!r}  ctx="{ctx_txt}"')
    except Exception as ex:
        print(f'  {repo} #{num}  ERROR: {ex}')
        results.append({'repo': repo, 'number': num, 'url': url,
                        'verified_reward_usd': -1, 'title': '', 'error': str(ex)})
    time.sleep(2)

with open('results_verified_full.json','w') as f:
    json.dump(results, f, indent=2, default=str)
print(f'\nWrote {len(results)} verified entries to results_verified_full.json')
