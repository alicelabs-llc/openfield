# 🌿 Touch Grass — Verified Field Notes

> Turn your outdoor photos into a cryptographically verified field journal.
> Photos never leave your machine. The journal cannot be tampered with after signing.

**Hacktoberfest 2026 — DEV Challenge Week 1: Touch Grass**

## What it does

Drop a folder of photos from your hike, walk, or run into `field_notes.py`:

1. **EXIF extraction** — reads GPS coordinates and timestamps from each photo
2. **Vision model** — asks a local Gemma 3n model (via Ollama) what it sees in each photo
3. **Cryptographic sealing** — seals the field notes + GPS trail into an `.aleth` container (Ed25519-signed, hash-linked DAG)
4. **Markdown report** — generates a journal with OpenStreetMap links + verification proof

The result: a one-page trail log you can share, with proof that the notes were not altered after the hike.

## Why open matters

| Concern | How this project addresses it |
|---------|------------------------------|
| **Privacy** | Photos with GPS coordinates never leave your machine. The vision model runs locally via Ollama. No cloud API calls. |
| **Verifiability** | Field notes are sealed in an `.aleth` container signed with Ed25519. Any post-hike tampering invalidates the signature. |
| **Cost** | $0 to run. No API keys, no cloud credits, no subscriptions. |
| **Portability** | The `.aleth` container is a single file you can email, sync, or archive. Anyone with the passphrase can verify it. |
| **Swappability** | Swap Gemma for LLaVA, Moondream, or any open-weight vision model by changing one line in the Ollama call. |

## Quick start

```bash
# Install Ollama (one-time)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3n:4b
ollama serve

# Install Python deps
pip install pillow piexif exifread alethech

# Run on your photos
python3 field_notes.py ./my_hike_photos/ --output journal.md
```

## Demo

```bash
# Create demo photos with EXIF GPS data
python3 src/create_demo_photos.py

# Run the full pipeline
python3 src/run_demo.py
```

Output:
- `output/journal.md` — Markdown report with GPS trail, field notes, and verification proof
- `output/journal.aleth` — Sealed `.aleth` container (Ed25519-signed)

### Demo trail

Parque Metropolitano Guangüiltagua, Quito, Ecuador — 5 photos, ~1h15m hike:

| # | Time | Location | Note |
|---|------|----------|------|
| 1 | 14:30 | -0.1807, -78.4678 | Bamboo grove at trail entrance, Chusquea species |
| 2 | 14:45 | -0.1795, -78.4665 | Rocky stream crossing with moss-covered boulders |
| 3 | 15:10 | -0.1782, -78.4652 | Panoramic vista of the Guayllabamba valley |
| 4 | 15:25 | -0.1775, -78.4640 | Yellow composite flowers (Asteraceae family) |
| 5 | 15:45 | -0.1790, -78.4660 | Mature eucalyptus grove at trail terminus |

## Architecture

```
photos/ ──→ EXIF reader ──→ GPS + timestamps
                ↓
         Ollama (Gemma 3n) ──→ field notes (what the model sees)
                ↓
         alethech .aleth container ──→ Ed25519 signature
                ↓
         Markdown report ──→ OSM links + verification proof
```

## Open-source components

| Component | License | What it does |
|-----------|---------|--------------|
| [alethech](https://github.com/eddyflores100-lang/alethech) | MIT | Cryptographic memory container (Ed25519 + scrypt + AES-256-GCM) |
| [Ollama](https://ollama.com) | MIT | Local inference engine for open-weight models |
| [Gemma 3n](https://ollama.com/library/gemma3n) | Gemma license | Open-weight vision-language model |
| [piexif](https://github.com/hMatoba/Piexif) | MIT | EXIF read/write for JPEG |
| [OpenStreetMap](https://openstreetmap.org) | ODbL | Map links (no API key needed) |

## Verify the demo

```bash
# The .aleth container is verifiable by anyone with the passphrase
alethech verify output/journal.aleth
```

## License

MIT — same as alethech.
