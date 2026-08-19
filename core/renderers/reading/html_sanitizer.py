"""
core/renderers/reading/html_sanitizer.py
HTML sanitizers, typography cleaners, reference validators, and deep-link generators.
"""

import re
from typing import Dict, Any, List
from core.renderers.reading.markdown_parser import slugify_id, convert_markdown_to_html

CANONICAL_DOC_LINKS = {
    "python": [
        {"title": "Trang chủ Tài liệu Chính thức Python 3", "url": "https://docs.python.org/3/"},
        {"title": "Hướng dẫn Cú pháp và Kiểu dữ liệu Python (MDN)", "url": "https://developer.mozilla.org/en-US/docs/Glossary/Python"}
    ],
    "javascript": [
        {"title": "Tài liệu Lập trình JavaScript (MDN Web Docs)", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"}
    ],
    "sql": [
        {"title": "Hướng dẫn Cú pháp SQL Chuẩn (W3Schools)", "url": "https://www.w3schools.com/sql/"}
    ],
    "c": [
        {"title": "Tài liệu Ngôn ngữ Lập trình C (cppreference)", "url": "https://en.cppreference.com/w/c"}
    ],
    "cpp": [
        {"title": "Tài liệu Ngôn ngữ C++ (cppreference)", "url": "https://en.cppreference.com/w/cpp"}
    ],
    "java": [
        {"title": "Tài liệu Ngôn ngữ Java (Oracle)", "url": "https://docs.oracle.com/en/java/"}
    ]
}

FORBIDDEN_INTRO_CONCEPTS = [
    ("try-except", ["try:", "except ", "except:", "raise "]),
    ("OOP / Class", ["class ", "__init__", "self."]),
    ("Advanced Decorator", ["@staticmethod", "@classmethod", "@property"]),
    ("Async / Concurrency", ["async def", "await ", "asyncio"]),
    ("Lambda / Functional", ["lambda ", "map(", "filter("]),
]

def validate_scope_boundary(html_content: str, is_intro_lesson: bool = True) -> List[str]:
    """Check if introductory HTML content violates scope boundary by using advanced concepts."""
    if not html_content or not is_intro_lesson:
        return []
    violations = []
    for concept, keywords in FORBIDDEN_INTRO_CONCEPTS:
        for kw in keywords:
            if kw in html_content:
                violations.append(f"Scope Violation: Concept '{concept}' ('{kw}') found in introductory reading.")
                break
    return violations

def sanitize_llm_json_text(raw_text: str) -> str:
    """Pre-sanitize raw LLM response to remove invalid control chars before JSON parsing."""
    if not raw_text:
        return ""
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw_text)

def sanitize_references(refs: List[Dict[str, str]], tech_stack: str) -> List[Dict[str, str]]:
    """Sanitize reference links, replacing hallucinated or empty URLs with canonical official docs."""
    valid_refs = []
    if isinstance(refs, list):
        for r in refs:
            if isinstance(r, dict):
                url = (r.get("url") or "").strip()
                title = (r.get("title") or "").strip()
                if url.startswith("http://") or url.startswith("https://"):
                    valid_refs.append({"title": title or url, "url": url})

    if not valid_refs:
        if not tech_stack or not str(tech_stack).strip():
            raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] sanitize_references: 'tech_stack' bị trống.")
        tech_key = str(tech_stack).lower().strip()
        for k, links in CANONICAL_DOC_LINKS.items():
            if k in tech_key:
                return links
        return [{"title": f"Tài liệu chính thức {tech_stack}", "url": f"https://www.google.com/search?q={tech_stack}+official+documentation"}]
    return valid_refs

