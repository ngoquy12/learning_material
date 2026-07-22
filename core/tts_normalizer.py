"""
core/tts_normalizer.py

Bộ Lọc Phiên Âm Thuật Ngữ Tiếng Anh Chuyên Ngành Cho TTS Tiếng Việt
=====================================================================
Chuẩn hóa phiên âm các thuật ngữ kỹ thuật (Python, IDE, CLI, Web Framework)
trước khi gửi sang engine TTS tiếng Việt (Edge-TTS / Kokoro / gTTS).

Nguyên tắc:
- Chuyển đổi thuật ngữ tiếng Anh thành chuỗi phiên âm tiếng Việt tự nhiên.
- Giữ nguyên các từ tiếng Việt.
- Ưu tiên match cụm từ dài trước (longest match first).
- Case-insensitive matching.
"""

from __future__ import annotations

import re
from typing import Dict


# ── Bảng Phiên Âm Thuật Ngữ Kỹ Thuật ─────────────────────────────────────────
# Sắp xếp theo thứ tự cụm từ dài → ngắn để longest-match-first

PHONETIC_MAP: Dict[str, str] = {
    # ── IDE & Editor ──
    "Visual Studio Code": "Vi-du-ồ Xtiu-đi-ô Cốt",
    "VS Code": "Vi-Ét-S Cốt",
    "IntelliJ IDEA": "In-te-li-gi Ai-đi-a",
    "PyCharm": "Pai-chăm",
    "Jupyter Notebook": "Giu-pi-tờ Nốt-bút",
    "Command Palette": "Cồm-man Pa-lét",

    # ── Python Core ──
    "python -m venv": "pai-thần trừ m vi-en-vờ",
    "python -m pip": "pai-thần trừ m pip",
    "python --version": "pai-thần phiên bản",
    "pip install": "píp in-xtồ",
    "pip freeze": "píp phờ-ri-zờ",
    "requirements.txt": "ri-quai-mần chấm tê-ích-tì",
    "Virtual Environment": "vơ-chiu-ồ en-vai-rần-mần",
    "Virtualenv": "vơ-chiu-ồ-en-vờ",
    "Python Interpreter": "Pai-thần In-tơ-prê-tờ",
    "Python": "Pai-thần",
    "interpreter": "in-tơ-prê-tờ",

    # ── Phím tắt ──
    "Ctrl+Shift+P": "phím Cồn-trồ Sịp Pì",
    "Ctrl+Shift+X": "phím Cồn-trồ Sịp Ích",
    "Ctrl+Shift+`": "phím Cồn-trồ Sịp bách-tíc",

    # ── CLI & Terminal ──
    "PowerShell": "Pao-ờ Seo",
    "Terminal": "Tơ-mi-nồ",
    "Command Prompt": "Cồm-man Prôm",
    "command line": "cồm-man lai-nờ",
    "activate": "ắc-ti-vết",
    ".venv": "chấm vi-en-vờ",
    "venv": "vi-en-vờ",

    # ── Biến môi trường ──
    "PATH": "pát-th",
    "Add to PATH": "ét tu pát-th",
    "Add python.exe to PATH": "ét pai-thần chấm ê-xờ tu pát-th",
    "environment variable": "en-vai-rần-mần ve-ri-ờ-bồ",
    "env": "en-vờ",

    # ── Extension & Plugin ──
    "Extension": "ếch-sten-sần",
    "extension": "ếch-sten-sần",
    "Extensions Marketplace": "ếch-sten-sần ma-kịt-plây-xờ",
    "Select Interpreter": "se-léc in-tơ-prê-tờ",

    # ── Web Framework ──
    "FastAPI": "Phát-Ây-Pi-Ai",
    "uvicorn": "iu-vi-coóc-nờ",
    "endpoint": "en-poin",
    "router": "rao-tờ",
    "middleware": "mi-đờ-oe",
    "request": "ri-quýét",
    "response": "ri-s-pôn-xờ",
    "REST API": "rét Ây-Pi-Ai",
    "API": "Ây-Pi-Ai",
    "HTTP": "ết-ti-ti-pi",
    "HTTPS": "ết-ti-ti-pi-ết",
    "JSON": "giây-xonn",
    "CRUD": "cờ-rắp",
    "ORM": "Ô-a-em",
    "SQLAlchemy": "ét-kiu-eo ôn-kơ-mi",
    "Pydantic": "pai-đan-tíc",
    "BaseModel": "bây-xờ mô-đồ",
    "localhost": "lô-cờ-hốt",

    # ── Git & Version Control ──
    "GitHub": "gít-hấp",
    "repository": "ri-pô-zi-tô-ri",
    "commit": "cồm-mít",
    "push": "pút-sờ",
    "pull": "pun",
    "clone": "cơ-lôn",
    "branch": "bơ-ran-chờ",

    # ── Data Types & Syntax ──
    "string": "x-tring",
    "integer": "in-tờ-giờ",
    "boolean": "bu-li-ần",
    "float": "phờ-lốt",
    "list": "lít",
    "dictionary": "đíc-shần-ne-ri",
    "tuple": "tu-pồ",
    "set": "xét",
    "None": "nần",
    "True": "tru",
    "False": "phôn-xờ",
    "def": "đép",
    "class": "cờ-lát",
    "import": "im-po",
    "return": "ri-tơn",
    "print": "prin",
    "input": "in-pút",
    "lambda": "lam-đa",
    "async": "ây-xình",
    "await": "ơ-uết",

    # ── File Extensions ──
    ".py": "chấm pai",
    ".html": "chấm ết-ti-em-eo",
    ".css": "chấm xi-ét-ét",
    ".js": "chấm giây-ét",
    ".json": "chấm giây-xonn",
    ".md": "chấm em-đi",
    ".env": "chấm en-vờ",

    # ── Misc ──
    "framework": "phờ-rêm-guốc",
    "library": "lai-brơ-ri",
    "package": "péc-kít-giờ",
    "module": "mô-đun",
    "syntax": "xin-tắc",
    "debug": "đi-bấc",
    "runtime": "ran-thăm",
    "localhost:8000": "lô-cờ-hốt hai-chấm tám-nghìn",
    "decorator": "đe-cờ-rây-tờ",
    "dependency": "đì-pen-đần-xi",
    "dependencies": "đì-pen-đần-xi-zờ",
    "server": "xơ-vờ",
    "client": "cờ-lai-ần",
    "database": "đây-tờ-bây-xờ",
    "schema": "xơ-ki-ma",
    "migration": "mai-grây-sần",
    "deployment": "đi-ploi-mần",
    "Docker": "Đốc-cờ",
    "container": "cần-tây-nờ",
}

# Pre-sort by length descending for longest-match-first
_SORTED_TERMS = sorted(PHONETIC_MAP.keys(), key=len, reverse=True)


def normalize_tts_text(text: str) -> str:
    """
    Chuẩn hóa phiên âm thuật ngữ tiếng Anh trong văn bản tiếng Việt
    trước khi gửi sang engine TTS.

    Args:
        text: Văn bản narration gốc chứa lẫn tiếng Việt và tiếng Anh.

    Returns:
        Văn bản đã được phiên âm hóa, sẵn sàng cho TTS.
    """
    if not text:
        return text

    result = text
    for term in _SORTED_TERMS:
        # Case-insensitive replacement, preserve surrounding whitespace
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        result = pattern.sub(PHONETIC_MAP[term], result)

    return result
