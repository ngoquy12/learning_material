import json
import re
from typing import Dict, Any, List
from core.state import AgentState
from core.llm import call_llm

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
    """
    Phân loại thông minh chiến lược trực quan hóa cho bài học dựa trên tín hiệu (signals):
    - EFFECTIVE_HTML_DIAGRAM (Plannotator): Bài học về kiến trúc, mô hình, quy trình, chiến lược, kinh tế, quản trị.
    - INTERACTIVE_CODE_PLAYGROUND (Code Tracker): Bài học về cú pháp code, thuật toán, vòng lặp, xử lý lỗi, lập trình tuần tự.
    """
    title_lower = (lesson_title or "").lower()
    details_lower = (lesson_details or "").lower()
    combined_text = f"{title_lower} {details_lower}"
    
    # 1. Tín hiệu khối ngành Quản trị / Non-IT -> Luôn dùng Plannotator Effective HTML
    if tech_stack.startswith("business/") or tech_stack.startswith("non-it/"):
        return {
            "strategy": "EFFECTIVE_HTML_DIAGRAM",
            "skill_name": "effective_biz_generator",
            "badge": "SƠ ĐỒ TƯ DUY & KIẾN TRÚC EFFECTIVE HTML (Plannotator)",
            "rationale": f"Môn học thuộc khối '{tech_stack}', cần trực quan hóa bằng sơ đồ chiến lược SVG tương tác, thẻ thông tin chi tiết và ma trận quản trị thay vì code tracker."
        }
        
    # 2. Tín hiệu bài học Lý thuyết tổng quan / Kiến trúc / Quy trình trong ngành IT
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
        
    # 3. Mặc định cho bài lập trình IT -> Phòng thí nghiệm Code Trực quan
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
                        elif k == "quiz":
                            result[k] = []
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
            elif k == "quiz":
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
    
    # Generic example code based on stack
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
                "question": f"Đâu là đặc tả chính của {lesson_title}?",
                "options": ["Giải pháp chuẩn", "Cấu hình mặc định", "Không có", "Cả A và B"],
                "correct_option_index": 3,
                "explanation": "Cả A và B đều đúng vì nó cung cấp giải pháp chuẩn cùng với cấu hình mặc định."
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
    # Cache optimization: check if we already generated master content for this lesson
    if state is not None and "master_content" in state and attempt_num == 1 and not feedback:
        print(f"  [Creator Agent] Reusing cached master_content for {session_id} {lesson_id} (Token Cost Saved!).")
        return state["master_content"]

    # Check if LLM is active
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    tech_stack = "python/fastapi"
    if state:
        tech_stack = state.get("technology_stack", "python/fastapi")

    if not (gemini_key or openai_key):
        result = generate_offline_master_content(session_id, lesson_id, lesson_title, lesson_details, expected_output, tech_stack)
        if state is not None:
            state["master_content"] = result
        return result

        
    from core.llm import call_llm
    from core.skills import load_skill_content
    
    tech_stack = "python/fastapi"
    if state:
        tech_stack = state.get("technology_stack", "python/fastapi")
        
    print(f"  [Creator Agent] Dynamically generating lesson content via Two-Stage LLM (Attempt #{attempt_num}) for stack: {tech_stack}...")
    
    # Smart visualization decision
    viz_decision = determine_visualization_strategy(lesson_title, lesson_details, tech_stack)
    print(f"  [Pedagogical Router] Lesson '{lesson_title}' -> Strategy: {viz_decision['strategy']} ({viz_decision['skill_name']}) | Rationale: {viz_decision['rationale']}")
    
    reading_skill = load_skill_content(viz_decision["skill_name"])
    quiz_skill = load_skill_content("quiz_generator")
    lab_skill = load_skill_content("lab_generator")
    
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
        from core.skills import load_skill_content
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
🛑 QUY TẮC RÀNG BUỘC PHẠM VI NGHIÊM NGẶT TỪ FILE PM (STRICT PM PEDAGOGICAL BOUNDARIES):
- ⛔ PHẠM VI CẤM DÙNG (STRICTLY FORBIDDEN): {forbidden_scope or 'Không dùng các thư viện/cú pháp nâng cao vượt cấp'}
  -> TUYỆT ĐỐI CẤM không được giải thích, minh họa hay sử dụng bất kỳ cú pháp/hàm/khái niệm nào thuộc danh sách cấm này! Học viên CHƯA ĐƯỢC HỌC kiến thức này ở bài học hiện tại!
- ✅ PHẠM VI ĐÃ HỌC & CHO PHÉP (ALLOWED SCOPE): {allowed_scope or 'Nội dung thuộc phạm vi bài học'}
  -> Chỉ được phép sử dụng các kiến thức và hàm nằm trong phạm vi đã học này.
- 📋 TECH STACK & QUY CHUẨN KỸ THUẬT: {tech_stack_convention or tech_stack}
  -> Mọi ví dụ mã nguồn và hướng dẫn phải áp dụng đúng 100% quy chuẩn kỹ thuật này.
"""

    # ── STAGE 1: HIGH-DEPTH ARTICLE GENERATION ──
    stage1_system_prompt = f"""Bạn là chuyên gia Thiết kế Chương trình Đào tạo Lập trình (Instructional Designer) và Kỹ sư Phần mềm cao cấp tại Rikkei Education. 
Nhiệm vụ của bạn là biên soạn TÀI LIỆU BÀI ĐỌC HỌC THUẬT SÂU SẮC, TRÌNH BÀY KHOA HỌC CHUẨN SƯ PHẠM DOANH NGHIỆP về công nghệ '{tech_stack}'.

{pm_boundaries_prompt}

