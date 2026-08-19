"""
core/utils/llm_parser.py
Consolidated & Robust Parser for LLM Responses.
Handles JSON extraction, auto-repair for trailing commas/unescaped quotes,
markdown fence stripping, and XML element extraction.
"""

import re
import json
from typing import Any, Dict, List, Optional
from core.utils.json_sanitizer import clean_and_parse_json

def extract_json_from_response(raw_text: str, default: Optional[Any] = None) -> Any:
    """
    Safely extracts and parses JSON object or array from raw LLM output.
    Returns default if parsing fails instead of crashing.
    """
    if not raw_text or not raw_text.strip():
        return default
    try:
        return clean_and_parse_json(raw_text)
    except Exception:
        # Fallback auto-repair: remove trailing commas before closing braces
        try:
            cleaned = re.sub(r",\s*([\]}])", r"\1", raw_text)
            return clean_and_parse_json(cleaned)
        except Exception:
            return default

def clean_markdown_fences(text: str) -> str:
    """Strips outer markdown code fences (``` or ```html / ```python)."""
    if not text:
        return ""
    cleaned = text.strip()
    match = re.match(r"^```(?:[a-zA-Z0-9_\-]+)?\n?(.*?)\n?```$", cleaned, re.DOTALL)
    if match:
        return match.group(1).strip()
    return cleaned

def extract_xml_tag_content(text: str, tag_name: str, default: str = "") -> str:
    """Extracts the inner text content of a specified XML-like tag (e.g. <tag>content</tag>)."""
    if not text:
        return default
    pattern = rf"<{tag_name}[^>]*>(.*?)</{tag_name}>"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return default

def extract_all_xml_tags(text: str, tag_name: str) -> List[str]:
    """Extracts all instances of a specified XML-like tag."""
    if not text:
        return []
    pattern = rf"<{tag_name}[^>]*>(.*?)</{tag_name}>"
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    return [m.strip() for m in matches]
