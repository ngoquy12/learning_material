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
    
    mindmap_dir = session_dir / "Mindmap"
    mindmap_dir.mkdir(exist_ok=True)
    
    print(f"\n  ---> [Session Mindmap Agent] Đang tạo Sơ đồ Tư duy Tổng hợp Session: {session_id} - {session_title}...")
    
    image_skill = load_skill_content("image_prompt_standard")
    mindmap_skill = load_skill_content("mindmap_generator")
    
    system_prompt = f"""You are a Lead Master System Mindmap Architect at Rikkei Education.
Your task is to synthesize a complete, highly-condensed, and visually structured SESSION-LEVEL MASTER MINDMAP (Session-Level Markmap Markdown) covering all core lessons and concepts within the Session.

MANDATORY MINDMAP DIRECTIVES:
1. Strictly follow the rules, branching hierarchy, and constraints specified in the Mindmap Generator Skill:
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
- Target Output Language: All mindmap nodes, objectives, problems, and notes MUST be written in 100% Accented Vietnamese.
- The mindmap must be extremely concise, rich in technical depth but visually clean, with no long paragraphs.
- Level 1 Heading (#) MUST contain ONLY the clean content/topic title, stripping any prefixes like "{session_id} - " or "{session_id}: ". For example, if session is "Session 05 - Vòng lặp", the H1 MUST be "# Vòng lặp".
- Level 2 Headings (##) MUST follow this strict sequence:
  1. First branch MUST be "## Mục tiêu bài học" (outlining 3-4 generalized goals in Accented Vietnamese).
  2. Second branch MUST be "## Đặt tình huống" (outlining real-world business context/problem statement).
  3. Subsequent branches MUST represent the actual child lessons or core technical topics of this session.
- Level 3 Headings (###) MUST be dynamic and ultra-short (e.g. use "### Cú pháp" instead of "### Cú pháp lập trình", and "### Lưu ý" instead of "### Các lưu ý thực chiến").
- For difficult concepts or workflow control, embed a standard English image generation prompt matching: *Prompt tạo ảnh: A clean 2D flat vector technical illustration of [logic]. Main title in concise Accented Vietnamese. Strictly NO text emojis. 16:9 aspect ratio...*
- ABSOLUTELY FORBIDDEN to use any text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶) anywhere in the mindmap content.
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
        if not markmap_content.startswith("```markmap"):
            if "```markmap" in markmap_content:
                idx = markmap_content.find("```markmap")
                markmap_content = markmap_content[idx:].strip()
            else:
                markmap_content = "```markmap\n" + markmap_content
                
        lines = markmap_content.splitlines()
        if not lines[-1].strip() == "```":
            lines.append("```")
        markmap_content = "\n".join(lines)
    else:
        markmap_content = f"```markmap\n# {session_id}: {session_title}\n## Tổng quan Session\n- Nội dung sơ đồ tư duy tổng hợp Session.\n```"

    # Post-process image prompts inside the mindmap and generate 2D flat vector diagrams
    state_mock = {
        "course_dir_name": session_dir.name, 
        "technology_stack": tech_stack,
        "images_dir": session_dir / "images"
    }
    processed_content = process_mindmap_images(markmap_content, state_mock)
    
    out_file = mindmap_dir / "session_mindmap.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(processed_content)
        
    print(f"  [Success] Saved Session Mindmap: {out_file}")
    return processed_content
