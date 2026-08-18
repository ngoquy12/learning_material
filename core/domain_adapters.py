# core/domain_adapters.py
"""
Domain-Specific Prompt Adapters for Elearning Content Factory.
Injects industrial coding standards and enterprise business scenarios into System Prompts.
Supports Local SLM (vLLM / Ollama) endpoints for offline fine-tuned model execution.
"""

import os
import urllib.request
import json
from typing import Dict, Any, Optional, Set, List

DOMAIN_RULES = {
    "python/core": """
=== INDUSTRY CODING ADAPTER: PYTHON CORE ===
1. Strict PEP 8 Compliance: 4-space indentation, snake_case function/variable naming, PascalCase for classes.
2. Type Hints Required: All function signatures must include type annotations (e.g., def add(a: int, b: int) -> int:).
3. Explicit Error Handling: Avoid bare `except:`, use specific exceptions (e.g. `ValueError`, `KeyError`).
4. Modern Python 3.10+ Features: Favor type union syntax `int | str` over `Optional[Union[int, str]]`.
""",

    "web_framework/backend": """
=== INDUSTRY CODING ADAPTER: WEB FRAMEWORK & RESTFUL BACKEND ===
1. Validation Schemas / DTOs: Use explicit DTO schemas with field validation.
2. Dependency Injection / Middleware: Use dependency injection for database sessions and auth guards.
3. Asynchronous Handlers: Prefer async non-blocking handlers for I/O bound endpoints.
4. HTTP Status Codes: Always pass explicit status codes (e.g. 200 OK, 201 Created, 400 Bad Request, 404 Not Found).
""",

    "web/frontend": """
=== INDUSTRY CODING ADAPTER: WEB FRONTEND (HTML/CSS/JS) ===
1. Semantic HTML5: Use `<main>`, `<article>`, `<section>`, `<nav>`, `<aside>` elements.
2. Responsive Layouts: Use CSS Flexbox/Grid and relative units (rem, em, %).
3. Modern JS (ES6+): Use `const`/`let`, arrow functions, async/await, and template literals.
4. Accessibility (a11y): Include `alt` attributes for images and ARIA tags for interactive elements.
""",

    "database/sql": """
=== INDUSTRY CODING ADAPTER: DATABASE & SQL ===
1. Parameterized Queries: Always use prepared statements or ORM binding to prevent SQL injection.
2. Indexing Strategy: Create explicit indexes on foreign keys and frequently queried columns.
3. Transactional Integrity: Wrap multi-table mutations inside explicit ACID transactions.
4. Schema Normalization: Ensure table schemas adhere to 3NF standards.
""",

    "devops/docker": """
=== INDUSTRY CODING ADAPTER: DEVOPS & DOCKER ===
1. Multi-Stage Builds: Use multi-stage Dockerfiles to minimize production image footprint.
2. Security Practices: Never run container as root user (`USER 1000:1000`).
3. Explicit Tagging: Avoid `latest` tag; pin base image versions.
4. Layer Caching: Copy dependencies before source code to optimize build cache.
""",

    "office/productivity": """
=== INDUSTRY ADAPTER: OFFICE PRODUCTIVITY & BUSINESS APPLICATION (EXCEL / WORD / POWERPOINT) ===
1. Professional Document & Data Formatting: Follow official administrative document standards (Nghị định 30/2020/NĐ-CP for Word), clean typography, proper margins, and high-contrast color palettes.
2. Robust Excel Formula Design: Favor uppercase standard functions (`IF`, `AND`, `OR`, `VLOOKUP`, `XLOOKUP`, `SUMIFS`, `INDEX/MATCH`). Use relative and absolute cell references (`$A$1`) correctly.
3. Logical Data Organization: Structure Excel tables cleanly with clear headers, proper data types (Date, Currency, Number), and Conditional Formatting.
4. Presentation Mastery (PowerPoint): Use 16:9 widescreen layout, 3-30-300 rule (max 3 keypoints per slide, max 30 words per keypoint), Master Slide layout consistency, and clear data visualization charts.
"""
}

