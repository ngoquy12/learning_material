"""
core/renderers/reading/visualizer_component.py
Section 2.4 Domain-Adaptive Step-by-Step Execution Visualizer Component Builder.
"""

import re
import json
import html
from typing import Dict, Any, List
from core.renderers.reading.code_sandbox_renderer import highlight_code_syntax, get_clean_language_name

def generate_fallback_visualizer_steps(code_lines: List[str], variables: List[Any], lesson_title: str) -> List[Dict[str, Any]]:
    """
    Generates intelligent step data if LLM omitted or provided incomplete steps.
    Extracts variable mutations and step explanations in 100% Accented Vietnamese.
    """
    steps = []
    curr_ram = {}
    
    var_slug_map = {}
    for v in variables:
        if isinstance(v, dict):
            name = v.get("name", "var")
            slug = re.sub(r'[^a-zA-Z0-9_-]', '-', name).lower()
            var_slug_map[name] = slug
        elif isinstance(v, str):
            slug = re.sub(r'[^a-zA-Z0-9_-]', '-', v).lower()
            var_slug_map[v] = slug

    for idx, raw_line in enumerate(code_lines, 1):
        line = str(raw_line).strip()
        if not line or line.startswith("//") or line.startswith("#") or line.startswith("/*") or line.startswith("*") or line in ("}", "};"):
            continue
            
        step_ram = dict(curr_ram)
        step_badge = ""
        
        assign_match = re.search(r'(?:const|let|var)?\s*([a-zA-Z0-9_$]+)\s*=\s*(.+?);?$', line)
        if assign_match:
            v_name = assign_match.group(1).strip()
            v_val = assign_match.group(2).strip()
            v_val = re.sub(r'\s*//.*$', '', v_val).rstrip(';').strip()
            slug = var_slug_map.get(v_name, re.sub(r'[^a-zA-Z0-9_-]', '-', v_name).lower())
            step_ram[slug] = v_val[:30]
            curr_ram[slug] = v_val[:30]
            step_badge = f"{v_name} = {v_val[:20]}"
            step_log = f"&gt; [Bước {len(steps)+1}] Khởi tạo/gán giá trị: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800 font-bold'>{html.escape(v_name)} = {html.escape(v_val[:30])}</code>"
        elif "function" in line or "def " in line:
            fn_match = re.search(r'(?:function|def)\s+([a-zA-Z0-9_$]+)', line)
            fn_name = fn_match.group(1) if fn_match else "hàm"
            step_badge = f"Định nghĩa {fn_name}()"
            step_log = f"&gt; [Bước {len(steps)+1}] Định nghĩa hàm: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800 font-bold'>{html.escape(fn_name)}()</code>"
        elif "return" in line:
            ret_val = line.replace("return", "").strip().rstrip(";")
            step_badge = f"return {ret_val[:15]}"
            step_log = f"&gt; [Bước {len(steps)+1}] Trả về kết quả: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800 font-bold'>{html.escape(ret_val[:30])}</code>"
        elif "console.log" in line or "print(" in line or "System.out.print" in line:
            step_badge = "Xuất Console"
            step_log = f"&gt; [Bước {len(steps)+1}] Xuất dữ liệu ra màn hình Console"
        else:
            step_badge = "Thực thi"
            step_log = f"&gt; [Bước {len(steps)+1}] Thực thi dòng lệnh: <code class='px-1 py-0.5 bg-slate-100 rounded text-slate-800'>{html.escape(line[:40])}</code>"
            
        steps.append({
            "line": idx,
            "ram": step_ram,
            "log": step_log,
            "badge": step_badge
        })
        
    return steps

