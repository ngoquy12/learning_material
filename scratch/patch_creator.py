# patch_creator.py
import os

file_path = r"d:\Rikkei Education\Elearning_Agent\Learning-Material\agents\creator_agents.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = '    html_template = f"""<!DOCTYPE html>'
end_marker = '</html>"""'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("Error: start_marker not found!")
    exit(1)

# Find the first end_marker after start_idx
end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("Error: end_marker not found!")
    exit(1)

end_idx += len(end_marker)

new_template_code = """    html_template = f\"\"\"<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} - Trực quan hóa & Tương tác Động</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/dracula.min.css">
    <style>
        :root {{
            --bg-body: #FAF9F5;
            --bg-panel: #ffffff;
            --bg-card: #ffffff;
            --bg-canvas: #F0EEE6;
            --primary: #4A8EB3;
            --primary-glow: rgba(74, 142, 179, 0.15);
            --accent: #D97757;
            --accent-glow: rgba(217, 119, 87, 0.15);
            --text-main: #141413;
            --text-muted: #87867F;
            --border-color: #D1CFC5;
            --bg-hover: #F0EEE6;
            
            --clay: #D97757;
            --clay-light: rgba(217, 119, 87, 0.06);
            --olive: #788C5D;
            --olive-light: rgba(120, 140, 93, 0.12);
            --rust: #B04A3F;
            --rust-light: rgba(176, 74, 63, 0.1);
            --gold: #E8B83D;
            --blue: #4A8EB3;
            --blue-light: rgba(74, 142, 179, 0.15);

            --color-idle: var(--blue);
            --color-compare: var(--gold);
            --color-swap: var(--clay);
            --color-done: var(--olive);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;

            --font-serif: ui-serif, Georgia, "Times New Roman", serif;
            --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            --font-mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
        }}

        .theme-dark, html.dark, :root.dark {{
            --bg-body: #0b0f19;
            --bg-panel: #151d30;
            --bg-card: #1e293b;
            --bg-canvas: #0b0f19;
            --primary: #60a5fa;
            --primary-glow: rgba(96, 165, 250, 0.15);
            --accent: #f97316;
            --accent-glow: rgba(249, 115, 22, 0.15);
            --text-main: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: #1e293b;
            --bg-hover: #1e293b;
            
            --clay: #f97316;
            --clay-light: rgba(249, 115, 22, 0.15);
            --olive: #10b981;
            --olive-light: rgba(16, 185, 129, 0.15);
            --rust: #ef4444;
            --rust-light: rgba(239, 68, 68, 0.15);
            --gold: #f59e0b;
            --blue: #3b82f6;
            --blue-light: rgba(59, 130, 246, 0.15);
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
            padding: 30px 20px;
            transition: background-color 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
        }}

        /* Header Styling */
        header {{
            background: var(--bg-panel);
            border: 1.5px solid var(--border-color);
            padding: 30px 40px;
            border-radius: var(--radius-lg);
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            position: relative;
        }}

        .header-info h1 {{
            font-family: var(--font-serif);
            font-size: 2.2rem;
            font-weight: 500;
            color: var(--text-main);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .badge-session {{
            background-color: var(--primary);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}

        .header-tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .pill-tag {{
            background: var(--bg-hover);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        /* Effective HTML 2-Column Grid Layout */
        .layout {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) 280px;
            gap: 32px;
            align-items: start;
        }}

        @media (max-width: 960px) {{
            .layout {{
                grid-template-columns: 1fr;
            }}
        }}

        .main-content {{
            display: flex;
            flex-direction: column;
        }}

        /* Sticky Sidebar Column */
        aside {{
            position: sticky;
            top: 24px;
            align-self: start;
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
            grid-template-columns: 1.5fr 1fr;
            gap: 24px;
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
            height: 360px;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 16px;
            padding: 30px 20px 20px;
            position: relative;
            overflow: hidden;
            transition: background-color 0.3s;
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
            font-family: var(--font-mono);
            font-size: 13px;
            color: var(--text-main);
            margin-bottom: 6px;
            font-weight: 600;
        }}

        .step-loc .range {{
            color: var(--text-muted);
            font-weight: 400;
        }}

        .step-body {{
            font-size: 0.95rem;
            color: var(--text-main);
        }}

        /* Code syntax container */
        .code-container {{
            border: 1.5px solid var(--border-color);
            border-radius: var(--radius-md);
            overflow: hidden;
            margin: 16px 0;
        }}

        .code-header {{
            background: var(--bg-hover);
            border-bottom: 1px solid var(--border-color);
            padding: 10px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .copy-btn {{
            background: rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .copy-btn:hover {{
            background: rgba(0, 0, 0, 0.1);
        }}

        .code-body pre {{
            margin: 0;
            padding: 16px;
            overflow-x: auto;
            background: #1e1e1e;
        }}

        /* Note, Tip & Warning Boxes */
        .box {{
            padding: 18px 22px;
            border-radius: var(--radius-sm);
            margin: 20px 0;
            border-left: 4px solid;
            font-size: 0.95rem;
        }}

        .tip-box {{ background: var(--olive-light); border-color: var(--olive); color: var(--text-main); }}
        .note-box {{ background: var(--blue-light); border-color: var(--blue); color: var(--text-main); }}
        .warning-box {{ background: var(--clay-light); border-color: var(--clay); color: var(--text-main); }}

        .selftest-item {{
            background: var(--bg-panel);
            border: 1.5px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 12px;
            padding: 16px;
        }}
        .selftest-question {{ font-weight: 600; color: var(--primary); cursor: pointer; }}
        .selftest-answer {{ margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-color); display: none; color: var(--text-main); }}
        .selftest-item.active .selftest-answer {{ display: block; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Top Header Navigation -->
        <header>
            <div class="header-info">
                <span class="badge-session">{session_id}</span>
                <h1>{lesson_title}</h1>
                <p style="color: var(--text-muted); font-size: 1rem; margin-top: 4px;">Phòng thí nghiệm Trực quan hóa & Thao tác Động ngay trên trình duyệt</p>
            </div>
            <div class="header-tags">
                <span class="pill-tag">✨ Thực Tiễn</span>
                <span class="pill-tag">🚀 Sáng Tạo</span>
                <span class="pill-tag">💡 Tự Tin</span>
                <span class="pill-tag">🤝 Hợp Tác</span>
            </div>
        </header>

        <!-- Main Layout grid matching effective-html structure -->
        <div class="layout">
            
            <div class="main-content">
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
                </div>

                <!-- Walkthrough Step-by-Step Sections -->
                <div class="walkthrough-section">
                    <h2 style="font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; margin: 30px 0 20px; border-bottom: 2px solid var(--border-color); padding-bottom: 8px;">
                        Cơ chế hoạt động & Phân tích chi tiết (Step-by-step Walkthrough)
                    </h2>

                    <!-- Step 1: Problem Breakdown -->
                    <div class="step">
                        <div class="badge">1</div>
                        <div class="step-body">
                            <div class="step-loc">Đặt vấn đề & Thách thức thực tế <span class="range">· Problem Breakdown</span></div>
                            {problem_html}
                        </div>
                    </div>

                    <!-- Step 2: Deep Dive Internals -->
                    <div class="step">
                        <div class="badge">2</div>
                        <div class="step-body">
                            <div class="step-loc">Phân tích Bản chất & Cơ chế vận hành nội bộ <span class="range">· Deep Dive Internals</span></div>
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
                            <div class="step-loc">Giới thiệu Giải pháp & Kiến trúc Triển khai <span class="range">· Solution & Architecture</span></div>
                            {solution_html}
                            <div class="box tip-box">
                                <strong>Giải pháp tối ưu:</strong> Sử dụng trực quan hóa giúp nhanh chóng định vị điểm nghẽn và cải thiện tốc độ phản hồi đáng kể.
                            </div>
                        </div>
                    </div>

                    <!-- Step 4: Production Code Walkthrough -->
                    <div class="step">
                        <div class="badge">4</div>
                        <div class="step-body">
                            <div class="step-loc">Mã nguồn chuẩn hóa & Phân tích thực thi <span class="range">· Implementation & Execution</span></div>
                            {code_block_html}
                            <div style="margin-top: 16px;">
                                {resolve_html}
                            </div>
                        </div>
                    </div>

                    <!-- Step 5: Self-Test Checklist -->
                    <div class="step">
                        <div class="badge">5</div>
                        <div class="step-body">
                            <div class="step-loc">Bộ câu hỏi Khảo thí tự học & Đánh giá năng lực <span class="range">· Self-Test Checklist</span></div>
                            <p style="margin-bottom: 12px; font-size: 0.9rem;">Học viên nhấp chuột vào từng câu hỏi bên dưới để đối chiếu gợi ý tự học và rèn luyện:</p>
                            <div class="selftest-container">
                                {self_test_html}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sticky Right Sidebar Panel for specs & gotchas -->
            <aside>
                <div class="panel">
                    <h3>Khái niệm Cốt lõi</h3>
                    <ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 12px;">
                        <li>
                            <strong style="font-size: 0.85rem; display: block; color: var(--text-main);">{lesson_title}</strong>
                            <span style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-top: 2px;">
                                Tài liệu hướng dẫn chuyên sâu bám sát lộ trình đào tạo thực tế.
                            </span>
                        </li>
                        <li>
                            <strong style="font-size: 0.85rem; display: block; color: var(--text-main);">Công nghệ trọng tâm</strong>
                            <span style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-top: 2px; font-family: var(--font-mono);">
                                {tech_stack.upper()}
                            </span>
                        </li>
                    </ul>
                </div>

                <div class="gotchas">
                    <h3>Cạm bẫy & Sai lầm (Gotchas)</h3>
                    <div style="font-size: 0.8rem; color: var(--text-main); line-height: 1.5;">
                        {summary_html}
                    </div>
                </div>
            </aside>
            
        </div>
    </div>

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
    </script>
</body>
</html>\"\"\""""

content_before = content[:start_idx]
content_after = content[end_idx:]

patched_content = content_before + new_template_code + content_after

with open(file_path, "w", encoding="utf-8") as f:
    f.write(patched_content)

print("Patch successfully applied programmatically!")
