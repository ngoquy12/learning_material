import json
import re
import logging
from typing import Any

logger = logging.getLogger("app.utils.json_helper")

def get_open_containers(s: str):
    in_string = False
    escape = False
    stack = []
    
    for char in s:
        if escape:
            escape = False
        elif char == '\\':
            if in_string:
                escape = True
        elif char == '"':
            in_string = not in_string
        elif not in_string:
            if char in '{[':
                stack.append(char)
            elif char in '}]':
                if stack:
                    if (char == '}' and stack[-1] == '{') or (char == ']' and stack[-1] == '['):
                        stack.pop()
    return stack, in_string

def repair_truncated_json(s: str) -> str:
    s = s.strip()
    if not s:
        return "[]"
        
    for _ in range(50):
        # Determine current open containers
        stack, in_string = get_open_containers(s)
        
        # Construct candidate string
        candidate = s
        if in_string:
            candidate += '"'
            
        # Append closing brackets/braces
        closing = ""
        for container in reversed(stack):
            if container == '{':
                closing += '}'
            elif container == '[':
                closing += ']'
        candidate += closing
        
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            # Find the last occurrence of a delimiter: comma `,`, open brace `{`, open bracket `[`
            last_delim_idx = -1
            in_str = False
            esc = False
            for idx, char in enumerate(s):
                if esc:
                    esc = False
                elif char == '\\':
                    if in_str:
                        esc = True
                elif char == '"':
                    in_str = not in_str
                elif not in_str:
                    if char in ',{[':
                        last_delim_idx = idx
            
            if last_delim_idx == -1 or last_delim_idx == 0:
                return "[]"
                
            pruned_s = s[:last_delim_idx]
            if s[last_delim_idx] == ',':
                pruned_s = s[:last_delim_idx]
            else:
                pruned_s = s[:last_delim_idx + 1]
                
            s = pruned_s.rstrip()
            
    return "[]"

def clean_and_parse_json(raw_str: str) -> Any:
    if not raw_str or not raw_str.strip():
        raise ValueError("Empty response received from the agent.")
        
    cleaned = raw_str.strip()
    
    # 1. Clean markdown code blocks (e.g. ```json ... ```)
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Extract from first [ or { to the last ] or }
        indices = [i for i in [cleaned.find('['), cleaned.find('{')] if i > -1]
        rindices = [i for i in [cleaned.rfind(']'), cleaned.rfind('}')] if i > -1]
        if indices and rindices:
            cleaned = cleaned[min(indices):max(rindices)+1]
            
    # 2. Remove comments
    # Remove single line comments starting with // but not part of a URL
    cleaned = re.sub(r'(?<!:)\/\/.*$', '', cleaned, flags=re.MULTILINE)
    # Remove python-style comments
    cleaned = re.sub(r'#.*$', '', cleaned, flags=re.MULTILINE)
    # Remove multi-line comments /* ... */
    cleaned = re.sub(r'\/\*.*?\*\/', '', cleaned, flags=re.DOTALL)
    
    # 3. Remove trailing commas before closing braces/brackets
    cleaned = re.sub(r',\s*([\]}])', r'\1', cleaned)
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as initial_err:
        # Try to repair truncated JSON
        try:
            repaired = repair_truncated_json(cleaned)
            return json.loads(repaired)
        except Exception as repair_err:
            logger.error("Failed to parse and repair JSON from agent response.")
            logger.error(f"Raw string: {raw_str}")
            logger.error(f"Cleaned string: {cleaned}")
            logger.error(f"Initial parse error: {initial_err}")
            logger.error(f"Repair error: {repair_err}")
            raise ValueError(
                f"JSON parsing failed: {initial_err}. "
                f"Raw response logged. First 200 chars: '{raw_str[:200]}'"
            )

def normalize_id(id_str: str) -> str:
    if not id_str:
        return ""
    s = str(id_str).lower()
    s = s.replace("chương", "session").replace("chuong", "session").replace("sess", "session")
    s = s.replace("bài", "lesson").replace("bai", "lesson").replace("less", "lesson")
    s = re.sub(r'[^a-z0-9]', '', s)
    s = re.sub(r'0+(\d+)', r'\1', s)
    return s

