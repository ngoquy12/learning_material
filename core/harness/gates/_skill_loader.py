"""Nạp script của skill (skills/*/scripts/*.py) bằng spec_from_file_location, có nhớ đệm."""
from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path
from types import ModuleType

REPO = Path(__file__).resolve().parents[3]


@lru_cache(maxsize=None)
def load_skill_script(skill: str, script: str) -> ModuleType:
    """load_skill_script("slide_deck", "check_deck") -> module của skills/slide_deck/scripts/check_deck.py."""
    path = REPO / "skills" / skill / "scripts" / f"{script}.py"
    spec = importlib.util.spec_from_file_location(f"_harness_{skill}_{script}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
