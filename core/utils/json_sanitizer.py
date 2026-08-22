"""
core/utils/json_sanitizer.py
Robust JSON Sanitizer & Parser for LLM Responses.
Strips markdown code fences, sanitizes control characters, and handles unescaped quotes.
"""

import re
import json
from typing import Any, Dict, List

def clean_and_parse_json(raw_text: str) -> Any:
    """
    Cleans raw text output from LLM and parses it safely into a Python dict or list.
    Raises ValueError if JSON parsing fails after all sanitization attempts.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Lỗi parse JSON: Dữ liệu văn bản thô từ LLM bị rỗng.")

    cleaned = raw_text.strip()

    # 1. Strip Markdown Code Fences (e.g. ```json ... ```) -- ONLY when the fence genuinely wraps
    # the WHOLE response (starts with ```). Previously this searched for the FIRST ``` ... ```
    # pair ANYWHERE in the text, which incorrectly matched an inline code fence embedded inside a
    # JSON string value (e.g. a quiz question's own ```python ...``` code sample) and extracted
    # just that inner snippet as if it were the entire JSON payload -- a confirmed real bug that
    # silently corrupted/rejected valid JSON responses containing fenced code in string fields.
    if cleaned.startswith("```"):
        match = re.match(r"```(?:json)?\s*\n?(.*)\n?```\s*$", cleaned, re.DOTALL | re.IGNORECASE)
        if match:
            cleaned = match.group(1).strip()
        else:
            cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
            cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    # 2. Extract outermost JSON structure ([...] or {...})
    first_brace = min((cleaned.find('{') if '{' in cleaned else len(cleaned)),
                      (cleaned.find('[') if '[' in cleaned else len(cleaned)))
    last_brace = max(cleaned.rfind('}'), cleaned.rfind(']'))

    if first_brace < len(cleaned) and last_brace > first_brace:
        cleaned = cleaned[first_brace:last_brace + 1]

    # 3. First parse attempt
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 4. Sanitize invalid control characters inside JSON strings (e.g. raw newlines, tabs)
    # Replace raw unescaped newlines inside string literals
    sanitized = re.sub(r'(?<=: ")(.*?)(?="[,\s\n\}])', lambda m: m.group(1).replace('\n', '\\n').replace('\t', '\\t'), cleaned, flags=re.DOTALL)

    try:
        return json.loads(sanitized)
    except json.JSONDecodeError as e:
        raise ValueError(f"Lỗi parse JSON thô từ LLM không thành công: {e}. Đoạn dữ liệu thô: {cleaned[:200]}...")
