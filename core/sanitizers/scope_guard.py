"""
core/sanitizers/scope_guard.py
Post-generation scope validator and cleaner to prevent unauthorized concepts/keywords.
"""

import re
from typing import Dict, Any, Tuple, List

def validate_and_clean_forbidden_scope(content: Dict[str, Any], forbidden_scope: str) -> Tuple[Dict[str, Any], List[str]]:
    """Validates content fields against forbidden scope and sanitizes infractions."""
    if not forbidden_scope or not isinstance(forbidden_scope, str) or not content or not isinstance(content, dict):
        return content, []
    
    terms = [t.strip() for t in re.split(r'[,;\n/•\-]', forbidden_scope) if t.strip() and len(t.strip()) > 2]
    
    violations = []
    text_fields = ["problem", "analysis", "solution", "example", "example_good", "example_bad", "resolve", "summary"]
    
    for field in text_fields:
        if field in content and isinstance(content[field], str):
            val = content[field]
            for term in terms:
                pattern = r'\b' + re.escape(term) + r'\b' if term.isascii() else re.escape(term)
                if re.search(pattern, val, flags=re.IGNORECASE):
                    violations.append(f"Field '{field}': Found forbidden term '{term}'")
                    val = re.sub(pattern, f"/* [Scope Guard: Filtered '{term}'] */", val, flags=re.IGNORECASE)
            content[field] = val

    if violations:
        print(f"  [Forbidden Scope Post-Linter] ⚠️ Discovered & cleaned {len(violations)} forbidden scope violations:")
        for v in violations[:5]:
            print(f"    - ❌ {v}")
            
    return content, violations
