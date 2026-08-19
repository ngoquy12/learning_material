"""
core/renderers/lecture/simulation_builder.py
Interactive Simulation Dashboard Builder and Generic Fallback Generators for Classroom Lectures.
"""

import os
import re
import json
import jinja2
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.llm import call_llm
from core.prompts import render_prompt
from core.renderers.lecture.text_sanitizer import (
    clean_title_string,
    extract_concise_topic_name,
    get_icon_for_topic,
    detect_file_info_for_tech_stack
)
from core.renderers.lecture.knowledge_extractor import (
    derive_unified_session_scenario,
    infer_scope_boundary_rules,
    extract_knowledge_from_lesson_folder
)
from core.renderers.lecture.deck_renderer import LOGO_URL

def clean_and_parse_llm_json(raw_text: str) -> Optional[Dict[str, Any]]:
    """Robust multi-pass JSON extractor for LLM responses."""
    if not raw_text:
        return None
    cleaned = raw_text.strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()

    # Pass 1: Standard json.loads
    try:
        return json.loads(cleaned, strict=False)
    except Exception:
        pass

    # Pass 2: Clean unescaped newlines inside string values
    try:
        sanitized = re.sub(r'[\r\n\t]', ' ', cleaned)
        return json.loads(sanitized, strict=False)
    except Exception:
        pass

    # Pass 3: Regex match outermost JSON object
    try:
        m = re.search(r'(\{[\s\S]*\})', cleaned)
        if m:
            candidate = m.group(1)
            fixed = re.sub(r'[\x00-\x1f]', ' ', candidate)
            return json.loads(fixed, strict=False)
    except Exception:
        pass

    return None

