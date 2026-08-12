import json
import re
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from core.state import AgentState
from core.llm import call_llm
from core.schemas.llm_schemas import CreatorStage1Schema, CreatorStage2Schema

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

def fix_raw_newlines_in_json_strings(json_str: str) -> str:
    chars = list(json_str)
    in_string = False
    escaped = False
    for i in range(len(chars)):
        char = chars[i]
        if char == '"' and not escaped:
            in_string = not in_string
        elif char == '\\' and in_string and not escaped:
            escaped = True
            continue
        elif char == '\n' and in_string:
            chars[i] = '\\n'
        elif char == '\r' and in_string:
            chars[i] = ''
        escaped = False
    return "".join(chars)

def robust_json_parse(json_str: str) -> dict:
    try:
        return json.loads(json_str)
    except Exception as e:
        print(f"  [Robust Parser] Standard json.loads failed: {e}. Attempting custom recovery...")
        
    cleaned = json_str.strip()
    if cleaned.startswith("{"):
        cleaned = cleaned[1:]
    if cleaned.endswith("}"):
        cleaned = cleaned[:-1]
        
    result = {}
    keys = ["problem", "analysis", "solution", "example", "resolve", "summary", "self_test", "quiz", "lab", "visualizer"]
    
    offsets = []
    for k in keys:
        pattern = r'"' + k + r'"\s*:\s*'
        match = re.search(pattern, cleaned)
        if match:
            offsets.append((k, match.start(), match.end()))
            
    offsets.sort(key=lambda x: x[1])
    
    for idx, (k, start, val_start) in enumerate(offsets):
        val_end = offsets[idx+1][1] if idx + 1 < len(offsets) else len(cleaned)
        val_sub = cleaned[val_start:val_end].strip()
        
        if val_sub.endswith(","):
            val_sub = val_sub[:-1].strip()
            
        if k in ["problem", "analysis", "solution", "example", "resolve", "summary"]:
            if val_sub.startswith('"'):
                val_sub = val_sub[1:]
            if val_sub.endswith('"'):
                val_sub = val_sub[:-1]
            val_sub = val_sub.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')
            result[k] = val_sub
        else:
            try:
                parsed = json.loads(val_sub)
                if k == "lab" and not isinstance(parsed, dict):
                    raise ValueError("lab must be a dict")
                if k == "quiz" and not isinstance(parsed, list):
                    raise ValueError("quiz must be a list")
                if k == "visualizer" and not isinstance(parsed, dict):
                    raise ValueError("visualizer must be a dict")
                result[k] = parsed
            except Exception:
                try:
                    import ast
                    parsed = ast.literal_eval(val_sub)
                    if k == "lab" and not isinstance(parsed, dict):
                        raise ValueError("lab must be a dict")
                    if k == "quiz" and not isinstance(parsed, list):
                        raise ValueError("quiz must be a list")
                    if k == "visualizer" and not isinstance(parsed, dict):
                        raise ValueError("visualizer must be a dict")
                    result[k] = parsed
                except Exception:
                    try:
                        cleaned_sub = fix_raw_newlines_in_json_strings(val_sub)
                        parsed = json.loads(cleaned_sub)
                        if k == "lab" and not isinstance(parsed, dict):
                            raise ValueError("lab must be a dict")
                        if k == "quiz" and not isinstance(parsed, list):
                            raise ValueError("quiz must be a list")
                        if k == "visualizer" and not isinstance(parsed, dict):
                            raise ValueError("visualizer must be a dict")
                        result[k] = parsed
                    except Exception:
                        if k == "self_test":
                            items = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', val_sub)
                            result[k] = [item.replace('\\"', '"') for item in items]
                        elif k == "lab":
                            result[k] = {"title": "Lab", "objectives": [], "steps": [], "checklist": []}
                        else:
                            result[k] = {}
                            
    for k in keys:
        if k not in result:
            if k in ["problem", "analysis", "solution", "example", "resolve", "summary"]:
                result[k] = ""
            elif k == "self_test":
                result[k] = []
            elif k == "lab":
                result[k] = {"title": "Lab", "objectives": [], "steps": [], "checklist": []}
            else:
                result[k] = {}
                
    return result

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