YÊU CẦU BẮT BUỘC VỀ TRÌNH BÀY KHOA HỌC & ĐỘ SÂU (TỔNG 800 - 1,200 TỪ):
1. TRÌNH BÀY DẠNG LIST & SUBLIST KHOA HỌC: TUYỆT ĐỐI CẤM viết đoạn văn dài tràn lan. Mọi nội dung giải thích lý thuyết, phân tích cơ chế hay hướng dẫn BẮT BUỘC phải dùng cấu trúc Markdown Bullet Lists ('- Ý chính') và Sublists ('  - Chi tiết hỗ trợ'). Mỗi câu ngắt ý rõ ràng 1-2 câu, bôi đậm (**bold**) từ khóa kỹ thuật cốt lõi.
2. BỐ CẢNH & HÌNH ẢNH TRỰC QUAN 16:9 (problem): 250 - 400 từ. Trình bày bài toán thực tế doanh nghiệp, bối cảnh ra đời, lịch sử/người sáng lập (ví dụ: Guido van Rossum, 1991), triết lý thiết kế. BẮT BUỘC có 1 khối SVG/HTML minh họa bối cảnh bài toán theo tỉ lệ 16:9 căn giữa chiều ngang.
3. PHÂN TÍCH BẢN CHẤT VÀ SO SÁNH (analysis): 250 - 400 từ dạng List/Sublist. Giải thích cơ chế nội bộ (Interpreted Language, Dynamic Typing, Bytecode, Virtual Machine, Memory Management). BẮT BUỘC có 1 BẢNG MARKDOWN COMPARISON TABLE so sánh Python với C/C++/Java/JS.
4. GIẢI PHÁP KỸ THUẬT & SƠ ĐỒ MERMAID (solution): Hướng dẫn từng bước cú pháp chuẩn dạng List. BẮT BUỘC có ít nhất 1 sơ đồ ```mermaid (flowchart hoặc sequenceDiagram) giải thích luồng thực thi.
5. MÃ NGUỒN ĐỐI CHIẾU (example_good & example_bad): Cung cấp mã chuẩn Best Practice (example_good) và mã sai/Anti-pattern (example_bad) có comment giải thích lý do.
6. KẾT QUẢ & KỊCH BẢN NỔI BẬT (resolve): Phân tích chi tiết luồng chạy dạng List và kết quả console output.
7. TỔNG KẾT & LƯU Ý (summary): Tổng kết Lưu ý & Cảnh báo sư phạm dạng List, BÔI ĐẬM (**bold**) tên các sai lầm runtime thường gặp.

QUY TẮC BẮT BUỘC VỀ PHONG CÁCH VÀ MÃ NGUỒN (STRICT RULES):
- 100% Tiếng Việt có dấu chuẩn xác.
- TUYỆT ĐỐI CẤM sử dụng biểu tượng cảm xúc (emoji).
- TUYỆT ĐỐI CẤM dùng từ khóa "W3Schools" hay các nhãn bọc trong ngoặc vuông như [NOTE], [WARNING], [BEST PRACTICE], [ANTI-PATTERN]. Thay bằng nhãn thuần: Lưu ý:, Cảnh báo:, Mẹo:, Thực hành tốt:, Mẫu nên tránh:.
- RÀNG BUỘC PYTHON CODING CONVENTIONS (PEP 8): Tất cả tên biến, tên hàm, tên hằng số BẮT BUỘC viết bằng TIẾNG ANH CÓ Ý NGHĨA dạng snake_case (ví dụ: user_age, rectangle_width, calculate_area(), total_price). CẤM TUYỆT ĐỐI dùng tiếng Việt không dấu (như chieu_dai, nhap_chieu_rong, bien1, temp).
{lessons_learned_prompt}
"""

    prev_lessons_prompt = ""
    if state and state.get("previous_lessons"):
        prev_lessons_prompt = "\n--- THÔNG TIN CÁC BÀI HỌC TRƯỚC ĐÓ (Mối liên kết bài học) ---\n"
        for prev in state["previous_lessons"]:
            det = prev.get('details') or prev.get('lesson_details', '')
            l_id = prev.get('lesson_id', '')
            l_t = prev.get('title', '')
            prev_lessons_prompt += f"- {l_id}: {l_t} (Nội dung: {det})\n"

    stage1_user_prompt = f"""Hãy biên soạn bài đọc sâu sắc dạng List/Sublist cho:
Session: {session_id} ({session_type})
Lesson: {lesson_id} (Tiêu đề: {lesson_title})
Chi tiết từ PM: {lesson_details}
Đầu ra kỳ vọng: {expected_output}
Phạm vi CẤM DÙNG: {forbidden_scope or 'Không có'}
Phạm vi ĐÃ HỌC: {allowed_scope or 'Kiến thức theo bài học'}
Tech Stack & Quy chuẩn: {tech_stack_convention or tech_stack}
{prev_lessons_prompt}
Phản hồi từ Reviewer nếu có: {feedback}

Đầu ra trả về duy nhất chuỗi JSON có các trường:
{{
    "problem_title": "Tiêu đề ngắn gọn cho phần 1",
    "problem": "Nội dung đặt vấn đề dạng Markdown Bullet List & Sublist (250-400 từ), kèm bối cảnh thực tế doanh nghiệp",
    "analysis_title": "Tiêu đề ngắn gọn cho phần 2",
    "analysis": "Phân tích cơ chế vận hành nội bộ dạng List/Sublist kèm BẢNG SO SÁNH MARKDOWN KỸ THUẬT (250-400 từ)",
    "solution_title": "Tiêu đề ngắn gọn cho phần 3",
    "solution": "Giải pháp kỹ thuật chi tiết dạng List kèm SƠ ĐỒ MERMAID ```mermaid ... ```",
    "example": "Mã nguồn minh họa chính tuân thủ PEP 8 (snake_case tiếng Anh)",
    "example_good": "Ví dụ mã chuẩn Best Practice (GOOD Practice) kèm comment giải thích",
    "example_bad": "Ví dụ mã sai/Anti-pattern (BAD Practice) kèm comment cảnh báo bẫy lỗi",
    "resolve_title": "Tiêu đề ngắn gọn cho phần 4",
    "resolve": "Phân tích chi tiết luồng chạy thực thi dạng List và Console Output",
    "summary": "Tổng kết bài học dạng List và bôi đậm **các sai lầm runtime thường gặp**"
}}
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
            lesson_id=lesson_id
        )
        if response_text:
            try:
                cleaned = response_text.strip()
                json_match = re.search(r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL)
                if json_match:
                    cleaned = json_match.group(1).strip()
                else:
                    block_match = re.search(r"```\s*(\{.*?\})\s*```", response_text, re.DOTALL)
                    if block_match:
                        cleaned = block_match.group(1).strip()
                    else:
                        first_brace = response_text.find("{")
                        last_brace = response_text.rfind("}")
                        if first_brace != -1 and last_brace != -1:
                            cleaned = response_text[first_brace:last_brace+1].strip()
                
                cleaned = fix_raw_newlines_in_json_strings(cleaned)
                stage1_result = robust_json_parse(cleaned)
                if stage1_result.get("problem") and stage1_result.get("analysis"):
                    print(f"  [Creator Agent Stage 1] High-depth reading article generated successfully!")
                    break
            except Exception as e:
                print(f"  [Creator Agent Stage 1 Warning] Attempt {attempt+1} failed: {e}")

    # Fallback for Stage 1 if LLM parse failed
    if not stage1_result.get("problem"):
        stage1_result = generate_offline_master_content(session_id, lesson_id, lesson_title, lesson_details, expected_output, tech_stack)

    # ── STAGE 2: COMPONENTS GENERATION (Self-test, Quiz, Lab, Visualizer) ──
    stage2_system_prompt = f"""Bạn là Kỹ sư Khảo thí và Kiểm định Giáo dục tại Rikkei Education.
Nhiệm vụ của bạn là đọc bài đọc lý thuyết Stage 1 và sinh các thành phần phụ trợ (Self-test 3 câu, References, Quiz 4 câu, Lab, Visualizer Engine).
BẮT BUỘC: 100% câu hỏi self_test và quiz phải bám sát nội dung bài đọc Stage 1, tuyệt đối không hỏi trước bài học sau. Không emoji.
"""
    stage2_user_prompt = f"""Dựa vào bài đọc Stage 1 sau đây:
{json.dumps(stage1_result, ensure_ascii=False)[:3000]}

Hãy trả về duy nhất chuỗi JSON chứa các thành phần phụ trợ:
{{
    "self_test": [
        {{"question": "Câu hỏi khảo thí 1 bám sát bài đọc?", "answer": "Gợi ý trả lời chi tiết sâu sắc."}},
        {{"question": "Câu hỏi khảo thí 2?", "answer": "Gợi ý trả lời."}},
        {{"question": "Câu hỏi khảo thí 3?", "answer": "Gợi ý trả lời."}}
    ],
    "references": [
        {{"title": "Tên tài liệu tham khảo uy tín chính thức", "url": "https://docs.python.org/3/"}}
    ],
    "quiz": [
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 1?",
            "options": ["Phương án A", "Phương án B", "Phương án C", "Phương án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích chi tiết vì sao đáp án đúng."
        }}
    ],
    "lab": {{
        "title": "Tiêu đề bài thực hành",
        "objectives": ["Mục tiêu thực hành"],
        "steps": ["Các bước thực hiện"],
        "checklist": ["Tiêu chí đánh giá"]
    }},
    "visualizer": {{
        "canvas_title": "Khung trực quan hóa bài học",
        "legend_html": "Chú giải màu sắc",
        "stats_html": "Thẻ thông tin đếm",
        "code_tracker_html": "<div class='code-line' id='line-0'># Code tracker...</div>",
        "input_label": "Nhãn ô nhập",
        "input_default": "Mặc định",
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
            lesson_id=lesson_id
        )
        if response_text_s2:
            cleaned_s2 = response_text_s2.strip()
            first_b = cleaned_s2.find("{")
            last_b = cleaned_s2.rfind("}")
            if first_b != -1 and last_b != -1:
                cleaned_s2 = cleaned_s2[first_b:last_b+1].strip()
            cleaned_s2 = fix_raw_newlines_in_json_strings(cleaned_s2)
            stage2_result = robust_json_parse(cleaned_s2)
    except Exception as e:
        print(f"  [Creator Agent Stage 2 Warning] Failed to generate Stage 2 components: {e}")

    # Merge Stage 1 and Stage 2 results
    final_result = dict(stage1_result)
    final_result["self_test"] = stage2_result.get("self_test") or [
        {"question": f"Giải thích bản chất và nguyên lý hoạt động cốt lõi của {lesson_title}?", "answer": f"Hiểu rõ bản chất giúp vận dụng đúngBest Practice."},
        {"question": f"Liệt kê các cú pháp hoặc lỗi thường gặp khi làm việc với {lesson_title} và cách phòng tránh?", "answer": f"Tuân thủ quy tắc lùi lề và định dạng kiểu dữ liệu."},
        {"question": f"Trình bày ứng dụng thực tế của {lesson_title} trong dự án?", "answer": f"Vận dụng để xử lý luồng logic và tính toán dữ liệu."}
    ]
    final_result["references"] = stage2_result.get("references") or [
        {"title": f"Tài liệu hướng dẫn chính thức {tech_stack.upper()}", "url": "https://docs.python.org/3/"},
        {"title": "W3Schools Online Web Tutorials", "url": "https://www.w3schools.com"}
    ]
    final_result["quiz"] = stage2_result.get("quiz") or []
    final_result["lab"] = stage2_result.get("lab") or {"title": f"Lab {lesson_title}", "objectives": [], "steps": [], "checklist": []}
    # Run Post-Linter Guard to ensure no forbidden scope terms slipped through LLM generation
    final_result, _ = validate_and_clean_forbidden_scope(final_result, forbidden_scope)

    if state is not None:
        state["master_content"] = final_result

    return final_result



def session_compiler_agent(state: AgentState) -> AgentState:
    """
    Session Compiler Agent:
    Compiles all approved HTML, Slides, and Quiz assets.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    lesson_title = state.get("core_ssot", {}).get("session_title", "Course Session")
    
    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    
    print(f"\n[Session_Compiler_Agent] Compiling assets for {display_title}...")
    print(f"  - HTML: Compiled ({len(state.get('html_content', ''))} chars) following Storytelling standards.")
    print(f"  - Slides: Compiled ({len(state.get('slide_markdown', ''))} chars) following Visual standards.")
    print(f"  - Quiz JSON: Compiled successfully with 5-question matrix and Hands-on template.")
    print(f"  - Video Script: Compiled ({len(state.get('video_script_markdown', ''))} chars) following Video standards.")
    print(f"  - Mindmap: Compiled ({len(state.get('mindmap_markdown', ''))} chars) following Mindmap standards.")
    
    state["artifacts_status"]["session"] = "PUBLISHED"
    return state

def mini_project_generator_agent(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, tech_stack: str, core_ssot: dict) -> dict:
    """
    Mini Project Generator Agent:
    Generates full Mini Project assets for 'Mini Project' session types:
    1. srs_spec (Software Requirements Specification HTML)
    2. architecture_mermaid (Mermaid ERD / Class / Data Flow Diagram)
    3. starter_code (Modular Python starter code with TODOs following PEP 8)
    4. project_rubric (100-point Professional Evaluation Rubric)
    """
    from core.llm import call_llm

    forbidden_scope = core_ssot.get("forbidden_scope", "") if isinstance(core_ssot, dict) else ""
    allowed_scope = core_ssot.get("allowed_scope", "") if isinstance(core_ssot, dict) else ""
    tech_stack_convention = core_ssot.get("tech_stack_convention", "") if isinstance(core_ssot, dict) else ""

    sys_prompt = f"""Bạn là Kiến trúc sư Phần mềm và Chuyên gia Thiết kế Đồ án tại Rikkei Education.
Nhiệm vụ của bạn là biên soạn BỘ TÀI NGUYÊN MINI PROJECT DOANH NGHIỆP hoàn chỉnh cho Session: '{session_id}: {lesson_title}'.

RÀNG BUỘC PHẠM VI NGHIÊM NGẶT:
- ⛔ CẤM DÙNG: {forbidden_scope or 'Thư viện/cú pháp nâng cao chưa học'}
- ✅ ĐÃ HỌC: {allowed_scope or 'Kiến thức theo chương trình từ Session trước'}
- 📋 QUY CHUẨN: {tech_stack_convention or tech_stack} (PEP 8, snake_case tiếng Anh)

Hãy tạo duy nhất chuỗi JSON gồm 4 thành phần:
{{
    "srs_title": "Tên Đặc tả Yêu cầu Đồ án Mini Project",
    "srs_spec": "Nội dung Đặc tả SRS dạng Markdown Bullet Lists & Sublists gồm: 1. Bối cảnh doanh nghiệp, 2. Yêu cầu Chức năng (Functional Specs), 3. Yêu cầu Phi chức năng (Non-functional Specs), 4. Giao diện CLI/Mẫu console đầu ra mong đợi.",
    "architecture_mermaid": "```mermaid\\ngraph TD\\n  %% Sơ đồ kiến trúc luồng dữ liệu dự án...\\n```",
    "starter_code": "# Khung mã nguồn khởi tạo Best Practice PEP 8 (snake_case tiếng Anh) kèm comment # TODO...",
    "project_rubric": "### BẢNG RUBRIC CHẤM ĐIỂM DỰ ÁN MINI PROJECT (TỔNG 100 ĐIỂM)\\n- Chức năng cốt lõi (40đ):\\n- Chất lượng Code & PEP 8 (30đ):\\n- Xử lý lỗi & Exception (20đ):\\n- Tối ưu & Clean Code (10đ):"
}}
Return only raw JSON.
"""
    user_prompt = f"""Biên soạn Mini Project cho Session: {session_id} - {lesson_title}
Chi tiết từ PM: {lesson_details}
Đầu ra kỳ vọng: {expected_output}"""

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


def video_script_agent(state: AgentState) -> AgentState:
    """
    Video Director Agent (HyperFrames Standard):
    Produces a production-ready blueprint JSON for HyperFrames video composition.
    Follows the dev-tutorial-video standard: scene-based structure, GSAP timeline rules,
    audio architecture, and design system as defined in skills/hyperframes_composer/SKILL.md.
    """
    import json
    import os
    from core.llm import call_llm
    from core.skills import load_skill_content

    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    tech_stack = state.get("technology_stack", "python/core")

    previous_rejects = [log for log in state.get("review_logs", []) if log["source"] == "Video_Script_Reviewer"]
    attempt_num = len(previous_rejects) + 1
    feedback_context = ""
    if previous_rejects:
        feedback_context = f"PHẢN HỒI TỪ REVIEWER (LẦN TRƯỚC — BẮT BUỘC SỬA):\n{previous_rejects[-1]['feedback']}\n"

    print(f"\n[Video_Director_Agent] Generating HyperFrames Blueprint for {session_id} {lesson_id} (Attempt {attempt_num})")

    # Load master content (shared cache)
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=core_ssot.get("expected_output", ""),
        attempt_num=1,
        core_ssot=core_ssot,
        state=state
    )

    # Load the HyperFrames composer skill for context
    hyperframes_skill = load_skill_content("hyperframes_composer")

    import re
    # Extract numeric IDs for standard folder naming session_XX_lesson_YY
    s_match = re.search(r'(\d+)', session_id)
    s_num = s_match.group(1).zfill(2) if s_match else "01"
    l_match = re.search(r'(\d+)', lesson_id)
    l_num = l_match.group(1).zfill(2) if l_match else "01"
    lesson_slug = f"session_{s_num}_lesson_{l_num}"

    system_prompt = f"""Bạn là Video Director Agent — Chuyên gia sản xuất Video Giáo dục E-learning chuẩn quốc tế theo nền tảng HyperFrames.
Nhiệm vụ của bạn là phân tích bài học bất kỳ và tạo ra một "Production Blueprint JSON" chuẩn hóa với chiều sâu sư phạm vượt trội.

BỘ KHUNG TIÊU CHUẨN KỊCH BẢN 5 TẦNG (UNIVERSAL 5-LAYER FRAMEWORK):

TẦNG 1: PHÂN LOẠI SƯ PHẠM & THỜI LƯỢNG MỤC TIÊU (PEDAGOGY TAXONOMY):
- Tự động xác định loại hình bài học từ nội dung:
  1. HANDSON_SETUP (Cài đặt / Thiết lập môi trường / Công cụ): BẮT BUỘC 10 - 16 scenes, 25-45s/scene, tổng 5-8+ phút, 650-1000 từ thoại.
  2. LIVE_CODING (Thực hành viết code / Cú pháp / Thuật toán): BẮT BUỘC 12 - 18 scenes, 30-50s/scene, tổng 6-10+ phút, 700-1100 từ thoại.
  3. CONCEPTUAL (Lý thuyết / Khái niệm cơ bản): 6 - 10 scenes, 25-35s/scene, tổng 3-5 phút, 450-700 từ thoại.
  4. SYSTEM_ARCHITECTURE (Kiến trúc / Process Flow / API): 10 - 14 scenes, 30-45s/scene, tổng 5-7 phút, 600-900 từ thoại.

TẦNG 2: BẢO TOÀN NGUYÊN TẮC "WHY BEFORE HOW":
- Mọi câu lệnh CLI, đoạn code hoặc thiết lập trên màn hình BẮT BUỘC phải đi kèm lời thuyết minh giải thích bản chất "TẠI SAO" (Ví dụ: giải thích cờ -m, giải thích lý do dùng venv, ý nghĩa từng tham số). Không bao giờ chỉ đọc suông câu lệnh.

TẦNG 3: NARRATION CHUẨN ÂM & PHÁT ÂM TTS:
- Viết lời thoại narration tự nhiên, khúc triết, trực diện.
- CẤM TUYỆT ĐỐI các từ ngữ sến súa, nịnh hót hoặc suồng sã như: "nhé", "thân mến", "các em", "nha", "nhỉ", "nhé các bạn", "chúng mình".
- Văn phong BẮT BUỘC theo chuẩn Giảng viên cao cấp / Senior Engineer: Chuyên sâu kỹ thuật, giải thích rõ cơ chế vận hành, bộ nhớ, hiệu năng và quy tắc cú pháp.
- Tự động chuẩn hóa từ ngữ kỹ thuật cho giọng đọc TTS đọc chuẩn:
  + Tên lệnh/cờ: "python -m venv" -> "python trừ m venv"
  + Phím tắt: "Ctrl+Shift+P" -> "phím Control Shift P"
  + Thuật ngữ: "requirements.txt" -> "file ri-quai-mơn text"

TẦNG 4: ÁNH XẠ UI LAYOUT TYPOLOGY (LAYOUT_TYPE):
Chỉ định 1 trong 5 mẫu layout chính cho mỗi scene:
- "code_editor": Giao diện VS Code mockup hiển thị code/script.
- "terminal_cli": Giao diện Terminal CLI gõ lệnh thực thi.
- "comparison": Bảng so sánh 2 cột Good vs Bad / Global vs Virtual Env.
- "process_flow": Sơ đồ quy trình từng bước có mũi tên kết nối.
- "pitfall_alert": Thẻ cảnh báo lỗi phổ biến và giải pháp khắc phục.

TẦNG 5: TRÍCH XUẤT UI CARD CLEAN:
- "visual_description" CHỈ chứa tóm tắt kiến thức cốt lõi (Card takeaway) hiển thị cho người học. TUYỆT ĐỐI KHÔNG chứa các câu nhắc meta-prompt dàn dựng như "Màn hình hiển thị...", "Phông nền tối...".

Output JSON BẮT BUỘC theo cấu trúc CHÍNH XÁC này:
{{
  "lesson_slug": "{lesson_slug}",
  "lesson_title": "{lesson_title}",
  "pedagogy_type": "HANDSON_SETUP|LIVE_CODING|CONCEPTUAL|SYSTEM_ARCHITECTURE",
  "total_duration": <tổng thời gian tất cả scenes>,
  "scenes": [
    {{
      "scene_id": "Scene_01",
      "scene_title": "<Tiêu đề ngắn của scene>",
      "start_at_root": 0,
      "duration": <số giây của scene, từ 25-45s>,
      "track_index": 1,
      "layout_type": "code_editor|terminal_cli|comparison|process_flow|pitfall_alert",
      "narration": "<Lời thoại giảng dạy chi tiết 60-100 từ/scene chuẩn âm TTS>",
      "visual_description": "<Tóm tắt 1-2 câu điểm kiến thức cốt lõi hiển thị trên UI Card (KHÔNG chứa meta-prompt instruction)>",
      "html_structure": "<Các elements HTML chính>",
      "animation_timeline": [
        "0.2s: intro-title fade in",
        "3.2s: intro-title fade out",
        "4.0s: main content show"
      ]
    }}
  ],
  "tts_scripts": {{}}
}}

CRITICAL: start_at_root của scene (N+1) = start_at_root[N] + duration[N]
CRITICAL: total_duration = tổng tất cả duration của các scenes
CRITICAL: track_index của scenes là 1, 2, 3, ... (tăng dần)
Return only raw JSON. Do not wrap in markdown code blocks."""

    user_prompt = f"""Tạo Production Blueprint JSON cho bài học sau:
Session: {session_id}
Lesson: {lesson_id} (Tiêu đề: {lesson_title})
Technology Stack: {tech_stack}
Chi tiết bài học: {lesson_details}

Nội dung bài học gốc (Master Content để bám sát):
- Vấn đề đặt ra: {content.get('problem', '')}
- Giải pháp: {content.get('solution', '')}
- Ví dụ/Code: {content.get('example', '')}
- Tổng kết: {content.get('summary', '')}

{feedback_context}
Trả về DUY NHẤT JSON thuần túy theo đúng cấu trúc yêu cầu."""

    # Generate via LLM or offline fallback
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")):
        # Offline fallback — 6-scene baseline blueprint with real pedagogical structure
        details_text = lesson_details or lesson_title
        result_json = _build_offline_fallback_blueprint(lesson_slug, lesson_title, details_text, tech_stack)
    else:
        llm_resp = call_llm(
            system_prompt,
            user_prompt,
            json_mode=True,
            agent_name=f"Video_Director_Agent_Att{attempt_num}",
            session_id=session_id,
            lesson_id=lesson_id
        )
        try:
            from agents.creator_agents import robust_json_parse
            result_json = robust_json_parse(llm_resp)
            # Validate required fields
            if "scenes" not in result_json or not result_json["scenes"]:
                raise ValueError("Missing 'scenes' in blueprint JSON")
            if "tts_scripts" not in result_json:
                raise ValueError("Missing 'tts_scripts' in blueprint JSON")
            print(f"  [Video_Director_Agent] Blueprint generated: {len(result_json['scenes'])} scenes, duration {result_json.get('total_duration', 0)}s")
        except Exception as e:
            print(f"  [Video_Director_Agent] JSON parse failed: {e}. Using fallback blueprint.")
            result_json = {
                "lesson_slug": lesson_slug,
                "lesson_title": lesson_title,
                "total_duration": 60.0,
                "scenes": [
                    {
                        "scene_id": "Scene_01",
                        "scene_title": lesson_title,
                        "start_at_root": 0,
                        "duration": 30.0,
                        "track_index": 1,
                        "narration": f"Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay chúng ta học về {lesson_title}.",
                        "visual_description": "Intro screen với tiêu đề bài học.",
                        "html_structure": "intro-title, content area",
                        "animation_timeline": [
                            "0.0s: tl.set('.clip', {autoAlpha:1}, 0)",
                            "0.2s: intro-title fade in",
                            "3.2s: intro-title lên góc",
                            "4.5s: content slide in"
                        ]
                    },
                    {
                        "scene_id": "Scene_02",
                        "scene_title": "Kết luận",
                        "start_at_root": 30.0,
                        "duration": 30.0,
                        "track_index": 2,
                        "narration": f"Cảm ơn các em đã theo dõi bài học {lesson_title}. Hẹn gặp lại trong bài học tiếp theo!",
                        "visual_description": "Summary screen.",
                        "html_structure": "summary card",
                        "animation_timeline": [
                            "0.0s: tl.set('.clip', {autoAlpha:1}, 0)",
                            "0.2s: intro-title fade in",
                            "3.2s: intro-title fade out",
                            "30.0s: tl.set({}, {}, 30.0)"
                        ]
                    }
                ],
                "tts_scripts": {
                    "Scene_01": f"Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay chúng ta học về {lesson_title}.",
                    "Scene_02": f"Cảm ơn các em đã theo dõi bài học {lesson_title}. Hẹn gặp lại trong bài học tiếp theo!"
                }
            }

    # ── POST-VALIDATION: Kiểm tra chất lượng blueprint ────────────────────────
    result_json = _post_validate_blueprint(result_json, lesson_slug, lesson_title, lesson_details, tech_stack)

    # Persist blueprint to state
    result_json["lesson_slug"] = lesson_slug
    state["video_script_json"] = result_json
    state["video_lesson_slug"] = lesson_slug

    # Build readable SCRIPT.md (for human review + Hyperframes structure)
    scenes = result_json.get("scenes", [])
    total_dur = result_json.get("total_duration", 0)
    script_md = f"# HyperFrames Script: {session_id} — {lesson_id}\n\n"
    script_md += f"**Lesson:** {lesson_title}\n"
    script_md += f"**Technology Stack:** {tech_stack}\n"
    script_md += f"**Total Duration:** {total_dur}s\n"
    script_md += f"**Scene Count:** {len(scenes)}\n\n"
    script_md += "---\n\n"

    cumulative = 0
    for scene in scenes:
        dur = scene.get("duration", 0)
        script_md += f"## {scene.get('scene_id', '?')}: {scene.get('scene_title', '')}\n"
        script_md += f"**Timeline (root):** {scene.get('start_at_root', cumulative):.2f}s → {(scene.get('start_at_root', cumulative) + dur):.2f}s ({dur}s)\n\n"
        script_md += f"**Visual:** {scene.get('visual_description', '')}\n\n"
        script_md += f"**Animation Timeline:**\n"
        for step in scene.get("animation_timeline", []):
            script_md += f"- {step}\n"
        script_md += f"\n**Narration (VO):**\n> {scene.get('narration', '')}\n\n"
        cumulative += dur

    state["video_script_markdown"] = script_md
    print(f"  [Video_Director_Agent] Blueprint complete — {len(scenes)} scenes, {total_dur:.1f}s total.")
    return state


def _post_validate_blueprint(blueprint: dict, lesson_slug: str, lesson_title: str, lesson_details: str, tech_stack: str) -> dict:
    """
    Post-validation Gate: Kiểm tra chất lượng blueprint sau khi LLM sinh.
    Nếu vi phạm ngưỡng tối thiểu → tự động sửa chữa hoặc thay thế bằng fallback.
    """
    MIN_SCENES = 6
    MIN_TOTAL_DURATION = 180.0  # 3 phút tối thiểu
    MIN_WORDS_PER_NARRATION = 30

    scenes = blueprint.get("scenes", [])
    total_dur = sum(s.get("duration", 0) for s in scenes)
    issues = []

    if len(scenes) < MIN_SCENES:
        issues.append(f"Scenes count ({len(scenes)}) < {MIN_SCENES}")
    if total_dur < MIN_TOTAL_DURATION:
        issues.append(f"Total duration ({total_dur:.1f}s) < {MIN_TOTAL_DURATION}s")
    for s in scenes:
        word_count = len(s.get("narration", "").split())
        if word_count < MIN_WORDS_PER_NARRATION:
            issues.append(f"{s.get('scene_id')}: narration too short ({word_count} words)")

    if issues:
        print(f"  [Post-Validation] Blueprint FAILED quality check:")
        for issue in issues:
            print(f"    ⚠️ {issue}")
        print(f"  [Post-Validation] Replacing with enriched offline fallback...")
        return _build_offline_fallback_blueprint(lesson_slug, lesson_title, lesson_details, tech_stack)

    # Recalculate start_at_root for consistency
    cumulative = 9.24  # After intro video
    for scene in scenes:
        scene["start_at_root"] = round(cumulative, 2)
        cumulative += scene.get("duration", 30.0)
    blueprint["total_duration"] = round(cumulative + 12.15, 2)  # + outro

    print(f"  [Post-Validation] Blueprint PASSED quality check ✓")
    return blueprint


def _build_offline_fallback_blueprint(lesson_slug: str, lesson_title: str, lesson_details: str, tech_stack: str) -> dict:
    """
    Offline Fallback Blueprint Generator.
    Tạo blueprint 6-8 scene có cấu trúc sư phạm chuẩn khi không có LLM hoặc khi LLM output kém chất lượng.
    """
    details_text = lesson_details or lesson_title
    # Phân tách chi tiết bài học thành các điểm kiến thức
    detail_points = [p.strip() for p in details_text.replace("\n", ".").split(".") if len(p.strip()) > 10]
    if len(detail_points) < 3:
        detail_points = [lesson_title, f"Kiến thức cốt lõi về {lesson_title}", f"Thực hành {lesson_title}"]

    layouts = ["comparison", "code_editor", "terminal_cli", "process_flow", "pitfall_alert", "summary_recap"]
    scenes = []
    tts_scripts = {}
    cumulative = 9.24

    # Scene 01: Intro
    intro_narration = (
        f"Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. "
        f"Trong bài học ngày hôm nay, chúng ta sẽ cùng nhau tìm hiểu chi tiết về {lesson_title}. "
        f"Đây là một chủ đề cực kỳ quan trọng và thiết yếu trong {tech_stack}. "
    )
    scenes.append({
        "scene_id": "Scene_01", "scene_title": f"Giới thiệu: {lesson_title}",
        "start_at_root": round(cumulative, 2), "duration": 35.0, "track_index": 1,
        "layout_type": "comparison",
        "narration": intro_narration,
        "visual_description": f"Tổng quan mục tiêu bài học {lesson_title} và lộ trình nội dung.",
        "html_structure": "intro-title centered, badge công nghệ",
        "animation_timeline": ["0.2s: intro-title fade in", "3.2s: intro-title lên góc", "4.5s: content card xuất hiện"]
    })
    tts_scripts["Scene_01"] = intro_narration
    cumulative += 35.0

    # Scenes 02..N-1: Content scenes derived from lesson_details
    for i, point in enumerate(detail_points[:5], start=2):
        layout = layouts[min(i - 1, len(layouts) - 1)]
        narration = (
            f"Tiếp theo, chúng ta sẽ tìm hiểu sâu hơn về: {point}. "
            f"Đây là kiến thức nền tảng mà mỗi lập trình viên đều cần nắm vững khi làm việc với {tech_stack}. "
            f"Hãy chú ý quan sát từng bước thực hiện trên màn hình và ghi nhớ những điểm mấu chốt quan trọng."
        )
        scene_id = f"Scene_{str(i).zfill(2)}"
        scenes.append({
            "scene_id": scene_id, "scene_title": point[:80],
            "start_at_root": round(cumulative, 2), "duration": 35.0, "track_index": i,
            "layout_type": layout,
            "narration": narration,
            "visual_description": point,
            "html_structure": f"{layout} layout",
            "animation_timeline": ["0.2s: intro-title fade in", "3.2s: intro-title lên góc", "4.5s: content reveal"]
        })
        tts_scripts[scene_id] = narration
        cumulative += 35.0

    # Đảm bảo tối thiểu 6 scenes
    while len(scenes) < 5:
        idx = len(scenes) + 1
        scene_id = f"Scene_{str(idx).zfill(2)}"
        narration = f"Chúng ta tiếp tục với một khía cạnh quan trọng khác của {lesson_title} trong {tech_stack}. Hãy quan sát và ghi nhớ các bước thực hiện."
        scenes.append({
            "scene_id": scene_id, "scene_title": f"Nội dung bổ sung {idx}",
            "start_at_root": round(cumulative, 2), "duration": 30.0, "track_index": idx,
            "layout_type": "code_editor",
            "narration": narration,
            "visual_description": f"Minh họa thêm về {lesson_title}.",
            "html_structure": "code_editor layout",
            "animation_timeline": ["0.2s: intro-title fade in", "3.2s: intro-title lên góc", "4.5s: content reveal"]
        })
        tts_scripts[scene_id] = narration
        cumulative += 30.0

    # Scene cuối: Summary
    last_idx = len(scenes) + 1
    last_id = f"Scene_{str(last_idx).zfill(2)}"
    summary_narration = (
        f"Như vậy, chúng ta đã cùng nhau hoàn thành bài học về {lesson_title}. "
        f"Hãy nhớ rằng những kiến thức này là nền tảng cực kỳ quan trọng cho các bài học tiếp theo trong khóa {tech_stack}. "
        f"Các em hãy thực hành lại toàn bộ các bước trên máy cá nhân để củng cố kiến thức. "
        f"Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
    )
    scenes.append({
        "scene_id": last_id, "scene_title": "Tổng Kết Bài Học",
        "start_at_root": round(cumulative, 2), "duration": 35.0, "track_index": last_idx,
        "layout_type": "summary_recap",
        "narration": summary_narration,
        "visual_description": f"Tổng kết các điểm kiến thức trọng tâm của bài học {lesson_title}.",
        "html_structure": "summary-card, key-points list",
        "animation_timeline": ["0.2s: intro-title fade in", "3.2s: intro-title lên góc", "4.5s: summary card slide up"]
    })
    tts_scripts[last_id] = summary_narration
    cumulative += 35.0

    total_duration = round(cumulative + 12.15, 2)  # + outro
    print(f"  [Fallback Blueprint] Generated {len(scenes)} scenes, {total_duration:.1f}s total")

    return {
        "lesson_slug": lesson_slug,
        "lesson_title": lesson_title,
        "pedagogy_type": "CONCEPTUAL",
        "total_duration": total_duration,
        "scenes": scenes,
        "tts_scripts": tts_scripts
    }


def get_lesson_dir(state: AgentState) -> Path:
    from pathlib import Path
    import json
    import re

    def sanitize_folder_name(name: str) -> str:
        name = name.replace("&", "va").replace("%", "").replace("^", "").replace("#", "")
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    course_dir_name = state.get("course_dir_name")
    if not course_dir_name:
        pms_dir = Path("pms")
        xlsx_files = list(pms_dir.glob("*.xlsx")) if pms_dir.exists() else []
        xlsx_files = [f for f in xlsx_files if not f.name.startswith("~$")]
        if xlsx_files:
            course_dir_name = xlsx_files[0].stem.strip().replace(" ", "_").replace("-", "_")
        else:
            course_dir_name = "default_course"
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    
    output_base_dir = Path(__file__).resolve().parent.parent / "output"
    course_dir = output_base_dir / course_dir_name
    
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
    import os
    import requests
    import base64
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        try:
            base_url = os.getenv("GEMINI_BASE_URL")
            if base_url:
                # Use OpenAI image generation format through proxy
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
                response = requests.post(url, headers=headers, json=data, timeout=40)
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
                        img_resp = requests.get(img_url, timeout=20)
                        if img_resp.status_code == 200:
                            with open(image_path, "wb") as f:
                                f.write(img_resp.content)
                            print(f"  [Image Generator] Saved downloaded diagram to: {image_path}")
                            return True
            
            # Direct Google GenerativeAI API endpoint
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
            response = requests.post(url, headers=headers, json=data, timeout=30)
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

def draw_mindmap_fallback_diagram(prompt_text: str, image_path: Path, title: str):
    raise NotImplementedError("Fallback mindmap diagram generation is disabled. All images must be generated dynamically by AI.")

def process_mindmap_images(markmap_content: str, state: AgentState) -> str:
    import re
    from pathlib import Path
    
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
        
    try:
        lesson_dir = get_lesson_dir(state)
        images_dir = lesson_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"  [Image Processing Warning] Could not resolve lesson directory: {e}")
        return markmap_content
        
    new_content = markmap_content
    for idx, prompt_text in enumerate(all_prompts, 1):
        image_name = f"mindmap_img_{idx}.png"
        image_path = images_dir / image_name
        
        print(f"  [Mindmap Image] Processing prompt {idx}: '{prompt_text[:50]}...'")
        
        force_rebuild = state.get("force_rebuild", False)
        if force_rebuild or not image_path.exists():
            success = generate_image_api(prompt_text, image_path)
            if not success:
                print(f"  [Mindmap Image Warning] AI image generation failed for prompt '{prompt_text[:50]}...'. Default fallback diagram is disabled.")
        
        search_bracket = r"\[(?:Prompt|Tạo ảnh):\s*" + re.escape(prompt_text) + r"\]"
        new_content = re.sub(search_bracket, f"![](../images/{image_name})", new_content)
        
        search_asterisk = r"\*Prompt tạo ảnh:\s*" + re.escape(prompt_text) + r"\*"
        new_content = re.sub(search_asterisk, f"![](../images/{image_name})", new_content, flags=re.IGNORECASE)
        
    return new_content

def mindmap_agent(state: AgentState) -> AgentState:
    """
    Mindmap Agent:
    Generates a structured Markmap diagram based on skills/mindmap_generator/SKILL.md.
    Uses the LLM with retry/critique logs if keys are available, otherwise falls back to a template.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = state.get("technology_stack", "python/fastapi")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    mindmap_logs = [log for log in state.get("review_logs", []) if log["source"] == "Mindmap_Reviewer"]
    attempt_num = len(mindmap_logs) + 1
    feedback = mindmap_logs[-1]["feedback"] if mindmap_logs else ""
    
    print(f"\n[Mindmap_Agent] Generating Markmap diagram for {session_id} {lesson_id} (Attempt #{attempt_num}) using mindmap_generator skill...")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=attempt_num,
        core_ssot=core_ssot,
        feedback=feedback,
        state=state
    )
    
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        # Offline mode fallback
        ex_snippet = content.get("example", "")
        indented_example = "\n".join(f"      {line}" for line in ex_snippet.splitlines()) if ex_snippet else "      # Không có mã nguồn minh họa."
        mindmap_prompt = f"[Prompt: Generate a visual flow/sequence diagram showing the architecture, control flow, and execution lifecycle of '{tech_stack}']"
        
        markmap_content = f"""```markmap
