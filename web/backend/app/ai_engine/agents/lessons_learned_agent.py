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
    tech_stack = state.get("technology_stack", "python/fastapi")

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
            "Bạn là Kỹ sư Trưởng kiêm Chuyên gia Thiết kế Giáo trình tại Rikkei Education. "
            "Nhiệm vụ của bạn là đúc rút các quy tắc kỹ thuật thực tiễn từ nhật ký sửa đổi lỗi "
            "để bổ sung quy tắc phòng chống lỗi cho các Agent thế hệ sau."
        )
        user_prompt = f"""Đã xảy ra lỗi trong quá trình tự động sinh học liệu cho bài học sau:
- Công nghệ: {tech_stack}
- Bài học: {lesson_id} - {lesson_title}

Nhật ký lỗi/Feedback sửa lỗi từ Reviewer:
{logs_formatted}

Mã nguồn/Nội dung đã sửa đổi và được phê duyệt (Approved):
```
{approved_example}
```

Hãy phát biểu DUY NHẤT một câu quy tắc kỹ thuật ngắn gọn, cụ thể bằng tiếng Việt để phòng tránh lỗi này trong tương lai.
Quy tắc phải thiết thực, chi tiết kỹ thuật rõ ràng (ví dụ: tên thư viện, phương thức, cấu hình cụ thể), tránh nói chung chung.
Ví dụ chuẩn: "Khi sử dụng FastAPI với SQLAlchemy, luôn cấu hình async_sessionmaker với expire_on_commit=False để tránh lỗi GreenletDetached khi truy cập thuộc tính trễ."

Chỉ trả về duy nhất dòng quy tắc đó. Không có lời chào hay lời dẫn giải nào khác.
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
        rule_text = f"Cần lưu ý kiểm thử kỹ các lỗi phát sinh từ {sources_str} liên quan đến cú pháp và định dạng của {lesson_title}."

    # Write/Append to skills/lessons_learned/SKILL.md
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_dir = os.path.join(base_path, "skills", "lessons_learned")
    os.makedirs(skill_dir, exist_ok=True)
    skill_file = os.path.join(skill_dir, "SKILL.md")

    # Clean lesson title for the link
    lesson_title_clean = lesson_title.replace("/", "_").replace("\\", "_").replace(":", "-")
    l_folder_name = f"{lesson_id} - {lesson_title_clean}" if lesson_id else lesson_title_clean

    new_entry = f"* **[{tech_stack.upper()}]**: {rule_text} | Trích từ bài [[{l_folder_name}]]"

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
description: Kho tri thức đúc rút kinh nghiệm phòng chống lỗi kỹ thuật từ các Agent thế hệ trước.
---

# 🧠 Kho tri thức bài học kinh nghiệm (Lessons Learned)

Dưới đây là danh sách các quy tắc chặn lỗi được các Agent thế hệ trước đúc rút ra sau khi giải quyết các phản hồi lỗi từ Reviewer:

## 📌 Quy tắc kỹ thuật tích lũy
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
