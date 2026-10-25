"""Pytest config."""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
os.environ.setdefault("BUSINESS_NAME", "Test Shop")