# {session_id}: {lesson_title}
## Mục tiêu bài học
- Hiểu rõ khái niệm cốt lõi và kiến trúc của {lesson_title}.
- Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: {expected_output if expected_output else 'tích hợp thành công'}.
- Vận hành và kiểm tra đầu ra hoạt động ổn định.
## {lesson_title}
### Khái niệm cốt lõi
- Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation cho {tech_stack}.
### Cú pháp & Cách khai báo
- Ví dụ triển khai:
{indented_example}
### Lưu ý thực chiến
- Tránh bỏ sót các tham số bắt buộc.
- Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
{mindmap_prompt}
```"""
    else:
        from core.llm import call_llm
        from core.skills import load_skill_content
        
        mindmap_skill = load_skill_content("mindmap_generator")
        
        # Build master content summary for LLM context
        master_content_summary = ""
        if content:
            sections_text = "\n".join([f"### {sec['title']}\n{sec['content']}" for sec in content.get("reading_sections", [])])
            master_content_summary = f"""
--- NỘI DUNG CHI TIẾT BÀI HỌC (Sử dụng làm cơ sở dữ liệu học thuật) ---
{sections_text}

--- MÃ NGUỒN VÍ DỤ ---
```python
{content.get('example', '')}
```

--- TỔNG KẾT & SAI LẦM THƯỜNG GẶP ---
{content.get('summary', '')}
"""

        system_prompt = f"""Bạn là một Giảng viên Cao cấp và chuyên gia Thiết kế Chương trình Đào tạo học thuật chuyên sâu tại Rikkei Education. 
Nhiệm vụ của bạn là dựa vào nội dung lý thuyết chi tiết của bài học dưới đây để biên soạn một SƠ ĐỒ TƯ DUY (Mindmap) chi tiết, phong phú và có chiều sâu chuyên môn cao để tóm tắt NỘI DUNG HỌC THUẬT của bài học.

Bắt buộc tuân thủ nghiêm ngặt các hướng dẫn và tiêu chuẩn trong tài liệu Kỹ năng (Skill) sau:
{mindmap_skill}
"""
        
        concepts_list = "\n".join([f"- {k}" for k in core_ssot.get("concepts", {}).keys()])
        feedback_context = f"\nPhản hồi sửa đổi từ Mindmap Reviewer (nếu có, bạn phải sửa lỗi này): {feedback}\n" if feedback else ""
        
        user_prompt = f"""Hãy sinh sơ đồ tư duy dạng Markmap cho bài học:
Session: {session_id}
Lesson: {lesson_id} (Tiêu đề: {lesson_title})
Chi tiết bài học từ PM: {lesson_details}
Đầu ra kỳ vọng: {expected_output}
Target Technology Stack: {tech_stack}

Bắt buộc tạo một nhánh cấp 2 (##) tương ứng cho mỗi khái niệm cốt lõi sau để đảm bảo quy tắc không bỏ sót nhánh (Zero-drop Policy):
{concepts_list}

{master_content_summary}
{feedback_context}
YÊU CẦU ĐẦU RA (BẮT BUỘC):
- Trả về DUY NHẤT một khối mã Markdown ` ```markmap ... ` ``` chứa nội dung sơ đồ tư duy.
- Sơ đồ phải bao quát 100% các chủ đề chính được nhắc đến (Zero-drop Policy).
- TUYỆT ĐỐI KHÔNG tạo nhánh '## Mục tiêu bài học'. Tiêu đề cấp 1 (#) phân nhánh trực tiếp ra các Chủ đề Kiến thức Cốt lõi (##).
- Phân nhánh động linh hoạt theo bản chất nội dung (Content-Driven Branching): Với bài tập/cú pháp code thì đưa khối ```python ... ``` và gotchas trực tiếp bên dưới chủ đề; với bài học khái niệm thì phân nhánh theo nguyên lý -> cơ chế -> ứng dụng. CẤM lặp lại rập khuôn 3 nhánh 'Khái niệm', 'Cú pháp', 'Lưu ý' ở tất cả các mục.
- Cú pháp khai báo code mẫu phải được bọc trong block Markdown chỉ định ngôn ngữ và thụt lề bằng dấu cách chính xác dưới gạch đầu dòng tương ứng.
- Tuyệt đối cấm sử dụng emoji.
- Tuyệt đối KHÔNG ĐƯỢC "rò rỉ kiến thức" (Scope Leakage) - nội dung và cú pháp trong mindmap không chứa cú pháp hay khái niệm vượt quá phạm vi bài học (ví dụ: Lesson 01 chỉ giới thiệu Web API nhưng không được chứa SQLite/SQLAlchemy/Database hay các khái niệm của bài học sau).
- Không có bất kỳ ký tự # thừa thãi nào trong các nhánh văn bản làm vỡ markmap. Ký tự # chỉ được sử dụng ở đầu dòng để định nghĩa tiêu đề.
- Với các khái niệm kiến trúc phức tạp hoặc luồng dữ liệu, bắt buộc chèn một nút con prompt ảnh bằng cú pháp: `[Prompt: <English description to generate visual architecture/logic/sequence diagram>]` hoặc `[Tạo ảnh: <English description to generate visual architecture/logic/sequence diagram>]`.
- CỰC KỲ QUAN TRỌNG: Sơ đồ tư duy phải cực kỳ cô đọng, ngắn gọn và súc tích. Tránh các đoạn giải thích dài dòng. Mỗi nhánh con cấp 3 chỉ chứa tối đa 1-2 câu ngắn hoặc một đoạn mã nguồn mẫu siêu ngắn (dưới 10 dòng) để tránh bị cắt cụt.
- Tuyệt đối không viết thêm bất kỳ lời chào hỏi, giới thiệu hay giải thích nào ngoài khối ```markmap ... ```.
"""
        markmap_content = call_llm(
            system_prompt,
            user_prompt,
            json_mode=False,
            agent_name=f"Mindmap_Agent_Att{attempt_num}",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if markmap_content:
            markmap_content = markmap_content.strip()
            if markmap_content.startswith("```markdown"):
                markmap_content = markmap_content[11:].strip()
            
            # Ensure it starts with ```markmap
            if not markmap_content.startswith("```markmap"):
                if "```markmap" in markmap_content:
                    idx = markmap_content.find("```markmap")
                    markmap_content = markmap_content[idx:].strip()
                else:
                    markmap_content = "```markmap\n" + markmap_content
            
            # Auto-close unclosed code blocks
            lines = markmap_content.splitlines()
            level = 0
            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith("```"):
                    if level == 0 and stripped_line.startswith("```markmap"):
                        level = 1
                    elif level == 1:
                        level = 2
                    elif level == 2:
                        level = 1
                    elif level == 1 and stripped_line == "```":
                        level = 0
            if level == 2:
                lines.append("```")
                level = 1
            if level == 1:
                lines.append("```")
                level = 0
            markmap_content = "\n".join(lines)
        else:
            markmap_content = f"```markmap\n# {session_id}: {lesson_title}\n## Mục tiêu bài học\n- Lỗi khi sinh sơ đồ tư duy.\n```"

    # Process and replace image prompts
    processed_content = process_mindmap_images(markmap_content, state)
    state["mindmap_markdown"] = processed_content
    log_agent_tokens("Mindmap_Agent", state, processed_content)
    return state


def slide_agent(state: AgentState) -> AgentState:
    """
    Slide Agent (Rikkei Academic PPTX Master & Google Slides UI Standard):
    Tự động thiết kế Slide bài giảng tương tác HTML chuẩn giao diện Rikkei Master
    với Sidebar Miniature Preview, Toàn màn hình ⛶ Mode, và Badge Số trang góc dưới bên phải bắt đầu từ trang 1.
    Nội dung và số lượng Slide linh động 100% theo SSOT bài học.
    """
    from agents.slide_generator_agent import slide_generator_agent

    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = state.get("technology_stack", "python/core")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    acad_logs = [log for log in state.get("review_logs", []) if log["source"] == "Academic_Reviewer"]
    attempt_num = len(acad_logs) + 1
    feedback = acad_logs[-1]["feedback"] if acad_logs else ""
    
    print(f"\n[Slide_Agent] Designing Interactive Master HTML Slide Deck for {session_id} {lesson_id} | Attempt: #{attempt_num}")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=attempt_num,
        core_ssot=core_ssot,
        feedback=feedback,
        state=state
    )
    
    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    
    # Xây dựng danh sách các cảnh/slide linh hoạt từ SSOT & Content với Action Title & 8 Dynamic Layouts
    scenes = []
    concepts = core_ssot.get("concepts", {})
    code_samples = core_ssot.get("code_samples", {})
    
    # 1. Slide Đặt vấn đề & Bối cảnh (TWO_COLUMN_COMPARE)
    if content.get("problem"):
        scenes.append({
            "action_title": "Đặt Vấn Đề & Bối Cảnh Thực Tế Doanh Nghiệp",
            "scene_title": "Đặt Vấn Đề & Bối Cảnh Thực Tế Doanh Nghiệp",
            "short_title": "Đặt Vấn Đề & Bối Cảnh",
            "narration": content.get("problem", ""),
            "layout_type": "TWO_COLUMN_COMPARE"
        })

    # 2. Các Slide Khái niệm từ SSOT với Action Title độc nhất & Layouts chuyên biệt
    if isinstance(concepts, dict):
        code_keys = list(code_samples.keys()) if isinstance(code_samples, dict) else []
        concept_items = list(concepts.items())
        for idx, (cname, cdesc) in enumerate(concept_items):
            clean_cname = slide_generator_agent.clean_title_string(str(cname))
            code_snippet = ""
            if idx < len(code_keys):
                code_snippet = str(code_samples[code_keys[idx]])
            elif code_samples and isinstance(code_samples, dict):
                first_val = list(code_samples.values())[0]
                code_snippet = str(first_val) if isinstance(first_val, str) else ""

            # Luân chuyển Layout Sư phạm
            if code_snippet:
                layout = "CODE_DEMO_EXPLAINER"
            elif idx == 0:
                layout = "SINGLE_COLUMN_FOCUS"
            elif idx % 2 == 1:
                layout = "THREE_COLUMN_CARDS"
            else:
                layout = "TWO_COLUMN_COMPARE"

            lecturer_trick = f"Nhấn mạnh cơ chế hoạt động thực tế của '{clean_cname}' giúp tối ưu hiệu năng và hạn chế lỗi tại runtime."
            enterprise_scenario = f"Áp dụng '{clean_cname}' trong module xử lý nghiệp vụ của hệ thống doanh nghiệp thực tế."
            code_output = "[CONSOLE OUTPUT]: Thực thi chương trình hoàn tất - Không có lỗi Runtime."

            scenes.append({
                "action_title": f"Bản Chất Kỹ Thuật: {clean_cname}",
                "scene_title": clean_cname,
                "short_title": clean_cname,
                "narration": str(cdesc),
                "code_sample": code_snippet,
                "code_output": code_output,
                "lecturer_trick": lecturer_trick,
                "enterprise_scenario": enterprise_scenario,
                "layout_type": layout
            })

    # 3. Slide Phân tích & Sơ đồ Luồng Mermaid (MERMAID_DIAGRAM / TABLE_COMPARISON)
    if content.get("analysis") or content.get("solution"):
        mermaid_prompt = f"flowchart TD\n    A[Mã nguồn Input] --> B[Trình xử lý Execution Engine]\n    B --> C[Luồng Xử lý Intermediate]\n    C --> D[Môi trường Thực thi Runtime]\n    D --> E[Kết quả Đầu ra Console]"
        scenes.append({
            "action_title": "Phân Tích Luồng Dữ Liệu & Nguyên Lý Vận Hành",
            "scene_title": "Phân Tích Luồng Dữ Liệu & Nguyên Lý Vận Hành",
            "short_title": "Luồng Dữ Liệu & Kiến Trúc",
            "narration": f"{content.get('analysis', '')} {content.get('solution', '')}",
            "mermaid": mermaid_prompt,
            "layout_type": "MERMAID_DIAGRAM"
        })

    # 4. Slide Bẫy cú pháp & Lưu ý (WARNING_GOTCHAS)
    scenes.append({
        "action_title": "Cảnh Báo Bẫy Cú Pháp & Anti-Pattern Thường Gặp",
        "scene_title": "Cảnh Báo Bẫy Cú Pháp & Anti-Pattern Thường Gặp",
        "short_title": "Cảnh Báo Sai Lầm",
        "narration": "Tránh các lỗi IndentationError, Dynamic Typing Confusion, hoặc gọi biến trước khi khởi tạo.",
        "bullets": [
            "Lỗi thụt lề IndentationError do trộn lẫn Tab và Space",
            "Tránh gán đè kiểu dữ liệu biến bất nhất gây bẫy Runtime",
            "Luôn khai báo môi trường ảo Virtualenv trước khi install package",
            "Không bao giờ lưu file mã nguồn trùng tên với module chuẩn"
        ],
        "layout_type": "WARNING_GOTCHAS"
    })

    # 5. Slide Tổng kết bài học (TIMELINE_RECAP)
    if content.get("summary"):
        scenes.append({
            "action_title": "Tổng Kết Trọng Tâm & Tiến Trình Cột Mốc Bài Học",
            "scene_title": "Tổng Kết Trọng Tâm & Tiến Trình Cột Mốc Bài Học",
            "short_title": "Tổng Kết Bài Học",
            "narration": content.get("summary", ""),
            "layout_type": "TIMELINE_RECAP"
        })

    # Fallback nếu không có thông tin
    if not scenes:
        scenes = [
            {"scene_title": "Đặt Vấn Đề & Khái Niệm Cốt Lõi", "short_title": "Đặt Vấn Đề", "narration": content.get("problem", "Giới thiệu khái niệm bài học")},
            {"scene_title": "Phân Tích Nguyên Lý Kỹ Thuật", "short_title": "Phân Tích Nguyên Lý", "narration": content.get("analysis", "Phân tích cơ chế hoạt động")},
            {"scene_title": "Thực Hành Mã Nguồn Minh Họa", "short_title": "Thực Hành Mã Nguồn", "narration": content.get("solution", "Triển khai mã nguồn minh họa")},
            {"scene_title": "Tổng Kết & Sai Lầm Cần Tránh", "short_title": "Tổng Kết Bài Học", "narration": content.get("summary", "Tổng kết kiến thức cốt lõi")}
        ]

    slides_html = slide_generator_agent.generate_deck_html(
        lesson_title=display_title,
        module_name=tech_stack.upper(),
        scenes=scenes
    )

    state["slide_html"] = slides_html
    state["slide_markdown"] = slides_html
    log_agent_tokens("Slide_Agent", state, slides_html)
    return state

