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
    
    problem_req = lab_data.get("problem_statement") or lab_data.get("requirements") or ""
    problem_md = f"\n## 2. Yêu cầu bài toán\n{problem_req.strip()}\n" if problem_req else ""
    
    desc = lab_data.get("description", {})
    inputs_text = desc.get("inputs") if isinstance(desc, dict) else "Môi trường phát triển và mã nguồn bài học."
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
    steps_md = "\n".join(formatted_steps) if formatted_steps else "1. Bước 1: Khởi tạo môi trường.\n2. Bước 2: Viết mã nguồn và kiểm thử."
    
    ref_code = lab_data.get("reference_code") or lab_data.get("code_demo") or ""
    tech_stack = lab_data.get("tech_stack") or ""
    default_lang = tech_stack.split("/")[0].lower() if tech_stack else "text"
    code_block_lang = lab_data.get("tech_stack_lang") or default_lang
    code_md = f"\n## 4. Mã nguồn tham khảo (Code Demo)\n\n```{code_block_lang}\n{ref_code.strip()}\n```\n" if ref_code else ""
    
    eval_data = lab_data.get("evaluation", {})
    checklist = eval_data.get("checklist") if isinstance(eval_data, dict) else []
    if not checklist and isinstance(lab_data.get("checklist"), list):
        checklist = lab_data.get("checklist")
        
    formatted_checklist = []
    for item in checklist:
        clean_item = str(item).replace("[ ]", "").strip()
        formatted_checklist.append(f"- [ ] {clean_item}")
    checklist_md = "\n".join(formatted_checklist) if formatted_checklist else "- [ ] Mã nguồn thực thi không phát sinh lỗi cú pháp."
    
    section_num_steps = "3" if problem_md else "2"
    section_num_checklist = "5" if (problem_md and code_md) else ("4" if (problem_md or code_md) else "3")
    
    md_content = f"""{title}

## 1. Mục tiêu bài học
{obj_md}
{problem_md}
## {section_num_steps}. Các bước thực hiện
- **Tài nguyên đầu vào**: {inputs_text}

### Các bước thực hiện:
{steps_md}
{code_md}
## {section_num_checklist}. Checklist đánh giá kết quả
{checklist_md}
"""
    return md_content.strip()

