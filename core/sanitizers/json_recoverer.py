"""
core/sanitizers/json_recoverer.py
Robust JSON recovery parser and newline sanitizer for LLM output payloads.
"""

import json
import re
import ast
from typing import Dict, Any

def fix_raw_newlines_in_json_strings(json_str: str) -> str:
    """Escapes raw newlines and unescaped quotes inside JSON string literals."""
    if not json_str:
        return ""
    chars = list(json_str)
    in_string = False
    escaped = False
    for i in range(len(chars)):
        char = chars[i]
        if char == '"' and not escaped:
            in_string = not in_string
        elif char == '\\' and in_string and not escaped:
            escaped = True
            continue
        elif char == '\n' and in_string:
            chars[i] = '\\n'
        elif char == '\r' and in_string:
            chars[i] = ''
        escaped = False
    return "".join(chars)

def robust_json_parse(json_str: str) -> Dict[str, Any]:
    """Robust multi-pass JSON parser capable of recovering truncated or partially broken LLM JSON."""
    if not json_str:
        return {}
    try:
        return json.loads(json_str)
    except Exception as e:
        print(f"  [Robust Parser] Standard json.loads failed: {e}. Attempting custom recovery...")
        
    cleaned = json_str.strip()
    if cleaned.startswith("{"):
        cleaned = cleaned[1:]
    if cleaned.endswith("}"):
        cleaned = cleaned[:-1]
        
    result = {}
    keys = ["problem", "analysis", "solution", "example", "resolve", "summary", "self_test", "quiz", "lab", "visualizer"]
    
    offsets = []
    for k in keys:
        pattern = r'"' + k + r'"\s*:\s*'
        match = re.search(pattern, cleaned)
        if match:
            offsets.append((k, match.start(), match.end()))
            
    offsets.sort(key=lambda x: x[1])
    
    for idx, (k, start, val_start) in enumerate(offsets):
        val_end = offsets[idx+1][1] if idx + 1 < len(offsets) else len(cleaned)
        val_sub = cleaned[val_start:val_end].strip()
        
        if val_sub.endswith(","):
            val_sub = val_sub[:-1].strip()
            
        if k in ["problem", "analysis", "solution", "example", "resolve", "summary"]:
            if val_sub.startswith('"'):
                val_sub = val_sub[1:]
            if val_sub.endswith('"'):
                val_sub = val_sub[:-1]
            val_sub = val_sub.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')
            result[k] = val_sub
        else:
            try:
                parsed = json.loads(val_sub)
                if k == "lab" and not isinstance(parsed, dict):
                    raise ValueError("lab must be a dict")
                if k == "quiz" and not isinstance(parsed, list):
                    raise ValueError("quiz must be a list")
                if k == "visualizer" and not isinstance(parsed, dict):
                    raise ValueError("visualizer must be a dict")
                result[k] = parsed
            except Exception:
                try:
                    parsed = ast.literal_eval(val_sub)
                    if k == "lab" and not isinstance(parsed, dict):
                        raise ValueError("lab must be a dict")
                    if k == "quiz" and not isinstance(parsed, list):
                        raise ValueError("quiz must be a list")
                    if k == "visualizer" and not isinstance(parsed, dict):
                        raise ValueError("visualizer must be a dict")
                    result[k] = parsed
                except Exception:
                    try:
                        cleaned_sub = fix_raw_newlines_in_json_strings(val_sub)
                        parsed = json.loads(cleaned_sub)
                        if k == "lab" and not isinstance(parsed, dict):
                            raise ValueError("lab must be a dict")
                        if k == "quiz" and not isinstance(parsed, list):
                            raise ValueError("quiz must be a list")
                        if k == "visualizer" and not isinstance(parsed, dict):
                            raise ValueError("visualizer must be a dict")
                        result[k] = parsed
                    except Exception:
                        if k == "self_test":
                            items = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', val_sub)
                            result[k] = [item.replace('\\"', '"') for item in items]
                        elif k == "lab":
                            result[k] = {"title": "Lab", "objectives": [], "steps": [], "checklist": []}
                        else:
                            result[k] = {}
                            
    for k in keys:
        if k not in result:
            if k in ["problem", "analysis", "solution", "example", "resolve", "summary"]:
                result[k] = ""
            elif k == "self_test":
                result[k] = []
            elif k == "lab":
                result[k] = {"title": "Lab", "objectives": [], "steps": [], "checklist": []}
            else:
                result[k] = {}
                
    return result