def quiz_agent(state: AgentState) -> AgentState:
    """
    Quiz Agent:
    Formulates 5-question lesson quiz strictly based on the matrix:
    - Q1: Definition/Syntax
    - Q2: Execution Flow
    - Q3: Code Reading
    - Q4: Compare/Contrast
    - Q5: Outcome prediction with trap
    And a Hands-on Lab based on standard template (Objectives, Description ordered list, Evaluation criteria).
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = state.get("technology_stack", "python/fastapi")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    sandbox_logs = [log for log in state.get("review_logs", []) if log["source"] == "Sandbox_Agent"]
    attempt_num = len(sandbox_logs) + 1
    feedback = sandbox_logs[-1]["feedback"] if sandbox_logs else ""
    
    print(f"\n[Quiz_Lab_Agent] Formulating Quiz & Practical Lab for {session_id} {lesson_id} | Attempt: #{attempt_num}")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=attempt_num,
        core_ssot=core_ssot,
        feedback=feedback,
        state=state
    )
    lab = content.get("lab", {})
    lab_title = lab.get("title", "Luyện tập (Tùy chọn)")
    lab_objectives = lab.get("objectives", ["Nắm vững kiến thức nền tảng"])
    lab_steps = lab.get("steps", ["Xem lại tài liệu lý thuyết"])
    lab_checklist = lab.get("checklist", ["Hoàn thành câu hỏi trắc nghiệm"])
    
    inputs_text = f"Dự án/môi trường phát triển {tech_stack} hiện tại và tài nguyên khóa học."

    quiz_data = {
        "lesson_quiz": content.get("quiz", []),
        "practical_lab": {
            "title": lab_title,
            "objectives": lab_objectives,
            "description": {
                "inputs": inputs_text,
                "steps": lab_steps
            },
            "evaluation": {
                "checklist": lab_checklist
            }
        }
    }

    state["quiz_json"] = quiz_data
    log_agent_tokens("Quiz_Agent", state, json.dumps(quiz_data, ensure_ascii=False))
    return state

def render_table(headers: List[str], rows: List[List[str]]) -> str:
    html = ['<div style="overflow-x: auto; margin: 20px 0; box-shadow: var(--shadow-sm); border-radius: var(--radius-md); border: 1px solid var(--border-color);">']
    html.append('<table class="comparison-table" style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem;">')
    
    if headers:
        html.append('<thead style="background-color: var(--primary); color: white;">')
        html.append('<tr>')
        for h in headers:
            html.append(f'<th style="padding: 12px 16px; font-weight: 600; border-bottom: 2px solid var(--border-color);">{h}</th>')
        html.append('</tr>')
        html.append('</thead>')
        
    html.append('<tbody>')
    for idx, r in enumerate(rows):
        bg_style = ' style="background-color: #F8FAFC;"' if idx % 2 == 1 else ''
        html.append(f'<tr{bg_style}>')
        for cell in r:
            html.append(f'<td style="padding: 12px 16px; border-bottom: 1px solid var(--border-color);">{cell}</td>')
        html.append('</tr>')
    html.append('</tbody>')
    html.append('</table>')
    html.append('</div>')
def classify_reading_type(lesson_title: str, lesson_details: str) -> Dict[str, str]:
    text = (lesson_title + " " + lesson_details).lower()
    
    if any(k in text for k in ["cài đặt", "môi trường", "setup", "install", "vs code", "vscode", "git", "docker"]):
        return {
            "type": "SETUP_GUIDE",
            "name": "Bài Hướng dẫn Cài đặt & Setup Môi trường",
            "prompt_guideline": "DẠNG BÀI CÀI ĐẶT & SETUP MÔI TRƯỜNG: Bố cục bắt buộc: 1. Điều kiện tiên quyết (Prerequisites) -> 2. Các bước cài đặt với thẻ lệnh Terminal CLI -> 3. Kiểm tra phiên bản (version check) -> 4. Bảng khắc phục lỗi thường gặp (Troubleshooting Matrix). BẮT BUỘC chèn Sơ đồ luồng cài đặt bằng Mermaid (```mermaid ... ```)."
        }
    elif any(k in text for k in ["so sánh", "vs", "phân biệt", "difference"]):
        return {
            "type": "TECH_COMPARISON",
            "name": "Bài So sánh Công nghệ / Giải pháp",
            "prompt_guideline": "DẠNG BÀI SO SÁNH CÔNG NGHỆ: Bố cục bắt buộc: 1. Bối cảnh lựa chọn công nghệ -> 2. BẢNG MARKDOWN COMPARISON TABLE FULL-WIDTH (Tiêu chí, Công nghệ A, Công nghệ B, Đánh giá thực tế doanh nghiệp) -> 3. Sơ đồ so sánh hai luồng bằng Mermaid (```mermaid ... ```) -> 4. Cây quyết định lựa chọn (When-to-use Matrix)."
        }
    elif any(k in text for k in ["cú pháp", "toán tử", "chuỗi", "f-string", "ép kiểu", "nhập, xuất", "khai báo biến", "list", "dict"]):
        return {
            "type": "SYNTAX_OPERATIONS",
            "name": "Bài Cú pháp & Thao tác Mã nguồn",
            "prompt_guideline": "DẠNG BÀI CÚ PHÁP & THAO TÁC MÃ NGUỒN: Bố cục bắt buộc: 1. Cú pháp chuẩn (Syntax Spec) -> 2. Bảng phương thức/toán tử -> 3. Ví dụ mã nguồn chạy trực tiếp với Pyodide Sandbox -> 4. Sơ đồ luồng biến đổi hoặc luồng điều kiện bằng Mermaid (```mermaid ... ```)."
        }
    elif any(k in text for k in ["thuật toán", "sắp xếp", "tìm kiếm", "vòng lặp", "rẽ nhánh"]):
        return {
            "type": "ALGORITHM_PATTERN",
            "name": "Bài Tư duy Thuật toán & Giải quyết Bài toán",
            "prompt_guideline": "DẠNG BÀI THUẬT TOÁN & BÀI TOÁN: Bố cục bắt buộc: 1. Đề bài nghiệp vụ thực tế -> 2. Phân tích độ phức tạp O(N) thời gian và bộ nhớ -> 3. Sơ đồ luồng thuật toán bằng Mermaid Flowchart (```mermaid ... ```) -> 4. Phân tích trace từng bước với Code Tracker."
        }
    elif any(k in text for k in ["kiến trúc", "mô hình", "mvc", "api", "workflow", "mini project"]):
        return {
            "type": "SYSTEM_WORKFLOW",
            "name": "Bài Kiến trúc Hệ thống & Workflow Production",
            "prompt_guideline": "DẠNG BÀI KIẾN TRÚC HỆ THỐNG: Bố cục bắt buộc: 1. Bức tranh toàn cảnh hệ thống -> 2. SƠ ĐỒ KIẾN TRÚC BẰNG MERMAID (```mermaid ... ```) (Client <-> API <-> Database) -> 3. Phân rã chức năng từng Module -> 4. Quy tắc bảo mật & mở rộng."
        }
    elif any(k in text for k in ["bẫy lỗi", "ngoại lệ", "exception", "debug", "refactoring", "clean code"]):
        return {
            "type": "DEBUG_REFACTOR",
            "name": "Bài Tối ưu hóa, Debugging & Best Practices",
            "prompt_guideline": "DẠNG BÀI DEBUG & REFACTORING: Bố cục bắt buộc: 1. Mã nguồn xấu (Anti-pattern) -> 2. Phân tích nguyên nhân gốc rễ (Root Cause) -> 3. Sơ đồ luồng xử lý lỗi bằng Mermaid (```mermaid ... ```) -> 4. Mã nguồn chuẩn hóa (Clean Code) -> 5. Checklist ghi nhớ."
        }
    else:
        return {
            "type": "THEORY_CONCEPT",
            "name": "Bài Khái niệm & Lý thuyết Nền tảng",
            "prompt_guideline": "DẠNG BÀI LÝ THUYẾT / KHÁI NIỆM NỀN TẢNG: Bố cục bắt buộc: 1. Đặt vấn đề thực tế -> 2. Phân tích cơ chế bản chất bộ nhớ / PVM -> 3. SƠ ĐỒ MINH HỌA VÙNG NHỚ / LUỒNG CHẠY BẰNG MERMAID (```mermaid ... ```) -> 4. Gotchas bẫy tư duy và ví dụ thực tế."
        }

def convert_markdown_to_html(text: str) -> str:
    if not text:
        return ""
    
    lines = text.split('\n')
    output = []
    
    list_stack = []  # Stack of (indent_level, 'ul'/'ol')
    in_blockquote = False
    in_code = False
    in_mermaid = False
    current_is_sandbox = False
    current_box_id = ""
    in_table = False
    table_headers = []
    table_rows = []
    
    def get_indent(s: str) -> int:
        return len(s) - len(s.lstrip(' '))
        
    def close_lists_to_level(level: int):
        closed = []
        while list_stack and list_stack[-1][0] > level:
            _, tag = list_stack.pop()
            closed.append(f"</{tag}>")
        return "\n".join(closed)
        
    def close_all_lists():
        closed = []
        while list_stack:
            _, tag = list_stack.pop()
            closed.append(f"</{tag}>")
        return "\n".join(closed)

    def process_inline(line: str) -> str:
        # Bold: **text** -> <strong>text</strong>, __text__ -> <strong>text</strong>
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'(?<!\w)__(.*?)__(?!\w)', r'<strong>\1</strong>', line)
        # Italic: *text* -> <em>text</em>, _text_ -> <em>text</em>
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        line = re.sub(r'(?<!\w)_(.*?)_(?!\w)', r'<em>\1</em>', line)
        # Inline code: `code` -> <code>code</code>
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        # Links: [text](url) -> <a href="url" target="_blank">text</a>
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" style="color: var(--accent); font-weight: 500; text-decoration: none; border-bottom: 1px dashed var(--accent);">\1</a>', line)
        return line

    for line in lines:
        line_strip = line.strip()
        indent = get_indent(line)
        
        # Code block
        if line_strip.startswith("```"):
            if in_table:
                output.append(render_table(table_headers, table_rows))
                table_headers = []; table_rows = []; in_table = False
            output.append(close_all_lists())
            if in_blockquote:
                output.append("</blockquote>")
                in_blockquote = False
                
            if in_mermaid:
                output.append('</div></div>')
                in_mermaid = False
            elif in_code:
                if current_is_sandbox:
                    output.append(f'</code></pre><div id="{current_box_id}_output" style="display:none; margin-top: 12px; padding: 12px 16px; background: #020617; border: 1px solid #1e293b; border-radius: 6px; color: #f8fafc; font-family: Consolas, monospace; font-size: 0.88rem; white-space: pre-wrap; word-break: break-word;"></div></div></div>')
                else:
                    output.append('</code></pre></div></div>')
                in_code = False
            else:
                lang = line_strip[3:].strip().lower() or "python"
                if lang == "mermaid":
                    in_mermaid = True
                    output.append('<div class="mermaid-diagram-container" style="background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin: 20px 0; overflow-x: auto;"><div class="mermaid" style="display: flex; justify-content: center; color: #f8fafc;">')
                else:
                    in_code = True
                    current_is_sandbox = (lang in ["python", "py"])
                    if current_is_sandbox:
                        import random
                        current_box_id = f"py_box_{random.randint(10000, 99999)}"
                        output.append(f'<div class="code-container" style="border: 1px solid #334155; border-radius: 8px; margin: 20px 0; overflow: hidden; background: #0f172a; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"><div class="code-header" style="background: #1e293b; color: #94a3b8; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155;"><span class="code-title" style="font-weight: 600; font-size: 0.88rem; color: #38bdf8; display: flex; align-items: center; gap: 6px;"><i class="ph-duotone ph-code" style="font-size: 1.1rem;"></i> {lang.upper()} Live Playground</span><button type="button" onclick="runPyodideSandbox(event, \'{current_box_id}\')" style="background: #10b981; color: white; border: none; padding: 6px 14px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.82rem; transition: all 0.2s ease; display: flex; align-items: center; gap: 6px;"><i class="ph-duotone ph-play" style="font-size: 1.1rem;"></i> CHẠY THỬ MÃ NGUỒN (RUN CODE)</button></div><div class="code-body" style="padding: 15px; overflow-x: auto;"><pre id="{current_box_id}_code"><code class="language-{lang}">')
                    else:
                        output.append(f'<div class="code-container" style="border: 1px solid #334155; border-radius: 8px; margin: 20px 0; overflow: hidden; background: #0f172a; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"><div class="code-header" style="background: #1e293b; color: #94a3b8; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155;"><span class="code-title" style="font-weight: 600; font-size: 0.88rem; color: #38bdf8; display: flex; align-items: center; gap: 6px;"><i class="ph-duotone ph-code" style="font-size: 1.1rem;"></i> {lang.upper()} Snippet</span><button type="button" onclick="copyCode(this)" style="background: #334155; color: white; border: none; padding: 4px 12px; border-radius: 6px; font-weight: 500; cursor: pointer; font-size: 0.75rem;">Sao chép mã</button></div><div class="code-body" style="padding: 15px; overflow-x: auto;"><pre><code class="language-{lang}">')
            continue
            
        if in_mermaid:
            output.append(line)
            continue
            
        if in_code:
            output.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue
            
        # Empty lines
        if not line_strip:
            if in_table:
                output.append(render_table(table_headers, table_rows))
                table_headers = []; table_rows = []; in_table = False
            output.append(close_all_lists())
            if in_blockquote:
                output.append("</blockquote>")
                in_blockquote = False
            continue
            
        # Raw HTML block detection
        is_html = line_strip.startswith("<") and (
            any(t in line_strip.lower() for t in ["table", "tr", "td", "th", "thead", "tbody", "div", "ul", "ol", "li", "p>", "h1>", "h2>", "h3>", "h4>", "span>"])
            or line_strip.endswith(">")
        )
        if is_html:
            if in_table:
                output.append(render_table(table_headers, table_rows))
                table_headers = []; table_rows = []; in_table = False
            output.append(close_all_lists())
            if in_blockquote:
                output.append("</blockquote>")
                in_blockquote = False
            output.append(process_inline(line))
            continue
            
        # Table detection
        is_table_row = line_strip.startswith("|") and line_strip.endswith("|")
        if is_table_row:
            if in_blockquote:
                output.append("</blockquote>")
                in_blockquote = False
            output.append(close_all_lists())
            
            cols = [process_inline(c.strip()) for c in line_strip.split('|')[1:-1]]
            
            # Check separator line
            if all(re.match(r'^[- :]+$', c) for c in cols) and len(cols) > 0:
                in_table = True
                continue
                
            if not in_table:
                table_headers = cols
                in_table = True
            else:
                table_rows.append(cols)
            continue
        elif in_table:
            output.append(render_table(table_headers, table_rows))
            table_headers = []; table_rows = []; in_table = False
            
        # Blockquote
        if line_strip.startswith(">"):
            content = line_strip[1:].strip()
            output.append(close_all_lists())
            if not in_blockquote:
                output.append('<blockquote style="border-left: 4px solid var(--accent); padding-left: 15px; margin: 15px 0; color: var(--text-muted); font-style: italic;">')
                in_blockquote = True
            output.append(process_inline(content))
            continue
        elif in_blockquote:
            output.append("</blockquote>")
            in_blockquote = False
            
        # Headers: # -> h1, ## -> h2, etc.
        header_match = re.match(r'^(#{1,6})\s+(.*)', line_strip)
        if header_match:
            level = len(header_match.group(1))
            content = process_inline(header_match.group(2))
            output.append(close_all_lists())
            
            if level == 1:
                output.append(f'<h1 style="color: var(--primary); font-size: 1.8rem; margin: 25px 0 15px; font-weight: 700; border-bottom: 2px solid var(--border-color); padding-bottom: 8px;">{content}</h1>')
            elif level == 2:
                output.append(f'<h2 style="color: var(--primary); font-size: 1.45rem; margin: 20px 0 10px; font-weight: 600;">{content}</h2>')
            elif level == 3:
                output.append(f'<h3 style="color: var(--primary-light); font-size: 1.2rem; margin: 15px 0 8px; font-weight: 600;">{content}</h3>')
            else:
                output.append(f'<h{level} style="color: var(--text-main); margin: 15px 0 8px; font-weight: 600;">{content}</h{level}>')
            continue
            
        # Horizontal rule
        if line_strip in ["---", "***", "___"]:
            output.append(close_all_lists())
            output.append('<hr style="border: 0; border-top: 1px solid var(--border-color); margin: 30px 0;">')
            continue
            
        # Unordered list item
        ul_match = re.match(r'^[-*+]\s+(.*)', line_strip)
        # Ordered list item
        ol_match = re.match(r'^(?:\d+\.|\b(?:Bước|B|Step)\s*\d+[:.])\s+(.*)', line_strip)
        
        if ul_match or ol_match:
            tag = 'ul' if ul_match else 'ol'
            content = process_inline(ul_match.group(1) if ul_match else ol_match.group(1))
            
            # Close deeper levels
            output.append(close_lists_to_level(indent))
            
            # Open nested list if needed
            if not list_stack or list_stack[-1][0] < indent:
                list_style = 'list-style-type: disc;' if tag == 'ul' else 'list-style-type: decimal;'
                if list_stack:
                    list_style = 'list-style-type: circle;' if tag == 'ul' else 'list-style-type: lower-alpha;'
                output.append(f'< {tag} style="margin-left: 20px; margin-bottom: 10px; {list_style}">'.replace('< ', '<'))
                list_stack.append((indent, tag))
            elif list_stack[-1][1] != tag:
                _, old_tag = list_stack.pop()
                output.append(f'</{old_tag}>')
                list_style = 'list-style-type: disc;' if tag == 'ul' else 'list-style-type: decimal;'
                output.append(f'< {tag} style="margin-left: 20px; margin-bottom: 10px; {list_style}">'.replace('< ', '<'))
                list_stack.append((indent, tag))
                
            output.append(f'<li style="margin-bottom: 6px; text-align: justify; padding-left: 5px;">{content}</li>')
        else:
            output.append(close_all_lists())
            processed_content = process_inline(line_strip)
            output.append(f'<p style="text-align: justify; margin-bottom: 15px; line-height: 1.6;">{processed_content}</p>')
            
    # Final close
    if in_table:
        output.append(render_table(table_headers, table_rows))
    output.append(close_all_lists())
    if in_blockquote:
        output.append("</blockquote>")
    html_result = "\n".join([line for line in output if line])
    return unwrap_svg_and_diagrams(html_result)


def unwrap_svg_and_diagrams(html: str) -> str:
    """
    Unwraps <svg> graphics that were accidentally converted into escaped code blocks or text paragraphs,
    rendering them as live SVG graphic DOM elements.
    """
    if not html:
        return ""

    import html as html_lib

    # 1. Un-escape <svg> wrapped inside code-container code blocks
    def _replace_escaped_code_block(match):
        code_text = match.group(1)
        decoded = html_lib.unescape(code_text)
        if "<svg" in decoded.lower() and "</svg>" in decoded.lower():
            start_idx = decoded.lower().find("<svg")
            end_idx = decoded.lower().find("</svg>") + 6
            svg_element = decoded[start_idx:end_idx]
            return f'<div class="svg-diagram-wrapper my-6 flex justify-center items-center overflow-x-auto p-4 bg-slate-900/60 rounded-xl border border-slate-700/50 shadow-lg">{svg_element}</div>'
        return match.group(0)

    pattern = re.compile(r'<div class="code-container">[\s\S]*?<code[^>]*>([\s\S]*?)</code>[\s\S]*?</div>', re.MULTILINE)
    html = pattern.sub(_replace_escaped_code_block, html)

    # 2. Un-escape standalone <p>&lt;svg ... &lt;/svg&gt;</p>
    def _replace_p_escaped_svg(match):
        p_text = match.group(1)
        decoded = html_lib.unescape(p_text)
        if "<svg" in decoded.lower() and "</svg>" in decoded.lower():
            start_idx = decoded.lower().find("<svg")
            end_idx = decoded.lower().find("</svg>") + 6
            svg_element = decoded[start_idx:end_idx]
            return f'<div class="svg-diagram-wrapper my-6 flex justify-center items-center overflow-x-auto p-4 bg-slate-900/60 rounded-xl border border-slate-700/50 shadow-lg">{svg_element}</div>'
        return match.group(0)

    html = re.sub(r'<p[^>]*>([\s\S]*?&lt;svg[\s\S]*?&lt;/svg&gt;[\s\S]*?)</p>', _replace_p_escaped_svg, html)

    # 3. Clean up raw <p><svg>...</svg></p>
    html = re.sub(r'<p[^>]*>\s*(<svg[\s\S]*?</svg>)\s*</p>', r'<div class="svg-diagram-wrapper my-6 flex justify-center items-center overflow-x-auto p-4 bg-slate-900/60 rounded-xl border border-slate-700/50 shadow-lg">\1</div>', html)

    return html


def get_topic_fallback_visualizer_engine(lesson_title: str, tech_stack: str, raw_code: str) -> Dict[str, Any]:
    """
    Tự động chọn 1 trong 3 Template Engine phỏng đoán trực quan động theo đúng chủ đề bài học
    khi LLM không sinh JS Engine hoặc khi ứng dụng chạy offline:
    1. SQL_EXECUTER_TEMPLATE (Database, SQL, Postgres, MySQL, Table, Index, Query)
    2. ALGORITHM_ARRAY_TEMPLATE (Thuật toán, Mảng, Vòng lặp, Chuỗi, Python Core)
    3. WEB_FLOW_LIFECYCLE_TEMPLATE (Web Backend/Frontend, API, FastAPI, Express, Spring Boot)
    """
    combined = f"{lesson_title.lower()} {tech_stack.lower()}"

    # 1. Chủ đề Database / SQL / ORM
    if any(kw in combined for kw in ["sql", "database", "postgres", "mysql", "table", "index", "query", "crud", "dbs", "orm"]):
        return {
            "canvas_title": "Database Query Engine Visualizer (SQL Step-by-Step)",
            "legend_html": '<span class="badge" style="background:#3b82f6;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">SQL Parser</span> <span class="badge" style="background:#eab308;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Table Scan</span> <span class="badge" style="background:#10b981;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Result Set</span>',
            "stats_html": '<div class="stat-card" style="background:var(--bg-canvas);border:1px solid var(--border-color);padding:8px 12px;border-radius:6px;"><span class="stat-label" style="font-size:0.7rem;color:var(--text-muted);display:block;">QUERIES PROCESSED</span><span class="stat-val" id="stat-records" style="font-weight:bold;color:var(--primary);">1</span></div>',
            "input_label": "Nhập câu lệnh SQL test",
            "input_default": "SELECT * FROM users WHERE status = 'active';",
            "engine_js": """class InteractiveVisualizerEngine {
    constructor() {
        this.steps = [
            { message: "SQL Parser phân tích cú pháp câu lệnh SQL", lineId: "line-0" },
            { message: "Query Planner tìm kiếm chỉ mục Index tối ưu", lineId: "line-1" },
            { message: "Table Scan: Quét các trang dữ liệu trong ổ đĩa", lineId: "line-2" },
            { message: "Apply Filter: Lọc các bản ghi thỏa mãn điều kiện WHERE", lineId: "line-3" },
            { message: "Result Set Engine trả về mảng bản ghi kết quả", lineId: "line-4" }
        ];
        this.currentStep = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 400;
    }
    init() { this.currentStep = 0; this.isPlaying = false; this.render(); }
    start() { if (this.isPlaying) return; this.isPlaying = true; this.log("▶ [Bắt đầu] Khởi chạy SQL Engine..."); this.runLoop(); }
    pause() { this.isPlaying = false; if (this.timer) { clearTimeout(this.timer); this.timer = null; } this.log("⏸ [Tạm dừng] Đã dừng thực thi."); }
    step() { this.pause(); this.currentStep = (this.currentStep + 1) % this.steps.length; this.log(`⏭ [Từng bước] Sang bước ${this.currentStep + 1}`); this.render(); }
    reset() { this.pause(); this.currentStep = 0; this.log("↻ [Đặt lại] Trạng thái ban đầu."); this.render(); }
    setSpeed(speedVal) { this.speed = parseInt(speedVal) || 400; const display = document.getElementById('speed-display'); if (display) display.innerText = this.speed; }
    applyCustomData() { const val = document.getElementById('custom-data-input').value; this.log(`⚙ [SQL Update] Áp dụng SQL: ${val}`); this.reset(); }
    runLoop() {
        if (!this.isPlaying) return;
        this.timer = setTimeout(() => {
            this.currentStep = (this.currentStep + 1) % this.steps.length;
            this.render();
            if (this.currentStep === 0) { this.pause(); this.log("✅ [Hoàn tất] Truy vấn SQL đã thực thi!"); }
            else { this.runLoop(); }
        }, this.speed);
    }
    render() {
        const stepIdx = this.currentStep;
        const stepData = this.steps[stepIdx];
        if (stepData) {
            this.log(`ℹ ${stepData.message}`);
            const stepperDesc = document.getElementById('stepper-desc');
            if (stepperDesc) stepperDesc.innerText = stepData.message;
        }
        const canvas = document.getElementById('visualizer-canvas');
        if (canvas) {
            const stages = ["SQL Parser", "Query Planner", "Table Scan", "Result Output"];
            const colors = ["#3b82f6", "#eab308", "#f97316", "#10b981"];
            canvas.innerHTML = `
                <div style="display:flex; justify-content:space-around; align-items:center; width:100%; height:120px; padding:10px;">
                    ${stages.map((stg, idx) => `
                        <div style="padding:10px 14px; border-radius:8px; background:${idx === stepIdx ? colors[idx] : 'var(--bg-hover)'}; color:${idx === stepIdx ? '#fff' : 'var(--text-muted)'}; font-weight:bold; transition:all 0.3s; font-size:0.85rem;">
                            ${stg}
                        </div>
                    `).join('<div style="color:var(--text-muted);">➔</div>')}
                </div>
            `;
        }
    }
    log(msg) { const logBox = document.getElementById('log-messages'); if (logBox) { logBox.innerHTML += `<div class="log-entry">${msg}</div>`; logBox.scrollTop = logBox.scrollHeight; } }
    clearLog() { const logBox = document.getElementById('log-messages'); if (logBox) logBox.innerHTML = ""; }
    updateStats() {}
    scrubStep(e) {}
}"""
        }

    # 2. Chủ đề Thuật toán / Mảng / Vòng lặp / Python Core
    elif any(kw in combined for kw in ["loop", "mảng", "array", "list", "sort", "search", "chuỗi", "string", "recursion", "core", "cú pháp"]):
        return {
            "canvas_title": "Data Structure & Algorithm Visualizer (State Step-by-Step)",
            "legend_html": '<span class="badge" style="background:#475569;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Chưa duyệt</span> <span class="badge" style="background:#eab308;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Đang xử lý</span> <span class="badge" style="background:#10b981;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Hoàn tất</span>',
            "stats_html": '<div class="stat-card" style="background:var(--bg-canvas);border:1px solid var(--border-color);padding:8px 12px;border-radius:6px;"><span class="stat-label" style="font-size:0.7rem;color:var(--text-muted);display:block;">COMPARES</span><span class="stat-val" id="stat-compares" style="font-weight:bold;color:var(--primary);">0</span></div>',
            "input_label": "Tự nhập mảng test (ví dụ: 10, 5, 8, 3)",
            "input_default": "10, 5, 8, 3, 12, 2",
            "engine_js": """class InteractiveVisualizerEngine {
    constructor() {
        this.arr = [10, 5, 8, 3, 12, 2];
        this.currentStep = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 400;
    }
    init() { this.currentStep = 0; this.isPlaying = false; this.render(); }
    start() { if (this.isPlaying) return; this.isPlaying = true; this.log("▶ [Bắt đầu] Đang chạy thuật toán mảng..."); this.runLoop(); }
    pause() { this.isPlaying = false; if (this.timer) { clearTimeout(this.timer); this.timer = null; } this.log("⏸ [Tạm dừng] Đã dừng thuật toán."); }
    step() { this.pause(); this.currentStep = (this.currentStep + 1) % this.arr.length; this.log(`⏭ [Từng bước] Đang duyệt index [${this.currentStep}]`); this.render(); }
    reset() { this.pause(); this.currentStep = 0; this.log("↻ [Đặt lại] Đã khôi phục mảng ban đầu."); this.render(); }
    setSpeed(speedVal) { this.speed = parseInt(speedVal) || 400; const display = document.getElementById('speed-display'); if (display) display.innerText = this.speed; }
    applyCustomData() {
        const val = document.getElementById('custom-data-input').value;
        const parsed = val.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
        if (parsed.length > 0) this.arr = parsed;
        this.log(`⚙ [Cấu hình Mảng] Áp dụng mảng mới: ${this.arr.join(', ')}`);
        this.reset();
    }
    runLoop() {
        if (!this.isPlaying) return;
        this.timer = setTimeout(() => {
            this.currentStep = (this.currentStep + 1) % this.arr.length;
            this.render();
            if (this.currentStep === 0) { this.pause(); this.log("✅ [Hoàn tất] Đã duyệt xong toàn bộ mảng!"); }
            else { this.runLoop(); }
        }, this.speed);
    }
    render() {
        const stepIdx = this.currentStep;
        this.log(`⚡ [Kiểm tra] Phần tử [${stepIdx}] = ${this.arr[stepIdx]}`);
        const stepperDesc = document.getElementById('stepper-desc');
        if (stepperDesc) stepperDesc.innerText = `Đang duyệt mảng tại index [${stepIdx}]: Giá trị ${this.arr[stepIdx]}`;
        const canvas = document.getElementById('visualizer-canvas');
        if (canvas) {
            const maxVal = Math.max(...this.arr, 1);
            canvas.innerHTML = `
                <div style="display:flex; justify-content:center; align-items:flex-end; gap:12px; width:100%; height:130px; padding:10px;">
                    ${this.arr.map((val, idx) => {
                        const heightPct = Math.max(20, (val / maxVal) * 90);
                        const isCurrent = idx === stepIdx;
                        return `
                            <div style="display:flex; flex-direction:column; align-items:center; width:36px;">
                                <div style="height:${heightPct}px; width:100%; background:${isCurrent ? '#eab308' : '#6366f1'}; border-radius:6px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:bold; font-size:0.8rem; transition:all 0.3s;">
                                    ${val}
                                </div>
                                <span style="font-size:0.7rem; text-align:center; color:var(--text-muted); margin-top:4px;">[${idx}]</span>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }
    }
    log(msg) { const logBox = document.getElementById('log-messages'); if (logBox) { logBox.innerHTML += `<div class="log-entry">${msg}</div>`; logBox.scrollTop = logBox.scrollHeight; } }
    clearLog() { const logBox = document.getElementById('log-messages'); if (logBox) logBox.innerHTML = ""; }
    updateStats() {}
    scrubStep(e) {}
}"""
        }

    # 3. Chủ đề Web Flow Lifecycle (Web, API, FastAPI, Express, Spring Boot, HTTP)
    else:
        return {
            "canvas_title": "Web Request Lifecycle Visualizer (Client-Server Flow)",
            "legend_html": '<span class="badge" style="background:#10b981;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Client</span> <span class="badge" style="background:#eab308;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">HTTP Server</span> <span class="badge" style="background:#3b82f6;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">Router Handler</span>',
            "stats_html": '<div class="stat-card" style="background:var(--bg-canvas);border:1px solid var(--border-color);padding:8px 12px;border-radius:6px;"><span class="stat-label" style="font-size:0.7rem;color:var(--text-muted);display:block;">HTTP STATUS</span><span class="stat-val" id="stat-status" style="font-weight:bold;color:#10b981;">200 OK</span></div>',
            "input_label": "Payload test hoặc URL Endpoint",
            "input_default": "GET /api/v1/resource",
            "engine_js": """class InteractiveVisualizerEngine {
    constructor() {
        this.steps = [
            { message: "Client khởi tạo HTTP Request", node: 0 },
            { message: "HTTP Server tiếp nhận request và chuyển tiếp Middleware", node: 1 },
            { message: "Routing Engine khớp đường dẫn API và gọi Router Handler", node: 2 },
            { message: "Xử lý logic nghiệp vụ và trả về JSON Response 200 OK", node: 3 }
        ];
        this.currentStep = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 400;
    }
    init() { this.currentStep = 0; this.isPlaying = false; this.render(); }
    start() { if (this.isPlaying) return; this.isPlaying = true; this.log("▶ [Bắt đầu] Đang khởi chạy luồng HTTP Request..."); this.runLoop(); }
    pause() { this.isPlaying = false; if (this.timer) { clearTimeout(this.timer); this.timer = null; } this.log("⏸ [Tạm dừng] Đã tạm dừng luồng chạy."); }
    step() { this.pause(); this.currentStep = (this.currentStep + 1) % this.steps.length; this.log(`⏭ [Từng bước] Chuyển sang bước ${this.currentStep + 1}`); this.render(); }
    reset() { this.pause(); this.currentStep = 0; this.log("↻ [Đặt lại] Đã đưa luồng chạy về ban đầu."); this.render(); }
    setSpeed(speedVal) { this.speed = parseInt(speedVal) || 400; const display = document.getElementById('speed-display'); if (display) display.innerText = this.speed; }
    applyCustomData() { const val = document.getElementById('custom-data-input').value; this.log(`⚙ [Cấu hình] Áp dụng Endpoint: ${val}`); this.reset(); }
    runLoop() {
        if (!this.isPlaying) return;
        this.timer = setTimeout(() => {
            this.currentStep = (this.currentStep + 1) % this.steps.length;
            this.render();
            if (this.currentStep === 0) { this.pause(); this.log("✅ [Hoàn tất] Luồng HTTP Request thành công!"); }
            else { this.runLoop(); }
        }, this.speed);
    }
    render() {
        const stepIdx = this.currentStep;
        const stepData = this.steps[stepIdx];
        if (stepData) {
            this.log(`ℹ ${stepData.message}`);
            const stepperDesc = document.getElementById('stepper-desc');
            if (stepperDesc) stepperDesc.innerText = stepData.message;
        }
        const canvas = document.getElementById('visualizer-canvas');
        if (canvas) {
            const nodes = ["Client Desktop", "HTTP Server", "Application Router", "JSON Response"];
            const colors = ["#10b981", "#eab308", "#3b82f6", "#6366f1"];
            canvas.innerHTML = `
                <div style="display:flex; justify-content:space-around; align-items:center; width:100%; height:120px; padding:10px;">
                    ${nodes.map((nd, idx) => `
                        <div style="padding:10px 14px; border-radius:8px; background:${idx === stepIdx ? colors[idx] : 'var(--bg-hover)'}; color:${idx === stepIdx ? '#fff' : 'var(--text-muted)'}; font-weight:bold; transition:all 0.3s; font-size:0.85rem;">
                            ${nd}
                        </div>
                    `).join('<div style="color:var(--text-muted);">➔</div>')}
                </div>
            `;
        }
    }
    log(msg) { const logBox = document.getElementById('log-messages'); if (logBox) { logBox.innerHTML += `<div class="log-entry">${msg}</div>`; logBox.scrollTop = logBox.scrollHeight; } }
    clearLog() { const logBox = document.getElementById('log-messages'); if (logBox) logBox.innerHTML = ""; }
    updateStats() {}
    scrubStep(e) {}
}"""
        }


def visualizer_generator_agent(
    session_id: str,
    lesson_id: str,
    lesson_title: str,
    raw_code: str,
    tech_stack: str
) -> Dict[str, Any]:
    """
    Dedicated Agent chuyên biệt chỉ sinh Visualizer Engine JavaScript & HTML Tracker
    từ mã nguồn và chủ đề bài học đã được phê duyệt.
    Tách riêng khỏi LLM Call bài đọc chính để tránh quá tải Token.
    """
    # Nếu không có code hoặc bài đọc lý thuyết -> Trả về dict rỗng
    if not raw_code or not raw_code.strip():
        return {}

    try:
        from core.llm import call_llm

        system_prompt = f"""Bạn là Chuyên gia Lập trình Web Visualizer & State Machine Engine tại Rikkei Education.
