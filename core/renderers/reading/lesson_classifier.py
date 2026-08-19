"""
core/renderers/reading/lesson_classifier.py
Reading Material Lesson Type Classifier and Pedagogical Routing Guidelines.
"""

from typing import Dict, Any

def classify_reading_type(lesson_title: str, lesson_details: str) -> Dict[str, str]:
    """Classify a lesson's reading type and return metadata including prompt_guideline.
    Called by common_utils.py and generators to route LLM prompt generation.
    MUST always include: type, name, prompt_guideline.
    """
    text_to_check = (lesson_title + " " + lesson_details).lower()
    
    orientation_signals = ["tổng quan lộ trình", "định hướng", "tổng quan môn học", "demo sản phẩm", "lộ trình và demo"]
    is_orientation = any(sig in text_to_check for sig in orientation_signals)
    
    if is_orientation:
        return {
            "type": "ORIENTATION_LESSON",
            "name": lesson_title,
            "prompt_guideline": (
                "Author a Session 01 Orientation lesson titled 'Tổng quan lộ trình và Demo sản phẩm'.\n"
                "Structure the document into exactly 3 clear main sub-sections:\n"
                "1. '1. Tổng quan nội dung & Lộ trình môn học': Summarize course modules and learning milestones as a visual connected Timeline component (<div class='timeline-track'>...) or a structured list.\n"
                "2. '2. Phương pháp học tập hiệu quả & Kiến thức tiền đề': Detail proactive learning strategies, AI Pair-Programming workflow (Cursor/Windsurf), and prerequisite skills/knowledge required.\n"
                "3. '3. Demo sản phẩm dự án đầu ra': Present demo specifications, features, and outcomes of the capstone/mini-project students will build upon course completion.\n"
                "STRICT DIRECTIVES:\n"
                "- ABSOLUTELY FORBIDDEN to generate code demo snippets, executable sandboxes, or empty code blocks for this lesson.\n"
                "- Flexible titles and layout allowed (do NOT force rigid 5-section IDs).\n"
                "- Use 100% Accented Vietnamese for text and 2D Flat Vector Infographics/Timeline visual components."
            )
        }
        
    coding_keywords = ["python", "javascript", "c++", "cpp", "java", "sql", "react", "html", "css", "c#", "typescript", "programming", "code", "syntax", "array", "variable", "loop", "function", "struct", "class", "pointer", "oop"]
    
    is_coding = any(kw in text_to_check for kw in coding_keywords)
    
    if is_coding:
        return {
            "type": "CODING_LESSON",
            "name": lesson_title,
            "prompt_guideline": (
                "Author a programming/code-based lesson. Focus on syntax anatomy, RAM/Stack diagrams, "
                "side-by-side good/bad practice code blocks, and executable code snippets that run in the interactive playground. "
                "Enforce case-sensitive naming conventions (camelCase/snake_case) in English, and clear Vietnamese output for explanation text."
            )
        }
    else:
        return {
            "type": "PROCESS_OR_THEORY_LESSON",
            "name": lesson_title,
            "prompt_guideline": (
                "Author a process, tool, setup, or theoretical/management lesson (e.g. Git, Agile/Scrum, Excel, System Design, UML). "
                "DO NOT force code sandboxes or code files if not applicable. Instead, focus on Mermaid process workflows (flowchart/sequence), "
                "comparison matrix tables, step-by-step UI guides, configuration file templates, or terminal command sequences. "
                "Ensure logical flowcharts and operational lifecycle diagrams are present."
            )
        }
