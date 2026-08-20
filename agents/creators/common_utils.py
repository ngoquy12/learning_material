import json
import re
import os
import base64
import requests
from typing import Dict, Any, List, Optional
from pathlib import Path
from core.state import AgentState
from core.llm import call_llm
from core.schemas.llm_schemas import CreatorStage1Schema, CreatorStage2Schema
from core.sanitizers import (
    fix_raw_newlines_in_json_strings,
    robust_json_parse,
    ensure_vietnamese_diacritics,
    clean_unwanted_text,
    clean_markdown_formulas,
    normalize_markdown_headers,
    validate_and_clean_forbidden_scope,
)

def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    vietnamese_char_count = sum(1 for c in text if c.lower() in "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ")
    english_char_count = len(text) - vietnamese_char_count
    return int(vietnamese_char_count / 1.5 + english_char_count / 4.0)

def log_agent_tokens(agent_name: str, state: AgentState, output_text: str):
    input_text = f"{state.get('pm_input', '')} {json.dumps(state.get('core_ssot', {}), ensure_ascii=False)}"
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    total_tokens = input_tokens + output_tokens
    savings = int(total_tokens * 0.4)
    print(f"  [Optimizer] {agent_name} Token Cost: {total_tokens} tokens (Input: {input_tokens}, Output: {output_tokens}) | Saved: {savings} tokens via local rules")

def get_base_topic_key(session_id: str) -> str:
    s_id = session_id.upper()
    if "SESSION 01" in s_id: return "orientation"
    elif "SESSION 02" in s_id or "SESSION 03" in s_id: return "intro"
    elif "SESSION 04" in s_id: return "validation"
    elif "SESSION 05" in s_id or "SESSION 06" in s_id or "SESSION 07" in s_id or "SESSION 08" in s_id or "SESSION 09" in s_id: return "crud"
    elif "SESSION 10" in s_id or "SESSION 11" in s_id or "SESSION 12" in s_id or "SESSION 13" in s_id: return "database"
    elif "SESSION 14" in s_id or "SESSION 15" in s_id: return "structure"
    elif "SESSION 16" in s_id or "SESSION 17" in s_id: return "relationship"
    elif "SESSION 18" in s_id or "SESSION 19" in s_id or "SESSION 20" in s_id: return "security"
    elif "SESSION 21" in s_id or "SESSION 22" in s_id: return "middleware"
    elif "SESSION 23" in s_id or "SESSION 24" in s_id: return "upload"
    elif "SESSION 25" in s_id: return "testing"
    return "fallback"

def get_base_topic_key_for_core(session_id: str) -> str:
    s_id = session_id.upper()
    if "SESSION 01" in s_id: return "core_intro"
    elif "SESSION 02" in s_id: return "core_operators"
    elif "SESSION 03" in s_id: return "core_loops"
    elif "SESSION 04" in s_id: return "core_practice"
    elif "SESSION 05" in s_id: return "core_strings"
    elif "SESSION 06" in s_id: return "core_lists"
    elif "SESSION 07" in s_id: return "core_dicts"
    elif "SESSION 08" in s_id: return "core_functions"
    elif "SESSION 09" in s_id: return "core_advanced"
    elif "SESSION 10" in s_id: return "core_midterm"
    return "core_fallback"

def determine_visualization_strategy(lesson_title: str, lesson_details: str, tech_stack: str) -> Dict[str, str]:
    title_lower = (lesson_title or "").lower()
    details_lower = (lesson_details or "").lower()
    combined_text = f"{title_lower} {details_lower}"
    
    if tech_stack.startswith("business/") or tech_stack.startswith("non-it/"):
        return {
            "strategy": "EFFECTIVE_HTML_DIAGRAM",
            "skill_name": "effective_biz_generator",
            "badge": "SƠ ĐỒ TƯ DUY & KIẾN TRÚC EFFECTIVE HTML (Plannotator)",
            "rationale": f"Môn học thuộc khối '{tech_stack}', cần trực quan hóa bằng sơ đồ chiến lược SVG tương tác, thẻ thông tin chi tiết và ma trận quản trị thay vì code tracker."
        }
        
    concept_signals = [
        "tổng quan", "kiến trúc", "architecture", "mô hình", "framework", 
        "quy trình", "workflow", "flowchart", "chiến lược", "strategy", 
        "chuỗi giá trị", "sơ đồ", "khái niệm", "giới thiệu", "overview", 
        "lifecycle", "client-server", "mvc", "agile", "scrum",
        "lộ trình", "phương pháp", "hướng dẫn", "chuẩn bị", "tài liệu", 
        "đánh giá", "roadmap", "method", "methodology", "study plan", 
        "kế hoạch", "milestone", "milestones", "kỹ năng", "tự học"
    ]
    if any(sig in combined_text for sig in concept_signals):
        return {
            "strategy": "EFFECTIVE_HTML_DIAGRAM",
            "skill_name": "effective_biz_generator",
            "badge": "SƠ ĐỒ TƯ DUY & KIẾN TRÚC EFFECTIVE HTML (Plannotator)",
            "rationale": f"Bài học '{lesson_title}' tập trung vào kiến trúc/mô hình tổng quan, phù hợp nhất với sơ đồ toàn màn hình SVG tương tác (Plannotator Effective HTML)."
        }
        
    return {
        "strategy": "INTERACTIVE_CODE_PLAYGROUND",
        "skill_name": "reading_generator",
        "badge": "PHÒNG THÍ NGHIỆM CODE TRỰC QUAN (Interactive Code Playground)",
        "rationale": f"Bài học '{lesson_title}' tập trung vào thực thi mã nguồn, thuật toán hoặc xử lý logic lập trình, cần Code Tracker theo dõi dòng lệnh và Console Log thời gian thực."
    }

