"""
core/sanitizers/json_recoverer.py
Robust JSON recovery parser and newline sanitizer for LLM output payloads.
"""

import json
import re
import ast
from typing import Dict, Any, Union

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

def robust_json_parse(json_str: str) -> Union[Dict[str, Any], list]:
    """Robust multi-pass JSON parser capable of recovering truncated or partially broken LLM JSON."""
    if not json_str:
        return {}
    
    # 1. Clean markdown code fences and whitespace
    clean_str = json_str.strip()
    if clean_str.startswith("```"):
        clean_str = re.sub(r"^```(?:json)?\s*", "", clean_str)
        clean_str = re.sub(r"\s*```$", "", clean_str)
        clean_str = clean_str.strip()

    # 2. Try standard json.loads directly
    try:
        return json.loads(clean_str)
    except Exception:
        pass

    # 3. Try finding outermost JSON structure { ... } or [ ... ]
    s_obj = clean_str.find("{")
    e_obj = clean_str.rfind("}")
    s_arr = clean_str.find("[")
    e_arr = clean_str.rfind("]")

    if s_obj != -1 and e_obj != -1 and e_obj > s_obj:
        sub_obj = clean_str[s_obj:e_obj+1]
        try:
            return json.loads(sub_obj)
        except Exception:
            try:
                fixed_sub = fix_raw_newlines_in_json_strings(sub_obj)
                return json.loads(fixed_sub)
            except Exception:
                pass

    if s_arr != -1 and e_arr != -1 and e_arr > s_arr:
        sub_arr = clean_str[s_arr:e_arr+1]
        try:
            return json.loads(sub_arr)
        except Exception:
            try:
                fixed_arr = fix_raw_newlines_in_json_strings(sub_arr)
                return json.loads(fixed_arr)
            except Exception:
                pass

    # 4. Try ast.literal_eval
    try:
        eval_res = ast.literal_eval(clean_str)
        if isinstance(eval_res, (dict, list)):
            return eval_res
    except Exception:
        pass

    # 5. Specialized Stage 1 / Stage 2 Reading Generator offset extraction fallback
    cleaned = clean_str
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
            
    if not offsets:
        return {}

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
                result[k] = parsed
            except Exception:
                try:
                    parsed = ast.literal_eval(val_sub)
                    result[k] = parsed
                except Exception:
                    try:
                        cleaned_sub = fix_raw_newlines_in_json_strings(val_sub)
                        parsed = json.loads(cleaned_sub)
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
