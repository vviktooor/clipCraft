"""English (default) and Polish interface strings. Author: WR"""

import json
import locale
import os
from pathlib import Path

LOCALES = Path(__file__).parent / "locales"
LANGUAGES = ("en", "pl")


def load(lang: str) -> dict:
    return json.loads((LOCALES / f"{lang}.json").read_text(encoding="utf-8"))


def default_language() -> str:
    """APP_LANG wins, then the system language, then English."""
    wanted = os.environ.get("APP_LANG") or (locale.getlocale()[0] or "")
    code = wanted[:2].lower()
    return code if code in LANGUAGES else "en"
