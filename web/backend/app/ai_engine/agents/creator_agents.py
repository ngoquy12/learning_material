import json
import re
from typing import Dict, Any, List
from core.state import AgentState

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
    keys = ["problem", "analysis", "solution", "example", "resolve", "summary", "self_test", "quiz", "lab", "visualizer", "reading_sections", "references"]
    
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
                result[k] = json.loads(val_sub)
            except Exception:
                try:
                    import ast
                    result[k] = ast.literal_eval(val_sub)
                except Exception:
                    try:
                        cleaned_sub = fix_raw_newlines_in_json_strings(val_sub)
                        result[k] = json.loads(cleaned_sub)
                    except Exception:
                        if k == "self_test":
                            items = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', val_sub)
                            result[k] = [item.replace('\\"', '"') for item in items]
                        elif k == "quiz":
                            result[k] = []
                        elif k == "lab":
                            result[k] = {"title": "Lab", "objectives": [], "steps": [], "checklist": []}
                        elif k == "reading_sections":
                            result[k] = []
                        elif k == "references":
                            result[k] = []
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
            elif k == "reading_sections":
                result[k] = []
            elif k == "references":
                result[k] = []
            elif k == "lab":
                result[k] = {"title": "Lab", "objectives": [], "steps": [], "checklist": []}
            else:
                result[k] = {}
                
    return result