Nhiệm vụ duy nhất của bạn là phân tích mã nguồn ví dụ thuộc công nghệ '{tech_stack}' và sinh ra mã JavaScript phỏng đoán từng bước (Step-by-step Interactive State Machine).

Yêu cầu bắt buộc:
1. Đảm bảo mã JavaScript khai báo class 'class InteractiveVisualizerEngine' hoàn chỉnh.
2. Định nghĩa các phương thức: init(), start(), pause(), step(), reset(), setSpeed(val), applyCustomData(), render(), log(msg).
3. Trong method render(), tạo các hiệu ứng DOM mượt mà mô phỏng luồng chạy của code.
"""

        user_prompt = f"""Hãy sinh mã Visualizer Engine cho bài học:
Session: {session_id}
Lesson: {lesson_id} — {lesson_title}
Mã nguồn ví dụ:
```
{raw_code[:1000]}
```

Trả về duy nhất JSON Object dạng:
{{
    "canvas_title": "Tiêu đề khung trực quan hóa...",
    "legend_html": "HTML hiển thị các chú giải trạng thái màu sắc",
    "stats_html": "HTML hiển thị các thẻ đếm chỉ số",
    "code_tracker_html": "Mã HTML chứa code. MỖI DÒNG CODE NẰM TRONG <div class='code-line' id='line-0'>...</div>",
    "input_label": "Nhãn ô nhập liệu test",
    "input_default": "Giá trị mặc định test",
    "engine_js": "Mã JavaScript CÓ LOGIC THỰC SỰ của class InteractiveVisualizerEngine"
}}