def sanitize_html_tags_and_italics(html_str: str) -> str:
    """Sanitize HTML string to eliminate unclosed/broken tags and prevent italic text leakage."""
    if not html_str:
        return ""
    c = html_str

    c = re.sub(r'<(?:i|em|span|div|p|h[1-6])\b[^>]*?class\s*=\s*(?:["\'][^"\'>]*$|[^>]*$)', '', c, flags=re.MULTILINE | re.IGNORECASE)
    c = re.sub(r'<i\s+class=[^>]*?(?=<h[1-6]|<p|<div|<ul|<li|<pre|$)', '', c, flags=re.IGNORECASE)

    def normalize_icon_to_span(m):
        attrs = m.group(1).strip()
        body = m.group(2)
        if "ph-" in attrs or "ph " in attrs or "ph\b" in attrs:
            return f'<span {attrs}>{body}</span>'
        return body
    c = re.sub(r'<i\b([^>]*)>(.*?)</i>', normalize_icon_to_span, c, flags=re.DOTALL | re.IGNORECASE)

    c = re.sub(r'<(?:i|em)\b[^>]*/>', '', c, flags=re.IGNORECASE)
    c = re.sub(r'<(?:i|em)\b[^>]*>', '', c, flags=re.IGNORECASE)
    c = re.sub(r'</(?:i|em)>', '', c, flags=re.IGNORECASE)

    parts = re.split(r'(<pre\b.*?</pre>|<code\b.*?</code>)', c, flags=re.DOTALL | re.IGNORECASE)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'</?em\b[^>]*>', '', parts[i], flags=re.IGNORECASE)
    c = "".join(parts)

    return c

def inject_subheading_ids(html_content: str) -> str:
    """Auto-inject IDs into <h3> subheadings for deep linking & strip stray '>' characters."""
    if not html_content: return ""
    html_content = re.sub(r'(<h[234]\b[^>]*>)\s*(?:&gt;|>)\s*', r'\1', html_content)
    def add_id(m):
        tag_open, h3_title = m.group(1), m.group(2)
        clean_title = re.sub(r'^(?:&gt;|>)\s*', '', h3_title).strip()
        if 'id=' in tag_open:
            return f'{tag_open}{clean_title}</h3>'
        sub_id = slugify_id(clean_title)
        return f'<h3 id="{sub_id}" class="font-montserrat font-bold text-xl text-slate-900 mb-3">{clean_title}</h3>'
    return re.sub(r'(<h3\b[^>]*>)(.*?)</h3>', add_id, html_content, flags=re.DOTALL)

