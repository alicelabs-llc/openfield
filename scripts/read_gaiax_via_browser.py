import sys, time
sys.path.insert(0, '/home/z/my-project/scripts')
from agent_bridge_cli import send_command

# Navigate to the raw file
files = [
    "contexts/SignatureContext.tsx",
    "web-crypto/sign.ts",
    "web-crypto/index.ts",
    "models/wallet.ts",
    "hooks/useLocalWallet.ts",
]

for path in files:
    print(f"\n=== Reading {path} ===")
    url = f"https://gitlab.com/gaia-x/lab/wizards/compliance-wizard/-/raw/main/{path}"
    resp = send_command('open', url=url, timeout=30)
    if not resp:
        continue
    time.sleep(3)
    resp = send_command('gettext', selector='pre', timeout=20)
    if resp and resp.get('ok'):
        text = resp.get('result', {}).get('text', '')
        print(f"  ✅ {len(text)} chars")
        # Save locally
        local_path = f"/tmp/gaiax_{path.replace('/','_')}"
        with open(local_path, 'w') as f:
            f.write(text)
        print(f"  saved to {local_path}")
    else:
        # Try body
        resp = send_command('gettext', selector='body', timeout=20)
        if resp and resp.get('ok'):
            text = resp.get('result', {}).get('text', '')
            if len(text) > 100:
                print(f"  ✅ via body: {len(text)} chars")
                local_path = f"/tmp/gaiax_{path.replace('/','_')}"
                with open(local_path, 'w') as f:
                    f.write(text)
                print(f"  saved to {local_path}")
            else:
                print(f"  ❌ too short: {text[:100]}")
        else:
            print("  ❌ timeout")