def merge_curriculums(original: Any, updated: Any) -> list:
    if not isinstance(original, list):
        return updated if isinstance(updated, list) else []
    if not isinstance(updated, list):
        return original
        
    # Build maps of original sessions by normalized session_id
    original_sessions_list = [s for s in original if isinstance(s, dict)]
    original_sessions_by_id = {}
    for s in original_sessions_list:
        sess_id = s.get("session_id")
        if sess_id:
            norm_id = normalize_id(sess_id)
            if norm_id:
                original_sessions_by_id[norm_id] = s

    # Map original session object id to its merged version
    merged_by_original_id = {}
    new_sessions = []
    used_original_sessions = set()
    
    # Match updated sessions to original sessions
    for updated_s in updated:
        if not isinstance(updated_s, dict):
            continue
        sess_id = updated_s.get("session_id")
        if not sess_id:
            continue
            
        norm_sess_id = normalize_id(sess_id)
        
        orig_s = None
        if norm_sess_id in original_sessions_by_id:
            candidate = original_sessions_by_id[norm_sess_id]
            if id(candidate) not in used_original_sessions:
                orig_s = candidate
                
        if orig_s is None:
            # Find the first unused original session
            for candidate in original_sessions_list:
                if id(candidate) not in used_original_sessions:
                    orig_s = candidate
                    break
                    
        if orig_s is not None:
            used_original_sessions.add(id(orig_s))
            
            # Merge session fields, preserving form/deadline if present at session level
            merged_s = {
                "session_id": updated_s.get("session_id") or orig_s.get("session_id"),
                "title": updated_s.get("title") or orig_s.get("title"),
                "form": updated_s.get("form") or orig_s.get("form") or "Lý thuyết",
                "deadline": updated_s.get("deadline") or orig_s.get("deadline") or "",
                "lessons": []
            }
            
            orig_lessons_list = [l for l in orig_s.get("lessons", []) if isinstance(l, dict)]
            orig_lessons_by_id = {}
            for l in orig_lessons_list:
                l_id = l.get("lesson_id")
                if l_id:
                    norm_l_id = normalize_id(l_id)
                    if norm_l_id:
                        orig_lessons_by_id[norm_l_id] = l
                        
            used_lessons = set()
            updated_lessons = updated_s.get("lessons", [])
            
            merged_lessons_by_orig_id = {}
            new_lessons_for_s = []
            
            if isinstance(updated_lessons, list):
                for updated_l in updated_lessons:
                    if not isinstance(updated_l, dict):
                        continue
                    l_id = updated_l.get("lesson_id")
                    norm_l_id = normalize_id(l_id) if l_id else ""
                    
                    matched_l = None
                    if norm_l_id and norm_l_id in orig_lessons_by_id:
                        candidate_l = orig_lessons_by_id[norm_l_id]
                        if id(candidate_l) not in used_lessons:
                            matched_l = candidate_l
                            
                    if matched_l is None:
                        for candidate_l in orig_lessons_list:
                            if id(candidate_l) not in used_lessons:
                                matched_l = candidate_l
                                break
                                
                    if matched_l is not None:
                        used_lessons.add(id(matched_l))
                        merged_l = {
                            "lesson_id": updated_l.get("lesson_id") or matched_l.get("lesson_id"),
                            "title": updated_l.get("title") or matched_l.get("title"),
                            "form": updated_l.get("form") or matched_l.get("form") or "Lý thuyết",
                            "deadline": updated_l.get("deadline") or matched_l.get("deadline") or "",
                            "details": updated_l.get("details") or matched_l.get("details"),
                            "expected_output": updated_l.get("expected_output") or matched_l.get("expected_output")
                        }
                        merged_lessons_by_orig_id[id(matched_l)] = merged_l
                    else:
                        new_lessons_for_s.append(updated_l)
                        
            # Build merged lessons preserving original order
            for orig_l in orig_lessons_list:
                if id(orig_l) in merged_lessons_by_orig_id:
                    merged_s["lessons"].append(merged_lessons_by_orig_id[id(orig_l)])
                else:
                    merged_s["lessons"].append(orig_l)
            
            # Append brand new lessons
            for new_l in new_lessons_for_s:
                merged_s["lessons"].append(new_l)
                
            merged_by_original_id[id(orig_s)] = merged_s
        else:
            new_sessions.append(updated_s)
            
    # Build final list of sessions preserving original order
    final_sessions = []
    for orig_s in original_sessions_list:
        if id(orig_s) in merged_by_original_id:
            final_sessions.append(merged_by_original_id[id(orig_s)])
        else:
            final_sessions.append(orig_s)
            
    # Append brand new sessions
    for new_s in new_sessions:
        final_sessions.append(new_s)
        
    return final_sessions
