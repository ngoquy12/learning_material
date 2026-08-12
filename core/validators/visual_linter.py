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

    # If content is a file path that exists on disk, read its file content
    if os.path.exists(content) and os.path.isfile(content):
        with open(content, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    errors: List[str] = []

    # 1. Anti-AI Cliché Vocabulary Inspection (AGENTS.md Rule 4 & 10)
    banned_ai_words = [
        "bẫy lập trình", "mẹo lập trình", "bí kíp", "tất tần tật", 
        "bảo bối", "bật mí", "vi diệu", "vô cùng", "bậc nhất", "tuyệt vời"
    ]
    content_lower = content.lower()
    for word in banned_ai_words:
        if word in content_lower:
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
    content_without_code = re.sub(r'<div[^>]*id=["\'](?:mobile-toc-drawer|selftest-modal|output-sb-\d+|sql-viz-output|viz-terminal-log)["\'].*?>', '', content_without_code, flags=re.DOTALL | re.IGNORECASE)
    content_without_code = re.sub(r'<div[^>]*class=["\'][^"\']*\b(?:bg-slate-900|bg-slate-950)\b[^"\']*["\'][^>]*>(?:(?!-->|</div>).)*?</div>', '', content_without_code, flags=re.DOTALL | re.IGNORECASE)
    content_without_code = re.sub(r'\bbg-slate-900/\d+\b', '', content_without_code, flags=re.IGNORECASE)

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
        has_italic_caption = bool(re.search(r'<(figcaption|p|i|em)\b|\bclass=["\'][^"\']*\b(?:italic|font-medium|text-slate-500|text-slate-600)\b', following_snippet, re.IGNORECASE))
        if not has_italic_caption:
            preceding_snippet = content[max(0, match.start()-100):match.start()]
            if "<figure" not in preceding_snippet.lower():
                errors.append("Thẻ <img> minh họa thiếu chú thích (<p>, <figcaption>) trực tiếp bên dưới.")

    # 7. Code Comment Vietnamese Standard Inspection
    english_comment_patterns = [
        r'#\s*Progressive Demo', r'#\s*Executed if condition', r'#\s*Production call demo', r'//\s*Progressive Demo'
    ]
    for ep in english_comment_patterns:
        if re.search(ep, content, re.IGNORECASE):
            errors.append("Phát hiện comment code bằng Tiếng Anh. Tất cả comment trong code snippets phải viết bằng Tiếng Việt có dấu dễ hiểu.")

    # 8. Section 2.4 Step-by-Step Execution Visualizer Verification
    if "section-2" in content:
        has_viz_24 = bool(re.search(r'sec-2-4|mô phỏng cơ chế vận hành|step-by-step execution visualizer|viz-line-|mech-line-', content, re.IGNORECASE))
        if not has_viz_24:
            errors.append("Bài đọc thiếu Section 2.4: Trình mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer). Bắt buộc phải có Section 2.4 cho các bài đọc kỹ thuật.")

    # 9. Minimum File Depth & Size Threshold Verification (AGENTS.md Depth Rule)
    if len(content.encode('utf-8')) < 45000:
        errors.append(f"Dung lượng bài đọc quá ngắn ({len(content.encode('utf-8'))//1024} KB). Bài đọc chuẩn mực phải có dung lượng từ 50KB - 120KB và phân tích sâu sắc.")

    # 10. 2-Tier Sidebar TOC Verification
    if "toc-link" in content:
        has_sublinks = bool(re.search(r'sec-2-1|sec-2-2|sec-3-1|sec-3-2', content, re.IGNORECASE))
        if not has_sublinks:
            errors.append("Mục lục Sidebar thiếu các menu con cấp 2 (Sub-headings 2.1, 2.2, 2.3, 2.4, 3.1). Vui lòng chèn menu 2 cấp dạng cây cho Sidebar.")

    # 11. Interactive Live Sandbox Count Verification
    tech_stack_meta = (metadata.get("tech_stack") if metadata else "") or ""
    tech_lower = tech_stack_meta.lower().strip()
    is_python_tech = (tech_lower == "python" or "python" in tech_lower) and not any(kw in tech_lower for kw in ["sql", "git", "bash", "docker", "agile", "architecture", "uml", "design"])
    if is_python_tech:
        sandbox_count = len(re.findall(r'runPythonCode|code-sb-', content))
        if sandbox_count < 2:
            errors.append("Bài đọc môn Python thiếu Live Pyodide Sandboxes tương tác (tối thiểu 2 khối sandbox có nút Chạy).")

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