def build_domain_adaptive_visualizer(lesson_title: str, tech_stack: str, viz_spec: Any) -> str:
    """
    Dynamically construct a Section 2.4 Step-by-Step Execution Visualizer component 
    from structured visualizer spec JSON without hardcoding any variables or language idioms.
    If the lesson is conceptual/theory or viz_spec is not applicable, cleanly returns "" (omits Section 2.4).
    """
    if not isinstance(viz_spec, dict) or not viz_spec.get("is_applicable", True):
        return ""
    
    clean_title = lesson_title.split(" - ")[-1] if " - " in lesson_title else lesson_title
    clean_lang = get_clean_language_name(tech_stack)
    
    title = viz_spec.get("title") or "2.4. Mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer)"
    if not title.startswith("2.4"):
        title = f"2.4. {title}"
    explanation = viz_spec.get("explanation") or f"Quan sát tiến trình thực thi từng dòng lệnh và biến đổi trạng thái của dữ liệu trong bộ nhớ cho bài học {clean_title}:"
    
    code_lines = viz_spec.get("code_lines") or []
    variables = viz_spec.get("variables") or []
    raw_steps = viz_spec.get("steps") or []
    
    if not code_lines and not raw_steps:
        return ""
    
    # 1. Build Code Display Lines
    code_lines_html = []
    for idx, line in enumerate(code_lines, 1):
        highlighted = highlight_code_syntax(str(line), clean_lang)
        code_lines_html.append(f"""        <div id="viz-line-{idx}" class="p-1.5 rounded transition-all duration-200 flex items-center justify-between font-mono text-xs whitespace-pre">
          <div class="flex items-center min-w-0">
            <span class="w-6 text-slate-400 text-[10px] select-none text-right mr-3 font-mono shrink-0">{idx}</span>
            <span class="truncate">{highlighted}</span>
          </div>
          <span id="viz-badge-{idx}" class="hidden text-[10px] font-sans px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold border border-amber-300 ml-2 shrink-0 animate-pulse"></span>
        </div>""")
    code_html = "\n".join(code_lines_html)
    
    # 2. Build Memory RAM State Rows
    ram_rows_html = []
    if variables:
        for var in variables:
            if isinstance(var, dict):
                v_name = var.get("name", "var")
                v_label = var.get("label") or f"Biến {v_name}"
                v_slug = re.sub(r'[^a-zA-Z0-9_-]', '-', v_name).lower()
                ram_rows_html.append(f"""        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center">
          <span class="text-slate-600 font-medium">{html.escape(v_label)}:</span>
          <span id="viz-ram-{v_slug}" class="font-bold text-slate-700 px-2.5 py-0.5 rounded bg-white border border-slate-200 min-w-[60px] text-center transition-all duration-300">---</span>
        </div>""")
            elif isinstance(var, str):
                v_slug = re.sub(r'[^a-zA-Z0-9_-]', '-', var).lower()
                ram_rows_html.append(f"""        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center">
          <span class="text-slate-600 font-medium">Biến {html.escape(var)}:</span>
          <span id="viz-ram-{v_slug}" class="font-bold text-slate-700 px-2.5 py-0.5 rounded bg-white border border-slate-200 min-w-[60px] text-center transition-all duration-300">---</span>
        </div>""")
    else:
        ram_rows_html.append(f"""        <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center">
          <span class="text-slate-600 font-medium">Trạng thái luồng:</span>
          <span id="viz-ram-status" class="font-bold text-emerald-600 px-2 py-0.5 rounded bg-white border border-slate-200">Đang hoạt động (Active)</span>
        </div>""")
        
    ram_html = "\n".join(ram_rows_html)
    
    # 3. Build window.vizSteps JSON
    sanitized_steps = []
    if raw_steps and isinstance(raw_steps, list) and len(raw_steps) >= 2:
        for s in raw_steps:
            if isinstance(s, dict):
                raw_ram = s.get("ram") or {}
                clean_ram = {}
                for rk, rv in raw_ram.items():
                    clean_rk = re.sub(r'[^a-zA-Z0-9_-]', '-', str(rk)).lower()
                    clean_ram[clean_rk] = str(rv)
                
                log_val = s.get("log") or f"&gt; Thực thi dòng {s.get('line', 1)}"
                if not log_val.startswith("&gt;") and not log_val.startswith("<div") and not log_val.startswith(">"):
                    log_val = f"&gt; {log_val}"
                if log_val.startswith(">"):
                    log_val = f"&gt;{log_val[1:]}"
                    
                sanitized_steps.append({
                    "line": s.get("line", 1),
                    "ram": clean_ram,
                    "log": log_val,
                    "badge": s.get("badge") or (list(clean_ram.values())[-1] if clean_ram else "")
                })
    else:
        sanitized_steps = generate_fallback_visualizer_steps(code_lines, variables, clean_title)
            
    script_block = f"<script>window.vizSteps = {json.dumps(sanitized_steps, ensure_ascii=False)};</script>" if sanitized_steps else ""
    
    return f"""
<h3 id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc" class="font-montserrat font-bold text-xl text-slate-900 mb-3">{title}</h3>
<p class="text-slate-600 mb-4 leading-relaxed">{explanation}</p>

<div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm my-6 text-slate-800">
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-4">
    <!-- Cột trái: Mã nguồn thực thi -->
    <div class="flex flex-col bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="bg-slate-100/80 px-4 py-2 text-xs font-mono text-slate-700 font-bold border-b border-slate-200 flex items-center justify-between">
        <span>Mã nguồn thực thi ({clean_lang})</span>
        <span id="viz-step-badge" class="px-2 py-0.5 bg-slate-200 text-slate-700 text-[11px] rounded font-sans">Sẵn sàng</span>
      </div>
      <div id="viz-code-display" class="p-3.5 font-mono text-xs text-slate-800 space-y-1.5 overflow-x-auto min-h-[160px]">
{code_html}
      </div>
    </div>

    <!-- Cột phải: Trạng thái bộ nhớ RAM -->
    <div class="flex flex-col bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="bg-slate-100/80 px-4 py-2 text-xs font-mono text-slate-700 font-bold border-b border-slate-200 flex items-center justify-between">
        <span>Trạng thái bộ nhớ (Memory Canvas)</span>
        <span class="px-2 py-0.5 rounded bg-sky-100 text-sky-800 text-[11px] font-bold font-sans">RAM State</span>
      </div>
      <div class="p-4 space-y-3 flex-1 text-xs font-mono">
{ram_html}
      </div>
    </div>
  </div>

  <!-- Nút điều khiển -->
  <div class="flex flex-wrap items-center justify-between gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
    <div class="flex items-center gap-2">
      <button type="button" onclick="runVizStep(-1)" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center gap-1 transition-all">
        <span class="ph-bold ph-caret-left"></span> Bước trước
      </button>
      <button type="button" onclick="runVizStep(1)" class="px-3 py-1.5 rounded-lg bg-rikkei-red text-white font-semibold text-xs flex items-center gap-1 hover:bg-rikkei-darkred transition-all shadow-sm">
        Tiếp theo <span class="ph-bold ph-caret-right"></span>
      </button>
      <button type="button" onclick="runVizStep(-999)" class="px-2.5 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 text-xs transition-all" title="Reset">
        <span class="ph-bold ph-arrow-counter-clockwise"></span> Đặt lại
      </button>
    </div>
    <div class="flex items-center gap-1.5">
      <button type="button" onclick="vizToggleAuto()" id="viz-auto-btn" class="px-3 py-1.5 rounded-lg bg-rikkei-red text-white font-semibold text-xs hover:bg-rikkei-darkred transition-all shadow-sm">Tự động chạy</button>
    </div>
  </div>

  <!-- Terminal log -->
  <div class="mt-3 bg-slate-100 rounded-xl p-3 border border-slate-200 shadow-inner">
    <div class="text-[11px] font-mono text-slate-600 mb-1.5 flex items-center gap-1.5 font-bold">
      <span class="ph-bold ph-terminal text-emerald-800"></span> Nhật ký thực thi từng bước (Console Log):
    </div>
    <div id="viz-terminal-log" class="h-[110px] overflow-y-auto bg-white text-slate-800 font-mono text-xs p-2.5 rounded border border-slate-200 space-y-1">
      <div class="text-slate-400 italic">&gt; Sẵn sàng mô phỏng từng bước cho {clean_title}. Bấm "Tiếp theo" để bắt đầu...</div>
    </div>
  </div>
</div>
{script_block}
"""