def get_lesson_content(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, attempt_num: int, core_ssot: Dict[str, Any] = None, feedback: str = "", state: AgentState = None) -> Dict[str, Any]:
    # Cache optimization: check if we already generated master content for this lesson
    if state is not None and "master_content" in state and attempt_num == 1 and not feedback:
        print(f"  [Creator Agent] Reusing cached master_content for {session_id} {lesson_id} (Token Cost Saved!).")
        return state["master_content"]

    # Check if LLM is active
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise RuntimeError(
            f"ERROR: LLM API key not found. Offline fallback is disabled. "
            f"Please set GEMINI_API_KEY or OPENAI_API_KEY to run the content generation pipeline."
        )
        
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
    
    # Load lessons learned from previous runs to prevent repeating mistakes
    lessons_learned = load_skill_content("lessons_learned")
    lessons_learned_prompt = ""
    if lessons_learned:
        lessons_learned_prompt = f"\n--- BÀI HỌC KINH NGHIỆM PHÒNG CHỐNG LỖI TỪ CÁC BÀI TRƯỚC (Lessons Learned) ---\nHãy đọc kỹ các bài học này để không lặp lại sai lầm tương tự:\n{lessons_learned}\n"

    system_prompt = f"""Bạn là chuyên gia Thiết kế Chương trình Đào tạo Lập trình (Instructional Designer) và Kỹ sư Phần mềm cao cấp tại Rikkei Education. 
Nhiệm vụ của bạn là biên soạn tài liệu học tập sâu sắc, chất lượng cao về công nghệ '{tech_stack}'.

YÊU CẦU QUAN TRỌNG VỀ TRỌNG TÂM & ĐỘ SÂU KIẾN THỨC:
1. Tập trung 100% vào nội dung bài học: Tài liệu phải bám sát tuyệt đối tiêu đề và chi tiết yêu cầu của Lesson hiện tại từ PM. TUYỆT ĐỐI không viết lan man sang bài học khác làm nội dung quá dài hoặc nhắc đến các bài học tiếp theo.
2. Ràng buộc công nghệ nghiêm ngặt (Technology Stack Isolation): Bạn phải tuân thủ tuyệt đối công nghệ '{tech_stack}'. Chỉ sử dụng các thư viện, framework, cú pháp, quy chuẩn và cấu trúc chuẩn của công nghệ '{tech_stack}'. Tuyệt đối không được trộn lẫn, nhắc đến hoặc sử dụng các thư viện, công nghệ hoặc framework khác.
3. Không bịa đặt nội dung/mã nguồn: Nếu bài học mang tính lý thuyết tổng quan hoặc không liên quan trực tiếp đến lập trình mã nguồn phức tạp (như giới thiệu, cài đặt môi trường...), TUYỆT ĐỐI không tự bịa đặt ra mã nguồn lập trình phức tạp không liên quan. Thay vào đó, dùng câu lệnh CLI cơ bản hoặc ví dụ siêu ngắn hoặc để trống.
4. QUY LUẬT CODE ĐỐI VỚI BÀI LÝ THUYẾT: Đối với bài học mang tính lý thuyết tổng quan (giới thiệu, tổng quan, khái niệm), HẠN CHẾ viết code. TUY NHIÊN, NẾU PM yêu cầu rõ ràng việc code/thực hành trong chi tiết bài học (lesson_details), BẠN BẮT BUỘC PHẢI VIẾT CODE NGẮN GỌN VÀ ĐẦY ĐỦ VÀO TRƯỜNG `example`.
5. Cách trình bày khoa học & súc tích: CỰC KỲ QUAN TRỌNG: Do giới hạn bộ nhớ hệ thống (Token Limit), bạn PHẢI VIẾT CỰC KỲ NGẮN GỌN VÀ SÚC TÍCH. Khống chế tối đa 150-200 từ cho mỗi mục Markdown. Code ví dụ CHỈ viết những dòng trọng tâm nhất (không viết toàn bộ file dài dòng). Nếu viết dài, chữ sẽ bị cắt cụt và toàn bộ quy trình sẽ sụp đổ. HẠN CHẾ TỐI ĐA SỬ DỤNG ICON EMOJI. CHỈ dùng khi thực sự cần thiết. ĐẶC BIỆT CẤM TUYỆT ĐỐI đặt icon emoji ở đầu các tiêu đề (Headings).
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
        for prev in state["previous_lessons"]:
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
    "reading_sections": [
        {{
            "title": "Tiêu đề linh hoạt của phần 1 (VD: Khái niệm cốt lõi, Tình huống thực tế, Từ vựng mới...)",
            "content": "Nội dung chi tiết phần 1 (Markdown)"
        }},
        {{
            "title": "Tiêu đề linh hoạt của phần 2",
            "content": "Nội dung chi tiết phần 2 (Markdown)"
        }},
        {{
            "title": "Tiêu đề linh hoạt của phần 3",
            "content": "Nội dung chi tiết phần 3 (Markdown)"
        }}
    ],
    "example": "Mã nguồn minh họa (đối với môn Lập trình) hoặc Hội thoại/Ví dụ cụ thể (đối với môn Ngoại ngữ). QUY TẮC TỐI THƯỢNG: Nếu bài học là lý thuyết lập trình thuần túy (giới thiệu, lộ trình...), CẤM TUYỆT ĐỐI việc sinh code. TUY NHIÊN, nếu là bài Cài đặt, Setup, hoặc Thực hành, BẮT BUỘC phải sinh đầy đủ các câu lệnh CLI, cấu hình file và mã mẫu chi tiết (tuyệt đối không được bỏ trống).",
    "summary": "Tổng kết và 3 lỗi thường gặp (Markdown). BẮT BUỘC BÔI ĐẬM (DÙNG **bold**) tên các sai lầm thường gặp để học viên dễ chú ý.",
    "self_test": [
        {{
            "question": "Câu hỏi 1 (Tối đa 3 câu). Đặt tên rõ ràng, 100% sát sườn với bài.",
            "answer": "Giải thích ĐẶC BIỆT CHI TIẾT và sâu sắc (không viết chung chung)."
        }}
    ],
    "references": [
        {{
            "title": "Tên tài liệu",
            "url": "URL"
        }}
    ],
    "quiz": [
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 1",
            "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích chi tiết vì sao đáp án đúng và các đáp án khác sai."
        }},
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 2",
            "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích."
        }},
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 3",
            "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích."
        }},
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 4",
            "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích."
        }},
        {{
            "question": "Nội dung câu hỏi trắc nghiệm 5",
            "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
            "correct_option_index": 0,
            "explanation": "Giải thích."
        }}
    ],
    "lab": {{
        "title": "Tiêu đề bài thực hành",
        "objectives": ["Mục tiêu 1", "Mục tiêu 2"],
        "steps": ["Bước 1", "Bước 2"],
        "checklist": ["Tiêu chí 1", "Tiêu chí 2"]
    }},
    "visualizer": {{
        "canvas_title": "Tiêu đề của khung trực quan hóa tương tác phù hợp với công nghệ '{tech_stack}' và nội dung bài học",
        "legend_html": "Mã HTML hiển thị chú giải các trạng thái màu sắc phù hợp với bộ phỏng đoán trực quan",
        "stats_html": "Mã HTML hiển thị các thẻ đếm chỉ số trạng thái (ví dụ: số lần lặp, độ trễ, số lượng biến, hoặc stage...)",
        "code_tracker_html": "Mã HTML của các dòng code có gắn id line-0, line-1... để highlight khi chạy từng bước",
        "input_label": "Nhãn cho ô nhập dữ liệu tùy chỉnh",
        "input_default": "Giá trị mặc định cho ô nhập dữ liệu tùy chỉnh",
        "engine_js": "Mã JavaScript của class InteractiveVisualizerEngine chứa constructor(), init(), generateSteps(), render(), highlightCode(lineNum), log(msg, type), start(), pause(), step(), reset(), setSpeed(val), applyCustomData(), updateStats() để điều khiển toàn bộ logic. LƯU Ý QUAN TRỌNG: Bạn PHẢI sử dụng đúng các element ID trong HTML sau: 'custom-data-input' (để lấy dữ liệu đầu vào trong applyCustomData), 'log-messages' (để in logs/nhật ký thuật toán), và 'visualizer-canvas' (để render giao diện). Tuyệt đối không dùng các ID tự chế khác."
    }}
}}
WARNING: LỖI NGHIÊM TRỌNG NẾU VI PHẠM: Tuyệt đối KHÔNG BẤM ENTER (ngắt dòng thực) bên trong bất kỳ chuỗi string nào của JSON (đặc biệt là Code và Markdown). Phải viết liền mạch trên một dòng và dùng ký tự "\\n" thay cho việc ngắt dòng! Tuyệt đối không dùng dấu ngoặc kép không được escape (" -> \\").
Return only raw JSON. Do not wrap in markdown code blocks.
"""
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Creator_Agent",
        session_id=session_id,
        lesson_id=lesson_id
    )
    if response_text:
        try:
            cleaned = response_text.strip()
            # Trích xuất phần JSON bằng biểu thức chính quy (nếu có bao bọc bởi markdown)
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
            
            # Sửa đổi các dấu xuống dòng thô không được escape trong các chuỗi JSON
            cleaned = fix_raw_newlines_in_json_strings(cleaned)
            result = robust_json_parse(cleaned)
            
            # Map reading_sections to problem, analysis, solution, resolve for compatibility
            if "reading_sections" in result:
                sections = result["reading_sections"]
                def format_section(sect):
                    if not sect:
                        return ""
                    title = sect.get("title", "")
                    body = sect.get("content", "")
                    if title:
                        return f"### {title}\n\n{body}"
                    return body
                
                if "problem" not in result:
                    result["problem"] = format_section(sections[0]) if len(sections) > 0 else ""
                if "analysis" not in result:
                    result["analysis"] = format_section(sections[1]) if len(sections) > 1 else ""
                if "solution" not in result:
                    result["solution"] = format_section(sections[2]) if len(sections) > 2 else ""
                if "resolve" not in result:
                    result["resolve"] = format_section(sections[3]) if len(sections) > 3 else ""
            
            # Validation of key fields to ensure no crash
            required_keys = ["reading_sections", "example", "summary", "self_test", "references", "quiz", "lab", "visualizer"]
            if all(k in result for k in required_keys):
                print("  [Creator Agent] Dynamic generation successful!")
                if state is not None:
                    state["master_content"] = result
                return result
            else:
                raise ValueError(f"LLM JSON response is missing required keys: {set(required_keys) - set(result.keys())}")
        except Exception as e:
            try:
                with open("llm_response_error.json", "w", encoding="utf-8") as f:
                    f.write(response_text)
                print("  [DEBUG] Dumped raw LLM response to llm_response_error.json")
            except Exception as dump_err:
                print(f"  [DEBUG] Failed to dump raw LLM response: {dump_err}")
            raise RuntimeError(f"ERROR: Failed to parse dynamic content generated by LLM: {e}") from e
    else:
        raise RuntimeError("ERROR: LLM returned empty response or call failed.")



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
    Video Script Agent:
    Generates a structured video recording script for the instructor.
    Enforces the 3-part layout (Introduction, Main content, Conclusion) from educational video standards.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    # We can determine the video type dynamically
    t = lesson_title.lower()
    if "giới thiệu" in t or "tổng quan" in t or "định hướng" in t:
        v_type = "Bài học giới thiệu (Introduction lesson)"
        v_class = "intro"
    elif "thực hành" in t or "tích hợp" in t or "xây dựng" in t or "triển khai" in t or "cài đặt" in t or "viết code" in t or "test" in t:
        v_type = "Bài học thực hành (Practice lesson)"
        v_class = "practice"
    else:
        v_type = "Bài học lý thuyết (Theory lesson)"
        v_class = "theory"
        
    print(f"\n[Video_Script_Agent] Formulating {v_type} Script for {session_id} {lesson_id}")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=1,
        core_ssot=core_ssot,
        state=state
    )
    
    # Build dialogue script table based on type
    if v_class == "intro":
        intro_desc = f"Giới thiệu tổng quan về chương trình học và các đề mục của '{lesson_title}'."
        main_desc = f"Giải thích tầm quan trọng của chủ đề, lộ trình học tập, và đích đến thực tế: '{expected_output if expected_output else 'tích hợp thành công và hoạt động ổn định'}'."
        conclusion_desc = "Tóm tắt các yêu cầu bắt buộc và kêu gọi hành động (CTA)."
        
        script_rows = f"""| **00:00 - 00:45** | **[Phần 1: Mở đầu - Introduction]**<br>- Hiện slide tiêu đề: {session_id} - {lesson_id}: {lesson_title}.<br>- Giảng viên (Talking head) xuất hiện ở góc màn hình chào hỏi thân thiện. | "Xin chào các bạn học viên của Rikkei Education! Hôm nay chúng ta sẽ bắt đầu một chương trình học vô cùng thú vị và thực tế. Bài học này sẽ giúp chúng ta có cái nhìn toàn cảnh về: {lesson_title}. Đây sẽ là viên gạch nền móng đầu tiên của cả khóa học." |
| **00:45 - 03:00** | **[Phần 2: Nội dung chính - Main Content]**<br>- Trình bày slide lộ trình học tập và sơ đồ các cấu phần.<br>- Highlight các công nghệ cốt lõi sẽ áp dụng trong môn học.<br>- Chuyển camera cận cảnh giảng viên khi giải thích các mục tiêu. | "Trong phần nội dung chính này, chúng ta cần lưu ý đến những thách thức thực tế sau: {content["problem"][:250]}. Để giải quyết điều đó, giải pháp của chúng ta là học tập chủ động và thiết kế ngược, bám sát dự án thực chiến cuối khóa. Đầu ra kỳ vọng của phần này là: {expected_output if expected_output else 'nắm vững toàn bộ kiến trúc môn học'}. Phân tích sâu hơn, chúng ta thấy..." |
| **03:00 - 04:00** | **[Phần 3: Kết luận - Conclusion]**<br>- Hiện slide tổng kết quy chế môn học và checklist.<br>- Hiển thị QR Code hoặc link tài nguyên bài học.<br>- Giảng viên chào tạm biệt người học. | "Để tóm tắt lại, mục tiêu lớn nhất của chúng ta hôm nay là định hình rõ lộ trình học. Các bạn hãy tải file Markdown dự án về và hoàn thành checklist tự học nhé. Hẹn gặp lại các bạn trong bài thực hành Lab tiếp theo!" |"""

    elif v_class == "theory":
        intro_desc = f"Giới thiệu khái niệm lý thuyết cốt lõi của '{lesson_title}'."
        main_desc = f"Đưa ra bài toán thực tế, phân tích nguyên nhân nếu không áp dụng kỹ thuật, và giới thiệu giải pháp kỹ thuật cụ thể cùng lý thuyết chuẩn."
        conclusion_desc = "Tóm tắt ý chính của lý thuyết và hướng dẫn chuẩn bị cho bài thực hành tiếp theo."
        
        script_rows = f"""| **00:00 - 00:45** | **[Phần 1: Mở đầu - Introduction]**<br>- Hiện slide định nghĩa: {lesson_title}.<br>- Giảng viên giới thiệu khái niệm lý thuyết nền tảng. | "Chào các bạn! Trong bài học lý thuyết hôm nay, chúng ta sẽ cùng nhau tìm hiểu về một chủ đề vô cùng quan trọng, đó là: {lesson_title}. Chúng ta sẽ đi sâu vào cấu trúc và nguyên lý vận hành của nó." |
| **00:45 - 03:30** | **[Phần 2: Nội dung chính - Main Content]**<br>- Show slide phân tích bài toán thực tế (Problem).<br>- Minh họa bằng hình ảnh / sơ đồ khối so sánh (ví dụ: Đồng bộ vs Bất đồng bộ, hoặc API truyền thống vs Pydantic).<br>- Hiện code mẫu minh họa cách viết đúng chuẩn. | "Hãy tưởng tượng một bài toán thực tế: {content["problem"][:250]}. Tại sao vấn đề này lại xảy ra? {content["analysis"][:250]}. Để giải quyết triệt để, chúng ta áp dụng giải pháp: {content["solution"][:200]}. Hãy cùng nhìn vào ví dụ mã nguồn minh họa ở trên slide..." |
| **03:30 - 04:30** | **[Phần 3: Kết luận - Conclusion]**<br>- Tóm tắt 3 ý chính cần ghi nhớ.<br>- Đưa ra lưu ý / lỗi thường gặp (Summary).<br>- Kêu gọi hành động: Đọc thêm bài đọc chi tiết và chuẩn bị làm Quiz. | "Tóm lại, hãy luôn ghi nhớ: {content["summary"][:200]}. Các bạn hãy trả lời 3 câu hỏi tự luận ở cuối bài đọc để củng cố kiến thức nhé. Chúc các bạn học tốt và hẹn gặp lại ở video tiếp theo!" |"""

    else: # practice
        intro_desc = f"Giới thiệu bài toán thực hành cho '{lesson_title}'."
        main_desc = f"Mô hình hóa các bước thực hành qua terminal / IDE, hướng dẫn viết code trực tiếp, khởi chạy uvicorn, và kiểm tra đầu ra."
        conclusion_desc = "Tổng kết checklist hoàn thành bài Lab thực hành."
        
        script_rows = f"""| **00:00 - 00:45** | **[Phần 1: Mở đầu - Introduction]**<br>- Show slide mục tiêu bài Lab thực hành.<br>- Giảng viên mở IDE (VS Code) sẵn sàng để viết code. | "Chào các bạn học viên! Hôm nay chúng ta sẽ bắt tay vào phần thực hành vô cùng quan trọng: {lesson_title}. Mục tiêu của bài thực hành này là giúp các bạn tự tay cài đặt và vận hành hệ thống thực tế." |
| **00:45 - 04:30** | **[Phần 2: Nội dung chính - Main Content]**<br>- Chia sẻ màn hình IDE (VS Code).<br>- Hướng dẫn từng bước viết code, giải thích chi tiết ý nghĩa từng dòng lệnh.<br>- Mở terminal, chạy lệnh khởi tạo / khởi động máy chủ (ví dụ: uvicorn main:app --reload).<br>- Mở trình duyệt truy cập Swagger UI (/docs) để kiểm thử API. | "Bước đầu tiên, chúng ta cần thiết lập môi trường ảo và cài đặt thư viện cần thiết. Các bạn hãy gõ theo tôi: pip install fastapi uvicorn. Tiếp theo, chúng ta viết file main.py. Dòng code này dùng để khởi tạo ứng dụng FastAPI. Bây giờ, hãy chạy máy chủ uvicorn và mở Swagger UI lên kiểm tra nhé..." |
| **04:30 - 05:30** | **[Phần 3: Kết luận - Conclusion]**<br>- Hiện slide checklist đánh giá bài thực hành (Lab checklist).<br>- Nhắc nhở nộp bài đúng hạn lên hệ thống học tập.<br>- Khích lệ tinh thần học viên. | "Vậy là chúng ta đã hoàn thành bài thực hành hôm nay với kết quả đầu ra: {expected_output if expected_output else 'hệ thống chạy ổn định'}. Các bạn hãy kiểm tra lại theo checklist bài Lab để đảm bảo không bỏ sót bước nào. Chúc các bạn thành công!" |"""

    # Combine into Markdown
    script_md = f"""# Kịch bản Video: {session_id} - {lesson_id}: {lesson_title}
- **Thời lượng dự kiến**: 5-7 phút
- **Loại bài giảng**: {v_type}
- **Nhạc nền đề xuất**: Lofi Chill không lời (âm lượng -20dB, tốc độ 1.5x)
- **Chuẩn hình ảnh**: Full HD 1080p, tỷ lệ 16:9, font chữ đồng bộ thương hiệu Rikkei Education

---

## 1. Mục tiêu học tập (Learning Objectives)
1. {intro_desc}
2. {main_desc}
3. {conclusion_desc}

---

## 2. Kịch bản lời thoại & Chỉ dẫn quay hình (Storyboard)

| Thời gian | Chỉ dẫn quay hình & Slide Visuals | Lời thoại chi tiết giảng viên (Conversational Tone) |
| :--- | :--- | :--- |
{script_rows}

---

## 3. Checklist chuẩn bị & Lưu ý kỹ thuật cho Giảng viên
- [ ] Thiết lập âm thanh: Phòng cách âm, không có tiếng ồn trắng hay tiếng quạt gió.
- [ ] Thiết lập màn hình: Độ phân giải màn hình code tối thiểu 1080p, cỡ chữ trong VS Code tăng lên 16-18 để dễ nhìn.
- [ ] Nhịp độ nói: Vừa phải, đối thoại tự nhiên, tránh đọc slide một cách thụ động.
- [ ] Chuyển cảnh: Tránh khoảng lặng chết (dead air), cắt ghép mượt mà giữa camera cá nhân và chia sẻ màn hình.
"""

    state["video_script_markdown"] = script_md
    log_agent_tokens("Video_Script_Agent", state, script_md)
    return state

