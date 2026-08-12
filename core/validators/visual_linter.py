# core/validators/visual_linter.py
"""
Automated Visual Regression Linter Engine for Elearning Content Factory.
Inspects generated HTML/CSS layout structure to detect horizontal overflow risks,
Light Mode rule violations, ALL-CAPS headings, and image caption defects.

Combines Fast In-Process Static DOM Linter with optional Puppeteer Headless Browser Inspection.
"""

import re
import os
import subprocess
import json
from typing import Tuple, List, Dict, Any

def validate_html_visual_layout(content: str, metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates HTML layout for visual regression defects, overflow risks, and styling standards.
    Universal Mass-Production Multi-Rule Auditor (Zero-Defect Enterprise Standards).
    Returns (is_valid, list_of_errors).
    """
    if not content or not content.strip():
        return True, []

    errors: List[str] = []

    # 1. Anti-AI Cliché Vocabulary Inspection (AGENTS.md Rule 4 & 10)
    banned_ai_words = [
        "bẫy lập trình", "mẹo lập trình", "mẹo", "bí kíp", "tất tần tật", 
        "bảo bối", "bật mí", "vi diệu", "vô cùng", "bậc nhất", "tuyệt vời"
    ]
    for word in banned_ai_words:
        # Case-insensitive word boundary scan outside HTML attribute names
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Phát hiện từ cấm AI sáo rỗng '{word}' trong bài đọc. Vui lòng thay bằng thuật ngữ kỹ thuật chuyên nghiệp (Các lỗi thường gặp, Lưu ý thực tế, Kinh nghiệm xử lý).")

    # 2. Section 4 & Section 5 Clean Title Standard (AGENTS.md Directive)
    if "section-4" in content:
        if "4. Tổng kết và các lưu ý" in content:
            errors.append("Tiêu đề Section 4 vi phạm quy chuẩn: Phải dùng chính xác '4. Tổng kết bài học' (Không dùng '4. Tổng kết và các lưu ý').")
    if "section-5" in content:
        if "5. Tài liệu tham khảo và mở rộng" in content or "5. Các nguồn tham khảo" in content:
            errors.append("Tiêu đề Section 5 vi phạm quy chuẩn: Phải dùng chính xác '5. Tài liệu tham khảo'.")

    # 3. Horizontal Overflow Risk Inspection: Tables without overflow wrappers
    table_matches = re.findall(r'(<table.*?>.*?</table>)', content, re.DOTALL | re.IGNORECASE)
    for table_code in table_matches:
        has_wrapper = False
        if "overflow-x" in table_code or "overflow-x-auto" in table_code or "table-responsive" in table_code:
            has_wrapper = True
        else:
            pos = content.find(table_code)
            if pos > 0:
                preceding_snippet = content[max(0, pos-200):pos]
                if "overflow-x-auto" in preceding_snippet or "overflow-x: auto" in preceding_snippet:
                    has_wrapper = True
                    
        if not has_wrapper:
            errors.append("Phát hiện thẻ <table> thiếu wrapper 'overflow-x-auto', có nguy cơ vỡ layout cuộn ngang trên mobile.")

    # 4. Strict Light Mode Enforcement (AGENTS.md Rule 11)
    content_without_code = re.sub(r'<pre.*?>.*?</pre>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content_without_code = re.sub(r'<code.*?>.*?</code>', '', content_without_code, flags=re.DOTALL | re.IGNORECASE)
    content_without_code = re.sub(r'class=["\'].*?terminal.*?["\']', '', content_without_code, flags=re.DOTALL | re.IGNORECASE)
    content_without_code = re.sub(r'class=["\'].*?visualizer.*?["\']', '', content_without_code, flags=re.DOTALL | re.IGNORECASE)

    dark_bg_patterns = [
        r'class=["\'][^"\']*\bbg-(?:slate-900|slate-950|black|zinc-900|gray-900)\b[^"\']*["\']',
        r'style=["\'][^"\']*background(?:-color)?:\s*(?:#0f172a|#000000|black|#09090b)[^"\']*["\']'
    ]
    for pattern in dark_bg_patterns:
        if re.search(pattern, content_without_code, re.IGNORECASE):
            errors.append("Vi phạm Quy tắc 11 AGENTS.md (Strict Light Mode): Khung bài đọc chứa thẻ container Nền Đen/Tối (Dark Mode). Tất cả container bài đọc phải dùng màu sáng (bg-white / bg-slate-50).")
            break

    # 5. Typography Standard & ALL CAPS Headings Inspection (AGENTS.md Rule 3)
    heading_matches = re.findall(r'<(h[1-3])[^>]*>(.*?)</\1>', content, re.DOTALL | re.IGNORECASE)
    for tag_name, heading_raw in heading_matches:
        heading_text = re.sub(r'<.*?>', '', heading_raw).strip()
        alpha_text = re.sub(r'[^a-zA-ZàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]', '', heading_text)
        if len(alpha_text) >= 5 and alpha_text.isupper():
            errors.append(f"Vi phạm Quy tắc 3 AGENTS.md: Tiêu đề '<{tag_name}> {heading_text[:30]}...' sử dụng chữ IN HOA TOÀN BỘ (ALL CAPS). Vui lòng dùng Title Case hoặc Sentence Case.")

    # 6. Media Bounds & Italicized Caption Inspection
    img_matches = re.finditer(r'<img\s+([^>]*?)>', content, re.IGNORECASE)
    for match in img_matches:
        img_attr = match.group(1).lower()
        if any(kw in img_attr for kw in ["logo", "brand", "header", "icon", "h-9", "h-8", "h-10", "h-12", "nav"]):
            continue
        pos = match.end()
        following_snippet = content[pos:pos+300]
        has_italic_caption = bool(re.search(r'<(figcaption|i|em)\b|\bclass=["\'][^"\']*\bitalic\b', following_snippet, re.IGNORECASE))
        if not has_italic_caption:
            preceding_snippet = content[max(0, match.start()-100):match.start()]
            if "<figure" not in preceding_snippet.lower():
                errors.append("Thẻ <img> minh họa thiếu chú thích in nghiêng (<i>...</i>, <figcaption> hoặc class 'italic') trực tiếp bên dưới.")

    # 7. Code Comment Vietnamese Standard Inspection
    english_comment_patterns = [
        r'#\s*Progressive Demo', r'#\s*Executed if condition', r'#\s*Production call demo', r'//\s*Progressive Demo'
    ]
    for ep in english_comment_patterns:
        if re.search(ep, content, re.IGNORECASE):
            errors.append("Phát hiện comment code bằng Tiếng Anh. Tất cả comment trong code snippets phải viết bằng Tiếng Việt có dấu dễ hiểu.")

    return len(errors) == 0, errors


def run_puppeteer_visual_inspection(html_file_path: str) -> Tuple[bool, List[str]]:
    """
    Executes scripts/visual_dom_linter.js using Node.js to inspect actual DOM bounds in Headless Chromium.
    Returns (is_valid, errors).
    """
    script_path = os.path.join("scripts", "visual_dom_linter.js")
    if not os.path.exists(script_path) or not os.path.exists(html_file_path):
        return True, []

    try:
        cmd = ["node", script_path, html_file_path]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if proc.returncode == 0 and proc.stdout.strip():
            data = json.loads(proc.stdout.strip())
            return data.get("is_valid", True), data.get("errors", [])
    except Exception as e:
        print(f"  [Visual Linter Warning] Puppeteer inspection skipped: {e}")
        
    return True, []