def clean_stray_chars(html_str: str) -> str:
    """Cleans unwanted classes, dark styling, AI clichés, and formatting artifacts."""
    if not html_str: return ""
    c = re.sub(r'\bdark:[a-zA-Z0-9_/-]+\b', '', html_str)
    c = re.sub(r'\bvô cùng\b', 'cực kỳ', c, flags=re.IGNORECASE)
    c = re.sub(r'\btuyệt vời\b', 'hiệu quả', c, flags=re.IGNORECASE)
    c = re.sub(r'\bbậc nhất\b', 'hàng đầu', c, flags=re.IGNORECASE)
    c = re.sub(r'\bbí kíp\b', 'quy tắc', c, flags=re.IGNORECASE)
    c = re.sub(r'\b(text-slate-100|text-slate-200|text-slate-300|text-slate-400|text-white)\b', 'text-slate-700', c)

    def deduplicate_class_attributes(m):
        tag_name = m.group(1)
        full_tag = m.group(0)
        classes = re.findall(r'class=["\']([^"\']*)["\']', full_tag)
        merged = " ".join(classes).strip()
        tag_without_classes = re.sub(r'\s*class=["\'][^"\']*["\']', '', full_tag)
        tag_open = tag_without_classes[:-1].rstrip()
        return f'{tag_open} class="{merged}">'
    c = re.sub(r'<(h[1-6]|div|p|span|button|section)\b[^>]*\bclass=["\'][^"\']*["\'][^>]*\bclass=["\'][^"\']*["\'][^>]*>', deduplicate_class_attributes, c, flags=re.IGNORECASE)

    c = re.sub(r'(<h[1-6]\b[^>]*>)\s*(?:&gt;|>|\|)+\s*', r'\1', c)
    c = re.sub(r'(<p\b[^>]*>)\s*(?:&gt;|>|\|)+\s*', r'\1', c)
    c = re.sub(r'(<li\b[^>]*>)\s*(?:&gt;|>|\|)+\s*', r'\1', c)
    c = re.sub(r'(^|\n|>)\s*(?:&gt;|>|\|)+\s*(?=[A-Za-z0-90-9ĐđÀ-ỹ])', r'\1', c)
    c = re.sub(r'(</(?:p|div|section|li|h[1-6])>)\s*\|\s*', r'\1', c)
    c = re.sub(r'(^|\n)\s*\|\s*($|\n)', r'\1\2', c)
    c = re.sub(r'<script\b[^>]*>(?:(?!</script>).)*$', '', c, flags=re.DOTALL)
    c = re.sub(r'<script\b[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    c = sanitize_html_tags_and_italics(c)

    c = re.sub(r'id="mem-(?:total[_-]?sum|tong)"', 'id="viz-var-sum"', c)
    c = re.sub(r'id="mem-(?:number|bien[_-]?lap|counter|so)"', 'id="viz-var-number"', c)
    c = re.sub(r'id="viz-console-out(?:put)?"', 'id="viz-console"', c)
    c = re.sub(r'(id="viz-console"[^>]*class="[^"]*)\bbg-slate-900\b([^"]*")', r'\1bg-slate-100 border border-slate-200 text-emerald-800\2', c)
    c = re.sub(r'(id="viz-console"[^>]*class="[^"]*)\btext-emerald-400\b([^"]*")', r'\1text-emerald-800 font-semibold\2', c)
    c = re.sub(r'class="([^"]*)\bbg-slate-900\b([^"]*viz-console[^"]*)"', r'class="\1bg-slate-100 border border-slate-200 text-emerald-800\2"', c)

    c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizAutoRun|vizAutoStart|vizStartAuto|vizRunAuto|autoRun|autoPlay|toggleAuto|vizTogglePlay|vizPlay)\s*\(\s*\)"', 'onclick="vizToggleAuto()"', c, flags=re.IGNORECASE)
    c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizStepNext|vizNextStep|vizNext|vizStepForward|vizForward|stepNext|nextStep|vizStep|vizStart|vizRun)\s*\(\s*\)"', 'onclick="runVizStep(1)"', c, flags=re.IGNORECASE)
    c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizStepPrev|vizPrevStep|vizPrev|vizStepBackward|vizBackward|stepPrev|prevStep)\s*\(\s*\)"', 'onclick="runVizStep(-1)"', c, flags=re.IGNORECASE)
    c = re.sub(r'onclick="(?:\s*javascript:)?\s*(?:vizReset|vizRestart|resetVisualizer|resetViz)\s*\(\s*\)"', 'onclick="runVizStep(-999)"', c, flags=re.IGNORECASE)

    c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Lùi lại|Quay lại|Trở về)\s*</button>', r'\1 onclick="runVizStep(-1)">Lùi lại</button>', c, flags=re.IGNORECASE)
    c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Tiếp theo|Kế tiếp|Chạy tiếp)\s*</button>', r'\1 onclick="runVizStep(1)">Tiếp theo</button>', c, flags=re.IGNORECASE)
    c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Tự động chạy|Auto Play)\s*</button>', r'\1 onclick="vizToggleAuto()">Tự động chạy</button>', c, flags=re.IGNORECASE)
    c = re.sub(r'(<button\b(?![^>]*onclick=)[^>]*>)\s*(?:Thử lại|Đặt lại|Reset)\s*</button>', r'\1 onclick="runVizStep(-999)">Thử lại</button>', c, flags=re.IGNORECASE)

    c = re.sub(r'\bitalic\b', '', c)
    c = re.sub(r'(?:Sơ đồ 2D flat vector minh họa|Hình ảnh 2D flat vector minh họa|Minh họa 2D flat vector|Sơ đồ 2D|Minh họa 2D|Sơ đồ minh họa)\s*(?:quy trình|ngữ cảnh thực tế cho bài học|cho)?\s*', 'Hình 1.1: Quy trình ', c, flags=re.IGNORECASE)
    c = re.sub(r'class="([^"]*\b(?:bg-\[#[a-fA-F0-9]+\]|bg-emerald-\d+|bg-rose-\d+|bg-blue-\d+|bg-rikkei-\w+|bg-amber-\d+)\b[^"]*)\btext-slate-[678]00\b', r'class="\1text-white', c)

    def wrap_unwrapped_table(m):
        tbl_str = m.group(0)
        if "overflow-x" in tbl_str or "overflow-x-auto" in tbl_str or "table-responsive" in tbl_str:
            return tbl_str
        return f'<div class="overflow-x-auto my-4 rounded-xl border border-slate-200 shadow-sm overflow-hidden">\n{tbl_str}\n</div>'
    c = re.sub(r'<table\b[^>]*>.*?</table>', wrap_unwrapped_table, c, flags=re.DOTALL | re.IGNORECASE)

    c = re.sub(r'(id="[^"]*(?:mech-line|line-)[^"]*"[^>]*>)\s*(?:<span[^>]*>)?\s*(?:\d+\.|\b(?:Dòng|Line)\s*\d+[:.]?)\s*(?:</span>)?\s*', r'\1', c, flags=re.IGNORECASE)

    def sanitize_heading_fonts(m):
        tag_name = m.group(1)
        attrs = m.group(2)
        class_match = re.search(r'class=["\']([^"\']*)["\']', attrs)
        if class_match:
            classes = [cls for cls in class_match.group(1).split() if cls not in ('font-mono', 'font-montserrat', 'font-bold')]
            classes = ['font-montserrat', 'font-bold'] + classes
            clean_attrs = re.sub(r'class=["\'][^"\']*["\']', f'class="{" ".join(classes)}"', attrs)
        else:
            clean_attrs = f'class="font-montserrat font-bold" {attrs}'
        return f'<{tag_name} {clean_attrs}>'
    c = re.sub(r'<(h[1-6])\s+([^>]*)>', sanitize_heading_fonts, c)

    def sanitize_tag_classes(m):
        tag_name = m.group(1)
        attrs = m.group(2)
        clean_attrs = re.sub(r'\b(bg-slate-900|bg-black|bg-slate-800|bg-slate-950|text-white|rounded-full)\b', '', attrs)
        clean_attrs = re.sub(r'\s+', ' ', clean_attrs).strip()
        return f'<{tag_name} {clean_attrs}>'
    c = re.sub(r'<(h[1-6]|p|li|span)\s+([^>]*class="[^"]*"[^>]*)>', sanitize_tag_classes, c)

    c = re.sub(r'<div\s+class="([^"]*)\b(bg-slate-900|bg-black|bg-slate-800)\b([^"]*)"', r'<div class="\1bg-slate-50/50 dark:bg-slate-900/60\3"', c)
    c = re.sub(r'<pre\b[^>]*>\s*(?:<code\b[^>]*>\s*</code>)?\s*</pre>', '', c)
    c = re.sub(r'<div\s+class="[^"]*\b(?:bg-slate-900|bg-black)\b[^"]*">\s*</div>', '', c)
    c = re.sub(r'<div\s+class="[^"]*p-4[^"]*rounded-xl[^"]*"[^>]*>\s*(?:<h[1-6][^>]*>.*?</h[1-6]>\s*)?(<pre\b[^>]*>.*?</pre>)\s*</div>', r'\1', c, flags=re.DOTALL)
    return c

def ensure_html(val: str) -> str:
    """Ensures input value is HTML string, converting markdown if necessary."""
    if not val: return ""
    val_str = str(val).strip()
    if "<p" in val_str or "<ul" in val_str or "<div" in val_str or "<h3" in val_str or "<span" in val_str:
        return val_str
    return convert_markdown_to_html(val_str)

def extract_2tier_toc(know_html: str, ex_text: str, section1_title: str, section2_title: str) -> str:
    """Generate clean 5-section Table of Contents navigation listing strictly main sections 1 to 5."""
    clean_sec1 = re.sub(r'^\s*1\.\s*', '', section1_title).strip()
    clean_sec2 = re.sub(r'^\s*2\.\s*', '', section2_title).strip()
    
    return f"""
    <a href="#section-1" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">1. {clean_sec1}</a>
    <a href="#section-2" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">2. {clean_sec2}</a>
    <a href="#section-3" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">3. Các ví dụ ứng dụng thực tiễn</a>
    <a href="#section-4" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">4. Tổng kết bài học</a>
    <a href="#section-5" class="toc-link pl-4 py-1.5 border-l-2 border-transparent text-slate-600 hover:text-slate-900 font-semibold transition-all">5. Tài liệu tham khảo</a>
    """
