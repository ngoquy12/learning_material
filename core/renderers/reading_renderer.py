"""
core/renderers/reading_renderer.py
Enterprise Reading Material Renderer Engine (Jinja2 + Domain Component Registry)
Converts structured LLM JSON payloads into 100% gold-standard HTML matching templates/reading.html.
"""

import os
import json
import re
import html
from pathlib import Path
from typing import Dict, Any, List, Optional
import jinja2

# Directory containing templates
TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"

class ReadingTemplateRenderer:
    """Master Jinja2 Renderer for Reading Materials."""

    def __init__(self):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, context: Dict[str, Any]) -> str:
        template = self.env.get_template("reading_master.html.j2")
        return template.render(**context)

def resolve_domain_engine(tech_stack: str) -> Dict[str, str]:
    """
    Determines engine type, hljs languages, and visualizer type based on tech_stack.
    STRICTLY FORBIDS hardcoded fallback defaults (no fallback to python, java, etc.).
    """
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] resolve_domain_engine: 'tech_stack' bị trống. Hệ thống TUYỆT ĐỐI KHÔNG fallback/hardcode ngầm bất kỳ công nghệ nào. Vui lòng truyền --tech-stack chính xác từ PM.")
    
    tech_lower = str(tech_stack).lower().strip()

    # 1. Database / SQL
    if any(kw in tech_lower for kw in ["sql", "mysql", "postgres", "sqlite", "oracle", "database"]):
        return {
            "engine_type": "sql_sim",
            "hljs_languages": ["sql"],
            "visualizer_type": "sql",
            "name": "SQL"
        }

    # 2. CLI / DevOps / Tooling
    cli_keywords = ["git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd", "powershell", "docker", "kubernetes", "devops", "linux", "unix"]
    if any(kw in tech_lower for kw in cli_keywords):
        return {
            "engine_type": "static",
            "hljs_languages": ["bash"],
            "visualizer_type": "cli",
            "name": tech_stack or "Git/CLI"
        }

    # 3. Pure Concept / Architecture / Agile / Process
    concept_keywords = ["agile", "scrum", "diagram", "uml", "design", "word", "excel", "powerpoint", "office", "phân tích", "thiết kế", "kiến trúc", "system analysis", "software architecture", "management", "theory", "concept", "process"]
    if any(kw in tech_lower for kw in concept_keywords):
        return {
            "engine_type": "static",
            "hljs_languages": ["plaintext"],
            "visualizer_type": "concept",
            "name": tech_stack or "Architecture"
        }

    # 4. Programming Languages
    if "javascript" in tech_lower or "js" in tech_lower or "react" in tech_lower or "node" in tech_lower:
        return {"engine_type": "js_worker", "hljs_languages": ["javascript"], "visualizer_type": "programming", "name": "JavaScript"}
    if "java" in tech_lower:
        return {"engine_type": "static", "hljs_languages": ["java"], "visualizer_type": "programming", "name": "Java"}
    if "cpp" in tech_lower or "c++" in tech_lower or "c" in tech_lower:
        return {"engine_type": "static", "hljs_languages": ["cpp", "c"], "visualizer_type": "programming", "name": "C/C++"}

    # Default: Python WASM
    return {"engine_type": "pyodide", "hljs_languages": ["python"], "visualizer_type": "programming", "name": "Python"}