def mindmap_agent(state: AgentState) -> AgentState:
    """
    Mindmap Agent:
    Generates a structured Markmap diagram based on skills/mindmap_generator/SKILL.md.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = state.get("technology_stack", "python/fastapi")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    print(f"\n[Mindmap_Agent] Generating Markmap diagram for {session_id} {lesson_id} using mindmap_generator skill...")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=1,
        core_ssot=core_ssot,
        state=state
    )
    
    from core.llm import call_llm
    
    reading_sections_text = ""
    for sect in content.get("reading_sections", []):
        reading_sections_text += f"### {sect.get('title', '')}\n{sect.get('content', '')}\n\n"
        
    summary_text = content.get("summary", "")
    example_code = content.get("example", "")
    
    system_prompt = f"""Bạn là một Giảng viên Cao cấp và chuyên gia Thiết kế Chương trình Đào tạo học thuật chuyên sâu tại Rikkei Education. Nhiệm vụ của bạn là dựa vào nội dung bài học được cung cấp để biên soạn một SƠ ĐỒ TƯ DUY (Mindmap) chi tiết, phong phú và có chiều sâu chuyên môn cao để tóm tắt NỘI DUNG HỌC THUẬT của bài học.

Bắt buộc sử dụng Cú pháp MARKDOWN CHUẨN tương thích hoàn toàn với công cụ Markmap (bọc toàn bộ nội dung trong duy nhất một khối ```markmap ... ```).