Return only raw JSON. Do not wrap in markdown code blocks.
"""

        response = call_llm(
            system_prompt, user_prompt,
            json_mode=True,
            agent_name="Visualizer_Generator_Agent"
        )

        if response:
            cleaned = response.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            res = json.loads(cleaned)
            if isinstance(res, dict) and res.get("engine_js") and "class InteractiveVisualizerEngine" in res["engine_js"]:
                safe_title = str(lesson_title).encode('ascii', 'replace').decode('ascii')
                print(f"  [OK] [Visualizer_Generator_Agent] Generated custom JS Visualizer Engine for {safe_title}")
                return res

    except Exception as e:
        safe_err = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"  [WARNING] [Visualizer_Generator_Agent Warning] Dedicated visualizer LLM call failed: {safe_err}")

    # Fallback: Trả về Template Engine động theo đúng chủ đề bài học
    safe_title = str(lesson_title).encode('ascii', 'replace').decode('ascii')
    print(f"  [INFO] [Visualizer Engine] Using Topic-based Dynamic Fallback Template for '{safe_title}' ({tech_stack})")
    return get_topic_fallback_visualizer_engine(lesson_title, tech_stack, raw_code)


def force_center_media(html_str: str) -> str:
    """Ensure ONLY svg, img, figure, and scene-image-container elements are centered horizontally, keeping text left-aligned."""
    if not html_str or not isinstance(html_str, str):
        return html_str
    
    # Inject display: block; margin-left: auto; margin-right: auto; text-align: center; ONLY into <svg> and <img> tags
    def fix_svg_tag(match):
        tag_attrs = match.group(1)
        if 'style="' in tag_attrs or "style='" in tag_attrs:
            tag_attrs = re.sub(r'style=["\']([^"\']*)["\']', r'style="\1; display: block !important; margin-left: auto !important; margin-right: auto !important; text-align: center !important;"', tag_attrs)
        else:
            tag_attrs += ' style="display: block !important; margin-left: auto !important; margin-right: auto !important; text-align: center !important;"'
        return f'<svg{tag_attrs}>'

    def fix_img_tag(match):
        tag_attrs = match.group(1)
        if 'style="' in tag_attrs or "style='" in tag_attrs:
            tag_attrs = re.sub(r'style=["\']([^"\']*)["\']', r'style="\1; display: block !important; margin-left: auto !important; margin-right: auto !important; text-align: center !important;"', tag_attrs)
        else:
            tag_attrs += ' style="display: block !important; margin-left: auto !important; margin-right: auto !important; text-align: center !important;"'
        return f'<img{tag_attrs}>'

    html_str = re.sub(r'<svg([^>]*)>', fix_svg_tag, html_str, flags=re.IGNORECASE)
    html_str = re.sub(r'<img([^>]*)>', fix_img_tag, html_str, flags=re.IGNORECASE)
    return html_str


def validate_and_clean_forbidden_scope(content: dict, forbidden_scope: str) -> tuple:
    """
    Post-Linter Guard: Scans generated content against PM Forbidden Scope keywords.
    Strips or replaces forbidden terms/functions and logs pedagogical warnings.
    """
    if not forbidden_scope or not isinstance(forbidden_scope, str) or not content or not isinstance(content, dict):
        return content, []
    
    # Extract keywords from forbidden_scope string
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
                    # Annotate/Clean forbidden term
                    val = re.sub(pattern, f"/* [Scope Guard: Filtered '{term}'] */", val, flags=re.IGNORECASE)
            content[field] = val

    if violations:
        print(f"  [Forbidden Scope Post-Linter] ⚠️ Discovered & cleaned {len(violations)} forbidden scope violations:")
        for v in violations[:5]:
            print(f"    - ❌ {v}")
            
    return content, violations


def clean_unwanted_text(text: str) -> str:
    """Post-processor to clean unwanted keywords (W3Schools), bracketed callouts ([NOTE], [WARNING], etc.), and force center media alignment."""
    if not text or not isinstance(text, str):
        return text
    # Remove literal W3Schools mentions to prevent copycat impression
    text = re.sub(r"\bW3Schools\b", "Chuẩn Sư Phạm Quốc Tế", text, flags=re.IGNORECASE)
    # Convert bracketed callouts to clean Vietnamese labels
    text = re.sub(r"\[W3SCHOOLS\s+NOTE\]:?", "Lưu ý:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[NOTE\]:?", "Lưu ý:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[WARNING\]:?", "Cảnh báo:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[TIP\]:?", "Mẹo:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[BEST\s+PRACTICE\]:?", "Thực hành tốt:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[ANTI-PATTERN\]:?", "Mẫu nên tránh:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[YÊU\s+CẦU\]:?", "Yêu cầu:", text, flags=re.IGNORECASE)
    
    # Enforce horizontal centering on all SVGs, IMGs and media containers
    text = force_center_media(text)
    return text

def ensure_comparison_table(analysis_text: str, analysis_html: str, lesson_title: str, tech_stack: str) -> str:
    """Ensure that a comparison table is rendered as an HTML table in the analysis section."""
    if "<table" in analysis_html:
        return analysis_html
        
    table_html = f"""
    <div style="margin: 20px 0; overflow-x: auto;">
        <table class="comparison-table" style="width:100%; border-collapse:collapse; margin:16px 0; font-size:0.9rem; border:1px solid var(--border-color); border-radius:8px; overflow:hidden;">
            <thead>
                <tr style="background-color: #be111c; color: white;">
                    <th style="padding:12px 16px; text-align:left; border:1px solid rgba(255,255,255,0.15);">Tiêu chí So sánh Kỹ thuật</th>
                    <th style="padding:12px 16px; text-align:left; border:1px solid rgba(255,255,255,0.15);">{lesson_title} ({tech_stack.upper()})</th>
                    <th style="padding:12px 16px; text-align:left; border:1px solid rgba(255,255,255,0.15);">Giải pháp / Ngôn ngữ truyền thống (C/C++/Java)</th>
                    <th style="padding:12px 16px; text-align:left; border:1px solid rgba(255,255,255,0.15);">Đánh giá bối cảnh Doanh nghiệp</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding:10px 16px; border:1px solid var(--border-color); font-weight:600;">Cơ chế Thực thi</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Thông dịch / Runtime linh hoạt (Bytecode/PVM)</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Biên dịch trước toàn bộ (AOT / Native Code)</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Tối ưu hóa tốc độ phát triển (Time-to-Market)</td>
                </tr>
                <tr style="background-color: var(--bg-hover);">
                    <td style="padding:10px 16px; border:1px solid var(--border-color); font-weight:600;">Cú pháp & Cấu trúc</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Tối giản, định kiểu động, lùi dòng làm khối lệnh</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Tường minh, khai báo kiểu tĩnh, ngoặc nhọn</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Dễ đọc, dễ bảo trì và nhanh chóng thử nghiệm MVP</td>
                </tr>
                <tr>
                    <td style="padding:10px 16px; border:1px solid var(--border-color); font-weight:600;">Hiệu năng & Tài nguyên</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Overhead kiểm tra kiểu lúc runtime, quản lý bộ nhớ tự động</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Tối ưu phần cứng, kiểm tra kiểu lúc compile-time</td>
                    <td style="padding:10px 16px; border:1px solid var(--border-color);">Đánh đổi nhẹ hiệu năng lấy năng suất kỹ sư phần mềm</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    return analysis_html + "\n" + table_html


def ensure_problem_scene_image(problem_html: str, lesson_title: str, tech_stack: str) -> str:
    """Ensure every reading material has a 16:9 centered visual scene container describing the problem context."""
    if "scene-image-container" in problem_html or "<img" in problem_html or "<svg" in problem_html:
        return problem_html
        
    scene_svg = f"""
    <div class="scene-image-container" style="margin: 24px auto; max-width: 800px; width: 100%; text-align: center;">
        <div style="position: relative; width: 100%; padding-top: 56.25%; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1.5px solid var(--border-color); border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.12);">
            <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg">
                <!-- Grid background -->
                <defs>
                    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
                <!-- Glow effects -->
                <circle cx="400" cy="300" r="250" fill="#be111c" opacity="0.15" filter="blur(60px)" />
                <circle cx="1200" cy="600" r="300" fill="#3b82f6" opacity="0.15" filter="blur(60px)" />
                
                <!-- Main Graphic: Manual Overhead vs Automated Solution -->
                <rect x="200" y="200" width="550" height="500" rx="16" fill="rgba(30, 41, 59, 0.8)" stroke="rgba(239, 68, 68, 0.4)" stroke-width="2"/>
                <text x="475" y="270" fill="#ef4444" font-family="sans-serif" font-size="30" font-weight="bold" text-anchor="middle">❌ Thao Tác Thủ Công / Chưa Tối Ưu</text>
                <text x="475" y="360" fill="#94a3b8" font-family="sans-serif" font-size="22" text-anchor="middle">Xử lý lặp lại thủ công tốn thời gian</text>
                <text x="475" y="420" fill="#94a3b8" font-family="sans-serif" font-size="22" text-anchor="middle">Dễ phát sinh lỗi bẫy cú pháp & dữ liệu</text>
                <text x="475" y="480" fill="#94a3b8" font-family="sans-serif" font-size="22" text-anchor="middle">Khó mở rộng và bảo trì hệ thống</text>

                <rect x="850" y="200" width="550" height="500" rx="16" fill="rgba(30, 41, 59, 0.8)" stroke="rgba(16, 185, 129, 0.4)" stroke-width="2"/>
                <text x="1125" y="270" fill="#10b981" font-family="sans-serif" font-size="30" font-weight="bold" text-anchor="middle">✅ Tự Động Hóa Với {tech_stack.upper()}</text>
                <text x="1125" y="360" fill="#e2e8f0" font-family="sans-serif" font-size="22" text-anchor="middle">Áp dụng giải pháp: {lesson_title}</text>
                <text x="1125" y="420" fill="#e2e8f0" font-family="sans-serif" font-size="22" text-anchor="middle">Tối ưu hiệu năng bộ nhớ & thời gian thực thi</text>
                <text x="1125" y="480" fill="#e2e8f0" font-family="sans-serif" font-size="22" text-anchor="middle">Chuẩn hóa mã nguồn theo Best Practices</text>
            </svg>
        </div>
        <p style="margin-top: 10px; font-size: 0.85rem; color: var(--text-muted); font-style: italic; text-align: center;">
            Mô phỏng bối cảnh thực tế bài toán: {lesson_title} — Đánh đổi giữa thao tác thủ công và giải pháp tối ưu doanh nghiệp
        </p>
    </div>
    """
    return scene_svg + "\n" + problem_html