def generate_offline_master_content(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, tech_stack: str) -> Dict[str, Any]:
    print(f"  [Creator Fallback] Generating offline mock master content for stack: {tech_stack}...")
    parts = tech_stack.lower().split('/')
    lang = parts[0] if len(parts) > 0 else "generic"
    framework = parts[1] if len(parts) > 1 else "core"
    
    example_code = ""
    if lang == "python":
        if framework == "fastapi":
            example_code = (
                "from fastapi import FastAPI\n"
                "app = FastAPI()\n\n"
                "@app.get('/')\n"
                "def read_root():\n"
                "    return {'message': 'Hello FastAPI'}"
            )
        else:
            example_code = "print('Hello, Python Core!')"
    elif lang in ("typescript", "javascript"):
        if framework == "nestjs":
            example_code = (
                "import { Controller, Get } from '@nestjs/common';\n\n"
                "@Controller()\n"
                "export class AppController {\n"
                "  @Get()\n"
                "  getHello(): string {\n"
                "    return 'Hello NestJS!';\n"
                "  }\n"
                "}"
            )
        elif framework == "react":
            example_code = (
                "import React from 'react';\n"
                "export default function App() {\n"
                "  return <h1>Hello React</h1>;\n"
                "}"
            )
        else:
            example_code = "console.log('Hello, JS/TS Core!');"
    elif lang == "java":
        if framework == "springboot":
            example_code = (
                "import org.springframework.web.bind.annotation.GetMapping;\n"
                "import org.springframework.web.bind.annotation.RestController;\n\n"
                "@RestController\n"
                "public class HelloController {\n"
                "    @GetMapping('/')\n"
                "    public String hello() { return 'Hello Spring!'; }\n"
                "}"
            )
        else:
            example_code = "System.out.println(\"Hello, Java Core!\");"
    else:
        example_code = f"// Hello World for {tech_stack}"

    return {
        "problem": f"### Đặt vấn đề\nHọc viên cần làm quen với {lesson_title} và cấu hình cơ bản cho {tech_stack}.",
        "analysis": f"### Phân tích cơ chế\n{lesson_title} giải quyết các bài toán về {lesson_details or 'kiến trúc phần mềm'}.",
        "solution": f"### Giải pháp kỹ thuật\nSử dụng các thư viện chuẩn và tuân thủ các quy tắc của {tech_stack}.",
        "example": example_code,
        "resolve": f"### Phân tích luồng chạy\nKhi ứng dụng chạy, mã nguồn ví dụ trên sẽ khởi chạy và thực thi.",
        "summary": "### Tổng kết\n- Hiểu rõ cơ chế hoạt động.\n- Tránh cấu hình sai.\n- Áp dụng đúng chuẩn.\n\n### 3 lỗi thường gặp\n1. **Sai cấu hình môi trường**: Lỗi phổ biến nhất.\n2. **Import sai thư viện**: Thiếu package.\n3. **Cú pháp chưa chuẩn**: Vi phạm quy chuẩn code.",
        "self_test": [
            {
                "question": f"Câu hỏi 1: Mục đích chính của {lesson_title} là gì?",
                "answer": f"Mục đích chính là làm quen với kiến thức {lesson_title} và tích hợp vào hệ thống {tech_stack}."
            }
        ],
        "references": [
            {
                "title": f"Tài liệu chính thức của {lang.capitalize()}",
                "url": f"https://www.google.com/search?q={lang}+official+documentation"
            }
        ],
        "quiz": [
            {
                "question": f"Khi khởi tạo cấu hình cho {lesson_title} trong ứng dụng {tech_stack}, cú pháp nào sau đây là bắt buộc và đúng chuẩn?",
                "options": [f"Khai báo theo đúng quy chuẩn đặt tên của {tech_stack}", "Sử dụng từ khóa không thuộc phạm vi hỗ trợ", "Bỏ qua các tham số khởi tạo quan trọng", "Đặt tên biến chứa ký tự bị cấm"],
                "correct_option_index": 0,
                "explanation": f"Cú pháp khai báo trong {tech_stack} bắt buộc tuân thủ đúng quy ước đặt tên và các thành phần khởi tạo chuẩn."
            },
            {
                "question": f"Trong luồng thực thi của {lesson_title}, điều gì xảy ra với khối lệnh khi điều kiện rẽ nhánh chính trả về kết quả False?",
                "options": ["Bỏ qua khối lệnh đó và chuyển sang nhánh tiếp theo", "Dừng toàn bộ chương trình và báo lỗi crash", "Thực thi khối lệnh lặp đi lặp lại vô tận", "Tự động đổi điều kiện thành True"],
                "correct_option_index": 0,
                "explanation": "Khi điều kiện trả về False, luồng chạy sẽ bỏ qua khối lệnh rẽ nhánh đó và chuyển sang kiểm tra nhánh kế tiếp."
            },
            {
                "question": f"Cho đoạn mã nguồn minh họa {lesson_title}. Kết quả giá trị đầu ra trả về khi chương trình chạy hoàn tất là gì?",
                "options": ["Trả về kết quả tính toán chính xác theo đúng nhánh được kích hoạt", "Trả về giá trị chưa khởi tạo do lỗi cú pháp", "Báo lỗi NullPointerException/AttributeError", "Giá trị bị giữ nguyên không thay đổi"],
                "correct_option_index": 0,
                "explanation": "Chương trình thực thi trơn tru và trả về kết quả tính toán chính xác theo đúng nhánh điều kiện được kích hoạt."
            },
            {
                "question": f"Điểm khác biệt bản chất về tính ứng dụng giữa cấu trúc rẽ nhánh cơ bản và cấu trúc nâng cao trong {lesson_title} là gì?",
                "options": ["Cấu trúc nâng cao cho phép xử lý các quy tắc nghiệp vụ đa mốc phức tạp", "Cấu trúc cơ bản chạy nhanh hơn gấp nhiều lần", "Cấu trúc nâng cao chỉ dành cho kiểu dữ liệu số", "Không có bất kỳ điểm khác biệt nào"],
                "correct_option_index": 0,
                "explanation": "Cấu trúc rẽ nhánh nâng cao được thiết kế để phân loại các mốc dữ liệu nghiệp vụ phức tạp."
            },
            {
                "question": f"Khi lập trình viên thiết lập điều kiện trong {lesson_title} nhưng quên không cập nhật biến tham gia điều kiện, bẫy lỗi (Pitfall) nào sẽ xảy ra?",
                "options": ["Chương trình rơi vào bẫy lặp vô tận hoặc giữ nguyên kết quả cũ", "Ngôn ngữ tự động bổ sung câu lệnh cập nhật biến", "Chương trình tự động bỏ qua khối lệnh rẽ nhánh", "Biến tự động giải phóng khỏi bộ nhớ RAM"],
                "correct_option_index": 0,
                "explanation": "Nếu biến tham gia điều kiện không thay đổi giá trị trong thân khối lệnh, biểu thức điều kiện luôn giữ nguyên giá trị dẫn đến lặp vô tận."
            }
        ],
        "lab": {
            "title": f"Lab thực hành {lesson_title}",
            "objectives": [f"Khởi tạo thành công ứng dụng {tech_stack}", "Cấu hình cơ bản"],
            "steps": ["Bước 1: Tạo thư mục", "Bước 2: Viết mã nguồn", "Bước 3: Chạy và kiểm tra"],
            "checklist": ["Ứng dụng chạy không lỗi", "Kết quả trả về đúng mong đợi"]
        },
        "visualizer": {
            "canvas_title": f"Trực quan hóa {lesson_title}",
            "legend_html": "<span class='badge bg-success'>Hoạt động</span>",
            "stats_html": "<div>Trạng thái: OK</div>",
            "code_tracker_html": f"<div class='code-line' id='line-0'>{example_code.splitlines()[0] if example_code else ''}</div>",
            "input_label": "Tham số đầu vào",
            "input_default": "Mặc định",
            "engine_js": (
                "class InteractiveVisualizerEngine {\n"
                "  constructor() { this.interval = null; }\n"
                "  start() {\n"
                "    console.log('Started visualizer');\n"
                "    const l = document.getElementById('line-0');\n"
                "    if(l) l.classList.add('active-line');\n"
                "    const log = document.getElementById('log-messages');\n"
                "    if(log) log.innerHTML += '<p>Visualizer started successfully.</p>';\n"
                "  }\n"
                "  pause() { console.log('Paused'); }\n"
                "  step() { console.log('Step'); }\n"
                "  reset() {\n"
                "    console.log('Reset');\n"
                "    const l = document.getElementById('line-0');\n"
                "    if(l) l.classList.remove('active-line');\n"
                "  }\n"
                "}"
            )
        }
    }

