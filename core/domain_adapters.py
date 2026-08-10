# core/domain_adapters.py
"""
Domain-Specific Prompt Adapters for Elearning Content Factory.
Injects industrial coding standards and enterprise business scenarios into System Prompts.
Supports Local SLM (vLLM / Ollama) endpoints for offline fine-tuned model execution.
"""

import os
import urllib.request
import json
from typing import Dict, Any, Optional

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
    elif any(kw in stack_lower for kw in ["docker", "k8s", "devops", "ci/cd"]):
        return DOMAIN_RULES["devops/docker"]
        
    return ""


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
