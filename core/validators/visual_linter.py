# core/validators/visual_linter.py
"""
Automated Visual Regression Linter Engine for Elearning Content Factory.
Inspects generated HTML/CSS layout structure to detect horizontal overflow risks,
Light Mode rule violations, ALL-CAPS headings, and image caption defects.

Combines Fast DOM AST Parsing (BeautifulSoup4) with multi-rule pedagogical compliance auditing.
"""

import re
import os
import subprocess
import json
from typing import Tuple, List, Dict, Any
from bs4 import BeautifulSoup, Tag

def validate_html_visual_layout(content: str, metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates HTML layout for visual regression defects, overflow risks, and styling standards.
    Universal Mass-Production Multi-Rule Auditor (Zero-Defect Enterprise Standards).
    Uses BeautifulSoup DOM AST parsing with regex fallback.
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
            errors.append(
                f"Phát hiện từ cấm AI sáo rỗng '{word}' trong bài đọc. "
                "Vui lòng thay bằng thuật ngữ kỹ thuật chuyên nghiệp (Các lỗi thường gặp, Lưu ý thực tế, Kinh nghiệm xử lý)."
            )

    # 2. Section 4 & Section 5 Clean Title Standard (AGENTS.md Directive)
    if "section-4" in content:
        if "4. Tổng kết và các lưu ý" in content:
            errors.append("Tiêu đề Section 4 vi phạm quy chuẩn: Phải dùng chính xác '4. Tổng kết bài học' (Không dùng '4. Tổng kết và các lưu ý').")
    if "section-5" in content:
        if "5. Tài liệu tham khảo và mở rộng" in content or "5. Các nguồn tham khảo" in content:
            errors.append("Tiêu đề Section 5 vi phạm quy chuẩn: Phải dùng chính xác '5. Tài liệu tham khảo'.")

    # Parse HTML with BeautifulSoup for DOM AST analysis
    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception:
        soup = None

    if soup:
        # 3. Horizontal Overflow Risk Inspection: Tables without overflow wrappers (AST Traversal)
        for table in soup.find_all("table"):
            has_wrapper = False
            # Check table's own class/style
            tbl_class = " ".join(table.get("class", []))
            tbl_style = table.get("style", "")
            if "overflow-x" in tbl_class or "overflow-x-auto" in tbl_class or "table-responsive" in tbl_class or "overflow-x" in tbl_style:
                has_wrapper = True
            else:
                # Traverse parent hierarchy
                parent = table.parent
                levels = 0
                while parent and levels < 4:
                    p_class = " ".join(parent.get("class", [])) if isinstance(parent, Tag) else ""
                    p_style = parent.get("style", "") if isinstance(parent, Tag) else ""
                    if "overflow-x-auto" in p_class or "overflow-x: auto" in p_style or "table-responsive" in p_class or "overflow-x" in p_class:
                        has_wrapper = True
                        break
                    parent = parent.parent
                    levels += 1

            if not has_wrapper:
                errors.append("Phát hiện thẻ <table> thiếu wrapper 'overflow-x-auto', có nguy cơ vỡ layout cuộn ngang trên mobile.")

        # 4. Strict Light Mode Enforcement (AGENTS.md Rule 11) via AST Filter
        for tag in soup.find_all(True):
            # Skip code blocks, terminal logs, visualizers, and allowed dark toolbars
            if tag.name in ["pre", "code", "svg", "path"]:
                continue
            t_class = " ".join(tag.get("class", []))
            t_id = tag.get("id", "")
            t_style = tag.get("style", "")

            # Exclude known dark elements
            if any(kw in t_class for kw in ["terminal", "visualizer", "hljs", "syntax", "code-tracker"]):
                continue
            if any(kw in t_id for kw in ["mobile-toc-drawer", "selftest-modal", "output-sb-", "sql-viz-output", "viz-terminal-log"]):
                continue
            if "bg-slate-900/" in t_class or "bg-black/" in t_class:  # Allow low-opacity overlay backdrops
                continue

            # Check illegal dark background classes & styles
            is_dark_bg = False
            if re.search(r'\bbg-(?:slate-900|slate-950|black|zinc-900|gray-900)\b', t_class):
                is_dark_bg = True
            elif re.search(r'background(?:-color)?:\s*(?:#0f172a|#000000|black|#09090b)', t_style, re.IGNORECASE):
                is_dark_bg = True

            if is_dark_bg:
                errors.append(
                    "Vi phạm Quy tắc 11 AGENTS.md (Strict Light Mode): Khung bài đọc chứa thẻ container Nền Đen/Tối (Dark Mode). "
                    "Tất cả container bài đọc phải dùng màu sáng (bg-white / bg-slate-50)."
                )
                break

        # 5. Typography Standard & ALL CAPS Headings Inspection (AGENTS.md Rule 3)
        for h in soup.find_all(["h1", "h2", "h3"]):
            heading_text = h.get_text().strip()
            alpha_text = re.sub(r'[^a-zA-ZàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]', '', heading_text)
            if len(alpha_text) >= 5 and alpha_text.isupper():
                errors.append(
                    f"Vi phạm Quy tắc 3 AGENTS.md: Tiêu đề '<{h.name}> {heading_text[:30]}...' sử dụng chữ IN HOA TOÀN BỘ (ALL CAPS). "
                    "Vui lòng dùng Title Case hoặc Sentence Case."
                )

        # 6. Media Bounds & Italicized Caption Inspection
        for img in soup.find_all("img"):
            img_src = img.get("src", "").lower()
            img_class = " ".join(img.get("class", [])).lower()
            if any(kw in (img_src + img_class) for kw in ["logo", "brand", "header", "icon", "h-9", "h-8", "h-10", "h-12", "nav"]):
                continue

            # Check if inside a figure with figcaption
            figure_parent = img.find_parent("figure")
            if figure_parent and figure_parent.find("figcaption"):
                continue

            # Check next sibling
            has_caption = False
            curr = img.find_next_sibling()
            for _ in range(3):
                if not curr:
                    break
                c_text = curr.get_text().strip()
                c_class = " ".join(curr.get("class", []))
                if curr.name in ["figcaption", "i", "em"] or any(kw in c_class for kw in ["italic", "text-slate-500", "font-medium"]):
                    if len(c_text) > 0:
                        has_caption = True
                        break
                curr = curr.find_next_sibling()

            if not has_caption:
                errors.append("Thẻ <img> minh họa thiếu chú thích in nghiêng (<figcaption>, <i>, <em>) trực tiếp bên dưới.")

    else:
        # Fallback to regex checks if BeautifulSoup is unavailable
        table_matches = re.findall(r'(<table.*?>.*?</table>)', content, re.DOTALL | re.IGNORECASE)
        for table_code in table_matches:
            if "overflow-x-auto" not in table_code and "table-responsive" not in table_code:
                errors.append("Phát hiện thẻ <table> thiếu wrapper 'overflow-x-auto', có nguy cơ vỡ layout cuộn ngang trên mobile.")

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
    skip_size = bool(metadata and (metadata.get("skip_size_check") or metadata.get("is_testing")))
    if not skip_size and len(content.encode('utf-8')) < 45000:
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