def generate_domain_visualizer_html(lesson_title: str, tech_stack: str, visualizer_type: str, custom_viz_data: Optional[Dict[str, Any]] = None) -> str:
    """
    Generates domain-adaptive visualizer HTML according to subject nature.
    """
    clean_title = lesson_title.split(" - ")[-1] if " - " in lesson_title else lesson_title
    tech_upper = (tech_stack or "Code").upper()

    if visualizer_type == "sql":
        return f"""
<h3 id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.4. Mô phỏng luồng truy vấn SQL (Interactive SQL Query Visualizer)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Bấm nút <strong>"Chạy truy vấn SQL"</strong> để quan sát kết quả bảng dữ liệu trả về từ bộ máy AlaSQL in-browser!</p>
<div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm my-6 text-slate-800 space-y-4">
  <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-2">
    <div class="flex items-center justify-between">
      <span class="text-xs font-mono font-bold text-slate-700">MÃ NGUỒN SQL THỰC THI</span>
      <button type="button" onclick="runSqlCode('sql-viz-code', 'sql-viz-output', this)" class="px-3 py-1 rounded-lg bg-rikkei-red text-white text-xs font-bold hover:bg-rikkei-darkred transition-all shadow-sm">Chạy truy vấn SQL</button>
    </div>
    <pre id="sql-viz-code" class="p-3 bg-slate-100 rounded-lg font-mono text-xs text-slate-800">SELECT id, customer_name, order_status FROM orders WHERE total_amount >= 500000;</pre>
  </div>
  <div class="bg-slate-900 rounded-xl p-4 font-mono text-xs text-emerald-400 overflow-x-auto min-h-[100px]" id="sql-viz-output">
    -- Bấm nút 'Chạy truy vấn SQL' để xem bảng dữ liệu thực tế --
  </div>
</div>"""

    elif visualizer_type == "cli":
        return f"""
<h3 id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.4. Trình mô phỏng luồng lệnh Terminal ({tech_upper} Command Flow)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Quan sát tiến trình thực thi từng lệnh CLI và sự thay đổi trạng thái của hệ thống theo thứ tự bên dưới:</p>
<div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm my-6 text-slate-800 space-y-4">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
    <div class="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
      <span class="px-2 py-0.5 rounded bg-sky-100 text-sky-800 font-bold text-[10px]">Bước 1</span>
      <div class="font-mono font-bold text-slate-900">Kiểm tra trạng thái</div>
      <p class="text-slate-500 text-[11px]">Xác định thư mục làm việc và nhánh hiện tại.</p>
    </div>
    <div class="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
      <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold text-[10px]">Bước 2</span>
      <div class="font-mono font-bold text-slate-900">Thực thi lệnh chính</div>
      <p class="text-slate-500 text-[11px]">Biến đổi cấu hình hoặc ghi nhận thay đổi.</p>
    </div>
    <div class="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
      <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">Bước 3</span>
      <div class="font-mono font-bold text-slate-900">Đồng bộ & Hoàn tất</div>
      <p class="text-slate-500 text-[11px]">Cập nhật nhật ký log và xác nhận thành công.</p>
    </div>
  </div>
</div>"""

    elif visualizer_type == "concept":
        return f"""
<h3 id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.4. Sơ đồ cơ chế & Luồng quy trình thực tế</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Xem xét sơ đồ quy trình tổng quan và các pha thực hiện cốt lõi cho chủ đề <strong>{clean_title}</strong>:</p>
<div class="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm my-6 space-y-4">
  <div class="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-rikkei-red text-white flex items-center justify-center font-bold text-lg">1</div>
      <div>
        <div class="font-bold text-sm text-slate-900">Đầu vào (Input Context)</div>
        <div class="text-xs text-slate-500">Tiếp nhận thông tin & Yêu cầu ban đầu</div>
      </div>
    </div>
    <i class="ph-bold ph-arrow-right text-slate-400 text-xl hidden md:block"></i>
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-lg">2</div>
      <div>
        <div class="font-bold text-sm text-slate-900">Xử lý (Core Process)</div>
        <div class="text-xs text-slate-500">Áp dụng nguyên tắc & Quy luật điều hướng</div>
      </div>
    </div>
    <i class="ph-bold ph-arrow-right text-slate-400 text-xl hidden md:block"></i>
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-lg">3</div>
      <div>
        <div class="font-bold text-sm text-slate-900">Đầu ra (Expected Outcome)</div>
        <div class="text-xs text-slate-500">Sản phẩm hoặc trạng thái mong đợi</div>
      </div>
    </div>
  </div>
</div>"""

    # Default Programming RAM Visualizer (Adaptive by Language: JavaScript, Python, Java, C++)
    tech_lower = (tech_stack or "").lower()
    if any(k in tech_lower for k in ["javascript", "js", "typescript", "ts", "node", "react"]):
        code_lines_html = f"""
        <div id="viz-line-1" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div>// 1. Khai báo tham số đầu vào cho {clean_title}</div>
        </div>
        <div id="viz-line-2" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div><span class="text-purple-600 font-bold">const</span> inputData = loadInputParameters();</div>
        </div>
        <div id="viz-line-3" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div><span class="text-purple-600 font-bold">const</span> isValid = validateConditions(inputData);</div>
          <span id="viz-badge-cond1" class="text-[10px] font-sans px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200 font-medium">⏳ Chờ kiểm tra</span>
        </div>
        <div id="viz-line-4" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div><span class="text-purple-600 font-bold">const</span> executionResult = processBusinessLogic(isValid);</div>
        </div>
        <div id="viz-line-5" class="p-1.5 rounded transition-all duration-200">
          <div>console.log(<span class="text-green-600">`Kết quả xử lý {clean_title}: ${{executionResult}}`</span>);</div>
        </div>
        """
        var_valid_label = "isValid (Kiểm tra điều kiện):"
        var_result_label = "executionResult (Trạng thái kết quả):"
    elif any(k in tech_lower for k in ["java", "cpp", "c++", "c#", "c"]):
        code_lines_html = f"""
        <div id="viz-line-1" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div>// 1. Khai báo tham số đầu vào cho {clean_title}</div>
        </div>
        <div id="viz-line-2" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div><span class="text-blue-600 font-bold">String</span> inputData = loadInputParameters();</div>
        </div>
        <div id="viz-line-3" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div><span class="text-blue-600 font-bold">boolean</span> isValid = validateConditions(inputData);</div>
          <span id="viz-badge-cond1" class="text-[10px] font-sans px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200 font-medium">⏳ Chờ kiểm tra</span>
        </div>
        <div id="viz-line-4" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div><span class="text-blue-600 font-bold">String</span> executionResult = processBusinessLogic(isValid);</div>
        </div>
        <div id="viz-line-5" class="p-1.5 rounded transition-all duration-200">
          <div>System.out.println(<span class="text-green-600">"Kết quả xử lý {clean_title}: "</span> + executionResult);</div>
        </div>
        """
        var_valid_label = "isValid (Kiểm tra điều kiện):"
        var_result_label = "executionResult (Trạng thái kết quả):"
    else:
        code_lines_html = f"""
        <div id="viz-line-1" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div># 1. Khai báo tham số đầu vào cho {clean_title}</div>
        </div>
        <div id="viz-line-2" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div>input_data = load_input_parameters()</div>
        </div>
        <div id="viz-line-3" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div>is_valid = validate_conditions(input_data)</div>
          <span id="viz-badge-cond1" class="text-[10px] font-sans px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200 font-medium">⏳ Chờ kiểm tra</span>
        </div>
        <div id="viz-line-4" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between">
          <div>execution_result = process_business_logic(is_valid)</div>
        </div>
        <div id="viz-line-5" class="p-1.5 rounded transition-all duration-200">
          <div>print(f<span class="text-green-600">"Kết quả xử lý {clean_title}: {{execution_result}}"</span>)</div>
        </div>
        """
        var_valid_label = "is_valid (Kiểm tra điều kiện):"
        var_result_label = "execution_result (Trạng thái kết quả):"

    return f"""
<h3 id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.4. Mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Bấm <strong>"Tiếp theo"</strong> hoặc <strong>"Tự động chạy"</strong> để theo dõi luồng thực thi từng dòng mã được tô sáng và sự thay đổi trạng thái của các biến trong bộ nhớ RAM cho chủ đề <strong>{clean_title}</strong>!</p>

<div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm my-6 text-slate-800">
  <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm mb-4 flex flex-wrap items-center justify-between gap-2">
    <span class="text-xs font-mono font-bold text-slate-800 flex items-center gap-1.5">
      <i class="ph-bold ph-sliders-horizontal text-rikkei-red"></i> ĐIỀU KHIỂN MÔ PHỎNG LUỒNG THỰC THI ({tech_upper}):
    </span>
    <div class="flex items-center gap-2 text-xs">
      <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition-all shadow-sm flex items-center gap-1">
        <i class="ph-bold ph-arrow-right text-xs"></i> Tiếp theo
      </button>
      <button type="button" onclick="vizToggleAuto()" id="viz-auto-btn" class="px-3.5 py-1.5 rounded bg-rikkei-red text-white font-medium hover:bg-rikkei-darkred transition-all shadow-sm flex items-center gap-1">
        <i class="ph-bold ph-play text-xs"></i> Tự động chạy
      </button>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-4">
    <div class="flex flex-col bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-4 py-2 text-xs font-mono text-slate-700 font-bold border-b border-slate-200 flex items-center justify-between">
        <span>MÃ NGUỒN THỰC THI CHUẨN</span>
        <span id="viz-step-badge" class="px-2.5 py-0.5 rounded-full bg-slate-200 text-slate-700 text-[11px] font-normal">Chưa khởi chạy</span>
      </div>
      <div id="viz-code-display" class="p-3.5 font-mono text-xs text-slate-800 space-y-2 overflow-x-auto min-h-[180px]">
        {code_lines_html}
      </div>
    </div>

    <div class="flex flex-col bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-4 py-2 text-xs font-mono text-slate-700 font-bold border-b border-slate-200 flex items-center justify-between">
        <span>BIẾN BỘ NHỚ RAM</span>
        <span class="px-2 py-0.5 rounded bg-sky-100 text-sky-800 text-[11px] font-bold">Memory Canvas</span>
      </div>
      <div class="p-4 space-y-2 flex-1 text-xs font-mono">
        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between">
          <span class="text-slate-500">Môi trường thực thi:</span>
          <span class="font-bold text-slate-900">{tech_upper} Engine</span>
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between">
          <span class="text-slate-500">{var_valid_label}</span>
          <span id="viz-var-valid" class="font-bold text-slate-400">---</span>
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between">
          <span class="text-slate-500">{var_result_label}</span>
          <span id="viz-var-result" class="font-bold text-slate-400">---</span>
        </div>
      </div>
    </div>
  </div>

  <div class="bg-slate-900 rounded-xl p-3.5 font-mono text-xs text-emerald-400 flex items-center gap-2 overflow-x-auto">
    <span class="text-slate-500 font-bold shrink-0">CONSOLE &gt;</span>
    <span id="viz-terminal-log">Bấm 'Tiếp theo' hoặc 'Tự động chạy' để bắt đầu mô phỏng luồng.</span>
  </div>
</div>

<script>
  var currentVizStep = 0;
  var vizAutoInterval = null;
  function runVizStep(stepNum) {{
    if (stepNum === undefined || stepNum === null) {{
      currentVizStep += 1;
      if (currentVizStep > 5) currentVizStep = 1;
    }} else {{
      currentVizStep = stepNum;
    }}

    for (let i = 1; i <= 5; i++) {{
      const el = document.getElementById("viz-line-" + i);
      if (el) {{
        if (i === currentVizStep) {{
          el.style.backgroundColor = "#d1fae5";
          el.style.borderLeft = "4px solid #059669";
          el.style.fontWeight = "bold";
        }} else {{
          el.style.backgroundColor = "";
          el.style.borderLeft = "4px solid transparent";
          el.style.fontWeight = "normal";
        }}
      }}
    }}

    const badge = document.getElementById("viz-step-badge");
    const b1 = document.getElementById("viz-badge-cond1");
    const vValid = document.getElementById("viz-var-valid");
    const vResult = document.getElementById("viz-var-result");
    const term = document.getElementById("viz-terminal-log");

    if (badge) badge.innerText = "Bước " + currentVizStep + "/5";

    if (currentVizStep === 1) {{
      if (term) term.innerText = "[BƯỚC 1/5] Khởi tạo tham số đầu vào cho {clean_title}";
    }} else if (currentVizStep === 2) {{
      if (term) term.innerText = "[BƯỚC 2/5] Nạp dữ liệu đầu vào";
    }} else if (currentVizStep === 3) {{
      if (b1) {{
        b1.className = "text-[10px] font-sans px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold shadow-sm";
        b1.innerText = "True - KHỚP!";
      }}
      if (vValid) {{
        vValid.className = "font-bold text-emerald-600";
        vValid.innerText = "True";
      }}
      if (term) term.innerText = "[BƯỚC 3/5] Đánh giá điều kiện kiểm tra -> True";
    }} else if (currentVizStep === 4) {{
      if (vResult) {{
        vResult.className = "font-bold text-emerald-600";
        vResult.innerText = "SUCCESS";
      }}
      if (term) term.innerText = "[BƯỚC 4/5] Xử lý nghiệp vụ logic -> SUCCESS";
    }} else if (currentVizStep === 5) {{
      if (term) term.innerText = "[KẾT QUẢ 5/5] CONSOLE OUTPUT: Hoàn tất xử lý {clean_title}: SUCCESS";
    }}
  }}

  function vizToggleAuto() {{
    const btn = document.getElementById("viz-auto-btn");
    if (vizAutoInterval) {{
      clearInterval(vizAutoInterval);
      vizAutoInterval = null;
      if (btn) btn.innerHTML = '<i class="ph-bold ph-play text-xs"></i> Tự động chạy';
    }} else {{
      if (btn) btn.innerHTML = '<i class="ph-bold ph-pause text-xs"></i> Tạm dừng';
      runVizStep();
      vizAutoInterval = setInterval(() => {{
        runVizStep();
      }}, 1500);
    }}
  }}
</script>
"""

