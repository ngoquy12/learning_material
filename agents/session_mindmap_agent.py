# agents/session_mindmap_agent.py
import os
import re
from pathlib import Path
from typing import Dict, Any
from core.llm import call_llm
from core.skills import load_skill_content
from agents.creators.mindmap_creator import process_mindmap_images

def generate_session_mindmap(
    session_id: str,
    session_title: str,
    session_dir_path: str,
    tech_stack: str,
    previous_lessons_text: str
) -> str:
    """
    Session-Level Mindmap Agent:
    Tự động biên soạn Sơ đồ tư duy Tổng hợp cấp Session (Session-Level Mindmap)
    bao quát toàn bộ kiến thức của các bài học trong Session.
    Lưu vào thư mục: Session XX/Mindmap/session_mindmap.md
    """
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)
    
    mindmap_dir = session_dir / "Sơ đồ tư duy"
    if not mindmap_dir.exists() and (session_dir / "Mindmap").exists():
        mindmap_dir = session_dir / "Mindmap"
    mindmap_dir.mkdir(exist_ok=True)
    
    print(f"\n  ---> [Session Mindmap Agent] Đang tạo Sơ đồ Tư duy Tổng hợp Session: {session_id} - {session_title}...")
    
    image_skill = load_skill_content("image_prompt_standard")
    mindmap_skill = load_skill_content("session_mindmap_compiler")
    
    system_prompt = f"""You are a Lead Master System Mindmap Architect at Rikkei Education.
Your task is to synthesize a complete, highly-condensed, and visually structured SESSION-LEVEL MASTER MINDMAP (Session-Level Markmap Markdown) covering all core lessons and concepts within the Session.

MANDATORY MINDMAP DIRECTIVES:
1. Strictly follow the rules, branching hierarchy, and constraints specified in the Session Mindmap Compiler Skill:
{mindmap_skill}

2. Visual Design & Image Prompts Standard:
For complex architecture/flow concepts, embed image prompt nodes adhering strictly to the blueprint formula below:
{image_skill}
"""

    user_prompt = f"""Generate the Master Markmap Mindmap for Session:
Session ID: {session_id}
Session Title: {session_title}
Target Technology Stack: {tech_stack}

--- SESSION LESSONS & CURRICULUM SYLLABUS ---
{previous_lessons_text}

MANDATORY OUTPUT CONTRACT:
- Return ONLY a single Markdown code block: ` ```markmap ... ` ```.
- Target Output Language: All mindmap nodes and notes MUST be written in 100% Accented Vietnamese.
- The mindmap must be extremely concise, rich in technical depth but visually clean, with no long paragraphs.
- Level 1 Heading (#) MUST contain ONLY the clean content/topic title, stripping any prefixes like "{session_id} - " or "{session_id}: ". For example, if session is "Session 04 - Toán tử", the H1 MUST be "# Toán tử".
- Level 2 Headings (##) MUST represent the child lessons within this session, ending with a final "## Liên kết hệ thống" connection branch.
- Each Lesson branch MUST contain exactly these 4 sub-branches (###):
  1. "### Khái niệm & Vai trò" (brief definition and technical purpose)
  2. "### Cú pháp & Giải nghĩa" (standard syntax code block with brief explanations of components)
  3. "### Ví dụ thực hành" (runnable example of 5-8 lines max using realistic variable names, no 'a', 'b', 'x', 'temp')
  4. "### Lưu ý triển khai" (Gotchas, common mistakes, style guide formatting, NO AI clichés like "thực chiến" or "gotcha")
- The final "## Liên kết hệ thống" branch MUST summarize the logical dependency flow, input-process-output data mapping, and overall cross-lesson integration.
- ABSOLUTELY FORBIDDEN to include "Mục tiêu bài học", "Bài toán", or "Đặt tình huống" branches anywhere in the mindmap.
- ABSOLUTELY FORBIDDEN to use any text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶) anywhere in the mindmap content.
- STRICT KNOWLEDGE SCOPING: Only reference concepts within allowed taught lessons; do not leak unlearned future topics.
"""

    markmap_content = call_llm(
        system_prompt,
        user_prompt,
        json_mode=False,
        agent_name="Session_Mindmap_Agent",
        session_id=session_id,
        lesson_id="SESSION_LEVEL"
    )
    
    if markmap_content:
        markmap_content = markmap_content.strip()
        if markmap_content.startswith("```markdown"):
            markmap_content = markmap_content[11:].strip()
        elif markmap_content.startswith("```markmap"):
            markmap_content = markmap_content[10:].strip()
        elif markmap_content.startswith("```"):
            markmap_content = markmap_content[3:].strip()
            
        if markmap_content.endswith("```"):
            markmap_content = markmap_content[:-3].strip()
    else:
        markmap_content = f"# {session_title}\n## Tổng quan Session\n- Nội dung sơ đồ tư duy tổng hợp Session."

    # Post-process image prompts inside the mindmap and generate 2D flat vector diagrams
    state_mock = {
        "course_dir_name": session_dir.name, 
        "technology_stack": tech_stack,
        "images_dir": session_dir / "images"
    }
    processed_content = process_mindmap_images(markmap_content, state_mock)
    
    # Ensure final output is clean Pure Markdown without outer code fences
    processed_content = processed_content.strip()
    if processed_content.startswith("```markmap"):
        processed_content = processed_content[10:].strip()
    if processed_content.startswith("```markdown"):
        processed_content = processed_content[11:].strip()
    if processed_content.startswith("```"):
        processed_content = processed_content[3:].strip()
    if processed_content.endswith("```"):
        processed_content = processed_content[:-3].strip()
    
    out_file = mindmap_dir / "mindmap.md" if (mindmap_dir.name == "Sơ đồ tư duy") else mindmap_dir / "session_mindmap.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(processed_content)
        
    print(f"  [Success] Saved Session Mindmap: {out_file}")
    return processed_content