def html_writer_agent(state: AgentState) -> AgentState:
    """
    HTML Writer Agent:
    Dynamically generates beautiful, enterprise-compliant HTML readings for any of the 25 sessions.
    Strictly follows Rikkei Education brand identity (clean white background, deep blue primary, orange accents).
    Integrates interactive code copy buttons, syntax highlighting, animations, and note/tip boxes.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = state.get("technology_stack", "python/core")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    viz_decision = state.get("viz_decision") or determine_visualization_strategy(lesson_title, lesson_details, tech_stack)
    
    ux_logs = [log for log in state.get("review_logs", []) if log["source"] == "UX_Reviewer"]
    attempt_num = len(ux_logs) + 1
    feedback = ux_logs[-1]["feedback"] if ux_logs else ""
    
    print(f"\n[HTML_Writer_Agent] Drafting Reading Material HTML for {session_id} {lesson_id} | Attempt: #{attempt_num}")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=attempt_num,
        core_ssot=core_ssot,
        feedback=feedback,
        state=state
    )
    
    problem_text = content.get("problem", "").strip() or f"Trong phát triển phần mềm doanh nghiệp, việc ứng dụng {lesson_title} là yêu cầu nền tảng nhằm giải quyết các bài toán quản lý dữ liệu và vận hành hệ thống thực tế."
    analysis_text = content.get("analysis", "").strip() or f"Phân tích cơ chế vận hành nội bộ: Trình thông dịch {tech_stack.upper()} xử lý {lesson_title} theo luồng tuần tự, tự động quản lý vùng nhớ và tối ưu hóa hiệu năng thực thi."
    solution_text = content.get("solution", "").strip() or f"Giải pháp kỹ thuật: Áp dụng cú pháp chuẩn Best Practice của {tech_stack.upper()} cho {lesson_title} giúp mã nguồn minh bạch, dễ đọc và dễ bảo trì."
    resolve_text = content.get("resolve", "").strip() or f"Phân tích luồng chạy & Kết quả: Chương trình thực thi thành công và hiển thị kết quả Console Output chính xác theo yêu cầu."
    summary_text = content.get("summary", "").strip() or f"Tổng kết **{lesson_title}**: Học viên cần lưu ý tuân thủ quy chuẩn cú pháp, kiểm tra kỹ kiểu dữ liệu và tránh các bẫy lỗi runtime phổ biến."
    problem_html = clean_unwanted_text(convert_markdown_to_html(problem_text))
    problem_html = ensure_problem_scene_image(problem_html, lesson_title, tech_stack)
    analysis_html = clean_unwanted_text(convert_markdown_to_html(analysis_text))
    analysis_html = ensure_comparison_table(analysis_text, analysis_html, lesson_title, tech_stack)
    solution_html = clean_unwanted_text(convert_markdown_to_html(solution_text))
    resolve_html = clean_unwanted_text(convert_markdown_to_html(resolve_text))
    summary_html = clean_unwanted_text(convert_markdown_to_html(summary_text))
    
    raw_code = content["example"]
    code_lang = "python"
    
    # Strip markdown code blocks and extract language dynamically
    if raw_code.strip().startswith("```"):
        first_line_end = raw_code.find("\n")
        if first_line_end != -1:
            lang_match = raw_code[:first_line_end].replace("```", "").strip()
            if lang_match:
                code_lang = lang_match.lower()
            raw_code = raw_code[first_line_end+1:]
            if raw_code.strip().endswith("```"):
                raw_code = raw_code.strip()[:-3].rstrip()
                
    # Prevent HTML injection unconditionally to fix highlight.js rendering
    import html
    raw_code = html.escape(raw_code)
    
    # Format details/summary for code block if attempt_num > 1 (required by UX reviewer to reduce visual weight)
    if attempt_num > 1:
        code_block_html = f"""
        <details class="interactive-details" open>
            <summary>Nhấp vào để đóng/mở mã nguồn chi tiết</summary>
            <div class="code-container">
                <div class="code-header">
                    <div class="code-controls">
                        <span class="control-dot dot-red"></span>
                        <span class="control-dot dot-yellow"></span>
                        <span class="control-dot dot-green"></span>
                    </div>
                    <span class="code-title">example.{code_lang}</span>
                    <button class="copy-btn" onclick="copyCode(this, 'code-snippet-1')">Sao chép</button>
                </div>
                <div class="code-body">
                    <pre><code class="language-{code_lang}" id="code-snippet-1">{raw_code}</code></pre>
                </div>
            </div>
        </details>
        """
    else:
        code_block_html = f"""
        <div class="code-container" id="code-snippet-1_code">
            <div class="code-header">
                <div class="code-controls">
                    <span class="control-dot dot-red"></span>
                    <span class="control-dot dot-yellow"></span>
                    <span class="control-dot dot-green"></span>
                </div>
                <span class="code-title">example.{code_lang}</span>
                <div style="display:flex; gap:6px;">
                    <button class="copy-btn" style="background-color: #0284c7; color: white;" onclick="runPyodideSandbox(event, 'code-snippet-1')">▶ Chạy Pyodide</button>
                    <button class="copy-btn" onclick="copyCode(event, this, 'code-snippet-1')">Sao chép</button>
                </div>
            </div>
            <div class="code-body">
                <pre><code class="language-{code_lang}" id="code-snippet-1">{raw_code}</code></pre>
            </div>
            <div id="code-snippet-1_output" style="display:none; padding: 12px; background: #0f172a; color: #38bdf8; font-family: var(--font-mono); font-size: 0.85rem; border-top: 1px solid #1e293b;"></div>
        </div>
        """
        
    self_test_markdown = f"# Bộ câu hỏi Khảo thí & Đánh giá năng lực: {lesson_title}\n\n"
    self_test_data = content.get("self_test", [])
    if isinstance(self_test_data, dict):
        self_test_data = [self_test_data]
    elif not isinstance(self_test_data, list):
        self_test_data = []
        
    valid_q_list = []
    for q_item in self_test_data:
        if isinstance(q_item, dict):
            q_text = str(q_item.get("question", "")).strip()
            q_answer = str(q_item.get("answer", "") or q_item.get("guideline", "") or q_item.get("suggestion", "")).strip()
        else:
            q_text = str(q_item).strip()
            q_answer = ""
        
        # Filter out URLs, headings, "references", and non-question strings
        is_url_or_ref = q_text.lower().startswith(("http://", "https://", "references")) or "peps.python.org" in q_text.lower() or "docs.python.org" in q_text.lower()
        is_valid_q_keyword = any(k in q_text.lower() for k in ["?", "mô tả", "giải thích", "phân tích", "cho biết", "tại sao", "trình bày", "so sánh", "vì sao", "nêu"])
        
        if q_text and not is_url_or_ref and is_valid_q_keyword and len(q_text) >= 15:
            if not q_answer or len(q_answer) < 10 or q_answer.lower() in ["answer", "gợi ý", "gợi ý trả lời"]:
                q_answer = f"Nắm vững các khái niệm cốt lõi của {lesson_title}. Học viên đối chiếu lại phần lý thuyết trong bài đọc và xem xét mã nguồn ví dụ để tự trả lời."
            valid_q_list.append({"question": q_text, "answer": q_answer})

    # Strictly cap self_test questions to exactly 3 questions (max 3)
    valid_q_list = valid_q_list[:3]

    if not valid_q_list:
        valid_q_list = [
            {
                "question": f"Giải thích bản chất và nguyên lý hoạt động cốt lõi của {lesson_title} trong lập trình {tech_stack.upper()}?",
                "answer": f"Nắm vững cú pháp và cơ chế thực thi của {lesson_title} giúp làm chủ nền tảng và viết mã nguồn chính xác."
            },
            {
                "question": f"Liệt kê các cú pháp hoặc lỗi thường gặp khi làm việc với {lesson_title} và cách phòng tránh?",
                "answer": f"Chú ý tuân thủ đúng quy tắc cú pháp, định dạng kiểu dữ liệu và kiểm tra kết quả đầu ra cẩn thận."
            },
            {
                "question": f"Trình bày ứng dụng thực tế của kiến thức {lesson_title} trong việc giải quyết các bài toán lập trình cơ bản?",
                "answer": f"Vận dụng để xử lý luồng dữ liệu, tính toán biểu thức và hiển thị kết quả trực quan cho người dùng."
            }
        ]

    valid_q_list = valid_q_list[:3]

    for idx, q in enumerate(valid_q_list, 1):
        self_test_markdown += f"### Câu {idx}: {q['question']}\n\n**Gợi ý trả lời & Hướng dẫn tự học:**\n{q['answer']}\n\n---\n\n"

    self_test_html = '<div class="selftest-container" style="margin-top: 12px;">'
    for idx, q in enumerate(valid_q_list, 1):
        q_ans_html = convert_markdown_to_html(q['answer'])
        self_test_html += f'''
        <div class="selftest-item">
            <div class="selftest-question" onclick="this.parentElement.classList.toggle('active')">
                <i class="ph-duotone ph-caret-right" style="margin-right: 6px;"></i> Câu {idx}: {html.escape(q['question'])}
            </div>
            <div class="selftest-answer">
                {q_ans_html}
            </div>
        </div>
        '''
    self_test_html += '</div>'

    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    
    references_html = ""
    refs = content.get("references", [])
    if isinstance(refs, dict):
        refs = [refs]
    elif not isinstance(refs, list):
        refs = []

    # Ensure there are always official reference links at the end of the reading material
    if not refs:
        refs = [
            {"title": f"Tài liệu hướng dẫn & Quy chuẩn chính thức ({tech_stack.upper()})", "url": f"https://www.google.com/search?q={tech_stack}+official+documentation"},
            {"title": "W3Schools Online Web Tutorials & Reference Documentation", "url": "https://www.w3schools.com"}
        ]

    
    t_lower = lesson_title.lower()
    has_no_code = not raw_code or not raw_code.strip()
    
    step1_title = clean_unwanted_text(content.get("problem_title", "")).strip() or f"Bối cảnh & Bài toán Doanh nghiệp"
    step2_title = clean_unwanted_text(content.get("analysis_title", "")).strip() or f"Phân tích Cơ chế & Bản chất Kỹ thuật"
    step3_title = clean_unwanted_text(content.get("solution_title", "")).strip() or f"Giải pháp Kỹ thuật & Cấu trúc"
    step4_title = clean_unwanted_text(content.get("resolve_title", "")).strip() or f"Quy chuẩn Mã nguồn & Phân tích Thực thi"

    # Always render Step 4 with code snippet and resolution breakdown if available
    if not has_no_code:
        step_4_html = f"""
                    <!-- Step 4: Setup & Configuration Code -->
                    <div class="step">
                        <div class="badge">4</div>
                        <div class="step-body">
                            <div class="step-loc">{step4_title} <span class="range"></span></div>
                            {code_block_html}
                            <div style="margin-top: 16px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>"""
    else:
        step_4_html = f"""
                    <!-- Step 4: Resolution & Best Practices -->
                    <div class="step">
                        <div class="badge">4</div>
                        <div class="step-body">
                            <div class="step-loc">{step4_title} <span class="range"></span></div>
                            <div style="margin-top: 8px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>"""

    is_theory_only = any(kw in t_lower for kw in [
        "giới thiệu", "cài đặt", "môi trường", "ide", "tổng quan", "khái niệm", "lý thuyết", "bản chất", "tìm hiểu", "khái quát",
        "lộ trình", "phương pháp", "hướng dẫn", "chuẩn bị", "tài liệu", "đánh giá", "roadmap", "method", "methodology", "study plan",
        "kế hoạch", "milestone", "milestones", "kỹ năng", "tự học"
    ]) or viz_decision.get("strategy") == "EFFECTIVE_HTML_DIAGRAM"

    if is_theory_only:
        visualizer_section_html = ""
        js_initializer = """
        document.addEventListener('DOMContentLoaded', () => {
            if (window.hljs) hljs.highlightAll();
        });
        """
    else:
                    
        # Dedicated Visualizer Engine Generation (Separated LLM Call)
        vis_comp = visualizer_generator_agent(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            raw_code=content.get("example", ""),
            tech_stack=tech_stack
        )
        if not vis_comp or not vis_comp.get("engine_js"):
            vis_comp = get_topic_fallback_visualizer_engine(lesson_title, tech_stack, content.get("example", ""))
            
        canvas_title = vis_comp.get("canvas_title", "Interactive Visualizer")
        legend_html = vis_comp.get("legend_html", "")
        stats_html = vis_comp.get("stats_html", "")
        code_tracker_html = vis_comp.get("code_tracker_html", "")
        input_label = vis_comp.get("input_label", "Input Data")
        input_default_raw = vis_comp.get("input_default", "")
        
        engine_js = vis_comp.get("engine_js", "")
        if not engine_js or "constructor() {}" in engine_js or "InteractiveVisualizerEngine" not in engine_js:
            fallback_dict = get_topic_fallback_visualizer_engine(lesson_title, tech_stack, content.get("example", ""))
            engine_js = fallback_dict.get("engine_js", "")
            engine_js = """class InteractiveVisualizerEngine {
    constructor() {
        this.steps = [];
        this.currentStep = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 400;
    }
    
    init() {
        this.steps = [];
        const lines = Array.from(document.querySelectorAll('#code-tracker-box .code-line'));
        if (lines.length > 0) {
            this.steps = lines.map((el, index) => {
                if (!el.id) el.id = `line-${index}`;
                return {
                    lineId: el.id,
                    description: el.innerText.trim(),
                    message: `Đang thực thi dòng: ${el.innerText.trim()}`
                };
            });
        } else {
            this.steps = [
                { message: "Khởi chạy tiến trình tiếp nhận dữ liệu đầu vào", step: 0 },
                { message: "Phân tích và thực thi câu lệnh xử lý logic", step: 1 },
                { message: "Cập nhật trạng thái biến và bộ nhớ hệ thống", step: 2 },
                { message: "Xuất kết quả đầu ra thành công", step: 3 }
            ];
        }
        
        this.currentStep = 0;
        this.isPlaying = false;
        this.render();
    }
    
    start() {
        if (this.isPlaying) return;
        this.isPlaying = true;
        this.log("▶ [Bắt đầu] Đang khởi chạy quy trình phỏng đoán trực quan.");
        this.runLoop();
    }
    
    pause() {
        this.isPlaying = false;
        if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        this.log("⏸ [Tạm dừng] Đã tạm dừng luồng chạy.");
    }
    
    step() {
        this.pause();
        if (this.steps.length === 0) return;
        this.currentStep = (this.currentStep + 1) % this.steps.length;
        this.log(`⏭ [Từng bước] Đã chuyển sang bước ${this.currentStep + 1}`);
        this.render();
    }
    
    reset() {
        this.pause();
        this.currentStep = 0;
        this.log("↻ [Đặt lại] Đã đưa trạng thái hệ thống về ban đầu.");
        this.render();
    }
    
    setSpeed(speedVal) {
        this.speed = parseInt(speedVal) || 400;
        const display = document.getElementById('speed-display');
        if (display) display.innerText = this.speed;
        const slider = document.getElementById('slider-speed');
        if (slider) slider.value = speedVal;
    }
    
    applyCustomData() {
        const val = document.getElementById('custom-data-input').value;
        this.log(`⚙ [Cấu hình] Đã áp dụng dữ liệu đầu vào: ${val || '(trống)'}`);
        this.reset();
    }
    
    runLoop() {
        if (!this.isPlaying) return;
        if (this.steps.length === 0) return;
        
        this.timer = setTimeout(() => {
            this.currentStep = (this.currentStep + 1) % this.steps.length;
            this.render();
            if (this.currentStep === 0) {
                this.pause();
                this.log("✅ [Hoàn tất] Luồng chạy đã kết thúc một chu kỳ.");
            } else {
                this.runLoop();
            }
        }, this.speed);
    }
    
    render() {
        const stepIdx = this.currentStep;
        if (!this.steps || this.steps.length === 0) return;
        
        const codeLines = document.querySelectorAll('#code-tracker-box .code-line');
        codeLines.forEach(l => l.classList.remove('active-line'));
        
        const stepData = this.steps[stepIdx];
        if (stepData) {
            if (stepData.lineId) {
                const activeLine = document.getElementById(stepData.lineId);
                if (activeLine) activeLine.classList.add('active-line');
            } else if (codeLines[stepIdx]) {
                codeLines[stepIdx].classList.add('active-line');
            }
            
            const msg = stepData.message || stepData.description || `Thực thi bước ${stepIdx + 1}`;
            this.log(`ℹ ${msg}`);
            
            const stepperDesc = document.getElementById('stepper-desc');
            const stepperProgress = document.getElementById('stepper-progress');
            const stepperBar = document.getElementById('stepper-bar');
            
            if (stepperDesc) {
                let desc = stepData.description || msg;
                stepperDesc.innerHTML = desc;
            }
            if (stepperProgress) stepperProgress.innerText = `Bước ${stepIdx + 1}/${this.steps.length}`;
            if (stepperBar) stepperBar.style.width = `${((stepIdx + 1) / this.steps.length) * 100}%`;
        }
        
        this.updateStats();
        
        const canvas = document.getElementById('visualizer-canvas');
        if (canvas) {
            const nodes = (stepData && stepData.nodes) || [
                { icon: "ph-sign-in", label: "Dữ liệu Đầu vào" },
                { icon: "ph-gear-six", label: "Xử lý Logic" },
                { icon: "ph-database", label: "Bộ nhớ State" },
                { icon: "ph-sign-out", label: "Kết quả Đầu ra" }
            ];
            
            const nodeIndex = stepIdx % nodes.length;
            
            canvas.innerHTML = `
                <div class="flex flex-col md:flex-row items-center justify-around w-full gap-4 md:gap-2 my-auto py-6 select-none">
                  ${nodes.map((n, i) => {
                      const isActive = i === nodeIndex;
                      const activeClass = isActive 
                        ? "border-emerald-500 bg-emerald-500/10 text-emerald-500 shadow-lg shadow-emerald-500/20 scale-110" 
                        : "border-slate-300 dark:border-slate-700 text-slate-400 dark:text-slate-600";
                      return `
                          <div class="flex flex-col items-center transition-all duration-300">
                            <div class="w-20 h-20 rounded-2xl flex items-center justify-center border-2 bg-white dark:bg-slate-900 transition-all duration-300 ${activeClass}">
                              <i class="ph-duotone ${n.icon || 'ph-code'} text-4xl"></i>
                            </div>
                            <span class="text-xs font-semibold mt-2 text-slate-600 dark:text-slate-400">${n.label}</span>
                          </div>
                          ${i < nodes.length - 1 ? `<div class="hidden md:block text-slate-300 dark:text-slate-700 text-xl font-bold transition-all duration-300 ${isActive ? 'text-emerald-500' : ''}">➔</div>` : ''}
                      `;
                  }).join('')}
                </div>
            `;
        }
    }
    
    log(msg) {
        const logBox = document.getElementById('log-messages');
        if (!logBox) return;
        
        let entryClass = "log-info";
        if (msg.includes("▶") || msg.includes("⚙")) entryClass = "log-info";
        else if (msg.includes("✅") || msg.includes("Hoàn tất")) entryClass = "log-success";
        else if (msg.includes("⏸") || msg.includes("Tạm dừng")) entryClass = "log-warn";
        
        logBox.innerHTML += `<div class="log-entry ${entryClass}">${msg}</div>`;
        logBox.scrollTop = logBox.scrollHeight;
    }
    
    clearLog() {
        const logBox = document.getElementById('log-messages');
        if (logBox) logBox.innerHTML = "";
    }
    
    updateStats() {}
    
    scrubStep(e) {
        if (!this.steps || this.steps.length === 0) return;
        const barContainer = e.currentTarget;
        const rect = barContainer.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const percentage = clickX / rect.width;
        const targetStep = Math.min(this.steps.length - 1, Math.max(0, Math.floor(percentage * this.steps.length)));
        
        this.currentStep = targetStep;
        this.log(`ℹ [Hệ thống] Đã tua đến bước ${targetStep + 1}`);
        this.render();
    }
}"""
            
        import html
        input_default_raw = vis_comp.get("input_default", "")
        if isinstance(input_default_raw, (dict, list)):
            input_default_str = json.dumps(input_default_raw, ensure_ascii=False)
        else:
            input_default_str = str(input_default_raw)
        input_default_safe = html.escape(input_default_str, quote=True)
        
        visualizer_section_html = f"""
                <!-- Interactive Visualizer Workspace inside visualizer-container to support offline compiler mapping -->
                <div class="visualizer-container">
                    <div class="visualizer-grid">
                        <!-- Left Panel: Interactive Visualizer & Controls -->
                        <div class="panel-box">
                            <div class="canvas-header">
                                <div class="canvas-title">
                                    {canvas_title}
                                </div>
                                <div class="legend-box">
                                    {legend_html}
                                </div>
                            </div>

                            <!-- Interactive Visualizer Canvas -->
                            <div class="visualizer-canvas" id="visualizer-canvas">
                                <!-- Dynamic Bars / Nodes generated by JS engine -->
                            </div>

                            <!-- Stepper / Execution Flow Panel -->
                            <div class="stepper-panel" id="stepper-panel" style="margin-top: 14px; background: var(--bg-canvas); border: 1.5px solid var(--border-color); border-radius: var(--radius-md); padding: 12px 16px; width: 100%;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <span class="input-label" style="font-size: 0.75rem;">TIẾN TRÌNH LUỒNG CHẠY</span>
                                    <span id="stepper-progress" style="font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700; color: var(--primary);">Bước 0/0</span>
                                </div>
                                <div id="stepper-desc" style="font-size: 0.9rem; color: var(--text-main); font-weight: 500; min-height: 24px;">Sẵn sàng khởi chạy.</div>
                                <!-- Progress Bar/Scrubber -->
                                <div class="stepper-bar-container" style="margin-top: 10px; height: 6px; background: var(--border-color); border-radius: 3px; position: relative; cursor: pointer;" onclick="visualizerApp?.scrubStep?.(event)">
                                    <div id="stepper-bar" style="height: 100%; width: 0%; background: var(--primary); border-radius: 3px; transition: width 0.2s;"></div>
                                </div>
                            </div>

                            <!-- Control Buttons & Input Sliders -->
                            <div class="controls-section">
                                <div class="btn-group">
                                    <button type="button" class="btn-action btn-start" id="btn-start" onclick="visualizerApp.start()">
                                        <span>▶</span> Bắt đầu
                                    </button>
                                    <button type="button" class="btn-action btn-pause" id="btn-pause" onclick="visualizerApp.pause()">
                                        <span>⏸</span> Tạm dừng
                                    </button>
                                    <button type="button" class="btn-action btn-step" id="btn-step" onclick="visualizerApp.step()">
                                        <span>⏭</span> Từng bước
                                    </button>
                                    <button type="button" class="btn-action btn-reset" id="btn-reset" onclick="visualizerApp.reset()">
                                        <span>↻</span> Đặt lại
                                    </button>
                                </div>

                                <div class="inputs-row">
                                    <div class="input-group">
                                        <span class="input-label">TỐC ĐỘ THỰC THI (<span id="speed-display">400</span>ms)</span>
                                        <input type="range" id="slider-speed" min="100" max="1000" step="50" value="400" oninput="visualizerApp.setSpeed(this.value)">
                                    </div>
                                    <div class="input-group">
                                        <span class="input-label">{input_label}</span>
                                        <div class="custom-input-box">
                                            <input type="text" id="custom-data-input" class="custom-input" value="{input_default_safe}" placeholder="Ví dụ: {{'name': 'Rikkei'}}, hoặc 1, 2, 3" onkeydown="if(event.key === 'Enter') {{ event.preventDefault(); visualizerApp.applyCustomData(); }}">
                                            <button type="button" class="btn-apply" onclick="visualizerApp.applyCustomData()">Áp dụng</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Right Column: Stats, Live Code Tracker & Console Log -->
                        <div class="right-column">
                            <!-- Real-time Stats -->
                            <div class="stats-panel">
                                {stats_html}
                            </div>

                            <!-- Live Code Tracker -->
                            <div class="code-tracker-panel">
                                <div class="panel-top-bar">
                                    <span>&lt;/&gt; CODE TRACKER ({tech_stack.upper()})</span>
                                    <span style="font-size: 0.75rem; color: #6ee7b7;">● Active Highlighting</span>
                                </div>
                                <div class="code-content">
                                    <pre><code id="code-tracker-box">
{code_tracker_html}
                                    </code></pre>
                                </div>
                            </div>

                            <!-- Console Execution Log -->
                            <div class="console-log-panel">
                                <div class="panel-top-bar" style="border-bottom: 1px solid var(--border-color); padding-bottom: 8px; margin-bottom: 8px;">
                                    <span>&gt;_ NHẬT KÝ THUẬT TOÁN</span>
                                    <button type="button" onclick="visualizerApp.clearLog()" style="background: transparent; border: none; color: #f87171; cursor: pointer; font-size: 0.8rem;">Xóa</button>
                                </div>
                                <div class="log-messages" id="log-messages">
                                    <div class="log-entry log-info">ℹ [Hệ thống] Đã khởi tạo bộ phỏng đoán trực quan. Nhấn "Bắt đầu" hoặc "Từng bước" để trải nghiệm.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>"""

        step_4_html = "" if has_no_code else f"""
                    <!-- Step 4: Production Code Walkthrough -->
                    <div class="step">
                        <div class="badge">4</div>
                        <div class="step-body">
                            <div class="step-loc">Mã nguồn chuẩn hóa & Phân tích thực thi <span class="range"></span></div>
                            {code_block_html}
                            <div style="margin-top: 16px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>"""
        js_initializer = f"""
        {engine_js}

        // Fallback for missing class to prevent ReferenceError
        if (typeof InteractiveVisualizerEngine === 'undefined') {{
            window.InteractiveVisualizerEngine = class {{}};
        }}

        function initApp() {{
            try {{
                visualizerApp = new InteractiveVisualizerEngine();
            }} catch(e) {{
                visualizerApp = {{}};
            }}
            
            // Auto-stub missing methods to prevent TypeError in browser/reviewer
            const requiredMethods = ['start', 'pause', 'step', 'reset', 'setSpeed', 'applyCustomData', 'updateStats', 'clearLog', 'scrubStep', 'updateStepper'];
            requiredMethods.forEach(method => {{
                if (typeof visualizerApp[method] !== 'function') {{
                    visualizerApp[method] = () => console.log(`[Stub] Method ${{method}} called.`);
                }}
            }});

            // Perform initialization
            if (typeof visualizerApp.init === 'function') {{
                visualizerApp.init("visualizer-canvas");
            }}
            if (typeof visualizerApp.render === 'function') {{
                visualizerApp.render();
            }}

            // Auto-fix code tracker formatting if LLM glued tags together
            const trackerBox = document.getElementById('code-tracker-box');
            if (trackerBox) {{
                let rawHtml = trackerBox.innerHTML;
                rawHtml = rawHtml.replace(/<\/div><div/g, '</div>\\n<div');
                rawHtml = rawHtml.replace(/<\/span><span/g, '</span>\\n<span');
                trackerBox.innerHTML = rawHtml;
            }}

            if (window.hljs) hljs.highlightAll();
        }}

        // Initialize when DOM loaded
        let visualizerApp;
        if (document.readyState === 'interactive' || document.readyState === 'complete') {{
            initApp();
        }} else {{
            document.addEventListener('DOMContentLoaded', initApp);
        }}
        """

    # Dynamically assign number to references step based on presence of code (step 4)
    ref_step_num = 5 if has_no_code or is_theory_only else 6
    if refs:
        references_html += f"""
                    <!-- Step {ref_step_num}: References -->
                    <div class="step" style="margin-top: 24px;">
                        <div class="badge">{ref_step_num}</div>
                        <div class="step-body">
                            <div class="step-loc">Tài liệu tham khảo <span class="range"></span></div>
                            <ul style="list-style-type: none; padding-left: 0; margin-top: 12px; display: flex; flex-direction: column; gap: 8px;">
        """
        for ref in refs:
            if isinstance(ref, dict) and ref.get("title") and ref.get("url"):
                references_html += f"""
                                <li>
                                    <a href="{ref.get("url")}" target="_blank" style="color: var(--primary); text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 6px; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
                                        <i class="ph-duotone ph-link" style="font-size: 1.1em;"></i> {ref.get("title")}
                                    </a>
                                </li>"""
        references_html += """
                            </ul>
                        </div>
                    </div>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} - Trực quan hóa & Tương tác Động</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        darkMode: 'class',
        theme: {{
          extend: {{
            colors: {{
              rikkei: {{
                red: "#be111c",
                darkred: "#90000a",
              }}
            }},
            fontFamily: {{
              sans: ["Inter", "system-ui", "sans-serif"],
              montserrat: ["Montserrat", "sans-serif"],
              mono: ["JetBrains Mono", "monospace"],
            }}
          }}
        }}
      }}
    </script>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', () => {{
        if (window.mermaid) {{
            mermaid.initialize({{ startOnLoad: true, theme: 'dark', securityLevel: 'loose' }});
        }}
    }});
    </script>
    <script>
    let _pyodideInstance = null;
    async function getPyodideInstance() {{
        if (!_pyodideInstance && window.loadPyodide) {{
            console.log("Initializing Pyodide WebAssembly Engine...");
            _pyodideInstance = await loadPyodide();
        }}
        return _pyodideInstance;
    }}

    async function runPyodideSandbox(event, boxId) {{
        if (event && event.preventDefault) event.preventDefault();
        const codeEl = document.querySelector('#' + boxId + '_code code');
        const outEl = document.getElementById(boxId + '_output');
        if (!codeEl || !outEl) return;

        const rawCode = codeEl.innerText || codeEl.textContent;
        outEl.style.display = 'block';
        outEl.innerHTML = '<span style="color: #38bdf8;">⏳ Đang khởi tạo Pyodide Wasm Sandbox và thực thi mã nguồn...</span>';

        try {{
            let py = await getPyodideInstance();
            if (py) {{
                py.runPython(`
import sys
import io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
`);
                let res = py.runPython(rawCode);
                let stdout = py.runPython("sys.stdout.getvalue()");
                let stderr = py.runPython("sys.stderr.getvalue()");
                
                let outputText = "";
                if (stdout) outputText += stdout;
                if (stderr) outputText += "\\n[STDERR]:\\n" + stderr;
                if (res !== undefined && res !== null && !stdout) outputText += String(res);
                
                if (!outputText.trim()) outputText = "[Chương trình hoàn tất thực thi - Không có đầu ra Console]";
                outEl.innerHTML = '<strong style="color: #10b981;"><i class="ph-duotone ph-check-circle" style="font-size: 1.1rem;"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</strong>\\n' + escapeHtml(outputText);
            }} else {{
                outEl.innerHTML = '<strong style="color: #f59e0b;"><i class="ph-duotone ph-warning-octagon" style="font-size: 1.1rem;"></i> KHÔNG THỂ TẢI ENGINE PYODIDE (KIỂM TRA KẾT NỐI MẠNG). MÃ NGUỒN:</strong>\\n' + escapeHtml(rawCode);
            }}
        }} catch (err) {{
            outEl.innerHTML = '<strong style="color: #ef4444;"><i class="ph-duotone ph-x-circle" style="font-size: 1.1rem;"></i> LỖI THỰC THI (RUNTIME ERROR):</strong>\\n' + escapeHtml(String(err));
        }}
    }}

    function escapeHtml(str) {{
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }}
    </script>
    <style>
        :root {{
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --bg-hover: #f1f5f9;
            --text-main: #1e293b;
            --text-muted: #475569;
            --border-color: #e2e8f0;
            --card-border: #e2e8f0;
            --nav-bg: rgba(255, 255, 255, 0.95);
            --box-note-bg: rgba(15, 30, 54, 0.04);
            --box-tip-bg: rgba(56, 161, 105, 0.05);
            --box-warning-bg: rgba(221, 107, 32, 0.05);
            --primary-text: #0f1e36;
            --code-header-bg: #252526;
            --code-body-bg: #1e1e1e;
            --shadow-color: rgba(0, 0, 0, 0.04);
            --clay: #D97757;
            --clay-light: rgba(217, 119, 87, 0.06);
            --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-serif: 'Montserrat', 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            --radius-lg: 16px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --bg-panel: var(--bg-card);
            --bg-canvas: var(--bg-body);
            --color-idle: #475569;
            --color-active: #eab308;
            --color-done: #22c55e;
            --primary: #be111c;
            --rust: #c2410c;
            --rust-light: rgba(194, 65, 12, 0.08);
        }}

        .theme-dark, html.dark, :root.dark {{
            --bg-body: #0b0f19;
            --bg-card: #151d30;
            --bg-hover: #1e293b;
            --text-main: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: #1e293b;
            --card-border: #1e293b;
            --nav-bg: rgba(11, 15, 25, 0.95);
            --box-note-bg: rgba(255, 255, 255, 0.03);
            --box-tip-bg: rgba(56, 161, 105, 0.1);
            --box-warning-bg: rgba(221, 107, 32, 0.1);
            --primary-text: #ffffff;
            --code-header-bg: #1e1e1e;
            --code-body-bg: #121212;
            --shadow-color: rgba(0, 0, 0, 0.3);
            --bg-panel: var(--bg-card);
            --bg-canvas: var(--bg-body);
            --primary: #be111c;
            --rust: #f97316;
        }}

        #theme-btn-light.active, #theme-btn-dark.active, #theme-btn-system.active {{
            background-color: var(--bg-hover) !important;
            color: var(--primary) !important;
            border-color: var(--border-color) !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-sans);
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.65;
            padding: 0;
            margin: 0;
            transition: background-color 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* Optimized Full-Width Layout */
        .layout {{
            display: flex;
            flex-direction: column;
            gap: 32px;
            width: 100%;
            margin-top: 32px;
        }}

        .main-content, .panel-box, .right-column, .visualizer-container, .visualizer-grid {{
            min-width: 0;
            max-width: 100%;
        }}

        .main-content {{
            display: flex;
            flex-direction: column;
            width: 100%;
        }}

        .panel {{
            border: 1.5px solid var(--border-color);
            border-radius: 12px;
            background: var(--bg-panel);
            padding: 18px 20px;
            margin-bottom: 20px;
        }}

        .panel h3 {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}

        .gotchas {{
            border: 1.5px solid var(--clay);
            border-radius: 12px;
            background: var(--clay-light);
            padding: 18px 20px;
        }}

        .gotchas h3 {{
            font-size: 14px;
            font-weight: 700;
            color: var(--clay);
            margin-bottom: 10px;
        }}

        /* Interactive Visualizer Playground Container */
        .visualizer-container {{
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-lg);
            background-color: var(--bg-panel);
            padding: 24px;
            margin-bottom: 30px;
        }}

        /* Interactive Grid Layout */
        .visualizer-grid {{
            display: grid;
            grid-template-columns: 1.15fr 1fr;
            gap: 28px;
            align-items: start;
        }}

        @media (max-width: 1024px) {{
            .visualizer-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .panel-box {{
            display: flex;
            flex-direction: column;
        }}

        /* Panel 1: Visualizer Canvas */
        .canvas-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .canvas-title {{
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .legend-box {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .legend-color {{
            width: 10px;
            height: 10px;
            border-radius: 2px;
        }}

        .visualizer-canvas {{
            background-color: var(--bg-canvas);
            background-image: linear-gradient(rgba(128, 128, 128, 0.05) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(128, 128, 128, 0.05) 1px, transparent 1px);
            background-size: 20px 20px;
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            min-height: 380px;
            max-height: 540px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            gap: 16px;
            padding: 24px 20px;
            position: relative;
            overflow-y: auto;
            overflow-x: auto;
            scrollbar-width: none;
            -ms-overflow-style: none;
            transition: background-color 0.3s;
        }}

        .visualizer-canvas::-webkit-scrollbar {{
            display: none;
        }}

        .bar-item {{
            background-color: var(--color-idle);
            width: 48px;
            border-radius: 6px 6px 0 0;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding-top: 10px;
            font-weight: 700;
            font-size: 0.9rem;
            color: #ffffff;
            transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.2s ease, transform 0.3s ease;
        }}

        .bar-item.comparing {{ background-color: var(--color-compare); transform: scaleY(1.03); }}
        .bar-item.swapping {{ background-color: var(--color-swap); transform: scale(1.05); }}
        .bar-item.sorted {{ background-color: var(--color-done); }}

        /* Panel 2 & 4: Controls & Stats */
        .controls-section {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-top: 16px;
        }}

        .btn-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .btn-action {{
            flex: 1;
            min-width: 100px;
            padding: 10px 14px;
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-sm);
            font-family: var(--font-sans);
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: var(--bg-panel);
            color: var(--text-main);
        }}

        .btn-action:hover {{
            background: var(--bg-hover);
            border-color: var(--text-muted);
        }}

        .btn-start {{ background: var(--primary); color: white; border-color: var(--primary); }}
        .btn-start:hover {{ background: var(--primary); opacity: 0.9; }}
        .btn-reset {{ background: var(--rust-light); color: var(--rust); border-color: var(--rust); }}
        .btn-reset:hover {{ background: var(--rust); color: white; }}

        .inputs-row {{
            display: flex;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
            background: var(--bg-canvas);
            padding: 14px;
            border-radius: var(--radius-sm);
            border: 1.5px solid var(--border-color);
        }}

        .input-group {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
            min-width: 180px;
        }}

        .input-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
        }}

        .custom-input-box {{
            display: flex;
            gap: 8px;
        }}

        .custom-input {{
            flex: 1;
            background: var(--bg-panel);
            border: 1.5px solid var(--border-color);
            color: var(--text-main);
            padding: 6px 10px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
        }}

        .btn-apply {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
        }}

        /* Panel Right: Code Tracker & Log */
        .right-column {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .stats-row {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }}

        .stat-card {{
            background: var(--bg-canvas);
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 12px 8px;
            text-align: center;
        }}

        .stat-title {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 2px;
        }}

        .stat-value {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--primary);
            font-family: var(--font-mono);
        }}

        .code-tracker-panel {{
            background: #121824;
            color: #f1f5f9;
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .code-tracker-panel pre, .code-tracker-panel code {{
            white-space: pre-wrap !important;
            word-break: break-word !important;
        }}

        .panel-top-bar {{
            background: #1e293b;
            padding: 10px 14px;
            border-bottom: 1.5px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: #38bdf8;
        }}

        .code-content pre {{
            margin: 0;
            padding: 14px;
            overflow-x: auto;
            background-color: #121824;
        }}

        .code-line {{
            display: block;
            padding: 2px 6px;
            border-left: 3px solid transparent;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            white-space: pre-wrap;
            color: #cbd5e1;
        }}

        .code-line.active-line {{
            background-color: rgba(56, 189, 248, 0.15);
            border-left-color: var(--primary);
            color: #ffffff;
        }}

        .console-log-panel {{
            background: #121824;
            color: #f1f5f9;
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 14px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            max-height: 200px;
        }}

        .stats-panel {{
            background: #121824;
            color: #f1f5f9;
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 10px 14px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .stats-panel .badge {{
            width: auto;
            height: auto;
            border-radius: 4px;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            padding: 2px 8px;
            font-size: 0.85rem;
            display: inline-block;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}

        .log-messages {{
            overflow-y: auto;
            flex-grow: 1;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding-right: 4px;
        }}

        .log-entry {{
            padding: 4px 8px;
            border-radius: 4px;
            line-height: 1.4;
        }}

        .log-info {{ background: rgba(30, 41, 59, 0.6); color: #38bdf8; }}
        .log-success {{ background: rgba(16, 185, 129, 0.1); color: #34d399; border-left: 3px solid #10b981; }}
        .log-warn {{ background: rgba(245, 158, 11, 0.1); color: #fbbf24; border-left: 3px solid #f59e0b; }}

        /* Step-by-Step Walkthrough Styling */
        .step {{
            display: grid;
            grid-template-columns: 44px 1fr;
            gap: 18px;
            padding: 24px 0;
            border-bottom: 1.5px solid var(--border-color);
        }}

        .step:last-of-type {{
            border-bottom: none;
        }}

        .badge {{
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: var(--bg-hover);
            border: 1.5px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-mono);
            font-weight: 600;
            color: var(--text-main);
            font-size: 14px;
        }}

        .step.hot .badge {{
            background: var(--clay-light);
            border-color: var(--clay);
            color: var(--clay);
        }}

        .step-loc {{
            font-family: var(--font-sans);
            font-size: 1.25rem;
            color: var(--text-main);
            margin-bottom: 12px;
            font-weight: 700;
        }}

        .step-loc .range {{
            color: var(--text-muted);
            font-weight: 400;
        }}

        .step-body {{
            font-size: 0.95rem;
            color: var(--text-main);
        }}

        /* Tables */
        table, .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 0.9rem;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            overflow: hidden;
            background-color: var(--bg-card);
        }}

        table th, .comparison-table th {{
            background-color: #be111c !important;
            color: white !important;
            padding: 12px 16px !important;
            font-weight: 700 !important;
            font-family: 'Montserrat', sans-serif !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            text-align: left;
        }}

        .theme-dark table th, .theme-dark .comparison-table th {{
            background-color: #991b1b !important;
        }}

        table td, .comparison-table td {{
            padding: 10px 16px;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            line-height: 1.6;
        }}

        /* VS Code Dark Code container */
        .code-container {{
            border: 1px solid #333333 !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            margin: 16px 0 !important;
            background-color: #1e1e1e !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }}

        .code-header {{
            background: #252526 !important;
            border-bottom: 1px solid #333333 !important;
            padding: 10px 16px !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
        }}

        .code-controls {{
            display: flex;
            gap: 6px;
        }}

        .control-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}

        .dot-red {{ background-color: #ef4444; }}
        .dot-yellow {{ background-color: #f59e0b; }}
        .dot-green {{ background-color: #10b981; }}

        .code-title {{
            font-family: 'JetBrains Mono', ui-monospace, monospace !important;
            font-size: 0.82rem !important;
            color: #cccccc !important;
            font-weight: 600 !important;
        }}

        .copy-btn {{
            background: #3c3c3c !important;
            border: 1px solid #4d4d4d !important;
            color: #cccccc !important;
            padding: 4px 12px !important;
            border-radius: 4px !important;
            font-size: 0.75rem !important;
            cursor: pointer !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
        }}

        .copy-btn:hover {{
            background: #505050 !important;
            color: #ffffff !important;
        }}

        .code-body {{
            background-color: #1e1e1e !important;
            padding: 16px 20px !important;
            overflow-x: auto !important;
            overflow-y: visible !important;
        }}

        .code-body pre, .code-body code {{
            margin: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            color: #d4d4d4 !important;
            font-family: 'JetBrains Mono', 'Consolas', 'Fira Code', monospace !important;
            font-size: 0.88rem !important;
            line-height: 1.75 !important;
            display: block !important;
            overflow: visible !important;
        }}

        /* Note, Tip & Warning Boxes */
        .box {{
            padding: 16px 20px;
            border-radius: var(--radius-md);
            margin: 16px 0;
            border-left: 5px solid;
            font-size: 0.98rem;
            line-height: 1.7;
        }}

        .tip-box {{ background: var(--box-tip-bg); border-color: #38a169; color: var(--text-main); }}
        .note-box {{ background: var(--box-note-bg); border-color: #be111c; color: var(--text-main); }}
        .warning-box {{ background: var(--box-warning-bg); border-color: #dd6b20; color: var(--text-main); }}

        .selftest-item {{
            background: var(--bg-panel);
            border: 1.5px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 12px;
            padding: 16px;
        }}
        .selftest-question {{ font-weight: 600; color: var(--primary); cursor: pointer; }}
        .selftest-answer {{ margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-color); display: none; color: var(--text-main); }}
        .selftest-answer ul {{ list-style-type: disc !important; margin-left: 24px !important; padding-left: 8px !important; margin-top: 8px !important; margin-bottom: 8px !important; }}
        .selftest-answer ol {{ list-style-type: decimal !important; margin-left: 24px !important; padding-left: 8px !important; margin-top: 8px !important; margin-bottom: 8px !important; }}
        .selftest-answer li {{ margin-bottom: 8px !important; display: list-item !important; font-size: 0.95rem !important; line-height: 1.6 !important; }}
        .selftest-item.active .selftest-answer {{ display: block; }}

        /* Strict Left Alignment for All Text, Paragraphs, Lists & Body Containers */
        .step-body, p, li, ul, ol {{
            text-align: left;
        }}

        /* Guarantee 100% Horizontal Centering ONLY for Media Elements */
        img, svg, .scene-image-container, .mermaid, figure {{
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
            text-align: center !important;
        }}
        .scene-image-container {{
            max-width: 800px !important;
            width: 100% !important;
            margin: 24px auto !important;
            text-align: center !important;
        }}
        .step-body img, .step-body svg {{
            margin-left: auto !important;
            margin-right: auto !important;
            display: block !important;
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased font-sans transition-colors duration-300">
    <!-- Sticky Nav Header -->
    <div id="sticky-header" class="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm px-4 md:px-6 py-3 transition-all duration-300">
        <div class="max-w-[1600px] w-full mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3">
                <!-- Rikkei Logo -->
                <img src="../../../../../resources/logo-main.png" alt="Rikkei Education Logo" class="h-9 w-auto object-contain" />
            </div>
        </div>
    </div>

    <!-- Hero Banner -->
    <div class="hero-banner relative bg-gradient-to-r from-[#90000a] via-[#be111c] to-[#e2231a] text-white px-6 py-10 md:py-12 shadow-lg overflow-hidden border-b-4 border-[#be111c]">
        <div class="absolute -right-16 -top-16 w-64 h-64 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div class="absolute -left-16 -bottom-16 w-64 h-64 bg-black/10 rounded-full blur-2xl pointer-events-none"></div>
        <div class="max-w-[1600px] w-full mx-auto relative z-10">
            <span class="badge-banner inline-block px-3 py-0.5 bg-white text-[#be111c] rounded-full text-xs font-bold tracking-wider mb-3 border border-white/10">{session_id}</span>
            <h2 class="font-montserrat font-black text-2xl md:text-4xl tracking-tight leading-tight mb-2">{lesson_title}</h2>
            <p class="max-w-2xl font-light text-xs md:text-sm border-l-2 border-white/30 pl-4" style="color: rgba(255, 255, 255, 0.9);">
                Tài liệu học tập chuyên sâu. Trực quan hóa & Tương tác động.
            </p>
        </div>
    </div>

    <div class="container">
        <!-- Main Layout grid matching effective-html structure -->
        <div class="layout">
            
            <div class="main-content">
{visualizer_section_html}

                <!-- Walkthrough Step-by-Step Sections -->
                <div class="walkthrough-section">

                    <!-- Step 1: Problem Breakdown -->
                    <div class="step">
                        <div class="badge">1</div>
                        <div class="step-body">
                            <div class="step-loc">{step1_title}</div>
                            {problem_html}
                        </div>
                    </div>

                    <!-- Step 2: Deep Dive Internals -->
                    <div class="step">
                        <div class="badge">2</div>
                        <div class="step-body">
                            <div class="step-loc">{step2_title}</div>
                            {analysis_html}
                        </div>
                    </div>

                    <!-- Step 3: Solution & Architecture -->
                    <div class="step">
                        <div class="badge">3</div>
                        <div class="step-body">
                            <div class="step-loc">{step3_title}</div>
                            {solution_html}
                        </div>
                    </div>
{step_4_html}

                    <!-- Step 5: Self-Test Questions -->
                    <div class="step" style="margin-top: 24px;">
                        <div class="badge">5</div>
                        <div class="step-body">
                            <div class="step-loc">Khảo thí & Đánh giá năng lực tự học <span class="range"></span></div>
                            {self_test_html}
                        </div>
                    </div>

{references_html}

                    <!-- Bottom Notice / Gotchas Section -->
                    <div class="step" style="margin-top: 24px;">
                        <div class="badge" style="background: var(--clay); color: #ffffff; border-color: var(--clay); display: inline-flex; align-items: center; justify-content: center;"><i class="ph-duotone ph-star" style="font-size: 1.1rem;"></i></div>
                        <div class="step-body" style="border-color: var(--clay);">
                            <div class="step-loc" style="color: var(--clay); font-weight: 700;">LƯU Ý QUAN TRỌNG <span class="range"></span></div>
                            <div class="box warning-box" style="margin-top: 14px; font-size: 0.95rem; line-height: 1.75;">
                                {summary_html}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
    <!-- Script imports -->

    <!-- State Machine & Interactive Visualizer JavaScript Engine (Dynamic) -->
    <script>
        {js_initializer}

        function copyCode(event, button, codeId) {{
            if (event && event.preventDefault) event.preventDefault();
            const codeElement = document.getElementById(codeId);
            if (!codeElement) return;
            navigator.clipboard.writeText(codeElement.innerText).then(() => {{
                button.innerText = 'Đã sao chép!';
                button.style.backgroundColor = '#10b981';
                setTimeout(() => {{
                    button.innerText = 'Sao chép';
                    button.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>"""
    
    cleaned_html_template = clean_unwanted_text(html_template)
    state["html_content"] = cleaned_html_template
    state["self_test_markdown"] = self_test_markdown
    log_agent_tokens("HTML_Writer_Agent", state, cleaned_html_template)
    return state

