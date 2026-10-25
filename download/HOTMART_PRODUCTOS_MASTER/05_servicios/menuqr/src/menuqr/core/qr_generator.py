"""MenuQR Pro — QR code generator."""
from __future__ import annotations
import io
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from pathlib import Path
from menuqr.core.config import get_settings


def generate_qr(url: str, output_path: str | Path = None, color: str = "#000000", bg_color: str = "#FFFFFF") -> Path | bytes:
    """Generate a QR code for a URL.

    If output_path is None, returns bytes. Otherwise saves to file.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% recovery
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Try styled (rounded modules), fall back to standard
    try:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color=color,
            back_color=bg_color,
        )
    except Exception:
        img = qr.make_image(fill_color=color, back_color=bg_color)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(out))
        return out
    else:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


def generate_table_qr(table_id: str, base_url: str = None) -> Path | bytes:
    """Generate a QR code that points to the digital menu for a specific table."""
    s = get_settings()
    base = base_url or s.qr_base_url
    url = f"{base}/m/{table_id}"
    return generate_qr(url, color=s.qr_color, bg_color=s.qr_bg_color)


def generate_menu_qr(menu_id: str = "default", base_url: str = None) -> Path | bytes:
    """Generate a QR code for the general menu."""
    s = get_settings()
    base = base_url or s.qr_base_url
    url = f"{base}/menu/{menu_id}"
    return generate_qr(url, color=s.qr_color, bg_color=s.qr_bg_color)