# 6 Enterprise Business Scenario Templates (Real-World High-Scale Architecture)
ENTERPRISE_SCENARIOS: Dict[str, str] = {
    "ecommerce_checkout": """
=== ENTERPRISE BUSINESS SCENARIO: E-COMMERCE ORDER PROCESSING ===
- Context: High-concurrency checkout pipeline processing 10,000+ orders/min.
- Focus: Idempotent transaction handling, Inventory atomic deduction, Order state machine (Pending -> Paid -> Shipped).
""",
    "lms_assessment": """
=== ENTERPRISE BUSINESS SCENARIO: LMS AUTOMATED GRADING & ASSESSMENT ===
- Context: Enterprise E-learning Assessment Engine handling 50,000+ concurrent students.
- Focus: Automated testcase evaluation, Plagiarism score thresholding, Learning outcome mapping (CLO/PLO).
""",
    "payment_webhook": """
=== ENTERPRISE BUSINESS SCENARIO: PAYMENT GATEWAY WEBHOOK INTEGRATION ===
- Context: Asynchronous Stripe/PayPal webhook receiver with cryptographic signature verification.
- Focus: Signature validation, Anti-replay attack timestamp check, Idempotent event processing.
""",
    "microservices_ratelimit": """
=== ENTERPRISE BUSINESS SCENARIO: MICROSERVICES RATE LIMITER GATEWAY ===
- Context: API Gateway managing 1M+ requests/sec across distributed microservices.
- Focus: Token Bucket / Sliding Window Algorithm using Redis atomic Lua scripts.
""",
    "security_auth": """
=== ENTERPRISE BUSINESS SCENARIO: ENTERPRISE AUTH & RBAC GUARD ===
- Context: Zero-Trust Security Module with JWT Bearer authentication and Role-Based Access Control.
- Focus: Token validation, Claims extraction, Refresh Token rotation, Cryptographic hashing.
""",
    "cache_redis": """
=== ENTERPRISE BUSINESS SCENARIO: DISTRIBUTED REDIS CACHING ===
- Context: High-throughput Cache-Aside Architecture for heavy database reads.
- Focus: Cache Stampede protection (SingleFlight/Mutex), TTL Expiration, Cache Invalidation strategies.
"""
}


def get_domain_rules(tech_stack: str) -> str:
    """
    Returns industrial coding rules matching the provided tech stack.
    """
    if not tech_stack:
        return ""
        
    stack_lower = tech_stack.lower().strip()
    
    if any(kw in stack_lower for kw in ["fastapi", "express", "spring", "flask", "django", "nest", "web api", "rest api"]):
        return DOMAIN_RULES["web_framework/backend"]
    elif "python" in stack_lower:
        return DOMAIN_RULES["python/core"]
    elif any(kw in stack_lower for kw in ["html", "css", "js", "react", "frontend", "vue"]):
        return DOMAIN_RULES["web/frontend"]
    elif any(kw in stack_lower for kw in ["sql", "postgres", "mysql", "db", "database"]):
        return DOMAIN_RULES["database/sql"]
    elif any(kw in stack_lower for kw in ["office", "excel", "word", "powerpoint", "tinhocvanphong", "workspace"]):
        return DOMAIN_RULES["office/productivity"]
    elif any(kw in stack_lower for kw in ["docker", "k8s", "devops", "ci/cd"]):
        return DOMAIN_RULES["devops/docker"]
        
    # Universal Dynamic Fallback for ANY arbitrary CLO/PLO course (Data Science, UI/UX, Cybersecurity, Mobile, Networking...)
    # Generic default for unspecified tech stacks
    return """
=== GENERAL INDUSTRY CODING STANDARDS ===
1. Clean Code & Modular Design: Keep functions small, single-responsibility, and well-documented.
2. Robust Error Handling: Validate inputs, handle boundary conditions, and provide meaningful error logs.
3. Industry Naming Conventions: Follow standard naming conventions and architectural patterns for the domain.
"""

