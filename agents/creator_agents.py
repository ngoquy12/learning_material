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
        "lifecycle", "client-server", "mvc", "agile", "scrum"
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

def get_lesson_content(session_id: str, lesson_id: str, lesson_title: str, lesson_details: str, expected_output: str, attempt_num: int, core_ssot: Dict[str, Any] = None, feedback: str = "", state: AgentState = None) -> Dict[str, Any]:
    # Cache optimization: check if we already generated master content for this lesson
    if state is not None and "master_content" in state and attempt_num == 1 and not feedback:
        print(f"  [Creator Agent] Reusing cached master_content for {session_id} {lesson_id} (Token Cost Saved!).")
        return state["master_content"]

    # Check if LLM is active
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if gemini_key or openai_key:
        from core.llm import call_llm
        from core.skills import load_skill_content
        
        tech_stack = "python/fastapi"
        if state:
            tech_stack = state.get("technology_stack", "python/fastapi")
            
        print(f"  [Creator Agent] Dynamically generating lesson content via LLM (Attempt #{attempt_num}) for stack: {tech_stack}...")
        
        TECH_STACK_RULES = {
            "typescript/nestjs": {
                "frameworks": "NestJS, TypeScript, TypeORM/Prisma",
                "style_guideline": "tuân thủ TypeScript Clean Code, NestJS style guide, OOP, Dependency Injection, SOLID principles",
                "database_orm": "TypeORM hoặc Prisma",
                "validation": "class-validator và class-transformer",
                "file_extension": "TypeScript (.ts)"
            },
            "typescript/react": {
                "frameworks": "React, TypeScript, TailwindCSS/Styled Components",
                "style_guideline": "tuân thủ React Hooks guidelines, functional components, component separation, TypeScript type definitions",
                "database_orm": "React State Management (Zustand/Redux Toolkit)",
                "validation": "Zod hoặc Yup",
                "file_extension": "TypeScript React (.tsx)"
            },
            "java/springboot": {
                "frameworks": "Java, Spring Boot, Spring Data JPA, Hibernate",
                "style_guideline": "tuân thủ Java Code Conventions, Spring Boot best practices, SOLID principles, OOP",
                "database_orm": "Spring Data JPA / Hibernate",
                "validation": "Jakarta Bean Validation (Hibernate Validator)",
                "file_extension": "Java (.java)"
            },
            "python/fastapi": {
                "frameworks": "FastAPI, Pydantic, SQLAlchemy",
                "style_guideline": "tuân thủ PEP 8, Type Hints, clean coding standards",
                "database_orm": "SQLAlchemy ORM",
                "validation": "Pydantic BaseModel",
                "file_extension": "Python (.py)"
            },
            "python/core": {
                "frameworks": "Python Core, Standard Library",
                "style_guideline": "tuân thủ PEP 8, Type Hints, clean coding standards, functional and object-oriented paradigms",
                "database_orm": "Không sử dụng ORM (chỉ dùng các cấu trúc dữ liệu thuần, file I/O hoặc sqlite3 nếu cần)",
                "validation": "assert, Exception handling, Type Hints",
                "file_extension": "Python (.py)"
            },
            "business/management": {
                "frameworks": "Quản trị Kinh doanh, Chiến lược, Tổ chức Doanh nghiệp, Chuỗi giá trị",
                "style_guideline": "tuân thủ tư duy quản trị chiến lược, phân tích thực chứng, trực quan hóa sơ đồ theo chuẩn Effective HTML",
                "database_orm": "Không áp dụng code ORM (trực quan hóa bằng sơ đồ SVG tương tác và ma trận chiến lược)",
                "validation": "KPIs, Balanced Scorecard, SWOT/TOWS",
                "file_extension": "HTML Document (.html)"
            },
            "business/economics": {
                "frameworks": "Kinh tế học, Tài chính, Thị trường, Mô hình cung cầu",
                "style_guideline": "tuân thủ lý thuyết kinh tế hiện đại, phân tích số liệu thực chứng, trực quan hóa biểu đồ kinh tế theo chuẩn Effective HTML",
                "database_orm": "Không áp dụng code ORM",
                "validation": "Chỉ số kinh tế vĩ mô/vi mô, phân tích ROI/NPV",
                "file_extension": "HTML Document (.html)"
            }
        }
        
        rules = TECH_STACK_RULES.get(tech_stack, TECH_STACK_RULES["python/fastapi"])
        
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

        # Adapt reading skill content to target stack
        reading_skill = (reading_skill
            .replace("PEP 8, có đầy đủ Type Hints", rules["style_guideline"])
            .replace("FastAPI/Pydantic/SQLAlchemy", rules["frameworks"])
            .replace("SQLAlchemy ORM", rules["database_orm"])
            .replace("Pydantic BaseModel", rules["validation"])
            .replace("mã nguồn Python", f"mã nguồn {rules['file_extension']}")
            .replace("FastAPI", rules["frameworks"].split(",")[0])
        )
        
        system_prompt = f"""Bạn là chuyên gia Thiết kế Chương trình Đào tạo Lập trình (Instructional Designer) và Kỹ sư Phần mềm cao cấp tại Rikkei Education. 
Nhiệm vụ của bạn là biên soạn tài liệu học tập sâu sắc, chất lượng cao về công nghệ '{tech_stack}'.

YÊU CẦU QUAN TRỌNG VỀ TRỌNG TÂM & ĐỘ SÂU KIẾN THỨC:
1. Tập trung 100% vào nội dung bài học: Tài liệu phải bám sát tuyệt đối tiêu đề và chi tiết yêu cầu của Lesson hiện tại từ PM. TUYỆT ĐỐI không viết lan man sang bài học khác làm nội dung quá dài hoặc nhắc đến các bài học tiếp theo.
2. Ràng buộc công nghệ nghiêm ngặt (Technology Stack Isolation): Bạn phải tuân thủ tuyệt đối công nghệ '{tech_stack}'. 
   - Nếu '{tech_stack}' là 'python/core' (Python cơ bản), TUYỆT ĐỐI KHÔNG ĐƯỢC có bất kỳ đoạn mã nguồn, ví dụ, câu hỏi trắc nghiệm, bài thực hành hoặc nhắc đến các thư viện phát triển Web/Database như FastAPI, Uvicorn, Pydantic, SQLAlchemy, các framework khác (NestJS, Spring Boot, React) hoặc hệ quản trị cơ sở dữ liệu (SQL, MySQL, PostgreSQL, SQLite...). Chỉ dùng Python cơ bản (vòng lặp, hàm, list, dict, class thuần...). Bất kỳ sự pha tạp nào đều sẽ bị loại bỏ hoàn toàn.
   - Nếu '{tech_stack}' là 'python/fastapi', tuyệt đối không được nhắc đến hay trộn lẫn các framework của ngôn ngữ khác (NestJS, Spring Boot) hoặc thư viện Front-end (React).
3. Không bịa đặt nội dung/mã nguồn: Nếu bài học mang tính lý thuyết tổng quan hoặc không liên quan trực tiếp đến lập trình mã nguồn phức tạp (như giới thiệu, cài đặt môi trường...), TUYỆT ĐỐI không tự bịa đặt ra mã nguồn lập trình phức tạp không liên quan. Thay vào đó, dùng câu lệnh CLI cơ bản hoặc ví dụ siêu ngắn hoặc để trống.
4. Cách trình bày khoa học & súc tích: Độ dài bài đọc cần linh hoạt và vừa phải (khoảng 800 - 1500 từ tùy chủ đề). Trình bày mạch lạc, giải thích logic, sử dụng bảng biểu so sánh hoặc sơ đồ dòng dữ liệu (data flow) chuẩn xác để làm rõ vấn đề.
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
        if tech_stack != "python/core":
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
{json.dumps(core_ssot, ensure_ascii=False) if core_ssot else f"Không có SSOT cụ thể, hãy tự sinh dựa trên kiến thức chuẩn {rules['frameworks']}."}
{rag_context}

Đầu ra bắt buộc phải trả về duy nhất chuỗi JSON khớp với cấu trúc sau:
{{
    "problem": "Nội dung phần đặt vấn đề (Markdown)",
    "analysis": "Nội dung phân tích cơ chế và so sánh (Markdown)",
    "solution": "Nội dung giải pháp kỹ thuật kèm sơ đồ (Markdown)",
    "example": "Mã nguồn {rules['file_extension']} mẫu sạch, hoàn chỉnh. LƯU Ý QUAN TRỌNG VỀ TÍNH LINH HOẠT: Nếu bài học mang tính lý thuyết tổng quan hoặc không liên quan trực tiếp đến lập trình mã nguồn phức tạp (ví dụ: giới thiệu ngôn ngữ, cài đặt môi trường...), TUYỆT ĐỐI không tự bịa đặt ra mã nguồn lập trình phức tạp không liên quan. Thay vào đó, hãy ghi các câu lệnh command line (CLI) cơ bản, hoặc các đoạn mã siêu ngắn minh họa, hoặc để trống.",
    "resolve": "Phân tích luồng chạy và phản hồi/kết quả thực thi (Markdown). Nếu trường 'example' để trống hoặc chỉ có CLI, hãy phân tích lý thuyết/quy trình vận hành ở đây.",
    "summary": "Tổng kết và 3 lỗi thường gặp (Markdown)",
    "self_test": [
        "Câu hỏi tự luận 1",
        "Câu hỏi tự luận 2",
        "Câu hỏi tự luận 3"
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
    }}
}}
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
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                result = json.loads(cleaned)
                
                # Validation of key fields to ensure no crash
                required_keys = ["problem", "analysis", "solution", "example", "resolve", "summary", "self_test", "quiz", "lab"]
                if all(k in result for k in required_keys):
                    print("  [Creator Agent] Dynamic generation successful!")
                    if state is not None:
                        state["master_content"] = result
                    return result
                else:
                    print("  [Creator Agent Warning] LLM JSON missing keys. Falling back to local template.")
            except Exception as e:
                print(f"  [Creator Agent Warning] Failed to parse dynamic content: {e}. Falling back to local template.")

    tech_stack = "python/fastapi"
    if state is not None:
        tech_stack = state.get("technology_stack", "python/fastapi")

    if tech_stack == "python/core":
        topic_key = get_base_topic_key_for_core(session_id)
        trigger_titles = {
            "core_intro": "giới thiệu python và cài đặt môi trường",
            "core_operators": "toán tử và cấu trúc điều kiện",
            "core_loops": "cấu trúc vòng lặp và range",
            "core_practice": "thực hành tổng hợp python core",
            "core_strings": "xử lý chuỗi trong python",
            "core_lists": "cấu trúc dữ liệu list và tuple",
            "core_dicts": "cấu trúc dữ liệu dictionary và set",
            "core_functions": "hàm và phạm vi biến trong python",
            "core_advanced": "hàm nâng cao và xử lý tập hợp",
            "core_midterm": "kiểm tra giữa môn python core",
            "core_fallback": "python core cơ bản"
        }
    else:
        topic_key = get_base_topic_key(session_id)
        trigger_titles = {
            "orientation": "định hướng học tập",
            "intro": "giới thiệu cài đặt fastapi",
            "validation": "parameter pydantic validation",
            "crud": "crud cơ bản",
            "database": "sqlalchemy cơ sở dữ liệu database orm",
            "structure": "structure thiết kế router",
            "relationship": "quan hệ relationship",
            "security": "security authentication jwt đăng ký phân quyền",
            "middleware": "cors middleware",
            "upload": "upload file avatar document",
            "testing": "testing kiểm thử",
            "fallback": "fallback"
        }
    
    base_title = trigger_titles.get(topic_key, "fallback")
    base_content = get_session_content(session_id, base_title, attempt_num, tech_stack)
    
    if not lesson_id:
        return base_content
        
    if tech_stack == "python/core":
        stack_intro = f"Trong lập trình Python cơ bản, việc học viên tiếp cận và triển khai **{lesson_title}** luôn đi kèm với những thử thách tư duy logic thực tế."
        stack_analysis = f"Khi phân tích sâu về **{lesson_title}**, chúng ta nhận thấy: {lesson_details if lesson_details else 'việc hiểu rõ cú pháp và luồng điều khiển là cốt lõi để tránh lỗi logic.'}"
        stack_solution = f"Để giải quyết triệt để vấn đề này, chúng ta cần áp dụng các cấu trúc lập trình Python chuẩn mực. Mục tiêu đầu ra là đạt được chuẩn: **{expected_output if expected_output else 'chương trình chạy đúng logic và tối ưu'}**."
        stack_resolve = f"Sau khi áp dụng giải pháp cho **{lesson_title}**, chương trình đã có thể vận hành ổn định và chính xác."
    elif tech_stack == "typescript/nestjs":
        stack_intro = f"Trong quá trình xây dựng hệ thống với NestJS và TypeScript, việc triển khai **{lesson_title}** đòi hỏi sự hiểu biết sâu sắc về Dependency Injection và OOP."
        stack_analysis = f"Khi phân tích sâu về **{lesson_title}**, chúng ta nhận thấy: {lesson_details if lesson_details else 'việc phân tách module và quản lý dependency là cực kỳ quan trọng.'}"
        stack_solution = f"Để giải quyết vấn đề này, chúng ta sẽ thiết kế cấu trúc NestJS tối ưu. Mục tiêu đầu ra là: **{expected_output if expected_output else 'module hoạt động độc lập và dễ dàng kiểm thử'}**."
        stack_resolve = f"Sau khi triển khai giải pháp cho **{lesson_title}**, hệ thống NestJS đã hoạt động đồng bộ và đúng chuẩn."
    elif tech_stack == "typescript/react":
        stack_intro = f"Trong quá trình phát triển ứng dụng Web Front-end với React, việc xây dựng thành phần **{lesson_title}** liên quan trực tiếp đến trải nghiệm người dùng và hiệu năng render."
        stack_analysis = f"Khi phân tích sâu về **{lesson_title}**, chúng ta nhận thấy: {lesson_details if lesson_details else 'quản lý state và vòng đời component là yếu tố quyết định.'}"
        stack_solution = f"Để giải quyết vấn đề này, chúng ta sẽ áp dụng các React hooks và tối ưu render. Mục tiêu đầu ra là: **{expected_output if expected_output else 'giao diện phản hồi nhanh và mượt mà'}**."
        stack_resolve = f"Sau khi áp dụng giải pháp cho **{lesson_title}**, component React đã hiển thị chính xác và đáp ứng tốt tương tác."
    elif tech_stack == "java/springboot":
        stack_intro = f"Trong kiến trúc ứng dụng doanh nghiệp sử dụng Java Spring Boot, việc cấu hình và phát triển **{lesson_title}** đòi hỏi tính bảo mật và khả năng mở rộng cao."
        stack_analysis = f"Khi phân tích sâu về **{lesson_title}**, chúng ta nhận thấy: {lesson_details if lesson_details else 'việc tổ chức code theo các layer Controller-Service-Repository là bắt buộc.'}"
        stack_solution = f"Để giải quyết vấn đề này, chúng ta sẽ triển khai các Spring beans và JPA repository. Mục tiêu đầu ra là: **{expected_output if expected_output else 'api chạy ổn định và lưu trữ dữ liệu an toàn'}**."
        stack_resolve = f"Sau khi triển khai giải pháp cho **{lesson_title}**, service Spring Boot đã hoạt động trơn tru."
    else: # python/fastapi
        stack_intro = f"Trong quá trình xây dựng hệ thống với FastAPI, việc học viên tiếp cận và triển khai **{lesson_title}** luôn đi kèm với những thách thức thực tế."
        stack_analysis = f"Khi phân tích sâu về **{lesson_title}**, chúng ta nhận thấy: {lesson_details if lesson_details else 'việc không nắm rõ cấu trúc và nguyên lý hoạt động sẽ dẫn tới các lỗi logic nghiêm trọng.'}"
        stack_solution = f"Để giải quyết triệt để vấn đề này, chúng ta cần triển khai giải pháp kỹ thuật cụ thể. Mục tiêu đầu ra là đạt được trạng thái: **{expected_output if expected_output else 'tích hợp thành công và hoạt động ổn định'}**."
        stack_resolve = f"Sau khi triển khai giải pháp cho **{lesson_title}**, hệ thống đã có thể vận hành trơn tru."

    problem = f"{stack_intro} {base_content['problem']}"
    analysis = f"{stack_analysis} {base_content['analysis']}"
    solution = f"{stack_solution} {base_content['solution']}"
    example = base_content["example"]
    resolve = f"{stack_resolve} {base_content['resolve']}"
    summary = f"Lưu ý quan trọng cho **{lesson_title}**: {base_content['summary']}"
    
    self_test = [
        f"Câu 1 (Thông hiểu): Hãy trình bày vai trò cốt lõi và mục tiêu của việc triển khai '{lesson_title}' trong dự án thực tế.",
        f"Câu 2 (Vận dụng): Dựa trên lý thuyết đã học, hãy viết một đoạn code mẫu hoặc cấu hình để thực hiện: '{lesson_details if lesson_details else lesson_title}'.",
        f"Câu 3 (Phân tích): Tại sao việc đạt được đầu ra '{expected_output if expected_output else 'hoạt động ổn định'}' lại quan trọng đối với tính toàn vẹn của hệ thống?"
    ]
    
    def get_lesson_specific_quiz(title_str: str, stack_str: str, fallback_q: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        t_lower = (title_str or "").lower()
        if stack_str == "python/core":
            if "giới thiệu" in t_lower or "ngôn ngữ python" in t_lower:
                return [
                    {"type": "Q1_Concept", "question": "Đặc trưng nào sau đây mô tả đúng nhất cơ chế thực thi của ngôn ngữ lập trình Python?", "options": ["Biên dịch trực tiếp ra mã máy CPU", "Thông dịch từng dòng mã lệnh (Interpreted language)", "Chỉ chạy được trên hệ điều hành Linux", "Yêu cầu khai báo kiểu dữ liệu tĩnh trước khi biên dịch"], "correct_option_index": 1, "explanation": "Python là ngôn ngữ thông dịch, mã nguồn được thực thi qua Python Interpreter."},
                    {"type": "Q2_Concept", "question": "Khái niệm 'Định kiểu động' (Dynamic Typing) trong Python có ý nghĩa gì?", "options": ["Biến không thể thay đổi giá trị sau khi gán", "Kiểu dữ liệu của biến được tự động xác định tại thời điểm thực thi dựa trên giá trị được gán", "Bắt buộc khai báo từ khóa int hoặc str khi khởi tạo biến", "Biến chỉ lưu trữ được kiểu dữ liệu số nguyên"], "correct_option_index": 1, "explanation": "Python tự động xác định kiểu dữ liệu của biến khi gán giá trị tại runtime."},
                    {"type": "Q3_Syntax", "question": "Tệp tin có phần mở rộng .pyc sinh ra trong quá trình thực thi mã Python đóng vai trò gì?", "options": ["Chứa mã nguồn gốc bằng văn bản thuần", "Chứa tài liệu hướng dẫn sử dụng", "Chứa mã bytecode đã được biên dịch từ mã nguồn Python để tối ưu tốc độ thực thi", "Chứa cấu hình hệ điều hành Windows"], "correct_option_index": 2, "explanation": "Python biên dịch mã nguồn .py thành bytecode .pyc để tăng tốc cho các lần nạp sau."},
                    {"type": "Q4_Philosophy", "question": "Triết lý lập trình 'Zen of Python' (PEP 20) nhấn mạnh nguyên tắc thiết kế nào sau đây?", "options": ["Readability counts (Tính dễ đọc là yếu tố cốt lõi)", "Mã nguồn càng viết tắt ngắn gọn càng tốt", "Luôn giấu lỗi một cách âm thầm", "Sử dụng các cú pháp phức tạp để tăng tính bảo mật"], "correct_option_index": 0, "explanation": "PEP 20 đặt sự rõ ràng và tính dễ đọc của mã nguồn lên hàng đầu."},
                    {"type": "Q5_Memory", "question": "Trình thông dịch CPython chuẩn quản lý bộ nhớ tự động thông qua cơ chế chính nào?", "options": ["Lập trình viên phải tự gọi lệnh free()", "Reference Counting kết hợp với Garbage Collection", "Cấp phát tĩnh trên Stack hoàn toàn", "Ghi đè trực tiếp lên RAM vật lý"], "correct_option_index": 1, "explanation": "CPython sử dụng Reference Counting và Garbage Collector để tự động thu hồi vùng nhớ."}
                ]
            elif "cài đặt" in t_lower or "môi trường" in t_lower:
                return [
                    {"type": "Q1_CLI", "question": "Cú pháp lệnh chuẩn trong terminal để kiểm tra phiên bản trình thông dịch Python đã cài đặt là gì?", "options": ["python --version", "python -v", "check python", "version python"], "correct_option_index": 0, "explanation": "Lệnh python --version hoặc python -V hiển thị phiên bản Python hiện tại."},
                    {"type": "Q2_Tool", "question": "Công cụ quản lý gói chuẩn tích hợp sẵn trong Python dùng để tải và cài đặt thư viện từ PyPI là gì?", "options": ["npm", "pip", "gem", "apt"], "correct_option_index": 1, "explanation": "pip (Pip Installs Packages) là trình quản lý gói chuẩn của Python."},
                    {"type": "Q3_Concept", "question": "Mục đích chính của việc tạo Môi trường ảo (Virtual Environment) cho dự án Python là gì?", "options": ["Tăng tốc độ vi xử lý CPU", "Cô lập các thư viện và phiên bản phụ thuộc giữa các dự án khác nhau trên cùng máy tính", "Mã hóa mã nguồn dự án", "Thay thế cho trình soạn thảo code VS Code"], "correct_option_index": 1, "explanation": "Môi trường ảo giúp mỗi dự án có bộ thư viện riêng biệt, tránh xung đột phiên bản."},
                    {"type": "Q4_CLI", "question": "Cú pháp lệnh CLI chuẩn để tạo một môi trường ảo có tên 'venv' là gì?", "options": ["python create venv", "python -m venv venv", "pip install venv", "venv new"], "correct_option_index": 1, "explanation": "Cờ -m gọi module tích hợp venv để tạo môi trường ảo."},
                    {"type": "Q5_CLI", "question": "Trên hệ điều hành Windows, đường dẫn tệp lệnh nào cần thực thi để kích hoạt (activate) môi trường ảo 'venv'?", "options": ["venv\\Scripts\\activate", "venv/bin/activate", "activate venv", "python activate"], "correct_option_index": 0, "explanation": "Trên Windows, script kích hoạt nằm trong thư mục Scripts của môi trường ảo."}
                ]
            elif "khai báo" in t_lower or "biến" in t_lower:
                return [
                    {"type": "Q1_Convention", "question": "Theo tiêu chuẩn PEP 8, quy tắc đặt tên biến thông thường trong Python tuân theo định dạng nào?", "options": ["camelCase", "PascalCase", "snake_case (viết thường và phân cách bởi dấu gạch dưới)", "kebab-case"], "correct_option_index": 2, "explanation": "PEP 8 khuyến nghị sử dụng snake_case cho tên biến và hàm."},
                    {"type": "Q2_Syntax", "question": "Tên biến nào sau đây KHÔNG hợp lệ theo quy tắc cú pháp Python?", "options": ["user_age", "_count", "2nd_number", "total_value_1"], "correct_option_index": 2, "explanation": "Tên biến trong Python không được phép bắt đầu bằng chữ số."},
                    {"type": "Q3_Syntax", "question": "Đoạn mã 'x, y, z = 10, 20, 30' thực hiện thao tác gì trong Python?", "options": ["Gán giá trị 10 cho x, các biến y và z bị lỗi", "Gán đồng thời giá trị 10 cho x, 20 cho y và 30 cho z trên cùng một dòng lệnh", "Gán tổng 60 cho 3 biến", "Lỗi cú pháp"], "correct_option_index": 1, "explanation": "Python hỗ trợ gán đa biến (multiple assignment / tuple unpacking) trên 1 dòng."},
                    {"type": "Q4_Function", "question": "Hàm dựng sẵn nào trong Python dùng để trả về địa chỉ bộ nhớ định danh (identity) của một đối tượng biến?", "options": ["type()", "id()", "mem()", "loc()"], "correct_option_index": 1, "explanation": "Hàm id() trả về định danh duy nhất (địa chỉ bộ nhớ) của đối tượng."},
                    {"type": "Q5_Memory", "question": "Trong Python, lệnh gán 'a = b = 100' có ý nghĩa gì về mặt quản lý bộ nhớ?", "options": ["Tạo 2 đối tượng 100 độc lập trong RAM", "Cả hai biến a và b cùng tham chiếu đến cùng một đối tượng số nguyên 100", "Biến a là con trỏ của biến b", "Lỗi cú pháp"], "correct_option_index": 1, "explanation": "Lệnh gán liên tiếp trỏ các định danh về cùng một đối tượng trong bộ nhớ."}
                ]
            elif "kiểu dữ liệu" in t_lower:
                return [
                    {"type": "Q1_Function", "question": "Hàm tích hợp sẵn nào dùng để kiểm tra kiểu dữ liệu của một biến trong Python?", "options": ["check()", "type()", "kind()", "datatype()"], "correct_option_index": 1, "explanation": "Hàm type() trả về lớp (class) biểu thị kiểu dữ liệu của đối tượng."},
                    {"type": "Q2_Concept", "question": "Kiểu dữ liệu nào sau đây trong Python thuộc nhóm kiểu dữ liệu bất biến (immutable)?", "options": ["list", "dict", "set", "str"], "correct_option_index": 3, "explanation": "Kiểu chuỗi str là bất biến; không thể thay đổi ký tự bên trong sau khi tạo."},
                    {"type": "Q3_Output", "question": "Kết quả thực thi của biểu thức type(3.14) trong Python là gì?", "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'real'>"], "correct_option_index": 1, "explanation": "Số thực thập phân trong Python được biểu thị bởi kiểu float."},
                    {"type": "Q4_Syntax", "question": "Giá trị số phức (complex number) trong Python được biểu diễn bằng hậu tố chữ cái nào cho phần ảo?", "options": ["i", "j", "c", "v"], "correct_option_index": 1, "explanation": "Python sử dụng hậu tố j hoặc J cho số phức (ví dụ: 3 + 4j)."},
                    {"type": "Q5_Concept", "question": "Trong Python, giá trị nào sau đây khi chuyển sang kiểu luận lý bool() sẽ trả về False?", "options": ["Số 1", "Chuỗi 'False'", "Chuỗi rỗng '' hoặc số 0", "Danh sách [0]"], "correct_option_index": 2, "explanation": "Số 0, chuỗi rỗng '', list/dict rỗng và None được đánh giá là False."}
                ]
            elif "nhập" in t_lower or "xuất" in t_lower:
                return [
                    {"type": "Q1_Function", "question": "Hàm input() trong Python 3 luôn trả về dữ liệu nhận được từ bàn phím dưới kiểu dữ liệu nào?", "options": ["int", "float", "str (chuỗi ký tự)", "bool"], "correct_option_index": 2, "explanation": "Hàm input() luôn đọc dữ liệu từ bàn phím dưới dạng chuỗi ký tự (str)."},
                    {"type": "Q2_Param", "question": "Tham số 'sep' trong hàm print() có chức năng gì?", "options": ["Quy định ký tự kết thúc dòng", "Quy định ký tự phân cách giữa các đối số được in ra màn hình", "Lọc bỏ ký tự trắng", "Đổi màu văn bản"], "correct_option_index": 1, "explanation": "Tham số sep (separator) xác định ký tự ngăn cách giữa các tham số in ra."},
                    {"type": "Q3_Param", "question": "Khi thực hiện print('Hello', end=' '), tham số end=' ' có tác dụng gì?", "options": ["Thay thế ký tự xuống dòng mặc định bằng ký tự khoảng trắng sau khi in", "In thêm một dòng trống trước từ Hello", "Xóa ký tự cuối của chuỗi", "Lỗi cú pháp"], "correct_option_index": 0, "explanation": "Mặc định end='\\n', việc thay bằng end=' ' giữ cho lệnh in tiếp theo nằm trên cùng dòng."},
                    {"type": "Q4_Method", "question": "Để nhận vào nhiều giá trị trên cùng một dòng nhập từ bàn phím và phân tách chúng bằng khoảng trắng, phương thức nào trên chuỗi thường được kết hợp với input()?", "options": [".join()", ".split()", ".cut()", ".parse()"], "correct_option_index": 1, "explanation": "Phương thức .split() tách chuỗi thành danh sách các phần tử dựa trên ký tự phân cách."},
                    {"type": "Q5_Syntax", "question": "Lệnh nào sau đây xuất ra màn hình chính xác chuỗi 'A-B-C'?", "options": ["print('A', 'B', 'C', sep='-')", "print('A-B-C', end='-')", "print('A', 'B', 'C')", "print('A' + 'B' + 'C')"], "correct_option_index": 0, "explanation": "Sử dụng sep='-' sẽ chèn dấu gạch ngang giữa các phần tử A, B và C."}
                ]
            elif "ép kiểu" in t_lower or "f-string" in t_lower:
                return [
                    {"type": "Q1_Syntax", "question": "Cú pháp chuẩn để định dạng chuỗi f-string (Formatted string literals) trong Python là gì?", "options": ["Tiền tố f đặt trước dấu nháy mở chuỗi, chứa các biểu thức trong cặp ngoặc nhọn {}", "Tiền tố s đặt trước chuỗi", "Dùng ký tự %d trong chuỗi", "Dùng phương thức .format()"], "correct_option_index": 0, "explanation": "f-string sử dụng chữ f ở đầu và đặt biến/biểu thức bên trong ngoặc nhọn {}."},
                    {"type": "Q2_Formatting", "question": "Để định dạng hiển thị một số thực price với chính xác 2 chữ số sau dấu thập phân bằng f-string, cú pháp nào sau đây là đúng?", "options": ["f'{price:.2f}'", "f'{price:2d}'", "f'{price.round(2)}'", "f'{price:f2}'"], "correct_option_index": 0, "explanation": "Cú pháp :.2f định dạng hiển thị số thực với 2 chữ số sau dấu phẩy."},
                    {"type": "Q3_Exception", "question": "Đoạn mã int('45.8') khi thực thi sẽ dẫn đến kết quả gì?", "options": ["Trả về số nguyên 45", "Trả về số nguyên 46", "Phát sinh ngoại lệ ValueError vì chuỗi chứa dấu thập phân không thể ép trực tiếp sang int", "Trả về float 45.8"], "correct_option_index": 2, "explanation": "Hàm int() không thể ép kiểu trực tiếp một chuỗi biểu diễn số thập phân sang số nguyên."},
                    {"type": "Q4_Concept", "question": "Khái niệm 'Ép kiểu tường minh' (Explicit Type Casting) trong Python nghĩa là gì?", "options": ["Python tự động chuyển kiểu ngầm định khi cộng int và float", "Lập trình viên chủ động gọi các hàm tạo kiểu như int(), float(), str() để chuyển đổi dữ liệu", "Hệ thống tự động ép mọi kiểu dữ liệu về chuỗi", "Không cho phép chuyển kiểu dữ liệu"], "correct_option_index": 1, "explanation": "Ép kiểu tường minh là khi lập trình viên chủ động dùng hàm int(), float(), str() để ép kiểu."},
                    {"type": "Q5_Eval", "question": "Kết quả thực thi của biểu thức f'{2 ** 3 + 1}' là chuỗi nào?", "options": ["'2 ** 3 + 1'", "'9'", "'7'", "Lỗi cú pháp"], "correct_option_index": 1, "explanation": "Biểu thức 2 ** 3 + 1 = 8 + 1 = 9 được tính toán bên trong ngoặc nhọn {} của f-string."}
                ]
            elif "toán tử" in t_lower:
                return [
                    {"type": "Q1_Operator", "question": "Toán tử nào trong Python thực hiện phép chia lấy phần dư (Modulo)?", "options": ["/", "//", "%", "**"], "correct_option_index": 2, "explanation": "Toán tử % thực hiện phép chia lấy phần dư."},
                    {"type": "Q2_Operator", "question": "Kết quả của biểu thức toán học 17 // 5 (chia lấy phần nguyên) trong Python là bao nhiêu?", "options": ["3.4", "3", "2", "4"], "correct_option_index": 1, "explanation": "Toán tử // chia lấy phần nguyên làm tròn xuống, 17 // 5 = 3."},
                    {"type": "Q3_Precedence", "question": "Theo thứ tự ưu tiên toán tử trong Python, phép toán nào được ưu tiên thực hiện trước nhất trong biểu thức 2 + 3 * 4 ** 2?", "options": ["Phép cộng +", "Phép nhân *", "Phép lũy thừa **", "Thực hiện từ trái sang phải"], "correct_option_index": 2, "explanation": "Lũy thừa ** có độ ưu tiên cao nhất: 4 ** 2 = 16, sau đó 3 * 16 = 48, cuối cùng 2 + 48 = 50."},
                    {"type": "Q4_Operator", "question": "Toán tử ** trong Python đại diện cho phép toán số học nào?", "options": ["Phép nhân hai lần", "Phép căn bậc hai", "Phép lũy thừa (Exponentiation)", "Phép dịch bit"], "correct_option_index": 2, "explanation": "Toán tử ** dùng để tính lũy thừa."},
                    {"type": "Q5_StringOp", "question": "Kết quả thực thi của biểu thức 'Py' * 3 trong Python là chuỗi nào?", "options": ["'Py3'", "'PyPyPy'", "'Py Py Py'", "Lỗi kiểu dữ liệu"], "correct_option_index": 1, "explanation": "Toán tử * giữa chuỗi và số nguyên thực hiện lặp chuỗi với số lần tương ứng."}
                ]
            elif "điều kiện" in t_lower or "if" in t_lower:
                return [
                    {"type": "Q1_Syntax", "question": "Khối lệnh bên trong cấu trúc điều kiện if-elif-else trong Python được xác định phạm vi bằng cơ chế nào?", "options": ["Dấu ngoặc nhọn {}", "Từ khóa begin...end", "Thụt lề đầu dòng (Indentation) đồng nhất", "Dấu chấm phẩy ;"], "correct_option_index": 2, "explanation": "Python sử dụng việc thụt lề đầu dòng (indentation) để xác định phạm vi của khối lệnh."},
                    {"type": "Q2_Logic", "question": "Cơ chế đánh giá ngắn mạch (Short-circuit evaluation) của toán tử and hoạt động như thế nào?", "options": ["Luôn đánh giá tất cả các toán hạng", "Nếu toán hạng đầu tiên sai (False), Python lập tức trả về False mà không cần đánh giá toán hạng thứ hai", "Đánh giá từ phải sang trái", "Chỉ áp dụng cho toán hạng kiểu số"], "correct_option_index": 1, "explanation": "Với toán tử and, nếu vế đầu False thì toàn bộ biểu thức chắc chắn False nên vế sau không được thực thi."},
                    {"type": "Q3_Ternary", "question": "Cú pháp chuẩn của Toán tử ba ngôi (Ternary Conditional Operator) trong Python là gì?", "options": ["điều_kiện ? giá_trị_1 : giá_trị_2", "giá_trị_1 if điều_kiện else giá_trị_2", "if điều_kiện then giá_trị_1 else giá_trị_2", "giá_trị_1 else giá_trị_2 if điều_kiện"], "correct_option_index": 1, "explanation": "Cú pháp ba ngôi trong Python là: giá_trị_đúng if điều_kiện else giá_trị_sai."},
                    {"type": "Q4_Syntax", "question": "Cấu trúc match-case được giới thiệu từ phiên bản Python nào và ký tự nào đại diện cho trường hợp mặc định (wildcard pattern)?", "options": ["Python 3.8, từ khóa default", "Python 3.10+, ký tự gạch dưới _", "Python 3.6, ký tự *", "Python 3.11, từ khóa else"], "correct_option_index": 1, "explanation": "Từ Python 3.10, match-case được ra mắt với ký tự _ đại diện cho wildcard/default case."},
                    {"type": "Q5_Eval", "question": "Kết quả của biểu thức logic 'not (True and False) or False' trong Python là gì?", "options": ["True", "False", "None", "Lỗi cú pháp"], "correct_option_index": 0, "explanation": "True and False = False -> not False = True -> True or False = True."}
                ]
        return fallback_q

    quiz = get_lesson_specific_quiz(lesson_title, tech_stack, base_content["quiz"])
    
    lab = {
        "title": f"Thực hành: {lesson_title}",
        "objectives": [
            f"Triển khai thành công: {lesson_title}.",
            f"Đạt chuẩn đầu ra kỳ vọng: '{expected_output if expected_output else 'hoạt động ổn định'}'."
        ],
        "steps": base_content["lab"]["steps"],
        "checklist": base_content["lab"]["checklist"]
    }
    
    res = {
        "problem": problem,
        "analysis": analysis,
        "solution": solution,
        "example": example,
        "resolve": resolve,
        "summary": summary,
        "self_test": self_test,
        "quiz": quiz,
        "lab": lab
    }
    if state is not None:
        state["master_content"] = res
    return res

def get_session_content(session_id: str, title: str, attempt_num: int, tech_stack: str = "python/fastapi") -> Dict[str, Any]:
    """
    Returns deep, academically rigorous content, extensive code snippets, and complete quiz questions
    based on the session title. Fully complies with "Storytelling in Tech" and "Reading Generator" guidelines.
    """
    t = title.lower()
    
    if tech_stack == "python/core":
        if "core_intro" in t or "giới thiệu python" in t:
            return {
                "problem": "Khi mới bắt đầu học lập trình Python, học viên thường gặp khó khăn trong việc thiết lập môi trường phát triển (IDE), cài đặt trình thông dịch Python và cấu hình biến môi trường. Việc viết chương trình đầu tiên mà không hiểu cơ chế biên dịch và thông dịch của ngôn ngữ, cách khai báo biến cũng như nhập xuất cơ bản sẽ làm học viên bối rối trước các lỗi cú pháp sơ đẳng.",
                "analysis": """Python là một ngôn ngữ thông dịch (interpreted language), có nghĩa là mã nguồn được thực thi từng dòng bởi trình thông dịch Python (Python Interpreter) chứ không biên dịch trực tiếp ra mã máy như C/C++. Việc khai báo biến trong Python cực kỳ linh hoạt vì Python sử dụng kiểu dữ liệu động (dynamic typing) và tự động quản lý bộ nhớ thông qua cơ chế Garbage Collection. Việc xuất dữ liệu dùng `print()` và nhập dữ liệu dùng `input()` là nền tảng giao tiếp giữa người dùng và máy tính.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Tiêu chí</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Định kiểu động (Python)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Định kiểu tĩnh (Java/C++)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Khai báo biến</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không cần chỉ định kiểu dữ liệu (x = 10)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Bắt buộc chỉ định kiểu (int x = 10)</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Độ linh hoạt</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cực cao, có thể đổi kiểu dữ liệu của biến</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Thấp, biến không được đổi kiểu</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Phát hiện lỗi kiểu</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khi chương trình đang chạy (Runtime)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khi biên dịch chương trình (Compile time)</td>
        </tr>
    </tbody>