def generate_section_with_llm(
    sec_id: str,
    sec_num: int,
    lesson_title: str,
    tech_stack: str,
    session_title: str,
    unified_scenario: str,
    extracted_knowledge: Dict[str, Any],
    lesson_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Uses LLM to dynamically generate concise 2-hour review lecture content for ANY subject.
    """
    filename, lang = detect_file_info_for_tech_stack(tech_stack, lesson_title)
    bullets_text = "\n".join(f"- {b}" for b in extracted_knowledge.get("bullets", []))
    gotcha_text = extracted_knowledge.get("gotcha_text", "")
    pm_meta = extracted_knowledge.get("pm_meta", {})
    curriculum_details = pm_meta.get("curriculum_details", "")
    scope_rules = infer_scope_boundary_rules(session_title, tech_stack, pm_meta)
    concise_topic_default = extract_concise_topic_name(lesson_title)

    system_prompt = render_prompt("prompts/classroom_lecture_section.j2", {
        "unified_scenario": unified_scenario,
        "scope_rules": scope_rules,
        "tech_stack": tech_stack,
        "concise_topic": concise_topic_default
    })

    user_prompt = f"""Generate lecture section data for:
- Lesson Title: {lesson_title}
- Concise Topic Name: {concise_topic_default}
- Session Title: {session_title}
- Subject / Tech Stack: {tech_stack}
- File to simulate: {filename} ({lang})
- Mandatory Unified Scenario: {unified_scenario}
- Syllabus Sub-topics to Cover: {curriculum_details if curriculum_details else lesson_title}
- Extracted Theory Bullets from Reading:
{bullets_text if bullets_text else 'N/A'}
- Extracted Gotchas:
{gotcha_text if gotcha_text else 'N/A'}"""

    try:
        response_str = call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=True,
            agent_name="classroom_lecture_agent",
            session_id=str(sec_id),
            lesson_id=str(sec_num)
        )

        if not response_str:
            return None

        data = clean_and_parse_llm_json(response_str)
        if not (isinstance(data, dict) and ("concept_bullets" in data or "knowledge_cards" in data)):
            return None

        if "knowledge_cards" in data and isinstance(data["knowledge_cards"], list):
            knowledge_cards = data["knowledge_cards"]
        else:
            c_bullets = data.get("concept_bullets", [])
            c_title = data.get("concept_title", "Khái niệm & Cú pháp Cốt lõi")
            g_points = data.get("gotcha_points", [])
            g_title = data.get("gotcha_title", "Lưu ý & Bẫy lỗi Thường gặp")

            b_items = "".join(f"<li>{b}</li>" for b in c_bullets[:3])
            g_items = "".join(f"<p>{p}</p>" for p in g_points[:2])

            knowledge_cards = [
                {
                    "title": c_title,
                    "icon": "ph-bold ph-lightbulb text-amber-500",
                    "badge": "KHÁI NIỆM & CÚ PHÁP",
                    "badge_style": "bg-amber-50 text-amber-700 border border-amber-200",
                    "border_color": "border-slate-200/80",
                    "content_html": f"""
                    <ul class="space-y-2 list-disc pl-4 text-slate-700">
                      {b_items}
                    </ul>
                    """
                },
                {
                    "title": g_title,
                    "icon": "ph-bold ph-warning-octagon text-rose-600",
                    "badge": "LƯU Ý THỰC HÀNH",
                    "badge_style": "bg-rose-50 text-rose-700 border border-rose-200",
                    "border_color": "border-rose-200 bg-rose-50/40",
                    "title_color": "text-rose-950",
                    "content_html": f"""
                    <div class="space-y-2 text-rose-950 leading-relaxed">
                      {g_items}
                    </div>
                    """
                }
            ]

        raw_demo_title = data.get("demo_title", "")
        if not raw_demo_title or len(raw_demo_title.split()) > 9:
            demo_title = f"Trực quan: {concise_topic_default}"
        else:
            demo_title = raw_demo_title
        code_snippet = data.get("code_snippet", "")
        code_box_html = f"""<pre class="font-mono text-xs leading-relaxed whitespace-pre-wrap"><code id="{sec_id}-code-snippet">{code_snippet}</code></pre>"""

        scenarios = data.get("scenarios", [])
        if not scenarios or not isinstance(scenarios, list):
            scenarios = [
                {
                    "name": "1. Trường hợp Chuẩn (Standard)",
                    "param_values": {},
                    "trace_steps": ["1. Khởi tạo tham số chuẩn", "2. Thực thi biểu thức", "3. Đạt kết quả mong đợi"],
                    "result_value": "Thành công",
                    "status_badge": "Thành công"
                }
            ]

        params = data.get("parameters", [])
        opt_html = []
        for s_idx, sc in enumerate(scenarios):
            s_name = sc.get("name", f"Kịch bản {s_idx + 1}")
            opt_html.append(f'<option value="scen_{s_idx}">{s_name}</option>')

        options_str = "\n".join(opt_html)

        if params and isinstance(params, list) and len(params) > 0:
            col_span_class = f"grid-cols-1 sm:grid-cols-2 lg:grid-cols-{min(len(params), 4)}"
            param_inputs_html = []
            for p in params:
                p_id = p.get("id", "p")
                p_lbl = p.get("label", p_id)
                p_type = p.get("type", "text")
                p_def = p.get("default", "")
                param_inputs_html.append(f"""
              <div class="min-w-0">
                <label class="block text-xs font-semibold text-slate-500 mb-1.5 truncate">{p_lbl}:</label>
                <input type="{p_type}" id="{sec_id}-{p_id}" value="{p_def}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-slate-50/50" oninput="run_{sec_id}_sim()" />
              </div>""")
            
            params_grid_str = "\n".join(param_inputs_html)
            controllers_html = f"""
        <div class="space-y-3.5">
          <div class="min-w-0">
            <label class="block text-xs font-semibold text-slate-500 mb-1.5">Kịch bản Thử nghiệm (Scenario):</label>
            <select id="{sec_id}-scenario" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="on_change_{sec_id}_scenario()">
              {options_str}
            </select>
          </div>
          <div class="grid {col_span_class} gap-3">
            {params_grid_str}
          </div>
        </div>"""
        else:
            default_param = scenarios[0].get("param_value", "")
            controllers_html = f"""
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="min-w-0">
            <label class="block text-xs font-semibold text-slate-500 mb-1.5">Kịch bản Thử nghiệm (Scenario):</label>
            <select id="{sec_id}-scenario" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="run_{sec_id}_sim()">
              {options_str}
            </select>
          </div>
          <div class="min-w-0">
            <label class="block text-xs font-semibold text-slate-500 mb-1.5">Giá trị Tham số (Input Value):</label>
            <input type="text" id="{sec_id}-val" value="{default_param}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-slate-50/50" oninput="run_{sec_id}_sim()" />
          </div>
        </div>"""

        js_scen_map = {}
        for s_idx, sc in enumerate(scenarios):
            pv = sc.get("param_values") if "param_values" in sc else {"val": sc.get("param_value", "")}
            js_scen_map[f"scen_{s_idx}"] = {
                "params": pv,
                "val": sc.get("param_value", ""),
                "trace": "".join(f"<div class='text-slate-400'>> {st}</div>" for st in sc.get("trace_steps", [])),
                "res": sc.get("result_value", "Success"),
                "badge": sc.get("status_badge", "Thành công")
            }

        scen_json_str = json.dumps(js_scen_map, ensure_ascii=False)

        js_code = f"""
  const {sec_id}_scenMap = {scen_json_str};

  function on_change_{sec_id}_scenario() {{
    const scenSelect = document.getElementById("{sec_id}-scenario");
    if (!scenSelect) return;
    const scenData = {sec_id}_scenMap[scenSelect.value] || {sec_id}_scenMap["scen_0"];
    if (scenData && scenData.params) {{
      for (const [k, v] of Object.entries(scenData.params)) {{
        const el = document.getElementById("{sec_id}-" + k);
        if (el) el.value = v;
      }}
    }}
    run_{sec_id}_sim();
  }}

  function run_{sec_id}_sim() {{
    const scenSelect = document.getElementById("{sec_id}-scenario");
    const traceBox = document.getElementById("{sec_id}-trace-box");
    const resVal = document.getElementById("{sec_id}-res-val");
    const resBadge = document.getElementById("{sec_id}-res-badge");

    if (!scenSelect || !traceBox || !resVal || !resBadge) return;

    const currentScen = scenSelect.value;
    const scenData = {sec_id}_scenMap[currentScen] || {sec_id}_scenMap["scen_0"];

    traceBox.innerHTML = scenData.trace;
    resVal.innerText = scenData.res;
    resBadge.innerText = scenData.badge;
    resBadge.className = "font-mono text-xs px-2.5 py-1 " + (currentScen === "scen_2" ? "bg-rose-50 text-rose-700 border border-rose-200" : currentScen === "scen_1" ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-emerald-50 text-emerald-700 border border-emerald-200") + " rounded-full font-semibold";
  }}"""

        first_trace = "".join(f"<div class='text-slate-400'>> {st}</div>" for st in scenarios[0].get("trace_steps", []))

        return {
            "knowledge_cards": knowledge_cards,
            "sim_title": demo_title,
            "snippet_filename": filename,
            "controllers_html": controllers_html,
            "code_box_html": code_box_html,
            "initial_trace_html": first_trace if first_trace else f"<div class='text-slate-400'>> Sẵn sàng thực thi mã nguồn {filename}.</div>",
            "default_res_val": scenarios[0].get("result_value", "Success"),
            "default_res_badge": scenarios[0].get("status_badge", "Thành công"),
            "js_code": js_code,
            "init_call": f"run_{sec_id}_sim();"
        }

    except Exception as e:
        print(f"  [Classroom Lecture Agent] LLM parse error: {e}")

    return None

def build_generic_multi_subject_section(
    sec_id: str,
    sec_num: int,
    lesson_title: str,
    icon: str,
    tech_stack: str,
    session_title: str,
    unified_scenario: str,
    extracted_knowledge: Dict[str, Any],
    lesson_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Universal Generic Multi-Subject Fallback Base (Zero Hardcoding)."""
    filename, lang = detect_file_info_for_tech_stack(tech_stack, lesson_title)
    clean_tech = tech_stack.split(",")[0].strip() if "," in tech_stack else tech_stack
    lt_lower = lesson_title.lower()

    is_arithmetic = any(k in lt_lower for k in ["số học", "arithmetic", "gán gộp", "assignment", "toán tử số"])
    is_comparison = any(k in lt_lower for k in ["so sánh", "comparison", "equal", "strict", "==="])
    is_logic = any(k in lt_lower for k in ["logic", "ngắn mạch", "short-circuit", "boolean", "&&", "||"])

    if is_arithmetic:
        c_bullets = [
            "Toán tử số học (+, -, *, /, %, **) thực hiện các phép toán đại số cơ bản; toán tử gán gộp (+=, -=, *=, /=) giúp cập nhật giá trị biến ngắn gọn.",
            "Toán tử tăng giảm (++ / --): Tiền tố (++x) tăng giá trị trước rồi mới trả về; Hậu tố (x++) trả về giá trị hiện tại rồi mới tăng.",
            "Thứ tự ưu tiên toán tử: Lũy thừa (**) -> Nhân / Chia / Chia lấy dư (*, /, %) -> Cộng / Trừ (+, -). Dùng ngoặc đơn () để điều khiển thứ tự."
        ]
        g_points = [
            "Bẫy ép kiểu chuỗi với '+': Nếu một trong hai toán hạng là chuỗi (String), toán tử '+' sẽ nối chuỗi thay vì cộng số (ví dụ: 10 + '5' = '105').",
            "Sai số số thực (Floating-point): Các phép tính thập phân có thể có sai số nhị phân (ví dụ: 0.1 + 0.2 = 0.30000000000000004)."
        ]
    elif is_comparison:
        c_bullets = [
            "Toán tử === (bằng nghiêm ngặt) và !== (khác nghiêm ngặt) so sánh cả giá trị và kiểu dữ liệu mà KHÔNG ép kiểu ngầm định.",
            "Toán tử so sánh quan hệ (>, <, >=, <=) dùng để kiểm tra thứ tự lớn bé giữa các giá trị số và chuỗi theo bảng mã chuẩn.",
            "Quy chuẩn lập trình ES6+: Luôn sử dụng === và !== thay cho == và != để đảm bảo tính an toàn và minh bạch tuyệt đối của mã nguồn."
        ]
        g_points = [
            "Bẫy ép kiểu ngầm định của '==': Phép so sánh lỏng lẻo có thể gây lỗi logic nguy hiểm (ví dụ: 0 == false là true, '' == 0 là true, null == undefined là true).",
            "Dữ liệu từ biểu mẫu/DOM luôn ở dạng String; so sánh '18' === 18 sẽ luôn trả về false nếu chưa ép kiểu sang Number."
        ]
    elif is_logic:
        c_bullets = [
            "Toán tử logic kết hợp biểu thức: && (AND - cả 2 đúng), || (OR - một trong hai đúng), ! (NOT - đảo ngược giá trị boolean).",
            "Cơ chế Ngắn mạch (Short-circuit): A && B dừng ngay và trả về A nếu A là Falsy; A || B dừng ngay và trả về A nếu A là Truthy.",
            "Danh sách 6 giá trị Falsy trong JavaScript: false, 0, '' (chuỗi rỗng), null, undefined, NaN. Mọi giá trị khác đều là Truthy."
        ]
        g_points = [
            "Toán tử || và && không chỉ trả về true/false mà trả về giá trị thực tế của toán hạng quyết định (ví dụ: '' || 'Khách' trả về 'Khách').",
            "Bẫy Falsy với số 0: Sử dụng || để gán giá trị mặc định có thể ghi đè nhầm số lượng 0 hợp lệ (ví dụ: quantity || 10 sẽ biến 0 thành 10)."
        ]
    else:
        bullets_raw = extracted_knowledge.get("bullets", [])
        c_bullets = bullets_raw[:3] if bullets_raw else [
            f"Nắm vững bản chất cú pháp và nguyên lý thực thi của <code>{lesson_title}</code>.",
            f"Áp dụng chuẩn quy ước đặt tên và cấu trúc mã nguồn theo tiêu chuẩn của <code>{clean_tech}</code>.",
            f"Đảm bảo xử lý đầy đủ các điều kiện biên và kiểm soát luồng dữ liệu an toàn."
        ]
        g_points = [
            extracted_knowledge.get("gotcha_text") or f"Luôn kiểm tra ràng buộc kiểu dữ liệu, các giá trị biên khi triển khai {lesson_title}."
        ]

    knowledge_cards = [
        {
            "title": "Khái niệm & Cú pháp Cốt lõi",
            "icon": "ph-bold ph-lightbulb text-amber-500",
            "badge": "KHÁI NIỆM & CÚ PHÁP",
            "badge_style": "bg-amber-50 text-amber-700 border border-amber-200",
            "border_color": "border-slate-200/80",
            "content_html": f"""
            <ul class="space-y-2 list-disc pl-4 text-slate-700">
              {"".join(f"<li>{b}</li>" for b in c_bullets)}
            </ul>
            """
        },
        {
            "title": "Lưu ý & Bẫy lỗi Thường gặp",
            "icon": "ph-bold ph-warning-octagon text-rose-600",
            "badge": "LƯU Ý THỰC HÀNH",
            "badge_style": "bg-rose-50 text-rose-700 border border-rose-200",
            "border_color": "border-rose-200 bg-rose-50/40",
            "title_color": "text-rose-950",
            "content_html": f"""
            <div class="space-y-2 text-rose-950 leading-relaxed">
              {"".join(f"<p>{p}</p>" for p in g_points)}
            </div>
            """
        }
    ]

    concise_topic = extract_concise_topic_name(lesson_title)
    if is_arithmetic:
        sim_title = "Trực quan: Toán tử Số học & Gán gộp (Giỏ hàng)"
        code_sample = """// --- Bước 1: Tính tiền hàng ban đầu (Số học *, +) ---
let unitPrice = 120000;
let quantity = 2;
let subtotal = unitPrice * quantity; // 120000 * 2 = 240000 VNĐ
let shippingFee = 15000;

// --- Bước 2: Áp dụng giảm giá & Cập nhật gán gộp (-=, ++) ---
subtotal -= 30000;                   // Gán gộp trừ (-= 30k) -> 210000 VNĐ
quantity++;                          // Tăng hậu tố (++) -> Số lượng: 3 món

// --- Bước 3: Đánh giá tổng thanh toán & Quay số trúng thưởng ---
let grandTotal = subtotal + shippingFee; // Tổng: 225000 VNĐ
let orderLuckyParity = 105 % 2;      // Chia lấy dư (%): 1 (Số lẻ - Trúng thưởng)
console.log(`Tổng thanh toán: ${grandTotal} VNĐ | Lượt quay: ${orderLuckyParity}`);"""
        params = [
            {"id": "price", "label": "Đơn giá (VNĐ)", "type": "number", "default": "120000"},
            {"id": "qty", "label": "Số lượng (món)", "type": "number", "default": "2"},
            {"id": "discount", "label": "Mã giảm giá (VNĐ)", "type": "number", "default": "30000"},
            {"id": "shipping", "label": "Phí ship (VNĐ)", "type": "number", "default": "15000"}
        ]
        scenarios = [
            {
                "name": "1. Mua 2 sản phẩm (Chuẩn)",
                "param_values": {"price": "120000", "qty": "2", "discount": "30000", "shipping": "15000"},
                "trace_steps": [
                    "1. Bước 1: Tính tiền hàng ban đầu: 120000 * 2 = 240000 VNĐ",
                    "2. Bước 2: Áp dụng gán gộp giảm giá (-= 30000): 240000 - 30000 = 210000 VNĐ",
                    "3. Bước 3: Cộng phí ship (+ 15000) và tính dư chẵn lẻ (105 % 2 = 1)"
                ],
                "result_value": "225,000 VNĐ",
                "status_badge": "Thành công"
            }
        ]
    elif is_comparison:
        sim_title = "Trực quan: So sánh Nghiêm ngặt (===) & Ép kiểu"
        code_sample = """// --- Bước 1: So sánh nghiêm ngặt mã Voucher (===) ---
const inputVoucher = "FREESHIP";
const isVoucherMatch = (inputVoucher === "FREESHIP");  // true (cùng kiểu String)

// --- Bước 2: Kiểm tra mức đơn hàng tối thiểu (>=) ---
const orderAmount = 250000;
const MIN_REQUIRED = 200000;
const isMinTotalReached = (orderAmount >= MIN_REQUIRED); // true

// --- Bước 3: Phân biệt Bẫy ép kiểu '==' vs '===' an toàn ---
const looseCheck = ("250000" == orderAmount);   // true (Ép kiểu ngầm nguy hiểm)
const strictCheck = ("250000" === orderAmount); // false (Kiểm tra an toàn kiểu dữ liệu)
console.log(`Voucher khớp: ${isVoucherMatch}, Đạt mức tối thiểu: ${isMinTotalReached}`);"""
        params = [
            {"id": "voucher", "label": "Mã Voucher nhập vào", "type": "text", "default": "FREESHIP"},
            {"id": "amount", "label": "Giá trị đơn hàng (VNĐ)", "type": "number", "default": "250000"},
            {"id": "tier", "label": "Hạng thành viên (ID)", "type": "text", "default": "101"}
        ]
        scenarios = [
            {
                "name": "1. Voucher chuẩn & Đủ điều kiện (Chuẩn)",
                "param_values": {"voucher": "FREESHIP", "amount": "250000", "tier": "101"},
                "trace_steps": [
                    "1. Bước 1: So sánh nghiêm ngặt mã voucher: 'FREESHIP' === 'FREESHIP' -> true",
                    "2. Bước 2: So sánh quan hệ giá trị đơn: 250000 >= 200000 -> true",
                    "3. Bước 3: Kết luận: Đủ điều kiện kích hoạt miễn phí vận chuyển"
                ],
                "result_value": "Hợp lệ (Approved)",
                "status_badge": "Thành công"
            }
        ]
    elif is_logic:
        sim_title = "Trực quan: Toán tử Logic & Ngắn mạch (Freeship)"
        code_sample = """// --- Bước 1: Đánh giá điều kiện Freeship (Logic &&, ||) ---
const isVipCustomer = true;
const hasEventCoupon = false;
const orderTotal = 350000;
const isEligibleFreeShip = (isVipCustomer && hasEventCoupon) || (orderTotal >= 300000);

// --- Bước 2: Gán giá trị mặc định an toàn qua Ngắn mạch (||) ---
const inputCustomerName = ""; // Falsy value (chuỗi rỗng)
const displayName = inputCustomerName || "Khách hàng vãng lai"; // Lấy vế sau vì vế 1 là Falsy

// --- Bước 3: Kiểm tra trạng thái đơn hàng bằng toán tử NOT (!) ---
const isOrderInvalid = !isEligibleFreeShip && (orderTotal < 100000);
console.log(`Được Freeship: ${isEligibleFreeShip} | Tên hiển thị: ${displayName}`);"""
        params = [
            {"id": "isvip", "label": "Khách VIP", "type": "select", "options": [("true", "Khách VIP (true)"), ("false", "Khách thường (false)")], "default": "true"},
            {"id": "total", "label": "Giá trị đơn hàng (VNĐ)", "type": "number", "default": "350000"}
        ]
        scenarios = [
            {
                "name": "1. Đơn hàng trên 300k được Freeship (Chuẩn)",
                "param_values": {"isvip": "true", "total": "350000"},
                "trace_steps": [
                    "1. Bước 1: Đánh giá (true && false) -> false, vế 2: 350000 >= 300000 -> true",
                    "2. Bước 2: Biểu thức logic chung: false || true -> true (Được Freeship)",
                    "3. Bước 3: Hoàn tất đánh giá"
                ],
                "result_value": "Freeship: true",
                "status_badge": "Thành công"
            }
        ]
    else:
        sim_title = f"Trực quan: {concise_topic}"
        code_sample = f"""// --- Bước 1: Khởi tạo giá trị cơ sở ---
const targetVal = 100;

// --- Bước 2: Thực thi biểu thức tính toán ---
const processedResult = targetVal * 2;

// --- Bước 3: Xuất kết quả đánh giá ---
console.log(`Kết quả xử lý theo tiêu chuẩn {clean_tech}: ${{processedResult}}`);"""
        params = [
            {"id": "p1", "label": "Tham số 1 (Giá trị cơ sở)", "type": "number", "default": "100"},
            {"id": "p2", "label": "Tham số 2 (Hệ số xử lý)", "type": "number", "default": "2"}
        ]
        scenarios = [
            {
                "name": "1. Trường hợp Chuẩn (Standard)",
                "param_values": {"p1": "100", "p2": "2"},
                "trace_steps": [
                    "1. Bước 1: Nhận giá trị tham số đầu vào: 100",
                    "2. Bước 2: Thực thi xử lý: 100 * 2 = 200",
                    "3. Bước 3: Đạt kết quả mong đợi"
                ],
                "result_value": "Success (200)",
                "status_badge": "Thành công"
            }
        ]

    opt_html = [f'<option value="scen_{s_idx}">{sc["name"]}</option>' for s_idx, sc in enumerate(scenarios)]
    options_str = "\n".join(opt_html)

    param_inputs_html = []
    for p in params:
        p_id = p.get("id", "p")
        p_lbl = p.get("label", p_id)
        p_type = p.get("type", "text")
        p_def = p.get("default", "")
        if p_type == "select":
            opts = p.get("options", [])
            opt_str = "\n".join(f'<option value="{v}" {"selected" if v == p_def else ""}>{lbl}</option>' for v, lbl in opts)
            param_inputs_html.append(f"""
          <div class="min-w-0">
            <label class="block text-xs font-semibold text-slate-500 mb-1.5 truncate">{p_lbl}:</label>
            <select id="{sec_id}-{p_id}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="run_{sec_id}_sim()">
              {opt_str}
            </select>
          </div>""")
        else:
            param_inputs_html.append(f"""
          <div class="min-w-0">
            <label class="block text-xs font-semibold text-slate-500 mb-1.5 truncate">{p_lbl}:</label>
            <input type="{p_type}" id="{sec_id}-{p_id}" value="{p_def}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-slate-50/50" oninput="run_{sec_id}_sim()" />
          </div>""")

    col_span_class = f"grid-cols-1 sm:grid-cols-2 lg:grid-cols-{min(len(params), 4)}"
    controllers_html = f"""
    <div class="space-y-3.5">
      <div class="min-w-0">
        <label class="block text-xs font-semibold text-slate-500 mb-1.5">Kịch bản Thử nghiệm (Scenario):</label>
        <select id="{sec_id}-scenario" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="on_change_{sec_id}_scenario()">
          {options_str}
        </select>
      </div>
      <div class="grid {col_span_class} gap-3">
        {"\n".join(param_inputs_html)}
      </div>
    </div>"""

    js_scen_map = {}
    for s_idx, sc in enumerate(scenarios):
        pv = sc.get("param_values", {})
        js_scen_map[f"scen_{s_idx}"] = {
            "params": pv,
            "trace": "".join(f"<div class='text-slate-400'>> {st}</div>" for st in sc.get("trace_steps", [])),
            "res": sc.get("result_value", "Success"),
            "badge": sc.get("status_badge", "Thành công")
        }

    scen_json_str = json.dumps(js_scen_map, ensure_ascii=False)
    js_code = f"""
  const {sec_id}_scenMap = {scen_json_str};

  function on_change_{sec_id}_scenario() {{
    const scenSelect = document.getElementById("{sec_id}-scenario");
    if (!scenSelect) return;
    const scenData = {sec_id}_scenMap[scenSelect.value] || {sec_id}_scenMap["scen_0"];
    if (scenData && scenData.params) {{
      for (const [k, v] of Object.entries(scenData.params)) {{
        const el = document.getElementById("{sec_id}-" + k);
        if (el) el.value = v;
      }}
    }}
    run_{sec_id}_sim();
  }}

  function run_{sec_id}_sim() {{
    const scenSelect = document.getElementById("{sec_id}-scenario");
    const traceBox = document.getElementById("{sec_id}-trace-box");
    const resVal = document.getElementById("{sec_id}-res-val");
    const resBadge = document.getElementById("{sec_id}-res-badge");

    if (!scenSelect || !traceBox || !resVal || !resBadge) return;

    const currentScen = scenSelect.value;
    const scenData = {sec_id}_scenMap[currentScen] || {sec_id}_scenMap["scen_0"];

    traceBox.innerHTML = scenData.trace;
    resVal.innerText = scenData.res;
    resBadge.innerText = scenData.badge;
    resBadge.className = "font-mono text-xs px-2.5 py-1 " + (currentScen === "scen_2" ? "bg-rose-50 text-rose-700 border border-rose-200" : currentScen === "scen_1" ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-emerald-50 text-emerald-700 border border-emerald-200") + " rounded-full font-semibold";
  }}"""

    first_trace = "".join(f"<div class='text-slate-400'>> {st}</div>" for st in scenarios[0].get("trace_steps", []))

    return {
        "id": sec_id,
        "num": sec_num,
        "title": lesson_title,
        "icon": icon,
        "knowledge_cards": knowledge_cards,
        "sim_title": sim_title,
        "snippet_filename": filename,
        "controllers_html": controllers_html,
        "code_box_html": f"""<pre class="font-mono text-xs leading-relaxed whitespace-pre-wrap"><code id="{sec_id}-code-snippet">{code_sample}</code></pre>""",
        "initial_trace_html": first_trace if first_trace else f"<div class='text-slate-400'>> Sẵn sàng thực thi mã nguồn {filename} ({clean_tech}).</div>",
        "default_res_val": scenarios[0].get("result_value", "Success"),
        "default_res_badge": scenarios[0].get("status_badge", "Thành công"),
        "js_code": js_code,
        "init_call": f"run_{sec_id}_sim();"
    }

def render_interactive_section(
    sec_id: str,
    sec_num: int,
    lesson_title: str,
    icon: str,
    lesson_data: Dict[str, Any],
    tech_stack: str,
    session_title: str = "",
    unified_scenario: str = "",
    session_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Renders structured interactive visualizer data for 1 lesson section across ANY subject."""
    extracted = extract_knowledge_from_lesson_folder(session_dir, session_title, lesson_title)

    llm_data = None
    if os.getenv("SKIP_LIVE_LLM_TESTS") != "1":
        try:
            llm_data = generate_section_with_llm(
                sec_id=sec_id,
                sec_num=sec_num,
                lesson_title=lesson_title,
                tech_stack=tech_stack,
                session_title=session_title,
                unified_scenario=unified_scenario,
                extracted_knowledge=extracted,
                lesson_data=lesson_data
            )
        except Exception as e:
            print(f"  [Classroom Lecture Agent] LLM generation error: {e}, falling back to Generic Base.")
            llm_data = None
            
    if llm_data and isinstance(llm_data, dict) and llm_data.get("knowledge_cards"):
        llm_data["id"] = sec_id
        llm_data["num"] = sec_num
        llm_data["title"] = lesson_title
        llm_data["icon"] = icon
        llm_data["init_call"] = f"run_{sec_id}_sim();"
        return llm_data

    return build_generic_multi_subject_section(
        sec_id=sec_id,
        sec_num=sec_num,
        lesson_title=lesson_title,
        icon=icon,
        tech_stack=tech_stack,
        session_title=session_title,
        unified_scenario=unified_scenario,
        extracted_knowledge=extracted,
        lesson_data=lesson_data
    )

def generate_interactive_visualizer_html(
    session_title: str,
    module_name: str,
    lessons_data: List[Dict[str, Any]],
    core_ssot: Optional[Dict[str, Any]] = None,
    session_dir_path: Optional[str] = None
) -> str:
    """Builds the complete Interactive Visual Classroom Lecture Dashboard HTML."""
    clean_session_title = clean_title_string(session_title)
    clean_module_name = module_name.strip() if module_name else "Khóa học Công nghệ"
    
    session_dir = Path(session_dir_path) if session_dir_path else None
    unified_scenario = derive_unified_session_scenario(clean_session_title, clean_module_name)
    
    nav_items = []
    sections_data = []
    js_functions = []
    init_calls = []
    
    for idx, l_data in enumerate(lessons_data, 1):
        sec_id = f"s{idx}"
        l_title = l_data.get("lesson_title") or f"Bài học {idx}"
        clean_lt = clean_title_string(l_title)
        concise_nav_title = extract_concise_topic_name(clean_lt)
        icon = l_data.get("icon") or get_icon_for_topic(clean_lt, clean_module_name)
        
        nav_items.append({
            "id": sec_id,
            "title": concise_nav_title,
            "icon": icon
        })

        sec_dict = render_interactive_section(
            sec_id=sec_id,
            sec_num=idx,
            lesson_title=clean_lt,
            icon=icon,
            lesson_data=l_data,
            tech_stack=clean_module_name,
            session_title=clean_session_title,
            unified_scenario=unified_scenario,
            session_dir=session_dir
        )
        sections_data.append(sec_dict)
        js_functions.append(sec_dict["js_code"])
        init_calls.append(sec_dict["init_call"])

    template_file = Path("templates/classroom_lecture.html.j2")
    if template_file.exists():
        template_str = template_file.read_text(encoding="utf-8")
        j2_template = jinja2.Template(template_str)
        full_html = j2_template.render(
            session_title=clean_session_title,
            module_name=clean_module_name,
            logo_url=LOGO_URL,
            nav_items=nav_items,
            sections=sections_data,
            client_scripts="\n\n".join(js_functions),
            init_calls="\n        ".join(init_calls),
            current_year=datetime.now().year
        )
        return full_html
    else:
        raise FileNotFoundError("Classroom lecture Jinja2 template not found at templates/classroom_lecture.html.j2")
