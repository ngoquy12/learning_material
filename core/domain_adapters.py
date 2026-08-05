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
