from core.state import AgentState
from agents.creators.common_utils import get_lesson_content, log_agent_tokens
import re

def slide_agent(state: AgentState) -> AgentState:
    """
    Slide Agent (Rikkei Master Presentation Engine):
    Tự động thiết kế Slide bài giảng HTML 16:9 sắc nét, chuẩn mực sư phạm doanh nghiệp theo slide_result/index.html.
    """
    from agents.slide_generator_agent import slide_generator_agent

    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "Lesson 01")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "slide_agent")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Quản lý phiên bản và phát triển phần mềm"
    lesson_details = core_ssot.get("lesson_details", "")

    # 1. Resolve Course Name Cleanly (Dynamic, Zero Hardcoding)
    course_name = core_ssot.get("course_name") or state.get("course_name") or state.get("subject_name") or core_ssot.get("subject_name")
    if not course_name:
        course_name = f"Chương trình đào tạo {tech_stack.title()}" if tech_stack else "Chương trình đào tạo chuyên sâu"
    
    acad_logs = [log for log in state.get("review_logs", []) if log["source"] == "Academic_Reviewer"]
    attempt_num = len(acad_logs) + 1
    feedback = acad_logs[-1]["feedback"] if acad_logs else ""
    
    print(f"\n[Slide_Agent] Generating Master HTML Slide Deck for {session_id} - {lesson_id}: {lesson_title} | Course: {course_name}")
    
    content = state.get("lesson_content")
    if not content:
        content = get_lesson_content(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            lesson_details=lesson_details,
            expected_output="",
            attempt_num=attempt_num,
            core_ssot=core_ssot,
            feedback=feedback,
            state=state
        )

    if not isinstance(content, dict):
        content = {}

    concepts = core_ssot.get("concepts", {})
    code_samples = core_ssot.get("code_samples", {})
    problem_desc = content.get("problem") or f"Vấn đề vận hành và quản lý khi làm việc nhóm nếu thiếu {lesson_title}."
    analysis_desc = content.get("analysis") or f"Phân tích nguyên lý vận hành và kiến trúc của {lesson_title}."
    solution_desc = content.get("solution") or f"Giải pháp triển khai tối ưu cho {lesson_title}."
    summary_desc = content.get("summary") or f"Tổng kết các điểm trọng tâm và lưu ý kỹ thuật cho {lesson_title}."

    concept_list = []
    if isinstance(concepts, dict):
        for cname, cdesc in concepts.items():
            concept_list.append(f"{cname}: {cdesc}")
    elif isinstance(concepts, list):
        concept_list = [str(c) for c in concepts]

    first_code = ""
    if isinstance(code_samples, dict) and code_samples:
        first_code = str(list(code_samples.values())[0])
    elif isinstance(code_samples, str) and code_samples:
        first_code = code_samples

    ts_lower = tech_stack.lower()
    is_cli_or_tooling = any(k in ts_lower for k in ["git", "terminal", "cli", "bash", "docker", "agile", "scrum", "uml", "figma", "ui", "design"])

    clean_lesson_name = lesson_title.strip()
    clean_lesson_name = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_lesson_name, flags=re.IGNORECASE).strip()
    clean_lesson_name = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_lesson_name, flags=re.IGNORECASE).strip()

    if not first_code or len(first_code) < 15:
        if is_cli_or_tooling:
            cli_bin = tech_stack.lower().split()[0] if tech_stack else "app"
            first_code = f"""# Thao tác vận hành công nghệ: {tech_stack}
# 1. Khởi tạo môi trường làm việc
$ {cli_bin} init

# 2. Kiểm tra trạng thái hệ thống
$ {cli_bin} status

# 3. Đưa tài nguyên vào luồng xử lý cho {clean_lesson_name}
$ {cli_bin} add .

# 4. Ghi nhận trạng thái vận hành
$ {cli_bin} commit -m "feat: triển khai module {clean_lesson_name}" """
        else:
            first_code = f"""# Mã nguồn thực chiến: {clean_lesson_name}
def execute_enterprise_module(config_data: dict) -> bool:
    \"\"\"Thực thi quy trình xử lý dữ liệu chuẩn doanh nghiệp.\"\"\"
    print(f"--- Khởi chạy module: {clean_lesson_name} ---")
    if not config_data:
        raise ValueError("Cấu hình không hợp lệ!")
    
    processed_status = True
    return processed_status

if __name__ == "__main__":
    init_config = {{"env": "production", "status": "active"}}
    execute_enterprise_module(init_config)"""

    p_text1 = concept_list[0] if len(concept_list) > 0 else problem_desc
    p_text2 = concept_list[1] if len(concept_list) > 1 else solution_desc
    p_text3 = concept_list[2] if len(concept_list) > 2 else analysis_desc

    # ── Scene 1: Problem vs Solution Bento Grid ─────────────────────────────
    slide_1_html = f"""
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch h-110">
        <div class="bento-card p-6 rounded-xl border border-red-200 bg-red-500/5 text-left flex flex-col justify-between relative overflow-hidden">
            <div class="select-none">
                <h5 class="font-bold text-red-900 text-[18px] flex items-center gap-1.5 mb-3">
                    <i class="ph-bold ph-x-circle text-lg"></i> Thách thức &amp; Hạn chế phương pháp cũ
                </h5>
                <p class="text-slate-800 text-[16px] leading-relaxed mb-3">
                    {p_text1}
                </p>
                <ul class="text-slate-700 text-[15px] space-y-1.5 list-disc pl-5">
                    <li>Hạn chế khi xử lý thủ công và dễ phát sinh xung đột dữ liệu.</li>
                    <li>Khó truy vết tác giả và thời điểm phát sinh sự cố hệ thống.</li>
                </ul>
            </div>
            <div class="mt-4 p-3 bg-red-100/60 border border-red-200 rounded-lg text-red-800 text-xs font-semibold">
                Rủi ro phát sinh lỗi và rào cản lớn khi mở rộng quy mô dự án.
            </div>
        </div>
        <div class="bento-card p-6 rounded-xl border border-emerald-200 bg-emerald-500/5 text-left flex flex-col justify-between relative overflow-hidden">
            <div class="select-none">
                <h5 class="font-bold text-emerald-900 text-[18px] flex items-center gap-1.5 mb-3">
                    <i class="ph-bold ph-check-circle text-lg"></i> Giải pháp hiện đại chuẩn doanh nghiệp
                </h5>
                <p class="text-slate-800 text-[16px] leading-relaxed mb-3">
                    {p_text2}
                </p>
                <ul class="text-slate-700 text-[15px] space-y-1.5 list-disc pl-5">
                    <li>Tự động hóa và chuẩn hóa quy trình vận hành hệ thống.</li>
                    <li>Cho phép phối hợp quy trình làm việc nhóm an toàn.</li>
                </ul>
            </div>
            <div class="mt-4 p-3 bg-emerald-100/60 border border-emerald-200 rounded-lg text-emerald-800 text-xs font-semibold">
                Tối ưu hóa hiệu năng và chuẩn hóa quy trình làm việc thực tế.
            </div>
        </div>
    </div>
"""

    # ── Scene 2: Dynamic Mermaid Workflow Diagram ───────────────────────────
    if is_cli_or_tooling:
        mermaid_diagram = f"""flowchart LR
    A["Không gian làm việc (Worktree)"] -- "Khởi tạo &amp; thêm tệp" --> B["Vùng đệm xử lý (Staging)"]
    B -- "Xác nhận ghi vết" --> C["Kho lưu trữ cục bộ (Local)"]
    C -- "Đồng bộ hệ thống" --> D["Kho lưu trữ tập trung (Remote)"]
    style A fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af;
    style B fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#92400e;
    style C fill:#f0fdf4,stroke:#22c55e,stroke-width:2px,color:#166534;
    style D fill:#fdf2f8,stroke:#ec4899,stroke-width:2px,color:#9d174d;"""
    else:
        mermaid_diagram = f"""flowchart TD
    A[Yêu cầu thực tế {clean_lesson_name}] --> B[Khởi tạo Module &amp; Cấu hình]
    B --> C[Thực thi Logic nghiệp vụ cốt lõi]
    C --> D[Kiểm tra ràng buộc &amp; Validation]
    D --> E[Xuất kết quả Console Output]
    style A fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af;
    style B fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#92400e;
    style C fill:#f0fdf4,stroke:#22c55e,stroke-width:2px,color:#166534;
    style E fill:#fdf2f8,stroke:#ec4899,stroke-width:2px,color:#9d174d;"""

    # ── Scene 3: Theory & Code Explainer ────────────────────────────────────
    code_lang = "bash" if is_cli_or_tooling else "python"
    slide_3_html = f"""
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full items-stretch h-110">
        <div class="flex flex-col justify-between text-left space-y-4">
            <div class="bento-card p-6 rounded-xl bg-slate-50 border border-slate-200 flex-1 flex flex-col justify-start">
                <h5 class="font-bold text-slate-900 text-[18px] mb-4 flex items-center gap-1.5">
                    <i class="ph-bold ph-warning text-rikkei-red"></i> Quy chuẩn thực thi &amp; Cảnh báo kỹ thuật
                </h5>
                <div class="space-y-4 text-slate-800 text-[16px]">
                    <div>
                        <div class="font-bold text-slate-900 text-[16px] mb-1">
                            • Quy tắc vận hành chuẩn:
                        </div>
                        <p class="text-slate-600 text-[15px]">{p_text3}</p>
                    </div>
                    <div>
                        <div class="font-bold text-slate-900 text-[16px] mb-1 mt-3">
                            • Phòng tránh sự cố thực chiến:
                        </div>
                        <p class="text-slate-600 text-[15px]">{summary_desc}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-col h-full">
            <pre class="bg-slate-50 text-slate-800 p-6 rounded-xl font-mono text-[13px] overflow-auto border border-slate-200 h-full flex flex-col justify-between shadow-sm"><code class="language-{code_lang}">{first_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</code></pre>
        </div>
    </div>
"""

    # ── Scene 4: 3-Column Enterprise Best Practices ──────────────────────────
    b_text1 = concept_list[0] if len(concept_list) > 0 else "Tuân thủ quy chuẩn đặt tên và cấu trúc mã nguồn."
    b_text2 = concept_list[1] if len(concept_list) > 1 else "Tối ưu hóa bộ nhớ và giảm thiểu chi phí tính toán."
    b_text3 = concept_list[2] if len(concept_list) > 2 else "Xây dựng bộ kiểm thử cho từng chức năng."

    slide_4_html = f"""
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full h-110 items-stretch">
        <div class="bento-card p-6 rounded-xl border border-red-200 bg-red-500/5 text-left flex flex-col justify-between">
            <div>
                <h5 class="font-bold text-red-900 text-[18px] mb-3 flex items-center gap-1.5"><i class="ph-bold ph-warning text-red-600"></i> Bẫy cú pháp &amp; Anti-pattern</h5>
                <p class="text-slate-800 text-[15px] leading-relaxed mt-2">{b_text1}</p>
            </div>
            <div class="mt-4 p-3 bg-red-100/60 border border-red-200 rounded-lg text-red-800 text-xs font-semibold">Cảnh báo rủi ro phát sinh lỗi.</div>
        </div>
        <div class="bento-card p-6 rounded-xl border border-blue-200 bg-blue-500/5 text-left flex flex-col justify-between">
            <div>
                <h5 class="font-bold text-blue-900 text-[18px] mb-3 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-blue-600"></i> Tối ưu hiệu năng</h5>
                <p class="text-slate-800 text-[15px] leading-relaxed mt-2">{b_text2}</p>
            </div>
            <div class="mt-4 p-3 bg-blue-100/60 border border-blue-200 rounded-lg text-blue-800 text-xs font-semibold">Tối ưu bộ nhớ &amp; tốc độ.</div>
        </div>
        <div class="bento-card p-6 rounded-xl border border-emerald-200 bg-emerald-500/5 text-left flex flex-col justify-between">
            <div>
                <h5 class="font-bold text-emerald-900 text-[18px] mb-3 flex items-center gap-1.5"><i class="ph-bold ph-check-circle text-emerald-600"></i> Chuẩn doanh nghiệp</h5>
                <p class="text-slate-800 text-[15px] leading-relaxed mt-2">{b_text3}</p>
            </div>
            <div class="mt-4 p-3 bg-emerald-100/60 border border-emerald-200 rounded-lg text-emerald-800 text-xs font-semibold">✅ Quy chuẩn dự án thực tế.</div>
        </div>
    </div>
"""

    scenes = [
        {
            "action_title": f"Bối cảnh dự án &amp; vấn đề cần giải quyết với {clean_lesson_name}",
            "scene_title": "Bối cảnh thực tế &amp; vấn đề",
            "short_title": "Đặt vấn đề &amp; Bối cảnh",
            "layout_type": "IMAGE_EXPLAINER",
            "image_url": "images/slide_lesson_01.png",
            "image_caption": f"Hình 1.1: Bối cảnh quy trình thực tế khi vận hành {clean_lesson_name}",
            "bullets": [
                f"Vấn đề thực tế: {p_text1}",
                f"Giải pháp áp dụng: {p_text2}"
            ]
        },
        {
            "action_title": f"Sơ đồ kiến trúc &amp; quy trình vận hành {clean_lesson_name}",
            "scene_title": "Sơ đồ kiến trúc hệ thống",
            "short_title": "Sơ đồ kiến trúc",
            "layout_type": "VISUAL_MINDMAP",
            "mindmap_center": f"Quy trình Core {clean_lesson_name[:30]}",
            "mindmap_branches": [
                {
                    "title": "Môi trường thực thi",
                    "icon": "ph-laptop",
                    "description": p_text1[:90] if p_text1 else "Khởi tạo thư mục và không gian làm việc chuẩn."
                },
                {
                    "title": "Luồng xử lý dữ liệu",
                    "icon": "ph-arrows-left-right",
                    "description": p_text2[:90] if p_text2 else "Kiểm soát trạng thái dữ liệu và logic hệ thống."
                },
                {
                    "title": "Quy chuẩn đóng gói",
                    "icon": "ph-database",
                    "description": p_text3[:90] if p_text3 else "Lưu trữ và đóng gói thành phần ứng dụng."
                },
                {
                    "title": "Phòng tránh lỗi",
                    "icon": "ph-shield-check",
                    "description": summary_desc[:90] if summary_desc else "Tuân thủ quy chuẩn kiểm thử và an toàn hệ thống."
                }
            ]
        },
        {
            "action_title": f"Thực thi mã nguồn &amp; quy trình vận hành {clean_lesson_name}",
            "scene_title": "Minh họa thực chiến &amp; thao tác kỹ thuật",
            "short_title": "Minh họa thực chiến",
            "layout_type": "CODE",
            "code_sample": first_code,
            "bullets": [
                f"Quy tắc vận hành chuẩn: {p_text3}",
                f"Phòng tránh sự cố thực tế: {summary_desc}"
            ]
        },
        {
            "action_title": "Lỗi thường gặp &amp; cách xử lý chuẩn",
            "scene_title": "Quy chuẩn &amp; lưu ý",
            "short_title": "Quy chuẩn &amp; lưu ý",
            "layout_type": "COMPARISON",
            "bad_practice": {
                "title": "Anti-Pattern: Thao tác thủ công &amp; bỏ qua ràng buộc",
                "code": f"Bỏ qua các bước kiểm tra ràng buộc khi triển khai {clean_lesson_name}",
                "reason": "Gây mất vết lịch sử chỉnh sửa và khó kiểm soát khi có sự cố."
            },
            "good_practice": {
                "title": "Best Practice: Chuẩn hóa &amp; tự động hóa quy trình",
                "code": f"Tuân thủ quy trình kiểm thử và tự động hóa cho {clean_lesson_name}",
                "reason": "Đảm bảo tính ổn định và tối ưu năng suất làm việc nhóm."
            }
        }
    ]

    # Stripping redundant prefixes from lesson_title for clean display
    clean_lesson_name = lesson_title.strip()
    clean_lesson_name = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_lesson_name, flags=re.IGNORECASE).strip()
    clean_lesson_name = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_lesson_name, flags=re.IGNORECASE).strip()

    # ── Dynamic Session Lessons Extraction (Zero Hardcoding) ────────────────────
    extracted_lessons = []
    
    # 1. From SSOT / State explicit session lessons list
    raw_lessons = (
        core_ssot.get("session_lessons") or
        core_ssot.get("lessons") or
        state.get("session_lessons") or
        state.get("lessons") or
        state.get("session_data", {}).get("lessons", [])
    )
    if isinstance(raw_lessons, list) and len(raw_lessons) > 0:
        for idx, item in enumerate(raw_lessons, 1):
            if isinstance(item, dict):
                t = item.get("title") or item.get("lesson_title") or item.get("name") or f"Bài học {idx}"
            else:
                t = str(item)
            clean_t = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', str(t), flags=re.IGNORECASE).strip()
            clean_t = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_t, flags=re.IGNORECASE).strip()
            if clean_t:
                extracted_lessons.append(clean_t)

    # 2. From content sub_topics / outline / sections
    if len(extracted_lessons) <= 1 and isinstance(content, dict):
        sub_t = content.get("sub_topics") or content.get("topics") or content.get("outline") or content.get("sections")
        if isinstance(sub_t, list) and len(sub_t) > 0:
            for item in sub_t:
                clean_t = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', str(item)).strip()
                if clean_t:
                    extracted_lessons.append(clean_t)

    # 3. Fallback to concept topics if available
    if len(extracted_lessons) <= 1 and concept_list and len(concept_list) >= 2:
        for c in concept_list:
            c_name = c.split(':', 1)[0].strip()
            if c_name and len(c_name) > 3:
                extracted_lessons.append(c_name)

    # Deduplicate extracted lesson titles
    unique_lessons = []
    for l in extracted_lessons:
        l_clean = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', l, flags=re.IGNORECASE).strip()
        l_clean = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', l_clean, flags=re.IGNORECASE).strip()
        if l_clean and l_clean not in unique_lessons:
            unique_lessons.append(l_clean)

    # Build multi-lesson lessons_data (3 dedicated visual scenes per lesson)
    if len(unique_lessons) > 1:
        lessons_data = []
        for idx, l_name in enumerate(unique_lessons, 1):
            l_scenes = [
                {
                    "action_title": "Bối Cảnh & Thách Thức Kỹ Thuật",
                    "scene_title": "Bối Cảnh & Thách Thức",
                    "short_title": "Bối cảnh thực tế",
                    "layout_type": "IMAGE_EXPLAINER",
                    "image_url": f"images/slide_lesson_{idx:02d}.png",
                    "image_caption": f"Hình {idx}.1: Bối cảnh sự cố và bối cảnh dự án cho {' '.join(l_name.split()[:4])}",
                    "bullets": [
                        f"Thách thức thực tế: Hạn chế của phương pháp thủ công khi làm việc với {' '.join(l_name.split()[:4])}.",
                        f"Giải pháp doanh nghiệp: Tự động hóa và chuẩn hóa quy trình xử lý dữ liệu."
                    ]
                },
                {
                    "action_title": "Sơ Đồ Tư Duy & Luồng Kiến Trúc",
                    "scene_title": "Sơ Đồ Tư Duy Kiến Trúc",
                    "short_title": "Sơ đồ tư duy",
                    "layout_type": "VISUAL_MINDMAP",
                    "mindmap_center": f"Core Kiến Trúc {' '.join(l_name.split()[:4])}",
                    "mindmap_branches": [
                        {"title": "Môi Trường", "icon": "ph-laptop", "description": f"Thiết lập không gian làm việc chuẩn cho {' '.join(l_name.split()[:3])}."},
                        {"title": "Xử Lý Dữ Liệu", "icon": "ph-arrows-left-right", "description": "Kiểm soát trạng thái tệp và lưu vết chọn lọc."},
                        {"title": "Quy Chuẩn", "icon": "ph-database", "description": "Lưu trữ snapshot lịch sử an toàn."},
                        {"title": "Kiểm Thử", "icon": "ph-shield-check", "description": "Phòng tránh lỗi rủi ro hệ thống."}
                    ]
                },
                {
                    "action_title": "So Sánh Quy Chuẩn vs Anti-Pattern",
                    "scene_title": "Quy Chuẩn & Anti-Pattern",
                    "short_title": "So sánh quy chuẩn",
                    "layout_type": "COMPARISON",
                    "bad_practice": {
                        "title": f"Thao tác thủ công & Bỏ qua ràng buộc",
                        "code": "Ghi đè thủ công hoặc không kiểm tra ràng buộc an toàn.",
                        "reason": "Dễ gây mất dữ liệu và rủi ro sự cố khi triển khai dự án."
                    },
                    "good_practice": {
                        "title": f"Chuẩn doanh nghiệp & Tự động hóa",
                        "code": "Sử dụng công cụ tự động hóa và Semantic Standards.",
                        "reason": "Tối ưu hóa 300% hiệu năng và đảm bảo an toàn tuyệt đối."
                    }
                }
            ]
            lessons_data.append({
                "lesson_id": f"Lesson {idx:02d}",
                "lesson_title": l_name,
                "scenes": l_scenes
            })
    else:
        lessons_data = [{
            "lesson_id": "Lesson 01",
            "lesson_title": clean_lesson_name,
            "scenes": scenes
        }]

    slides_html = slide_generator_agent.generate_deck_html(
        lesson_title=clean_lesson_name,
        module_name=course_name,
        scenes=scenes,
        lessons_data=lessons_data,
        core_ssot=core_ssot
    )

    pptx_bytes = slide_generator_agent.generate_deck_pptx(
        lesson_title=clean_lesson_name,
        module_name=course_name,
        scenes=scenes,
        lessons_data=lessons_data,
        core_ssot=core_ssot
    )

    state["slide_html"] = slides_html
    state["slide_markdown"] = slides_html
    state["slide_pptx_bytes"] = pptx_bytes
    log_agent_tokens("Slide_Agent", state, slides_html)
    return state
