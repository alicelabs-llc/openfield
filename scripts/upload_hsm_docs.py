import json, ssl, time, base64, urllib.request, urllib.error

TOKEN = "glpat-PfWyLHoeZpLOyyQSzyDX72M6MQpvOjEKdTpranZqbQ8.01.1715hm5mn"
FORK_PID = 87980178
BRANCH = "feature/hsm-support"
CTX = ssl.create_default_context()
headers = {"PRIVATE-TOKEN": TOKEN, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

HSM_DOC = """# HSM Support

The Gaia-X Wizard supports signing Verifiable Credentials with Hardware Security Modules (HSMs) via the [Fortify](https://fortifyapp.com/) browser extension.

## How it works

When HSM mode is enabled, the Wizard:

1. Loads the Fortify web component from the Fortify CDN.
2. Opens a certificate selection dialog where the user picks a certificate from their HSM.
3. Extracts the public key and subject from the selected certificate (via `jsrsasign` X509 parsing).
4. Derives the signing algorithm from the certificate's key type:
   - ECDSA (P-256/P-384/P-521) -> ES256/ES384/ES512
   - RSA -> RS256
5. Signs Verifiable Credentials using the HSM's non-extractable private key via the WebCrypto API.

## Supported algorithms

| Algorithm | Key type | WebCrypto name |
|-----------|----------|---------------|
| ES256 | ECDSA P-256 | ECDSA with SHA-256 |
| ES384 | ECDSA P-384 | ECDSA with SHA-384 |
| ES512 | ECDSA P-521 | ECDSA with SHA-512 |
| RS256 | RSA 2048+ | RSASSA-PKCS1-v1_5 with SHA-256 |
| PS256 | RSA-PSS | RSA-PSS with SHA-256 |

## Enabling HSM

HSM support is a members-only feature. To enable it:

1. Install the [Fortify browser extension](https://fortifyapp.com/).
2. Connect your HSM or smart card to the Fortify app.
3. In the Wizard, navigate to the signing step.
4. Select "Use HSM" -- the Fortify certificate dialog will appear.
5. Select your certificate -- the Wizard will extract the public key and use it for signing.

## Architecture

- `web-crypto/fortify.ts` -- Fortify session management, certificate selection, algorithm detection.
- `web-crypto/signWithHsm.ts` -- JWS signing using the HSM's WebCrypto provider. Handles DER-to-raw signature conversion for ECDSA.
- `hooks/usePrivateKey.ts` -- Integrates HSM public key with the DID derivation flow.
- `hooks/useSignature.ts` -- Routes signing to HSM, eID, or software key based on the active mode.

## Limitations

- The HSM private key never leaves the hardware -- all signing happens via the WebCrypto API inside the Fortify provider.
- Only one HSM certificate can be active at a time (module-scoped session).
- RSA-PSS salt length is hardcoded per algorithm (32/48/64 bytes for SHA-256/384/512).
- The Fortify web component is loaded from CDN at a pinned version -- offline use is not supported.

## References

- [Fortify documentation](https://docs.fortifyapp.com/)
- [WebCrypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
- [JWS specification (RFC 7515)](https://tools.ietf.org/html/rfc7515)
"""

content_b64 = base64.b64encode(HSM_DOC.encode()).decode()
payload = {
    "branch": BRANCH,
    "content": content_b64,
    "commit_message": "docs: add HSM support documentation",
    "encoding": "base64",
}
data = json.dumps(payload).encode()

url = f"https://gitlab.com/api/v4/projects/{FORK_PID}/repository/files/docs%2FHSM_SUPPORT.md"

for attempt in range(5):
    try:
        req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            d = json.loads(resp.read().decode())
            print(f"✅ File uploaded: {d.get('file_path')}")
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body:
            # Try PUT instead
            req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"}, method="PUT")
            try:
                with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
                    d = json.loads(resp.read().decode())
                    print(f"✅ File updated: {d.get('file_path')}")
                    break
            except urllib.error.HTTPError as e2:
                print(f"PUT attempt {attempt+1}: HTTP {e2.code}: {e2.read().decode()[:200]}")
            except Exception as e3:
                print(f"PUT attempt {attempt+1}: {e3}")
        else:
            print(f"POST attempt {attempt+1}: HTTP {e.code}: {body[:200]}")
    except Exception as e:
        print(f"Attempt {attempt+1}: {e}")
    time.sleep(15)
else:
    print("❌ Failed after 5 attempts")

# Create MR
print("\n=== Create MR ===")
time.sleep(10)
mr_payload = {
    "title": "docs: add HSM support documentation",
    "source_branch": BRANCH,
    "target_branch": "main",
    "target_project_id": 44670736,
    "description": "Closes !27.\n\n## What\n\nAdds `docs/HSM_SUPPORT.md` documenting the existing HSM integration:\n\n- How HSM signing works (Fortify web component -> certificate selection -> WebCrypto signing)\n- Supported algorithms (ES256/384/512, RS256, PS256)\n- How to enable HSM (members-only feature)\n- Architecture: which files handle HSM (fortify.ts, signWithHsm.ts, usePrivateKey.ts, useSignature.ts)\n- Limitations (non-extractable keys, single active session, hardcoded salt lengths, CDN dependency)\n\nThe code already implements HSM support via Fortify -- this PR adds the missing documentation that issue !27 asks for. No code changes.",
}
data = json.dumps(mr_payload).encode()

for attempt in range(5):
    try:
        req = urllib.request.Request(
            f"https://gitlab.com/api/v4/projects/{FORK_PID}/merge_requests",
            data=data,
            headers={**headers, "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            d = json.loads(resp.read().decode())
            print(f"✅ MR !{d['iid']}: {d['web_url']}")
            break
    except urllib.error.HTTPError as e:
        print(f"Attempt {attempt+1}: HTTP {e.code}: {e.read().decode()[:200]}")
    except Exception as e:
        print(f"Attempt {attempt+1}: {e}")
    time.sleep(15)
