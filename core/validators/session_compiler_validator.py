"""
core/validators/session_compiler_validator.py
Programmatic Session Compiler Validator.
Validates merged reading_all.html and session_slides.html artifacts for DOM integrity,
ID isolation, sidebar button alignment, and zero JS class/variable redeclaration collisions.
"""

import re
from pathlib import Path
from typing import Tuple, List, Union, Dict, Any
from bs4 import BeautifulSoup
from core.validators.master_validator import register_validator

@register_validator("COMPILED_SESSION", "READING_ALL", "SESSION_SLIDES")
def validate_compiled_session_html(file_or_content: Union[Path, str], metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates compiled merged session HTML (reading_all.html / session_slides.html).
    Returns (is_valid, list_of_errors).
    """
    errors = []
    
    if isinstance(file_or_content, Path):
        if not file_or_content.exists():
            return False, [f"Tệp compiled session HTML không tồn tại: {file_or_content}"]
        with open(file_or_content, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = str(file_or_content)
        
    if not html.strip():
        return False, ["Nội dung compiled session HTML bị trống."]
        
    # 1. Check HTML Parse & DOM Integrity via BeautifulSoup
    try:
        soup = BeautifulSoup(html, "html.parser")
        
        # Check sidebar nav button counts vs content card counts
        nav_btns = soup.find_all(class_=re.compile(r"sidebar-nav-btn"))
        accordion_cards = soup.find_all(class_=re.compile(r"accordion-card|lesson-card"))
        
        if nav_btns and accordion_cards:
            if len(nav_btns) < len(accordion_cards):
                errors.append(f"[Sidebar Alignment] Số nút điều hướng ({len(nav_btns)}) ít hơn số thẻ bài học ({len(accordion_cards)}).")
    except Exception as e:
        errors.append(f"[DOM Integrity Error] Lỗi phân tích cây HTML session: {str(e)}")
        
    # 2. Check for unisolated JS Class redeclarations (Collisions)
    raw_class_matches = re.findall(r'class\s+InteractiveVisualizerEngine\s*\{', html)
    if len(raw_class_matches) > 1:
        errors.append(f"[JS Collision] Phát hiện {len(raw_class_matches)} lớp 'InteractiveVisualizerEngine' chưa được cô lập ID theo lesson.")
        
    # 3. Check for unescaped quotes in script tags causing Unexpected Token
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    for s_idx, script in enumerate(scripts, 1):
        if re.search(r'log\("<[^">]*"[^">]*"\)', script):
            errors.append(f"[Script Linter] Khối Script {s_idx} có lỗi unescaped quote trong chuỗi string literal.")
            
    return len(errors) == 0, errors
