"""
core/renderers/lecture/text_sanitizer.py
Text sanitization, title normalization, and icon mapping utilities for Classroom Lecture Presentations.
"""

import re
from typing import Tuple

def sanitize_slide_text(text: str) -> str:
    """
    Enforces pedagogical language rules:
    1. Forbids AI/academic buzzwords ('thách thức kỹ thuật', 'phân tích thực tế', etc.)
    2. Strips hyperbolic words ('nhất', 'quá', 'vô cùng', 'tuyệt vời', 'bậc nhất', 'triệt để', 'khám phá', 'khai phá')
    3. Enforces Sentence Case (capitalizes first letter & proper technical terms, lowercase rest).
    """
    if not text:
        return ""

    buzzwords_map = [
        (r"bối cảnh thực tế\s*&\s*thách thức kỹ thuật", "Bối cảnh dự án & vấn đề cần giải quyết"),
        (r"trực quan hóa luồng kiến trúc\s*&\s*thao tác cốt lõi", "Sơ đồ kiến trúc & quy trình vận hành"),
        (r"quy chuẩn thực thi chuẩn\s*vs\s*anti-pattern", "Lỗi thường gặp & cách xử lý chuẩn"),
        (r"thách thức\s*&\s*bối cảnh thực tế", "Vấn đề thực tế"),
        (r"giải pháp hiện đại chuẩn doanh nghiệp", "Giải pháp áp dụng thực tế"),
        (r"thách thức kỹ thuật", "vấn đề kỹ thuật"),
        (r"bối cảnh\s*&\s*phân tích thực tế", "Bối cảnh & phân tích dự án"),
        (r"chuẩn hóa quy trình kỹ thuật\s*&\s*tự động hóa vận hành doanh nghiệp", "Quy trình vận hành & tự động hóa hệ thống"),
        (r"kiến trúc cốt lõi", "Kiến trúc hệ thống"),
        (r"khai phá", "Tìm hiểu"),
        (r"khám phá", "Tìm hiểu"),
    ]

    for pattern, replacement in buzzwords_map:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    hyperboles = [
        r"\bnhất\b", r"\bquá\b", r"\bvô cùng\b", r"\btuyệt vời\b", r"\bbậc nhất\b", r"\btriệt để\b",
    ]
    for pattern in hyperboles:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    text = re.sub(r"\s+", " ", text).strip()

    proper_tech_terms = {
        "Git", "VCS", "CLI", "Python", "JS", "JavaScript", "TypeScript", "Java", "SQL", "HTML", "CSS",
        "Docker", "Linux", "Windows", "MacOS", "VS", "Code", "WASM", "Pyodide", "API", "REST", "JSON",
        "Anti-Pattern", "Best", "Practice", "Conventional", "Commits", "CI/CD", "RAM", "CPU", "Bento", "Rikkei",
        "Staging", "Area", "Commit", "Log", "Tree", "Working", "Restore", "Branch", "Merge", "Pull", "Push", "Rebase"
    }

    words = text.split()
    if len(words) > 1:
        title_cased_words = sum(1 for w in words if w[0].isupper() and w not in proper_tech_terms)
        if title_cased_words >= len(words) * 0.4:
            res_words = []
            for idx, w in enumerate(words):
                clean_w = re.sub(r"[^\w\-\/]", "", w)
                if idx == 0:
                    res_words.append(w[0].upper() + w[1:].lower())
                elif clean_w in proper_tech_terms or clean_w.isupper():
                    res_words.append(w)
                else:
                    res_words.append(w.lower())
            text = " ".join(res_words)

    if text:
        text = text[0].upper() + text[1:]

    return text