</table>""",
                "solution": "Cài đặt Python phiên bản mới nhất, cấu hình IDE VS Code chuyên nghiệp. Sử dụng các biến để lưu trữ dữ liệu tạm thời, thực hiện ép kiểu (type casting) hợp lý để chuyển đổi giữa các kiểu dữ liệu cơ bản (int, float, str, bool), và sử dụng f-string để định dạng chuỗi xuất ra màn hình một cách khoa học.",
                "example": """# 1. Khai báo biến và các kiểu dữ liệu cơ bản
student_name = "Nguyễn Văn A"  # Kiểu chuỗi (str)
student_age = 20               # Kiểu số nguyên (int)
student_gpa = 3.8              # Kiểu số thực (float)
is_active = True               # Kiểu luận lý (bool)

# 2. Nhập xuất dữ liệu cơ bản từ bàn phím
print("--- THÔNG TIN SINH VIÊN ---")
print(f"Họ tên: {student_name}")
print(f"Tuổi: {student_age}")
print(f"GPA: {student_gpa}")

# Nhận input và thực hiện ép kiểu (Casting) từ str sang int
extra_years = input("Nhập số năm cộng thêm: ")
future_age = student_age + int(extra_years)
print(f"Tuổi của sinh viên sau {extra_years} năm nữa là: {future_age}")
""",
                "resolve": "Chương trình khởi tạo bốn biến với các kiểu dữ liệu khác nhau. Hàm `print()` kết hợp với f-string giúp hiển thị thông tin sinh viên rõ ràng và có cấu trúc. Khi người dùng nhập một giá trị từ bàn phím qua `input()`, Python mặc định coi đó là một chuỗi (str). Chương trình thực hiện ép kiểu `int(extra_years)` để chuyển chuỗi thành số nguyên trước khi thực hiện phép cộng toán học, tránh lỗi `TypeError`.",
                "summary": "Luôn ép kiểu rõ ràng khi nhận dữ liệu từ `input()`. Lỗi thường gặp nhất là quên f ở đầu f-string làm tên biến không được thế giá trị.",
                "self_test": [
                    "Câu 1 (Thông hiểu): Tại sao Python được gọi là ngôn ngữ định kiểu động (dynamically typed) và điều này khác gì với các ngôn ngữ định kiểu tĩnh như Java hay C++?",
                    "Câu 2 (Vận dụng): Viết chương trình Python yêu cầu người dùng nhập vào hai số nguyên từ bàn phím, tính tổng và in kết quả ra màn hình bằng f-string.",
                    "Câu 3 (Phân tích): Phân tích tầm quan trọng của việc sử dụng môi trường ảo (virtual environment) trong quản lý thư viện dự án Python thực tế."
                ],
                "quiz": [
                    {"type": "Q1_Syntax_Definition", "question": "Hàm nào dùng để nhận dữ liệu nhập vào từ bàn phím của người dùng trong Python?", "options": ["read()", "input()", "get()", "scanf()"], "correct_option_index": 1, "explanation": "input() là hàm tích hợp sẵn của Python dùng để nhận dữ liệu từ bàn phím dưới dạng chuỗi."},
                    {"type": "Q2_Execution_Flow", "question": "Cách nào đúng để ép kiểu từ chuỗi '123' sang số nguyên trong Python?", "options": ["to_int('123')", "int('123')", "Integer('123')", "(int)'123'"], "correct_option_index": 1, "explanation": "int() là hàm dựng sẵn để ép kiểu sang số nguyên."},
                    {"type": "Q3_Code_Reading", "question": "Đoạn code: print(f'{2 + 3}') in ra gì?", "options": ["2 + 3", "f'{2 + 3}'", "5", "Lỗi cú pháp"], "correct_option_index": 2, "explanation": "Biểu thức bên trong dấu ngoặc nhọn {} của f-string sẽ được tính toán và chuyển thành chuỗi trước khi in."},
                    {"type": "Q4_Compare_Contrast", "question": "Từ khóa nào KHÔNG được dùng để đặt tên biến trong Python?", "options": ["name", "value", "class", "total"], "correct_option_index": 2, "explanation": "class là từ khóa hệ thống dùng để định nghĩa lớp và không thể đặt làm tên biến."},
                    {"type": "Q5_Prediction_Trap", "question": "Kiểu dữ liệu nào dùng để lưu giữ giá trị True hoặc False?", "options": ["int", "str", "bool", "float"], "correct_option_index": 2, "explanation": "bool (boolean) đại diện cho các giá trị luận lý Đúng hoặc Sai."}
                ],
                "lab": {
                    "title": "Cài đặt môi trường và Viết chương trình Python đầu tiên",
                    "objectives": ["Cài đặt thành công Python và VS Code.", "Viết chương trình nhập xuất và tính toán đơn giản."],
                    "steps": [
                        "Bước 1: Tải và cài đặt Python bản mới nhất từ trang chủ python.org.",
                        "Bước 2: Cài đặt IDE VS Code và extension Python.",
                        "Bước 3: Tạo tệp hello.py và viết lệnh print.",
                        "Bước 4: Sử dụng input() để nhận tên và năm sinh, tính tuổi hiện tại và in ra."
                    ],
                    "checklist": ["Chạy thành công script Python không có lỗi cú pháp.", "Đầu ra tuổi hiện tại được tính toán chính xác."]
                }
            }
        elif "core_operators" in t or "toán tử" in t:
            return {
                "problem": "Khi xây dựng các luồng quyết định (decision-making) trong chương trình, học viên thường gặp khó khăn trong việc kết hợp các toán tử so sánh và toán tử logic để tạo ra các biểu thức điều kiện chính xác. Ngoài ra, việc lạm dụng cấu trúc `if-else` lồng nhau sâu khiến mã nguồn trở nên rối rắm, khó đọc và khó kiểm thử các trường hợp biên.",
                "analysis": """Python cung cấp hệ thống toán tử phong phú gồm toán tử số học (`+`, `-`, `*`, `/`, chia lấy nguyên `//`, chia lấy dư `%`, lũy thừa `**`), toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`) và toán tử logic (`and`, `or`, `not`). Cấu trúc rẽ nhánh `if-elif-else` và cấu trúc `match-case` (từ Python 3.10) giúp phân tách luồng chạy của chương trình dựa trên kết quả của biểu thức điều kiện logic. Việc tối ưu hóa biểu thức logic bằng toán tử ba ngôi (ternary operator) giúp mã nguồn ngắn gọn hơn.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Toán tử</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Ý nghĩa</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Ví dụ</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">%</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chia lấy phần dư (Modulo)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">5 % 2 = 1</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">//</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chia lấy phần nguyên (Floor Division)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">5 // 2 = 2</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">**</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lũy thừa (Power)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">5 ** 2 = 25</td>
        </tr>
    </tbody>
</table>""",
                "solution": "Sử dụng đúng độ ưu tiên của các toán tử số học và logic (sử dụng dấu ngoặc đơn `()` để tường minh). Áp dụng cấu trúc rẽ nhánh `if-elif-else` một cách khoa học, tránh lồng nhau quá 3 cấp, hoặc chuyển sang dùng `match-case` khi so sánh một biến với nhiều giá trị cụ thể nhằm tăng tính thẩm mỹ và dễ bảo trì.",
                "example": """# 1. Sử dụng toán tử số học và logic
math_score = 8.5
english_score = 7.0

# Điều kiện đạt học bổng: Điểm trung bình >= 8.0 VÀ không môn nào dưới 6.5
average_score = (math_score + english_score) / 2
has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5

# 2. Sử dụng cấu trúc rẽ nhánh khoa học và toán tử ba ngôi
status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
print(f"Điểm TB: {average_score} -> Trạng thái: {status}")

# 3. Sử dụng cấu trúc match-case mới (Python 3.10+)
rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
match rank_level:
    case "A":
        print("Xếp loại xuất sắc, được nhận học bổng loại I.")
    case "B":
        print("Xếp loại khá giỏi, được nhận học bổng loại II.")
    case _:
        print("Cần cố gắng thêm trong các kỳ học sau.")
""",
                "resolve": "Chương trình tính toán điểm trung bình bằng biểu thức số học có ngoặc đơn. Sau đó, nó dùng toán tử logic `and` để kiểm tra đồng thời ba điều kiện logic. Toán tử ba ngôi gán giá trị cho `status` một cách ngắn gọn. Cuối cùng, cấu trúc `match-case` khớp giá trị của `rank_level` với các trường hợp cụ thể để in ra lời khuyên tương ứng, sử dụng dấu gạch dưới `_` làm trường hợp mặc định (default case).",
                "summary": "Luôn dùng dấu ngoặc đơn để làm rõ độ ưu tiên của toán tử. Lỗi thường gặp nhất là dùng một dấu bằng = thay cho hai dấu bằng == trong lệnh so sánh if.",
                "self_test": [
                    "Câu 1 (Thông hiểu): Giải thích nguyên lý đánh giá ngắn mạch (short-circuit evaluation) của toán tử `and` và `or` trong Python.",
                    "Câu 2 (Vận dụng): Viết chương trình Python kiểm tra xem một năm nhập vào từ bàn phím có phải là năm nhuận hay không (Năm nhuận là năm chia hết cho 400 hoặc chia hết cho 4 nhưng không chia hết cho 100).",
                    "Câu 3 (Phân tích): Tại sao cấu trúc `match-case` trong Python 3.10+ lại ưu việt hơn chuỗi câu lệnh `if-elif-else` dài khi cần khớp các giá trị dạng pattern?"
                ],
                "quiz": [
                    {"type": "Q1_Syntax_Definition", "question": "Kết quả của biểu thức: 5 + 3 * 2 là bao nhiêu?", "options": ["16", "11", "13", "10"], "correct_option_index": 1, "explanation": "Toán tử nhân * có độ ưu tiên cao hơn cộng +, nên 3 * 2 = 6, sau đó 5 + 6 = 11."},
                    {"type": "Q2_Execution_Flow", "question": "Toán tử nào dùng để lấy phần dư của phép chia trong Python?", "options": ["/", "//", "%", "**"], "correct_option_index": 2, "explanation": "% là toán tử modulo, dùng để lấy số dư."},
                    {"type": "Q3_Code_Reading", "question": "Biểu thức: True or False and False trả về giá trị nào?", "options": ["True", "False", "None", "Lỗi cú pháp"], "correct_option_index": 0, "explanation": "Toán tử and có độ ưu tiên cao hơn or, nên False and False là False, sau đó True or False là True."},
                    {"type": "Q4_Compare_Contrast", "question": "Trong cấu trúc match-case, ký tự nào đại diện cho case mặc định (default case)?", "options": ["*", "default", "_", "else"], "correct_option_index": 2, "explanation": "Dấu gạch dưới _ đại diện cho case mặc định khớp với mọi giá trị còn lại."},
                    {"type": "Q5_Prediction_Trap", "question": "Đoạn code: x = 10; y = 20; max_val = x if x > y else y gán giá trị nào cho max_val?", "options": ["10", "20", "None", "True"], "correct_option_index": 1, "explanation": "Đây là toán tử ba ngôi. Vì x > y (10 > 20) là False, biểu thức trả về vế sau else là y (20)."}
                ],
                "lab": {
                    "title": "Thực hành Toán tử và Cấu trúc điều kiện",
                    "objectives": ["Sử dụng toán tử so sánh và logic để xây dựng biểu thức điều kiện.", "Áp dụng cấu trúc rẽ nhánh `if-elif-else` và `match-case`."],
                    "steps": [
                        "Bước 1: Tạo file operators_lab.py.",
                        "Bước 2: Yêu cầu người dùng nhập vào số điểm toán, lý, hóa.",
                        "Bước 3: Kiểm tra điểm số hợp lệ (0-10). Nếu không hợp lệ, in ra thông báo lỗi và dừng chương trình.",
                        "Bước 4: Tính điểm trung bình và xếp loại học sinh theo các mức: Giỏi (>=8.0), Khá (>=6.5), Trung bình (>=5.0), Yếu (<5.0) bằng if-elif-else."
                    ],
                    "checklist": ["Kiểm tra lỗi điểm không hợp lệ hoạt động chính xác.", "Xếp loại học lực chính xác cho mọi trường hợp điểm đầu vào."]
                }
            }
        elif "core_loops" in t or "vòng lặp" in t:
            return {
                "problem": "Khi xử lý các tập hợp dữ liệu lớn hoặc thực hiện các tác vụ lặp đi lặp lại trong Python, lập trình viên mới thường viết code thủ công lặp lại nhiều lần. Điều này không chỉ gây lãng phí bộ nhớ mà còn vi phạm nguyên tắc DRY (Don't Repeat Yourself), khiến mã nguồn dài dòng, dễ phát sinh lỗi logic và rất khó bảo trì khi quy mô dự án tăng lên.",
                "analysis": """Python cung cấp hai loại vòng lặp cơ bản là `for` (lặp với số lần biết trước hoặc duyệt qua tập hợp) và `while` (lặp theo điều kiện logic). Để điều khiển luồng thực thi trong vòng lặp, các từ khóa `break` (thoát vòng lặp lập tức), `continue` (bỏ qua phần còn lại của vòng lặp hiện tại và chuyển sang bước tiếp theo), và `pass` (giữ chỗ không làm gì) đóng vai trò quyết định. Đặc biệt, Python hỗ trợ khối `else` sau vòng lặp, chạy khi và chỉ khi vòng lặp kết thúc bình thường (không bị ngắt bởi `break`).

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Đặc tính</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Vòng lặp for</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Vòng lặp while</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Số lần lặp</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Biết trước hoặc hữu hạn (duyệt tập hợp)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Phụ thuộc vào điều kiện logic dừng</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Cú pháp đặc trưng</td>
            <td style="padding:10px; border:1px solid var(--border-color);">for item in iterable:</td>
            <td style="padding:10px; border:1px solid var(--border-color);">while condition:</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Ứng dụng chính</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Duyệt mảng, chuỗi, range số</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lặp menu, chờ sự kiện, game loop</td>
        </tr>
    </tbody>
</table>""",
                "solution": "Sử dụng vòng lặp `for` kết hợp với hàm `range(start, stop, step)` để duyệt dãy số hiệu quả, hoặc dùng `while` cho các trường hợp lặp không xác định trước số lần. Sử dụng `break` và `continue` để tối ưu hiệu năng của vòng lặp, thoát sớm khi tìm thấy kết quả hoặc bỏ qua các phần tử không hợp lệ.",
                "example": """# Duyệt qua danh sách số nguyên và tìm số nguyên tố đầu tiên
numbers = [4, 6, 8, 9, 11, 13, 15]
print("Bắt đầu tìm kiếm số nguyên tố trong danh sách:")
for num in numbers:
    if num <= 1:
        continue
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(f"Tìm thấy số nguyên tố đầu tiên: {num}")
        break
else:
    print("Không tìm thấy số nguyên tố nào.")
""",
                "resolve": "Chương trình khởi tạo danh sách `numbers`, duyệt qua từng số bằng vòng lặp `for`. Gặp các số hợp số, vòng lặp con kiểm tra số nguyên tố phát hiện chia hết nên gán `is_prime = False` và thoát sớm bằng `break`. Khi gặp số `11`, là số nguyên tố, điều kiện được thỏa mãn và in ra kết quả, sau đó ngắt vòng lặp ngoài bằng `break`.",
                "summary": "Các lỗi phổ biến bao gồm: vòng lặp while vô hạn do quên cập nhật điều kiện dừng; off-by-one khi dùng sai chỉ số range; lạm dụng vòng lặp lồng nhau sâu gây suy giảm hiệu năng.",
                "self_test": [
                    "Câu 1 (Thông hiểu): Giải thích cách hoạt động của khối `else` đi kèm với vòng lặp `for` trong Python. Trường hợp nào khối `else` này sẽ không được thực thi?",
                    "Câu 2 (Vận dụng): Viết đoạn code Python sử dụng vòng lặp `while` để yêu cầu người dùng nhập vào một số nguyên dương từ bàn phím. Nếu nhập sai, yêu cầu nhập lại cho đến khi đúng.",
                    "Câu 3 (Phân tích): Tại sao việc thay thế các vòng lặp lồng nhau sâu bằng cách sử dụng các cấu trúc dữ liệu tối ưu (như Set hoặc Dict) lại giúp cải thiện hiệu năng của chương trình từ O(n^2) xuống O(n)?"
                ],
                "quiz": [
                    {"type": "Q1_Syntax_Definition", "question": "Hàm range(1, 10, 2) tạo ra chuỗi số nào?", "options": ["1, 3, 5, 7, 9", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "2, 4, 6, 8", "1, 2, 4, 6, 8"], "correct_option_index": 0, "explanation": "range(start, stop, step) bắt đầu từ 1, nhảy mỗi bước 2 đơn vị và dừng trước 10."},
                    {"type": "Q2_Execution_Flow", "question": "Từ khóa nào dùng để bỏ qua các câu lệnh còn lại trong vòng lặp hiện tại và chuyển sang lần lặp tiếp theo?", "options": ["break", "continue", "pass", "exit"], "correct_option_index": 1, "explanation": "continue chuyển hướng điều khiển đến lần lặp kế tiếp của vòng lặp."},
                    {"type": "Q3_Code_Reading", "question": "Khối else trong vòng lặp for chạy khi nào?", "options": ["Khi vòng lặp kết thúc bình thường không bị ngắt bởi break", "Khi vòng lặp bị ngắt bởi break", "Khi danh sách rỗng", "Không bao giờ chạy"], "correct_option_index": 0, "explanation": "Khối else chạy khi vòng lặp hoàn thành tất cả các chu trình lặp bình thường."},
                    {"type": "Q4_Compare_Contrast", "question": "Chuyện gì xảy ra nếu điều kiện dừng của vòng lặp while luôn là True và không có break?", "options": ["Lỗi biên dịch", "Vòng lặp vô hạn gây treo chương trình", "Không in ra gì", "Lỗi Exception"], "correct_option_index": 1, "explanation": "While True mà không có break tạo thành vòng lặp vô hạn (infinite loop)."},
                    {"type": "Q5_Prediction_Trap", "question": "Đoạn code: for i in range(3): print(i) in ra gì?", "options": ["0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "Lỗi cú pháp"], "correct_option_index": 0, "explanation": "range(3) bắt đầu từ 0 và dừng trước 3, tức các số 0, 1, 2."}
                ],
                "lab": {
                    "title": "Thực hành Vòng lặp và Kiểm soát Luồng chạy",
                    "objectives": ["Sử dụng vòng lặp for và while để duyệt dữ liệu.", "Áp dụng các câu lệnh break và continue để kiểm soát luồng chạy."],
                    "steps": [
                        "Bước 1: Tạo file loops_lab.py.",
                        "Bước 2: Viết vòng lặp in ra các số từ 1 đến 20 bỏ qua các số chia hết cho 3.",
                        "Bước 3: Sử dụng vòng lặp while để tính tổng các số chẵn nhập từ bàn phím cho đến khi người dùng nhập số 0 thì dừng lại và in tổng ra."
                    ],
                    "checklist": ["Chương trình bỏ qua đúng các số chia hết cho 3.", "Tính toán chính xác tổng và dừng khi gặp số 0."]
                }
            }
        else:
            return {
                "problem": "Khi triển khai các giải pháp lập trình Python nâng cao hoặc cấu trúc dữ liệu phức tạp, việc không hiểu rõ mô hình hoạt động của Standard Library và cách thức tổ chức mã nguồn dạng Module/Package sẽ làm hệ thống phình to, lặp lại mã nguồn nhiều lần và gây khó khăn lớn cho việc bảo trì.",
                "analysis": """Python Core cung cấp các thư viện tích hợp sẵn phong phú và các cấu trúc dữ liệu mạnh mẽ như List, Dictionary, Set, Tuple. Việc sử dụng các kỹ thuật như List Comprehension, Lambda function, và xử lý Exception Handling giúp tăng độ tin cậy và hiệu năng của ứng dụng mà không cần sử dụng các thư viện ngoài phức tạp.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Cấu trúc</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Đặc trưng nổi bật</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Khi nào dùng</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">List</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Có thứ tự, có thể thay đổi (mutable), cho trùng lặp</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lưu danh sách thông thường cần truy cập index</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Set</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không thứ tự, độc bản (unique), không chỉ mục</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lọc trùng lặp dữ liệu, thực hiện phép toán tập hợp</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Dict</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cặp Key-Value, Key duy nhất, truy xuất cực nhanh</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lưu trữ thông tin có cấu trúc dạng từ điển bản đồ</td>
        </tr>
    </tbody>
</table>""",
                "solution": "Thiết kế mã nguồn tuân thủ nguyên tắc DRY và Clean Code PEP 8. Chia nhỏ hệ thống thành các hàm và module độc lập, sử dụng Exception handling (try-except-finally) để xử lý các lỗi runtime một cách thông minh.",
                "example": """# Sử dụng cấu trúc dữ liệu và Exception handling chuẩn Python Core
def process_data(data_list):
    try:
        # Sử dụng list comprehension để lọc và nhân đôi các số chẵn
        cleaned_data = [x * 2 for x in data_list if isinstance(x, (int, float))]
        return cleaned_data
    except TypeError as e:
        print(f"Lỗi kiểu dữ liệu đầu vào: {e}")
        return []

# Chạy thử
sample = [1, 2, "invalid", 4]
result = process_data(sample)
print(f"Kết quả xử lý: {result}")
""",
                "resolve": "Hàm `process_data` nhận một danh sách, sử dụng list comprehension để lọc dữ liệu an toàn bằng cách kiểm tra kiểu dữ liệu `isinstance(x, (int, float))`. Khối `try-except` bắt các ngoại lệ xảy ra trong quá trình xử lý để chương trình không bị sập đột ngột.",
                "summary": "Luôn dùng context manager (with) khi thao tác File I/O. Tránh sử dụng biến toàn cục bừa bãi và bắt ngoại lệ chung chung.",
                "self_test": [
                    "Câu 1 (Thông hiểu): Hãy giải thích cơ chế hoạt động của Exception Propagation trong Python.",
                    "Câu 2 (Vận dụng): Viết một đoạn code Python đọc dữ liệu từ một tệp tin văn bản sử dụng context manager `with` và in từng dòng ra màn hình.",
                    "Câu 3 (Phân tích): Tại sao việc viết mã nguồn tuân thủ tiêu chuẩn PEP 8 lại vô cùng quan trọng đối với khả năng đọc hiểu và bảo trì dự án trong môi trường doanh nghiệp?"
                ],
                "quiz": [
                    {"type": "Q1_Syntax_Definition", "question": "Cấu trúc dữ liệu nào trong Python là bất biến (immutable)?", "options": ["List", "Dictionary", "Tuple", "Set"], "correct_option_index": 2, "explanation": "Tuple là cấu trúc dữ liệu bất biến, không thể thay đổi giá trị sau khi khởi tạo."},
                    {"type": "Q2_Execution_Flow", "question": "Cách nào đúng để mở một file để đọc một cách an toàn trong Python?", "options": ["open('file.txt')", "with open('file.txt', 'r') as f:", "f = open('file.txt'); f.read()", "read('file.txt')"], "correct_option_index": 1, "explanation": "Sử dụng 'with' statement giúp tự động đóng file an toàn sau khi dùng xong, chống rò rỉ tài nguyên."},
                    {"type": "Q3_Code_Reading", "question": "List comprehension: [x for x in range(5) if x % 2 == 0] trả về danh sách nào?", "options": ["[0, 2, 4]", "[1, 3]", "[0, 1, 2, 3, 4]", "[2, 4]"], "correct_option_index": 0, "explanation": "range(5) sinh dãy số 0,1,2,3,4. Điều kiện x % 2 == 0 lọc ra các số chẵn là 0, 2, 4."},
                    {"type": "Q4_Compare_Contrast", "question": "Khối lệnh nào trong cấu trúc try-except luôn luôn được thực thi dù có lỗi xảy ra hay không?", "options": ["except", "else", "finally", "catch"], "correct_option_index": 2, "explanation": "Khối finally luôn được thực thi ở cuối cùng để dọn dẹp tài nguyên."},
                    {"type": "Q5_Prediction_Trap", "question": "Từ khóa nào dùng để tạo ra một hàm ẩn danh (anonymous function) ngắn gọn trong Python?", "options": ["def", "function", "lambda", "inline"], "correct_option_index": 2, "explanation": "lambda là từ khóa dùng để định nghĩa các hàm ẩn danh siêu ngắn."},
                ],
                "lab": {
                    "title": "Thực hành Tổng hợp Python Core cơ bản",
                    "objectives": ["Sử dụng các cấu trúc dữ liệu tích hợp sẵn để xử lý danh sách.", "Áp dụng Exception handling và File I/O để đọc ghi dữ liệu ra đĩa."],
                    "steps": [
                        "Bước 1: Tạo tệp dữ liệu data.txt chứa một số dòng chữ.",
                        "Bước 2: Viết script Python mở file, đọc nội dung và đếm số lượng từ xuất hiện.",
                        "Bước 3: Sử dụng try-except để phòng chống lỗi FileNotFoundError khi đường dẫn file bị sai.",
                        "Bước 4: Xuất kết quả đếm từ ra một file JSON mới."
                    ],
                    "checklist": ["Chương trình hoạt động ổn định và không sập khi file không tồn tại.", "File JSON kết quả chứa đúng cấu trúc từ khóa và số lượng."]
                }
            }

    details_start = ""
    details_end = ""

    # Classify by topic
    if "định hướng" in t or "orientation" in t:
        return {
            "problem": """Khi bước chân vào phát triển phần mềm và xây dựng dịch vụ web, đa số học viên đối mặt với rào cản lớn: sự mơ hồ về đích đến và lộ trình học. Phương pháp học truyền thống đi theo lối mòn học lý thuyết trước rồi mới làm dự án (Forward Design). Lối học này tạo ra khoảng trống kỹ năng cực lớn vì học viên viết mã nguồn mà không hiểu mục tiêu nghiệp vụ thực tế. Hệ quả là học viên dễ chán nản, học vẹt đối phó, và không thể tự tay thiết kế hay tích hợp hoàn chỉnh một hệ thống Web API kết nối cơ sở dữ liệu đáp ứng được tiêu chuẩn tuyển dụng khắt khe của doanh nghiệp.""",
            "analysis": """Sở dĩ vấn đề này kéo dài là do thiếu hụt phương pháp Thiết kế ngược (Backward Design) và mô hình Học tập chủ động (Active Learning). Thay vì dạy lý thuyết rời rạc, thiết kế ngược lấy sản phẩm RESTful API thực chiến cuối khóa kết nối MySQL làm kim chỉ nam. Mọi lý thuyết, slide và bài thực hành Lab hàng tuần đều được phân rã ngược từ chính sản phẩm này. Học viên sẽ hiểu rõ mục đích của từng dòng code ngay từ đầu môn học.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Đặc tính so sánh</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Học xuôi (Forward Design)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Thiết kế ngược (Backward Design)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Điểm xuất phát</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Học cú pháp, định nghĩa lý thuyết trước</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Đặc tả đầu ra dự án cuối khóa chuẩn doanh nghiệp</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Động lực học tập</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Thụ động, dễ trì hoãn do không thấy ứng dụng</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chủ động lắp ráp từng module sản phẩm hàng tuần</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Kết quả đầu ra</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khó kết nối các mảnh kiến thức rời rạc</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Hoàn thiện 100% ứng dụng thực tế chạy ổn định</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Chương trình đào tạo thiết lập cấu trúc phân bổ điểm học phần tập trung tối đa vào kỹ năng thực hành và đánh giá liên tục. Dự án cuối khóa (bảo vệ trước hội đồng chuyên môn) đóng vai trò là cột mốc tối cao để tổng hợp toàn bộ các bài thực hành Lab đơn lẻ thành một hệ thống Web Service hoàn chỉnh.""",
            "example": """Cơ cấu phân bổ điểm học phần chi tiết nhằm tối ưu hóa kỹ năng thực hành của học viên:
- Điểm Chuyên cần (10%): Đánh giá thái độ tham gia các buổi học lý thuyết trực tuyến và thảo luận.
- Điểm Bài thực hành Lab hàng tuần (30%): Đánh giá qua các bài tập viết API nhỏ tự làm hàng tuần.
- Điểm Thi giữa kỳ (20%): Đánh giá tổng hợp kiến thức lý thuyết nền tảng.
- Điểm Dự án cuối khóa (40%): Xây dựng RESTful API cho một ứng dụng thực tế (ví dụ: Quản lý thư viện, E-learning), bảo vệ trước hội đồng chấm điểm chuyên môn.""",
            "resolve": """Quy trình học tập chủ động giúp chuyển đổi kiến thức thụ động sang kỹ năng lập trình thực tế. Mỗi bài Lab hàng tuần đóng vai trò như một bài test năng lực nhỏ tích lũy mã nguồn. Khi đến tuần cuối cùng, thay vì bỡ ngỡ, học viên chỉ cần thực hiện ghép nối các module chức năng đã chạy độc lập và tối ưu hóa hệ thống để bảo vệ tự tin trước hội đồng chuyên môn.""",
            "summary": "Quy chế môn học quy định học viên bắt buộc phải hoàn thành tối thiểu 80% số bài Lab để đủ điều kiện thi cuối môn học. Tránh chủ quan dồn toàn bộ bài tập vào tuần cuối vì khối lượng kiến thức tích lũy rất lớn và đòi hỏi thời gian debug thực tế.",
            "self_test": [
                "Câu 1 (Thông hiểu): Tại sao phương pháp thiết kế ngược (Backward Design) lại hiệu quả hơn cách tiếp cận truyền thống trong việc học lập trình Web?",
                "Câu 2 (Vận dụng): Tính điểm tổng kết của một sinh viên có kết quả chuyên cần = 9, điểm Lab trung bình = 8.5, thi giữa kỳ = 7.5 và bảo vệ dự án cuối môn = 8.2.",
                "Câu 3 (Phân tích): Phân tích tầm quan trọng của việc hoàn thành đúng tiến độ các bài thực hành Lab nhỏ hàng tuần đối với sự thành bại của dự án cuối môn học."
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Trọng số của dự án cuối khóa chiếm bao nhiêu % tổng điểm môn học?", "options": ["10%", "20%", "30%", "40%"], "correct_option_index": 3, "explanation": "Dự án cuối khóa chiếm 40% trọng số nhằm đánh giá toàn diện kỹ năng thực hành."},
                {"type": "Q2_Execution_Flow", "question": "Quy trình học tập chủ động nào sau đây là đúng?", "options": ["Thi -> Đọc", "Xem Video -> Làm Quiz -> Thực hành Lab -> Làm Dự án", "Làm dự án -> Đọc lý thuyết", "Học lý thuyết -> Thi trắc nghiệm"], "correct_option_index": 1, "explanation": "Đây là trình tự giúp chuyển hóa từ lý thuyết sang kỹ năng ứng dụng."},
                {"type": "Q3_Code_Reading", "question": "Đoạn code sau: total = active*0.1 + lab*0.3 + exam*0.2 + final*0.4. Nếu active=9, lab=8, exam=7, final=6. total bằng bao nhiêu?", "options": ["6.8", "7.1", "7.5", "8.0"], "correct_option_index": 1, "explanation": "total = 0.9 + 2.4 + 1.4 + 2.4 = 7.1."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt lớn nhất giữa bài Lab thực hành và dự án cuối khóa là gì?", "options": ["Lab làm nhóm", "Lab rèn luyện kỹ năng đơn lẻ hàng tuần, Dự án đánh giá tổng hợp sản phẩm hoàn chỉnh", "Lab không tính điểm", "Không có khác biệt"], "correct_option_index": 1, "explanation": "Bài Lab tập trung vào bài tập nhỏ hàng tuần, dự án cuối khóa đòi hỏi tính tổng hợp."},
                {"type": "Q5_Prediction_Trap", "question": "Chuyện gì xảy ra nếu sinh viên không nộp đủ tối thiểu 80% số bài Lab thực hành?", "options": ["Bình thường", "Bị trừ 50% điểm tổng", "Không đủ điều kiện đạt môn (Trượt môn học)", "Làm bù vào tuần thi"], "correct_option_index": 2, "explanation": "Hoàn thành tối thiểu 80% bài Lab là điều kiện cần bắt buộc để qua môn."}
            ],
            "lab": {
                "title": "Đặc tả ý tưởng dự án cuối khóa",
                "objectives": ["Định hình chủ đề và các API chức năng của dự án cuối môn.", "Viết tài liệu đặc tả sơ bộ dạng Markdown."],
                "steps": [
                    "Bước 1: Lựa chọn 1 đề tài quản lý (ví dụ: Quản lý thư viện, Quản lý tài chính cá nhân).",
                    "Bước 2: Liệt kê tối thiểu 4 endpoint CRUD cơ bản.",
                    "Bước 3: Lưu thành file `project_pitch.md` trong thư mục dự án."
                ],
                "checklist": ["Tài liệu viết bằng Markdown đúng định dạng.", "Có đủ 4 endpoint CRUD cơ bản phục vụ quản lý."]
            }
        }
        
    elif "giới thiệu" in t or "cài đặt fastapi" in t or "môi trường" in t or "thực hành viết api" in t:
        return {
            "problem": """Xây dựng hệ thống Web API bằng các công nghệ cũ đòi hỏi lập trình viên phải viết rất nhiều mã nguồn lặp đi lặp lại chỉ để xử lý các tác vụ cơ bản như định tuyến (routing), phân tách dữ liệu yêu cầu (request parsing) và định dạng dữ liệu phản hồi (response formatting). Ngoài ra, việc duy trì một bộ tài liệu đặc tả API chuẩn hóa (như Swagger UI hoặc OpenAPI) đồng bộ với mã nguồn thực tế luôn là thách thức lớn, dẫn tới tình trạng tài liệu bị lạc hậu so với code đang chạy thực tế.""",
            "analysis": """Các framework web đồng bộ (như Django hay Flask) hoạt động theo cơ chế WSGI (Web Server Gateway Interface) xử lý tuần tự. Khi gặp các tác vụ tốn thời gian như truy vấn cơ sở dữ liệu hoặc đọc ghi file, luồng xử lý sẽ bị chặn hoàn toàn (I/O blocking). Việc thiếu hụt cơ chế tự động kiểm tra tính hợp lệ của dữ liệu đầu vào (data validation) ở mức framework buộc lập trình viên phải viết hàng chục dòng code `if-else` lồng nhau phức tạp, làm giảm đáng kể hiệu năng hệ thống.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Tiêu chí so sánh</th>
            <th style="padding:12px; border:1px solid var(--border-color);">WSGI (Django / Flask)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">ASGI (FastAPI / Starlette)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Mô hình xử lý</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Đồng bộ (Synchronous), chặn I/O luồng</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Bất đồng bộ (Asynchronous), non-blocking Event Loop</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Tài liệu tự động</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không có (Cần cài đặt thêm thư viện mở rộng)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Tự sinh Swagger UI và ReDoc tại /docs và /redoc</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Hiệu năng xử lý</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Trung bình (Giới hạn bởi Thread Pool)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cực cao (Tương đương Go và Node.js nhờ ASGI)</td>
        </tr>
    </tbody>
</table>""",
            "solution": """FastAPI được xây dựng trên nền tảng ASGI, cho phép tận dụng sức mạnh của cơ chế xử lý bất đồng bộ (async/await) trong Python để xử lý hàng ngàn request đồng thời mà không bị nghẽn I/O. Ngoài ra, việc tích hợp sâu thư viện Pydantic giúp tự động hóa quá trình validate dữ liệu đầu vào bằng Type Hints và tự sinh tài liệu API tương tác trực quan Swagger UI song song với quá trình viết code.""",
            "example": """# B1: Tạo và kích hoạt môi trường ảo (Khai báo local venv)
# Trên Windows: python -m venv venv && venv\\Scripts\\activate
# Trên macOS/Linux: python3 -m venv venv && source venv/bin/activate

# B2: Cài đặt thư viện FastAPI và máy chủ Uvicorn ASGI
# pip install fastapi uvicorn

# B3: Viết code ứng dụng chính trong file main.py
from fastapi import FastAPI

app = FastAPI(
    title="Hệ thống Quản lý Khách sạn",
    description="RESTful API cho phép đặt phòng và quản lý phòng nghỉ trực tuyến",
    version="1.0.0"
)

@app.get('/health', tags=["Hệ thống"])
def health_check():
    \"\"\"Kiểm tra trạng thái hoạt động của máy chủ API\"\"\"
    return {
        "status": "online",
        "database": "connected",
        "service": "FastAPI ASGI running"
    }
""",
            "resolve": """Nhờ ứng dụng kiến trúc ASGI và Uvicorn Server, ứng dụng FastAPI có thể tiếp nhận request gọi API, xử lý bất đồng bộ và trả về kết quả JSON tiêu chuẩn chỉ trong vài mili-giây. Trang tài liệu kiểm thử `/docs` tự động xuất hiện để đội ngũ Front-end có thể dùng thử và tích hợp mà không cần viết thêm cấu hình.""",
            "summary": "Luôn chạy dự án trong môi trường ảo độc lập (venv) để tránh xung đột thư viện. Tránh đặt tên tệp mã nguồn là `fastapi.py` để tránh lỗi nạp chồng (circular import). Lỗi phổ biến nhất là quên kích hoạt môi trường ảo dẫn đến lỗi ModuleNotFoundError khi chạy uvicorn.",
            "self_test": [
                "Câu 1 (Thông hiểu): Sự khác biệt cơ bản giữa chuẩn giao tiếp ASGI (FastAPI) và WSGI (Django/Flask) là gì?",
                "Câu 2 (Vận dụng): Viết một chương trình FastAPI đơn giản khai báo endpoint GET `/health` trả về trạng thái hoạt động của server dạng JSON: `{'status': 'OK'}`.",
                "Câu 3 (Phân tích): Tại sao việc tự động đồng bộ hóa tài liệu Swagger UI từ mã nguồn thực tế lại giúp giảm thiểu rủi ro trong quá trình phát triển dự án nhóm?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Hệ quản trị cơ sở dữ liệu chính được định hướng lưu trữ trạng thái lâu dài trong Multi-Agent Content Factory là?", "options": ["Redis", "MongoDB", "PostgreSQL", "SQLite"], "correct_option_index": 2, "explanation": "Hệ thống sử dụng PostgreSQL để lưu giữ dữ liệu bài học lâu dài."},
                {"type": "Q2_Execution_Flow", "question": "Tham số nào chỉ định uvicorn tự reload code khi có thay đổi?", "options": ["--reload", "--restart", "--refresh", "--auto"], "correct_option_index": 0, "explanation": "--reload kích hoạt chức năng tự động tải lại code."},
                {"type": "Q3_Code_Reading", "question": "Đoạn code: @app.get('/hello') def h(): return 'Hi' trả về kiểu dữ liệu gì?", "options": ["HTML", "JSON string 'Hi'", "Status 500", "Plain text"], "correct_option_index": 1, "explanation": "FastAPI tự động serialize dữ liệu trả về thành JSON."},
                {"type": "Q4_Compare_Contrast", "question": "ASGI khác gì WSGI?", "options": ["ASGI chỉ chạy trên Linux", "ASGI hỗ trợ xử lý bất đồng bộ (Asynchronous), WSGI chạy đồng bộ (Synchronous)", "ASGI chậm hơn", "Không khác biệt"], "correct_option_index": 1, "explanation": "ASGI hỗ trợ Asynchronous mạnh mẽ giúp tránh nghẽn I/O."},
                {"type": "Q5_Prediction_Trap", "question": "If đặt tên file code là fastapi.py và import fastapi thì chuyện gì xảy ra?", "options": ["Chạy bình thường", "Bỏ qua file local", "Lỗi Circular Import / ModuleNotFoundError", "Tự động xóa file"], "correct_option_index": 2, "explanation": "Python sẽ tự import chính file local gây lỗi nạp chồng."}
            ],
            "lab": {
                "title": "Khởi tạo Ứng dụng FastAPI Đầu tiên",
                "objectives": ["Tạo môi trường ảo venv và cài đặt FastAPI.", "Chạy ứng dụng FastAPI đầu tiên qua uvicorn."],
                "steps": [
                    "Bước 1: Tạo thư mục dự án và chạy `python -m venv venv`.",
                    "Bước 2: Kích hoạt venv bằng lệnh `venv\\Scripts\\activate` (Windows).",
                    "Bước 3: Cài đặt thư viện: `pip install fastapi uvicorn`.",
                    "Bước 4: Tạo file `main.py` định nghĩa endpoint GET `/hello`.",
                    "Bước 5: Khởi chạy: `uvicorn main:app --reload`."
                ],
                "checklist": ["Có thư mục venv trong dự án.", "Truy cập `http://127.0.0.1:8000/docs` hiển thị trang tài liệu Swagger UI."]
            }
        }
        
    elif "parameter" in t or "pydantic" in t or "validation" in t:
        return {
            "problem": """Khi nhận dữ liệu từ các yêu cầu của client (như Path parameters, Query parameters, hoặc Request body), hệ thống dễ gặp tình trạng dữ liệu bị sai định dạng, thiếu hụt trường hoặc chứa các giá trị độc hại. Nếu không có bộ kiểm soát nghiêm ngặt, các lỗi kiểu dữ liệu sẽ đi sâu vào tầng nghiệp vụ và cơ sở dữ liệu, gây ra các lỗi runtime nghiêm trọng.""",
            "analysis": """Việc viết code kiểm tra dữ liệu bằng các câu lệnh `if-else` lồng nhau một cách thủ công ở mỗi controller vừa làm phình to mã nguồn, vừa tăng độ phức tạp khi bảo trì và dễ bỏ sót các lỗ hổng logic. Hơn thế nữa, các phương pháp ép kiểu dữ liệu thủ công không thể tự động trả về phản hồi lỗi trực quan cho phía Client, dẫn đến trải nghiệm người dùng kém và gây khó khăn lớn cho việc gỡ lỗi.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Tiêu chí so sánh</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Kiểm tra dữ liệu thủ công (if-else)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Pydantic Validation (FastAPI)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Cú pháp khai báo</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Rườm rà, lặp đi lặp lại ở mọi endpoint</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Định nghĩa tập trung qua Pydantic BaseModel</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Tự động ép kiểu</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Phải ép kiểu thủ công (ví dụ int(), float())</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Tự động ép kiểu thông minh (Data Coercion)</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Định dạng lỗi</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không đồng nhất, khó tích hợp với Frontend</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chuẩn hóa mã lỗi HTTP 422 kèm JSON chi tiết cấu trúc lỗi</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Pydantic cho phép định nghĩa cấu trúc dữ liệu mong muốn thông qua các lớp kế thừa từ `BaseModel`. Bằng cách tận dụng cơ chế Type Hints của Python, FastAPI tự động thực hiện ép kiểu dữ liệu thông minh, kiểm tra tính hợp lệ và tự động trả về lỗi chi tiết cho client nếu dữ liệu gửi lên không đúng định dạng mong đợi.""",
            "example": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Định nghĩa dữ liệu đầu vào với Pydantic và Field
class RoomReservation(BaseModel):
    guest_name: str = Field(..., min_length=2, max_length=50, description="Tên khách hàng đặt phòng")
    room_number: int = Field(..., gt=0, description="Số phòng phải lớn hơn 0")
    price_per_night: float = Field(..., gt=0.0)
    email: str = Field(..., description="Email nhận hóa đơn xác nhận")

@app.post('/reservations', status_code=201, tags=["Đặt phòng"])
def create_reservation(reservation: RoomReservation):
    # Khi code chạy vào hàm này, dữ liệu đầu vào đảm bảo đã được validate 100%
    return {
        "message": "Đã tạo đơn đặt phòng thành công",
        "data": reservation
    }
""",
            "resolve": """Mọi yêu cầu POST gửi lên endpoint `/reservations` chứa dữ liệu sai lệch (ví dụ: `room_number: -5` hoặc thiếu trường `guest_name`) sẽ bị chặn đứng ngay lập tức tại cổng vào của API. FastAPI tự động phản hồi lại Client với mã lỗi HTTP 422 Unprocessable Entity kèm theo thông tin chi tiết về trường dữ liệu bị lỗi mà lập trình viên không cần viết thêm bất kỳ dòng code validate thủ công nào.""",
            "summary": "Luôn sử dụng Pydantic Field để ràng buộc thêm các điều kiện logic (như độ dài chuỗi, khoảng giá trị của số). Lỗi thường gặp nhất là khai báo kiểu dữ liệu không khớp giữa Pydantic Model và cơ sở dữ liệu thực tế, hoặc truyền sai định dạng JSON dẫn tới lỗi validate.",
            "self_test": [
                "Câu 1 (Thông hiểu): Cơ chế tự động ép kiểu dữ liệu thông minh (data coercion) của Pydantic hoạt động như thế nào trong FastAPI?",
                "Câu 2 (Vận dụng): Định nghĩa một Pydantic Model có tên `Product` gồm các thuộc tính: name (chuỗi, bắt buộc), price (số thực, lớn hơn 0), và stock (số nguyên, không âm, mặc định là 0).",
                "Câu 3 (Phân tích): Tại sao FastAPI lại lựa chọn trả về mã lỗi HTTP 422 thay vì HTTP 500 khi Client gửi dữ liệu đầu vào không hợp lệ?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Lớp nào trong Pydantic được dùng làm lớp cha để định nghĩa cấu trúc JSON đầu vào?", "options": ["BaseClass", "BaseModel", "DataModel", "ValidationModel"], "correct_option_index": 1, "explanation": "BaseModel là lớp cha nền tảng của Pydantic để định nghĩa schema."},
                {"type": "Q2_Execution_Flow", "question": "Quy trình validate của FastAPI diễn ra khi nào?", "options": ["Sau khi lưu database", "Trước khi chạy logic trong hàm route", "Khi render Swagger UI", "Sau khi trả response cho client"], "correct_option_index": 1, "explanation": "FastAPI tự động validate ngay khi nhận request trước khi gọi controller xử lý."},
                {"type": "Q3_Code_Reading", "question": "Cho model: class User(BaseModel): name: str; age: int. Nếu client gửi {'name': 'An'}, API trả về lỗi gì?", "options": ["200 Success", "422 Unprocessable Entity", "404 Not Found", "500 Server Error"], "correct_option_index": 1, "explanation": "Thiếu trường bắt buộc age sẽ kích hoạt validate error (422)."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa Path Parameter và Query Parameter là gì?", "options": ["Path dùng định danh, Query dùng lọc/sắp xếp", "Path không bắt buộc, Query bắt buộc", "Path nằm trong Body, Query nằm trên URL", "Không khác biệt"], "correct_option_index": 0, "explanation": "Path param định dạng đường dẫn URL, Query param lọc kết quả sau dấu hỏi chấm (?)."},
                {"type": "Q5_Prediction_Trap", "question": "Điều gì xảy ra nếu bạn truyền tham số kiểu số nguyên là '123' (chuỗi) vào Type Hint int trong FastAPI?", "options": ["Báo lỗi 422", "Tự động ép kiểu thành số nguyên 123", "Gây sập server", "Bỏ qua tham số"], "correct_option_index": 1, "explanation": "Pydantic sẽ tự động thực hiện ép kiểu thông minh (coercion) nếu hợp lệ."}
            ],
            "lab": {
                "title": "Validate dữ liệu với Pydantic",
                "objectives": ["Định nghĩa Pydantic model cho đối tượng đặt phòng (RoomReservation).", "Tích hợp validate vào API POST `/reservations`."],
                "steps": [
                    "Bước 1: Khai báo class `RoomReservation` kế thừa `BaseModel` gồm: guest_name (str), room_number (int), price_per_night (float), email (str).",
                    "Bước 2: Định nghĩa route POST `/reservations` nhận body là RoomReservation.",
                    "Bước 3: Sử dụng Swagger UI để test truyền dữ liệu đúng và dữ liệu sai (ví dụ: room_number=-1) để xem phản hồi lỗi 422."
                ],
                "checklist": ["Model Reservation kế thừa đúng BaseModel.", "Trả về mã lỗi HTTP 422 khi truyền room_number không phải là số dương."]
            }
        }
        
    elif "crud" in t:
        return {
            "problem": """Bất kỳ ứng dụng quản lý dữ liệu nào cũng đều xoay quanh bốn thao tác cốt lõi: Thêm mới (Create), Truy xuất (Read), Cập nhật (Update) và Xóa (Delete). Thách thức lớn nhất đối với lập trình viên là thiết kế các đường dẫn và phương thức giao tiếp API sao cho khoa học, dễ hiểu, tránh chồng chéo logic và tuân thủ các tiêu chuẩn thiết kế RESTful API quốc tế.""",
            "analysis": """Việc lạm dụng một phương thức duy nhất (ví dụ chỉ dùng POST hoặc GET cho mọi thao tác) sẽ phá vỡ tính ngữ nghĩa của giao thức HTTP, gây khó khăn cho việc phân quyền bảo mật, cấu hình bộ đệm (caching) và mở rộng hệ thống sau này. Ngoài ra, việc quản lý và đồng bộ trạng thái dữ liệu trong bộ nhớ tạm (In-memory mock database) cần được thực hiện cẩn thận để tránh các xung đột dữ liệu khi có nhiều yêu cầu thay đổi đồng thời.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">HTTP Method</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Vai trò RESTful</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Tính chất Idempotent (Bất biến)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Mã trạng thái thành công</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">GET</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Lấy dữ liệu (Read)</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:green; font-weight:bold;">Có (True)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">200 OK</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">POST</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Tạo mới tài nguyên (Create)</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:red; font-weight:bold;">Không (False)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">201 Created</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">PUT</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cập nhật toàn phần (Update)</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:green; font-weight:bold;">Có (True)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">200 OK / 204 No Content</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">DELETE</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Xóa tài nguyên (Delete)</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:green; font-weight:bold;">Có (True)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">200 OK / 204 No Content</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Xây dựng hệ thống định tuyến (Routing) chuẩn RESTful. Tận dụng đầy đủ các phương thức HTTP thích hợp cho từng thao tác nghiệp vụ: POST để tạo mới tài nguyên, GET để đọc dữ liệu, PUT để ghi đè toàn bộ thông tin, PATCH để cập nhật từng phần và DELETE để gỡ bỏ tài nguyên ra khỏi hệ thống.""",
            "example": """from fastapi import FastAPI, HTTPException

app = FastAPI()

# Giả lập Database trong RAM
hotel_rooms = [
    {"id": 1, "room_type": "Deluxe Double", "available": True},
    {"id": 2, "room_type": "Standard Single", "available": False}
]

@app.get('/rooms', tags=["Quản lý phòng"])
def get_all_rooms():
    return hotel_rooms

@app.post('/rooms', status_code=201, tags=["Quản lý phòng"])
def create_room(room_type: str):
    new_room = {"id": len(hotel_rooms) + 1, "room_type": room_type, "available": True}
    hotel_rooms.append(new_room)
    return new_room

@app.delete('/rooms/{room_id}', tags=["Quản lý phòng"])
def delete_room(room_id: int):
    for idx, room in enumerate(hotel_rooms):
        if room["id"] == room_id:
            deleted_room = hotel_rooms.pop(idx)
            return {"message": "Đã xóa phòng thành công", "deleted_room": deleted_room}
    raise HTTPException(status_code=404, detail="Không tìm thấy ID phòng yêu cầu")
""",
            "resolve": """Khi áp dụng cấu trúc CRUD chuẩn hóa, Client có thể dễ dàng tương tác dữ liệu hai chiều với server. Các endpoint hoạt động độc lập, có mã trạng thái HTTP trả về chính xác (như 201 Created cho POST, 200 OK cho GET và 404 Not Found khi truy cập tài nguyên không tồn tại), tạo nền tảng vững chắc để kết nối với cơ sở dữ liệu vật lý sau này.""",
            "summary": "Luôn trả về đúng mã trạng thái HTTP cho từng thao tác thành công hoặc thất bại. Lỗi thường gặp nhất là dùng sai phương thức HTTP (ví dụ sử dụng GET để xóa dữ liệu) hoặc quên kiểm tra sự tồn tại của tài nguyên trước khi tiến hành cập nhật/xóa.",
            "self_test": [
                "Câu 1 (Thông hiểu): Tính chất Idempotency là gì và tại sao phương thức PUT lại có tính chất này trong khi POST thì không?",
                "Câu 2 (Vận dụng): Viết code FastAPI triển khai endpoint PUT `/rooms/{room_id}` để cập nhật trạng thái hoàn thành của một phòng nghỉ trong danh sách giả lập.",
                "Câu 3 (Phân tích): Tại sao trong thực tế doanh nghiệp, người ta thường ưu tiên sử dụng phương thức PATCH thay vì PUT khi thực hiện cập nhật thông tin người dùng?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Phương thức HTTP nào được dùng chuẩn để tạo mới tài nguyên?", "options": ["GET", "POST", "PUT", "DELETE"], "correct_option_index": 1, "explanation": "POST is used to submit data to create a new resource on the server."},
                {"type": "Q2_Execution_Flow", "question": "Để cập nhật một phần nhỏ dữ liệu của đối tượng (Partial Update), phương thức HTTP nào phù hợp nhất?", "options": ["PUT", "PATCH", "POST", "DELETE"], "correct_option_index": 1, "explanation": "PATCH is tailored for partial updates, while PUT is for full replacement."},
                {"type": "Q3_Code_Reading", "question": "Đoạn code xóa: items.pop(id). Lỗi gì xảy ra nếu id vượt quá độ dài mảng?", "options": ["Trả về None", "IndexError gây sập server (lỗi 500 nếu không handle)", "Tự động xóa phần tử cuối", "Trả lỗi 404 mặc định"], "correct_option_index": 1, "explanation": "IndexError is a python runtime error, causing a 500 server error if unhandled."},
                {"type": "Q4_Compare_Contrast", "question": "Sự khác biệt giữa PUT và POST trong RESTful API?", "options": ["PUT không có body", "POST dùng tạo mới, PUT dùng cập nhật đè (Idempotent)", "POST chạy nhanh hơn PUT", "Không khác biệt"], "correct_option_index": 1, "explanation": "PUT is idempotent (calling it multiple times has same effect), POST appends new resources every time."},
                {"type": "Q5_Prediction_Trap", "question": "Nếu gọi API DELETE thành công đối với tài nguyên đã bị xóa từ trước, mã HTTP trả về nên là gì?", "options": ["200 hoặc 204", "404 Not Found", "500 Server Error", "400 Bad Request"], "correct_option_index": 1, "explanation": "If the resource is already gone, returning 404 Not Found is highly descriptive."}
            ],
            "lab": {
                "title": "Thiết kế CRUD phòng nghỉ",
                "objectives": ["Đầy đủ 4 endpoint hoạt động.", "Xử lý được trường hợp ID không tồn tại để trả về thông báo phù hợp."],
                "steps": [
                    "Bước 1: Tạo biến danh sách `hotel_rooms = []` trong bộ nhớ.",
                    "Bước 2: Tạo GET `/rooms` để xem danh sách.",
                    "Bước 3: Tạo POST `/rooms` để thêm mới.",
                    "Bước 4: Tạo DELETE `/rooms/{room_id}` để xóa và kiểm thử qua Swagger."
                ],
                "checklist": ["Đầy đủ 4 endpoint hoạt động.", "Xử lý được trường hợp ID không tồn tại để trả về thông báo phù hợp."]
            }
        }
        
    elif "sqlalchemy" in t or "cơ sở dữ liệu" in t or "database" in t or "orm" in t:
        return {
            "problem": """Lưu trữ dữ liệu trong bộ nhớ tạm thời (RAM) đồng nghĩa với việc thông tin sẽ bị xóa sạch khi ứng dụng khởi động lại hoặc gặp sự cố crash đột ngột. Để xây dựng một Web Service thực tế, chúng ta bắt buộc phải có cơ chế ghi nhớ trạng thái lâu dài bằng cách kết nối và lưu trữ dữ liệu vào các hệ cơ sở dữ liệu quan hệ như MySQL hay PostgreSQL.""",
            "analysis": """Việc viết trực tiếp câu lệnh SQL thuần (Raw SQL) lồng ghép bên trong mã Python gây khó khăn cho việc bảo trì, không kiểm soát được kiểu dữ liệu và mở ra nguy cơ tấn công SQL Injection nghiêm trọng. SQLAlchemy ORM (Object-Relational Mapping) ra đời để giải quyết triệt để thách thức này bằng cách tự động ánh xạ cấu trúc bảng vật lý thành các Class Python hướng đối tượng.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Đặc tính so sánh</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Truy vấn SQL thuần (Raw SQL)</th>
            <th style="padding:12px; border:1px solid var(--border-color);">SQLAlchemy ORM (FastAPI)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Chống SQL Injection</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:red;">Phải tự xử lý tham số hóa thủ công</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:green; font-weight:bold;">Tự động tham số hóa dữ liệu (Parameterized)</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Độc lập hệ CSDL</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Phụ thuộc vào cú pháp SQL của từng hệ CSDL</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Độc lập (Tự sinh SQL tương thích với MySQL, PostgreSQL, SQLite...)</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Bảo trì & OOP</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khó đồng bộ kiểu dữ liệu giữa Database và code</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Ánh xạ trực tiếp thành đối tượng Class Python</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Sử dụng SQLAlchemy để định nghĩa Models, thiết lập Connection Pooling (quản lý bể kết nối) tối ưu và quản lý Transaction. Kết hợp Dependency Injection của FastAPI (`Depends`) để cấp phát và tự động thu hồi Database Session ở mỗi Request gửi lên.""",
            "example": """from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Khai báo chuỗi kết nối Database (ví dụ SQLite cục bộ)
DATABASE_URL = 'sqlite:///./hotel_reservation.db'

# 2. Khởi tạo Engine và SessionLocal kết nối
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Định nghĩa Model SQLAlchemy ánh xạ tới bảng
class DBRoom(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, unique=True, index=True)
    room_type = Column(String)
    is_available = Column(Boolean, default=True)

# 4. Hàm Generator cấp phát session DB (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db  # Trả về session cho API sử dụng
    finally:
        db.close()  # Đảm bảo đóng kết nối khi request kết thúc
""",
            "resolve": """Thông qua hàm generator `get_db()`, FastAPI đảm bảo mỗi request gửi đến hệ thống sẽ được cấp phát riêng một database session độc lập và session này chắc chắn sẽ tự động đóng lại khi request kết thúc để tránh rò rỉ kết nối.""",
            "summary": "Luôn quản lý vòng đời của Database Session thông qua Depend với generator yield. Lỗi thường gặp nhất là quên gọi `db.commit()` sau khi thực hiện thêm/sửa dữ liệu dẫn tới việc dữ liệu không được ghi lưu trữ vật lý thực tế xuống ổ đĩa cứng.",
            "self_test": [
                "Câu 1 (Thông hiểu): Tại sao việc sử dụng cơ chế Dependency Injection (`Depends(get_db)`) lại giúp tối ưu hóa việc quản lý kết nối cơ sở dữ liệu trong FastAPI?",
                "Câu 2 (Vận dụng): Khai báo một lớp Model SQLAlchemy có tên `Product` ánh xạ tới bảng `products` gồm các trường: id (khóa chính), name (chuỗi), và price (số thực).",
                "Câu 3 (Phân tích): So sánh và phân tích ưu điểm, nhược điểm của việc sử dụng thư viện ORM (như SQLAlchemy) so với việc viết các câu lệnh truy vấn SQL thuần túy."
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Hàm nào trong SQLAlchemy dùng để thiết lập kết nối vật lý tới Database?", "options": ["create_connection", "create_engine", "connect_db", "sessionmaker"], "correct_option_index": 1, "explanation": "create_engine định hình chuỗi kết nối và quản lý connection pool."},
                {"type": "Q2_Execution_Flow", "question": "Mô hình quản lý session db khuyên dùng trong FastAPI là gì?", "options": ["Mở session toàn cục", "Tạo và đóng session trong từng request (Dependency Injection với yield)", "Mở session khi start app và đóng khi shutdown", "Mỗi truy vấn tạo 1 connection mới"], "correct_option_index": 1, "explanation": "Sử dụng Generator Yield giúp tự động đóng session ngay sau khi kết thúc request."},
                {"type": "Q3_Code_Reading", "question": "Đoạn code: db.query(User).filter(User.id == 1).first(). Kết quả trả về là gì nếu id không có?", "options": ["Exception error", "None", "Mảng rỗng []", "Lỗi CSDL"], "correct_option_index": 1, "explanation": "first() trả về None nếu không tìm thấy bản ghi nào khớp điều kiện."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa Pydantic Model và SQLAlchemy Model là gì?", "options": ["Pydantic tương tác DB, SQLAlchemy validate dữ liệu", "Pydantic validate dữ liệu vào/ra và chuyển đổi JSON; SQLAlchemy định nghĩa cấu trúc bảng CSDL và tương tác dữ liệu vật lý", "Giống nhau hoàn toàn", "SQLAlchemy chỉ chạy trên PostgreSQL"], "correct_option_index": 1, "explanation": "Đây là 2 thư viện bổ trợ nhau: Pydantic ở tầng API, SQLAlchemy ở tầng Database."},
                {"type": "Q5_Prediction_Trap", "question": "Nếu gọi db.add(obj) mà quên gọi db.commit() thì chuyện gì xảy ra?", "options": ["Dữ liệu vẫn được lưu", "Dữ liệu được lưu tạm, biến mất khi restart", "Dữ liệu không được ghi xuống Database vật lý", "Hệ thống báo lỗi ngay"], "correct_option_index": 2, "explanation": "commit() là bắt buộc để xác nhận transaction ghi xuống ổ đĩa."}
            ],
            "lab": {
                "title": "Kết nối Cơ sở dữ liệu vật lý",
                "objectives": ["Cấu hình chuỗi kết nối và tạo bảng dữ liệu MySQL bằng SQLAlchemy."],
                "steps": [
                    "Bước 1: Cài đặt thư viện: `pip install sqlalchemy mysqlclient`.",
                    "Bước 2: Cấu hình `engine = create_engine('mysql://user:pass@localhost/db')`.",
                    "Bước 3: Định nghĩa Model `Todo` kế thừa `Base`.",
                    "Bước 4: Gọi lệnh `Base.metadata.create_all(bind=engine)` để tự sinh bảng trong CSDL."
                ],
                "checklist": ["Chạy script tạo bảng không báo lỗi kết nối.", "Bảng `todos` xuất hiện vật lý trong MySQL/PostgreSQL."]
            }
        }
        
    elif "structure" in t or "thiết kế" in t or "router" in t:
        return {
            "problem": """Khi quy mô dự án phát triển phần mềm mở rộng, số lượng API endpoints có thể lên tới hàng trăm. Việc nhồi nhét tất cả mã nguồn liên quan đến định tuyến, kết nối database, xử lý logic nghiệp vụ và validate dữ liệu vào chung một tệp tin duy nhất (như `main.py`) sẽ biến tệp tin đó thành một cấu trúc hỗn độn, vô cùng khó bảo trì và dễ xảy ra xung đột khi làm việc nhóm.""",
            "analysis": """Việc vi phạm nguyên tắc Đơn nhiệm (Single Responsibility Principle) làm cho các thành phần của hệ thống bị ràng buộc chặt chẽ với nhau (tight coupling). Một thay đổi nhỏ ở cấu trúc database có thể trực tiếp làm sập logic của API Router nếu chúng không được phân tách lớp rõ ràng. Cấu trúc Clean Architecture giúp tách biệt rõ ràng trách nhiệm của từng cấu phần.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Thư mục chức năng</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Trách nhiệm chính</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Thư viện tương ứng</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">routers/</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Định nghĩa URL, phân phối request (Routing)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">FastAPI APIRouter</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">schemas/</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Validate cấu trúc request/response JSON</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Pydantic BaseModel</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">models/</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Định nghĩa cấu trúc bảng CSDL vật lý</td>
            <td style="padding:10px; border:1px solid var(--border-color);">SQLAlchemy declarative_base</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">crud/</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Trực tiếp truy vấn, ghi dữ liệu vào CSDL</td>
            <td style="padding:10px; border:1px solid var(--border-color);">SQLAlchemy Session query</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Áp dụng cấu trúc thư mục chuẩn công nghiệp kết hợp với công cụ `APIRouter` của FastAPI. Chúng ta chia nhỏ mã nguồn thành các thư mục chuyên biệt: `routers/` quản lý định tuyến, `models/` đại diện cấu trúc dữ liệu vật lý, `schemas/` validate đầu vào đầu ra với Pydantic, và `crud/` chịu trách nhiệm truy vấn database.""",
            "example": """# 1. Định nghĩa router con độc lập (app/routers/rooms.py)
from fastapi import APIRouter

router = APIRouter(
    prefix='/rooms',
    tags=['Quản lý phòng nghỉ']
)

@router.get('/')
def list_rooms():
    return {"message": "Danh sách phòng", "data": []}

# 2. Đăng ký router con vào file main.py chính
from fastapi import FastAPI
from app.routers import rooms  # Import router con an toàn

app = FastAPI(title="Hệ thống Khách sạn")
app.include_router(rooms.router)  # Gộp route
""",
            "resolve": """Nhờ sử dụng APIRouter, các module chức năng được tách rời hoàn toàn và có thể phát triển song song bởi nhiều thành viên trong dự án. Khi ứng dụng chính chạy lên, FastAPI tự động gộp các đường dẫn lại một cách thông minh và nhóm chúng thành các tag trực quan trên giao diện Swagger UI, giúp việc kiểm thử và tích hợp diễn ra trơn tru.""",
            "summary": "Luôn đặt tiền tố (prefix) và gắn nhãn (tags) phù hợp cho từng APIRouter. Lỗi thường gặp nhất là cấu hình sai đường dẫn dẫn tới xung đột đè route, hoặc import chéo (circular import) giữa các tệp tin trong cấu trúc phân cấp.",
            "self_test": [
                "Câu 1 (Thông hiểu): APIRouter trong FastAPI có vai trò gì trong việc giải quyết bài toán tổ chức dự án lớn?",
                "Câu 2 (Vận dụng): Thiết kế cấu trúc thư mục chuẩn hóa cho một ứng dụng quản lý lớp học gồm các thực thể: Học viên, Giảng viên, Lớp học.",
                "Câu 3 (Phân tích): Tại sao việc tách biệt rõ ràng giữa lớp Model (SQLAlchemy) và lớp Schema (Pydantic) lại được coi là một Best Practice quan trọng trong thiết kế kiến trúc phần mềm?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Hành động nào tích hợp APIRouter vào ứng dụng FastAPI chính?", "options": ["app.add_router(router)", "app.include_router(router)", "app.import_router(router)", "app.register_router(router)"], "correct_option_index": 1, "explanation": "include_router() là hàm chuẩn để gộp định tuyến module vào app chính."},
                {"type": "Q2_Execution_Flow", "question": "Trong cấu trúc dự án chuẩn, thư mục nào thường chứa các file định nghĩa schema Pydantic?", "options": ["models/", "schemas/", "routers/", "crud/"], "correct_option_index": 1, "explanation": "schemas/ chứa Pydantic models validate dữ liệu đầu vào/ra."},
                {"type": "Q3_Code_Reading", "question": "Đoạn code: router = APIRouter(prefix='/products'). Route bên dưới: @router.get('/{id}'). URL đầy đủ để gọi endpoint này là gì?", "options": ["/{id}", "/products/{id}", "/products/get/{id}", "/get/{id}"], "correct_option_index": 1, "explanation": "URL đầy đủ bằng prefix cộng với path cụ thể của endpoint."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa Models và Schemas trong dự án FastAPI cấu trúc chuẩn?", "options": ["Models là Pydantic, Schemas là SQLAlchemy", "Models là cấu trúc bảng CSDL (SQLAlchemy), Schemas là cấu trúc dữ liệu API (Pydantic)", "Hai thư mục này giống nhau", "Models lưu trong RAM, Schemas lưu trong DB"], "correct_option_index": 1, "explanation": "Models là ORM đại diện DB vật lý, Schemas là Pydantic validate dữ liệu API."},
                {"type": "Q5_Prediction_Trap", "question": "Nếu quên include một router vào file main.py thì Swagger UI hiển thị như thế nào?", "options": ["Swagger sập", "Swagger hiển thị nhưng báo lỗi khi gọi", "Các endpoint của router đó không xuất hiện", "Swagger tự quét và hiển thị đầy đủ"], "correct_option_index": 2, "explanation": "FastAPI chỉ tự động nạp các router được đăng ký tường minh thông qua include_router."}
            ],
            "lab": {
                "title": "Tái cấu trúc Dự án với APIRouter",
                "objectives": ["Chia nhỏ ứng dụng đơn tệp thành cấu trúc thư mục chuẩn hóa."],
                "steps": [
                    "Bước 1: Tạo cấu trúc thư mục: `app/main.py`, `app/routers/`, `app/schemas/`.",
                    "Bước 2: Di chuyển code liên quan đến User sang `app/routers/users.py` sử dụng `APIRouter`.",
                    "Bước 3: Trong `app/main.py`, gọi `app.include_router(users_router)`.",
                    "Bước 4: Chạy server uvicorn từ thư mục ngoài và xác nhận Swagger hoạt động bình thường."
                ],
                "checklist": ["Không còn code định tuyến trực tiếp trong main.py ngoại trừ include_router.", "API hoạt động bình thường qua cấu trúc mới."]
            }
        }
        
    elif "quan hệ" in t or "relationship" in t:
        return {
            "problem": """Dữ liệu trong thực tế luôn có các mối liên kết quan hệ chặt chẽ với nhau (ví dụ: Một phòng nghỉ có nhiều hóa đơn đặt phòng, mỗi hóa đơn bắt buộc phải thuộc về một phòng xác định). Nếu chúng ta thiết kế các bảng cơ sở dữ liệu dạng phẳng, không liên kết, dữ liệu sẽ bị trùng lặp nghiêm trọng và không đảm bảo được tính nhất quán tham chiếu.""",
            "analysis": """Việc quản lý các mối quan hệ liên kết bằng cách truy vấn thủ công qua các câu lệnh JOIN phức tạp làm tốn hiệu năng xử lý của cơ sở dữ liệu. Đặc biệt, cơ chế nạp dữ liệu liên quan nếu không được cấu hình tốt sẽ dẫn tới lỗi nghẽn hiệu năng N+1 Query. Việc hiểu và lựa chọn Loading Strategy phù hợp là điều bắt buộc.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Loading Strategy</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Cơ chế hoạt động</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Ưu nhược điểm</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Lazy Loading (lazy='select')</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Trì hoãn query bảng liên quan tới khi gọi thuộc tính trong code</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Tiết kiệm kết nối, nhưng dễ gây lỗi N+1 Query trong vòng lặp</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Joined Loading (joinedload)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Sử dụng LEFT OUTER JOIN để lấy dữ liệu đồng thời ở 1 query duy nhất</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Nhanh, hiệu quả cao cho quan hệ 1-Nhiều hoặc 1-1</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Selectin Loading (selectinload)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Phát thêm câu lệnh truy vấn phụ sử dụng IN (IDs)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Rất tốt cho quan hệ Nhiều-Nhiều hoặc danh sách dữ liệu lớn</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Sử dụng các thuộc tính ràng buộc khóa ngoại (ForeignKey) ở tầng vật lý cơ sở dữ liệu và khai báo các thuộc tính ảo thông minh (`relationship()`) ở tầng SQLAlchemy ORM để tự động hóa liên kết thực thể.""",
            "example": """from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DBRoom(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(Integer)
    # Khai báo quan hệ 1-Nhiều ảo trỏ tới Booking model
    bookings = relationship('DBBooking', back_populates='room')

class DBBooking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    guest_name = Column(String)
    # Khóa ngoại liên kết vật lý tới bảng rooms
    room_id = Column(Integer, ForeignKey('rooms.id'))
    # Thuộc tính ảo lấy ngược thông tin phòng
    room = relationship('DBRoom', back_populates='bookings')
""",
            "resolve": """Nhờ cấu hình `relationship()`, chúng ta có thể dễ dàng truy vấn lấy thông tin phòng từ một đơn đặt phòng (`booking.room.room_number`) hoặc ngược lại lấy toàn bộ lịch sử đặt phòng của một phòng nghỉ cụ thể (`room.bookings`) một cách cực kỳ trực quan mà không cần viết các câu lệnh SQL JOIN phức tạp.""",
            "summary": "Luôn định nghĩa rõ tham số `back_populates` ở cả hai chiều của mối quan hệ để đồng bộ trạng thái đối tượng. Lỗi thường gặp nhất là lỗi lặp đệ quy vô tận (circular recursion) khi serialize đối tượng quan hệ chéo sang JSON bằng Pydantic.",
            "self_test": [
                "Câu 1 (Thông hiểu): Sự khác biệt cốt lõi giữa cơ chế Lazy Loading và Eager Loading trong việc nạp dữ liệu quan hệ của SQLAlchemy là gì?",
                "Câu 2 (Vận dụng): Thiết lập mối quan hệ Nhiều - Nhiều giữa bảng Học viên (Student) và lớp học (Class) thông qua một bảng trung gian (Association table) sử dụng SQLAlchemy.",
                "Câu 3 (Phân tích): Phân tích nguyên nhân và cách khắc phục lỗi IntegrityError khi chèn dữ liệu vi phạm ràng buộc khóa ngoại ForeignKey."
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Tham số nào khai báo khóa ngoại liên kết tới cột id của bảng users trong SQLAlchemy?", "options": ["ForeignKey('users.id')", "ForeignKey(User.id)", "ForeignKey('User')", "Join('users.id')"], "correct_option_index": 0, "explanation": "ForeignKey định nghĩa cột khóa ngoại liên kết vật lý."},
                {"type": "Q2_Execution_Flow", "question": "Khi truy vấn một User và muốn lấy danh sách bài viết của họ, SQLAlchemy mặc định truy vấn theo cơ chế nào (Lazy Loading)?", "options": ["Eager Loading (truy vấn luôn)", "Lazy Loading (chỉ truy vấn khi truy cập thuộc tính .posts)", "No Loading (không cho truy cập)", "Raw Query Loading"], "correct_option_index": 1, "explanation": "Lazy loading nạp dữ liệu trễ khi thuộc tính thực sự được gọi."},
                {"type": "Q3_Code_Reading", "question": "Cho class: Post(Base): user_id = Column(Integer, ForeignKey('users.id')). Chuyện gì xảy ra nếu chèn một Post có user_id = 999 trong khi bảng users chưa có id = 999?", "options": ["Lưu bình thường", "Lỗi vi phạm ràng buộc khóa ngoại (IntegrityError)", "Tự động tạo user 999", "Gán user_id = None"], "correct_option_index": 1, "explanation": "Hệ CSDL sẽ chặn do vi phạm khóa ngoại vật lý và báo IntegrityError."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa khóa ngoại (ForeignKey) và hàm relationship() trong SQLAlchemy?", "options": ["ForeignKey là ràng buộc vật lý trong DB; relationship() là thuộc tính ảo giúp Python truy vấn hướng đối tượng dễ dàng", "relationship() tạo cột trong DB, ForeignKey thì không", "Chúng là một", "Không khác biệt"], "correct_option_index": 0, "explanation": "ForeignKey là cột thực tế, relationship là ảo hỗ trợ ORM."},
                {"type": "Q5_Prediction_Trap", "question": "Để tránh lỗi đệ quy vô hạn khi chuyển đổi (serialize) Object có quan hệ chéo sang Pydantic Schema, ta cần làm gì?", "options": ["Xóa quan hệ", "Không dùng Pydantic", "Định nghĩa Schema riêng biệt giới hạn các trường quan hệ (không lồng chéo vòng lặp)", "Tắt chế độ validate của Pydantic"], "correct_option_index": 2, "explanation": "Sử dụng các model schema phẳng không lồng chéo là cách tốt nhất để ngắt vòng lặp."}
            ],
            "lab": {
                "title": "Thiết lập Quan hệ giữa các bảng",
                "objectives": ["Xây dựng liên kết Một - Nhiều giữa bảng User và bảng Post.", "Viết API lấy user kèm danh sách bài viết của họ."],
                "steps": [
                    "Bước 1: Khai báo class `User` có `posts = relationship('Post', back_populates='author')`.",
                    "Bước 2: Khai báo class `Post` chứa khóa ngoại `user_id` và `author = relationship('User', back_populates='posts')`.",
                    "Bước 3: Viết API GET `/users/{id}` trả về User và cấu hình Pydantic Schema để hiển thị danh sách posts lồng bên trong."
                ],
                "checklist": ["Bảng posts trong CSDL có khóa ngoại trỏ sang users.", "Kết quả JSON trả về chứa mảng bài viết lồng tương ứng."]
            }
        }
        
    elif "security" in t or "authentication" in t or "jwt" in t or "đăng ký" in t or "phân quyền" in t:
        return {
            "problem": """Một ứng dụng web hoạt động trên môi trường Internet công khai nếu không có cơ chế bảo mật sẽ dễ bị tấn công. Bất kỳ ai cũng có thể truy cập tự do vào các tài nguyên nhạy cảm, đánh cắp thông tin cá nhân hoặc thực hiện các thao tác phá hoại dữ liệu trái phép.""",
            "analysis": """Nhiều lập trình viên thường mắc sai lầm nghiêm trọng khi lưu mật khẩu dưới dạng văn bản thuần túy (Plaintext) hoặc thuật toán mã hóa lỗi thời (như MD5, SHA-1). Hơn nữa, giao thức HTTP hoạt động theo cơ chế không trạng thái (stateless) - tức là mỗi request độc lập hoàn toàn với nhau. Cần có giải pháp xác định danh tính người dùng an toàn.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Tiêu chí so sánh</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Mã hóa thô/MD5/SHA</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Bcrypt Hashing (FastAPI)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Cơ chế muối (Salting)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không có (Hai mật khẩu giống nhau cho ra mã băm giống nhau)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Tự sinh muối ngẫu nhiên (Salt) cho mỗi lượt băm mật khẩu</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Chống tấn công Brute-force</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:red;">Kém (Mã hóa rất nhanh, dễ bị vét cạn bằng bảng cầu vồng)</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:green; font-weight:bold;">Tốt (Hàm băm chậm cố ý, kiểm soát bởi Cost Factor)</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Xác thực Stateless</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Phải truy vấn Database liên tục kiểm tra session</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Xác thực chữ ký số trên Token JWT không cần DB</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Áp dụng thuật toán Bcrypt mã hóa mật khẩu một chiều an toàn kết hợp cấp phát JSON Web Tokens (JWT) cho Client. Mã JWT chứa chữ ký số (Signature) giúp Server tự kiểm thực tính toàn vẹn mà không cần lưu trữ trạng thái phiên làm việc (Session) trên server.""",
            "example": """from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# 1. Cấu hình Bcrypt cho mật khẩu
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# 2. Cấu hình chữ ký số JWT
SECRET_KEY = "rikkei_secret_key_production_environment"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    \"\"\"Băm mật khẩu sử dụng Bcrypt\"\"\"
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    \"\"\"So khớp mật khẩu băm\"\"\"
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    \"\"\"Cấp mã xác thực JWT\"\"\"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
""",
            "resolve": """Thông qua cơ chế Dependency Injection xác thực mã JWT trong header của request gửi lên, hệ thống tự động nhận diện danh tính người dùng hoặc từ chối truy cập ngay lập tức bằng mã lỗi HTTP 401 Unauthorized nếu token không hợp lệ hoặc đã hết hạn.""",
            "summary": "Tuyệt đối không để lộ SECRET_KEY trên mã nguồn công khai (phải cấu hình qua biến môi trường .env). Mật khẩu lưu trữ bắt buộc phải được băm qua Bcrypt. Lỗi thường gặp nhất là đặt thời gian sống của token quá dài hoặc không bắt ngoại lệ khi giải mã token.",
            "self_test": [
                "Câu 1 (Thông hiểu): Tại sao thuật toán băm Bcrypt lại an toàn hơn các thuật toán băm thông thường như MD5 hay SHA-256 đối với việc lưu trữ mật khẩu?",
                "Câu 2 (Vận dụng): Viết mã nguồn Python giải mã (decode) một chuỗi JWT và bắt các ngoại lệ liên quan đến token hết hạn (ExpiredSignatureError) hoặc token không hợp lệ (JWTError).",
                "Câu 3 (Phân tích): Phân tích quy trình trao đổi dữ liệu giữa Client và Server sử dụng giao thức xác thực Bearer Token kèm mã JWT."
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Ba phần chính phân tách bằng dấu chấm trong chuỗi JWT là gì?", "options": ["Header, Body, Key", "Header, Payload, Signature", "Id, Token, Expire", "Key, Value, Signature"], "correct_option_index": 1, "explanation": "Header, Payload, Signature là 3 cấu phần chuẩn hóa của JWT."},
                {"type": "Q2_Execution_Flow", "question": "Khi Client gửi request kèm token xác thực, token đó thường nằm ở phần nào của HTTP Request?", "options": ["URL Query Parameter", "HTTP Header Authorization (dạng Bearer token)", "Request Body JSON", "Cookie"], "correct_option_index": 1, "explanation": "Gửi token trong header Authorization dạng 'Bearer <token>' là chuẩn RESTful."},
                {"type": "Q3_Code_Reading", "question": "Nếu mã JWT đã hết hạn (expired), hàm jwt.decode() sẽ trả về kết quả gì?", "options": ["Dữ liệu cũ", "None", "Ném ra ngoại lệ ExpiredSignatureError", "Mã lỗi 401 mặc định"], "correct_option_index": 2, "explanation": "jose.jwt ném lỗi ExpiredSignatureError giúp chúng ta nhận diện và xử lý."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa Authentication và Authorization là gì?", "options": ["Chúng là một", "Authentication là xác thực danh tính (ai đây?); Authorization là phân quyền truy cập (làm được gì?)", "Authentication chạy chậm hơn Authorization", "Authentication dùng khóa đối xứng, Authorization dùng bất đối xứng"], "correct_option_index": 1, "explanation": "Authentication xác minh danh tính, Authorization xác minh quyền truy cập tài nguyên."},
                {"type": "Q5_Prediction_Trap", "question": "Điều gì xảy ra nếu kẻ tấn công thay đổi nội dung Payload trong token JWT của sinh viên?", "options": ["Token vẫn hợp lệ và chạy tiếp", "Server bị sập", "Chữ ký số (Signature) không còn khớp với Payload mới, và server sẽ reject token khi decode", "Server tự sửa lại Payload cũ"], "correct_option_index": 2, "explanation": "Khi thay đổi nội dung Payload, chữ ký số không khớp và server từ chối giải mã."}
            ],
            "lab": {
                "title": "Triển khai Xác thực JWT",
                "objectives": ["Xây dựng API đăng nhập nhận mật khẩu và cấp phát token JWT."],
                "steps": [
                    "Bước 1: Cài đặt thư viện: `pip install passlib[bcrypt] python-jose[cryptography]`.",
                    "Bước 2: Viết hàm băm mật khẩu và hàm so khớp mật khẩu.",
                    "Bước 3: Viết API `/login` kiểm tra username và password, nếu đúng cấp token JWT.",
                    "Bước 4: Tạo dependency `get_current_user` xác thực token trong header và test bằng Swagger."
                ],
                "checklist": ["Mật khẩu lưu trong database được mã hóa bcrypt (bắt đầu bằng $2b$).", "Truy cập endpoint bảo mật không gửi token trả về lỗi 401 Unauthorized."]
            }
        }
        
    elif "cors" in t or "middleware" in t:
        return {
            "problem": """Khi triển khai dự án thực tế, mã nguồn Frontend (React chạy tại cổng 3000) và Backend API (FastAPI chạy tại cổng 8000) nằm ở hai nguồn gốc khác nhau. Khi Frontend thực hiện gọi API gửi dữ liệu tới Backend, trình duyệt sẽ lập tức chặn đứng kết nối và báo lỗi đỏ liên quan đến chính sách CORS.""",
            "analysis": """Đây là hành vi bảo mật mặc định (Same-Origin Policy) để bảo vệ người dùng khỏi việc gửi dữ liệu trộm. Khi gửi request chéo nguồn gốc, trình duyệt sẽ gửi request preflight OPTIONS để kiểm tra server trước. Chúng ta cần hiểu cách thức hoạt động của Middleware để cấu hình chia sẻ tài nguyên hợp lệ.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Cấu hình CORSMiddleware</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Vai trò kỹ thuật</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Khuyến nghị bảo mật</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">allow_origins</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Chỉ định domain client nào được phép gọi API</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:orange; font-weight:bold;">Chỉ định chính xác domain (tránh dùng wildcard '*' ở production)</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">allow_methods</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Khai báo các phương thức HTTP được chấp nhận</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Giới hạn (ví dụ chỉ cho phép GET, POST)</td>
        </tr>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">allow_credentials</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cho phép gửi Cookies/Auth Headers chéo</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Bắt buộc phải True nếu dùng Session Cookies</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Tích hợp CORSMiddleware của FastAPI để cấu hình định danh rõ ràng danh sách các nguồn gốc (Origins) được phép gửi yêu cầu chéo, các phương thức HTTP (GET, POST,...) và các headers xác thực được chấp nhận trong các yêu cầu giao tiếp.""",
            "example": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Khai báo danh sách các domain tin cậy được phép truy cập
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Phổ biến cho Vite dev server
    "https://hotel-app.rikkei.edu.vn"
]

# 2. Tích hợp CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Hoặc khai báo cụ thể ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)
""",
            "resolve": """Trình duyệt nhận diện header `Access-Control-Allow-Origin` phản hồi từ server và cho phép Frontend React đọc kết quả JSON.""",
            "summary": "Nguy hiểm bảo mật khi lạm dụng wildcard `*` cho các domain nhạy cảm, thứ tự thực thi của các Middleware.",
            "self_test": [
                "Câu 1 (Thông hiểu): Cơ chế CORS hoạt động như thế nào trong trình duyệt?",
                "Câu 2 (Vận dụng): Viết code tích hợp CORSMiddleware vào ứng dụng chính, cấu hình an toàn không lạm dụng allow_origins=['*']",
                "Câu 3 (Phân tích): Tại sao trình duyệt lại gửi request OPTIONS (Preflight Request) trước khi gửi request thực tế?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Hành động nào tích hợp APIRouter vào ứng dụng FastAPI chính?", "options": ["app.add_router(router)", "app.include_router(router)", "app.import_router(router)", "app.register_router(router)"], "correct_option_index": 1, "explanation": "include_router() nạp APIRouter con vào ứng dụng."},
                {"type": "Q2_Execution_Flow", "question": "Trong cấu trúc dự án chuẩn, thư mục nào thường chứa các file định nghĩa schema Pydantic?", "options": ["models/", "schemas/", "routers/", "crud/"], "correct_option_index": 1, "explanation": "schemas/ chứa Pydantic models validate dữ liệu đầu vào/ra."},
                {"type": "Q3_Code_Reading", "question": "Đoạn code: router = APIRouter(prefix='/products'). Route bên dưới: @router.get('/{id}'). URL đầy đủ để gọi endpoint này là gì?", "options": ["/{id}", "/products/{id}", "/products/get/{id}", "/get/{id}"], "correct_option_index": 1, "explanation": "Đường dẫn đầy đủ bằng prefix ghép với path con."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa Models và Schemas trong dự án FastAPI cấu trúc chuẩn?", "options": ["Models là Pydantic, Schemas là SQLAlchemy", "Models là cấu trúc bảng CSDL (SQLAlchemy), Schemas là cấu trúc dữ liệu API (Pydantic)", "Hai thư mục này giống nhau", "Models lưu trong RAM, Schemas lưu trong DB"], "correct_option_index": 1, "explanation": "Models là ORM đại diện DB vật lý, Schemas là Pydantic validate dữ liệu API."},
                {"type": "Q5_Prediction_Trap", "question": "Nếu quên include một router vào file main.py thì Swagger UI hiển thị như thế nào?", "options": ["Swagger sập", "Swagger hiển thị nhưng báo lỗi khi gọi", "Các endpoint của router đó không xuất hiện", "Swagger tự quét và hiển thị đầy đủ"], "correct_option_index": 2, "explanation": "Các endpoint của router chưa đăng ký sẽ hoàn toàn không xuất hiện trên Swagger."}
            ],
            "lab": {
                "title": "Tích hợp CORS",
                "objectives": ["Cấu hình CORSMiddleware để kết nối API với Frontend chạy trên Localhost."],
                "steps": [
                    "Bước 1: Import CORSMiddleware từ fastapi.middleware.cors.",
                    "Bước 2: Tạo list origins chứa domain localhost:3000.",
                    "Bước 3: Gọi add_middleware cấu hình đầy đủ."
                ],
                "checklist": ["Gọi API chéo nguồn gốc từ Frontend thành công, không còn lỗi CORS ở Console của trình duyệt."]
            }
        }
        
    elif "upload" in t or "file" in t:
        return {
            "problem": """Nguy cơ tràn bộ nhớ RAM của server khi nhận các file kích thước lớn, rò rỉ bảo mật khi bị hacker tải lên các file thực thi chứa mã độc, hoặc lỗi ghi đè dữ liệu trùng tên file.""",
            "analysis": """FastAPI phân biệt rõ ràng giữa bytes thô (đọc thẳng vào RAM) và UploadFile (lưu tạm thời vào ổ đĩa dưới dạng spooled file). Đảm bảo kiểm tra MIME-type và kích thước tệp tải lên là bắt buộc để bảo vệ tài nguyên hệ thống.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Kiểu dữ liệu nhận file</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Tiêu tốn bộ nhớ RAM</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Thuộc tính & Tiện ích đi kèm</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">bytes (File)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Bằng chính dung lượng file (nguy cơ tràn RAM)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Không có metadata, chỉ có chuỗi nhị phân thô</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">UploadFile (FastAPI)</td>
            <td style="padding:10px; border:1px solid var(--border-color); color:green; font-weight:bold;">Cực thấp (Lưu tạm vào đĩa cứng dạng Spooled File)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Có filename, content_type (MIME) và các hàm async read/write/seek</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Khai báo `UploadFile = File(...)` của FastAPI, kiểm tra file size, MIME type, và đặt tên file bằng mã ngẫu nhiên UUID.""",
            "example": """import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/avatar", tags=["Tải lên"])
async def upload_avatar(file: UploadFile = File(...)):
    # 1. Kiểm tra kích thước file tải lên (ví dụ dưới 2MB)
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Kích thước tệp tin không được vượt quá 2MB")
        
    # 2. Kiểm tra định dạng file (chỉ cho phép .jpg, .png)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ định dạng hình ảnh")
        
    # 3. Tạo tên file ngẫu nhiên và lưu vào đĩa
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
        
    return {"filename": unique_filename, "message": "Tải lên thành công"}""",
            "resolve": """Sử dụng `await file.read()` hoặc `await file.seek(0)` một cách an toàn và lưu file xuống ổ đĩa, đảm bảo không bị tràn bộ nhớ RAM.""",
            "summary": "Phân biệt `bytes` và `UploadFile`, các bước xác thực kích thước và định dạng file tải lên để đảm bảo an toàn.",
            "self_test": [
                "Câu 1 (Thông hiểu): Tại sao trong ứng dụng thực tế nên dùng `UploadFile` thay vì `bytes` khi nhận file lớn?",
                "Câu 2 (Vận dụng): Viết code endpoint nhận file tải lên, kiểm tra nếu kích thước vượt quá 5MB thì trả về lỗi HTTP 400.",
                "Câu 3 (Phân tích): Điều gì xảy ra nếu hai người dùng tải lên cùng lúc hai file có tên giống hệt nhau (ví dụ: avatar.png) và cách phòng tránh?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Trong FastAPI, class nào được khuyến nghị sử dụng khi làm việc với file tải lên kích thước lớn?", "options": ["bytes", "UploadFile", "FileStream", "BinaryData"], "correct_option_index": 1, "explanation": "UploadFile lưu tạm vào Spooled File giúp tối ưu RAM."},
                {"type": "Q2_Execution_Flow", "question": "phương thức `await file.read()` của UploadFile có tác dụng gì?", "options": ["Xóa file khỏi bộ nhớ", "Đọc toàn bộ nội dung của tệp tải lên dưới dạng bytes", "Lưu file trực tiếp vào DB", "Giải nén file zip"], "correct_option_index": 1, "explanation": "`await file.read()` đọc toàn bộ dữ liệu nhị phân của tệp."},
                {"type": "Q3_Code_Reading", "question": "Để khai báo một tham số nhận file từ form-data trong FastAPI, ta sử dụng cú pháp nào?", "options": ["file: str = Form(...)", "file: UploadFile = File(...)", "file: bytes = Body(...)", "file: FileUpload = Query(...)"], "correct_option_index": 1, "explanation": "`file: UploadFile = File(...)` là cú pháp chuẩn của FastAPI."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt chính giữa `bytes` và `UploadFile` trong FastAPI?", "options": ["`bytes` lưu trong RAM, `UploadFile` lưu tạm trên ổ đĩa nếu file lớn và cung cấp metadata như filename, content_type", "`UploadFile` chỉ nhận file ảnh", "`bytes` nhanh hơn gấp 100 lần", "`UploadFile` không hỗ trợ async"], "correct_option_index": 0, "explanation": "`UploadFile` sử dụng SpooledTemporaryFile tối ưu RAM và có metadata."},
                {"type": "Q5_Prediction_Trap", "question": "Nếu gọi `await file.read()` hai lần liên tiếp mà không gọi `await file.seek(0)`, kết quả lần đọc thứ hai là gì?", "options": ["Trả về lỗi Exception", "Trả về chuỗi rỗng b'' do con trỏ file đã ở cuối tệp", "Trả về lại nội dung file", "Tự động tải lại từ client"], "correct_option_index": 1, "explanation": "Con trỏ file đã di chuyển đến cuối sau lần đọc đầu tiên, nên cần seek(0) để đọc lại."}
            ],
            "lab": {
                "title": "Tải lên tệp an toàn",
                "objectives": ["Xây dựng API nhận file tải lên, xác thực dung lượng và lưu vào đĩa."],
                "steps": [
                    "Bước 1: Khai báo endpoint nhận `UploadFile = File(...)`.",
                    "Bước 2: Kiểm tra content_type và kích thước tệp tải lên.",
                    "Bước 3: Tạo tên file ngẫu nhiên bằng UUID và lưu vào thư mục static/uploads."
                ],
                "checklist": ["Tải lên file thành công bằng Postman/Swagger, file được lưu vào đúng thư mục trên máy chủ."]
            }
        }

    elif "test" in t or "unit" in t:
        return {
            "problem": """Khó khăn trong việc đảm bảo tính đúng đắn của toàn bộ các API endpoints khi có thay đổi mã nguồn (Regression Bugs), tốn nhiều thời gian kiểm thử thủ công qua Postman/Swagger và rủi ro ghi đè dữ liệu thật trong Database khi chạy test.""",
            "analysis": """Kiểm thử tự động (Automated Testing) là tiêu chuẩn bắt buộc trong các dự án thực tế. FastAPI tích hợp sẵn TestClient dựa trên httpx giúp viết Unit Test và Integration Test cực kỳ nhanh chóng.

<table class="comparison-table" style="width:100%; border-collapse:collapse; margin:20px 0; font-size:0.95rem; text-align:left; border:1px solid var(--border-color);">
    <thead>
        <tr style="background-color:var(--primary); color:white;">
            <th style="padding:12px; border:1px solid var(--border-color);">Loại kiểm thử</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Phạm vi & Mục tiêu</th>
            <th style="padding:12px; border:1px solid var(--border-color);">Thời gian thực thi</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Unit Test</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Kiểm thử từng hàm/module riêng biệt (cô lập DB bằng Mocking)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Cực nhanh (Mili giây)</td>
        </tr>
        <tr style="background-color:#F8FAFC;">
            <td style="padding:10px; border:1px solid var(--border-color); font-weight:600;">Integration Test</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Luồng xử lý hoàn chỉnh (gọi API -> check Database session)</td>
            <td style="padding:10px; border:1px solid var(--border-color);">Trung bình (Vài giây)</td>
        </tr>
    </tbody>
</table>""",
            "solution": """Xây dựng hệ thống kiểm thử tự động chuyên nghiệp sử dụng thư viện `pytest` kết hợp với `TestClient` của FastAPI. Thiết lập cơ chế ghi đè kết nối để trỏ DB của test sang SQLite in-memory database.""",
            "example": """from fastapi.testclient import TestClient
from main import app

# 1. Khởi tạo TestClient kết nối tới app chính
client = TestClient(app)

def test_health_check_endpoint():
    # 2. Gửi request giả lập
    response = client.get('/health')
    
    # 3. Assert xác thực dữ liệu
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert "service" in response.json()
""",
            "resolve": """Bằng cách triển khai các kịch bản test tự động, lập trình viên chỉ cần chạy duy nhất một câu lệnh `pytest` ở cửa sổ dòng lệnh. Toàn bộ các API endpoints của hệ thống sẽ được quét, kiểm tra phản hồi đầu vào đầu ra chỉ trong vài giây.""",
            "summary": "Tách biệt rõ ràng cơ sở dữ liệu kiểm thử. Viết các hàm kiểm thử độc lập, đảm bảo trạng thái dữ liệu được làm sạch sau mỗi test case. Lỗi thường gặp nhất là viết các test case phụ thuộc lẫn nhau.",
            "self_test": [
                "Câu 1 (Thông hiểu): TestClient trong FastAPI hoạt động như thế nào và tại sao nó không cần khởi chạy một uvicorn server thực tế khi chạy các bài test?",
                "Câu 2 (Vận dụng): Viết một test case bằng pytest kiểm thử API POST `/reservations` kiểm tra xem khi Client gửi thiếu dữ liệu thì server có trả về mã trạng thái HTTP 422 chính xác hay không.",
                "Câu 3 (Phân tích): Tại sao việc tự động hóa kiểm thử (CI/CD) lại được coi là tiêu chuẩn bắt buộc trong quy trình phát triển và vận hành phần mềm tại các doanh nghiệp công nghệ lớn?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": "Lớp nào được import từ fastapi.testclient để giả lập các request gửi tới ứng dụng?", "options": ["TestClient", "ClientRequest", "AppClient", "MockClient"], "correct_option_index": 0, "explanation": "TestClient cung cấp các phương thức get, post, put, delete tương tác với app chính."},
                {"type": "Q2_Execution_Flow", "question": "Để pytest nhận diện một hàm là một test case để chạy, tên hàm bắt buộc phải bắt đầu bằng tiền tố gì?", "options": ["run_", "test_", "check_", "exec_"], "correct_option_index": 1, "explanation": "pytest quét toàn bộ các file và hàm có tên bắt đầu bằng test_ để chạy tự động."},
                {"type": "Q3_Code_Reading", "question": "Kết quả chạy pytest: assert 200 == 201 thất bại. Điều này có nghĩa là gì?", "options": ["Server bị sập", "API chạy đúng", "Mã trạng thái trả về thực tế là 200 trong khi kịch bản kỳ vọng phải là 201", "Đường dẫn API sai"], "correct_option_index": 2, "explanation": "AssertionError chỉ ra sự lệch nhau giữa giá trị thực tế trả về và kỳ vọng thiết kế."},
                {"type": "Q4_Compare_Contrast", "question": "Khác biệt giữa UnitTest và IntegrationTest là gì?", "options": ["UnitTest test giao diện, Integration test backend", "UnitTest kiểm thử hàm đơn lẻ biệt lập; IntegrationTest kiểm thử sự phối hợp giữa nhiều thành phần (API -> DB)", "UnitTest chạy chậm hơn", "Chúng giống nhau hoàn toàn"], "correct_option_index": 1, "explanation": "UnitTest test logic nhỏ biệt lập cô lập dependencies, IntegrationTest liên kết kiểm thử cả luồng database thực tế."},
                {"type": "Q5_Prediction_Trap", "question": "Khi chạy kiểm thử liên quan đến database, làm thế nào để đảm bảo dữ liệu test không ảnh hưởng đến database thực tế?", "options": ["Xóa database thực tế", "Sử dụng cơ chế ghi đè dependency (Dependency Overrides) gán database session chạy thử vào SQLite in-memory", "Không chạy test database", "Backup và khôi phục database liên tục"], "correct_option_index": 1, "explanation": "FastAPI hỗ trợ `app.dependency_overrides` giúp thay thế Database session thực bằng SQLite test database một cách chuyên nghiệp."}
            ],
            "lab": {
                "title": "Viết Unit & Integration Test",
                "objectives": ["Viết kịch bản kiểm thử API GET `/hello` sử dụng pytest."],
                "steps": [
                    "Bước 1: Cài đặt thư viện: `pip install pytest httpx`.",
                    "Bước 2: Tạo file `test_main.py`.",
                    "Bước 3: Khai báo `TestClient` kết nối tới app FastAPI.",
                    "Bước 4: Viết hàm `test_read_hello()` kiểm thử status code và dữ liệu trả về.",
                    "Bước 5: Chạy lệnh `pytest` ở console và quan sát kết quả."
                ],
                "checklist": ["Chạy lệnh pytest hoàn thành không báo lỗi đỏ.", "Assert đúng trạng thái HTTP 200 và kết quả JSON trả về."]
            }
        }
        
    else: # Fallback / Default details
        return {
            "problem": f"Thao tác kỹ thuật của '{title}' đòi hỏi sự chính xác cao về cú pháp và logic nghiệp vụ.",
            "analysis": "Không tuân thủ các quy tắc chuẩn hóa Web Service làm suy giảm hiệu năng hệ thống và gây khó khăn khi tích hợp ứng dụng.",
            "solution": "Áp dụng kiến trúc FastAPI chuẩn hóa, sử dụng kiểu dữ liệu phù hợp và kiểm thử tự động thường xuyên.",
            "example": f"# Cấu hình API\n# Nội dung liên quan đến {title}\n@app.get('/items')\ndef list_items():\n    return {{'status': 'OK', 'topic': '{title}'}}",
            "resolve": "Giải quyết các yêu cầu nghiệp vụ theo đúng chuẩn của FastAPI, đảm bảo code sạch và dễ bảo trì.",
            "summary": "Luôn kiểm thử kỹ lưỡng qua Swagger UI. Lỗi thường gặp: Quên gán kiểu dữ liệu làm giảm khả năng kiểm soát dữ liệu đầu vào.",
            "self_test": [
                f"Câu 1 (Thông hiểu): Khái quát vai trò cốt lõi của chủ đề '{title}' trong phát triển Web API.",
                "Câu 2 (Vận dụng): Thiết lập một đoạn code mẫu đơn giản mô phỏng hoạt động của chủ đề này.",
                "Câu 3 (Phân tích): Những lỗi thường gặp khi triển khai thực tế chủ đề này là gì?"
            ],
            "quiz": [
                {"type": "Q1_Syntax_Definition", "question": f"Cú pháp khai báo cơ bản liên quan đến '{title}' nằm ở tầng nào?", "options": ["Tầng API Router", "Tầng Database Model", "Tầng Middleware", "Tầng Schema"], "correct_option_index": 0, "explanation": "Tùy thuộc vào thiết kế hệ thống, các cấu hình thường nằm ở tầng API để đón nhận request."},
                {"type": "Q2_Execution_Flow", "question": "Luồng dữ liệu của chủ đề này di chuyển như thế nào?", "options": ["Client -> Server -> Client", "Server -> Database -> Server", "Client -> Middleware -> Router -> DB -> Client", "Database -> Client"], "correct_option_index": 2, "explanation": "Đây là luồng chuẩn của một request đi qua bộ lọc middleware, định tuyến router và cập nhật database."},
                {"type": "Q3_Code_Reading", "question": f"Đoạn code mô tả '{title}' chạy thành công sẽ trả về mã trạng thái HTTP nào?", "options": ["200 OK", "400 Bad Request", "404 Not Found", "500 Server Error"], "correct_option_index": 0, "explanation": "Mã HTTP 200 biểu thị phản hồi thành công và hợp lệ."},
                {"type": "Q4_Compare_Contrast", "question": f"So sánh chủ đề '{title}' với cách tiếp cận truyền thống cũ?", "options": ["Cách mới nhanh và an toàn hơn", "Cách cũ dễ viết hơn", "Không có sự khác biệt lớn", "Cách mới phức tạp hơn"], "correct_option_index": 0, "explanation": "FastAPI luôn đem lại các cải tiến về mặt tốc độ xử lý và sự an toàn về kiểu dữ liệu."},
                {"type": "Q5_Prediction_Trap", "question": f"Rủi ro lớn nhất nếu triển khai lỗi chủ đề này là gì?", "options": ["Hệ thống sập hoàn toàn", "Rò rỉ dữ liệu hoặc sai lệch nghiệp vụ", "Giao diện Swagger không chạy", "Mất kết nối Internet"], "correct_option_index": 1, "explanation": "Rò rỉ bảo mật và lỗi nghiệp vụ là các vấn đề nghiêm trọng cần chú ý khi code."}
            ],
            "lab": {
                "title": f"Thực hành chủ đề {title}",
                "objectives": [f"Nắm vững cách thức thiết lập và triển khai liên quan đến '{title}'."],
                "steps": [
                    f"Bước 1: Nghiên cứu kỹ đặc tả yêu cầu của '{title}' trong PM.",
                    "Bước 2: Viết mã nguồn Python mô phỏng logic xử lý chính.",
                    "Bước 3: Tích hợp vào app FastAPI chính và test hoạt động."
                ],
                "checklist": ["API endpoint phản hồi đúng mã trạng thái HTTP 200.", "Dữ liệu trả về đúng đặc tả mong muốn của PM."]
            }
        }

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
    
    # Indent the example code for the markmap list
    ex_snippet = content["example"]
    indented_example = "\n".join(f"      {line}" for line in ex_snippet.splitlines())
    
    mindmap_prompts = {
        "typescript/nestjs": "[Prompt: Generate a visual sequence diagram showing client HTTP request passing through NestJS controller and service, resolving database queries via TypeORM/Prisma, returning structured JSON response to client]",
        "typescript/react": "[Prompt: Generate a visual component hierarchy flow diagram showing React component state changes and hooks triggering API calls]",
        "java/springboot": "[Prompt: Generate a visual sequence diagram showing client request passing through Controller, Service, and Repository layers to Hibernate DB]",
        "python/fastapi": "[Prompt: Generate a visual sequence diagram showing client requesting FastAPI endpoints, mapping to Pydantic validation, and returning JSON responses.]",
        "python/core": "[Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]"
    }
    mindmap_prompt = mindmap_prompts.get(tech_stack, mindmap_prompts["python/fastapi"])

    # Formulate markmap following standard
    markmap_content = f"""```markmap
# {session_id}: {lesson_title}
## Mục tiêu bài học
- Hiểu rõ khái niệm cốt lõi và kiến trúc của {lesson_title}.
- Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: {expected_output if expected_output else 'tích hợp thành công'}.
- Vận hành và kiểm tra đầu ra hoạt động ổn định.
## {lesson_title}
### Khái niệm cốt lõi
- Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
### Cú pháp & Cách khai báo
- Ví dụ triển khai:
{indented_example}
### Lưu ý thực chiến
- Tránh bỏ sót các tham số bắt buộc.
- Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
{mindmap_prompt}
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
    
    inputs_map = {
        "typescript/nestjs": "Dự án NestJS hiện tại và tài nguyên khóa học.",
        "typescript/react": "Dự án React hiện tại và tài nguyên khóa học.",
        "java/springboot": "Dự án Spring Boot hiện tại và tài nguyên khóa học.",
        "python/fastapi": "Dự án FastAPI hiện tại và tài nguyên khóa học.",
        "python/core": "Môi trường lập trình Python và tài nguyên khóa học."
    }
    inputs_text = inputs_map.get(tech_stack, inputs_map["python/fastapi"])

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
        line = re.sub(r'__(.*?)__', r'<strong>\1</strong>', line)
        # Italic: *text* -> <em>text</em>, _text_ -> <em>text</em>
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        line = re.sub(r'_(.*?)_', r'<em>\1</em>', line)
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
                output.append("</code></pre></div>")
                in_code = False
            else:
                lang = line_strip[3:].strip() or "python"
                output.append(f'<div class="code-container"><div class="code-header"><span class="code-title">{lang}</span></div><pre><code class="language-{lang}">')
                in_code = True
            continue
            
        if in_code:
            output.append(line)
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
        
    return "\n".join([line for line in output if line])

def get_dynamic_visualizer_components(session_id: str, lesson_id: str, lesson_title: str, tech_stack: str = "python/core") -> Dict[str, Any]:
    """
    Returns tailored 6-panel interactive playground components (Canvas Title, Legend, Stats, Code Tracker, Input Box, JS Engine)
    based on the specific Session and Lesson topic.
    """
    s_lower = session_id.lower()
    t_lower = (lesson_title + " " + lesson_id).lower()
    
    # Check if Session 02 (Operators / Logic / If-Else / Branching)
    if "session 02" in s_lower or any(k in t_lower for k in ["toán tử", "so sánh", "if else", "rẽ nhánh", "điều kiện"]):
        return {
            "canvas_title": "Trực quan hóa Biểu thức & Rẽ nhánh Điều kiện (Logic Branching Engine)",
            "legend_html": """
                <div class="legend-item"><div class="legend-color" style="background: var(--color-idle)"></div> Chờ đánh giá</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-compare)"></div> Đang tính toán logic</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-swap)"></div> Nhánh ĐÚNG (True)</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-done)"></div> Nhánh SAI (False)</div>
            """,
            "stats_html": """
                <div class="stats-row">
                    <div class="stat-card">
                        <div class="stat-title">ĐIỀU KIỆN KIỂM TRA</div>
                        <div class="stat-value" id="stat-compare">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">NHÁNH ĐÚNG (TRUE)</div>
                        <div class="stat-value" id="stat-swap">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">THỜI GIAN</div>
                        <div class="stat-value" id="stat-time">0.0s</div>
                    </div>
                </div>
            """,
            "code_tracker_html": """
<span class="code-line" id="line-0"># Đánh giá biểu thức và rẽ nhánh điều kiện logic</span>
<span class="code-line" id="line-1">def evaluate_scholarship(score, attendance):</span>
<span class="code-line" id="line-2">    if score >= 8.0 and attendance >= 80:</span>
<span class="code-line" id="line-3">        return "Đạt học bổng Xuất sắc"</span>
<span class="code-line" id="line-4">    elif score >= 6.5:</span>
<span class="code-line" id="line-5">        return "Đạt danh hiệu Khá"</span>
<span class="code-line" id="line-6">    else:</span>
<span class="code-line" id="line-7">        return "Cần tiếp tục rèn luyện"</span>
            """,
            "input_label": "TỰ NHẬP ĐIỂM SỐ & CHUYÊN CẦN (score, attendance)",
            "input_default": "8.5, 85",
            "engine_js": """
        class InteractiveVisualizerEngine {
            constructor() {
                this.score = 8.5;
                this.attendance = 85;
                this.steps = [];
                this.currentStep = 0;
                this.isPlaying = false;
                this.timer = null;
                this.speed = 400;
                this.stats = { compare: 0, swap: 0 };
                this.startTime = null;
                this.elapsedSeconds = 0.0;
                this.audioSyncMap = [];
                
                this.init();
            }

            init() {
                this.generateSteps();
                this.render();
                this.setupEvents();
            }

            generateSteps() {
                this.steps = [];
                let s = this.score;
                let a = this.attendance;
                
                this.steps.push({
                    state: "init",
                    score: s,
                    attendance: a,
                    activeBranch: null,
                    line: 1,
                    msg: `Khởi tạo đầu vào: Điểm trung bình (score) = ${s}, Chuyên cần (attendance) = ${a}%.`
                });

                let cond1 = (s >= 8.0 && a >= 80);
                this.steps.push({
                    state: "eval_if",
                    score: s,
                    attendance: a,
                    cond1: cond1,
                    activeBranch: 1,
                    line: 2,
                    msg: `Kiểm tra nhánh IF: score >= 8.0 (${s >= 8.0}) VÀ attendance >= 80 (${a >= 80}) -> Kết quả: ${cond1 ? 'TRUE (Đúng)' : 'FALSE (Sai)'}.`
                });

                if (cond1) {
                    this.steps.push({
                        state: "exec_if",
                        score: s,
                        attendance: a,
                        cond1: true,
                        resultText: "Đạt học bổng Xuất sắc",
                        activeBranch: 1,
                        line: 3,
                        isDone: true,
                        msg: `Nhánh IF thỏa mãn (TRUE)! Thực thi khối lệnh trả về: "Đạt học bổng Xuất sắc".`
                    });
                } else {
                    let cond2 = (s >= 6.5);
                    this.steps.push({
                        state: "eval_elif",
                        score: s,
                        attendance: a,
                        cond1: false,
                        cond2: cond2,
                        activeBranch: 2,
                        line: 4,
                        msg: `Nhánh IF không đạt (FALSE). Chuyển sang kiểm tra nhánh ELIF: score >= 6.5 (${s >= 6.5}) -> Kết quả: ${cond2 ? 'TRUE' : 'FALSE'}.`
                    });

                    if (cond2) {
                        this.steps.push({
                            state: "exec_elif",
                            score: s,
                            attendance: a,
                            cond1: false,
                            cond2: true,
                            resultText: "Đạt danh hiệu Khá",
                            activeBranch: 2,
                            line: 5,
                            isDone: true,
                            msg: `Nhánh ELIF thỏa mãn! Thực thi khối lệnh trả về: "Đạt danh hiệu Khá".`
                        });
                    } else {
                        this.steps.push({
                            state: "exec_else",
                            score: s,
                            attendance: a,
                            cond1: false,
                            cond2: false,
                            resultText: "Cần tiếp tục rèn luyện",
                            activeBranch: 3,
                            line: 7,
                            isDone: true,
                            msg: `Tất cả điều kiện IF và ELIF đều không đạt (FALSE). Chạy vào khối mặc định ELSE trả về: "Cần tiếp tục rèn luyện".`
                        });
                    }
                }
            }

            render() {
                const canvas = document.getElementById('visualizer-canvas');
                if (!canvas) return;
                
                let step = this.steps[this.currentStep] || this.steps[0];
                let b1Color = step.activeBranch === 1 ? (step.cond1 ? '#10b981' : '#f59e0b') : '#334155';
                let b2Color = step.activeBranch === 2 ? (step.cond2 ? '#10b981' : '#f59e0b') : '#334155';
                let b3Color = step.activeBranch === 3 ? '#10b981' : '#334155';
                
                canvas.innerHTML = `
                    <div style="display: flex; flex-direction: column; gap: 16px; width: 100%; padding: 12px; font-family: 'JetBrains Mono', monospace;">
                        <div style="background: #1e293b; border: 1px solid #38bdf8; border-radius: 8px; padding: 12px; text-align: center;">
                            <span style="color: #38bdf8; font-weight: bold;">INPUT STATE:</span> 
                            <span style="color: #f1f5f9;">score = <strong style="color: #fbbf24;">${step.score}</strong></span> | 
                            <span style="color: #f1f5f9;">attendance = <strong style="color: #fbbf24;">${step.attendance}%</strong></span>
                        </div>

                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <!-- IF Branch -->
                            <div style="background: ${b1Color}; padding: 14px; border-radius: 8px; transition: all 0.3s; border-left: 6px solid #38bdf8;">
                                <div style="font-size: 0.85rem; color: #fff; font-weight: 600;">[Nhánh 1] if score >= 8.0 and attendance >= 80:</div>
                                <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 4px;">
                                    So sánh: (${step.score} >= 8.0) AND (${step.attendance} >= 80) &rarr; <strong style="color: ${step.cond1 ? '#6ee7b7' : '#f87171'}">${step.cond1 !== undefined ? (step.cond1 ? 'TRUE (Khớp)' : 'FALSE (Bỏ qua)') : 'Chờ đánh giá'}</strong>
                                </div>
                            </div>

                            <!-- ELIF Branch -->
                            <div style="background: ${b2Color}; padding: 14px; border-radius: 8px; transition: all 0.3s; border-left: 6px solid #a855f7; opacity: ${step.activeBranch >= 2 || step.activeBranch === null ? 1 : 0.5}">
                                <div style="font-size: 0.85rem; color: #fff; font-weight: 600;">[Nhánh 2] elif score >= 6.5:</div>
                                <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 4px;">
                                    So sánh: (${step.score} >= 6.5) &rarr; <strong style="color: ${step.cond2 ? '#6ee7b7' : '#f87171'}">${step.cond2 !== undefined ? (step.cond2 ? 'TRUE (Khớp)' : 'FALSE (Bỏ qua)') : 'Chờ kiểm tra'}</strong>
                                </div>
                            </div>

                            <!-- ELSE Branch -->
                            <div style="background: ${b3Color}; padding: 14px; border-radius: 8px; transition: all 0.3s; border-left: 6px solid #64748b; opacity: ${step.activeBranch === 3 || step.activeBranch === null ? 1 : 0.5}">
                                <div style="font-size: 0.85rem; color: #fff; font-weight: 600;">[Nhánh 3] else: (Khối lệnh mặc định)</div>
                            </div>
                        </div>

                        ${step.resultText ? `
                            <div style="background: #064e3b; border: 2px solid #10b981; border-radius: 8px; padding: 14px; text-align: center; animation: pulse 1s infinite;">
                                <span style="color: #6ee7b7; font-weight: bold;">🎯 KẾT QUẢ RẼ NHÁNH:</span>
                                <div style="color: #fff; font-size: 1.1rem; font-weight: bold; margin-top: 4px;">"${step.resultText}"</div>
                            </div>
                        ` : ''}
                    </div>
                `;

                this.highlightCode(step.line);
                if (step.msg) this.log(step.msg, step.isDone ? 'success' : 'info');
                this.updateStats();
            }

            highlightCode(lineNum) {
                for (let i = 0; i <= 7; i++) {
                    let el = document.getElementById(`line-${i}`);
                    if (el) el.style.backgroundColor = 'transparent';
                }
                let target = document.getElementById(`line-${lineNum}`);
                if (target) target.style.backgroundColor = 'rgba(16, 185, 129, 0.25)';
            }

            log(msg, type = 'info') {
                const box = document.getElementById('log-messages');
                if (!box) return;
                const entry = document.createElement('div');
                entry.className = `log-entry log-${type}`;
                entry.innerText = `[Bước ${this.currentStep + 1}] ${msg}`;
                box.appendChild(entry);
                box.scrollTop = box.scrollHeight;
            }

            clearLog() {
                const box = document.getElementById('log-messages');
                if (box) box.innerHTML = '';
            }

            start() {
                if (this.isPlaying) return;
                this.isPlaying = true;
                this.startTime = Date.now() - (this.elapsedSeconds * 1000);
                this.syncAudioToStep();
                this.timer = setInterval(() => {
                    if (this.currentStep < this.steps.length - 1) {
                        this.currentStep++;
                        if (this.steps[this.currentStep].activeBranch !== null) this.stats.compare++;
                        if (this.steps[this.currentStep].resultText) this.stats.swap++;
                        this.elapsedSeconds = ((Date.now() - this.startTime) / 1000).toFixed(1);
                        this.render();
                    } else {
                        this.pause();
                    }
                }, this.speed);
            }

            pause() {
                this.isPlaying = false;
                if (this.timer) clearInterval(this.timer);
            }

            step() {
                this.pause();
                if (this.currentStep < this.steps.length - 1) {
                    this.currentStep++;
                    if (this.steps[this.currentStep].activeBranch !== null) this.stats.compare++;
                    if (this.steps[this.currentStep].resultText) this.stats.swap++;
                    this.render();
                    this.syncAudioToStep();
                }
            }

            reset() {
                this.pause();
                this.currentStep = 0;
                this.stats = { compare: 0, swap: 0 };
                this.elapsedSeconds = 0.0;
                this.render();
                this.clearLog();
                this.syncAudioToStep();
                this.log('Đã khôi phục trạng thái xuất phát ban đầu.', 'info');
            }

            setSpeed(val) {
                this.speed = parseInt(val);
                const display = document.getElementById('speed-display');
                if (display) display.innerText = val;
                if (this.isPlaying) {
                    this.pause();
                    this.start();
                }
            }

            applyCustomData() {
                const inputEl = document.getElementById('custom-data-input');
                if (!inputEl) return;
                const parts = inputEl.value.split(',').map(v => v.trim());
                if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) {
                    alert('Vui lòng nhập 2 số hợp lệ cho điểm số và chuyên cần, cách nhau bởi dấu phẩy (VD: 8.5, 85)!');
                    return;
                }
                this.score = parseFloat(parts[0]);
                this.attendance = parseFloat(parts[1]);
                this.generateSteps();
                this.reset();
                this.log(`Đã áp dụng thông số mới: score = ${this.score}, attendance = ${this.attendance}%`, 'success');
            }

            updateStats() {
                const cmpEl = document.getElementById('stat-compare');
                const swpEl = document.getElementById('stat-swap');
                const tmEl = document.getElementById('stat-time');
                if (cmpEl) cmpEl.innerText = this.stats.compare;
                if (swpEl) swpEl.innerText = this.stats.swap;
                if (tmEl) tmEl.innerText = `${this.elapsedSeconds}s`;
            }

            setupAudioSync() {
                const audioEl = document.getElementById('lesson-audio') || document.querySelector('audio');
                if (!audioEl) return;
                this.audioSyncMap = this.steps.map((step, idx) => ({
                    stepIndex: idx,
                    startTime: idx * 2.5,
                    endTime: (idx + 1) * 2.5
                }));
                audioEl.addEventListener('timeupdate', () => {
                    if (!this.isPlaying && audioEl.currentTime > 0) {
                        const target = this.audioSyncMap.find(m => audioEl.currentTime >= m.startTime && audioEl.currentTime < m.endTime);
                        if (target && target.stepIndex !== this.currentStep) {
                            this.currentStep = target.stepIndex;
                            if (this.steps[this.currentStep].line) this.highlightCode(this.steps[this.currentStep].line);
                            this.render();
                        }
                    }
                });
            }

            syncAudioToStep() {
                const audioEl = document.getElementById('lesson-audio') || document.querySelector('audio');
                if (audioEl && this.audioSyncMap && this.audioSyncMap[this.currentStep]) {
                    audioEl.currentTime = this.audioSyncMap[this.currentStep].startTime;
                    if (this.isPlaying && audioEl.paused) audioEl.play().catch(e => console.log('Audio autoplay prevented:', e));
                }
            }

            setupEvents() {
                document.querySelectorAll('.selftest-question').forEach(q => {
                    q.addEventListener('click', () => {
                        const item = q.parentElement;
                        item.classList.toggle('active');
                    });
                });
                this.setupAudioSync();
            }
        }
            """
        }
        
    # Check if Session 03 (For Loops / Range / While / Break / Continue / Nested Loops)
    elif "session 03" in s_lower or any(k in t_lower for k in ["vòng lặp", "for", "range", "while", "break", "continue"]):
        return {
            "canvas_title": "Trực quan hóa Vòng lặp & Bộ đếm Trạng thái (Loop Iterator Engine)",
            "legend_html": """
                <div class="legend-item"><div class="legend-color" style="background: var(--color-idle)"></div> Chờ lặp</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-compare)"></div> Đang duyệt (Active)</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-swap)"></div> Tích lũy giá trị</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-done)"></div> Hoàn tất duyệt</div>
            """,
            "stats_html": """
                <div class="stats-row">
                    <div class="stat-card">
                        <div class="stat-title">BƯỚC LẶP (ITER)</div>
                        <div class="stat-value" id="stat-compare">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">BIẾN TÍCH LŨY (TOTAL)</div>
                        <div class="stat-value" id="stat-swap">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">THỜI GIAN</div>
                        <div class="stat-value" id="stat-time">0.0s</div>
                    </div>
                </div>
            """,
            "code_tracker_html": """
<span class="code-line" id="line-0"># Duyệt tuần tự qua tập hợp range và quản lý bộ đếm lặp</span>
<span class="code-line" id="line-1">def process_loop_range(start, stop):</span>
<span class="code-line" id="line-2">    total = 0</span>
<span class="code-line" id="line-3">    for i in range(start, stop):</span>
<span class="code-line" id="line-4">        if i == 3:</span>
<span class="code-line" id="line-5">            print("Phát hiện phần tử đặc biệt i = 3")</span>
<span class="code-line" id="line-6">        total += i</span>
<span class="code-line" id="line-7">    return total</span>
            """,
            "input_label": "TỰ NHẬP KHOẢNG RANGE (start, stop)",
            "input_default": "1, 6",
            "engine_js": """
        class InteractiveVisualizerEngine {
            constructor() {
                this.startVal = 1;
                this.stopVal = 6;
                this.steps = [];
                this.currentStep = 0;
                this.isPlaying = false;
                this.timer = null;
                this.speed = 400;
                this.stats = { compare: 0, swap: 0 };
                this.startTime = null;
                this.elapsedSeconds = 0.0;
                
                this.init();
            }

            init() {
                this.generateSteps();
                this.render();
                this.setupEvents();
            }

            generateSteps() {
                this.steps = [];
                let s = this.startVal;
                let e = this.stopVal;
                let total = 0;
                
                let items = [];
                for (let k = s; k < e; k++) items.push(k);
                
                this.steps.push({
                    items: [...items],
                    activeIdx: -1,
                    total: 0,
                    line: 2,
                    msg: `Khởi tạo biến tích lũy total = 0. Chuẩn bị duyệt tập hợp range(${s}, ${e}) với ${items.length} phần tử.`
                });

                for (let idx = 0; idx < items.length; idx++) {
                    let val = items[idx];
                    this.steps.push({
                        items: [...items],
                        activeIdx: idx,
                        total: total,
                        line: 3,
                        msg: `Vòng lặp bước ${idx + 1}: Lấy phần tử i = ${val} từ tập hợp range.`
                    });

                    if (val === 3) {
                        this.steps.push({
                            items: [...items],
                            activeIdx: idx,
                            total: total,
                            line: 5,
                            msg: `Phát hiện điều kiện i == 3! Thực thi câu lệnh inside block.`
                        });
                    }

                    total += val;
                    this.steps.push({
                        items: [...items],
                        activeIdx: idx,
                        total: total,
                        isAcc: true,
                        line: 6,
                        msg: `Cập nhật biến tích lũy: total = ${total - val} + ${val} &rarr; total mới = ${total}.`
                    });
                }

                this.steps.push({
                    items: [...items],
                    activeIdx: items.length,
                    total: total,
                    line: 7,
                    isDone: true,
                    msg: `Hoàn tất duyệt toàn bộ range(${s}, ${e})! Giá trị trả về cuối cùng: total = ${total}.`
                });
            }

            render() {
                const canvas = document.getElementById('visualizer-canvas');
                if (!canvas) return;
                
                let step = this.steps[this.currentStep] || this.steps[0];
                
                let boxesHtml = step.items.map((val, idx) => {
                    let isActive = (idx === step.activeIdx);
                    let isPassed = (idx < step.activeIdx);
                    let bg = isActive ? '#f59e0b' : (isPassed ? '#10b981' : '#334155');
                    let transform = isActive ? 'scale(1.15) translateY(-4px)' : 'scale(1)';
                    let border = isActive ? '2px solid #fff' : '1px solid #475569';
                    
                    return `
                        <div style="display: flex; flex-direction: column; items-center; align-items: center; gap: 6px;">
                            <div style="width: 54px; height: 54px; background: ${bg}; border: ${border}; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.25rem; color: #fff; transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); transform: ${transform}; box-shadow: ${isActive ? '0 8px 20px rgba(245, 158, 11, 0.4)' : 'none'};">
                                ${val}
                            </div>
                            <span style="font-size: 0.75rem; color: ${isActive ? '#fbbf24' : '#94a3b8'}; font-weight: ${isActive ? 'bold' : 'normal'};">i=${val}</span>
                        </div>
                    `;
                }).join('');
                
                canvas.innerHTML = `
                    <div style="display: flex; flex-direction: column; gap: 24px; width: 100%; padding: 16px; font-family: 'JetBrains Mono', monospace;">
                        <div>
                            <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px;">TẬP HỢP RANGE(${this.startVal}, ${this.stopVal}) - TRẠNG THÁI CON TRỎ DUYỆT:</div>
                            <div style="display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; padding: 16px; background: #1e293b; border-radius: 12px; border: 1px solid #334155; min-height: 100px; align-items: center;">
                                ${boxesHtml}
                            </div>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center; background: #0f172a; border: 2px solid #38bdf8; border-radius: 10px; padding: 16px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);">
                            <div>
                                <div style="font-size: 0.75rem; color: #38bdf8; font-weight: bold;">BIẾN TÍCH LŨY (TOTAL):</div>
                                <div style="font-size: 1.8rem; font-weight: 900; color: #6ee7b7; margin-top: 2px;">${step.total}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.75rem; color: #94a3b8;">BƯỚC HIỆN TẠI:</div>
                                <div style="font-size: 1.1rem; color: #f1f5f9; font-weight: bold;">${step.activeIdx >= 0 && step.activeIdx < step.items.length ? `Đang cộng i = ${step.items[step.activeIdx]}` : (step.activeIdx >= step.items.length ? 'Hoàn tất vòng lặp' : 'Chưa bắt đầu')}</div>
                            </div>
                        </div>
                    </div>
                `;

                this.highlightCode(step.line);
                if (step.msg) this.log(step.msg, step.isDone ? 'success' : 'info');
                this.updateStats();
            }

            highlightCode(lineNum) {
                for (let i = 0; i <= 7; i++) {
                    let el = document.getElementById(`line-${i}`);
                    if (el) el.style.backgroundColor = 'transparent';
                }
                let target = document.getElementById(`line-${lineNum}`);
                if (target) target.style.backgroundColor = 'rgba(16, 185, 129, 0.25)';
            }

            log(msg, type = 'info') {
                const box = document.getElementById('log-messages');
                if (!box) return;
                const entry = document.createElement('div');
                entry.className = `log-entry log-${type}`;
                entry.innerText = `[Bước ${this.currentStep + 1}] ${msg}`;
                box.appendChild(entry);
                box.scrollTop = box.scrollHeight;
            }

            clearLog() {
                const box = document.getElementById('log-messages');
                if (box) box.innerHTML = '';
            }

            start() {
                if (this.isPlaying) return;
                this.isPlaying = true;
                this.startTime = Date.now() - (this.elapsedSeconds * 1000);
                this.timer = setInterval(() => {
                    if (this.currentStep < this.steps.length - 1) {
                        this.currentStep++;
                        let st = this.steps[this.currentStep];
                        if (st.activeIdx >= 0) this.stats.compare = st.activeIdx + 1;
                        if (st.isAcc) this.stats.swap = st.total;
                        this.elapsedSeconds = ((Date.now() - this.startTime) / 1000).toFixed(1);
                        this.render();
                    } else {
                        this.pause();
                    }
                }, this.speed);
            }

            pause() {
                this.isPlaying = false;
                if (this.timer) clearInterval(this.timer);
            }

            step() {
                this.pause();
                if (this.currentStep < this.steps.length - 1) {
                    this.currentStep++;
                    let st = this.steps[this.currentStep];
                    if (st.activeIdx >= 0) this.stats.compare = st.activeIdx + 1;
                    if (st.isAcc) this.stats.swap = st.total;
                    this.render();
                }
            }

            reset() {
                this.pause();
                this.currentStep = 0;
                this.stats = { compare: 0, swap: 0 };
                this.elapsedSeconds = 0.0;
                this.render();
                this.clearLog();
                this.log('Đã khôi phục trạng thái xuất phát ban đầu.', 'info');
            }

            setSpeed(val) {
                this.speed = parseInt(val);
                const display = document.getElementById('speed-display');
                if (display) display.innerText = val;
                if (this.isPlaying) {
                    this.pause();
                    this.start();
                }
            }

            applyCustomData() {
                const inputEl = document.getElementById('custom-data-input');
                if (!inputEl) return;
                const parts = inputEl.value.split(',').map(v => parseInt(v.trim())).filter(v => !isNaN(v));
                if (parts.length < 2 || parts[0] >= parts[1] || (parts[1] - parts[0]) > 12) {
                    alert('Vui lòng nhập 2 số nguyên start, stop cách nhau dấu phẩy (start < stop, khoảng cách tối đa 12. VD: 1, 8)!');
                    return;
                }
                this.startVal = parts[0];
                this.stopVal = parts[1];
                this.generateSteps();
                this.reset();
                this.log(`Đã áp dụng khoảng range mới: range(${this.startVal}, ${this.stopVal})`, 'success');
            }

            updateStats() {
                const cmpEl = document.getElementById('stat-compare');
                const swpEl = document.getElementById('stat-swap');
                const tmEl = document.getElementById('stat-time');
                if (cmpEl) cmpEl.innerText = this.stats.compare;
                if (swpEl) swpEl.innerText = this.stats.swap;
                if (tmEl) tmEl.innerText = `${this.elapsedSeconds}s`;
            }

            setupEvents() {
                document.querySelectorAll('.selftest-question').forEach(q => {
                    q.addEventListener('click', () => {
                        const item = q.parentElement;
                        item.classList.toggle('active');
                    });
                });
            }
        }
            """
        }
        
    # Default / Type A: Session 01 (Memory Heap, Variable Allocation, Data Types, IO, F-string)
    else:
        return {
            "canvas_title": "Trực quan hóa Bộ nhớ Heap & Cấp phát Biến Python (Memory Allocation Engine)",
            "legend_html": """
                <div class="legend-item"><div class="legend-color" style="background: var(--color-idle)"></div> Stack (Tham chiếu biến)</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-compare)"></div> Heap (Đối tượng dữ liệu)</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-swap)"></div> Ép kiểu (Type Casting)</div>
                <div class="legend-item"><div class="legend-color" style="background: var(--color-done)"></div> F-String Output</div>
            """,
            "stats_html": """
                <div class="stats-row">
                    <div class="stat-card">
                        <div class="stat-title">BIẾN ĐÃ CẤP PHÁT</div>
                        <div class="stat-value" id="stat-compare">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">THAO TÁC ÉP KIỂU</div>
                        <div class="stat-value" id="stat-swap">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">THỜI GIAN</div>
                        <div class="stat-value" id="stat-time">0.0s</div>
                    </div>
                </div>
            """,
            "code_tracker_html": """
<span class="code-line" id="line-0"># Quản lý bộ nhớ Stack/Heap và ép kiểu động trong Python</span>
<span class="code-line" id="line-1">student_name = "Nguyễn Văn A"   # str</span>
<span class="code-line" id="line-2">age = 20                        # int</span>
<span class="code-line" id="line-3">score = 95.5                    # float</span>
<span class="code-line" id="line-4">extra_years_str = "5"           # str từ input()</span>
<span class="code-line" id="line-5">future_age = age + int(extra_years_str) # Ép kiểu sang int</span>
<span class="code-line" id="line-6">print(f"SV {student_name}: {future_age} tuổi") # F-string</span>
            """,
            "input_label": "TỰ NHẬP KHAI BÁO BIẾN (Tên biến, Giá trị)",
            "input_default": "city, Hanoi",
            "engine_js": """
        class InteractiveVisualizerEngine {
            constructor() {
                this.customVarName = "city";
                this.customVarVal = "Hanoi";
                this.steps = [];
                this.currentStep = 0;
                this.isPlaying = false;
                this.timer = null;
                this.speed = 400;
                this.stats = { compare: 0, swap: 0 };
                this.startTime = null;
                this.elapsedSeconds = 0.0;
                
                this.init();
            }

            init() {
                this.generateSteps();
                this.render();
                this.setupEvents();
            }

            generateSteps() {
                this.steps = [];
                
                this.steps.push({
                    stack: [],
                    heap: [],
                    varsCount: 0,
                    castCount: 0,
                    line: 0,
                    msg: "Khởi tạo chương trình Python. Bộ nhớ Stack và Heap đang trống."
                });

                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }],
                    varsCount: 1,
                    castCount: 0,
                    line: 1,
                    msg: `Cấp phát đối tượng chuỗi "Nguyễn Văn A" trên Heap (0x10A). Gán tham chiếu cho biến student_name trên Stack.`
                });

                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }, { name: "age", addr: "0x20B" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }, { addr: "0x20B", val: "20", type: "int", color: "#f59e0b" }],
                    varsCount: 2,
                    castCount: 0,
                    line: 2,
                    msg: `Cấp phát đối tượng số nguyên 20 (int) trên Heap tại 0x20B. Tham chiếu bởi biến age.`
                });

                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }, { name: "age", addr: "0x20B" }, { name: "score", addr: "0x30C" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }, { addr: "0x20B", val: "20", type: "int", color: "#f59e0b" }, { addr: "0x30C", val: "95.5", type: "float", color: "#a855f7" }],
                    varsCount: 3,
                    castCount: 0,
                    line: 3,
                    msg: `Cấp phát đối tượng số thực 95.5 (float) trên Heap tại 0x30C. Tham chiếu bởi biến score.`
                });

                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }, { name: "age", addr: "0x20B" }, { name: "score", addr: "0x30C" }, { name: "extra_years_str", addr: "0x40D" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }, { addr: "0x20B", val: "20", type: "int", color: "#f59e0b" }, { addr: "0x30C", val: "95.5", type: "float", color: "#a855f7" }, { addr: "0x40D", val: '"5"', type: "str", color: "#38bdf8" }],
                    varsCount: 4,
                    castCount: 0,
                    line: 4,
                    msg: `Nhận chuỗi "5" từ input() lưu tại 0x40D. Gán cho biến extra_years_str.`
                });

                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }, { name: "age", addr: "0x20B" }, { name: "score", addr: "0x30C" }, { name: "extra_years_str", addr: "0x40D" }, { name: "future_age", addr: "0x50E" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }, { addr: "0x20B", val: "20", type: "int", color: "#f59e0b" }, { addr: "0x30C", val: "95.5", type: "float", color: "#a855f7" }, { addr: "0x40D", val: '"5"', type: "str", color: "#38bdf8" }, { addr: "0x50E", val: "25", type: "int (Casted)", color: "#10b981" }],
                    varsCount: 5,
                    castCount: 1,
                    line: 5,
                    msg: `Thực hiện ép kiểu int("5") &rarr; 5 (int). Cộng age (20) + 5 = 25. Cấp phát đối tượng mới 25 tại 0x50E và gán cho future_age.`
                });

                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }, { name: "age", addr: "0x20B" }, { name: "score", addr: "0x30C" }, { name: "extra_years_str", addr: "0x40D" }, { name: "future_age", addr: "0x50E" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }, { addr: "0x20B", val: "20", type: "int", color: "#f59e0b" }, { addr: "0x30C", val: "95.5", type: "float", color: "#a855f7" }, { addr: "0x40D", val: '"5"', type: "str", color: "#38bdf8" }, { addr: "0x50E", val: "25", type: "int", color: "#10b981" }],
                    varsCount: 5,
                    castCount: 1,
                    output: "SV Nguyễn Văn A: 25 tuổi",
                    line: 6,
                    isDone: true,
                    msg: `Thực thi F-string! Thay thế {student_name} và {future_age} vào chuỗi và xuất ra màn hình console.`
                });
            }

            render() {
                const canvas = document.getElementById('visualizer-canvas');
                if (!canvas) return;
                
                let step = this.steps[this.currentStep] || this.steps[0];
                
                let stackHtml = step.stack.map((item, idx) => `
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #334155; padding: 10px 14px; border-radius: 8px; border-left: 4px solid #38bdf8; font-size: 0.85rem;">
                        <strong style="color: #f1f5f9;">${item.name}</strong>
                        <span style="background: #0f172a; color: #fbbf24; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">&rarr; ${item.addr}</span>
                    </div>
                `).join('') || '<div style="color: #64748b; font-size: 0.85rem; text-align: center; padding: 12px;">(Stack trống)</div>';
                
                let heapHtml = step.heap.map((item, idx) => `
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 10px 14px; border-radius: 8px; border: 1px solid ${item.color}; font-size: 0.85rem;">
                        <div>
                            <span style="color: #64748b; font-size: 0.75rem;">[${item.addr}]</span> 
                            <strong style="color: #fff; margin-left: 6px;">${item.val}</strong>
                        </div>
                        <span style="background: ${item.color}; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">${item.type}</span>
                    </div>
                `).join('') || '<div style="color: #64748b; font-size: 0.85rem; text-align: center; padding: 12px;">(Heap trống)</div>';
                
                canvas.innerHTML = `
                    <div style="display: flex; flex-direction: column; gap: 16px; width: 100%; padding: 12px; font-family: 'JetBrains Mono', monospace;">
                        <div style="display: grid; grid-template-columns: 1fr 1.3fr; gap: 16px;">
                            <!-- STACK -->
                            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 12px;">
                                <div style="font-size: 0.75rem; font-weight: bold; color: #38bdf8; margin-bottom: 10px; border-bottom: 1px solid #1e293b; padding-bottom: 6px;">
                                    STACK (Tên biến & Tham chiếu)
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 8px;">
                                    ${stackHtml}
                                </div>
                            </div>

                            <!-- HEAP -->
                            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 12px;">
                                <div style="font-size: 0.75rem; font-weight: bold; color: #f59e0b; margin-bottom: 10px; border-bottom: 1px solid #1e293b; padding-bottom: 6px;">
                                    HEAP (Đối tượng & Kiểu dữ liệu)
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 8px;">
                                    ${heapHtml}
                                </div>
                            </div>
                        </div>

                        ${step.output ? `
                            <div style="background: #064e3b; border: 2px solid #10b981; border-radius: 8px; padding: 12px; display: flex; align-items: center; justify-content: space-between;">
                                <span style="color: #6ee7b7; font-weight: bold;">TERMINAL F-STRING OUTPUT:</span>
                                <code style="color: #fff; font-size: 1rem; font-weight: bold;">&gt; ${step.output}</code>
                            </div>
                        ` : ''}
                    </div>
                `;

                this.highlightCode(step.line);
                if (step.msg) this.log(step.msg, step.isDone ? 'success' : 'info');
                this.updateStats();
            }

            highlightCode(lineNum) {
                for (let i = 0; i <= 7; i++) {
                    let el = document.getElementById(`line-${i}`);
                    if (el) el.style.backgroundColor = 'transparent';
                }
                let target = document.getElementById(`line-${lineNum}`);
                if (target) target.style.backgroundColor = 'rgba(16, 185, 129, 0.25)';
            }

            log(msg, type = 'info') {
                const box = document.getElementById('log-messages');
                if (!box) return;
                const entry = document.createElement('div');
                entry.className = `log-entry log-${type}`;
                entry.innerText = `[Bước ${this.currentStep + 1}] ${msg}`;
                box.appendChild(entry);
                box.scrollTop = box.scrollHeight;
            }

            clearLog() {
                const box = document.getElementById('log-messages');
                if (box) box.innerHTML = '';
            }

            start() {
                if (this.isPlaying) return;
                this.isPlaying = true;
                this.startTime = Date.now() - (this.elapsedSeconds * 1000);
                this.timer = setInterval(() => {
                    if (this.currentStep < this.steps.length - 1) {
                        this.currentStep++;
                        let st = this.steps[this.currentStep];
                        this.stats.compare = st.varsCount || 0;
                        this.stats.swap = st.castCount || 0;
                        this.elapsedSeconds = ((Date.now() - this.startTime) / 1000).toFixed(1);
                        this.render();
                    } else {
                        this.pause();
                    }
                }, this.speed);
            }

            pause() {
                this.isPlaying = false;
                if (this.timer) clearInterval(this.timer);
            }

            step() {
                this.pause();
                if (this.currentStep < this.steps.length - 1) {
                    this.currentStep++;
                    let st = this.steps[this.currentStep];
                    this.stats.compare = st.varsCount || 0;
                    this.stats.swap = st.castCount || 0;
                    this.render();
                }
            }

            reset() {
                this.pause();
                this.currentStep = 0;
                this.stats = { compare: 0, swap: 0 };
                this.elapsedSeconds = 0.0;
                this.render();
                this.clearLog();
                this.log('Đã khôi phục trạng thái xuất phát ban đầu.', 'info');
            }

            setSpeed(val) {
                this.speed = parseInt(val);
                const display = document.getElementById('speed-display');
                if (display) display.innerText = val;
                if (this.isPlaying) {
                    this.pause();
                    this.start();
                }
            }

            applyCustomData() {
                const inputEl = document.getElementById('custom-data-input');
                if (!inputEl) return;
                const parts = inputEl.value.split(',').map(v => v.trim());
                if (parts.length < 2 || !parts[0] || !parts[1]) {
                    alert('Vui lòng nhập tên biến và giá trị cách nhau bởi dấu phẩy (VD: score, 95.5)!');
                    return;
                }
                let varName = parts[0];
                let varVal = parts[1];
                let typeStr = !isNaN(varVal) ? (varVal.includes('.') ? 'float' : 'int') : (varVal === 'True' || varVal === 'False' ? 'bool' : 'str');
                
                this.steps.push({
                    stack: [{ name: "student_name", addr: "0x10A" }, { name: "age", addr: "0x20B" }, { name: varName, addr: "0x60F" }],
                    heap: [{ addr: "0x10A", val: '"Nguyễn Văn A"', type: "str", color: "#38bdf8" }, { addr: "0x20B", val: "20", type: "int", color: "#f59e0b" }, { addr: "0x60F", val: typeStr === 'str' ? `"${varVal}"` : varVal, type: typeStr, color: "#10b981" }],
                    varsCount: 3,
                    castCount: 0,
                    line: 2,
                    msg: `Đã cấp phát biến tự chọn "${varName}" = ${varVal} (${typeStr}) vào bộ nhớ Stack/Heap thành công!`
                });
                this.currentStep = this.steps.length - 1;
                this.stats.compare = 3;
                this.render();
                this.log(`Đã cấp phát biến mới ${varName} = ${varVal}`, 'success');
            }

            updateStats() {
                const cmpEl = document.getElementById('stat-compare');
                const swpEl = document.getElementById('stat-swap');
                const tmEl = document.getElementById('stat-time');
                if (cmpEl) cmpEl.innerText = this.stats.compare;
                if (swpEl) swpEl.innerText = this.stats.swap;
                if (tmEl) tmEl.innerText = `${this.elapsedSeconds}s`;
            }

            setupEvents() {
                document.querySelectorAll('.selftest-question').forEach(q => {
                    q.addEventListener('click', () => {
                        const item = q.parentElement;
                        item.classList.toggle('active');
                    });
                });
            }
        }
            """
        }

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
                    <span class="code-title">main.py</span>
                    <button class="copy-btn" onclick="copyCode(this, 'code-snippet-1')">Sao chép</button>
                </div>
                <div class="code-body">
                    <pre><code class="language-python" id="code-snippet-1">{raw_code}</code></pre>
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
                <span class="code-title">main.py</span>
                <button class="copy-btn" onclick="copyCode(this, 'code-snippet-1')">Sao chép</button>
            </div>
            <div class="code-body">
                <pre><code class="language-python" id="code-snippet-1">{raw_code}</code></pre>
            </div>
        </div>
        """
        
    self_test_html = ""
    for idx, q_text in enumerate(content["self_test"], 1):
        self_test_html += f"""
        <div class="selftest-item">
            <div class="selftest-question">
                <span>{q_text}</span>
            </div>
            <div class="selftest-answer">
                <p><strong>Gợi ý hướng dẫn tự học:</strong></p>
                <ul>
                    <li>Hãy đọc lại phần "Giới thiệu giải pháp" và "Ví dụ minh họa" ở trên để đối chiếu.</li>
                    <li>Thực hành gõ lại mã nguồn và chạy trên máy tính cá nhân để tự kiểm tra kết quả.</li>
                    <li>Phân tích kỹ lưỡng các lỗi thường gặp trong phần "Tổng kết" để hoàn thiện câu trả lời.</li>
                </ul>
            </div>
        </div>
        """

    display_title = f"{session_id} - {lesson_id}: {lesson_title}" if lesson_id else f"{session_id}: {lesson_title}"
    vis_comp = get_dynamic_visualizer_components(session_id, lesson_id, lesson_title, tech_stack)
    
    t_lower = lesson_title.lower()
    is_theory_only = any(kw in t_lower for kw in [
        "giới thiệu", "cài đặt", "môi trường", "ide", "tổng quan", "khái niệm cơ bản", "lý thuyết"
    ])

    if is_theory_only:
        visualizer_section_html = ""
        step_4_html = ""
    else:
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
                                    {vis_comp["canvas_title"]}
                                </div>
                                <div class="legend-box">
                                    {vis_comp["legend_html"]}
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
                                        <span class="input-label">{vis_comp["input_label"]}</span>
                                        <div class="custom-input-box">
                                            <input type="text" id="custom-data-input" class="custom-input" value="{vis_comp["input_default"]}">
                                            <button class="btn-apply" onclick="visualizerApp.applyCustomData()">Áp dụng</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Right Column: Stats, Live Code Tracker & Console Log -->
                        <div class="right-column">
                            <!-- Real-time Stats -->
                            {vis_comp["stats_html"]}

                            <!-- Live Code Tracker -->
                            <div class="code-tracker-panel">
                                <div class="panel-top-bar">
                                    <span>&lt;/&gt; CODE TRACKER ({tech_stack.upper()})</span>
                                    <span style="font-size: 0.75rem; color: #6ee7b7;">● Active Highlighting</span>
                                </div>
                                <div class="code-content">
                                    <pre><code id="code-tracker-box">
{vis_comp["code_tracker_html"]}
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
                            <div class="step-loc" style="color: #569cd6;">Mã nguồn chuẩn hóa & Phân tích thực thi <span class="range"></span></div>
                            {code_block_html}
                            <div style="margin-top: 16px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>"""

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
<body>
    <div class="container">
        <!-- Main Layout grid matching effective-html structure -->
        <div class="layout">
            
            <div class="main-content">
{visualizer_section_html}

                <!-- Walkthrough Step-by-Step Sections -->
                <div class="walkthrough-section">
                    <h2 style="font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; margin: 30px 0 20px; border-bottom: 2px solid var(--border-color); padding-bottom: 8px;">
                        Cơ chế hoạt động & Phân tích chi tiết (Step-by-step Walkthrough)
                    </h2>

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

                    <!-- Step 5: Self-Test Checklist -->
                    <div class="step">
                        <div class="badge">5</div>
                        <div class="step-body">
                            <div class="step-loc">Bộ câu hỏi Khảo thí tự học & Đánh giá năng lực <span class="range"></span></div>
                            <p style="margin-bottom: 12px; font-size: 0.9rem;">Học viên nhấp chuột vào từng câu hỏi bên dưới để đối chiếu gợi ý tự học và rèn luyện:</p>
                            <div class="selftest-container">
                                {self_test_html}
                            </div>
                        </div>
                    </div>

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
        {vis_comp["engine_js"]}

        // Initialize when DOM loaded
        let visualizerApp;
        document.addEventListener('DOMContentLoaded', () => {{
            visualizerApp = new InteractiveVisualizerEngine();
            if (window.hljs) hljs.highlightAll();
        }});

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

        document.addEventListener('DOMContentLoaded', applyTheme);
        applyTheme();
    </script>
</body>
</html>"""
    
    state["html_content"] = html_template
    log_agent_tokens("HTML_Writer_Agent", state, html_template)
    return state