# Universal multi-stack programming construct registry (Zero-Hardcode Mapping Matrix)
ABSTRACT_PROGRAMMING_CONSTRUCTS: Dict[str, Dict[str, Any]] = {
    "control_flow": {
        "keywords_vi": ["điều kiện", "rẽ nhánh", "if", "else", "switch", "case", "toán tử 3 ngôi", "ternary"],
        "tokens": {
            "python": ["if", "elif", "else", "match"],
            "javascript": ["if", "else", "switch", "case"],
            "typescript": ["if", "else", "switch", "case"],
            "java": ["if", "else", "switch", "case"],
            "c": ["if", "else", "switch", "case"],
            "cpp": ["if", "else", "switch", "case"],
            "csharp": ["if", "else", "switch", "case"],
            "golang": ["if", "else", "switch", "case"],
            "php": ["if", "else", "switch", "case"]
        }
    },
    "loops": {
        "keywords_vi": ["vòng lặp", "lặp", "for", "while", "do-while", "loop", "duyệt"],
        "tokens": {
            "python": ["for", "while"],
            "javascript": ["for", "while", "do-while"],
            "typescript": ["for", "while", "do-while"],
            "java": ["for", "while", "do"],
            "c": ["for", "while", "do"],
            "cpp": ["for", "while", "do"],
            "csharp": ["for", "while", "do", "foreach"],
            "golang": ["for", "range"],
            "php": ["for", "while", "do", "foreach"]
        }
    },
    "functions": {
        "keywords_vi": ["hàm", "function", "phương thức", "method", "thủ tục", "arrow function", "lambda"],
        "tokens": {
            "python": ["def", "lambda"],
            "javascript": ["function", "=>"],
            "typescript": ["function", "=>"],
            "java": ["public static", "private static", "void"],
            "c": ["void", "int main"],
            "cpp": ["void", "int main", "auto"],
            "csharp": ["void", "async"],
            "golang": ["func"],
            "php": ["function", "fn"]
        }
    },
    "data_structures": {
        "keywords_vi": ["mảng", "array", "danh sách", "list", "đối tượng", "object", "từ điển", "dict", "json", "cấu trúc dữ liệu"],
        "tokens": {
            "python": ["list", "dict", "set", "tuple"],
            "javascript": ["Array", "Object", "push(", "pop(", "splice("],
            "typescript": ["Array", "Object", "push(", "pop(", "splice(", "interface", "type"],
            "java": ["ArrayList", "HashMap", "List", "Map"],
            "c": ["struct", "malloc", "free"],
            "cpp": ["vector", "map", "set", "struct", "class"],
            "csharp": ["List", "Dictionary"],
            "golang": ["slice", "map", "struct"],
            "php": ["array()", "[]"]
        }
    },
    "async_and_dom": {
        "keywords_vi": ["bất đồng bộ", "async", "await", "promise", "dom", "document", "addeventlistener", "fetch", "ajax", "localstorage"],
        "tokens": {
            "javascript": ["async", "await", "Promise", "document.", "window.", "addEventListener", "fetch", "localStorage"],
            "typescript": ["async", "await", "Promise", "document.", "window.", "addEventListener", "fetch", "localStorage"],
            "python": ["async", "await", "asyncio"],
            "java": ["CompletableFuture", "Thread"]
        }
    }
}

def get_forbidden_syntax_for_scope(tech_stack: str, forbidden_concepts: Set[str]) -> List[str]:
    """
    Dynamically maps forbidden syllabus concepts into language-specific syntax tokens
    based on the multi-stack construct registry.
    """
    if not tech_stack or not forbidden_concepts:
        return []
        
    tech_lower = tech_stack.lower().strip()
    # Find matching stack key
    matched_stack = None
    for stack_key in ["javascript", "typescript", "python", "java", "csharp", "golang", "cpp", "c", "php"]:
        if stack_key in tech_lower:
            matched_stack = stack_key
            break
            
    if not matched_stack:
        return []
        
    forbidden_tokens: Set[str] = set()
    for concept in forbidden_concepts:
        c_lower = str(concept).lower()
        for category, cat_data in ABSTRACT_PROGRAMMING_CONSTRUCTS.items():
            if any(kw in c_lower for kw in cat_data["keywords_vi"]):
                tokens = cat_data["tokens"].get(matched_stack, [])
                forbidden_tokens.update(tokens)
                
    return sorted(list(forbidden_tokens))

def get_enterprise_domain_prompt(tech_stack: str, lesson_topic: str = "") -> str:
    """
    Combines domain rules with relevant Enterprise Real-World Business Scenario blueprints.
    """
    base_rules = get_domain_rules(tech_stack)
    topic_lower = (lesson_topic or "").lower().strip()
    
    selected_scenario = ""
    if any(kw in topic_lower for kw in ["payment", "webhook", "thanhtoan"]):
        selected_scenario = ENTERPRISE_SCENARIOS["payment_webhook"]
    elif any(kw in topic_lower for kw in ["auth", "jwt", "baomat", "login", "role", "rbac"]):
        selected_scenario = ENTERPRISE_SCENARIOS["security_auth"]
    elif any(kw in topic_lower for kw in ["cache", "redis", "bophodem"]):
        selected_scenario = ENTERPRISE_SCENARIOS["cache_redis"]
    elif any(kw in topic_lower for kw in ["rate", "limit", "gateway", "microservice"]):
        selected_scenario = ENTERPRISE_SCENARIOS["microservices_ratelimit"]
    elif any(kw in topic_lower for kw in ["order", "checkout", "donhang", "cart", "sales"]):
        selected_scenario = ENTERPRISE_SCENARIOS["ecommerce_checkout"]
    else:
        selected_scenario = ENTERPRISE_SCENARIOS["lms_assessment"]
        
    return f"{base_rules}\n{selected_scenario}".strip()


def resolve_slm_endpoint() -> Optional[str]:
    """
    Checks if a local SLM server (Ollama or vLLM) is active on default ports (11434 or 8000).
    Returns the endpoint URL string or None if unaccessible.
    """
    slm_url = os.getenv("LOCAL_SLM_URL")
    if slm_url:
        return slm_url

    for port, path in [(11434, "/api/version"), (8000, "/v1/models")]:
        url = f"http://127.0.0.1:{port}{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AntigravitySLMCheck"})
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                if resp.status == 200:
                    return f"http://127.0.0.1:{port}"
        except Exception:
            continue

    return None
