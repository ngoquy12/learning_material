import json
from typing import Dict, Any
from core.schemas.llm_schemas import VisualizerPayloadSchema

def get_topic_fallback_visualizer_engine(lesson_title: str, tech_stack: str, raw_code: str) -> Dict[str, Any]:
    """
    Tự động chọn 1 trong 3 Template Engine phỏng đoán trực quan động theo đúng chủ đề bài học
    khi LLM không sinh JS Engine hoặc khi ứng dụng chạy offline:
    1. SQL_EXECUTER_TEMPLATE (Database, SQL, Postgres, MySQL, Table, Index, Query)
    2. ALGORITHM_ARRAY_TEMPLATE (Thuật toán, Mảng, Vòng lặp, Chuỗi, Python Core)
    3. WEB_FLOW_LIFECYCLE_TEMPLATE (Web Backend/Frontend, API, FastAPI, Express, Spring Boot)
    """
    combined = f"{lesson_title.lower()} {tech_stack.lower()}"

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
    if not raw_code or not raw_code.strip():
        return {}

    try:
        from core.llm import call_llm

        system_prompt = f"""You are a Lead Web Visualizer & Interactive State Machine Engine Architect at Rikkei Education.
Your sole task is to analyze example source code for technology '{tech_stack}' and generate a step-by-step interactive JavaScript State Machine Engine.

MANDATORY ENGINE DIRECTIVES:
1. Ensure the JavaScript code declares a complete `class InteractiveVisualizerEngine`.
2. Implement methods: init(), start(), pause(), step(), reset(), setSpeed(val), applyCustomData(), render(), log(msg).
3. In method render(), implement smooth DOM visual updates reflecting code step-by-step execution.
"""

        user_prompt = f"""Generate Visualizer Engine JavaScript code for lesson:
Session: {session_id}
Lesson: {lesson_id} — {lesson_title}
Sample Code Snippet:
```
{raw_code[:1000]}
```

Return ONLY a raw JSON Object matching schema:
{{
    "canvas_title": "Visualizer Title in Accented Vietnamese...",
    "legend_html": "HTML displaying color status legend",
    "stats_html": "HTML displaying metric counter cards",
    "code_tracker_html": "HTML code lines block where EACH LINE is wrapped in <div class='code-line' id='line-0'>...</div>",
    "input_label": "Test input box label",
    "input_default": "Default test value",
    "engine_js": "Executable JavaScript source code containing FULL state machine logic of class InteractiveVisualizerEngine"
}}

Return ONLY raw JSON. Do not wrap in markdown code blocks.
"""

        response = call_llm(
            system_prompt, user_prompt,
            json_mode=True,
            agent_name="Visualizer_Generator_Agent",
            response_schema=VisualizerPayloadSchema
        )

        if response:
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            res = json.loads(cleaned)
            if isinstance(res, dict) and res.get("engine_js") and "class InteractiveVisualizerEngine" in res["engine_js"]:
                engine_js = res["engine_js"]
                engine_js = engine_js.replace("canvas-area", "visualizer-canvas")
                engine_js = engine_js.replace("custom-input-data", "custom-data-input")
                res["engine_js"] = engine_js

                safe_title = str(lesson_title).encode('ascii', 'replace').decode('ascii')
                print(f"  [OK] [Visualizer_Generator_Agent] Generated & synchronized custom JS Visualizer Engine for {safe_title}")
                return res

    except Exception as e:
        safe_err = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"  [WARNING] [Visualizer_Generator_Agent Warning] Dedicated visualizer LLM call failed: {safe_err}")

    safe_title = str(lesson_title).encode('ascii', 'replace').decode('ascii')
    print(f"  [INFO] [Visualizer Engine] Using Topic-based Dynamic Fallback Template for '{safe_title}' ({tech_stack})")
    return get_topic_fallback_visualizer_engine(lesson_title, tech_stack, raw_code)
