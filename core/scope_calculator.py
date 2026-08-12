# core/scope_calculator.py
"""
Dynamic Scope Calculator & Knowledge Boundary Validator.
Calculates cumulative allowed concepts and future forbidden concepts dynamically
from syllabus metadata for ANY technology stack (Python, Java, C, C++, JS, TS, C#, Go, Rust, SQL...)
without hardcoding language-specific assumptions or fixed keywords.
"""

import re
from typing import Dict, Any, List, Set, Tuple

# Dynamic Stack-Specific High-Level Framework Registry for Core/CLI Isolation Guards
STACK_FORBIDDEN_FRAMEWORKS: Dict[str, List[str]] = {
    "python": ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "django", "flask", "celery", "alembic"],
    "java": ["springboot", "spring", "hibernate", "jpa", "maven", "gradle"],
    "javascript": ["express", "nestjs", "react", "vue", "angular", "nextjs", "prisma"],
    "typescript": ["nestjs", "express", "prisma", "typeorm"],
    "c": ["qt", "gtk"],
    "cpp": ["qt", "boost"],
    "csharp": ["aspnet", "entityframework", "blazor"],
    "golang": ["gin", "fiber", "gorm"],
    "php": ["laravel", "symfony"]
}

def get_forbidden_frameworks_for_stack(tech_stack: str) -> List[str]:
    """
    Dynamically returns forbidden high-level web/ORM frameworks for a Core/CLI technology stack.
    If stack is explicitly a framework (e.g. typescript/nestjs), framework injection is allowed.
    """
    if not tech_stack:
        return []
        
    tech_lower = tech_stack.lower().strip()
    
    # If the course is explicitly a Web Framework course (e.g. nestjs, springboot, fastapi), don't ban frameworks
    is_framework_course = any(fw in tech_lower for fw in ["nestjs", "springboot", "fastapi", "express", "django", "laravel"])
    if is_framework_course:
        return []
        
    # Find matching stack key (sort by length descending so 'javascript' matches before 'java')
    for stack_key in sorted(STACK_FORBIDDEN_FRAMEWORKS.keys(), key=len, reverse=True):
        if stack_key in tech_lower:
            return STACK_FORBIDDEN_FRAMEWORKS[stack_key]
            
    return []

def calculate_lesson_scope_contract(
    syllabus: Dict[str, Any],
    current_session_idx: int,
    current_lesson_idx: int
) -> Tuple[Set[str], Set[str]]:
    """
    Dynamically computes allowed concepts (lessons 1..N) and forbidden concepts (lessons N+1..end)
    based on input syllabus tree metadata across any technology stack.
    """
    sessions = syllabus.get("sessions", [])
    allowed_concepts: Set[str] = set()
    forbidden_concepts: Set[str] = set()
    
    current_reached = False
    
    for s_idx, session in enumerate(sessions):
        lessons = session.get("lessons", [])
        for l_idx, lesson in enumerate(lessons):
            concepts = set()
            # Extract concepts from lesson metadata (topics, keywords, title, allowed_scope, forbidden_scope)
            if "title" in lesson:
                concepts.add(str(lesson["title"]).lower().strip())
            if "lesson_title" in lesson:
                concepts.add(str(lesson["lesson_title"]).lower().strip())
            if "keywords" in lesson and isinstance(lesson["keywords"], list):
                concepts.update(str(k).lower().strip() for k in lesson["keywords"] if k)
            if "topics" in lesson and isinstance(lesson["topics"], list):
                concepts.update(str(t).lower().strip() for t in lesson["topics"] if t)
            if "forbidden_scope" in lesson and lesson["forbidden_scope"]:
                # Parse forbidden concepts from syllabus column metadata
                raw_forb = str(lesson["forbidden_scope"]).replace("CẤM:", "").replace("TUYỆT ĐỐI CẤM:", "").strip()
                for item in re.split(r"[,;\n]", raw_forb):
                    item_clean = item.strip().lower()
                    if item_clean:
                        forbidden_concepts.add(item_clean)
                
            is_current = (s_idx == current_session_idx and l_idx == current_lesson_idx)
            
            if not current_reached:
                allowed_concepts.update(concepts)
                if is_current:
                    current_reached = True
            else:
                forbidden_concepts.update(concepts)
                
    # Filter out forbidden concepts that overlap with allowed concepts
    final_forbidden = set()
    for f_concept in forbidden_concepts:
        is_allowed = False
        for a_concept in allowed_concepts:
            if f_concept in a_concept or a_concept in f_concept:
                is_allowed = True
                break
        if not is_allowed:
            final_forbidden.add(f_concept)
            
    return allowed_concepts, final_forbidden

def validate_session_cadence_and_lesson_bounds(syllabus: Dict[str, Any]) -> List[str]:
    """
    Pedagogical Reviewer for Session Cadence & Lesson Counts.
    Ensures Theory Sessions have <= 4 Lessons (Cognitive Load Guard).
    """
    warnings = []
    sessions = syllabus.get("sessions", [])
    
    for s_idx, session in enumerate(sessions, 1):
        s_title = session.get("session_title") or session.get("title") or f"Session {s_idx}"
        s_code = str(session.get("session_code", "")).upper()
        lessons = session.get("lessons", [])
        
        if s_code == "THEORY" and len(lessons) > 4:
            warnings.append(
                f"[Cognitive Load Warning] {s_title} chứa {len(lessons)} Lessons (> 4 Lessons). "
                f"Khuyên dùng: Gộp các bài nhỏ lại để đảm bảo sinh viên không bị ngợp."
            )
            
    return warnings

def validate_text_against_scope(
    text: str, 
    forbidden_scope: Set[str], 
    tech_stack: str = ""
) -> List[str]:
    """
    Checks if given content text contains forbidden concepts from future syllabus lessons
    or unrequested high-level frameworks for core/CLI courses.
    Returns list of matched forbidden keywords.
    """
    if not text:
        return []
        
    text_lower = text.lower()
    # Strip disclaimer/prohibition sentences so that sentences like "Chú ý: Không dùng dict/list" do not trigger false positive.
    cleaned_text = re.sub(r'(?:cấm|không|tuyệt đối|chưa được|lưu ý|chú ý|note|forbid|forbidden|without|do not use)[^.\n]*', '', text_lower, flags=re.IGNORECASE)
    
    violations = []
    
    # 1. Check syllabus-derived forbidden scope
    if forbidden_scope:
        for concept in forbidden_scope:
            c_clean = concept.strip().lower()
            if len(c_clean) < 2:
                continue
            pattern = r"\b" + re.escape(c_clean) + r"\b"
            if re.search(pattern, cleaned_text):
                violations.append(concept)
                
    # 2. Check stack-specific forbidden frameworks
    if tech_stack:
        forbidden_frameworks = get_forbidden_frameworks_for_stack(tech_stack)
        for fw in forbidden_frameworks:
            pattern = r"\b" + re.escape(fw) + r"\b"
            if re.search(pattern, cleaned_text):
                violations.append(f"{fw} (framework nâng cao của {tech_stack.upper()})")
                
    return violations
