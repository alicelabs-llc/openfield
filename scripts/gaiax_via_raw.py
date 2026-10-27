import json, ssl, time, base64, urllib.request, urllib.error

TOKEN = "glpat-PfWyLHoeZpLOyyQSzyDX72M6MQpvOjEKdTpranZqbQ8.01.1715hm5mn"
PID = 44670736  # gaia-x/lab/wizards/compliance-wizard
FORK_PID = 87980178  # eddyflores100/compliance-wizard
UPSTREAM_PID = 44670736
BRANCH = "feature/hsm-support"
CTX = ssl.create_default_context()
headers = {"PRIVATE-TOKEN": TOKEN, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def get_file(path, retries=5):
    """Read a file from the repo via Contents API (returns base64 content)."""
    encoded_path = path.replace("/", "%2F")
    url = f"https://gitlab.com/api/v4/projects/{PID}/repository/files/{encoded_path}?ref=main"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
                d = json.loads(resp.read().decode())
                content = base64.b64decode(d["content"]).decode()
                return content, d["sha"]
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(12)
            else:
                return None, None

def put_file_fork(path, content, commit_msg, retries=5):
    """Upload/update a file in the fork via Contents API."""
    encoded_path = path.replace("/", "%2F")
    b64 = base64.b64encode(content.encode()).decode()
    url = f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/files/{encoded_path}"
    payload = {
        "branch": BRANCH,
        "content": b64,
        "commit_message": commit_msg,
        "encoding": "base64",
    }
    # First try PUT (update), then POST (create)
    for method in ["PUT", "POST"]:
        for attempt in range(3):
            try:
                data = json.dumps(payload).encode()
                req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"}, method=method)
                with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
                    d = json.loads(resp.read().decode())
                    return True
            except urllib.error.HTTPError as e:
                body = e.read().decode()
                if "already exists" in body and method == "PUT":
                    continue
                if attempt < 2:
                    time.sleep(12)
            except Exception:
                if attempt < 2:
                    time.sleep(12)
    return False

# Step 1: Create branch in fork
print("=== Step 1: Create branch ===")
url = f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/branches"
data = json.dumps({"branch": BRANCH, "ref": "main"}).encode()
for attempt in range(3):
    try:
        req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            print(f"  ✅ Branch created")
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body:
            print("  Branch already exists, continuing...")
            break
        time.sleep(12)
    except:
        time.sleep(12)

# Step 2: Read the key source files
print("\n=== Step 2: Read source files ===")
files_to_read = [
    "contexts/SignatureContext.tsx",
    "contexts/WalletContext.tsx",
    "hooks/useLocalWallet.ts",
    "hooks/useSigner.ts",
    "models/wallet.ts",
    "web-crypto/index.ts",
    "web-crypto/sign.ts",
    "components/Wallet/index.tsx",
]

read_files = {}
for path in files_to_read:
    print(f"  Reading {path}...", end=" ")
    content, sha = get_file(path)
    if content:
        print(f"✅ ({len(content)} chars)")
        read_files[path] = content
    else:
        print("❌ (Cloudflare)")
    time.sleep(3)

if not read_files:
    print("\n❌ Could not read ANY files. Cloudflare blocking all reads.")
    exit(1)

print(f"\nRead {len(read_files)} files")

# Step 3: Analyze what we have
print("\n=== Step 3: Analyze ===")
for path, content in read_files.items():
    print(f"\n--- {path} ({len(content)} chars) ---")
    print(content[:500])
    print("...")

# Step 4: Check if there's existing HSM/key handling
print("\n=== Step 4: Check for existing HSM/crypto code ===")
for path, content in read_files.items():
    for keyword in ["hsm", "HSM", "PKCS", "pkcs11", "signing", "privateKey", "private_key", "x509", "certificate"]:
        if keyword.lower() in content.lower():
            idx = content.lower().find(keyword.lower())
            print(f"  {path}: found '{keyword}' at pos {idx}: ...{content[max(0,idx-20):idx+80]}...")