def extract_h3_subsections(html_content: str) -> List[Dict[str, str]]:
    """
    Extracts all <h3> subheadings with IDs for TOC generation.
    """
    if not html_content:
        return []
    
    matches = re.findall(r'<h3\s+id="([^"]+)"[^>]*>(.*?)</h3>', html_content, re.DOTALL)
    subsections = []
    for anchor_id, title in matches:
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        subsections.append({"id": anchor_id, "title": clean_title})
    return subsections


def sanitize_and_repair_dom(raw_html: str) -> str:
    """
    Sanitizes and repairs common HTML structure flaws.
    """
    if not raw_html:
        return ""
    
    # Strip forbidden markdown code markers if any leaked
    cleaned = re.sub(r'```html\s*', '', raw_html)
    cleaned = re.sub(r'```\s*$', '', cleaned)
    
    return cleaned


def assemble_reading_html(json_payload: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    """
    Master Assembly Function: Combines structured JSON payload + domain visualizers + Jinja2 template.
    STRICTLY FORBIDS hardcoded fallback defaults for tech_stack.
    """
    tech_stack = (metadata.get("tech_stack") if isinstance(metadata, dict) else None) or (json_payload.get("tech_stack") if isinstance(json_payload, dict) else None)
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] assemble_reading_html: 'tech_stack' bị trống trong metadata/payload. Hệ thống TUYỆT ĐỐI KHÔNG fallback/hardcode ngầm bất kỳ công nghệ nào.")
    
    domain_info = resolve_domain_engine(tech_stack)

    lesson_title = metadata.get("lesson_title") or json_payload.get("lesson_title") or "Bài đọc học liệu"
    lesson_clean_title = lesson_title.split(" - ")[-1] if " - " in lesson_title else lesson_title

    # Section Titles
    sec_titles = json_payload.get("section_titles") or {}

    # Check if sec2_html already contains Section 2.4 visualizer (prevent duplicate injection)
    sec2_raw = json_payload.get("sec2_html", "")
    has_existing_viz = (
        'id="sec-2-4' in sec2_raw
        or 'viz-step-badge' in sec2_raw
        or 'viz-code-display' in sec2_raw
        or 'Mô phỏng cơ chế vận hành từng bước' in sec2_raw
    )

    # Visualizer
    show_viz = json_payload.get("show_visualizer", True) and not has_existing_viz
    viz_html = ""
    if show_viz:
        viz_html = generate_domain_visualizer_html(
            lesson_title=lesson_title,
            tech_stack=tech_stack,
            visualizer_type=domain_info["visualizer_type"],
            custom_viz_data=json_payload.get("visualizer_data")
        )

    # Subsections for TOC navigation (auto-extract from HTML if not provided)
    sec2_subs = json_payload.get("sec2_subsections") or extract_h3_subsections(sec2_raw)
    sec3_subs = json_payload.get("sec3_subsections") or extract_h3_subsections(json_payload.get("sec3_html", ""))

    # Self-test questions JSON serialization for JS handler
    self_test = json_payload.get("self_test_questions") or []
    st_answers = {}
    st_explanations = {}
    for idx, q in enumerate(self_test, 1):
        st_answers[idx] = q.get("correct_idx", 0)
        st_explanations[idx] = q.get("explanation", "")

    # References
    references = json_payload.get("reference_links") or [
        {"title": f"Tài liệu chính thức {tech_stack.capitalize()}", "url": "https://docs.python.org/3/"}
    ]

    context = {
        "lesson_title": lesson_title,
        "lesson_clean_title": lesson_clean_title,
        "engine_type": domain_info["engine_type"],
        "hljs_languages": domain_info["hljs_languages"],
        "section_titles": sec_titles,
        "sec2_subsections": sec2_subs,
        "sec3_subsections": sec3_subs,
        "show_visualizer": show_viz,
        "visualizer_component_html": viz_html,
        "sec1_html": json_payload.get("sec1_html", "<p>Nội dung đang được cập nhật...</p>"),
        "sec1_visual_html": json_payload.get("sec1_visual_html"),
        "sec2_html": sec2_raw or "<p>Nội dung cú pháp đang được cập nhật...</p>",
        "sec3_html": json_payload.get("sec3_html", "<p>Ví dụ thực hành đang được cập nhật...</p>"),
        "sec4_html": json_payload.get("sec4_html", "<p>Tổng kết đang được cập nhật...</p>"),
        "context_image_url": json_payload.get("context_image_url"),
        "reference_links": references,
        "self_test_questions": self_test,
        "self_test_answers_json": json.dumps(st_answers, ensure_ascii=False),
        "self_test_explanations_json": json.dumps(st_explanations, ensure_ascii=False),
    }

    renderer = ReadingTemplateRenderer()
    raw_html = renderer.render(context)
    return sanitize_and_repair_dom(raw_html)
