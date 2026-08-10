import json
from core.state import AgentState
from core.llm import call_llm
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def format_lab_to_markdown(lab_data: dict) -> str:
    title = lab_data.get("title", "Bài thực hành")
    if not title.startswith("#"):
        title = f"# {title}"
        
    objectives = lab_data.get("objectives", [])
    obj_md = "\n".join([f"- {o}" for o in objectives]) if objectives else "- Nắm vững kiến thức bài học và thực hành mã nguồn."
    
    desc = lab_data.get("description", {})
    inputs_text = desc.get("inputs") if isinstance(desc, dict) else "Môi trường làm việc và mã nguồn bài học."
    steps = desc.get("steps") if isinstance(desc, dict) else []
    if not steps and isinstance(lab_data.get("steps"), list):
        steps = lab_data.get("steps")
        
    formatted_steps = []
    for idx, step in enumerate(steps, 1):
        clean_step = str(step).strip()
        if not clean_step.startswith(f"{idx}."):
            formatted_steps.append(f"{idx}. {clean_step}")
        else:
            formatted_steps.append(clean_step)
    steps_md = "\n".join(formatted_steps) if formatted_steps else "1. Thực hiện viết script bài học.\n2. Kiểm định kết quả trên console."
    
    eval_data = lab_data.get("evaluation", {})
    checklist = eval_data.get("checklist") if isinstance(eval_data, dict) else []
    if not checklist and isinstance(lab_data.get("checklist"), list):
        checklist = lab_data.get("checklist")
        
    formatted_checklist = []
    for item in checklist:
        clean_item = str(item).replace("[ ]", "").strip()
        formatted_checklist.append(f"- [ ] {clean_item}")
    checklist_md = "\n".join(formatted_checklist) if formatted_checklist else "- [ ] Mã nguồn thực thi không phát sinh lỗi cú pháp."
    
    md_content = f"""{title}

## 1. Mục tiêu
{obj_md}

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: {inputs_text}

### Các bước thực hiện:
{steps_md}

## 3. Checklist đánh giá
{checklist_md}
"""
    return md_content.strip()

def practical_lab_creator_agent(state: AgentState) -> AgentState:
    """
    Practical Lab Creator Agent:
    Tự động biên soạn nội dung Bài thực hành (Hands-on Practical Lab) cấp bài học 
    tuân thủ chuẩn sư phạm Rikkei Education và xuất ra định dạng Markdown (practical_lab.md).
    Lưu vào state['practical_lab_markdown'].
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "practical_lab_creator_agent")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Python Doanh Nghiệp"
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    print(f"\n[Practical_Lab_Agent] Formulating Practical Lab Markdown for {session_id} - {lesson_id}: {lesson_title}")
    
    content = state.get("lesson_content")
    if not content:
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
        
    lab_candidate = content.get("lab") if isinstance(content, dict) else None
    
    if isinstance(lab_candidate, dict) and lab_candidate.get("title") and lab_candidate.get("description"):
        lab_title = lab_candidate.get("title")
        lab_objectives = lab_candidate.get("objectives", [])
        steps = lab_candidate.get("steps") or (lab_candidate.get("description", {}).get("steps") if isinstance(lab_candidate.get("description"), dict) else [])
        inputs_text = lab_candidate.get("inputs") or (lab_candidate.get("description", {}).get("inputs") if isinstance(lab_candidate.get("description"), dict) else f"Môi trường phát triển {tech_stack} và mã nguồn bài học.")
        checklist = lab_candidate.get("checklist") or (lab_candidate.get("evaluation", {}).get("checklist") if isinstance(lab_candidate.get("evaluation"), dict) else [])
        
        if lab_title and lab_objectives and steps and checklist:
            lab_data = {
                "title": lab_title,
                "objectives": lab_objectives,
                "description": {
                    "inputs": inputs_text,
                    "steps": steps
                },
                "evaluation": {
                    "checklist": checklist
                }
            }
            lab_md = format_lab_to_markdown(lab_data)
            state["lab_json"] = lab_data
            state["practical_lab_markdown"] = lab_md
            log_agent_tokens("Practical_Lab_Agent", state, lab_md)
            return state

    # If SSOT lab content is missing or incomplete, call LLM to generate rich practical lab JSON
    system_prompt = f"""You are a Senior Technical Instructor at Rikkei Education.
Generate a practical lab assignment (Bài thực hành) tailored to {tech_stack} for: {lesson_title}.

