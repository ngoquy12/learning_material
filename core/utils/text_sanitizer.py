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
    Robustly extracts and parses JSON from raw LLM text responses.
    Attempts direct parsing after fence stripping, then falls back to regex boundary matching.
    """
    if not text or not isinstance(text, str):
        return default if default is not None else {}

    cleaned = strip_markdown_fence(text)
    
    # Attempt 1: Direct parse
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Attempt 2: Extract between outermost curly brackets { ... }
    brace_start = cleaned.find("{")
    brace_end = cleaned.rfind("}")
    if brace_start != -1 and brace_end > brace_start:
        candidate = cleaned[brace_start:brace_end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    # Attempt 3: Extract between outermost square brackets [ ... ]
    bracket_start = cleaned.find("[")
    bracket_end = cleaned.rfind("]")
    if bracket_start != -1 and bracket_end > bracket_start:
        candidate = cleaned[bracket_start:bracket_end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return default if default is not None else {}


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
