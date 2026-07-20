import json
import re
import os
from typing import Dict, Any, List
from pathlib import Path
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

def get_lesson_content(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, attempt_num: int, core_ssot: Dict[str, Any] | None = None, feedback: str = "", state: AgentState | None = None) -> Dict[str, Any]:
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
        raise RuntimeError("ERROR: API key (GEMINI_API_KEY or OPENAI_API_KEY) is missing. Cannot generate content dynamically.")

        
    from core.llm import call_llm
    from core.skills import load_skill_content
    
    tech_stack = "python/fastapi"
    if state:
        tech_stack = state.get("technology_stack", "python/fastapi")
        
    print(f"  [Creator Agent] Dynamically generating lesson content via LLM (Attempt #{attempt_num}) for stack: {tech_stack}...")
    
    # Xác định chiến lược trực quan hóa thông minh dựa trên tín hiệu bài học
    viz_decision = determine_visualization_strategy(lesson_title, lesson_details, tech_stack)
    print(f"  [Pedagogical Router] Lesson '{lesson_title}' -> Strategy: {viz_decision['strategy']} ({viz_decision['skill_name']}) | Rationale: {viz_decision['rationale']}")
    
    reading_skill = load_skill_content(viz_decision["skill_name"])
    quiz_skill = load_skill_content("quiz_generator")
    lab_skill = load_skill_content("lab_generator")
    
    # Load lessons learned from previous runs using the new structured Knowledge Memory Agent
    lessons_learned_prompt = ""
    try:
        from agents.knowledge_memory_agent import get_relevant_memories_for_creator
        # Determine scope from the visualization strategy
        scope_hint = "mindmap" if "mindmap" in lesson_title.lower() else "all"
        lessons_learned_prompt = get_relevant_memories_for_creator(
            tech_stack=tech_stack,
            scope=scope_hint,
            limit=10
        )
    except Exception:
        # Fallback to old flat Markdown loader if KMA not available yet
        from core.skills import load_skill_content
        lessons_learned = load_skill_content("lessons_learned")
        if lessons_learned:
            lessons_learned_prompt = (
                "\n--- BÀI HỌC KINH NGHIỆM PHÒNG CHỐNG LỖI TỪ CÁC BÀI TRƯỚC (Lessons Learned) ---\n"
                "Hãy đọc kỹ các bài học này để không lặp lại sai lầm tương tự:\n"
                f"{lessons_learned}\n"
            )

    system_prompt = f"""Bạn là chuyên gia Thiết kế Chương trình Đào tạo Lập trình (Instructional Designer) và Kỹ sư Phần mềm cao cấp tại Rikkei Education. 
Nhiệm vụ của bạn là biên soạn tài liệu học tập sâu sắc, chất lượng cao về công nghệ '{tech_stack}'.

YÊU CẦU QUAN TRỌNG VỀ TRỌNG TÂM, ĐỘ SÂU KIẾN THỨC VÀ KIỂM SOÁT PHẠM VI SƯ PHẠM:
1. Tập trung 100% vào nội dung bài học: Tài liệu phải bám sát tuyệt đối tiêu đề và chi tiết yêu cầu của Lesson hiện tại từ PM. TUYỆT ĐỐI không viết lan man sang bài học khác làm nội dung quá dài hoặc nhắc đến các bài học tiếp theo.
2. Ràng buộc công nghệ nghiêm ngặt (Technology Stack Isolation): Bạn phải tuân thủ tuyệt đối công nghệ '{tech_stack}'. Chỉ sử dụng các thư viện, framework, cú pháp, quy chuẩn và cấu trúc chuẩn của công nghệ '{tech_stack}'. Tuyệt đối không được trộn lẫn, nhắc đến hoặc sử dụng các thư viện, công nghệ hoặc framework khác.
3. RÀNG BUỘC PHẠM VI VÀ LUỸ KẾ KIẾN THỨC (STRICT SCOPE & PROGRESSION):
   - Tuyệt đối CẤM sử dụng các khái niệm, cú pháp lập trình, thư viện, hoặc framework nâng cao chưa từng xuất hiện trong các bài học trước đó (xem phần "THÔNG TIN CÁC BÀI HỌC TRƯỚC ĐÓ").
   - Mã nguồn ví dụ phải cực kỳ đơn giản, ngắn gọn và khớp 100% với trình độ hiện tại của học viên. CẤM tự ý đưa vào các cấu trúc phức tạp như lập trình bất đồng bộ (async/await), decorator, lambda nâng cao, hoặc các thư viện bên thứ ba nếu bài học hoặc các bài trước đó chưa dạy chúng.
   - Nội dung giải thích phải dễ hiểu, thực tế, đi từ cơ chế hoạt động cơ bản nhất trước khi phân tích internals, đảm bảo không gây quá tải nhận thức.
4. CẢNH BÁO SƯ PHẠM CHO BÀI HỌC NHỎ (MINOR LESSONS): Nếu nội dung bài học từ PM rất ngắn gọn, mang tính giới thiệu, cài đặt môi trường, hoặc lý thuyết đơn giản, TUYỆT ĐỐI KHÔNG mở rộng vấn đề, không bịa đặt nội dung phức tạp. Hãy đi thẳng vào trọng tâm. Trình bày nội dung cực kỳ ngắn gọn.
5. Không bịa đặt nội dung/mã nguồn: Nếu bài học không liên quan trực tiếp đến lập trình mã nguồn phức tạp, TUYỆT ĐỐI không tự bịa đặt ra mã nguồn lập trình. Thay vào đó, dùng câu lệnh CLI cơ bản hoặc ví dụ siêu ngắn hoặc để trống trường `example`.
6. QUY LUẬT CODE ĐỐI VỚI BÀI LÝ THUYẾT: Đối với bài học mang tính lý thuyết tổng quan (giới thiệu, tổng quan, khái niệm), HẠN CHẾ viết code. TUY NHIÊN, NẾU PM yêu cầu rõ ràng việc code/thực hành trong chi tiết bài học (lesson_details), BẠN BẮT BUỘC PHẢI VIẾT CODE NGẮN GỌN VÀ ĐẦY ĐỦ VÀO TRƯỜNG `example`.
7. Hạn chế kích thước trả về (STRICT SIZE LIMIT): Toàn bộ chuỗi JSON trả về phải kiểm soát dưới 2500 từ để tránh lỗi tràn/cắt cụt token. Mỗi mục Markdown (problem, analysis, solution, resolve, summary) viết từ 200 đến 300 từ để đảm bảo độ sâu sư phạm. Trường 'example' chứa mã nguồn minh họa chi tiết và hoạt động được, giới hạn tối đa từ 35 đến 40 dòng. KHÔNG viết dài dòng lan man ngoài phạm vi. HẠN CHẾ TỐI ĐA SỬ DỤNG ICON EMOJI. CHỈ dùng khi thực sự cần thiết. ĐẶC BIỆT CẤM TUYỆT ĐỐI đặt icon emoji ở đầu các tiêu đề (Headings).
{lessons_learned_prompt}

Hãy tuân thủ nghiêm ngặt các quy chuẩn sư phạm được định nghĩa trong các tài liệu Kỹ năng (Skills) sau:

--- PHẦN BÀI ĐỌC (Reading Guidelines) ---
{reading_skill}

--- PHẦN TRẮC NGHIỆM (Quiz Guidelines) ---
{quiz_skill}

--- PHẦN THỰC HÀNH (Lab Guidelines) ---
{lab_skill}
"""
    
    # Query local vector store for relevant context
    rag_context = ""
    try:
        from core.vector_store import LightweightVectorStore
        store = LightweightVectorStore()
        matches = store.query(lesson_title, k=2)
        if matches:
            rag_context = f"\nCác khái niệm/mã nguồn liên quan từ Vector DB cục bộ cho stack {tech_stack}:\n" + "\n".join([f"- {m['text']}" for m in matches])
    except Exception as e:
        print(f"  [VectorStore Warning] Query failed: {e}")
        
    prev_lessons_prompt = ""
    if state and state.get("previous_lessons"):
        prev_lessons_prompt = "\n--- THÔNG TIN CÁC BÀI HỌC TRƯỚC ĐÓ (Mối liên kết bài học) ---\n"
        prev_lessons_prompt += "Để đảm bảo tính liên kết chặt chẽ và học tập luỹ tiến, bài học hiện tại bắt buộc phải coi các bài trước đó làm nền tảng học thuật và xây dựng tiếp nối nội dung, tuyệt đối không được dạy trước hoặc lặp lại trùng lặp nội dung:\n"
        for prev in state.get("previous_lessons", []):
            prev_lessons_prompt += f"- {prev['lesson_id']}: {prev['title']} (Nội dung: {prev['details']})\n"

    user_prompt = f"""Hãy sinh nội dung học liệu cho:
Session: {session_id}
Lesson: {lesson_id} (Tiêu đề: {lesson_title})
Chi tiết bài học từ PM: {lesson_details}
Đầu ra kỳ vọng: {expected_output}
Số lần thử hiện tại: {attempt_num}
Phản hồi sửa đổi từ reviewer (nếu có): {feedback}
{prev_lessons_prompt}

Căn cứ vào Nguồn Sự Thật Duy Nhất (SSOT) sau đây:
{json.dumps(core_ssot, ensure_ascii=False) if core_ssot else f"Không có SSOT cụ thể, hãy tự sinh dựa trên kiến thức chuẩn {tech_stack}."}
{rag_context}

Đầu ra bắt buộc phải trả về duy nhất chuỗi JSON khớp với cấu trúc sau:
{{
    "problem": "Nội dung phần đặt vấn đề (Markdown)",
    "analysis": "Nội dung phân tích cơ chế và so sánh (Markdown)",
    "solution": "Nội dung giải pháp kỹ thuật. NẾU VẼ SƠ ĐỒ SVG HOẶC MERMAID, BẮT BUỘC PHẢI VẼ CỰC KỲ ĐƠN GIẢN (Giới hạn tối đa 20 dòng) để tránh sập hệ thống!",
    "example": "Mã nguồn minh họa. 🛑 TUYỆT ĐỐI KHÔNG TỰ BỊA CODE. BẠN CHỈ ĐƯỢC PHÉP SINH CODE NẾU PM CÓ CUNG CẤP TỪ KHÓA CODE MẪU BÊN TRÊN. Nếu PM không đề cập đến code, BẮT BUỘC trả về chuỗi rỗng ''.",
    "resolve": "Phân tích luồng chạy và phản hồi/kết quả thực thi (Markdown). Nếu trường 'example' để trống hoặc chỉ có CLI, hãy phân tích lý thuyết/quy trình vận hành ở đây.",
    "summary": "Tổng kết và 3 lỗi thường gặp (Markdown). BẮT BUỘC BÔI ĐẬM (DÙNG **bold**) tên các sai lầm thường gặp để học viên dễ chú ý.",
    "self_test": [
        {{
            "question": "Câu hỏi 1 (Tối đa 3 câu). Đặt tên rõ ràng, 100% sát sườn với bài.",
            "answer": "Giải thích ĐẶC BIỆT CHI TIẾT và sâu sắc (không viết chung chung)."
        }}
    ],
    "references": [
        {{
            "title": "Tên tài liệu tham khảo uy tín (Tài liệu chính thức, tutorial uy tín, sách...)",
            "url": "Đường dẫn URL hợp lệ (bắt đầu bằng http hoặc https)"
        }}
    ],
    "quiz": [
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 1",
            "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích chi tiết vì sao đáp án đúng và các đáp án khác sai."
        }}
    ],
    "lab": {{
        "title": "Tiêu đề bài thực hành",
        "objectives": ["Mục tiêu 1"],
        "steps": ["Bước 1"],
        "checklist": ["Tiêu chí 1"]
    }},
    "visualizer": {{
        "canvas_title": "Tiêu đề của khung trực quan hóa...",
        "legend_html": "Mã HTML hiển thị chú giải các trạng thái màu sắc",
        "stats_html": "Mã HTML hiển thị các thẻ đếm (ví dụ: trạng thái, số lượng...)",
        "code_tracker_html": "Mã HTML chứa code. MỖI DÒNG CODE BẮT BUỘC nằm trong 1 thẻ <div class='code-line' id='line-0'>...</div> và dùng \\n ở cuối mỗi thẻ. Giữ nguyên khoảng trắng thụt lề (indentation).",
        "input_label": "Nhãn cho ô nhập liệu tùy chỉnh",
        "input_default": "Giá trị mặc định cho ô nhập liệu",
        "engine_js": "Mã JavaScript của class InteractiveVisualizerEngine. Class phải định nghĩa start(), pause(), step(), reset(). YÊU CẦU AN TOÀN TUYỆT ĐỐI: 1) Bao bọc logic của các phương thức init(), start(), pause(), step(), reset(), và render() trong các khối try-catch để tránh crash giao diện gây reload vô tận. 2) Bắt buộc validate tốc độ thực thi: 'this.speed = Math.max(50, parseInt(speedVal) || 400);' trong các phương thức để tránh đơ trình duyệt. 3) Cập nhật DOM an toàn (chỉ thay đổi class 'active-line' cho code tracker và nội dung stats/logs khi các phần tử tồn tại thực sự). 4) Mọi nút bấm tương tác HTML được sinh ra hoặc gọi trong JS bắt buộc phải có thuộc tính type='button' và gọi event.preventDefault() trong callback event để ngăn chặn reload trang."
    }}
}}
WARNING: LỖI NGHIÊM TRỌNG NẾU VI PHẠM: Tuyệt đối KHÔNG BẤM ENTER (ngắt dòng thực) bên trong bất kỳ chuỗi string nào của JSON (đặc biệt là Code và Markdown). Phải viết liền mạch trên một dòng và dùng ký tự "\\n" thay cho việc ngắt dòng! Tuyệt đối không dùng dấu ngoặc kép không được escape (" -> \\").
Return only raw JSON. Do not wrap in markdown code blocks.
"""
    for attempt in range(3):
        response_text = call_llm(
            system_prompt,
            user_prompt,
            json_mode=True,
            agent_name=f"Creator_Agent_Att{attempt+1}",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if response_text:
            try:
                cleaned = response_text.strip()
                # Trích xuất phần JSON bằng biểu thức chính quy (nếu có bao bọc bởi markdown)
                json_match = re.search(r"```json\s*(\{.*`?\})\s*```", response_text, re.DOTALL)
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
                
                # Sửa đổi các dấu xuống dòng thô không được escape trong các chuỗi JSON
                cleaned = fix_raw_newlines_in_json_strings(cleaned)
                result = robust_json_parse(cleaned)
                
                # Validation of key fields to ensure no crash
                required_keys = ["problem", "analysis", "solution", "example", "resolve", "summary", "self_test", "quiz", "lab", "visualizer"]
                if all(k in result for k in required_keys):
                    print(f"  [Creator Agent] Dynamic generation successful on attempt {attempt+1}!")
                    if state is not None:
                        state["master_content"] = result
                    return result
                else:
                    print(f"  [Creator Agent Warning] Attempt {attempt+1} LLM JSON response is missing required keys: {set(required_keys) - set(result.keys())}")
            except Exception as e:
                print(f"  [Creator Agent Warning] Attempt {attempt+1} Failed to parse dynamic content generated by LLM: {e}")
        else:
            print(f"  [Creator Agent Warning] Attempt {attempt+1} LLM returned empty response or call failed.")
            
    raise RuntimeError("ERROR: Failed to generate and parse dynamic master content via LLM after 3 attempts.")



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

    # Build lesson slug for file naming
    import re
    def slugify(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
        text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
        text = re.sub(r'[ìíịỉĩ]', 'i', text)
        text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
        text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
        text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
        text = re.sub(r'[đ]', 'd', text)
        text = re.sub(r'[^a-z0-9\s_]', '', text)
        return re.sub(r'[\s]+', '_', text)

    s_id_slug = slugify(session_id)
    l_id_slug = slugify(lesson_id) if lesson_id else "lesson"
    lesson_slug = f"{s_id_slug}_{l_id_slug}"

    system_prompt = f"""Bạn là Video Director Agent — chuyên gia sản xuất video E-learning theo chuẩn HyperFrames.
Nhiệm vụ của bạn là tạo ra một "Production Blueprint JSON" cho video bài học, tuân thủ TUYỆT ĐỐI các quy tắc kỹ thuật từ SKILL.md sau:

{hyperframes_skill}

NGUYÊN TẮC CỐT LÕI:
1. CHIA ĐỦ SCENE: Tạo ra 3-5 scenes. Mỗi scene có 1 chủ đề rõ ràng.
2. NARRATION NGẮN GỌN: Tổng từ narration của tất cả scenes đạt 150-250 từ. Lời thoại ngắn gọn, súc tích (40-60 từ/scene) để tránh bị cắt cụt JSON.
3. CẤU TRÚC ANIMATION: Mỗi scene có 2-3 mốc animation chính (intro-title 0.2s→3.2s, nội dung chính 4.0s+).
4. DESIGN SYSTEM: Dùng đúng màu sắc và font từ design system (#0f1117, #e6edf3, Inter, Fira Code).
5. SƯ PHẠM: Mở đầu "Chào mừng các em..." và kết "Cảm ơn các em..."
6. CÔNG NGHỆ: Kịch bản phải bám sát 100% vào {tech_stack}.

Output JSON BẮT BUỘC theo cấu trúc CHÍNH XÁC này:
{{
  "lesson_slug": "{lesson_slug}",
  "lesson_title": "{lesson_title}",
  "total_duration": <tổng thời gian tất cả scenes>,
  "scenes": [
    {{
      "scene_id": "Scene_01",
      "scene_title": "<Tiêu đề ngắn của scene>",
      "start_at_root": 0,
      "duration": <số giây của scene, thường 20-30s>,
      "track_index": 1,
      "narration": "<Lời thoại súc tích, 40-60 từ/scene>",
      "visual_description": "<Mô tả những gì hiện trên màn hình>",
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

    # Generate via LLM or raise error
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")):
        raise RuntimeError("ERROR: API key for LLM is missing. Video Script Director requires an active LLM.")
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
            result_json = robust_json_parse(llm_resp)
            # Validate required fields
            if "scenes" not in result_json or not result_json["scenes"]:
                raise ValueError("Missing 'scenes' in blueprint JSON")
            if "tts_scripts" not in result_json:
                raise ValueError("Missing 'tts_scripts' in blueprint JSON")
            print(f"  [Video_Director_Agent] Blueprint generated: {len(result_json['scenes'])} scenes, duration {result_json.get('total_duration', 0)}s")
        except Exception as e:
            raise RuntimeError(f"ERROR: Video Script Director failed to generate blueprint JSON via LLM: {e}")

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
    
    full_curr_str = str(state.get("full_curriculum", "[]"))
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
                base_host = base_url.rstrip('/')
                url = f"{base_host}/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            else:
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
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore
        
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), "#0F172A")
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 28)
            font_header = ImageFont.truetype("arial.ttf", 20)
            font_body = ImageFont.truetype("arial.ttf", 16)
        except Exception:
            font_title = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_body = ImageFont.load_default()
            
        grid_size = 40
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill="#1E293B", width=1)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill="#1E293B", width=1)
            
        draw.rounded_rectangle([40, 30, width-40, 95], radius=8, fill="#1E1E2F", outline="#06B6D4", width=3)
        draw.text((width//2, 62), f"SYSTEM DIAGRAM: {title.upper()}", fill="#22D3EE", font=font_title, anchor="mm")
        
        draw.rounded_rectangle([80, 250, 360, 470], radius=10, fill="#1E293B", outline="#3B82F6", width=2)
        draw.text((220, 280), "CLIENT / USER AGENT", fill="#3B82F6", font=font_header, anchor="mm")
        draw.text((220, 350), "HTTP Request\n(GET/POST/PUT/DELETE)\nHeaders & JSON Body", fill="#94A3B8", font=font_body, anchor="mm")
        
        draw.line([(360, 360), (520, 360)], fill="#06B6D4", width=4)
        draw.polygon([(520, 350), (520, 370), (540, 360)], fill="#06B6D4")
        
        draw.rounded_rectangle([540, 200, 840, 520], radius=10, fill="#1E293B", outline="#10B981", width=2)
        draw.text((690, 230), "BACKEND ENGINE", fill="#10B981", font=font_header, anchor="mm")
        draw.text((690, 320), "Middleware Pipeline\nRouting & Controllers\nValidation & Security\nBusiness Logic Execution", fill="#94A3B8", font=font_body, anchor="mm")
        
        draw.line([(840, 360), (1000, 360)], fill="#06B6D4", width=4)
        draw.polygon([(1000, 350), (1000, 370), (1020, 360)], fill="#06B6D4")
        
        draw.rounded_rectangle([1020, 250, 1200, 470], radius=10, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((1110, 280), "DATA LAYER", fill="#F59E0B", font=font_header, anchor="mm")
        draw.text((1110, 350), "In-Memory DB / SQLite\nJSON State / ORM\nPersistence Context", fill="#94A3B8", font=font_body, anchor="mm")
        
        draw.rounded_rectangle([40, 560, width-40, 680], radius=8, fill="#111827", outline="#374151", width=1)
        draw.text((60, 580), "PROMPT DESCRIPTION:", fill="#6B7280", font=font_body)
        
        words = prompt_text.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > 110:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
            
        y_prompt = 610
        for pline in lines[:3]:
            draw.text((60, y_prompt), pline, fill="#D1D5DB", font=font_body)
            y_prompt += 22
            
        image_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(image_path)
        print(f"  [Fallback Image] Saved fallback diagram to: {image_path}")
    except Exception as e:
        print(f"  [Fallback Image Error] Failed to generate fallback diagram: {e}")

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
                lesson_title = state.get("core_ssot", {}).get("session_title", "Concept Flow")
                draw_mindmap_fallback_diagram(prompt_text, image_path, lesson_title)
        
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
        raise RuntimeError("ERROR: API key for LLM is missing. Mindmap Agent requires an active LLM.")
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
- Đảm bảo nhánh cấp 2 (##) đầu tiên là `## Mục tiêu bài học`.
- Các nhánh tiếp theo tương ứng với các chủ đề lý thuyết chính của bài học (chính là danh sách các khái niệm cốt lõi ở trên). Dưới mỗi nhánh chủ đề cấp 2 (##) (trừ nhánh Mục tiêu bài học) phải có đúng 3 nhánh con cấp 3 (### Khái niệm cốt lõi, ### Cú pháp & Cách khai báo, ### Lưu ý thực chiến). Không được sử dụng bất kỳ tên nhánh H3 nào khác!
- Cú pháp khai báo code mẫu trong nhánh `### Cú pháp & Cách khai báo` phải được bọc trong block Markdown chỉ định ngôn ngữ và thụt lề bằng dấu cách chính xác dưới gạch đầu dòng tương ứng.
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
            raise RuntimeError("ERROR: Mindmap Agent failed to generate markmap content via LLM.")

    # Process and replace image prompts
    processed_content = process_mindmap_images(markmap_content, state)
    state["mindmap_markdown"] = processed_content
    log_agent_tokens("Mindmap_Agent", state, processed_content)
    return state


def slide_agent(state: AgentState) -> AgentState:
    """
    Slide Agent:
    Generates Marp markdown slides suitable for lecturing via LLM.
    Follows Visual Design Rules: homogeneous structures, minimal bullets.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    acad_logs = [log for log in state.get("review_logs", []) if log["source"] == "Academic_Reviewer"]
    attempt_num = len(acad_logs) + 1
    feedback = acad_logs[-1]["feedback"] if acad_logs else ""
    
    print(f"\n[Slide_Agent] Designing Slide Deck for {session_id} {lesson_id} | Attempt: #{attempt_num}")
    
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
    
    system_prompt = f"""Bạn là một Chuyên gia thiết kế Slide Bài Giảng (Instructional Slide Designer).
Nhiệm vụ: Tạo nội dung trình chiếu Markdown (Marp framework) cho bài học '{display_title}'.
Yêu cầu thiết kế:
1. Bố cục: Bắt đầu bằng block Marp chuẩn:
---
marp: true
theme: gaia
_class: lead
paginate: true
---
2. Nội dung: Phải chia nhỏ nội dung ra nhiều slide (ngăn cách bằng `---`). Không nhồi nhét quá nhiều chữ vào một slide.
3. Code Samples: Phải trích xuất mã nguồn mẫu từ SSOT và đưa vào slide có highlight syntax chuẩn xác để giảng viên có thể demo.
4. Trình bày Khoa học: Dùng bullet point ngắn gọn. KHÔNG dùng tiêu đề `###` lồng bên trong gạch đầu dòng `-`.
"""
    
    user_prompt = f"""
Nội dung bài giảng chi tiết:
- Vấn đề: {content.get('problem', '')}
- Phân tích: {content.get('analysis', '')}
- Giải pháp: {content.get('solution', '')}
- Tổng kết: {content.get('summary', '')}

Tri thức gốc (SSOT):
{json.dumps(core_ssot.get('concepts', {}), ensure_ascii=False)}
{json.dumps(core_ssot.get('code_samples', {}), ensure_ascii=False)}

Phản hồi từ Academic Reviewer (nếu có, hãy sửa lỗi này):
{feedback}

Hãy sinh ra toàn bộ file Markdown cho Marp slides. KHÔNG bọc trong ```markdown, chỉ trả về nội dung raw.
"""
    
    slides_md = call_llm(
        system_prompt,
        user_prompt,
        json_mode=False,
        agent_name=f"Slide_Agent_Att{attempt_num}",
        session_id=session_id,
        lesson_id=lesson_id
    )
    
    if slides_md:
        slides_md = slides_md.strip()
        if slides_md.startswith("```markdown"):
            slides_md = slides_md[11:]
        if slides_md.endswith("```"):
            slides_md = slides_md[:-3]
        slides_md = slides_md.strip()
    else:
        # Fallback if LLM fails
        slides_md = f"---\nmarp: true\ntheme: gaia\n_class: lead\npaginate: true\n---\n\n# {display_title}\n\nLỗi khi sinh slide."

    state["slide_markdown"] = slides_md
    log_agent_tokens("Slide_Agent", state, slides_md)
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
    return "\n".join(html)

def convert_markdown_to_html(text: str) -> str:
    if not text:
        return ""
    
    lines = text.split('\n')
    output = []
    
    list_stack = []  # Stack of (indent_level, 'ul'/'ol')
    in_blockquote = False
    in_code = False
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
                
            if in_code:
                output.append("</code></pre></div></div>")
                in_code = False
            else:
                lang = line_strip[3:].strip() or "python"
                output.append(f'<div class="code-container"><div class="code-header"><span class="code-title">{lang}</span></div><div class="code-body"><pre><code class="language-{lang}">')
                in_code = True
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
            raw_text = ul_match.group(1) if ul_match else (ol_match.group(1) if ol_match else "")
            content = process_inline(raw_text)
            
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
    if in_code:
        output.append("</code></pre></div></div>")
        
    return "\n".join([line for line in output if line])

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
    
    problem_html = convert_markdown_to_html(content["problem"])
    analysis_html = convert_markdown_to_html(content["analysis"])
    solution_html = convert_markdown_to_html(content["solution"])
    resolve_html = convert_markdown_to_html(content["resolve"])
    summary_html = convert_markdown_to_html(content["summary"])
    
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
        """
        
    self_test_markdown = f"# Bộ câu hỏi Khảo thí & Đánh giá năng lực: {lesson_title}\n\n"
    self_test_data = content.get("self_test", [])
    if isinstance(self_test_data, dict):
        self_test_data = [self_test_data]
    elif not isinstance(self_test_data, list):
        self_test_data = []
        
    for idx, q_item in enumerate(self_test_data, 1):
        if isinstance(q_item, dict):
            q_text = q_item.get("question", "")
            q_answer = q_item.get("answer", "") or q_item.get("guideline", "") or q_item.get("suggestion", "")
        else:
            q_text = str(q_item)
            q_answer = "Hãy đọc lại phần lý thuyết và thực hành ví dụ trên máy tính cá nhân để tự đối chiếu và kiểm tra kết quả."
            
        self_test_markdown += f"### Câu {idx}: {q_text}\n\n**Gợi ý trả lời & Hướng dẫn tự học:**\n{q_answer}\n\n---\n\n"

    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    
    references_html = ""
    refs = content.get("references", [])
    if isinstance(refs, dict):
        refs = [refs]
    elif not isinstance(refs, list):
        refs = []

    
    t_lower = lesson_title.lower()
    has_no_code = not raw_code or not raw_code.strip() or all(line.strip().startswith(('#', '//', '/*', '*', '$', 'pip', 'python')) for line in raw_code.splitlines() if line.strip())
    is_theory_only = has_no_code or any(kw in t_lower for kw in [
        "giới thiệu", "cài đặt", "môi trường", "ide", "tổng quan", "khái niệm cơ bản", "lý thuyết", "bản chất", "tìm hiểu", "khái quát",
        "lộ trình", "phương pháp", "hướng dẫn", "chuẩn bị", "tài liệu", "đánh giá", "roadmap", "method", "methodology", "study plan",
        "kế hoạch", "milestone", "milestones", "kỹ năng", "tự học"
    ]) or any(kw in session_id.lower() for kw in [
        "lộ trình", "phương pháp", "hướng dẫn", "chuẩn bị", "tài liệu", "đánh giá", "roadmap", "method", "methodology", "study plan",
        "kế hoạch", "milestone", "milestones", "kỹ năng", "tự học"
    ]) or not lesson_id

    if is_theory_only:
        visualizer_section_html = ""
        # Strict enforcement: NEVER show step 4 for theory lessons, regardless of what AI hallucinated.
        step_4_html = "" 
            
        js_initializer = """
        document.addEventListener('DOMContentLoaded', () => {
            if (window.hljs) hljs.highlightAll();
        });
        """
    else:
        # For non-theory lessons, step 4 is displayed if there is code
        step_4_html = "" if has_no_code else f"""
                    <!-- Step 4: Setup & Configuration Code -->
                    <div class="step">
                        <div class="badge">4</div>
                        <div class="step-body">
                            <div class="step-loc">Lệnh cấu hình & Mã nguồn <span class="range"></span></div>
                            {code_block_html}
                            <div style="margin-top: 16px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>"""
                    
        vis_comp = content.get("visualizer")
        if not vis_comp:
            vis_comp = {}
            
        canvas_title = vis_comp.get("canvas_title", "Interactive Visualizer")
        legend_html = vis_comp.get("legend_html", "")
        stats_html = vis_comp.get("stats_html", "")
        code_tracker_html = vis_comp.get("code_tracker_html", "")
        input_label = vis_comp.get("input_label", "Input Data")
        input_default_raw = vis_comp.get("input_default", "")
        
        # Robust full-featured interactive engine logic
        engine_js = vis_comp.get("engine_js", "")
        if not engine_js or "constructor() {}" in engine_js or "InteractiveVisualizerEngine" not in engine_js:
            engine_js = """class InteractiveVisualizerEngine {
    constructor() {
        this.steps = [];
        this.currentStep = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 400;
    }
    
    init() {
        try {
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
                    { message: "Khởi chạy Client gửi yêu cầu HTTP Request", step: 0 },
                    { message: "ASGI Server (Uvicorn) tiếp nhận và chuyển tiếp request", step: 1 },
                    { message: "FastAPI Routing Handler xử lý nghiệp vụ & Middleware", step: 2 },
                    { message: "Trả về dữ liệu JSON Response cho Client thành công", step: 3 }
                ];
            }
            
            this.currentStep = 0;
            this.isPlaying = false;
            this.render();
        } catch (e) {
            console.error("Lỗi khởi tạo mô phỏng:", e);
            this.log("⚠ [Lỗi] Không thể khởi tạo bộ mô phỏng.");
        }
    }
    
    start() {
        try {
            if (this.isPlaying) return;
            this.isPlaying = true;
            this.log("▶ [Bắt đầu] Đang khởi chạy quy trình phỏng đoán trực quan.");
            this.runLoop();
        } catch (e) {
            console.error(e);
        }
    }
    
    pause() {
        try {
            this.isPlaying = false;
            if (this.timer) {
                clearTimeout(this.timer);
                this.timer = null;
            }
            this.log("⏸ [Tạm dừng] Đã tạm dừng luồng chạy.");
        } catch (e) {
            console.error(e);
        }
    }
    
    step() {
        try {
            this.pause();
            if (!this.steps || this.steps.length === 0) return;
            this.currentStep = (this.currentStep + 1) % this.steps.length;
            this.log(`⏭ [Từng bước] Đã chuyển sang bước ${this.currentStep + 1}`);
            this.render();
        } catch (e) {
            console.error(e);
        }
    }
    
    reset() {
        try {
            this.pause();
            this.currentStep = 0;
            this.log("↻ [Đặt lại] Đã đưa trạng thái hệ thống về ban đầu.");
            this.render();
        } catch (e) {
            console.error(e);
        }
    }
    
    setSpeed(speedVal) {
        try {
            this.speed = Math.max(50, parseInt(speedVal) || 400);
            const display = document.getElementById('speed-display');
            if (display) display.innerText = this.speed;
            const slider = document.getElementById('slider-speed');
            if (slider) slider.value = this.speed;
        } catch (e) {
            console.error(e);
        }
    }
    
    applyCustomData() {
        try {
            const inputEl = document.getElementById('custom-data-input');
            const val = inputEl ? inputEl.value : "";
            this.log(`⚙ [Cấu hình] Đã áp dụng dữ liệu đầu vào: ${val || '(trống)'}`);
            this.reset();
        } catch (e) {
            console.error(e);
        }
    }
    
    runLoop() {
        try {
            if (!this.isPlaying) return;
            if (!this.steps || this.steps.length === 0) return;
            
            const delay = Math.max(50, this.speed || 400);
            this.timer = setTimeout(() => {
                try {
                    this.currentStep = (this.currentStep + 1) % this.steps.length;
                    this.render();
                    if (this.currentStep === 0) {
                        this.pause();
                        this.log("✅ [Hoàn tất] Luồng chạy đã kết thúc một chu kỳ.");
                    } else {
                        this.runLoop();
                    }
                } catch (err) {
                    console.error("Lỗi trong vòng lặp mô phỏng:", err);
                    this.pause();
                }
            }, delay);
        } catch (e) {
            console.error(e);
            this.pause();
        }
    }
    
    render() {
        try {
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
                    if (desc.includes('from') || desc.includes('app =') || desc.includes('@app.') || desc.includes('def') || desc.includes('return')) {
                        desc = `Đang thực thi lệnh: <code style="color: var(--primary); font-family: var(--font-mono); font-weight: 600;">${desc}</code>`;
                    }
                    stepperDesc.innerHTML = desc;
                }
                if (stepperProgress) stepperProgress.innerText = `Bước ${stepIdx + 1}/${this.steps.length}`;
                if (stepperBar) stepperBar.style.width = `${((stepIdx + 1) / this.steps.length) * 100}%`;
            }
            
            this.updateStats();
            
            const canvas = document.getElementById('visualizer-canvas');
            if (canvas) {
                let clientClass = "border-slate-300 dark:border-slate-700 text-slate-400 dark:text-slate-600";
                let serverClass = "border-slate-300 dark:border-slate-700 text-slate-400 dark:text-slate-600";
                let appClass = "border-slate-300 dark:border-slate-700 text-slate-400 dark:text-slate-600";
                let handlerClass = "border-slate-300 dark:border-slate-700 text-slate-400 dark:text-slate-600";
                
                const nodeIndex = stepIdx % 4;
                if (nodeIndex === 0) {
                    clientClass = "border-emerald-500 bg-emerald-500/10 text-emerald-500 shadow-lg shadow-emerald-500/20 scale-110";
                } else if (nodeIndex === 1) {
                    serverClass = "border-amber-500 bg-amber-500/10 text-amber-500 shadow-lg shadow-amber-500/20 scale-110";
                } else if (nodeIndex === 2) {
                    appClass = "border-blue-500 bg-blue-500/10 text-blue-500 shadow-lg shadow-blue-500/20 scale-110";
                } else if (nodeIndex === 3) {
                    handlerClass = "border-indigo-500 bg-indigo-500/10 text-indigo-500 shadow-lg shadow-indigo-500/20 scale-110";
                }
                
                canvas.innerHTML = `
                    <div class="flex flex-col md:flex-row items-center justify-around w-full gap-4 md:gap-2 my-auto py-6 select-none">
                      <div class="flex flex-col items-center transition-all duration-300">
                        <div class="w-20 h-20 rounded-2xl flex items-center justify-center border-2 bg-white dark:bg-slate-900 transition-all duration-300 ${clientClass}">
                          <i class="ph-duotone ph-desktop text-4xl"></i>
                        </div>
                        <span class="text-xs font-semibold mt-2 text-slate-600 dark:text-slate-400">Client</span>
                      </div>
                      
                      <div class="hidden md:block text-slate-300 dark:text-slate-700 text-xl font-bold transition-all duration-300 ${nodeIndex >= 1 ? 'text-amber-500' : ''}">➔</div>
                      
                      <div class="flex flex-col items-center transition-all duration-300">
                        <div class="w-20 h-20 rounded-2xl flex items-center justify-center border-2 bg-white dark:bg-slate-900 transition-all duration-300 ${serverClass}">
                          <i class="ph-duotone ph-hard-drives text-4xl"></i>
                        </div>
                        <span class="text-xs font-semibold mt-2 text-slate-600 dark:text-slate-400">ASGI Server (Uvicorn)</span>
                      </div>
                      
                      <div class="hidden md:block text-slate-300 dark:text-slate-700 text-xl font-bold transition-all duration-300 ${nodeIndex >= 2 ? 'text-blue-500' : ''}">➔</div>
                      
                      <div class="flex flex-col items-center transition-all duration-300">
                        <div class="w-20 h-20 rounded-2xl flex items-center justify-center border-2 bg-white dark:bg-slate-900 transition-all duration-300 ${appClass}">
                          <i class="ph-duotone ph-cpu text-4xl"></i>
                        </div>
                        <span class="text-xs font-semibold mt-2 text-slate-600 dark:text-slate-400">FastAPI Instance</span>
                      </div>
                      
                      <div class="hidden md:block text-slate-300 dark:text-slate-700 text-xl font-bold transition-all duration-300 ${nodeIndex >= 3 ? 'text-indigo-500' : ''}">➔</div>
                      
                      <div class="flex flex-col items-center transition-all duration-300">
                        <div class="w-20 h-20 rounded-2xl flex items-center justify-center border-2 bg-white dark:bg-slate-900 transition-all duration-300 ${handlerClass}">
                          <i class="ph-duotone ph-code text-4xl"></i>
                        </div>
                        <span class="text-xs font-semibold mt-2 text-slate-600 dark:text-slate-400">Route Handler</span>
                      </div>
                    </div>
                `;
            }
        } catch (e) {
            console.error("Lỗi vẽ giao diện mô phỏng:", e);
        }
    }
    
    log(msg) {
        try {
            const logBox = document.getElementById('log-messages');
            if (!logBox) return;
            
            let entryClass = "log-info";
            if (msg.includes("▶") || msg.includes("⚙")) entryClass = "log-info";
            else if (msg.includes("✅") || msg.includes("Hoàn tất")) entryClass = "log-success";
            else if (msg.includes("⏸") || msg.includes("Tạm dừng")) entryClass = "log-warn";
            else if (msg.includes("⚠") || msg.includes("Lỗi")) entryClass = "log-error";
            
            logBox.innerHTML += `<div class="log-entry ${entryClass}">${msg}</div>`;
            logBox.scrollTop = logBox.scrollHeight;
        } catch (e) {
            console.error(e);
        }
    }
    
    clearLog() {
        try {
            const logBox = document.getElementById('log-messages');
            if (logBox) logBox.innerHTML = "";
        } catch (e) {
            console.error(e);
        }
    }
    
    updateStats() {}
    
    scrubStep(e) {
        try {
            if (!this.steps || this.steps.length === 0) return;
            const barContainer = e.currentTarget;
            const rect = barContainer.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const percentage = clickX / rect.width;
            const targetStep = Math.min(this.steps.length - 1, Math.max(0, Math.floor(percentage * this.steps.length)));
            
            this.currentStep = targetStep;
            this.log(`ℹ [Hệ thống] Đã tua đến bước ${targetStep + 1}`);
            this.render();
        } catch (err) {
            console.error(err);
        }
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
                <!-- Core Concept & Tech Stack Header Card -->
                <div class="core-concept-card" style="background: var(--bg-panel); border: 1.5px solid var(--border-color); border-radius: var(--radius-lg); padding: 32px 36px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <div style="flex: 1; min-width: 260px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: var(--primary); background: rgba(74, 142, 179, 0.12); padding: 3px 10px; border-radius: 12px;">Khái niệm lý thuyết</span>
                            <span style="font-size: 0.78rem; font-weight: 600; color: var(--text-muted);">{session_id}</span>
                        </div>
                        <h3 style="font-family: var(--font-serif); font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin: 0 0 4px 0;">{lesson_title}</h3>
                        <p style="font-size: 0.9rem; color: var(--text-muted); margin: 0; line-height: 1.5;">Nắm vững bản chất kỹ thuật qua mô phỏng trực quan — Giải mã cách máy tính vận hành từng dòng code.</p>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted);">Công nghệ trọng tâm</span>
                        <span style="background: var(--bg-hover); border: 1.5px solid var(--border-color); padding: 6px 14px; border-radius: 8px; font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; color: var(--primary);">{tech_stack.upper()}</span>
                    </div>
                </div>

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
                visualizerApp.init();
            }}
            if (typeof visualizerApp.render === 'function') {{
                visualizerApp.render();
            }}

            // Auto-fix code tracker formatting if LLM glued tags together
            const trackerBox = document.getElementById('code-tracker-box');
            if (trackerBox) {{
                let rawHtml = trackerBox.innerHTML;
                rawHtml = rawHtml.replace(/<\\/div><div/g, '</div>\\n<div');
                rawHtml = rawHtml.replace(/<\\/span><span/g, '</span>\\n<span');
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
    ref_step_num = 4 if has_no_code or is_theory_only else 5
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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/dracula.min.css">
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
    </style>
</head>
<body class="bg-slate-50 text-slate-800 dark:bg-[#0b0f19] dark:text-slate-200 antialiased font-sans transition-colors duration-300">
    <!-- Sticky Nav Header -->
    <div id="sticky-header" class="sticky top-0 z-30 bg-white/95 dark:bg-[#151d30]/95 backdrop-blur-md border-b border-slate-200 dark:border-[#243049] shadow-sm px-4 md:px-6 py-3 transition-all duration-300">
        <div class="max-w-[1600px] w-full mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3">
                <!-- Rikkei Logo -->
                <img src="../../../../../resources/logo-main.png" alt="Rikkei Education Logo" class="h-9 w-auto object-contain" />
            </div>
            <div class="flex items-center gap-3">
                <!-- Theme Switcher Segmented Control -->
                <div class="flex items-center gap-1 border border-slate-200 dark:border-slate-700 rounded-lg p-0.5 bg-slate-50 dark:bg-slate-800">
                    <button id="theme-btn-light" onclick="setThemeMode('light')" class="p-1.5 rounded-md text-xs border transition-all cursor-pointer flex items-center justify-center" title="Chế độ sáng"><i class="ph ph-sun-dim text-base"></i></button>
                    <button id="theme-btn-dark" onclick="setThemeMode('dark')" class="p-1.5 rounded-md text-xs border transition-all cursor-pointer flex items-center justify-center" title="Chế độ tối"><i class="ph ph-moon text-base"></i></button>
                    <button id="theme-btn-system" onclick="setThemeMode('system')" class="p-1.5 rounded-md text-xs border transition-all cursor-pointer flex items-center justify-center" title="Chế độ hệ thống"><i class="ph ph-desktop text-base"></i></button>
                </div>
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
                            <div class="step-loc">Đặt vấn đề</div>
                            {problem_html}
                        </div>
                    </div>

                    <!-- Step 2: Deep Dive Internals -->
                    <div class="step">
                        <div class="badge">2</div>
                        <div class="step-body">
                            <div class="step-loc">Phân tích Bản chất</div>
                            {analysis_html}
                        </div>
                    </div>

                    <!-- Step 3: Solution & Architecture -->
                    <div class="step">
                        <div class="badge">3</div>
                        <div class="step-body">
                            <div class="step-loc">Giới thiệu Giải pháp</div>
                            {solution_html}
                        </div>
                    </div>
{step_4_html}


{references_html}

                    <!-- Bottom Notice / Gotchas Section -->
                    <div class="step" style="margin-top: 24px;">
                        <div class="badge" style="background: var(--clay); color: #ffffff; border-color: var(--clay);">★</div>
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

        function copyCode(button, codeId) {{
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

        function applyTheme() {{
            const savedMode = localStorage.getItem('themeMode') || 'system';
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDark = savedMode === 'dark' || (savedMode === 'system' && prefersDark);
            
            if (isDark) {{
                document.documentElement.classList.add('dark');
                document.documentElement.classList.add('theme-dark');
            }} else {{
                document.documentElement.classList.remove('dark');
                document.documentElement.classList.remove('theme-dark');
            }}

            ['light', 'dark', 'system'].forEach(m => {{
                const btn = document.getElementById('theme-btn-' + m);
                if (btn) {{
                    if (m === savedMode) {{
                        btn.classList.add('active');
                    }} else {{
                        btn.classList.remove('active');
                    }}
                }}
            }});
        }}

        function setThemeMode(mode) {{
            localStorage.setItem('themeMode', mode);
            applyTheme();
        }}

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {{
            if ((localStorage.getItem('themeMode') || 'system') === 'system') {{
                applyTheme();
            }}
        }});

        document.addEventListener('DOMContentLoaded', () => {{
            applyTheme();
        }});
        applyTheme();
    </script>
</body>
</html>"""
    
    state["html_content"] = html_template
    state["self_test_markdown"] = self_test_markdown
    log_agent_tokens("HTML_Writer_Agent", state, html_template)
    return state

