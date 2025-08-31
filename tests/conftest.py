"""Pytest bootstrap to ensure the repository root is importable.
This allows `from app.main import app` to work consistently.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
