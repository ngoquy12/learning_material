from core.llm import call_llm
from agents.creators.common_utils import fix_raw_newlines_in_json_strings, robust_json_parse

def mini_project_generator_agent(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, tech_stack: str, core_ssot: dict) -> dict:
    """
    Mini Project Generator Agent:
    Generates full Mini Project assets for 'Mini Project' session types:
    1. srs_spec (Software Requirements Specification HTML)
    2. architecture_mermaid (Mermaid ERD / Class / Data Flow Diagram)
    3. starter_code (Modular Python starter code with TODOs following PEP 8)
    4. project_rubric (100-point Professional Evaluation Rubric)
    """
    forbidden_scope = core_ssot.get("forbidden_scope", "") if isinstance(core_ssot, dict) else ""
    allowed_scope = core_ssot.get("allowed_scope", "") if isinstance(core_ssot, dict) else ""
    tech_stack_convention = core_ssot.get("tech_stack_convention", "") if isinstance(core_ssot, dict) else ""

    sys_prompt = f"""You are a Lead Software Architect & Enterprise Project Designer at Rikkei Education.
Your task is to author a complete ENTERPRISE MINI PROJECT RESOURCE PACKAGE for Session: '{session_id}: {lesson_title}'.

STRICT KNOWLEDGE SCOPE & CONVENTION DIRECTIVES:
- FORBIDDEN SCOPE: {forbidden_scope or 'Unlearned advanced libraries/syntax'}
- TAUGHT SCOPE: {allowed_scope or 'Prior taught curriculum concepts'}
- CONVENTIONS: {tech_stack_convention or tech_stack} (PEP 8, English snake_case identifiers)

Generate ONLY a raw JSON object containing 4 fields:
{{
    "srs_title": "Mini Project Software Requirements Specification Title in Accented Vietnamese",
    "srs_spec": "SRS spec in Markdown Bullet Lists & Sublists: 1. Enterprise Context, 2. Functional Specs, 3. Non-functional Specs, 4. Expected Console/CLI Interface.",
    "architecture_mermaid": "```mermaid\\ngraph TD\\n  %% Enterprise Data Flow Architecture Diagram...\\n```",
    "starter_code": "# Starter source code framework following Best Practice PEP 8 (English snake_case) with # TODO comments...",
    "project_rubric": "### BẢNG RUBRIC CHẤM ĐIỂM DỰ ÁN MINI PROJECT (TỔNG 100 ĐIỂM)\\n- Core Logic (40pts):\\n- Code Quality & PEP 8 (30pts):\\n- Error Handling & Exceptions (20pts):\\n- Clean Code & Optimization (10pts):"
}}
Return only raw JSON.
"""
    user_prompt = f"""Author Enterprise Mini Project resource package for Session: {session_id} - {lesson_title}
Curriculum Details from PM: {lesson_details}
Expected Output: {expected_output}"""

    try:
        res = call_llm(sys_prompt, user_prompt, json_mode=True, agent_name="Mini_Project_Generator", session_id=session_id, lesson_id=lesson_id)
        if res:
            cleaned = res.strip()
            f_b = cleaned.find("{")
            l_b = cleaned.rfind("}")
            if f_b != -1 and l_b != -1:
                cleaned = cleaned[f_b:l_b+1].strip()
            cleaned = fix_raw_newlines_in_json_strings(cleaned)
            parsed = robust_json_parse(cleaned)
            if parsed.get("srs_spec") or parsed.get("starter_code"):
                print(f"  [Mini Project Generator] Successfully compiled SRS, Architecture, Starter Code & Rubric for {session_id}!")
                return parsed
    except Exception as e:
        print(f"  [Mini Project Generator Warning] LLM generation failed: {e}")

    return {
        "srs_title": f"Dự án Mini Project {lesson_title}",
        "srs_spec": f"### Đặc tả Yêu cầu Mini Project {lesson_title}\n- Xây dựng ứng dụng hoàn chỉnh theo yêu cầu.",
        "architecture_mermaid": "```mermaid\ngraph TD\n  A[Input User] --> B[Processing Engine]\n  B --> C[Output Console]\n```",
        "starter_code": "# Starter Code PEP 8\ndef main():\n    # TODO: Implement mini project logic\n    pass\n\nif __name__ == '__main__':\n    main()\n",
        "project_rubric": "### Rubric Chấm điểm Mini Project (100đ)\n- Chức năng cốt lõi: 40đ\n- Mã nguồn chuẩn PEP 8: 30đ\n- Xử lý ngoại lệ: 20đ\n- Clean Code & Structural Layout: 10đ"
    }