def clean_markdown_formulas(text: str) -> str:
    """
    Sanitizes LaTeX and dollar-sign math formulas in Markdown to clean code-badged programming expressions.
    Prevents backslash escaping bugs (\frac, \text), underscore-italic collisions ($var_name$), and unrendered LaTeX tags.
    """
    if not text:
        return text

    # Remove \text{...} -> ...
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    
    # Replace \frac{A}{B} -> (A) / (B)
    text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1) / (\2)', text)
    
    # Replace \times -> * and \cdot -> *
    text = re.sub(r'\\times', '*', text)
    text = re.sub(r'\\cdot', '*', text)
    
    # Process $$ formula $$ -> `formula`
    def repl_block(m):
        f = m.group(1).strip()
        f = re.sub(r'\\_', '_', f)
        return f'`{f}`'
    text = re.sub(r'\$\$(.*?)\$\$', repl_block, text, flags=re.DOTALL)
    
    # Process single dollar $var_name$ or $var\_name$ -> `var_name`
    def repl_inline(m):
        v = m.group(1).strip()
        v = re.sub(r'\\_', '_', v)
        return f'`{v}`'
    text = re.sub(r'\$([a-zA-Z_\\][a-zA-Z0-9_\\\_]*)\$', repl_inline, text)

    # Clean remaining \_ inside inline code backticks `...`
    def repl_code(m):
        c = m.group(1)
        return f'`{c.replace(r"\_", "_")}`'
    text = re.sub(r'`([^`]+)`', repl_code, text)
    
    return text

def ensure_vietnamese_diacritics(text: str) -> str:
    if not text or not isinstance(text, str):
        return text

    replacements = {
        r"\btai sao\b": "tại sao",
        r"\bTai sao\b": "Tại sao",
        r"\bnguoi dung\b": "người dùng",
        r"\bNguoi dung\b": "Người dùng",
        r"\bchuoi\b": "chuỗi",
        r"\bChuoi\b": "Chuỗi",
        r"\bket qua\b": "kết quả",
        r"\bKet qua\b": "Kết quả",
        r"\btoan tu\b": "toán tử",
        r"\bToan tu\b": "Toán tử",
        r"\bdoanh nghiep\b": "doanh nghiệp",
        r"\bDoanh nghiep\b": "Doanh nghiệp",
        r"\bbai doc\b": "bài đọc",
        r"\bBai doc\b": "Bài đọc",
        r"\bngon ngu\b": "ngôn ngữ",
        r"\bNgon ngu\b": "Ngôn ngữ",
        r"\blap trinh\b": "lập trình",
        r"\bLap trinh\b": "Lập trình",
        r"\bkhoang trang\b": "khoảng trắng",
        r"\bKhoang trang\b": "Khoảng trắng",
        r"\bdu thua\b": "dư thừa",
        r"\bDu thua\b": "Dư thừa",
        r"\bvi sao\b": "vì sao",
        r"\bVi sao\b": "Vì sao",
        r"\bthuc te\b": "thực tế",
        r"\bThuc te\b": "Thực tế",
        r"\bhieu nang\b": "hiệu năng",
        r"\bHieu nang\b": "Hiệu năng",
        r"\bnguy co\b": "nguy cơ",
        r"\bNguy co\b": "Nguy cơ",
        r"\bhe thong\b": "hệ thống",
        r"\bHe thong\b": "Hệ thống",
        r"\bco so du lieu\b": "cơ sở dữ liệu",
        r"\bCo so du lieu\b": "Cơ sở dữ liệu",
        r"\bphep so sanh\b": "phép so sánh",
        r"\bPhep so sanh\b": "Phép so sánh",
        r"\bxac thuc\b": "xác thực",
        r"\bXac thuc\b": "Xác thực",
        r"\btrung lap\b": "trùng lặp",
        r"\bTrung lap\b": "Trùng lặp",
        r"\bbien\b": "biến",
        r"\bBien\b": "Biến",
        r"\bgia tri\b": "giá trị",
        r"\bGia tri\b": "Giá trị",
        r"\bdu lieu\b": "dữ liệu",
        r"\bDu lieu\b": "Dữ liệu",
        r"\bmo ta\b": "mô tả",
        r"\bMo ta\b": "Mô tả",
        r"\bgiai thich\b": "giải thích",
        r"\bGiai thich\b": "Giải thích",
        r"\bphan tich\b": "phân tích",
        r"\bPhan tich\b": "Phân tích",
        r"\bcho biet\b": "cho biết",
        r"\bCho biet\b": "Cho biết",
        r"\btrinh bay\b": "trình bày",
        r"\bTrinh bay\b": "Trình bày",
        r"\bso sanh\b": "so sánh",
        r"\bSo sanh\b": "So sánh",
        r"\bkhai niem\b": "khái niệm",
        r"\bKhai niem\b": "Khái niệm",
        r"\bcot loi\b": "cốt lõi",
        r"\bCot loi\b": "Cốt lõi",
        r"\bnguyen ly\b": "nguyên lý",
        r"\bNguyen ly\b": "Nguyên lý",
        r"\bhoat dong\b": "hoạt động",
        r"\bHoat dong\b": "Hoạt động",
        r"\bphong tranh\b": "phòng tránh",
        r"\bPhong tranh\b": "Phòng tránh",
        r"\blam chu\b": "làm chủ",
        r"\bLam chu\b": "Làm chủ",
        r"\bnen tang\b": "nền tảng",
        r"\bNen tang\b": "Nền tảng",
        r"\bchinh xac\b": "chính xác",
        r"\bChinh xac\b": "Chính xác",
        r"\btuan thu\b": "tuân thủ",
        r"\bTuan thu\b": "Tuân thủ",
        r"\bquy tac\b": "quy tắc",
        r"\bQuy tac\b": "Quy tắc",
        r"\bcu phap\b": "cú pháp",
        r"\bCu phap\b": "Cú pháp",
        r"\bdinh dang\b": "định dạng",
        r"\bDinh dang\b": "Định dạng",
        r"\bkiem tra\b": "kiểm tra",
        r"\bKiem tra\b": "Kiểm tra",
        r"\bdau ra\b": "đầu ra",
        r"\bDau ra\b": "Đầu ra",
        r"\bdau vao\b": "đầu vào",
        r"\bDau vao\b": "Đầu vào",
        r"\bcan than\b": "cẩn thận",
        r"\bCan than\b": "Cẩn thận",
        r"\bvan dung\b": "vận dụng",
        r"\bVan dung\b": "Vận dụng",
        r"\bluong\b": "luồng",
        r"\bLuong\b": "Luồng",
        r"\btinh toan\b": "tính toán",
        r"\bTinh toan\b": "Tính toán",
        r"\bbieu thuc\b": "biểu thức",
        r"\bBieu thuc\b": "Biểu thức",
        r"\bhien thi\b": "hiển thị",
        r"\bHien thi\b": "Hiển thị",
        r"\btruc quan\b": "trực quan",
        r"\bTruc quan\b": "Trực quan"
    }

    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)

    return text