def get_lesson_content(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, attempt_num: int, core_ssot: Dict[str, Any] = None, feedback: str = "", state: AgentState = None) -> Dict[str, Any]:
    if state is not None and "master_content" in state and attempt_num == 1 and not feedback:
        print(f"  [Creator Agent] Reusing cached master_content for {session_id} {lesson_id} (Token Cost Saved!).")
        return state["master_content"]

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "get_lesson_content")
        
    print(f"  [Creator Agent] Dynamically generating lesson content via Two-Stage LLM (Attempt #{attempt_num}) for stack: {tech_stack}...")
    
    viz_decision = determine_visualization_strategy(lesson_title, lesson_details, tech_stack)
    print(f"  [Pedagogical Router] Lesson '{lesson_title}' -> Strategy: {viz_decision['strategy']} ({viz_decision['skill_name']}) | Rationale: {viz_decision['rationale']}")
    
    from agents.creators.reading_creator import classify_reading_type
    reading_type_info = classify_reading_type(lesson_title, lesson_details)
    print(f"  [Smart Reading Router] Classified '{lesson_title}' -> Type: {reading_type_info['type']} ({reading_type_info['name']})")
    
    lessons_learned_prompt = ""
    try:
        from agents.knowledge_memory_agent import get_relevant_memories_for_creator
        scope_hint = "mindmap" if "mindmap" in lesson_title.lower() else "all"
        lessons_learned_prompt = get_relevant_memories_for_creator(
            tech_stack=tech_stack,
            scope=scope_hint,
            limit=10
        )
    except Exception:
        lessons_learned = load_skill_content("lessons_learned")
        if lessons_learned:
            lessons_learned_prompt = (
                "\n--- BÀI HỌC KINH NGHIỆM PHÒNG CHỐNG LỖI TỪ CÁC BÀI TRƯỚC (Lessons Learned) ---\n"
                "Hãy đọc kỹ các bài học này để không lặp lại sai lầm tương tự:\n"
                f"{lessons_learned}\n"
            )

    core_ssot = state.get("core_ssot", {}) if state else {}
    forbidden_scope = core_ssot.get("forbidden_scope", "") if isinstance(core_ssot, dict) else ""
    allowed_scope = core_ssot.get("allowed_scope", "") if isinstance(core_ssot, dict) else ""
    tech_stack_convention = core_ssot.get("tech_stack_convention", "") if isinstance(core_ssot, dict) else ""
    session_type = core_ssot.get("session_type", "") if isinstance(core_ssot, dict) else ""

    pm_boundaries_prompt = f"""
======================================================================
CRITICAL PEDAGOGICAL BOUNDARIES (VIOLATION WILL CAUSE IMMEDIATE FAILURE)
======================================================================
- FORBIDDEN SCOPE: {forbidden_scope or 'Do not use unlearned advanced libraries or syntax'}
  -> 🚨 FATAL ERROR TRIGGER 🚨: You are ABSOLUTELY FORBIDDEN to explain, demonstrate, or use ANY syntax, keywords, functions, or concepts from this list (e.g., if 'break/continue' is forbidden, DO NOT use it in loops). The reviewer WILL instantly reject your output if a single forbidden keyword is found.
- TAUGHT & ALLOWED SCOPE: {allowed_scope or 'Content within current curriculum scope'}
  -> ONLY permitted to use syntax and concepts within this taught scope.
- TECH STACK & CONVENTIONS: {tech_stack_convention or tech_stack}
  -> All code examples and explanations MUST strictly adhere to this technical standard.
======================================================================
"""

    is_coding_type = reading_type_info.get("type") == "CODING_LESSON"
    
    if is_coding_type:
        type_directive = f"""Task: Author a production-grade enterprise HTML reading material for basic programming courses ({tech_stack}).
        
=== MANDATORY 10 PEDAGOGICAL DIRECTIVES (NO EXCEPTIONS) ===

[DIRECTIVE 1 — STRICT 5-SECTION ARCHITECTURE]
The reading material MUST contain exactly 5 sections in the following order:
  Section 1 (problem): Real-World Problem Statement — Enterprise Scenario + Pain Point + New Solution
  Section 2 (analysis): Syntax & Operational Mechanism — Syntax Anatomy + RAM/Stack Diagram + Comparison Card
  Section 3 (solution + example): Practical Examples — Execution Code + Interactive Tracker + Mermaid Flow
  Section 4 (summary + resolve): Production Gotchas — Common Pitfalls + Decision Matrix Table + Anti-patterns
  Section 5 (self_test): Self-Test Assessment — 3 Scenario-based MCQ questions with Anti-AI Shortcuts

[DIRECTIVE 2 — 10-MINUTE MICRO-LEARNING]
- ABSOLUTELY FORBIDDEN to write long, monolithic text paragraphs.
- Every piece of content MUST use Bullet Lists ('- Main point') and Sublists ('  - Supporting details').
- Each point maximum 1-2 concise sentences with core technical keywords in **bold**.
- Total reading length equivalent to 800-1200 words (approx. 10-minute read).

[DIRECTIVE 3 — PROBLEM-FIRST PEDAGOGY]
- Section 1 MUST follow the flow: Real-World Scenario → Pain Point / Legacy Drawbacks → New Solution.
- Put the student in the shoes of a Developer solving a concrete problem (e.g., calculating payroll for 100 employees, filtering order lists).
- ABSOLUTELY FORBIDDEN to start with dry theoretical definitions.

[DIRECTIVE 4 — VISUAL-RICH INTEGRATION]
- Section 1: MUST include a 16:9 SVG diagram (viewBox="0 0 800 450") visualizing the problem context.
- Section 2: MUST include a Syntax Anatomy diagram or RAM/Stack memory diagram via SVG.
- Section 3: MUST include a Mermaid diagram (flowchart TD or sequenceDiagram) describing execution flow.
- Section 4: MUST include a Markdown Decision Matrix table comparing when to use Method A vs Method B.

[DIRECTIVE 5 — GOOD vs BAD PRACTICE CODE PAIRS]
- Section 2 or Section 3: MUST include side-by-side code comparison cards:
  - example_bad: Anti-pattern code with comment "# BAD: [description of negative impact]"
  - example_good: Best practice code with comment "# GOOD: [description of benefits]"

[DIRECTIVE 6 — ANTI-AI SHORTCUT QUESTIONING]
- All self_test assessment questions must reference specific scenario data from the reading material.
- The correct answer can only be found by reading the lesson text, avoiding AI shortcuts.

[DIRECTIVE 7 — DARK TERMINAL CONSOLE OUTPUT]
- All console outpu ts MUST be formatted in a dark code block with '# Output:' prefix.
- ABSOLUTELY FORBIDDEN to format execution outputs as plain bullet points.

[DIRECTIVE 8 — 100% ACCENTED VIETNAMESE OUTPUT]
- TARGET LANGUAGE: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất) for all text, headings, SVG labels, and code comments.
- FORBIDDEN to leave unaccented words like 'Du lieu', 'Hop le', 'Bao loi'.

[DIRECTIVE 9 — LANGUAGE CODING CONVENTIONS]
- Python/C: English snake_case (user_age, calculate_area, total_price). FORBIDDEN unaccented Vietnamese variable names.
- JavaScript/Java/C++: English camelCase (userName, calculateArea, totalPrice).
- FORBIDDEN meaningless names: a, b, temp, x, chieu_dai, bien1.

[DIRECTIVE 10 — HUMAN-LIKE QUALITY STANDARD]
- ABSOLUTELY FORBIDDEN to use text emojis in the reading text.
- FORBIDDEN cliché phrases like 'hãy cùng tìm hiểu', 'như vậy chúng ta thấy', 'thú vị là'.
- FORBIDDEN square bracket tags like [NOTE], [WARNING], [BEST PRACTICE]. Use 'Lưu ý:', 'Cảnh báo:', 'Thực hành tốt:'.
- FORBIDDEN ALL CAPS headings or buttons. Use Sentence case.
- FORBIDDEN referencing W3Schools.
"""
    else:
        type_directive = f"""Task: Author a production-grade enterprise HTML reading material for process, methodology, setup, or theoretical/management courses ({tech_stack}).
        
=== MANDATORY 10 PEDAGOGICAL DIRECTIVES (NO EXCEPTIONS) ===

[DIRECTIVE 1 — STRICT 5-SECTION ARCHITECTURE]
The reading material MUST contain exactly 5 sections in the following order:
  Section 1 (problem): Real-World Problem Statement — Practical Business Scenario + Operational Pain Point + Solution
  Section 2 (analysis): Core Concept, Workflow & Lifecycle — Mermaid Flowchart/Sequence Diagram or Architectural Block Layout + Parameters Table
  Section 3 (solution + example): Step-by-Step Practice Guide — Terminal Commands / YAML Config Snippets / Real Scenario walkthroughs + Detailed Setup Steps
  Section 4 (summary + resolve): Gotchas & Best Practices — Avoided Mistakes + Decision Matrix Table + Process Anti-patterns
  Section 5 (self_test): Self-Test Assessment — 3 Scenario-based MCQ questions with Anti-AI Shortcuts

[DIRECTIVE 2 — 10-MINUTE MICRO-LEARNING]
- ABSOLUTELY FORBIDDEN to write long, monolithic text paragraphs.
- Every piece of content MUST use Bullet Lists ('- Main point') and Sublists ('  - Supporting details').
- Each point maximum 1-2 concise sentences with core technical/business keywords in **bold**.
- Total reading length equivalent to 800-1200 words (approx. 10-minute read).

[DIRECTIVE 3 — PROBLEM-FIRST PEDAGOGY]
- Section 1 MUST follow the flow: Real-World Business Scenario → Operational Pain Point / Drawbacks of Old Approach → Solution.
- Put the student in the shoes of a Manager, PM, Analyst, or Developer solving a concrete workflow/system design problem (e.g. tracking tasks in Scrum, modeling database entities, styling an office document).
- ABSOLUTELY FORBIDDEN to start with dry theoretical definitions.

[DIRECTIVE 4 — VISUAL-RICH INTEGRATION]
- Section 1: MUST include a 16:9 SVG diagram (viewBox="0 0 800 450") visualizing the business scenario or flow.
- Section 2: MUST include a Mermaid Process workflow diagram or Architecture/UML diagram (flowchart TD or sequenceDiagram).
- Section 3: MUST include a step-by-step visual roadmap or process timeline (using clean Markdown tables or list formatting).
- Section 4: MUST include a Markdown comparison table (e.g. Scrum vs Kanban, Git Rebase vs Merge).

[DIRECTIVE 5 — GOOD vs BAD PRACTICE PROCESS PAIRS]
- Section 2 or Section 3: MUST include comparison cards or description panels:
  - example_bad: Common mistake/incorrect configuration with annotation explaining negative consequences.
  - example_good: Recommended practice/correct setup with annotation explaining benefits.

[DIRECTIVE 6 — ANTI-AI SHORTCUT QUESTIONING]
- All self_test assessment questions must reference specific scenario data from the reading material.
- The correct answer can only be found by reading the lesson text, avoiding AI shortcuts.

[DIRECTIVE 7 — DARK TERMINAL CONSOLE OUTPUT]
- All terminal/console configurations or commands MUST be formatted in a dark code block with '# Output:' or '$ terminal_command' prefix.
- ABSOLUTELY FORBIDDEN to format execution outputs as plain bullet points.

[DIRECTIVE 8 — 100% ACCENTED VIETNAMESE OUTPUT]
- TARGET LANGUAGE: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất) for all text, headings, SVG labels, and code comments.
- FORBIDDEN to leave unaccented words like 'Du lieu', 'Hop le', 'Bao loi'.

[DIRECTIVE 9 — NOMENCLATURE & CONVENTIONS]
- Ensure standard industry terminology in English is preserved (e.g. Scrum Master, Backlog, Commit, Pull Request, Pivot Table).
- Avoid translating standardized tech/business terminology into awkward Vietnamese equivalents.

[DIRECTIVE 10 — HUMAN-LIKE QUALITY STANDARD]
- ABSOLUTELY FORBIDDEN to use text emojis in the reading text.
- FORBIDDEN cliché phrases like 'hãy cùng tìm hiểu', 'như vậy chúng ta thấy', 'thú vị là'.
- FORBIDDEN square bracket tags like [NOTE], [WARNING], [BEST PRACTICE]. Use 'Lưu ý:', 'Cảnh báo:', 'Thực hành tốt:'.
- FORBIDDEN ALL CAPS headings or buttons. Use Sentence case.
- FORBIDDEN referencing W3Schools.
"""

    stage1_system_prompt = f"""You are a Senior Instructional Designer and Lead Software Engineer at Rikkei Education.
All generated content MUST strictly comply with the 10 Pedagogical Guidelines of Rikkei Education.

{pm_boundaries_prompt}

{type_directive}

=== MERMAID V10+ DIAGRAM STANDARDS ===
- Arrow labels: Use 'A -->|Label| B'. FORBIDDEN 'A -- Label --> B'.
- Special characters in nodes (/, %, >, <, =, :): MUST wrap in quotes 'A["label // val"]'.
- SequenceDiagram: Participant names must not contain parentheses ().
{lessons_learned_prompt}
"""

    prev_lessons_prompt = ""
    if state and state.get("previous_lessons"):
        prev_lessons_prompt = "\n--- PREVIOUS TAUGHT LESSONS CONTEXT ---\n"
        for prev in state["previous_lessons"]:
            det = prev.get('details') or prev.get('lesson_details', '')
            l_id = prev.get('lesson_id', '')
            l_t = prev.get('title', '')
            prev_lessons_prompt += f"- {l_id}: {l_t} (Content: {det})\n"

    stage1_user_prompt = f"""Author a basic programming reading material following Rikkei Education 10 Directives for:
Session: {session_id} ({session_type})
Lesson: {lesson_id} — Title: {lesson_title}
Lesson Details: {lesson_details}
Expected Output: {expected_output}
Forbidden Scope: {forbidden_scope or 'None'}
Taught & Allowed Scope: {allowed_scope or 'Curriculum concepts'}
Tech Stack & Conventions: {tech_stack_convention or tech_stack}
Reading Type: {reading_type_info['type']} — {reading_type_info['name']}
Type-Specific Guideline: {reading_type_info['prompt_guideline']}
{prev_lessons_prompt}
Reviewer Feedback (if any): {feedback}

Return ONLY raw JSON object with keys: problem_title, problem, analysis_title, analysis, solution_title, solution, example, example_good, example_bad, resolve_title, resolve, summary.
Return only raw JSON.
"""

    stage1_result = {}
    for attempt in range(3):
        response_text = call_llm(
            stage1_system_prompt,
            stage1_user_prompt,
            json_mode=True,
            agent_name=f"Creator_Agent_Stage1_Att{attempt+1}",
            session_id=session_id,
            lesson_id=lesson_id,
            response_schema=CreatorStage1Schema
        )
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()

                stage1_result = robust_json_parse(cleaned)
                if stage1_result.get("problem") and stage1_result.get("analysis"):
                    print(f"  [Creator Agent Stage 1] High-depth reading article generated successfully!")
                    break
            except Exception as e:
                print(f"  [Creator Agent Stage 1 Warning] Attempt {attempt+1} failed: {e}")

    if not stage1_result.get("problem"):
        stage1_result = generate_offline_master_content(session_id, lesson_id, lesson_title, lesson_details, expected_output, tech_stack)

    stage2_system_prompt = f"""You are an Educational Assessment and Testing Engineer at Rikkei Education.
Task: Analyze the complete Stage 1 reading material and generate a high-quality assessment question bank complying with 5 mandatory standards.

=== 5 MANDATORY ASSESSMENT QUESTION STANDARDS ===

[STANDARD 1 — NO ROTE THEORETICAL QUESTIONS]
- ABSOLUTELY FORBIDDEN: 'What is the definition of a function?', 'List types of loops', 'Present the syntax of...'.
- Test ONLY applied understanding and execution results, never memory regurgitation.

[STANDARD 2 — REAL-WORLD SCENARIO PRIORITIZATION]
- Each question MUST follow 1 of 3 formats:
  (a) Scenario: Put student in developer's shoes solving a specific technical problem.
  (b) Application: Select / write / analyze appropriate code snippet or data structure.
  (c) Practical Impact: If X happens, what will occur / what action should be taken?
- Good Example: 'Select the appropriate data structure to store a student roster and perform efficient insertions.'

[STANDARD 3 — 100% ADHERENCE TO READING CONTENT]
- Questions MUST be strictly derived from Stage 1 reading content, context, and examples.
- FORBIDDEN to introduce concepts from other unlearned topics.
- FORBIDDEN to ask about out-of-scope topics: {forbidden_scope or 'none'}.

[STANDARD 4 — STRICT OBJECTIVE DOMAIN PRESENTATION (NO CONTEXT REFERENCING)]
- ABSOLUTELY FORBIDDEN to use intermediate context or source referral phrases in questions, answer choices, or explanations: 'in the slide', 'on slide', 'lecture slide', 'slide mentions', 'in the lecture', 'according to the lecture', 'according to the video', 'in the video', 'from the instructor', 'instructor said', 'According to Section ...', 'in enterprise scenario ...', 'in the scenario', 'from an unknown source', etc.
- All questions, options, and explanations MUST be stated 100% objectively, independently, and professionally as standard domain knowledge.

[STANDARD 5 — HIGH-QUALITY MULTIPLE CHOICE (MCQ & HOMOGENEITY)]
- 4 options (A/B/C/D): 1 correct answer, 3 sophisticated distractors based on common student misconceptions or syntax traps.
- OPTION HOMOGENEITY (CRITICAL): All 4 choices (A, B, C, D) MUST have comparable text length, grammatical structure, and detail level.
- FORBIDDEN: 'All of the above are correct' or 'All of the above are incorrect'.
- RANDOM CORRECT INDEX: Randomly distribute correct answer positions across A, B, C, D (indices 0, 1, 2, 3) for each question.
- explanation: Detailed objective technical analysis explaining why the correct answer is right and why distractors are wrong (never write 'According to Section 2...' or 'In the slide...').
- TARGET OUTPUT LANGUAGE: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất), no emojis, no ALL CAPS.

[STANDARD 6 — PURE TECH STACK CONTEXT (ANTI-HALLUCINATION)]
- When creating enterprise scenarios, YOU MUST ONLY use pure {tech_stack} syntax and tools.
- ABSOLUTELY FORBIDDEN to hallucinate or introduce external web frameworks (e.g., FastAPI, Django, Flask, React, Express) unless explicitly stated in the lesson title.

[STANDARD 7 — CODE FORMATTING IN QUIZ]
- Whenever a question or option contains a code block, you MUST format it properly using Markdown code fences (```).
- You MUST preserve exact indentation (using spaces or \\t) and line breaks (using \\n) within the code blocks so that it renders correctly on Markdown-supported platforms (like LMS platforms reading from Excel).
- Example: "Cho đoạn mã sau:\\n```python\\nfor i in range(5):\\n    print(i)\\n```\\nKết quả in ra là gì?"

=== ASSESSMENT GENERATION PRINCIPLES ===
1. SCENARIO-BASED: Put student in concrete professional developer scenario derived from reading material.
2. ANTI-AI SHORTCUT: Correct answer must reference specific scenario data in the reading material.
3. 4-OPTION MCQ (A/B/C/D): Exactly 4 options — 1 correct, 3 plausible distractors.
4. PLAUSIBLE DISTRACTORS: Distractors must reflect actual common student mistakes (never use 'All of the above').
5. STRICT SCOPE GUARANTEE: Never ask about future topics in forbidden scope: {forbidden_scope or 'none'}.
6. PURE TECH STACK: Never hallucinate web frameworks (FastAPI/Django/React) for generic {tech_stack} lessons.
7. CODE FORMATTING: Use Markdown code blocks (```) with explicit \\n and indentation for any code snippets inside JSON string fields.
8. OUTPUT LANGUAGE: 100% Accented Vietnamese with full diacritics.
"""
    stage2_user_prompt = f"""Full Stage 1 Reading Material (use context from this to generate assessment questions):
{json.dumps(stage1_result, ensure_ascii=False)[:5000]}

Lesson Metadata:
- Title: {lesson_title}
- Target Tech Stack: {tech_stack}
- Curriculum Details: {lesson_details[:300]}
- FORBIDDEN Scope: {forbidden_scope or 'none'}

Question Generation Workflow:
Step 1: Identify 5 main sections of the reading (problem, analysis, solution, resolve, summary).
Step 2: For each section, select 1 concrete scenario/example from the reading text to formulate a question.
Step 3: Formulate questions adhering to 1 of 3 types: Situational / Application / Reasoning.
Step 4: Explicitly specify which reading section contains the answer (exact section name).

Return ONLY the raw JSON object below (no markdown wrappers):
{{
    "self_test": [
        {{
            "id": "q1",
            "type": "situational",
            "question": "[MANDATORY] Start with scenario: 'You are working at [real-world enterprise context from reading]...' then ask what the student must DO / SELECT / ANALYZE?",
            "reading_section": "Exact title of reading section containing answer (e.g., 'Phần 1 — Đặt vấn đề', 'Phần 3 — Ví dụ minh họa', 'Bảng Decision Matrix')",
            "options": [
                "Option A — Correct (based on precise knowledge in reading)",
                "Option B — Incorrect (common student misconception)",
                "Option C — Incorrect (distractor: plausible but wrong context)",
                "Option D — Incorrect (distractor: related to future or out-of-scope topics)"
            ],
            "correct_index": 0,
            "explanation": "Detailed explanation why A is correct — CITE EXACT section/paragraph in reading."
        }},
        {{
            "id": "q2",
            "type": "application",
            "question": "[Application Type] 'Select / Apply / Write [concept from reading] for situation [specific context]?'",
            "reading_section": "Title of reading section containing answer",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_index": 1,
            "explanation": "Detailed explanation referencing reading section."
        }},
        {{
            "id": "q3",
            "type": "reasoning",
            "question": "[Reasoning Type] 'If [specific situation from reading], what will occur / how will you handle it?'",
            "reading_section": "Title of reading section containing answer",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_index": 2,
            "explanation": "Detailed explanation referencing reading section."
        }}
    ],
    "references": [
        {{"title": "Title of official authoritative reference documentation (no W3Schools)", "url": "https://docs.python.org/3/"}}
    ],
    "quiz": [
        {{
            "question": "Scenario-based MCQ question 1 (enterprise context, never rote definition)?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_option_index": 0,
            "explanation": "Detailed explanation referencing reading material."
        }},
        {{
            "question": "Scenario-based MCQ question 2?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_option_index": 1,
            "explanation": "Detailed explanation."
        }},
        {{
            "question": "Scenario-based MCQ question 3?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_option_index": 2,
            "explanation": "Detailed explanation."
        }},
        {{
            "question": "Scenario-based MCQ question 4?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_option_index": 3,
            "explanation": "Detailed explanation."
        }}
    ],
    "lab": {{
        "title": "Practical Lab title tied to real-world enterprise scenario",
        "objectives": ["Specific skill student will master after Lab"],
        "steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
        "checklist": ["[ ] Quantitative verifiable assessment criteria"]
    }},
    "visualizer": {{
        "canvas_title": "Interactive visualizer board title",
        "legend_html": "Color status legend HTML",
        "stats_html": "Stats counter cards HTML",
        "code_tracker_html": "<div class='code-line' id='line-0'># Code tracker line...</div>",
        "input_label": "Input field label",
        "input_default": "Default test value",
        "engine_js": "class InteractiveVisualizerEngine {{ constructor() {{}} init() {{}} start() {{}} pause() {{}} step() {{}} reset() {{}} }}"
    }}
}}
Return only raw JSON.
"""


    stage2_result = {}
    try:
        response_text_s2 = call_llm(
            stage2_system_prompt,
            stage2_user_prompt,
            json_mode=True,
            agent_name=f"Creator_Agent_Stage2",
            session_id=session_id,
            lesson_id=lesson_id,
            response_schema=CreatorStage2Schema
        )
        if response_text_s2:
            cleaned_s2 = response_text_s2.strip()
            if cleaned_s2.startswith("```json"):
                cleaned_s2 = cleaned_s2[7:]
            if cleaned_s2.startswith("```"):
                cleaned_s2 = cleaned_s2[3:]
            if cleaned_s2.endswith("```"):
                cleaned_s2 = cleaned_s2[:-3]
            cleaned_s2 = cleaned_s2.strip()
            stage2_result = robust_json_parse(cleaned_s2)
            print(f"  [Creator Agent Stage 2] Aux components generated successfully via Structured Outputs!")
    except Exception as e:
        print(f"  [Creator Agent Stage 2 Warning] Failed to generate Stage 2 components: {e}")

    final_result = dict(stage1_result)
    final_result["self_test"] = stage2_result.get("self_test") or [
        {"question": f"Trong kịch bản quản lý dự án với {tech_stack} ở bài đọc, hãy phân tích rủi ro hệ thống khi không áp dụng {lesson_title} và đề xuất giải pháp xử lý.", "answer": f"Thiếu {lesson_title} dễ gây ra xung đột phiên bản hoặc sai lệch dữ liệu. Việc áp dụng đúng quy trình giúp cô lập thay đổi và bảo vệ tính toàn vẹn hệ thống."},
        {"question": f"Dựa vào ví dụ mã nguồn/lệnh CLI trong bài đọc, hãy chỉ ra điểm không tối ưu trong kịch bản cũ và giải thích các bước tái cấu trúc chuẩn Best Practice.", "answer": f"Kịch bản cũ chưa rà soát trạng thái hoặc thiếu cờ phạm vi. Cần bổ sung bước kiểm tra và sử dụng đúng tham số theo quy chuẩn công nghệ."},
        {"question": f"Phân tích lỗi Gotcha phổ biến được đề cập ở Phần 4 và trình bày cơ chế kiểm tra tự động để ngăn ngừa sự cố trên môi trường Production.", "answer": f"Lỗi Gotcha thường phát sinh do thao tác thiếu kiểm soát. Cần áp dụng danh sách kiểm tra và các công cụ rà soát tự động trước khi triển khai."}
    ]
    final_result["references"] = stage2_result.get("references") or [
        {"title": f"Tài liệu hướng dẫn chính thức {tech_stack.upper()}", "url": "https://docs.python.org/3/"},
        {"title": f"Trang chủ tài nguyên đào tạo Rikkei Education", "url": "https://rikkei.edu.vn"}
    ]
    final_result["quiz"] = stage2_result.get("quiz") or []
    final_result["lab"] = stage2_result.get("lab") or {"title": f"Lab {lesson_title}", "objectives": [], "steps": [], "checklist": []}
    
    final_result, _ = validate_and_clean_forbidden_scope(final_result, forbidden_scope)

    if state is not None:
        state["master_content"] = final_result
    return final_result


