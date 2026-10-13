import re, json, urllib.request, ssl

with open('/home/z/my-project/hacktoberfest-candidates/vajra/.git/config') as f:
    content = f.read()
m = re.search(r'https://[^:]+:([^@]+)@github\.com', content)
if not m:
    print("NO TOKEN FOUND")
    exit(1)
token = m.group(1)
print(f"Token length: {len(token)}")
print(f"First 4 chars: {token[:4]}")
print(f"Last 4 chars: {token[-4:]}")

# Test against GitHub API
headers = {
    "Authorization": f"token {token}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
ctx = ssl.create_default_context()
req = urllib.request.Request("https://api.github.com/user", headers=headers, method="GET")
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        d = json.loads(resp.read().decode())
    print(f"Authenticated as: {d.get('login','')} (id={d.get('id')})")
    print(f"Name: {d.get('name','')}")
    print(f"Email: {d.get('email','')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"ERR: {e}")
