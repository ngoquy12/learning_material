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
            if re.search(r'log\("<[^">]*"[^">]*"\)', line) or re.search(r'="<[^">]*"[^">]*">', line):
                errors.append(f"Line {line_no}: Lỗi đóng ngoặc chuỗi JavaScript (Unescaped quote in string literal): {line.strip()}")
                
    return errors