def clean_title_string(text: str) -> str:
    """Clean raw identifier/snake_case titles into synchronized formatted Vietnamese title strings."""
    if not text:
        return ""
    clean = text.strip()
    # Iteratively strip prefixes (e.g. Session 02 - Lesson 01: ...)
    while re.search(r'^\s*(?:Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', clean, flags=re.IGNORECASE):
        clean = re.sub(r'^\s*(?:Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean, flags=re.IGNORECASE).strip()
    
    if '_' in clean and ' ' not in clean:
        words = clean.split('_')
        clean_words = []
        for w in words:
            w_lower = w.lower()
            if w_lower in ['py', 'pvm', 'cli', 'api', 'http', 'crud', 'sql', 'orm', 'json', 'url', 'id', 'vs', 'code', 'wasm', 'git', 'vcs', 'pr', 'ui', 'ux', 'es6', 'v8', 'node', 'js']:
                clean_words.append(w.upper())
            elif w_lower in ['va']:
                clean_words.append("và")
            else:
                clean_words.append(w.capitalize())
        clean = " ".join(clean_words)
        
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def extract_concise_topic_name(title: str) -> str:
    """Extracts a concise, punchy topic name for titles, sidebar pills, and badges without text bloat."""
    clean = clean_title_string(title)
    clean = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean, flags=re.IGNORECASE).strip()
    clean = re.sub(r'^(?:Tìm hiểu|Giới thiệu|Khái niệm về|Khái niệm|Tổng quan về|Câu lệnh|Biểu thức)\s+', '', clean, flags=re.IGNORECASE).strip()
    words = clean.split()
    if len(words) > 7:
        clean = " ".join(words[:7])
    return clean

def get_icon_for_topic(topic: str, tech_stack: str = "") -> str:
    """Dynamically picks a Phosphor icon class based on topic keywords."""
    t_lower = topic.lower()
    if any(k in t_lower for k in ["toán tử", "operator", "tính toán", "biểu thức"]):
        return "ph-calculator"
    if any(k in t_lower for k in ["so sánh", "comparison", "equal", "logic", "boolean"]):
        return "ph-scales"
    if any(k in t_lower for k in ["điều kiện", "rẽ nhánh", "if", "else", "switch"]):
        return "ph-git-fork"
    if any(k in t_lower for k in ["vòng lặp", "loop", "for", "while"]):
        return "ph-arrows-clockwise"
    if any(k in t_lower for k in ["hàm", "function", "scope", "arrow"]):
        return "ph-brackets-curly"
    if any(k in t_lower for k in ["mảng", "array", "list", "danh sách"]):
        return "ph-list-numbers"
    return "ph-code"

def detect_file_info_for_tech_stack(tech_stack: str, lesson_title: str) -> Tuple[str, str]:
    """Detects the appropriate filename and language identifier for any tech stack."""
    ts_lower = (tech_stack or "").lower()
    if "python" in ts_lower:
        return "main.py", "python"
    elif "java" in ts_lower and "javascript" not in ts_lower:
        return "Main.java", "java"
    elif "typescript" in ts_lower or bool(re.search(r'\bts\b', ts_lower)):
        return "app.ts", "typescript"
    elif "javascript" in ts_lower or bool(re.search(r'\bjs\b', ts_lower)) or "es6" in ts_lower:
        return "script.js", "javascript"
    elif "c++" in ts_lower or "cpp" in ts_lower:
        return "main.cpp", "cpp"
    elif "c#" in ts_lower or "csharp" in ts_lower or ".net" in ts_lower:
        return "Program.cs", "csharp"
    elif "sql" in ts_lower or "database" in ts_lower or "cơ sở dữ liệu" in ts_lower:
        return "query.sql", "sql"
    elif "git" in ts_lower or "linux" in ts_lower or "bash" in ts_lower or "docker" in ts_lower or "devops" in ts_lower:
        return "terminal.sh", "bash"
    elif "html" in ts_lower or "css" in ts_lower:
        return "index.html", "html"
    elif "php" in ts_lower:
        return "index.php", "php"
    elif "go" in ts_lower or "golang" in ts_lower:
        return "main.go", "go"
    else:
        return "script.js", "javascript"