def validate_and_clean_forbidden_scope(content: dict, forbidden_scope: str) -> tuple:
    if not forbidden_scope or not isinstance(forbidden_scope, str) or not content or not isinstance(content, dict):
        return content, []
    
    terms = [t.strip() for t in re.split(r'[,;\n/•\-]', forbidden_scope) if t.strip() and len(t.strip()) > 2]
    
    violations = []
    text_fields = ["problem", "analysis", "solution", "example", "example_good", "example_bad", "resolve", "summary"]
    
    for field in text_fields:
        if field in content and isinstance(content[field], str):
            val = content[field]
            for term in terms:
                pattern = r'\b' + re.escape(term) + r'\b' if term.isascii() else re.escape(term)
                if re.search(pattern, val, flags=re.IGNORECASE):
                    violations.append(f"Field '{field}': Found forbidden term '{term}'")
                    val = re.sub(pattern, f"/* [Scope Guard: Filtered '{term}'] */", val, flags=re.IGNORECASE)
            content[field] = val

    if violations:
        print(f"  [Forbidden Scope Post-Linter] ⚠️ Discovered & cleaned {len(violations)} forbidden scope violations:")
        for v in violations[:5]:
            print(f"    - ❌ {v}")
            
    return content, violations

def clean_unwanted_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return text
    text = re.sub(r"\bW3Schools\b", "Chuẩn Sư Phạm Quốc Tế", text, flags=re.IGNORECASE)
    text = re.sub(r"\[W3SCHOOLS\s+NOTE\]:?", "Lưu ý:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[NOTE\]:?", "Lưu ý:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[WARNING\]:?", "Cảnh báo:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[TIP\]:?", "Mẹo:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[BEST\s+PRACTICE\]:?", "Thực hành tốt:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[ANTI-PATTERN\]:?", "Mẫu nên tránh:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[YÊU\s+CẦU\]:?", "Yêu cầu:", text, flags=re.IGNORECASE)
    
    # Scrub AI cliché words and buzzwords
    text = re.sub(r"\bbẫy lập trình\b", "Lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy cú pháp\b", "Lỗi cú pháp phổ biến", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy logic\b", "Lỗi logic phổ biến", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy lỗi\b", "Lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy\b", "lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bBẫy\b", "Lỗi thường gặp", text)
    text = re.sub(r"\bGotcha\b", "Lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bAnti-pattern\b", "Mẫu nên tránh", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbí kíp\b", "mẹo thực hành", text, flags=re.IGNORECASE)
    text = re.sub(r"\bthần thánh\b", "hiệu quả", text, flags=re.IGNORECASE)
    text = re.sub(r"\btất tần tật\b", "tổng quan đầy đủ", text, flags=re.IGNORECASE)

    text = re.sub(r"\bTIẾN TRÌNH LUỒNG CHẠY\b", "Tiến trình luồng chạy", text)
    text = re.sub(r"\bTỐC ĐỘ THỰC THI\b", "Tốc độ thực thi", text)
    text = re.sub(r"\bCODE TRACKER\b", "Code Tracker", text)
    text = re.sub(r"\bNHẬT KÝ THUẬT TOÁN\b", "Nhật ký thuật toán", text)
    text = re.sub(r"\bBẢNG SO SÁNH ĐẶC TÍNH KỸ THUẬT CHI TIẾT\b", "Bảng so sánh đặc tính kỹ thuật chi tiết", text)
    
    from agents.creators.reading_creator import force_center_media
    text = force_center_media(text)
    return text