def get_lesson_dir(state: AgentState) -> Path:
    course_dir_name = state.get("course_dir_name")
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")

    output_base_dir = Path(__file__).resolve().parent.parent.parent / "output" / "pms"
    if course_dir_name:
        clean_name = course_dir_name.replace("pms/", "").strip()
        course_dir = output_base_dir / clean_name
    else:
        course_dir = output_base_dir / "default_course"
    
    full_curr_str = state.get("full_curriculum", "[]")
    try:
        sessions = json.loads(full_curr_str)
    except Exception:
        sessions = []
        
    session_title = ""
    lesson_title = ""
    for s in sessions:
        if s.get("session_id") == session_id:
            session_title = s.get("title", "")
            for l in s.get("lessons", []):
                if l.get("lesson_id") == lesson_id:
                    lesson_title = l.get("title", "")
                    break
            break
            
    def sanitize_folder_name(name: str) -> str:
        name = name.replace("&", "va").replace("%", "").replace("^", "").replace("#", "")
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    session_prefix = session_id
    session_full = f"{session_id} - {session_title}"
    session_dir = course_dir / sanitize_folder_name(session_full)
    if course_dir.exists():
        for item in course_dir.iterdir():
            if item.is_dir():
                if item.name == sanitize_folder_name(session_full):
                    session_dir = item
                    break
                if item.name == session_prefix or item.name.startswith(session_prefix + " ") or item.name.startswith(session_prefix + "-"):
                    session_dir = item
                    break
                    
    lesson_prefix = lesson_id
    lesson_full = f"{lesson_id} - {lesson_title}"
    lesson_dir = session_dir / sanitize_folder_name(lesson_full)
    if session_dir.exists():
        for item in session_dir.iterdir():
            if item.is_dir():
                if item.name == sanitize_folder_name(lesson_full):
                    lesson_dir = item
                    break
                if item.name == lesson_prefix or item.name.startswith(lesson_prefix + " ") or item.name.startswith(lesson_prefix + "-"):
                    lesson_dir = item
                    break
                    
    return lesson_dir

