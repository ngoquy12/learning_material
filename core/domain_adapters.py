# core/domain_adapters.py
"""
Domain-Specific Prompt Adapters for Elearning Content Factory.
Injects industrial coding standards into System Prompts based on tech stack.
"""

DOMAIN_RULES = {
    "python/core": """
=== INDUSTRY CODING ADAPTER: PYTHON CORE ===
1. Strict PEP 8 Compliance: 4-space indentation, snake_case function/variable naming, PascalCase for classes.
2. Type Hints Required: All function signatures must include type annotations (e.g., def add(a: int, b: int) -> int:).
3. Explicit Error Handling: Avoid bare `except:`, use specific exceptions (e.g. `ValueError`, `KeyError`).
4. Modern Python 3.10+ Features: Favor type union syntax `int | str` over `Optional[Union[int, str]]`.
""",

    "python/fastapi": """
=== INDUSTRY CODING ADAPTER: PYTHON FASTAPI & BACKEND ===
1. Pydantic v2 Models: Use BaseModel with explicit Field descriptions and type validations.
2. Dependency Injection: Use `Depends()` for database sessions and authentication guards.
3. Asynchronous Handlers: Prefer `async def` for I/O bound endpoints.
4. HTTP Status Codes: Always pass explicit status codes (e.g., `status_code=status.HTTP_201_CREATED`).
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
1. ANSI SQL Standard: Capitalize SQL keywords (`SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`).
2. Normalization & Constraints: Enforce 3NF, declare Primary Keys (`PK`) and Foreign Keys (`FK`) explicitly.
3. Security: Highlight Parameterized Queries to prevent SQL Injection attacks.
4. Indexing: Mention B-Tree index optimization for high-frequency filter columns.
""",

    "devops/docker": """
=== INDUSTRY CODING ADAPTER: DEVOPS & DOCKER ===
1. Multi-Stage Builds: Use multi-stage Dockerfiles to minimize production image footprint.
2. Security Practices: Never run container as root user (`USER 1000:1000`).
3. Explicit Tagging: Avoid `latest` tag; pin base image versions (e.g. `python:3.10-slim`).
4. Layer Caching: Copy dependencies before source code to optimize build cache.
"""
}

def get_domain_rules(tech_stack: str) -> str:
    """
    Returns industrial coding rules matching the provided tech stack.
    """
    if not tech_stack:
        return DOMAIN_RULES["python/core"]
        
    stack_lower = tech_stack.lower().strip()
    
    for key, rules in DOMAIN_RULES.items():
        if key in stack_lower:
            return rules
            
    if "python" in stack_lower:
        return DOMAIN_RULES["python/core"]
    elif any(kw in stack_lower for kw in ["html", "css", "js", "react", "frontend", "vue"]):
        return DOMAIN_RULES["web/frontend"]
    elif any(kw in stack_lower for kw in ["sql", "postgres", "mysql", "db", "database"]):
        return DOMAIN_RULES["database/sql"]
    elif any(kw in stack_lower for kw in ["docker", "k8s", "devops", "ci/cd"]):
        return DOMAIN_RULES["devops/docker"]
        
    return DOMAIN_RULES["python/core"]
