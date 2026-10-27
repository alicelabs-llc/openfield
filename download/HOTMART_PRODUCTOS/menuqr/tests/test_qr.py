"""Tests for QR generator."""
from pathlib import Path
import pytest
from menuqr.core.qr_generator import generate_qr, generate_table_qr


def test_generate_qr_returns_bytes():
    """Test QR generation returns PNG bytes."""
    img_bytes = generate_qr("https://example.com/menu")
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 100
    # PNG signature
    assert img_bytes[:8] == b'\x89PNG\r\n\x1a\n'


def test_generate_qr_saves_to_file(tmp_path):
    """Test QR generation saves to file."""
    out = tmp_path / "qr.png"
    result = generate_qr("https://example.com", output_path=out)
    assert out.exists()
    assert out.stat().st_size > 100


def test_generate_table_qr():
    img_bytes = generate_table_qr("TBL-12345678")
    assert isinstance(img_bytes, bytes)
    assert img_bytes[:8] == b'\x89PNG\r\n\x1a\n'


def test_qr_with_custom_colors():
    img_bytes = generate_qr("https://example.com", color="#FF0000", bg_color="#FFFFFF")
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 100