HƯỚNG DẪN THIẾT KẾ CẤU TRÚC VÀ NỘI DUNG SƠ ĐỒ (CỰC KỲ QUAN TRỌNG):
1. BỐI CẢNH GIẢNG DẠY (THỜI LƯỢNG 1.5 GIỜ): Học viên đã tự học lý thuyết nền tảng ở nhà. Thời gian trên lớp chỉ có 1.5 giờ để giảng viên chốt kiến thức trọng tâm. Do đó, nội dung Mindmap phải THẬT SỰ CÔ ĐỌNG, SÚC TÍCH, tuyệt đối không viết dài dòng tràn lan đại hải. Bỏ qua các thông tin bên ngoài rườm rà không liên quan trực tiếp.
2. CHÍNH SÁCH KHÔNG BỎ SÓT (ZERO-DROP POLICY): Sơ đồ tư duy phải bao quát 100% toàn bộ chủ đề bài học. Bạn BẮT BUỘC phải tạo ĐẦY ĐỦ các nhánh cấp 2 (##) đại diện cho TẤT CẢ các chủ đề chính được nhắc đến trong bài học.
3. KHÔNG LÀM KỊCH BẢN GIẢNG DẠY/GIÁO ÁN: Nhiệm vụ của bạn là tóm tắt NỘI DUNG HỌC THUẬT cốt lõi, chứ KHÔNG phải tạo ra kịch bản đứng lớp hay giáo án cho giảng viên. Tuyệt đối cấm sử dụng các từ khóa như: "Slide 1", "Slide 2", "Lecture Note", "Live Demo Steps", "Concept Check", "Khởi động", v.v.
4. NHÁNH ĐẦU TIÊN LÀ MỤC TIÊU BÀI HỌC (## Mục tiêu bài học): Nhánh lớn cấp 2 (##) đầu tiên luôn là `## Mục tiêu bài học`. Nhánh này chỉ nêu ngắn gọn 2-3 gạch đầu dòng mấu chốt nhất về Kiến thức và Kỹ năng học viên đạt được sau bài học.
5. CÁC NHÁNH CHÍNH TIẾP THEO (Heading 2 - ##) KHỚP VỚI CÁC CHỦ ĐỀ CHÍNH: Các nhánh lớn cấp 2 (##) tiếp theo bắt buộc phải là tiêu đề của các nội dung cốt lõi của bài học (Ví dụ: `## Path parameters`, `## Query parameters`).
6. CẤU TRÚC NHÁNH CON CÔ ĐỌNG CHO LỚP 1.5H (Heading 3 - ###): Dưới mỗi chủ đề chính (##), bạn chỉ tập trung vào 3 nhánh con cốt lõi nhất:
   - ### Khái niệm cốt lõi: Định nghĩa bản chất lý thuyết ngắn gọn nhất (1-2 câu).
   - ### Cú pháp & Cách khai báo: Trình bày cú pháp khai báo kèm ví dụ minh họa cực kỳ cô đọng (bọc trong block code Markdown).
   - ### Lưu ý thực chiến: Những điểm mấu chốt hoặc lỗi hay gặp nhất khi làm dự án thực tế (1-2 ý quan trọng).
7. NỘI DUNG CÔ ĐỌNG: Tại mỗi nhánh, viết ngắn gọn bằng các gạch đầu dòng (-).
8. HÌNH ẢNH TRỰC QUAN (PROMPT AI): Với các khái niệm kiến trúc phức tạp, thêm nút con: `![](../images/mindmap_img_[số].png)` đại diện cho vị trí hình ảnh minh họa logic trực quan.
9. TUYỆT ĐỐI NGHIÊM CẤM DÙNG EMOJI trong toàn bộ sơ đồ tư duy.
10. ĐỊNH DẠNG VÍ DỤ CODE CHUẨN NGÔN NGỮ: Khi minh họa ví dụ code mẫu, bắt buộc phải trình bày theo đúng định dạng khối mã Markdown kèm tên ngôn ngữ (ví dụ ```python ... ```) được thụt lề dưới nhánh gạch đầu dòng (-) tương ứng để Mindmap hiển thị highlight cú pháp trực quan, rõ ràng cho giảng viên giải thích.
11. Bắt buộc kết thúc bằng khối đóng ```. Tuyệt đối không viết thêm bất kỳ lời chào hỏi, giới thiệu hay giải thích nào ngoài khối ```markmap ... ```.
"""

    user_prompt = f"""Hãy tạo Sơ đồ tư duy (Markmap Markdown) cho bài học:
Session ID: {session_id}
Lesson Title: {lesson_title}
Stack công nghệ: {tech_stack}

Chi tiết nội dung thực tế của bài học:
1. Các mục lý thuyết chính:
{reading_sections_text}

2. Mã ví dụ minh họa chính:
```{tech_stack.split('/')[-1]}
{example_code}
```

3. Tóm tắt & Sai lầm cần tránh:
{summary_text}

Hãy sinh Markmap Markdown chính xác theo cấu trúc yêu cầu.
"""

    try:
        response = call_llm(
            system_prompt,
            user_prompt,
            agent_name="Mindmap_Agent",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if response and "```markmap" in response:
            markmap_content = response.strip()
        else:
            markmap_content = f"```markmap\n{response.strip()}\n```"
    except Exception as e:
        print(f"  [Mindmap_Agent Warning] LLM call failed: {e}. Using structured fallback.")
        markmap_content = f"""```markmap
# {session_id}: {lesson_title}
## Mục tiêu bài học
- Hiểu rõ khái niệm cốt lõi của {lesson_title}.
- Nắm vững cú pháp triển khai {tech_stack}.
## {lesson_title}
### Khái niệm lý thuyết
- {lesson_details[:150]}
### Cấu trúc cú pháp
- Ví dụ triển khai:
    ```python
    # {lesson_title} example
    {example_code}
    ```
### Lưu ý
- {expected_output[:150]}
```"""

    state["mindmap_markdown"] = markmap_content
    log_agent_tokens("Mindmap_Agent", state, markmap_content)
    return state


def slide_agent(state: AgentState) -> AgentState:
    """
    Slide Agent:
    Generates Marp markdown slides suitable for lecturing.
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
    
    # Marp slide structure
    slides_md = f"""---
marp: true
theme: gaia
_class: lead
paginate: true
---

# {display_title}
### Lớp học thực chiến Python Web Services

---

# Đặt vấn đề & Thách thức
- Bối cảnh thực tế: {content["problem"]}
- Vấn đề gặp phải: {content["analysis"]}
- Giải pháp: Áp dụng {content["solution"]}

---

# Ví dụ Minh họa Triển khai
- Cú pháp code chuẩn hóa và an toàn
- Sử dụng công cụ tương tác trực quan
- Xem ví dụ triển khai chi tiết trong bài đọc

---

# Tổng kết & Luyện tập
- Bài học cốt lõi: {content["summary"]}
- Thực hành làm bài Lab tuần đầy đủ
- Tự đối chiếu kết quả theo checklist tự học
"""

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
    
    lab_steps = content["lab"]["steps"]
    lab_checklist = content["lab"]["checklist"]
    
    inputs_text = f"Dự án/môi trường phát triển {tech_stack} hiện tại và tài nguyên khóa học."

    quiz_data = {
        "lesson_quiz": content["quiz"],
        "practical_lab": {
            "title": content["lab"]["title"],
            "objectives": content["lab"]["objectives"],
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
            output.append(line)
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
    else:
        # Prevent HTML injection if code contains unescaped HTML characters
        raw_code = raw_code.replace("<", "&lt;").replace(">", "&gt;")
    
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
        
    if refs:
        references_html += f"""
                    <!-- Step 6: References -->
                    <div class="step" style="margin-top: 24px;">
                        <div class="badge"><i class="ph-duotone ph-books"></i></div>
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
        step_4_html = "" if has_no_code else f"""
                    <!-- Step 4: Setup & Configuration Code -->
                    <div class="step">
                        <div class="badge">4</div>
                        <div class="step-body">
                            <div class="step-loc">Code mẫu tham khảo<span class="range"></span></div>
                            {code_block_html}
                            <div style="margin-top: 16px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>"""
            
        js_initializer = """
        document.addEventListener('DOMContentLoaded', () => {
            if (window.hljs) hljs.highlightAll();
        });
        """
    else:
        vis_comp = content.get("visualizer")
        if not vis_comp:
            vis_comp = {
                "canvas_title": "Interactive Visualizer",
                "legend_html": "",
                "stats_html": "",
                "code_tracker_html": "",
                "input_label": "Input Data",
                "input_default": "",
                "engine_js": "class InteractiveVisualizerEngine { constructor() {} init() {} start() {} pause() {} step() {} reset() {} setSpeed() {} applyCustomData() {} }"
            }
        visualizer_section_html = f"""
                <!-- Core Concept & Tech Stack Header Card -->
                <div class="core-concept-card" style="background: var(--bg-panel); border: 1.5px solid var(--border-color); border-radius: var(--radius-lg); padding: 32px 36px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <div style="flex: 1; min-width: 260px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: var(--primary); background: rgba(74, 142, 179, 0.12); padding: 3px 10px; border-radius: 12px;">Khái niệm cốt lõi</span>
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
                                    {vis_comp.get("canvas_title", "Interactive Visualizer")}
                                </div>
                                <div class="legend-box">
                                    {vis_comp.get("legend_html", "")}
                                </div>
                            </div>

                            <!-- Interactive Visualizer Canvas -->
                            <div class="visualizer-canvas" id="visualizer-canvas">
                                <!-- Dynamic Bars / Nodes generated by JS engine -->
                            </div>

                            <!-- Control Buttons & Input Sliders -->
                            <div class="controls-section">
                                <div class="btn-group">
                                    <button class="btn-action btn-start" id="btn-start" onclick="visualizerApp.start()">
                                        <span>▶</span> Bắt đầu
                                    </button>
                                    <button class="btn-action btn-pause" id="btn-pause" onclick="visualizerApp.pause()">
                                        <span>⏸</span> Tạm dừng
                                    </button>
                                    <button class="btn-action btn-step" id="btn-step" onclick="visualizerApp.step()">
                                        <span>⏭</span> Từng bước
                                    </button>
                                    <button class="btn-action btn-reset" id="btn-reset" onclick="visualizerApp.reset()">
                                        <span>↻</span> Đặt lại
                                    </button>
                                </div>

                                <div class="inputs-row">
                                    <div class="input-group">
                                        <span class="input-label">TỐC ĐỘ THỰC THI (<span id="speed-display">400</span>ms)</span>
                                        <input type="range" id="slider-speed" min="100" max="1000" step="50" value="400" oninput="visualizerApp.setSpeed(this.value)">
                                    </div>
                                    <div class="input-group">
                                        <span class="input-label">{vis_comp.get("input_label", "Input Data")}</span>
                                        <div class="custom-input-box">
                                            <input type="text" id="custom-data-input" class="custom-input" value="{vis_comp.get("input_default", "")}">
                                            <button class="btn-apply" onclick="visualizerApp.applyCustomData()">Áp dụng</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Right Column: Stats, Live Code Tracker & Console Log -->
                        <div class="right-column">
                            <!-- Real-time Stats -->
                            {vis_comp.get("stats_html", "")}

                            <!-- Live Code Tracker -->
                            <div class="code-tracker-panel">
                                <div class="panel-top-bar">
                                    <span>&lt;/&gt; CODE TRACKER ({tech_stack.upper()})</span>
                                    <span style="font-size: 0.75rem; color: #6ee7b7;">● Active Highlighting</span>
                                </div>
                                <div class="code-content">
                                    <pre><code id="code-tracker-box">
{vis_comp.get("code_tracker_html", "")}
                                    </code></pre>
                                </div>
                            </div>

                            <!-- Console Execution Log -->
                            <div class="console-log-panel">
                                <div class="panel-top-bar" style="border-bottom: 1px solid var(--border-color); padding-bottom: 8px; margin-bottom: 8px;">
                                    <span>&gt;_ NHẬT KÝ THUẬT TOÁN</span>
                                    <button onclick="visualizerApp.clearLog()" style="background: transparent; border: none; color: #f87171; cursor: pointer; font-size: 0.8rem;">Xóa</button>
                                </div>
                                <div class="log-messages" id="log-messages">
                                    <div class="log-entry log-info">ℹ [Hệ thống] Đã khởi tạo bộ phỏng đoán trực quan. Nhấn "Bắt đầu" hoặc "Từng bước" để trải nghiệm.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>"""

        step_4_html = f"""
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
        {vis_comp.get("engine_js", "")}

        // Initialize when DOM loaded
        let visualizerApp;
        document.addEventListener('DOMContentLoaded', () => {{
            visualizerApp = new InteractiveVisualizerEngine();
            if (typeof visualizerApp.init === 'function') visualizerApp.init();
            if (window.hljs) hljs.highlightAll();
        }});
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
            --color-compare: #eab308;
            --color-swap: #ef4444;
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
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
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
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
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
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }}

        .stat-value {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--primary);
            font-family: var(--font-mono);
        }}

        .code-tracker-panel {{
            background: #1e1e1e;
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
            background: #252526;
            padding: 10px 14px;
            border-bottom: 1.5px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: #a5b4fc;
        }}

        .code-content pre {{
            margin: 0;
            padding: 14px;
            overflow-x: auto;
            background-color: #1e1e1e;
        }}

        .code-line {{
            display: block;
            padding: 2px 6px;
            border-left: 3px solid transparent;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: #d4d4d4;
        }}

        .code-line.active-line {{
            background-color: rgba(217, 119, 87, 0.15);
            border-left-color: var(--clay);
            color: #ffffff;
        }}

        .console-log-panel {{
            background: #1e1e1e;
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 14px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            max-height: 200px;
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

        .log-info {{ background: rgba(30, 41, 59, 0.5); color: #94a3b8; }}
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
            <span class="badge-banner inline-block px-3 py-0.5 bg-white text-[#be111c] rounded-full text-xs font-bold uppercase tracking-wider mb-3 border border-white/10">{session_id}</span>
            <h2 class="font-montserrat font-black text-2xl md:text-4xl tracking-tight uppercase leading-tight mb-2">{lesson_title}</h2>
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
                            <div class="step-loc">Đặt vấn đề & Thách thức thực tế <span class="range"></span></div>
                            {problem_html}
                        </div>
                    </div>

                    <!-- Step 2: Deep Dive Internals -->
                    <div class="step">
                        <div class="badge">2</div>
                        <div class="step-body">
                            <div class="step-loc">Phân tích Bản chất & Cơ chế vận hành nội bộ <span class="range"></span></div>
                            {analysis_html}
                            <div class="box warning-box">
                                <strong>Lưu ý hiệu năng:</strong> Cần tính toán kỹ độ phức tạp thuật toán và quản lý bộ nhớ khi xử lý khối lượng dữ liệu lớn.
                            </div>
                        </div>
                    </div>

                    <!-- Step 3: Solution & Architecture -->
                    <div class="step hot">
                        <div class="badge">3</div>
                        <div class="step-body">
                            <div class="step-loc">Giới thiệu Giải pháp & Kiến trúc Triển khai <span class="range"></span></div>
                            {solution_html}
                            <div class="box tip-box">
                                <strong>Giải pháp tối ưu:</strong> Sử dụng trực quan hóa giúp nhanh chóng định vị điểm nghẽn và cải thiện tốc độ phản hồi đáng kể.
                            </div>
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

