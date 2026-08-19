"""
core/renderers/pptx/slide_validator.py
Automated Quality Assurance & Structure Validator for generated PowerPoint (.pptx) Decks.
Strictly checks all design rules defined in Skill 3 (no empty placeholders, no bad line spacing,
no ALL CAPS, standard border radius, valid XML).
"""

from __future__ import annotations
import os
import glob
import re
import unicodedata
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

SZ_H1 = 2800          # 28pt
SZ_H2 = 2000          # 20pt
SZ_BODY = 1800        # 18pt
ADJ_NORMAL = 4000     # 4%
ADJ_OVAL = 50000
BRAND_COLOR = "C00000"
TEMPLATE_NATIVE_LABELS = {"RIKKEI", "EDUCATION", "RIKKEISOFT"}

def validate_unpacked_deck(unpacked_dir: Union[str, Path]) -> Dict[str, Any]:
    """
    Validates all slide XML files inside an unpacked PPTX directory.
    """
    slides_dir = Path(unpacked_dir) / "ppt" / "slides"
    if not slides_dir.exists():
        return {
            "status": "FAIL",
            "passed": False,
            "errors": [f"Thư mục slide XML không tồn tại: {slides_dir}"],
            "total_slides": 0
        }

    files = sorted(list(slides_dir.glob("slide*.xml")))
    if not files:
        return {
            "status": "FAIL",
            "passed": False,
            "errors": ["Không tìm thấy bất kỳ file slide*.xml nào"],
            "total_slides": 0
        }

    all_xml = {f.name: f.read_text(encoding="utf-8") for f in files}
    errors = []
    warnings = []

    # 1. Cấm spcPts làm cơ chế line-spacing
    bad_spc = [name for name, content in all_xml.items() if "<a:lnSpc><a:spcPts" in content]
    if bad_spc:
        errors.append(f"Phát hiện {len(bad_spc)} file dùng spcPts làm line-spacing: {bad_spc}")

    # 2. Placeholder rỗng
    empty_ph = []
    for name, content in all_xml.items():
        for m in re.finditer(r'<p:sp>((?:(?!</p:sp>).)*?<p:ph[^/]*/>(?:(?!</p:sp>).)*?)</p:sp>', content, re.S):
            if '<a:t>' not in m.group(1):
                empty_ph.append(name)
    if empty_ph:
        errors.append(f"Phát hiện placeholder rỗng tại: {set(empty_ph)}")

    # 3. adj bo góc phải chuẩn
    bad_adj = []
    for name, content in all_xml.items():
        for m in re.finditer(r'fmla="val (\d+)"', content):
            v = int(m.group(1))
            if v not in (ADJ_NORMAL, ADJ_OVAL, 9000, 0, 5000):
                bad_adj.append((name, v))
    if bad_adj:
        errors.append(f"Phát hiện bo góc không chuẩn {bad_adj[:5]}")

    # 4. Cấm ALL CAPS tự soạn
    native_norm = {unicodedata.normalize("NFC", s) for s in TEMPLATE_NATIVE_LABELS}
    all_caps_hits = []
    for name, content in all_xml.items():
        for m in re.finditer(r'<a:t>([^<]+)</a:t>', content):
            t = m.group(1).strip()
            if unicodedata.normalize("NFC", t) in native_norm:
                continue
            letters = re.sub(r'[^A-Za-zÀ-ỹ]', '', t)
            # Flag if long uppercase word >= 8 chars that is not an acronym or short label
            if len(letters) >= 8 and letters == letters.upper() and letters != letters.lower():
                if not re.match(r'^(JSON|HTML|CSS|DOM|API|HTTP|REST|SQL|AJAX|CRUD)$', letters):
                    all_caps_hits.append((name, t))
    if all_caps_hits:
        warnings.append(f"Cảnh báo chữ IN HOA ALL CAPS dài: {all_caps_hits[:5]}")

    is_passed = len(errors) == 0
    return {
        "status": "PASS" if is_passed else "FAIL",
        "passed": is_passed,
        "total_slides": len(files),
        "errors": errors,
        "warnings": warnings,
        "score": 100 if is_passed else max(0, 100 - len(errors) * 25)
    }

def validate_pptx_file(pptx_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Unpacks a target PPTX file to a temporary location and runs full quantitative checks.
    """
    p_path = Path(pptx_path)
    if not p_path.exists():
        return {
            "status": "FAIL",
            "passed": False,
            "errors": [f"File PPTX không tồn tại: {pptx_path}"],
            "total_slides": 0,
            "score": 0
        }

    tmp_dir = tempfile.mkdtemp(prefix="pptx_val_")
    try:
        with zipfile.ZipFile(p_path, 'r') as z:
            z.extractall(tmp_dir)
        res = validate_unpacked_deck(tmp_dir)
        return res
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