def generate_image_api(prompt_text: str, image_path) -> bool:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        try:
            base_url = os.getenv("GEMINI_BASE_URL")
            if base_url:
                url = f"{base_url.rstrip('/')}/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "prompt": prompt_text,
                    "n": 1,
                    "size": "1024x576"
                }
                response = requests.post(url, headers=headers, json=data, timeout=90)
                if response.status_code == 200:
                    resp_json = response.json()
                    img_data = resp_json.get("data", [])
                    if img_data and "b64_json" in img_data[0]:
                        img_b64 = img_data[0]["b64_json"]
                        with open(image_path, "wb") as f:
                            f.write(base64.b64decode(img_b64))
                        print(f"  [Image Generator] Saved diagram to: {image_path}")
                        return True
                    elif img_data and "url" in img_data[0]:
                        img_url = img_data[0]["url"]
                        img_resp = requests.get(img_url, timeout=30)
                        if img_resp.status_code == 200:
                            with open(image_path, "wb") as f:
                                f.write(img_resp.content)
                            print(f"  [Image Generator] Saved downloaded diagram to: {image_path}")
                            return True

            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "instances": [
                    {
                        "prompt": prompt_text
                    }
                ],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "16:9",
                    "outputMimeType": "image/png"
                }
            }
            response = requests.post(url, headers=headers, json=data, timeout=90)
            if response.status_code == 200:
                resp_json = response.json()
                if "predictions" in resp_json and len(resp_json["predictions"]) > 0:
                    img_b64 = resp_json["predictions"][0]["bytesBase64Encoded"]
                    with open(image_path, "wb") as f:
                        f.write(base64.b64decode(img_b64))
                    print(f"  [Image Generator] Saved diagram to: {image_path}")
                    return True
                else:
                    print(f"  [Image Generator Warning] Response did not contain images: {resp_json}")
            else:
                print(f"  [Image Generator Warning] API status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"  [Image Generator Warning] Dynamic image generation error: {e}")
    return False

def process_mindmap_images(markmap_content: str, state: AgentState) -> str:
    brackets = re.findall(r"\[(?:Prompt|Tạo ảnh):\s*([^\]]+)\]", markmap_content)
    asterisks = re.findall(r"\*Prompt tạo ảnh:\s*([^*]+)\*", markmap_content, flags=re.IGNORECASE)

    all_prompts = []
    seen = set()
    for p in brackets + asterisks:
        p_clean = p.strip()
        if p_clean not in seen:
            seen.add(p_clean)
            all_prompts.append(p_clean)

    if not all_prompts:
        return markmap_content

    images_dir = None
    if state and isinstance(state, dict) and "images_dir" in state and state["images_dir"]:
        images_dir = Path(state["images_dir"])
        images_dir.mkdir(parents=True, exist_ok=True)
    else:
        try:
            lesson_dir = get_lesson_dir(state)
            images_dir = lesson_dir / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"  [Image Processing Error] Could not resolve lesson/images directory: {e}")
            return markmap_content

    new_content = markmap_content
    for idx, prompt_text in enumerate(all_prompts, 1):
        image_name = f"mindmap_img_{idx}.png"
        image_path = images_dir / image_name

        print(f"  [Mindmap Image] Processing prompt {idx}: '{prompt_text[:50]}...' -> {image_path}")

        force_rebuild = state.get("force_rebuild", False) if isinstance(state, dict) else False
        if force_rebuild or not image_path.exists():
            success = generate_image_api(prompt_text, image_path)
            if not success or not image_path.exists():
                print(f"  [Mindmap Image Warning] Imagen 3 image generation failed/unavailable for prompt '{prompt_text[:50]}...'. Continuing without image tag.")
                search_bracket = r"\[(?:Prompt|Tạo ảnh):\s*" + re.escape(prompt_text) + r"\]"
                new_content = re.sub(search_bracket, "", new_content)
                search_asterisk = r"\*Prompt tạo ảnh:\s*" + re.escape(prompt_text) + r"\*"
                new_content = re.sub(search_asterisk, "", new_content, flags=re.IGNORECASE)
                continue

        search_bracket = r"\[(?:Prompt|Tạo ảnh):\s*" + re.escape(prompt_text) + r"\]"
        new_content = re.sub(search_bracket, f"![](../images/{image_name})", new_content)

        search_asterisk = r"\*Prompt tạo ảnh:\s*" + re.escape(prompt_text) + r"\*"
        new_content = re.sub(search_asterisk, f"![](../images/{image_name})", new_content, flags=re.IGNORECASE)

    return new_content

__all__ = [
    "estimate_tokens",
    "log_agent_tokens",
    "get_base_topic_key",
    "get_base_topic_key_for_core",
    "determine_visualization_strategy",
    "generate_offline_master_content",
    "get_lesson_content",
    "get_lesson_dir",
    "fix_raw_newlines_in_json_strings",
    "robust_json_parse",
    "ensure_vietnamese_diacritics",
    "clean_unwanted_text",
    "clean_markdown_formulas",
    "normalize_markdown_headers",
    "validate_and_clean_forbidden_scope",
    "generate_image_api",
    "process_mindmap_images",
]

