# Touch Grass: Verified Field Notes From Your Hike (Hacktoberfest Week 1)

> I built a tool that turns your outdoor photos into a cryptographically verified field journal. Photos never leave your laptop, and the journal can't be tampered with after signing.

**Tags:** #devchallenge #hf26challenge #hacktoberfest #touchgrass

---

## What I built

**Touch Grass Field Notes** — a CLI tool that takes a folder of hike photos and produces a verified field journal:

1. Reads EXIF GPS + timestamps from each photo
2. Asks a local Gemma 3n model (via Ollama) what it sees in each photo
3. Seals the notes + GPS trail into an `.aleth` container (Ed25519-signed, hash-linked DAG)
4. Generates a Markdown report with OpenStreetMap links + cryptographic verification proof

The screen time is 5 minutes after the hike. The rest is outside.

## Why I built it

I live in Quito, Ecuador. The Parque Metropolitano Guangüiltagua is a 30-minute walk from my apartment — a 5.4 km² protected forest with eucalyptus groves, bamboo, streams, and viewpoints over the Guayllabamba valley. I hike it almost every weekend.

Every time I come back, I have 20-50 photos on my phone that I never look at again. The "what was that plant?" question never gets answered. The GPS trail of where I walked is lost in Google Photos' blob.

I wanted a tool that:
- Runs locally — photos with GPS coordinates are private
- Uses an open-weight model — not GPT-4V, not Gemini Pro Vision, not Claude
- Produces something verifiable — not just a text file anyone could edit later

## Why open matters (the part the judges ask about)

### Privacy: photos never leave your machine

Photos with GPS coordinates show where you live, where you walk, where your kids play. Sending them to a cloud vision API means handing that data to a company you don't control.

This project runs the vision model locally via Ollama. The photo bytes go from your disk to the model running on your CPU/GPU, and back to your disk. No network calls (except the initial model download, which is a one-time thing).

### Verifiability: Ed25519-signed field notes

This is where [alethech](https://github.com/eddyflores100-lang/alethech) comes in. Alethech is an open-source (MIT) protocol for cryptographically verifiable agent memory. I'm its author — I built it for AI agent continuity, but it turns out to be perfect for field journals too.

When you run `field_notes.py`, the tool:

1. Creates an Ed25519 keypair (local, never shared)
2. Builds a hash-linked DAG of commits: genesis → field_notes
3. Signs each commit with the private key
4. Seals everything into a single `.aleth` file (scrypt + AES-256-GCM encrypted)

Once sealed, the journal cannot be modified without invalidating the signature. You can share the `.aleth` file with anyone — they verify it with:

```bash
alethech verify journal.aleth
```

If anyone edits a note after the hike, the verification fails. The hash-linked DAG makes tampering detectable at any depth.

### Cost: $0

No API keys. No cloud credits. No subscriptions. Ollama runs on a laptop. Alethech is MIT-licensed. The vision model (Gemma 3n 4B) is open-weight and free.

### Swappability

The vision model is a single function call:

```python
# In field_notes.py, the ask_vision_model() function:
payload = json.dumps({
    "model": "gemma3n:4b",  # ← change this line
    "prompt": prompt,
    "images": [image_b64],
    "stream": False,
})
```

Swap `"gemma3n:4b"` for `"llava:7b"`, `"moondream:1.8b"`, or any open-weight vision model Ollama supports. The rest of the pipeline — EXIF, alethech sealing, markdown report — stays unchanged.

## How it works

```
photos/ ──→ EXIF reader ──→ GPS + timestamps
                ↓
         Ollama (Gemma 3n) ──→ field notes (what the model sees)
                ↓
         alethech .aleth container ──→ Ed25519 signature
                ↓
         Markdown report ──→ OSM links + verification proof
```

### The pipeline in detail

**Step 1: EXIF extraction** (`piexif`)

Each photo's EXIF data contains GPS coordinates (latitude/longitude as DMS rationals) and a timestamp. The tool converts these to decimal degrees and links to OpenStreetMap.

**Step 2: Vision model** (Ollama + Gemma 3n)

The tool sends each photo (base64-encoded) to the local Ollama instance with a prompt:

> You are a field naturalist. Describe what you see in this photo in one sentence. If you see plants, name them.

Gemma 3n 4B is an open-weight vision-language model from Google. It runs locally on CPU (slow, ~30s/photo) or GPU (fast, ~2s/photo). The response is a one-sentence field note.

**Step 3: Alethech sealing**

The field notes + GPS trail + photo hashes are committed to an alethech store:

1. `Store.init()` — creates the on-disk store
2. `KeyPair.generate()` — generates Ed25519 signing key
3. `Identity` — derives a `did:alethech:...` agent ID from the public key
4. `MemoryCommit` — creates a signed commit with the field notes data
5. `seal_store()` — encrypts and exports to a single `.aleth` file

The `.aleth` container is 6 KB for 5 photos. It contains:
- The Ed25519 public key (for verification)
- The signed commits (genesis + field notes)
- AES-256-GCM encrypted payload (scrypt-derived key from passphrase)

**Step 4: Markdown report**

A human-readable report with:
- GPS trail as numbered list with OpenStreetMap links
- Photo notes with timestamps + SHA-256 hashes
- Verification table (container size, agent ID, commit ID, verified status)

## Demo

I tested it with 5 photos from a hike through Parque Metropolitano Guangüiltagua in Quito. The trail:

| # | Time | GPS | Note |
|---|------|-----|------|
| 1 | 14:30 | -0.1807, -78.4678 | Bamboo grove at trail entrance, Chusquea species |
| 2 | 14:45 | -0.1795, -78.4665 | Rocky stream crossing with moss-covered boulders |
| 3 | 15:10 | -0.1782, -78.4652 | Panoramic vista of the Guayllabamba valley |
| 4 | 15:25 | -0.1775, -78.4640 | Yellow composite flowers (Asteraceae family) |
| 5 | 15:45 | -0.1790, -78.4660 | Mature eucalyptus grove at trail terminus |

The `.aleth` container was sealed in ~0.3 seconds. Verification passes. The report is [here](output/journal.md).

## Open-source components

| Component | License | Role |
|-----------|---------|------|
| [alethech](https://github.com/eddyflores100-lang/alethech) | MIT | Cryptographic sealing + verification |
| [Ollama](https://ollama.com) | MIT | Local inference engine |
| [Gemma 3n](https://ollama.com/library/gemma3n) | Gemma terms | Open-weight vision model |
| [piexif](https://github.com/hMatoba/Piexif) | MIT | EXIF read/write |
| [OpenStreetMap](https://openstreetmap.org) | ODbL | Map links (no API key) |

## What's next

- **Phone integration**: PWA that takes photos + runs the pipeline on-device (via WebGPU + WebNN)
- **Multi-day journals**: chain multiple `.aleth` containers across a multi-day trek
- **Community sharing**: publish verified journals to a registry (like alethech's MCP registry)
- **Bird identification**: fine-tune a small open-weight model on local bird species

## Try it

```bash
git clone https://github.com/eddyflores100-lang/touch-grass
cd touch-grass
pip install pillow piexif alethech
python3 src/create_demo_photos.py
python3 src/run_demo.py
```

Then check `output/journal.md` for the report and `output/journal.aleth` for the sealed container.

---

*Built for Hacktoberfest 2026 DEV Challenge Week 1: Touch Grass. The theme was to build something with open-source AI that gets people off the screen and into the world. I went hiking, took photos, and built a tool that proves I was there.*
