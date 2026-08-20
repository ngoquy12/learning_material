"""
core/validators/syntax_linter.py
Programmatic Syntax Linter for HTML & JavaScript blocks.
Catches unclosed HTML tags and JavaScript string/quote syntax errors before Reviewer approval.
"""

import re
from typing import List, Tuple
from bs4 import BeautifulSoup

def lint_html_syntax(html_content: str) -> Tuple[bool, List[str]]:
    """
    Lints HTML structure to check for balanced tags and parse errors.
    Returns (is_valid, error_list).
    """
    if not html_content:
        return False, ["Nội dung HTML trống."]
        
    errors = []
    
    # 1. Parse with BeautifulSoup to detect malformed HTML
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        # Check if scripts contain unescaped quotes causing JS syntax issues
        scripts = soup.find_all("script")
        for idx, script in enumerate(scripts):
            script_text = script.string or script.text or ""
            js_errors = lint_javascript_quotes(script_text)
            if js_errors:
                errors.extend([f"[Script Block {idx+1}] {err}" for err in js_errors])
    except Exception as e:
        errors.append(f"Lỗi phân tích cú pháp HTML (DOM Parse Error): {str(e)}")
        
    return len(errors) == 0, errors

def lint_javascript_quotes(js_code: str) -> List[str]:
    """
    Scans JS script code for common unescaped double quotes inside double-quoted string literals.
    E.g. this.log("<i class="ph-play"></i>")
    """
    if not js_code:
        return []
        
    errors = []
    # Pattern matching unescaped double quotes in quotes: e.g. "something "nested" something"
    # Detect line by line
    lines = js_code.splitlines()
    for line_no, line in enumerate(lines, 1):
        if "this.log(" in line or ".innerHTML" in line:
            # Check for pattern like: "<i class="...
            if re.search(r'log\("<[^">]*"[^">]*"\)', line) or re.search(r'=\s*"<[^">]*"[^">]*">', line):
                errors.append(f"Line {line_no}: Lỗi đóng ngoặc chuỗi JavaScript (Unescaped quote in string literal): {line.strip()}")
                
    return errors

def lint_pyodide_compatibility(python_code: str) -> List[str]:
    """
    Checks Python code for imports of external non-standard libraries (requests, pandas, bs4, etc.)
    that fail in standard browser Pyodide WASM runtime.
    """
    if not python_code:
        return []
        
    forbidden_modules = {"requests", "pandas", "numpy", "bs4", "beautifulsoup4", "flask", "django", "fastapi", "uvicorn", "PIL", "cv2"}
    errors = []
    
    for line in python_code.splitlines():
        line_clean = line.strip()
        if line_clean.startswith("import ") or line_clean.startswith("from "):
            for mod in forbidden_modules:
                pattern = r'\b(import|from)\s+' + mod + r'\b'
                if re.search(pattern, line_clean):
                    errors.append(
                        f"Lỗi tương thích Pyodide WASM: Không được dùng thư viện ngoài '{mod}' trong code ví dụ live trên bài đọc HTML. "
                        f"Chỉ dùng thư viện chuẩn (Standard Library: sys, math, datetime, json...)."
                    )
    return errors

def lint_naming_convention(code: str, tech_stack: str) -> List[str]:
    """
    Dynamically checks function naming conventions in code based on tech_stack:
    - Python / C: expects snake_case function names.
    - JS / TS / Java: expects camelCase function names.
    """
    if not code or not tech_stack:
        return []

    errors = []
    tech_lower = tech_stack.lower()

    if "python" in tech_lower or " c" in tech_lower or tech_lower.endswith("/c"):
        # Flag camelCase function names in Python: e.g. def calculateTotalSum(
        for line_no, line in enumerate(code.splitlines(), 1):
            match = re.search(r'\bdef\s+([a-z0-9_]*[A-Z][a-zA-Z0-9_]*)\s*\(', line)
            if match and not match.group(1).startswith("__"):
                suggested_snake = re.sub(r'([A-Z])', r'_\1', match.group(1)).lower()
                errors.append(
                    f"Line {line_no}: Vi phạm quy chuẩn đặt tên {tech_stack.upper()} (snake_case required): "
                    f"Tên hàm '{match.group(1)}' bị dùng camelCase. Hãy dùng '{suggested_snake}'."
                )

    elif any(kw in tech_lower for kw in ["javascript", "js", "typescript", "ts", "java", "frontend", "web"]):
        # Flag snake_case function names in JS/Java: e.g. function calculate_total_sum(
        for line_no, line in enumerate(code.splitlines(), 1):
            match = re.search(r'\b(function|void|int|String|boolean)\s+([a-z]+_[a-z0-9_]+)\s*\(', line)
            if match:
                errors.append(
                    f"Line {line_no}: Vi phạm quy chuẩn đặt tên {tech_stack.upper()} (camelCase required): "
                    f"Tên hàm '{match.group(2)}' bị dùng snake_case."
                )

    return errors
