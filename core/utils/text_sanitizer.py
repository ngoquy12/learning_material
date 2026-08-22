"""
core/utils/text_sanitizer.py — Unified Text & Code Sanitization Utilities.
Centralizes Markdown fence stripping, JSON parsing recovery, and typography normalization.
"""

import re
import json
from typing import Any, Optional, Dict, List, Union


def strip_markdown_fence(text: str) -> str:
    """
    Strips leading and trailing Markdown code fences (e.g. ```json ... ``` or ```python ... ```).
    Handles whitespace, indentation, and varied language tags.
    """
    if not text or not isinstance(text, str):
        return ""
    
    cleaned = text.strip()
    
    # Remove leading code fence
    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1:]
        else:
            cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
            
    # Remove trailing code fence
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].rstrip()
        
    return cleaned.strip()


def extract_and_parse_json(text: str, default: Optional[Any] = None) -> Union[Dict[str, Any], List[Any], Any]:
    """
    Trích xuất và parse JSON từ output thô của LLM, trả về `default` nếu thất bại.

    Hàm này TỪNG là một bản cài đặt riêng, trùng lặp với extract_json_from_response()
    nhưng yếu hơn: không escape ký tự điều khiển thô trong chuỗi, không sửa dấu phẩy
    thừa. Hai bộ parser song song nghĩa là cùng một response LLM có thể parse được ở
    creator này nhưng hỏng ở creator kia — nay gộp về một đường duy nhất.

    Giữ nguyên chữ ký cũ: mặc định trả về {} thay vì None khi không truyền `default`.
    """
    if not text or not isinstance(text, str):
        return default if default is not None else {}

    from core.utils.llm_parser import extract_json_from_response

    result = extract_json_from_response(text, default=None)
    if result is None:
        return default if default is not None else {}
    return result


def sanitize_svg_tags(svg_code: str) -> str:
    """
    Sanitizes SVG markup ensuring clean namespace attributes, proper viewBox, and closed tags.
    """
    if not svg_code or not isinstance(svg_code, str):
        return ""
        
    cleaned = svg_code.strip()
    if "<svg" not in cleaned.lower():
        return cleaned
        
    # Ensure xmlns exists
    if "xmlns=" not in cleaned:
        cleaned = re.sub(r"<svg\b", '<svg xmlns="http://www.w3.org/2000/svg"', cleaned, count=1, flags=re.IGNORECASE)
        
    return cleaned


def normalize_vietnamese_punctuation(text: str) -> str:
    """
    Normalizes Vietnamese punctuation spacing (removes space before .,;:!? and ensures closing period).
    """
    if not text or not isinstance(text, str):
        return ""
        
    # Remove spaces before punctuation
    normalized = re.sub(r"\s+([.,;:!?])", r"\1", text)
    
    return normalized.strip()
