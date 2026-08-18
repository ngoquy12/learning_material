# agents/creators/blueprint_creator.py
from core.llm import call_llm
from core.state import AgentState, require_tech_stack
from agents.creators.common_utils import fix_raw_newlines_in_json_strings, robust_json_parse
from agents.creators.common_utils import get_lesson_dir
import json
import os

def blueprint_creator_agent(state: AgentState) -> AgentState:
    """
    Blueprint Creator Agent:
    Generates a structured intermediate JSON "Blueprint" containing:
    1. A unified real-world scenario (business context)
    2. Explanations and raw snippets of key concepts
    3. Three progressive hands-on coding/scripting examples (3.1, 3.2, 3.3)
    4. Anti-patterns and gotchas (common errors, bad vs good code samples)
    
    This Blueprint serves as the SSOT for derived creator agents (HTML, Quiz, Lab).
    """
    session_id = state.get("session_id", "Session")
    lesson_id = state.get("lesson_id", "")
    core_ssot = state.get("core_ssot", {})
    tech_stack = require_tech_stack(state, "blueprint_creator_agent")
    
    allowed_scope = ", ".join(state.get("allowed_scope", []))
    forbidden_scope = ", ".join(state.get("forbidden_scope", []))
    
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    # Retrieve previous memories from KMA if available to prevent repeating bugs
    try:
        from agents.knowledge_memory_agent import get_relevant_memories_for_creator
        memories_context = get_relevant_memories_for_creator(tech_stack, scope="all", limit=5)
    except Exception:
        memories_context = ""

    sys_prompt = f"""You are a Lead Curriculum Architect & Senior Engineer at Rikkei Education.
Your task is to draft a comprehensive, unified learning resource blueprint (Bản phác thảo học liệu) for a single lesson.
This blueprint serves as the single source of truth for the entire lesson's resources (HTML Reading material, Quiz questions, and Hands-on Practical Labs).

STRICT DIRECTIVES:
1. UNIFIED BUSINESS SCENARIO: You must establish exactly ONE unified concrete real-world business scenario (e.g., E-commerce shopping cart, ticket booking, library catalog). All progressive examples (3.1, 3.2, 3.3), syntax templates, and gotchas must revolve around this exact scenario and use consistent naming conventions.
2. SCOPE BOUNDARIES:
   - Allowed Scope (already taught): {allowed_scope or 'Basic fundamentals'}
   - Forbidden Scope (future lessons): {forbidden_scope or 'Advanced frameworks/features'}
   - Tech Stack: {tech_stack} (Use clean, PEP 8/industry-standard English variable/function naming).
3. 100% Vietnamese Explanations: All explanatory texts, requirements, descriptions, and comments in code must be in 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất).
{memories_context}

Generate ONLY a raw JSON object containing the following structure:
{{
  "lesson_slug": "lowercase-hyphen-slug",
  "lesson_title": "Clean Lesson Title (No 'Lesson 0X' prefix)",
  "real_world_scenario": {{
    "name": "Tên kịch bản (ví dụ: Hệ thống Giỏ hàng E-commerce)",
    "description": "Mô tả chi tiết kịch bản doanh nghiệp và bài toán thực tế cần giải quyết xuyên suốt bài học."
  }},
  "key_concepts": [
    {{
      "concept_name": "Tên khái niệm (ví dụ: Vòng lặp for)",
      "description": "Giải thích trực quan ngắn gọn về cơ chế hoạt động của khái niệm này.",
      "raw_code_snippet": "Đoạn code ví dụ cơ bản (English syntax, Vietnamese comments)"
    }}
  ],
  "progressive_examples": [
    {{
      "example_id": "3.1",
      "title": "Ví dụ 3.1: Cơ bản",
      "requirement": "Yêu cầu bài toán thực hành nhỏ.",
      "raw_code": "Mã nguồn đầy đủ có comment tiếng Việt."
    }},
    {{
      "example_id": "3.2",
      "title": "Ví dụ 3.2: Nâng cấp nghiệp vụ",
      "requirement": "Yêu cầu nghiệp vụ bổ sung để nâng cấp độ khó.",
      "raw_code": "Mã nguồn đầy đủ nâng cấp từ 3.1."
    }},
    {{
      "example_id": "3.3",
      "title": "Ví dụ 3.3: Ứng dụng thực tế doanh nghiệp",
      "requirement": "Yêu cầu nghiệp vụ phức tạp hơn xử lý lỗi/edge cases cấp doanh nghiệp.",
      "raw_code": "Mã nguồn đầy đủ hoàn thiện nhất."
    }}
  ],
  "gotchas_and_errors": [
    {{
      "error_name": "Lỗi thường gặp (ví dụ: Lặp vô hạn/Sai chỉ số)",
      "explanation": "Giải thích chi tiết tại sao lỗi xảy ra và ảnh hưởng thế nào.",
      "code_bad": "Mã nguồn sai lỗi",
      "code_good": "Mã nguồn đúng khắc phục"
    }}
  ]
}}
Return only raw JSON.
"""

    user_prompt = f"""Author a structured lesson blueprint for:
Lesson Topic: {lesson_id} - {lesson_title}
Curriculum Details: {lesson_details}
Expected Outcomes / Deliverables: {expected_output}
"""

    print(f"\n[Blueprint Creator] ✏️ Đang sinh bản phác thảo JSON Blueprint cho {session_id} - {lesson_id}...")

    try:
        res = call_llm(
            sys_prompt, user_prompt,
            json_mode=True,
            agent_name="Blueprint_Creator",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if res:
            cleaned = res.strip()
            f_b = cleaned.find("{")
            l_b = cleaned.rfind("}")
            if f_b != -1 and l_b != -1:
                cleaned = cleaned[f_b:l_b+1].strip()
            cleaned = fix_raw_newlines_in_json_strings(cleaned)
            parsed = robust_json_parse(cleaned)
            
            if parsed.get("real_world_scenario") and parsed.get("progressive_examples"):
                state["lesson_blueprint"] = parsed
                print(f"  [Blueprint Creator] ✅ Đã tạo xong Blueprint cho {lesson_id}!")
                
                # Write to disk as draft
                try:
                    lesson_dir = get_lesson_dir(state)
                    blueprint_sub = lesson_dir / "Blueprint"
                    blueprint_sub.mkdir(parents=True, exist_ok=True)
                    with open(blueprint_sub / "lesson_blueprint.json", "w", encoding="utf-8") as f:
                        json.dump(parsed, f, ensure_ascii=False, indent=2)
                except Exception as disk_err:
                    print(f"  [Blueprint Creator Warning] Không ghi được blueprint nháp lên đĩa: {disk_err}")
                
                return state
    except Exception as e:
        print(f"  [Blueprint Creator Error] Tạo blueprint bằng LLM lỗi: {e}")

    # Fallback structure if LLM fails
    state["lesson_blueprint"] = {
        "lesson_slug": "lesson-fallback",
        "lesson_title": lesson_title,
        "real_world_scenario": {
            "name": "Kịch bản mẫu",
            "description": "Hệ thống quản lý thông tin."
        },
        "key_concepts": [],
        "progressive_examples": [
            {"example_id": "3.1", "title": "Ví dụ 3.1", "requirement": "Yêu cầu cơ bản", "raw_code": "# Fallback code"},
            {"example_id": "3.2", "title": "Ví dụ 3.2", "requirement": "Yêu cầu nâng cấp", "raw_code": "# Fallback code"},
            {"example_id": "3.3", "title": "Ví dụ 3.3", "requirement": "Yêu cầu doanh nghiệp", "raw_code": "# Fallback code"}
        ],
        "gotchas_and_errors": []
    }
    return state