MANDATORY DIRECTIVES:
1. Output MUST be 100% Accented Vietnamese.
2. STRICT NO EMOJI DIRECTIVE: No text emojis.
3. Content MUST match the specific technology stack ({tech_stack}). If tech stack is Git/GitHub, focus on Git CLI commands, repository lifecycle, and branch/commit workflow. DO NOT mention Python .venv or PEP 8 unless the tech stack is Python!
4. Return ONLY a single valid JSON object matching the required structure.
"""

    user_prompt = f"""Formulate Practical Lab for:
Session: {session_id}
Lesson: {lesson_id} - {lesson_title}
Curriculum Context: {lesson_details}
Expected Output: {expected_output}
Tech Stack: {tech_stack}

MANDATORY OUTPUT FORMAT (Return ONLY a single valid JSON object, no extra markdown text):
{{
  "title": "Bài thực hành: [Tên kịch bản thực tế ngắn gọn]",
  "objectives": [
    "Vận dụng kiến thức {tech_stack} để thực thi bài toán...",
    "Thành thạo thao tác thực hành và kiểm chuẩn kết quả..."
  ],
  "description": {{
    "inputs": "Môi trường phát triển {tech_stack} và tệp tài nguyên thực hành.",
    "steps": [
      "Bước 1: Khởi tạo không gian làm việc và chuẩn bị tài nguyên...",
      "Bước 2: Thực thi các câu lệnh/thao tác cốt lõi theo yêu cầu...",
      "Bước 3: Kiểm tra và xử lý các bẫy lỗi/tình huống phát sinh...",
      "Bước 4: Kiểm tra kết quả hiển thị và hoàn tất bài thực hành."
    ]
  }},
  "evaluation": {{
    "checklist": [
      "Thao tác thực thi thành công không phát sinh lỗi.",
      "Tuân thủ quy chuẩn mã nguồn/quy trình làm việc của {tech_stack}.",
      "Kết quả kiểm thử đạt yêu cầu bài toán."
    ]
  }}
}}
"""

    response_str = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Practical_Lab_Agent",
        session_id=session_id,
        lesson_id=lesson_id
    )

    try:
        lab_data = json.loads(response_str)
    except Exception:
        if "git" in tech_stack.lower() or "version control" in lesson_title.lower():
            steps = [
                f"Bước 1: Khởi tạo kho lưu trữ local hoặc chuyển sang làm việc trên repo dự án {tech_stack}.",
                f"Bước 2: Thực hiện các câu lệnh kiểm tra trạng thái và theo dõi phiên bản cho {lesson_title}.",
                "Bước 3: Thực hiện lưu vết commit và đẩy/đồng bộ thay đổi lên nhánh làm việc.",
                "Bước 4: Kiểm tra nhật ký lịch sử log và nghiệm thu kết quả thao tác."
            ]
            checklist = [
                f"Thao tác các lệnh {tech_stack} chính xác không phát sinh xung đột ngoài ý muốn.",
                "Lưu vết commit rõ ràng và kiểm tra trạng thái repo sạch (clean working tree)."
            ]
        else:
            steps = [
                f"Bước 1: Khởi tạo không gian làm việc và tệp mã nguồn cho bài học {lesson_title}.",
                f"Bước 2: Triển khai cấu trúc và viết mã nguồn tuân thủ chuẩn quy định {tech_stack}.",
                "Bước 3: Thực thi chương trình và kiểm tra các kịch bản thử nghiệm dữ liệu.",
                "Bước 4: Xuất kết quả báo cáo nghiệm thu ra màn hình console/giao diện."
            ]
            checklist = [
                f"Mã nguồn triển khai chuẩn xác theo yêu cầu {tech_stack}.",
                "Chương trình chạy ổn định và đưa ra kết quả chính xác."
            ]
            
        lab_data = {
            "title": f"Bài thực hành: Xây dựng kịch bản thực tế cho {lesson_title}",
            "objectives": [
                f"Nắm vững nguyên lý và vận dụng thực hành {lesson_title} trong dự án.",
                f"Làm chủ các thao tác và quy chuẩn phát triển với {tech_stack}."
            ],
            "description": {
                "inputs": f"Môi trường phát triển {tech_stack} và tệp tài nguyên thực hành.",
                "steps": steps
            },
            "evaluation": {
                "checklist": checklist
            }
        }

    lab_md = format_lab_to_markdown(lab_data)
    state["lab_json"] = lab_data
    state["practical_lab_markdown"] = lab_md
    log_agent_tokens("Practical_Lab_Agent", state, lab_md)
    return state