def format_lab_to_html(lab_data: dict, tech_stack: str = "") -> str:
    raw_title = lab_data.get("title", "Bài thực hành").replace("#", "").strip()
    objectives = lab_data.get("objectives", [])
    obj_items = "\n".join([f'<li>{o}</li>' for o in objectives]) if objectives else '<li>Nắm vững kiến thức bài học và thực hành mã nguồn.</li>'
    
    problem_req = lab_data.get("problem_statement") or lab_data.get("requirements") or "Thực hiện cài đặt bài toán thực tế theo mô tả bài học."
    
    desc = lab_data.get("description", {})
    steps = desc.get("steps") if isinstance(desc, dict) else []
    if not steps and isinstance(lab_data.get("steps"), list):
        steps = lab_data.get("steps")
        
    step_items = []
    for idx, s in enumerate(steps, 1):
        clean_s = str(s).replace(f"Bước {idx}:", "").strip()
        step_items.append(f'''<div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-sm flex items-start gap-3">
  <span class="w-6 h-6 rounded-full bg-rikkei-red text-white font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">{idx}</span>
  <div>
    <strong class="text-slate-900">Bước {idx}</strong>
    <p class="text-xs text-slate-600 mt-0.5">{clean_s}</p>
  </div>
</div>''')
    steps_html = "\n".join(step_items) if step_items else '<div>Thực hiện theo hướng dẫn bài học.</div>'

    ref_code = lab_data.get("reference_code") or lab_data.get("code_demo") or "# Viết mã nguồn thực hành tại đây..."
    ref_code_escaped = ref_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    eval_data = lab_data.get("evaluation", {})
    checklist = eval_data.get("checklist") if isinstance(eval_data, dict) else []
    if not checklist and isinstance(lab_data.get("checklist"), list):
        checklist = lab_data.get("checklist")
        
    check_items = []
    for item in checklist:
        clean_item = str(item).replace("[ ]", "").strip()
        check_items.append(f'''<label class="flex items-start gap-3 cursor-pointer text-sm text-slate-700 select-none">
  <input type="checkbox" class="w-4 h-4 rounded border-slate-300 text-rikkei-red focus:ring-rikkei-red mt-0.5" />
  <span>{clean_item}</span>
</label>''')
    checklist_html = "\n".join(check_items) if check_items else '<div>Mã nguồn thực thi không có lỗi.</div>'

    stack_clean = tech_stack.lower().strip()
    is_python_stack = "python" in stack_clean
    lang_class = stack_clean.split("/")[0] if stack_clean else "text"

    pyodide_script = '<script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>' if is_python_stack else ''

    return f"""<!DOCTYPE html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{raw_title} - Rikkei Education</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        theme: {{
          extend: {{
            colors: {{
              rikkei: {{ red: "#be111c", darkred: "#90000a", dark: "#0f172a" }}
            }},
            fontFamily: {{
              sans: ["Inter", "system-ui", "sans-serif"],
              montserrat: ["Montserrat", "sans-serif"],
              mono: ["JetBrains Mono", "monospace"]
            }}
          }}
        }}
      }};
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    {pyodide_script}
    <style>
      code:not(.hljs):not([class*="language"]) {{
        background-color: #f1f5f9 !important;
        color: #be111c !important;
        padding: 0.125rem 0.375rem !important;
        border-radius: 0.25rem !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 0.875rem !important;
      }}
      [contenteditable="true"], [contenteditable="true"] *, code[contenteditable="true"], code[contenteditable="true"] * {{
        outline: none !important; border: none !important; box-shadow: none !important; background-color: transparent !important;
      }}
      code[contenteditable="true"] {{
        display: block !important; white-space: pre !important; overflow-x: auto !important;
        font-family: "JetBrains Mono", monospace !important; font-size: 0.875rem !important;
        line-height: 1.6 !important; color: #0f172a !important; padding: 1rem !important; background: #f8fafc !important; border-radius: 0.5rem !important;
      }}
    </style>
  </head>
  <body class="bg-slate-50 text-base text-slate-800 font-sans leading-relaxed min-h-screen">
    <header class="fixed top-0 left-0 right-0 h-16 bg-white/95 backdrop-blur-md border-b border-slate-200 z-40">
      <div class="max-w-6xl mx-auto h-full px-6 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Rikkei Academy Logo" class="h-9 object-contain" />
          <span class="text-sm font-semibold text-slate-500 border-l border-slate-300 pl-4">{raw_title}</span>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 pt-24 pb-16">
      <article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-10 shadow-sm">
        <div class="border-b border-slate-200 pb-6 mb-8">
          <h1 class="font-montserrat font-bold text-2xl sm:text-3xl text-slate-900 leading-tight">{raw_title}</h1>
          <p class="text-sm text-slate-500 mt-2">Thực hành chỉnh sửa dữ liệu và chạy trực tiếp mã nguồn ngay trên trình duyệt.</p>
        </div>

        <section class="mb-10">
          <h2 class="font-montserrat font-bold text-xl text-slate-900 mb-4">1. Mục tiêu bài học</h2>
          <ul class="list-disc pl-5 space-y-2 text-slate-700 text-sm">{obj_items}</ul>
        </section>

        <section class="mb-10">
          <h2 class="font-montserrat font-bold text-xl text-slate-900 mb-4">2. Yêu cầu bài toán</h2>
          <div class="p-5 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 text-sm leading-relaxed">
            {problem_req}
          </div>
        </section>

        <section class="mb-10">
          <h2 class="font-montserrat font-bold text-xl text-slate-900 mb-4">3. Các bước thực hiện</h2>
          <div class="space-y-3">{steps_html}</div>
        </section>

        <section class="mb-10">
          <h2 class="font-montserrat font-bold text-xl text-slate-900 mb-4">4. Mã nguồn tham khảo &amp; Thực thi trực tiếp</h2>
          <div class="border border-slate-200 rounded-2xl overflow-hidden shadow-sm my-4 bg-slate-50">
            <div class="px-5 py-3 bg-slate-100 border-b border-slate-200 flex justify-end items-center text-xs font-semibold text-slate-700 gap-2">
              <button onclick="resetSandboxCode()" class="px-3 py-1.5 bg-slate-200 text-slate-700 rounded hover:bg-slate-300 transition-all font-bold">
                Khôi phục mã gốc
              </button>
              <button onclick="runLabCode()" class="px-4 py-1.5 bg-rikkei-red text-white rounded hover:bg-rikkei-darkred transition-all font-bold shadow-sm">
                Chạy chương trình
              </button>
            </div>
            <div class="p-4 bg-slate-50 font-mono text-sm">
              <pre class="m-0"><code id="lab-code-editor" class="language-{lang_class}" contenteditable="true" spellcheck="false">{ref_code_escaped}</code></pre>
            </div>
            <div class="bg-slate-900 text-emerald-400 p-5 border-t border-slate-700 font-mono text-xs">
              <div class="text-slate-400 mb-2 font-bold flex items-center justify-between">
                <span>KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
              </div>
              <pre id="lab-console-output" class="m-0 text-emerald-400 whitespace-pre-wrap leading-relaxed">[Nhấn 'Chạy chương trình' để thực thi mã nguồn trên trình duyệt...]</pre>
            </div>
          </div>
        </section>

        <section class="mb-6">
          <h2 class="font-montserrat font-bold text-xl text-slate-900 mb-4">5. Checklist đánh giá kết quả</h2>
          <div class="p-5 rounded-xl border border-slate-200 bg-slate-50 space-y-3">{checklist_html}</div>
        </section>
      </article>
    </main>

    <script>
      document.addEventListener("DOMContentLoaded", () => {{ if (window.hljs) window.hljs.highlightAll(); }});
      let pyodideInstance = null;
      async function getPyodide() {{
        if (!pyodideInstance && window.loadPyodide) pyodideInstance = await window.loadPyodide();
        return pyodideInstance;
      }}
      async function runLabCode() {{
        const editor = document.getElementById("lab-code-editor");
        const output = document.getElementById("lab-console-output");
        if (!editor || !output) return;
        const code = editor.innerText || editor.textContent;
        const isPython = "{'true' if is_python_stack else 'false'}" === "true";
        if (isPython) {{
          output.innerText = "⏳ Đang nạp Pyodide WASM Engine và thực thi...";
          try {{
            const pyodide = await getPyodide();
            let buffer = "";
            pyodide.setStdout({{ batched: (str) => {{ buffer += str + "\\n"; }} }});
            pyodide.setStderr({{ batched: (str) => {{ buffer += "ERROR: " + str + "\\n"; }} }});
            await pyodide.runPythonAsync(code);
            output.innerText = buffer.trim() || "Thực thi hoàn tất!";
          }} catch (err) {{
            output.innerText = "❌ LỖI THỰC THI:\\n" + err;
          }}
        }} else {{
          output.innerText = "▶ Kiểm tra cú pháp mã nguồn {lang_class}: Đã ghi nhận mã nguồn thực hành!";
        }}
      }}
    </script>
  </body>
</html>"""

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
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Ứng dụng Doanh Nghiệp"
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
    from core.prompts import render_prompt
    from core.utils.llm_parser import extract_json_from_response
    from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt

    session_domain_data = state.get("session_domain") or get_domain_for_session(session_id)
    chosen_domain = state.get("chosen_domain") or session_domain_data.get("name_vi", "Hệ thống Doanh nghiệp")
    domain_prompt_block = format_domain_rules_for_prompt(session_domain_data)

    # Scope-contract: was previously never wired into this generator at all (unlike reading and
    # blueprint generation), which is the confirmed root cause of real scope leakage — a Session
    # 2 JS lab listed DOM API/Fetch API/Async-Await as objectives, concepts taught 9-11 sessions
    # later. `state["allowed_scope"]`/`state["forbidden_scope"]` are already computed per-lesson
    # by workflow_cmd.py (calculate_lesson_scope_contract) — this just needs to read them.
    allowed_scope_raw = state.get("allowed_scope") or state.get("previous_lessons") or []
    allowed_scope = ", ".join(str(x) for x in allowed_scope_raw if str(x).strip()) if isinstance(allowed_scope_raw, list) else str(allowed_scope_raw).strip()
    forbidden_scope_raw = state.get("forbidden_scope") or []
    forbidden_scope = ", ".join(str(x) for x in forbidden_scope_raw if str(x).strip()) if isinstance(forbidden_scope_raw, list) else str(forbidden_scope_raw).strip()

    system_prompt = render_prompt(
        "practical_lab_creator.j2",
        {
            "tech_stack": tech_stack,
            "lesson_title": lesson_title,
            "chosen_domain": chosen_domain,
            "domain_prompt_block": domain_prompt_block,
            "allowed_scope": allowed_scope,
            "forbidden_scope": forbidden_scope
        }
    )

    blueprint = state.get("lesson_blueprint")
    if blueprint:
        blueprint_context = f"""Dữ liệu phác thảo bài học (Lesson Blueprint):
- Kịch bản thống nhất: {json.dumps(blueprint.get('real_world_scenario', {}), ensure_ascii=False)}
- Ví dụ thực tế nâng cao (Hãy thiết kế bài Lab thực hành tương tự hoặc nâng cấp từ ví dụ 3.3 này): {json.dumps(blueprint.get('progressive_examples', [])[-1], ensure_ascii=False) if blueprint.get('progressive_examples') else ''}
- Lỗi thường gặp: {json.dumps(blueprint.get('gotchas_and_errors', []), ensure_ascii=False)}
"""
    else:
        blueprint_context = ""

    user_prompt = f"""{blueprint_context}
Formulate Practical Lab for:
Session: {session_id}
Lesson: {lesson_id} - {lesson_title}
Curriculum Context: {lesson_details}
Expected Output: {expected_output}
Tech Stack: {tech_stack}
Allowed Knowledge Scope: {allowed_scope or 'Fundamentals up to current lesson'}
Forbidden Knowledge Scope (STRICTLY PROHIBITED): {forbidden_scope or 'Future unlearned tech/syntax'}
"""

    response_str = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Practical_Lab_Agent",
        session_id=session_id,
        lesson_id=lesson_id
    )

    lab_data = extract_json_from_response(response_str)
    if not isinstance(lab_data, dict) or not lab_data.get("title"):
        # Generic fallback (LLM response was unusable) — was previously a special-cased branch
        # keyed on `"git" in tech_stack.lower()`, a hard-coded course/tech-specific carve-out
        # that violates the platform's "never hardcode course/tech-specific values" principle.
        # This single generic template already reads naturally for any stack/tool via the
        # dynamic {tech_stack}/{lesson_title} interpolation below.
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
    lab_html = format_lab_to_html(lab_data, tech_stack)
    state["lab_json"] = lab_data
    state["practical_lab_markdown"] = lab_md
    state["practical_lab_html"] = lab_html

    # Lightweight, non-blocking post-generation audits — mirrors the same pattern already added
    # to reading generation (reading_creator.py). Does not retry/reject; only surfaces content
    # bleed or domain drift via logs instead of it going completely unnoticed.
    forbidden_set_for_audit = set(str(x).strip().lower() for x in forbidden_scope_raw if str(x).strip()) if isinstance(forbidden_scope_raw, list) else set()
    if forbidden_set_for_audit:
        try:
            from core.scope_calculator import validate_text_against_scope
            scope_violations = validate_text_against_scope(lab_md, forbidden_set_for_audit, tech_stack)
            if scope_violations:
                print(f"  [Practical_Lab_Agent Scope Audit Warning] {session_id} - {lesson_id}: nội dung có thể đã dùng khái niệm chưa học: {scope_violations}")
        except Exception as e:
            print(f"  [Practical_Lab_Agent Scope Audit Notice] Could not run scope audit: {e}")

    if chosen_domain and chosen_domain.strip() and chosen_domain.lower() not in lab_md.lower():
        print(f"  [Practical_Lab_Agent Domain Audit Warning] {session_id} - {lesson_id}: domain thống nhất '{chosen_domain}' không xuất hiện trong nội dung sinh ra — có thể LLM đã lệch sang bối cảnh khác.")

    log_agent_tokens("Practical_Lab_Agent", state, lab_md)
    return state
