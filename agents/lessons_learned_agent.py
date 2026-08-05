import os
import json
from typing import Dict, Any, List
from core.state import AgentState

def lessons_learned_agent(state: AgentState) -> AgentState:
    """
    Lessons Learned Agent:
    Analyzes the reviewer rejects in state['review_logs'] (UX_Reviewer, Academic_Reviewer, Sandbox_Agent),
    compares the bad drafts with the final approved artifacts,
    extracts concrete technical rules, and updates/appends them to the lessons_learned skill.
    """
    review_logs = state.get("review_logs", [])
    if not review_logs:
        # Nothing to learn if there were no failures
        return state

    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "lessons_learned_agent")

    print(f"\n[Lessons_Learned_Agent] Analyzing {len(review_logs)} feedback logs to extract new rules...")

    # Formulate error logs representation
    log_texts = []
    for idx, log in enumerate(review_logs):
        log_texts.append(f"Feedback #{idx+1} from {log.get('source', 'Reviewer')}:\n{log.get('feedback', '')}")
    logs_formatted = "\n\n".join(log_texts)

    # We gather the final approved content as reference
    approved_example = state.get("master_content", {}).get("example", "")
    if not approved_example:
        approved_example = "Xem mã nguồn trong tệp HTML bài đọc."

    # Call LLM to extract rule
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")

    rule_text = ""
    if gemini_key or openai_key:
        from core.llm import call_llm
        system_prompt = (
            "You are a Lead Curriculum Quality Engineer & System Architect at Rikkei Education. "
            "Your task is to extract actionable, highly specific technical prevention rules "
            "from reviewer feedback logs to update the collective agent memory repository."
        )
        user_prompt = f"""An error occurred during curriculum generation for the following lesson:
- Technology Stack: {tech_stack}
- Lesson Context: {lesson_id} - {core_ssot.get('session_title', '')}

Reviewer Feedback Logs:
{logs_formatted}

Approved Reference Source Code / Content:
```
{approved_example}
```

Formulate EXACTLY ONE concise, highly specific technical rule in Accented Vietnamese to prevent this error in future generations.
The rule MUST be actionable and technically explicit (specifying library names, exact methods, or parameters), avoiding vague generalizations.
Standard example for python/core: "Khi khai báo vòng lặp duyệt qua danh sách, không thực hiện thay đổi kích thước danh sách (append/remove) trực tiếp trong vòng lặp để tránh lỗi IndexError."
Standard example for web stack: "Khi cấu hình kết nối Cơ sở dữ liệu, luôn đóng phiên làm việc (session) trong khối finally hoặc dùng Context Manager để tránh rò rỉ kết nối."

Return ONLY the single rule statement line without markdown wrappers or conversational filler.
"""
        try:
            response = call_llm(system_prompt, user_prompt, agent_name="Lessons_Learned_Agent", session_id=session_id, lesson_id=lesson_id)
            if response:
                rule_text = response.strip()
                # Clean up any potential surrounding quotes or markdown formatting
                if rule_text.startswith('"') and rule_text.endswith('"'):
                    rule_text = rule_text[1:-1].strip()
                if rule_text.startswith("`") and rule_text.endswith("`"):
                    rule_text = rule_text[1:-1].strip()
        except Exception as e:
            print(f"  [Lessons Learned Agent Warning] LLM call failed: {e}")

    # Fallback if LLM is offline or failed
    if not rule_text:
        # Generate a rule based on the error source
        error_sources = list(set([str(log.get('source')) for log in review_logs if log.get('source')]))
        sources_str = ", ".join(error_sources)
        rule_text = f"Carefully verify syntax and layout issues originating from {sources_str} for {lesson_title}."

    # Write/Append to skills/lessons_learned/SKILL.md
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_dir = os.path.join(base_path, "skills", "lessons_learned")
    os.makedirs(skill_dir, exist_ok=True)
    skill_file = os.path.join(skill_dir, "SKILL.md")

    # Clean lesson title for the link
    lesson_title_clean = lesson_title.replace("/", "_").replace("\\", "_").replace(":", "-")
    l_folder_name = f"{lesson_id} - {lesson_title_clean}" if lesson_id else lesson_title_clean

    new_entry = f"* **[{tech_stack.upper()}]**: {rule_text} | Source: [[{l_folder_name}]]"

    # Read existing rules to prevent duplicates
    existing_content = ""
    if os.path.exists(skill_file):
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                existing_content = f.read()
        except Exception as e:
            print(f"  [Lessons Learned Agent Warning] Read skill file failed: {e}")

    # Initialize skill if not present
    if not existing_content:
        existing_content = f"""---
name: lessons_learned
description: Repository of accumulated technical error prevention rules extracted from prior agent generations.
---

# Enterprise Technical Lessons Learned Repository

Repository of accumulated technical error prevention rules extracted by prior agent generations following reviewer feedback:

## Accumulated Technical Rules
"""

    # Check if the rule is already in the file or if we already linked this lesson
    link_pattern = f"[[{l_folder_name}]]"
    if link_pattern in existing_content:
        print(f"  [Lessons Learned Agent] Rule for lesson '{l_folder_name}' already registered. Skipping append.")
    else:
        # Append new entry to the end of the file
        if not existing_content.endswith("\n"):
            existing_content += "\n"
        existing_content += f"{new_entry}\n"
        try:
            with open(skill_file, "w", encoding="utf-8") as f:
                f.write(existing_content)
            print(f"  [Lessons Learned Agent] Successfully logged lessons learned: {rule_text}")
        except Exception as e:
            print(f"  [Lessons Learned Agent Error] Failed to write skill file: {e}")

    return state
