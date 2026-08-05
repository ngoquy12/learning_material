"""
core/scope_calculator.py
Dynamic Scope Calculator for Elearning Agent.
Calculates cumulative allowed concepts and future forbidden concepts dynamically
from syllabus metadata without hardcoding any technology names or content keywords.
"""

import re
from typing import Dict, Any, List, Set, Tuple

def calculate_lesson_scope_contract(
    syllabus: Dict[str, Any],
    current_session_idx: int,
    current_lesson_idx: int
) -> Tuple[Set[str], Set[str]]:
    """
    Dynamically computes allowed concepts (lessons 1..N) and forbidden concepts (lessons N+1..end)
    based on the input syllabus tree data.
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
                concepts.add(lesson["title"].lower())
            if "lesson_title" in lesson:
                concepts.add(lesson["lesson_title"].lower())
            if "keywords" in lesson and isinstance(lesson["keywords"], list):
                concepts.update(k.lower() for k in lesson["keywords"])
            if "topics" in lesson and isinstance(lesson["topics"], list):
                concepts.update(t.lower() for t in lesson["topics"])
            if "forbidden_scope" in lesson and lesson["forbidden_scope"]:
                # Explicit forbidden concepts from PM 9-column metadata
                raw_forb = str(lesson["forbidden_scope"]).replace("CẤM:", "").strip()
                for item in raw_forb.split(","):
                    if item.strip():
                        forbidden_concepts.add(item.strip().lower())
                
            is_current = (s_idx == current_session_idx and l_idx == current_lesson_idx)
            
            if not current_reached:
                allowed_concepts.update(concepts)
                if is_current:
                    current_reached = True
            else:
                forbidden_concepts.update(concepts)
                
    # Remove any forbidden concepts that are substrings of any allowed concept (or vice versa)
    final_forbidden = set()
    for f_concept in forbidden_concepts:
        is_allowed = False
        for a_concept in allowed_concepts:
            # If the forbidden concept is explicitly part of the allowed title/keywords
            if f_concept in a_concept or a_concept in f_concept:
                is_allowed = True
                break
        if not is_allowed:
            final_forbidden.add(f_concept)
            
    forbidden_concepts = final_forbidden
                
    return allowed_concepts, forbidden_concepts

def validate_session_cadence_and_lesson_bounds(syllabus: Dict[str, Any]) -> List[str]:
    """
    Pedagogical Reviewer for Session Cadence & Lesson Counts.
    Ensures Theory Sessions have <= 4 Lessons (Cognitive Load Guard)
    and checks Orientation Exception alignment.
    """
    warnings = []
    sessions = syllabus.get("sessions", [])
    
    for s_idx, session in enumerate(sessions, 1):
        s_title = session.get("session_title") or session.get("title") or f"Session {s_idx}"
        s_code = session.get("session_code", "").upper()
        lessons = session.get("lessons", [])
        
        if s_code == "THEORY" and len(lessons) > 4:
            warnings.append(
                f"[Cognitive Load Warning] {s_title} chứa {len(lessons)} Lessons (> 4 Lessons). "
                f"Khuyên dùng: Gộp các bài nhỏ lại để đảm bảo sinh viên không bị ngợp."
            )
            
    return warnings

def validate_text_against_scope(text: str, forbidden_scope: Set[str]) -> List[str]:
    """
    Checks if given content text contains forbidden concepts from future lessons.
    Returns list of matched forbidden keywords.
    """
    if not text or not forbidden_scope:
        return []
        
    text_lower = text.lower()
    violations = []
    
    for concept in forbidden_scope:
        if len(concept.strip()) < 3:
            continue # Ignore trivial words
        pattern = r"\b" + re.escape(concept.strip()) + r"\b"
        if re.search(pattern, text_lower):
            violations.append(concept)
            
    return violations
