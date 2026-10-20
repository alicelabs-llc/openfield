"""Generate simple PNG icons for the Agent Bridge extension."""
import struct
import zlib

def create_png(width, height, pixels):
    """Create a PNG file from RGBA pixel data."""
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xffffffff)
        return struct.pack(">I", len(data)) + c + crc

    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'
    # IHDR
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # 8bit RGBA
    # IDAT - row data with filter byte
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter: none
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            raw += struct.pack("BBBB", r, g, b, a)
    compressed = zlib.compress(raw)
    # IEND
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')

def make_icon(size):
    """Create a robot/bridge icon: dark bg with green accent."""
    pixels = []
    for y in range(size):
        for x in range(size):
            # Background: dark
            r, g, b, a = 15, 15, 15, 255
            # Draw a simple "bridge" / "agent" shape
            cx, cy = size // 2, size // 2
            # Head: rounded rectangle (top half)
            head_top = int(size * 0.2)
            head_bot = int(size * 0.55)
            head_left = int(size * 0.25)
            head_right = int(size * 0.75)
            if head_top <= y <= head_bot and head_left <= x <= head_right:
                # Green head
                r, g, b = 0, 255, 136
                # Eyes (dark dots)
                eye_y = (head_top + head_bot) // 2
                eye_size = max(1, size // 16)
                left_eye_x = int(size * 0.38)
                right_eye_x = int(size * 0.62)
                if (eye_y - eye_size <= y <= eye_y + eye_size and
                    (abs(x - left_eye_x) <= eye_size or abs(x - right_eye_x) <= eye_size)):
                    r, g, b = 15, 15, 15
            # Antenna
            ant_top = int(size * 0.05)
            if ant_top <= y <= head_top and abs(x - cx) <= max(1, size // 32):
                r, g, b = 0, 255, 136
            if y < ant_top and abs(x - cx) <= max(2, size // 8):
                r, g, b = 0, 255, 136
            # Body: rounded rect (bottom half)
            body_top = int(size * 0.6)
            body_bot = int(size * 0.85)
            body_left = int(size * 0.15)
            body_right = int(size * 0.85)
            if body_top <= y <= body_bot and body_left <= x <= body_right:
                r, g, b = 0, 200, 110
            # Bridge lines (3 horizontal lines representing connection)
            bridge_y_start = int(size * 0.88)
            bridge_y_end = int(size * 0.95)
            if bridge_y_start <= y <= bridge_y_end:
                if (size * 0.1) <= x <= (size * 0.9):
                    r, g, b = 0, 255, 136
            pixels.append((r, g, b, a))
    return create_png(size, size, pixels)

for size in [16, 48, 128]:
    png_data = make_icon(size)
    with open(f"/home/z/my-project/agent-bridge/icons/icon{size}.png", "wb") as f:
        f.write(png_data)
    print(f"icon{size}.png: {len(png_data)} bytes")
