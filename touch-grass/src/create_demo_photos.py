#!/usr/bin/env python3
"""
create_demo_photos.py — Creates demo photos with EXIF GPS data for Touch Grass.

Generates simple nature-themed JPEG images with embedded GPS coordinates
simulating a hike through a park. Used for demo purposes when real photos
are not available.
"""

from PIL import Image, ImageDraw, ImageFont
import piexif
from piexif.helper import UserComment
import struct
import os
from datetime import datetime

def create_photo(filename, width, height, color, label, lat, lon, timestamp):
    """Create a simple photo with EXIF GPS data."""
    img = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), label, fill="white")
    draw.text((10, height - 30), f"{lat}, {lon}", fill="white")

    # Create EXIF data with GPS
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef: "N" if lat >= 0 else "S",
        piexif.GPSIFD.GPSLatitude: _to_rational(abs(lat)),
        piexif.GPSIFD.GPSLongitudeRef: "E" if lon >= 0 else "W",
        piexif.GPSIFD.GPSLongitude: _to_rational(abs(lon)),
    }

    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: timestamp,
    }

    exif_dict = {"GPS": gps_ifd, "Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    img.save(filename, "jpeg", exif=exif_bytes, quality=85)
    print(f"  Created {filename} ({lat}, {lon})")

def _to_rational(decimal):
    """Convert decimal degrees to EXIF rational (d/m/s)."""
    d = int(decimal)
    m_full = (decimal - d) * 60
    m = int(m_full)
    s = round((m_full - m) * 60 * 10000)
    return [(d, 1), (m, 1), (s, 10000)]

# Simulate a hike through Parque Metropolitano Guangüiltagua, Quito, Ecuador
# Lat: -0.1807, Lon: -78.4678
photos = [
    {"name": "trail_start.jpg", "color": (34, 80, 20), "label": "Trail Start — Bamboo Grove",
     "lat": -0.1807, "lon": -78.4678, "time": "2026:10:08 14:30:00"},
    {"name": "stream_crossing.jpg", "color": (20, 60, 80), "label": "Stream Crossing — Rocky Path",
     "lat": -0.1795, "lon": -78.4665, "time": "2026:10:08 14:45:00"},
    {"name": "viewpoint.jpg", "color": (60, 100, 120), "label": "Viewpoint — Panoramic Vista",
     "lat": -0.1782, "lon": -78.4652, "time": "2026:10:08 15:10:00"},
    {"name": "wildflowers.jpg", "color": (80, 40, 20), "label": "Wildflower Meadow — Yellow Composite",
     "lat": -0.1775, "lon": -78.4640, "time": "2026:10:08 15:25:00"},
    {"name": "trail_end.jpg", "color": (40, 30, 10), "label": "Trail End — Eucalyptus Grove",
     "lat": -0.1790, "lon": -78.4660, "time": "2026:10:08 15:45:00"},
]

output_dir = os.path.join(os.path.dirname(__file__), "..", "photos")
os.makedirs(output_dir, exist_ok=True)

print("🌿 Creating demo photos for Touch Grass…")
for p in photos:
    create_photo(
        os.path.join(output_dir, p["name"]),
        800, 600, p["color"], p["label"], p["lat"], p["lon"], p["time"]
    )
print(f"\n✅ Created {len(photos)} demo photos in {output_dir}")
