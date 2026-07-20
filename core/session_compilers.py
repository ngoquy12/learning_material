import os
import re
from pathlib import Path
from core.skills import load_skill_content

def compile_session_html(session_dir: Path, session_title: str):
    """
    Finds all lesson-level HTML readings in session_dir subfolders,
    extracts their body content, wraps them in collapsible accordion cards,
    and writes a unified premium session-level reading_all.html with a sticky left sidebar.
    """
    html_files = sorted(list(session_dir.glob("*/Bài đọc/reading.html")), key=lambda p: int(m.group(1)) if (m := re.search(r'Lesson\s*(\d+)', p.parent.parent.name, re.IGNORECASE)) else 999)
    if not html_files:
        return
        
    print(f"  [Session Compiler] Merging {len(html_files)} lesson HTML readings into reading_all.html...")
    
    interactive_html = _build_session_reading_html(session_title, html_files, is_static=False)
    output_path = session_dir / "reading_all.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(interactive_html)
    print(f"  [Session Compiler] Successfully compiled {output_path.name}")

def _build_session_reading_html(session_title: str, html_files: list, is_static: bool = False) -> str:
    """
    Combines individual lesson HTML fragments into a single session-level reading artifact.
    """
    import json
    import re
    
    mobile_nav_buttons = []
    desktop_nav_buttons = []
    collapse_cards = []
    
    for idx, item in enumerate(html_files, 1):
        try:
            if isinstance(item, dict):
                content = item.get("content") or ""
                raw_title = item.get("title") or f"Bài học {idx}"
            else:
                with open(item, "r", encoding="utf-8") as f:
                    content = f.read()
                # Extract lesson title
                title_match = re.search(r"<title>(.*?)</title>", content)
                raw_title = title_match.group(1).replace(" - Trực quan hóa & Tương tác Động", "").strip() if title_match else f"Bài học {idx}"
            
            m = re.search(r'Lesson\s+(\d+)\s*[:-]\s*(.*)', raw_title, re.IGNORECASE)
            if m:
                full_lesson_name = f'Lesson {m.group(1).zfill(2)} - {m.group(2).strip()}'
                clean_name = m.group(2).strip()
            else:
                full_lesson_name = raw_title
                clean_name = raw_title            
            # Extract body content (inside .layout and including visualizer scripts)
            start_idx = content.find('<div class="layout">')
            if start_idx != -1:
                body_end = content.rfind('</body>')
                if body_end != -1:
                    body_content = content[start_idx:body_end].strip()
                else:
                    body_content = content[start_idx:].strip()
                
                # Use BeautifulSoup to robustly balance and self-repair all HTML tags
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(body_content, "html.parser")
                    body_content = str(soup)
                except Exception as e:
                    print(f"  [Warning] BeautifulSoup repair failed: {e}")
            else:
                body_content = content # Fallback
                
            # Isolate DOM IDs and script functions to prevent collision across lessons
            id_pattern = re.compile(r'id=["\'](.*?)["\']')
            ids = set(id_pattern.findall(body_content))
            
            # Find IDs queried in JS to ensure we rename them even if the HTML element is dynamically missing
            js_id_pattern = re.compile(r"getElementById\(['\"](.*?)['\"]\)")
            js_ids = set(js_id_pattern.findall(body_content))
            
            all_ids = ids.union(js_ids)
            
            for element_id in all_ids:
                if element_id.startswith(f'lesson{idx}-'):
                    continue
                body_content = body_content.replace(f'id="{element_id}"', f'id="lesson{idx}-{element_id}"')
                body_content = body_content.replace(f"id='{element_id}'", f"id='lesson{idx}-{element_id}'")
                body_content = body_content.replace(f"getElementById('{element_id}')", f"getElementById('lesson{idx}-{element_id}')")
                body_content = body_content.replace(f'getElementById("{element_id}")', f'getElementById("lesson{idx}-{element_id}")')
                body_content = body_content.replace(f"('#{element_id}')", f"('#lesson{idx}-{element_id}')")
                body_content = body_content.replace(f'("#{element_id}")', f'("#lesson{idx}-{element_id}")')
                body_content = body_content.replace(f'href="#{element_id}"', f'href="#lesson{idx}-{element_id}"')
                body_content = body_content.replace(f"href='#{element_id}'", f"href='#lesson{idx}-{element_id}'")
                body_content = body_content.replace(f'for="{element_id}"', f'for="lesson{idx}-{element_id}"')
                body_content = body_content.replace(f"for='{element_id}'", f"for='lesson{idx}-{element_id}'")
                
            # Prefix JS template literal IDs used in visualizers
            body_content = body_content.replace('getElementById(`line-${', f'getElementById(`lesson{idx}-line-${{')
            body_content = body_content.replace('id="line-', f'id="lesson{idx}-line-')
            # Prefix global JS variables and classes to prevent redeclaration syntax errors
            body_content = body_content.replace('InteractiveVisualizerEngine', f'InteractiveVisualizerEngine{idx}')
            body_content = body_content.replace('visualizerApp', f'visualizerApp{idx}')
            body_content = body_content.replace('applyTheme', f'applyTheme{idx}')
            body_content = body_content.replace('setThemeMode', f'setThemeMode{idx}')
            body_content = body_content.replace('function copyCode', f'function copyCode{idx}')
            
            # Button Templates
            btn_mobile = f"""
            <button onclick="scrollToAndExpand({idx}); toggleDrawer(false);" id="drawer-btn-{idx}" class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left text-xs font-medium border border-transparent transition-all duration-200 cursor-pointer sidebar-nav-btn">
              <span class="flex items-center justify-center w-6 h-6 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold text-2xs tracking-tight shrink-0 index-badge transition-colors">
                {idx:02d}
              </span>
              <span class="truncate text-slate-700 dark:text-slate-300 font-semibold text-xs leading-snug flex-grow">{full_lesson_name}</span>
            </button>"""
            mobile_nav_buttons.append(btn_mobile)
            
            btn_desktop = f"""
            <button onclick="scrollToAndExpand({idx})" id="sidebar-btn-{idx}" class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left text-xs font-medium border border-transparent transition-all duration-200 cursor-pointer sidebar-nav-btn">
              <span class="flex items-center justify-center w-6 h-6 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold text-2xs tracking-tight shrink-0 index-badge transition-colors">
                {idx:02d}
              </span>
              <span class="truncate text-slate-700 dark:text-slate-300 font-semibold text-xs leading-snug flex-grow">{full_lesson_name}</span>
            </button>"""
            desktop_nav_buttons.append(btn_desktop)
            
            card_content_class = "block border-t border-slate-100 dark:border-[#243049] p-5 md:p-6 bg-white dark:bg-[#151d30]" if is_static else "hidden border-t border-slate-100 dark:border-[#243049] p-5 md:p-6 bg-white dark:bg-[#151d30]"
            
            card = f"""
            <div class="border border-slate-200/80 dark:border-[#243049] rounded-2xl bg-white dark:bg-[#151d30] overflow-hidden shadow-sm transition-all duration-300 hover:shadow-md mb-6" id="lesson-card-{idx}">
              <button class="w-full flex justify-between items-center p-5 bg-slate-50/50 hover:bg-slate-50 dark:bg-slate-800/30 dark:hover:bg-slate-800/60 text-left border-none outline-none cursor-pointer transition-colors duration-200" onclick="toggleLesson({idx})">
                <div class="flex items-center gap-3">
                  <span class="flex items-center justify-center w-8 h-8 rounded-xl bg-red-50 dark:bg-red-950/20 text-[#be111c] dark:text-[#be111c] font-black text-xs border border-red-100 dark:border-red-900/10">
                    {idx:02d}
                  </span>
                  <div>
                    <span class="text-3xs font-bold text-slate-400 dark:text-slate-500 tracking-wider uppercase">Bài học {idx:02d}</span>
                    <h3 class="font-montserrat font-black text-sm md:text-base text-slate-800 dark:text-slate-200 m-0 leading-tight">
                      {clean_name}
                    </h3>
                  </div>
                </div>
                <i class="ph ph-caret-down text-slate-400 dark:text-slate-500 transition-transform duration-300 text-sm" id="chevron-{idx}"></i>
              </button>
              
              <div class="{card_content_class}" id="content-{idx}">
                {body_content}
              </div>
            </div>"""
            collapse_cards.append(card)
        except Exception as e:
            print(f"  [Session Compiler Warning] Failed to parse {item}: {e}")
            
    session_html = f"""<!doctype html>
<!-- =========================================================================
     CẢNH BÁO: ĐÂY LÀ FILE ĐƯỢC TẠO TỰ ĐỘNG (COMPILED).
     VUI LÒNG KHÔNG CHỈNH SỬA TRỰC TIẾP FILE NÀY ĐỂ TRÁNH MẤT DỮ LIỆU.
     
     Để đồng bộ việc chỉnh sửa:
     1. Hãy chỉnh sửa file reading.html tương ứng trong từng thư mục lesson_*/Bài đọc/
     2. Chạy lại session_compilers.py hoặc build_all để render lại file reading_all.html.
     ========================================================================= -->
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>
      Tài liệu học tập tổng hợp - {session_title}
    </title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap"
      rel="stylesheet"
    />

    <!-- Phosphor Icons & Tailwind CSS -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>

    <script>
      tailwind.config = {{
        darkMode: "class",
        theme: {{
          extend: {{
            colors: {{
              rikkei: {{
                red: "#be111c",
                darkred: "#90000a",
                black: "#1a1a1a",
                gray: "#f5f5f5",
                text: "#333333",
              }},
            }},
            fontFamily: {{
              sans: ["Inter", "system-ui", "sans-serif"],
              montserrat: ["Montserrat", "sans-serif"],
              mono: ["JetBrains Mono", "monospace"],
            }},
            fontSize: {{
              "2xs": "0.7rem",
              "3xs": "0.6rem",
            }},
          }},
        }},
      }};
    </script>

    <!-- VS Code (VS 2015) HighlightJS theme for accurate vscode colors -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/vs2015.min.css"
    />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>

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
        --clay: #d97757;
        --clay-light: rgba(217, 119, 87, 0.06);
        --font-sans:
          "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
          Roboto, sans-serif;
        --font-serif: "Montserrat", "Inter", sans-serif;
        --font-mono:
          "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco,
          Consolas, monospace;
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

      .theme-dark {{
        --bg-body: #0b0f19;
        --bg-card: #151d30;
        --bg-hover: #1e293b;
        --text-main: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #1e293b;
        --card-border: #243049;
        --nav-bg: rgba(21, 29, 48, 0.95);
        --box-note-bg: rgba(255, 255, 255, 0.04);
        --box-tip-bg: rgba(56, 161, 105, 0.08);
        --box-warning-bg: rgba(221, 107, 32, 0.08);
        --primary-text: #60a5fa;
        --code-header-bg: #0b0f19;
        --code-body-bg: #05070c;
        --shadow-color: rgba(0, 0, 0, 0.2);
        --clay: #f97316;
        --clay-light: rgba(249, 115, 22, 0.15);
      }}

      /* Premium scrollbar */
      ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
      }}
      ::-webkit-scrollbar-track {{
        background: var(--bg-body);
      }}
      ::-webkit-scrollbar-thumb {{
        background: #be111c;
        border-radius: 4px;
      }}
      ::-webkit-scrollbar-thumb:hover {{
        background: #90000a;
      }}

      body {{
        font-family: var(--font-sans) !important;
        color: var(--text-main);
        background-color: var(--bg-body);
        line-height: 1.7;
        letter-spacing: 0.015em;
        transition:
          background-color 0.3s ease,
          color 0.3s ease;
      }}

      /* Markdown paragraph render - optimized dimensions */
      p {{
        margin-bottom: 12px !important;
        color: var(--text-muted) !important;
        font-size: 1rem !important;
        text-align: justify !important;
        line-height: 1.7 !important;
      }}

      .hero-banner p {{
        color: rgba(255, 255, 255, 0.9) !important;
        text-align: left !important;
      }}

      p strong {{
        color: var(--primary-text) !important;
        font-weight: 700 !important;
      }}

      /* Card styling - compact spacing */
      .section-card {{
        background-color: var(--bg-card) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 1px 3px var(--shadow-color) !important;
        border: 1px solid var(--card-border) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
      }}

      .section-card:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 6px -1px var(--shadow-color) !important;
        border-color: rgba(190, 17, 28, 0.2) !important;
      }}

      .section-header {{
        display: flex !important;
        align-items: center !important;
        margin-bottom: 14px !important;
        border-bottom: 2px solid var(--border-color) !important;
        padding-bottom: 10px !important;
      }}

      .section-icon {{
        font-size: 1.3rem !important;
        margin-right: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 36px !important;
        height: 36px !important;
        background-color: var(--bg-hover) !important;
        color: var(--primary-text) !important;
        border-radius: 50% !important;
      }}

      .section-title {{
        font-family: "Montserrat", sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: var(--primary-text) !important;
        margin: 0 !important;
        letter-spacing: -0.01em !important;
      }}

      /* List formatting for bullet lists and nested points */
      .section-card ul {{
        list-style-type: disc !important;
        margin-left: 20px !important;
        padding-left: 10px !important;
        margin-top: 6px !important;
        margin-bottom: 14px !important;
      }}

      .section-card ul ul {{
        list-style-type: circle !important;
        margin-left: 20px !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
      }}

      .section-card ol {{
        list-style-type: decimal !important;
        margin-left: 20px !important;
        padding-left: 10px !important;
        margin-top: 6px !important;
        margin-bottom: 14px !important;
      }}

      .section-card ol ol {{
        list-style-type: lower-alpha !important;
        margin-left: 20px !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
      }}

      .section-card li {{
        margin-bottom: 6px !important;
        display: list-item !important;
        color: var(--text-muted) !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
        text-align: justify !important;
      }}

      /* Comparison and standard tables */
      .table-wrapper {{
        overflow-x: auto !important;
        width: 100% !important;
        margin: 16px 0 !important;
      }}

      table,
      .comparison-table {{
        width: 100% !important;
        min-width: 750px !important; /* Force table to maintain minimum width for readability */
        border-collapse: collapse !important;
        margin: 0 !important;
        font-size: 0.9rem !important;
        text-align: left !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 3px var(--shadow-color) !important;
        background-color: var(--bg-card) !important;
      }}

      table th,
      .comparison-table th {{
        background-color: #be111c !important;
        color: white !important;
        padding: 12px 16px !important;
        font-weight: 700 !important;
        font-family: "Montserrat", sans-serif !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
      }}

      .theme-dark table th,
      .theme-dark .comparison-table th {{
        background-color: #991b1b !important;
      }}

      table td,
      .comparison-table td {{
        padding: 8px 14px !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-main) !important;
        line-height: 1.6 !important;
      }}

      table tr:nth-child(even),
      .comparison-table tr:nth-child(even) {{
        background-color: var(--bg-body) !important;
      }}

      table tr:hover,
      .comparison-table tr:hover {{
        background-color: var(--bg-hover) !important;
      }}

      /* Warning boxes and notes */
      .box {{
        padding: 16px 20px !important;
        border-radius: 12px !important;
        margin: 16px 0 !important;
        position: relative !important;
        font-size: 0.98rem !important;
        line-height: 1.7 !important;
        background-color: var(--box-note-bg) !important;
        border-left: 5px solid var(--border-color) !important;
      }}

      .tip-box {{
        background-color: var(--box-tip-bg) !important;
        border-left: 5px solid #38a169 !important;
        color: #1b5e20 !important;
      }}
      .theme-dark .tip-box {{
        color: #81c784 !important;
      }}

      .note-box {{
        background-color: var(--box-note-bg) !important;
        border-left: 5px solid #be111c !important;
        color: var(--text-main) !important;
      }}

      .warning-box {{
        background-color: var(--box-warning-bg) !important;
        border-left: 5px solid #dd6b20 !important;
        color: #a04000 !important;
      }}
      .theme-dark .warning-box {{
        color: #ffb74d !important;
      }}

      /* VS Code dark style for code container */
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

      .code-title {{
        font-family: "JetBrains Mono", ui-monospace, monospace !important;
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

      .code-body pre,
      .code-body code {{
        margin: 0 !important;
        padding: 16px 20px !important;
        overflow-x: auto !important;
        background: #1e1e1e !important;
        color: #d4d4d4 !important;
        font-family:
          "JetBrains Mono", "Consolas", "Fira Code", monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.7 !important;
      }}

      .tip-box p,
      .tip-box li,
      .tip-box strong {{
        color: inherit !important;
      }}
      .note-box p,
      .note-box li,
      .note-box strong {{
        color: inherit !important;
      }}
      .warning-box p,
      .warning-box li,
      .warning-box strong {{
        color: inherit !important;
      }}

      /* VSCode code block styling */
      .code-container {{
        background-color: var(--code-body-bg) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        margin: 16px 0 !important;
        box-shadow: 0 4px 6px -1px var(--shadow-color) !important;
        border: 1px solid var(--border-color) !important;
      }}

      .code-header {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        background-color: var(--code-header-bg) !important;
        padding: 10px 16px !important;
        border-bottom: 1px solid var(--border-color) !important;
      }}

      .code-title {{
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-family: "JetBrains Mono", monospace !important;
        font-weight: 500 !important;
      }}

      .copy-btn {{
        background-color: var(--bg-hover) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border-color) !important;
        padding: 4px 10px !important;
        font-size: 0.8rem !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        font-weight: 600 !important;
      }}

      .copy-btn:hover {{
        background-color: #be111c !important;
        color: white !important;
        border-color: #be111c !important;
      }}

      .code-body {{
        padding: 14px !important;
        overflow-x: auto !important;
        background-color: var(--code-body-bg) !important;
      }}

      /* VSCode Dark+ Editor High-Fidelity Styling & Anti-Clipping Fix */
      .code-container {{
        background-color: #1e1e1e !important;
        border-radius: 8px !important;
        border: 1px solid #333333 !important;
        overflow: hidden !important;
        margin: 20px 0 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
      }}
      .code-header {{
        background-color: #252526 !important;
        padding: 10px 16px !important;
        border-bottom: 1px solid #333333 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        color: #cccccc !important;
        font-family: var(--font-sans) !important;
        font-size: 0.85rem !important;
      }}
      .code-body {{
        background-color: #1e1e1e !important;
        padding: 16px 20px !important;
        overflow-x: auto !important;
        overflow-y: visible !important;
      }}
      .code-body pre,
      .code-tracker-panel pre {{
        margin: 0 !important;
        padding: 0 !important;
        background-color: transparent !important;
        border: none !important;
        overflow: visible !important;
      }}
      .code-body code,
      .code-body pre code,
      .code-tracker-panel code,
      .code-tracker-panel pre code {{
        font-family:
          "JetBrains Mono", "Consolas", "Courier New", monospace !important;
        font-size: 14px !important;
        line-height: 1.7 !important;
        color: #d4d4d4 !important;
        background-color: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
        overflow: visible !important;
        white-space: pre !important;
      }}
      /* Exact VSCode Dark+ Syntax Highlight Theme Overrides */
      .hljs {{
        background: #1e1e1e !important;
        color: #d4d4d4 !important;
      }}
      .hljs-comment,
      .hljs-quote {{
        color: #6a9955 !important;
        font-style: italic !important;
      }}
      .hljs-keyword,
      .hljs-selector-tag {{
        color: #569cd6 !important;
        font-weight: normal !important;
      }}
      .hljs-string,
      .hljs-doctag {{
        color: #ce9178 !important;
      }}
      .hljs-number,
      .hljs-literal {{
        color: #b5cea8 !important;
      }}
      .hljs-title,
      .hljs-section,
      .hljs-selector-id,
      .hljs-title.function_ {{
        color: #dcdcaa !important;
      }}
      .hljs-type,
      .hljs-class .hljs-title {{
        color: #4ec9b0 !important;
      }}
      .hljs-built_in,
      .hljs-variable {{
        color: #9cdcfe !important;
      }}
      .hljs-attr,
      .hljs-attribute {{
        color: #9cdcfe !important;
      }}

      /* Layout stability: prevent aside sidebar overlap in accordion cards */
      .layout {{
        display: flex !important;
        flex-direction: column !important;
        gap: 32px !important;
        width: 100% !important;
      }}
      .main-content,
      .panel-box,
      .right-column,
      .visualizer-container,
      .visualizer-grid,
      aside {{
        min-width: 0 !important;
        max-width: 100% !important;
      }}
      aside {{
        position: static !important;
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
        gap: 20px !important;
        width: 100% !important;
      }}

      @media (max-width: 1200px) {{
        .visualizer-grid {{
          grid-template-columns: 1fr !important;
        }}
      }}

      /* Interactive details */
      .interactive-details {{
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        background-color: var(--bg-body) !important;
        margin: 16px 0 !important;
        overflow: hidden !important;
      }}

      .interactive-details .code-container {{
        margin: 14px 8px 16px 8px !important;
      }}

      @media (min-width: 640px) {{
        .interactive-details .code-container {{
          margin: 16px 20px !important;
        }}
      }}

      .interactive-details summary {{
        padding: 12px 16px !important;
        font-weight: 700 !important;
        color: var(--text-main) !important;
        cursor: pointer !important;
        outline: none !important;
        background-color: var(--bg-hover) !important;
        font-family: "Montserrat", sans-serif !important;
        font-size: 0.9rem !important;
      }}

      /* Sidebar Navigation buttons custom */
      .sidebar-nav-btn {{
        border: 1px solid transparent !important;
        color: var(--text-muted) !important;
      }}
      .sidebar-nav-btn:hover {{
        background-color: var(--bg-hover) !important;
        color: #be111c !important;
      }}
      .sidebar-nav-btn.active {{
        background-color: rgba(190, 17, 28, 0.08) !important;
        color: #be111c !important;
        border-color: rgba(190, 17, 28, 0.2) !important;
      }}
      .theme-dark .sidebar-nav-btn.active {{
        background-color: rgba(96, 165, 250, 0.1) !important;
        color: #60a5fa !important;
        border-color: rgba(96, 165, 250, 0.2) !important;
      }}

      /* Self-Test Questions Accordion */
      .selftest-container {{
        margin-top: 16px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
      }}

      .selftest-item {{
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        background-color: var(--bg-card) !important;
        transition: all 0.2s ease !important;
      }}

      .selftest-item:hover {{
        border-color: #be111c !important;
      }}
      .theme-dark .selftest-item:hover {{
        border-color: #60a5fa !important;
      }}

      .selftest-question {{
        padding: 12px 16px !important;
        background-color: var(--bg-hover) !important;
        font-weight: 600 !important;
        color: var(--primary-text) !important;
        cursor: pointer !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        user-select: none !important;
        font-size: 0.95rem !important;
      }}

      .selftest-answer {{
        padding: 16px !important;
        border-top: 1px solid var(--border-color) !important;
        display: none;
        background-color: var(--bg-card) !important;
      }}

      .selftest-answer ul {{
        list-style-type: disc !important;
        margin-left: 24px !important;
        padding-left: 8px !important;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
      }}

      .selftest-answer ol {{
        list-style-type: decimal !important;
        margin-left: 24px !important;
        padding-left: 8px !important;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
      }}

      .selftest-answer li {{
        margin-bottom: 8px !important;
        display: list-item !important;
        color: var(--text-muted) !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
      }}

      .selftest-question::after {{
        content: "▼" !important;
        font-size: 0.75rem !important;
        color: var(--text-muted) !important;
        transition: transform 0.2s !important;
        margin-left: 8px !important;
      }}

      .selftest-item.active .selftest-question::after {{
        transform: rotate(180deg) !important;
      }}

      /* Walkthrough & Effective-HTML Full-Width Layout */
      .layout {{
        display: flex !important;
        flex-direction: column !important;
        gap: 32px !important;
        width: 100% !important;
        margin-top: 24px !important;
      }}

      .layout aside {{
        position: sticky !important;
        top: 100px !important;
        align-self: start !important;
      }}

      .layout .panel {{
        border: 1.5px solid var(--border-color) !important;
        border-radius: 12px !important;
        background-color: var(--bg-card) !important;
        padding: 18px 20px !important;
        margin-bottom: 20px !important;
      }}

      .layout .panel h3 {{
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--text-muted) !important;
        margin-bottom: 12px !important;
        border: none !important;
        padding: 0 !important;
      }}

      .layout .gotchas {{
        border: 1.5px solid var(--clay, #d97757) !important;
        border-radius: 12px !important;
        background-color: var(
          --clay-light,
          rgba(217, 119, 87, 0.06)
        ) !important;
        padding: 18px 20px !important;
      }}

      .layout .gotchas h3 {{
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--clay, #d97757) !important;
        margin-bottom: 10px !important;
        border: none !important;
        padding: 0 !important;
      }}

      .step {{
        display: grid !important;
        grid-template-columns: 44px 1fr !important;
        gap: 18px !important;
        padding: 24px 0 !important;
        border-bottom: 1.5px solid var(--border-color) !important;
      }}

      .step:last-of-type {{
        border-bottom: none !important;
      }}

      .badge {{
        width: 34px !important;
        height: 34px !important;
        border-radius: 50% !important;
        background-color: var(--bg-hover) !important;
        border: 1.5px solid var(--border-color) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-family: var(--font-mono, monospace) !important;
        font-weight: 600 !important;
        color: var(--text-main) !important;
        font-size: 14px !important;
      }}

      .step.hot .badge {{
        background-color: var(
          --clay-light,
          rgba(217, 119, 87, 0.06)
        ) !important;
        border-color: var(--clay, #d97757) !important;
        color: var(--clay, #d97757) !important;
      }}

      .step-loc {{
        font-family: var(--font-sans, "Inter", sans-serif) !important;
        font-size: 1.25rem !important;
        color: var(--text-main) !important;
        margin-bottom: 12px !important;
        font-weight: 700 !important;
      }}

      .step-loc .range {{
        color: var(--text-muted) !important;
        font-weight: 400 !important;
      }}

      /* Interactive Visualizer Playground Container */
      .visualizer-container {{
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        background-color: var(--bg-panel) !important;
        padding: 24px !important;
        margin-bottom: 30px !important;
      }}

      /* Interactive Grid Layout */
      .visualizer-grid {{
        display: grid !important;
        grid-template-columns: 1.5fr 1fr !important;
        gap: 24px !important;
      }}

      @media (max-width: 1024px) {{
        .visualizer-grid {{
          grid-template-columns: 1fr !important;
        }}
      }}

      .panel-box {{
        display: flex !important;
        flex-direction: column !important;
      }}

      /* Panel 1: Visualizer Canvas */
      .canvas-header {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 16px !important;
        flex-wrap: wrap !important;
        gap: 15px !important;
      }}

      .canvas-title {{
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: var(--text-main) !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
      }}

      .legend-box {{
        display: flex !important;
        gap: 12px !important;
        flex-wrap: wrap !important;
        font-size: 0.8rem !important;
        color: var(--text-muted) !important;
      }}

      .legend-item {{
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
      }}

      .legend-color {{
        width: 10px !important;
        height: 10px !important;
        border-radius: 2px !important;
      }}

      .visualizer-canvas {{
        background-color: var(--bg-canvas) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        min-height: 380px !important;
        max-height: 540px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 16px !important;
        padding: 24px 20px !important;
        position: relative !important;
        overflow-y: auto !important;
        overflow-x: auto !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        transition: background-color 0.3s !important;
      }}

      .visualizer-canvas::-webkit-scrollbar {{
        display: none !important;
      }}

      .bar-item {{
        background-color: var(--color-idle) !important;
        width: 48px !important;
        border-radius: 6px 6px 0 0 !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: center !important;
        padding-top: 10px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        color: #ffffff !important;
        transition:
          height 0.3s cubic-bezier(0.4, 0, 0.2, 1),
          background-color 0.2s ease,
          transform 0.3s ease !important;
      }}

      .bar-item.comparing {{
        background-color: var(--color-compare) !important;
        transform: scaleY(1.03) !important;
      }}
      .bar-item.swapping {{
        background-color: var(--color-swap) !important;
        transform: scale(1.05) !important;
      }}
      .bar-item.sorted {{
        background-color: var(--color-done) !important;
      }}

      /* Panel 2 & 4: Controls & Stats */
      .controls-section {{
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
        margin-top: 16px !important;
      }}

      .btn-group {{
        display: flex !important;
        gap: 10px !important;
        flex-wrap: wrap !important;
      }}

      .btn-action {{
        flex: 1 !important;
        min-width: 100px !important;
        padding: 10px 14px !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-sans) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        background: var(--bg-panel) !important;
        color: var(--text-main) !important;
      }}

      .btn-action:hover {{
        background: var(--bg-hover) !important;
        border-color: var(--text-muted) !important;
      }}

      .btn-start {{
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
      }}
      .btn-start:hover {{
        background: var(--primary) !important;
        opacity: 0.9;
      }}
      .btn-reset {{
        background: var(--rust-light, rgba(194, 65, 12, 0.08)) !important;
        color: var(--rust) !important;
        border-color: var(--rust) !important;
      }}
      .btn-reset:hover {{
        background: var(--rust) !important;
        color: white !important;
      }}

      .inputs-row {{
        display: flex !important;
        justify-content: space-between !important;
        gap: 16px !important;
        flex-wrap: wrap !important;
        background: var(--bg-canvas) !important;
        padding: 14px !important;
        border-radius: var(--radius-sm) !important;
        border: 1.5px solid var(--border-color) !important;
      }}

      .input-group {{
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
        flex: 1 !important;
        min-width: 180px !important;
      }}

      .input-label {{
        font-size: 0.8rem !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
      }}

      .custom-input-box {{
        display: flex !important;
        gap: 8px !important;
      }}

      .custom-input {{
        flex: 1 !important;
        background: var(--bg-panel) !important;
        border: 1.5px solid var(--border-color) !important;
        color: var(--text-main) !important;
        padding: 6px 10px !important;
        border-radius: 6px !important;
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
      }}

      .btn-apply {{
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        cursor: pointer !important;
      }}

      /* Panel Right: Code Tracker & Log */
      .right-column {{
        display: flex !important;
        flex-direction: column !important;
        gap: 20px !important;
      }}

      .stats-row {{
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 12px !important;
      }}

      .stat-card {{
        background: var(--bg-canvas) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 8px !important;
        text-align: center !important;
      }}

      .stat-title {{
        font-size: 0.7rem !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 2px !important;
      }}

      .stat-value {{
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: var(--primary) !important;
        font-family: var(--font-mono) !important;
      }}

      .code-tracker-panel {{
        background: #1e1e1e !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
      }}

      .panel-top-bar {{
        background: #252526 !important;
        padding: 10px 14px !important;
        border-bottom: 1.5px solid var(--border-color) !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        font-family: var(--font-mono) !important;
        font-size: 0.8rem !important;
        color: #a5b4fc !important;
      }}

      .code-content pre {{
        margin: 0 !important;
        padding: 14px !important;
        overflow-x: auto !important;
        background-color: #1e1e1e !important;
      }}

      .code-line {{
        display: block !important;
        padding: 2px 6px !important;
        border-left: 3px solid transparent !important;
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
        color: #d4d4d4 !important;
      }}

      .code-line.active-line {{
        background-color: rgba(217, 119, 87, 0.15) !important;
        border-left-color: var(--clay) !important;
        color: #ffffff !important;
      }}

      .console-log-panel {{
        background: #1e1e1e !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 14px !important;
        flex-grow: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        max-height: 200px !important;
      }}

      .log-messages {{
        overflow-y: auto !important;
        flex-grow: 1 !important;
        font-family: var(--font-mono) !important;
        font-size: 0.8rem !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        padding-right: 4px !important;
      }}

      .log-entry {{
        padding: 4px 8px !important;
        border-radius: 4px !important;
        line-height: 1.4 !important;
      }}

      .log-info {{
        background: rgba(30, 41, 59, 0.5) !important;
        color: #94a3b8 !important;
      }}
      .log-success {{
        background: rgba(16, 185, 129, 0.1) !important;
        color: #34d399 !important;
        border-left: 3px solid #10b981 !important;
      }}
      .log-warn {{
        background: rgba(245, 158, 11, 0.1) !important;
        color: #fbbf24 !important;
        border-left: 3px solid #f59e0b !important;
      }}
    </style>
  </head>
  <body
    class="bg-slate-50 text-slate-800 dark:bg-[#0b0f19] dark:text-slate-200 antialiased font-sans transition-colors duration-300"
  >
    <!-- Sticky Nav Header -->
    <div
      id="sticky-header"
      class="sticky top-0 z-30 bg-white/95 dark:bg-[#151d30]/95 backdrop-blur-md border-b border-slate-200 dark:border-[#243049] shadow-sm px-4 md:px-6 py-3 transition-all duration-300"
    >
      <div
        class="max-w-[1600px] w-full mx-auto flex items-center justify-between"
      >
        <div class="flex items-center gap-3">
          <!-- Drawer Toggle Button for mobile -->
          <button
            class="lg:hidden flex items-center justify-center p-2 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-slate-800 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-[#be111c] cursor-pointer"
            onclick="toggleDrawer(true)"
          >
            <i class="ph ph-list text-xl"></i>
          </button>
          <!-- Rikkei Logo -->
          <img
            src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"
            alt="Rikkei Education Logo"
            class="h-9 w-auto object-contain"
          />
        </div>

        <div class="flex items-center gap-3">
          <!-- Theme Switcher Segmented Control -->
          <div
            class="flex items-center gap-1 border border-slate-200 dark:border-slate-700 rounded-lg p-0.5 bg-slate-50 dark:bg-slate-800"
          >
            <button
              id="theme-btn-light"
              onclick="setTheme('light')"
              class="p-1.5 rounded-md text-xs border transition-all cursor-pointer flex items-center justify-center"
              title="Chế độ sáng"
            >
              <i class="ph ph-sun-dim text-base"></i>
            </button>
            <button
              id="theme-btn-dark"
              onclick="setTheme('dark')"
              class="p-1.5 rounded-md text-xs border transition-all cursor-pointer flex items-center justify-center"
              title="Chế độ tối"
            >
              <i class="ph ph-moon text-base"></i>
            </button>
            <button
              id="theme-btn-system"
              onclick="setTheme('system')"
              class="p-1.5 rounded-md text-xs border transition-all cursor-pointer flex items-center justify-center"
              title="Chế độ hệ thống"
            >
              <i class="ph ph-desktop text-base"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Hero Banner -->
    <div
      class="hero-banner relative bg-gradient-to-r from-[#90000a] via-[#be111c] to-[#e2231a] text-white px-6 py-10 md:py-12 shadow-lg overflow-hidden border-b-4 border-[#be111c]"
    >
      <div
        class="absolute -right-16 -top-16 w-64 h-64 bg-white/5 rounded-full blur-2xl pointer-events-none"
      ></div>
      <div
        class="absolute -left-16 -bottom-16 w-64 h-64 bg-black/10 rounded-full blur-2xl pointer-events-none"
      ></div>

      <div class="max-w-[1600px] w-full mx-auto relative z-10">
        <span
          class="badge-banner inline-block px-3 py-0.5 bg-white text-[#be111c] rounded-full text-xs font-bold uppercase tracking-wider mb-3 border border-white/10"
          >Tài liệu học tập tổng hợp</span
        >
        <h2
          class="font-montserrat font-black text-2xl md:text-4xl tracking-tight uppercase leading-tight mb-2"
        >
          {session_title}
        </h2>
        <p
          class="max-w-2xl font-light text-xs md:text-sm border-l-2 border-white/30 pl-4" style="color: rgba(255, 255, 255, 0.9);"
        >
          Hệ thống giáo trình lý thuyết và thực hành phân rã chi tiết từng bài
          học trực thuộc dưới dạng thẻ mở rộng tương tác.
        </p>
      </div>
    </div>

    <!-- Mobile Drawer Backdrop -->
    <div
      id="drawer-backdrop"
      class="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm hidden transition-all duration-300"
      onclick="toggleDrawer(false)"
    ></div>

        <!-- Mobile Drawer Panel -->
    <div
      id="drawer-panel"
      class="fixed inset-y-0 left-0 w-72 z-50 bg-white dark:bg-[#151d30] border-r border-slate-200 dark:border-[#243049] shadow-2xl p-5 transform -translate-x-full transition-transform duration-300 ease-out flex flex-col"
    >
      <div class="flex items-center justify-between mb-5">
        <div class="flex items-center gap-2">
          <i class="ph ph-list-numbers text-lg text-[#be111c]"></i>
          <span
            class="font-montserrat font-bold text-sm tracking-wide text-slate-800 dark:text-slate-200"
            >DANH SÁCH BÀI HỌC</span
          >
        </div>
        <button class="p-1 rounded-md text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" onclick="toggleDrawer(false)">
          <i class="ph ph-x text-lg"></i>
        </button>
      </div>
      <div class="space-y-1 overflow-y-auto pb-6">
        {"".join(mobile_nav_buttons)}
      </div>
    </div>
<!-- Main Grid Layout -->
    <div class="max-w-[1600px] w-full mx-auto px-4 md:px-6 py-6 md:py-8">
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Left Column (Desktop Sidebar Menu) -->
        <div class="w-full lg:w-72 shrink-0 hidden lg:block">
          <div
            class="lg:sticky lg:top-24 bg-white dark:bg-[#151d30] border border-slate-200 dark:border-[#243049] rounded-xl p-4 shadow-sm transition-all duration-300"
          >
            <h3
              class="font-montserrat font-bold text-xs tracking-wider text-[#be111c] dark:text-blue-400 uppercase mb-3 flex items-center gap-2"
            >
              <i class="ph ph-list-numbers text-sm"></i> Danh sách bài học
            </h3>
            <div class="space-y-1">
              
        {"".join(desktop_nav_buttons)}

            </div>
          </div>
        </div>

        <!-- Right Column (Accordions Main Content) -->
        <div id="main-content" class="flex-grow min-w-0 space-y-6">
          {"".join(collapse_cards)}
        </div>
      </div>
    </div>
<script>
      // Theme Switcher Logic
      function setTheme(mode) {{
        localStorage.setItem("theme", mode);
        document.documentElement.classList.remove("theme-light", "theme-dark");

        let activeTheme = mode;
        if (mode === "system") {{
          const isDark = window.matchMedia(
            "(prefers-color-scheme: dark)",
          ).matches;
          activeTheme = isDark ? "dark" : "light";
        }}

        if (activeTheme === "dark") {{
          document.documentElement.classList.add("theme-dark");
          document.documentElement.classList.add("dark"); // for tailwind dark classes if any
        }} else {{
          document.documentElement.classList.add("theme-light");
          document.documentElement.classList.remove("dark");
        }}

        updateThemeSelectorUI(mode);
      }}

      function updateThemeSelectorUI(mode) {{
        const btnLight = document.getElementById("theme-btn-light");
        const btnDark = document.getElementById("theme-btn-dark");
        const btnSystem = document.getElementById("theme-btn-system");

        if (!btnLight || !btnDark || !btnSystem) return;

        [btnLight, btnDark, btnSystem].forEach((btn) => {{
          btn.classList.remove(
            "bg-red-50",
            "text-[#be111c]",
            "border-red-200",
            "bg-slate-700",
            "text-white",
            "border-slate-600",
            "dark:bg-slate-900",
          );
          btn.classList.add(
            "bg-transparent",
            "text-slate-500",
            "border-transparent",
            "dark:text-slate-400",
          );
        }});

        const activeBtn =
          mode === "light" ? btnLight : mode === "dark" ? btnDark : btnSystem;
        const isThemeDark =
          document.documentElement.classList.contains("theme-dark");

        if (isThemeDark) {{
          activeBtn.classList.remove(
            "bg-transparent",
            "text-slate-500",
            "border-transparent",
            "dark:text-slate-400",
          );
          activeBtn.classList.add(
            "bg-slate-700",
            "text-white",
            "border-slate-600",
          );
        }} else {{
          activeBtn.classList.remove(
            "bg-transparent",
            "text-slate-500",
            "border-transparent",
          );
          activeBtn.classList.add(
            "bg-red-50",
            "text-[#be111c]",
            "border-red-200",
          );
        }}
      }}

      // Initial theme set
      const savedTheme = localStorage.getItem("theme") || "system";
      setTheme(savedTheme);

      // Listen to system preference changes
      window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", (e) => {{
          if (localStorage.getItem("theme") === "system") {{
            setTheme("system");
          }}
        }});

      // Drawer Toggle Functions
      function toggleDrawer(open) {{
        const panel = document.getElementById("drawer-panel");
        const backdrop = document.getElementById("drawer-backdrop");
        if (!panel || !backdrop) return;

        if (open) {{
          panel.classList.remove("-translate-x-full");
          backdrop.classList.remove("hidden");
        }} else {{
          panel.classList.add("-translate-x-full");
          backdrop.classList.add("hidden");
        }}
      }}

      function getSessionStorageKey() {{
        return "session_expanded_" + encodeURIComponent(document.title);
      }}

      function saveLessonState(idx, isExpanded) {{
        try {{
          const key = getSessionStorageKey();
          let state = JSON.parse(localStorage.getItem(key) || "{{}}");
          state[idx] = isExpanded;
          localStorage.setItem(key, JSON.stringify(state));
        }} catch(e) {{
          console.error("Failed to save lesson state to localStorage", e);
        }}
      }}

      function loadLessonStates() {{
        try {{
          const key = getSessionStorageKey();
          return JSON.parse(localStorage.getItem(key) || "{{}}");
        }} catch(e) {{
          return "{{}}";
        }}
      }}

      document.addEventListener("DOMContentLoaded", (event) => {{
        document.querySelectorAll("pre code").forEach((el) => {{
          hljs.highlightElement(el);
        }});

        // Load saved states
        const savedStates = loadLessonStates();
        const cards = document.querySelectorAll('[id^="lesson-card-"]');
        let hasSavedState = Object.keys(savedStates).length > 0;

        if (hasSavedState) {{
          cards.forEach((card) => {{
            const idx = card.id.replace("lesson-card-", "");
            const isExpanded = savedStates[idx];
            if (isExpanded) {{
              expandLesson(parseInt(idx));
            }} else {{
              collapseLesson(parseInt(idx));
            }}
          }});
        }} else {{
          // Auto-toggle first lesson if no saved state exists
          expandLesson(1);
        }}

        // Restore scroll position
        try {{
          const scrollKey = "session_scroll_" + encodeURIComponent(document.title);
          const savedScroll = localStorage.getItem(scrollKey);
          if (savedScroll) {{
            setTimeout(() => {{
              window.scrollTo(0, parseInt(savedScroll));
            }}, 150);
          }}
        }} catch(e) {{}}

        // Save scroll position on scroll (throttled)
        let scrollTimeout;
        window.addEventListener("scroll", () => {{
          clearTimeout(scrollTimeout);
          scrollTimeout = setTimeout(() => {{
            try {{
              const scrollKey = "session_scroll_" + encodeURIComponent(document.title);
              localStorage.setItem(scrollKey, window.scrollY);
            }} catch(e) {{}}
          }}, 100);
        }});
      }});

      function toggleLesson(idx) {{
        const content = document.getElementById(`content-${{idx}}`);
        const chevron = document.getElementById(`chevron-${{idx}}`);
        const card = document.getElementById(`lesson-card-${{idx}}`);

        if (!content || !chevron || !card) return;

        const isHidden = content.classList.contains("hidden");

        if (isHidden) {{
          content.classList.remove("hidden");
          chevron.style.transform = "rotate(180deg)";
          card.classList.add(
            "border-[#be111c]",
            "dark:border-[#60a5fa]",
            "ring-1",
            "ring-[#be111c]/20",
            "dark:ring-[#60a5fa]/20",
          );
          saveLessonState(idx, true);
        }} else {{
          content.classList.add("hidden");
          chevron.style.transform = "rotate(0deg)";
          card.classList.remove(
            "border-[#be111c]",
            "dark:border-[#60a5fa]",
            "ring-1",
            "ring-[#be111c]/20",
            "dark:ring-[#60a5fa]/20",
          );
          saveLessonState(idx, false);
        }}
      }}

      function expandLesson(idx) {{
        const content = document.getElementById(`content-${{idx}}`);
        const chevron = document.getElementById(`chevron-${{idx}}`);
        const card = document.getElementById(`lesson-card-${{idx}}`);

        if (!content || !chevron || !card) return;

        if (content.classList.contains("hidden")) {{
          content.classList.remove("hidden");
          chevron.style.transform = "rotate(180deg)";
          card.classList.add(
            "border-[#be111c]",
            "dark:border-[#60a5fa]",
            "ring-1",
            "ring-[#be111c]/20",
            "dark:ring-[#60a5fa]/20",
          );
          saveLessonState(idx, true);
        }}
      }}

      function collapseLesson(idx) {{
        const content = document.getElementById(`content-${{idx}}`);
        const chevron = document.getElementById(`chevron-${{idx}}`);
        const card = document.getElementById(`lesson-card-${{idx}}`);

        if (!content || !chevron || !card) return;

        if (!content.classList.contains("hidden")) {{
          content.classList.add("hidden");
          chevron.style.transform = "rotate(0deg)";
          card.classList.remove(
            "border-[#be111c]",
            "dark:border-[#60a5fa]",
            "ring-1",
            "ring-[#be111c]/20",
            "dark:ring-[#60a5fa]/20",
          );
          saveLessonState(idx, false);
        }}
      }}

      function scrollToAndExpand(idx) {{
        expandLesson(idx);

        const card = document.getElementById(`lesson-card-${{idx}}`);
        if (!card) return;

        const offset = 90; // sticky header height
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = card.getBoundingClientRect().top;
        const elementPosition = elementRect - bodyRect;
        const offsetPosition = elementPosition - offset;

        window.scrollTo({{
          top: offsetPosition,
          behavior: "smooth",
        }});

        highlightActiveSidebarLink(idx);
      }}

      // Active navigation state highlight based on viewport scroll position
      window.addEventListener("scroll", () => {{
        const cards = document.querySelectorAll('[id^="lesson-card-"]');
        let currentActiveId = 1;

        cards.forEach((card) => {{
          const rect = card.getBoundingClientRect();
          if (rect.top <= 120) {{
            const idx = card.id.replace("lesson-card-", "");
            currentActiveId = parseInt(idx);
          }}
        }});

        highlightActiveSidebarLink(currentActiveId);
      }});

      function highlightActiveSidebarLink(idx) {{
        const btns = document.querySelectorAll(".sidebar-nav-btn");
        btns.forEach((btn) => {{
          btn.classList.remove(
            "bg-red-50",
            "dark:bg-blue-950/20",
            "text-[#be111c]",
            "dark:text-[#60a5fa]",
            "border-red-200",
            "dark:border-blue-900/30",
            "active",
          );
          const badge = btn.querySelector(".index-badge");
          if (badge) {{
            badge.classList.remove(
              "bg-red-100",
              "dark:bg-blue-950/40",
              "text-[#be111c]",
              "dark:text-[#60a5fa]",
            );
            badge.classList.add(
              "bg-slate-100",
              "dark:bg-slate-800",
              "text-slate-500",
              "dark:text-slate-400",
            );
          }}
        }});

        // Update sidebar desktop
        const sidebarBtn = document.getElementById("sidebar-btn-" + idx);
        if (sidebarBtn) {{
          sidebarBtn.classList.add(
            "bg-red-50",
            "dark:bg-blue-950/20",
            "text-[#be111c]",
            "dark:text-[#60a5fa]",
            "border-red-200",
            "dark:border-blue-900/30",
            "active",
          );
          const badge = sidebarBtn.querySelector(".index-badge");
          if (badge) {{
            badge.classList.remove(
              "bg-slate-100",
              "dark:bg-slate-800",
              "text-slate-500",
              "dark:text-slate-400",
            );
            badge.classList.add(
              "bg-red-100",
              "dark:bg-blue-950/40",
              "text-[#be111c]",
              "dark:text-[#60a5fa]",
            );
          }}
        }}

        // Update drawer mobile
        const drawerBtn = document.getElementById("drawer-btn-" + idx);
        if (drawerBtn) {{
          drawerBtn.classList.add(
            "bg-red-50",
            "dark:bg-blue-950/20",
            "text-[#be111c]",
            "dark:text-[#60a5fa]",
            "border-red-200",
            "dark:border-blue-900/30",
            "active",
          );
          const badge = drawerBtn.querySelector(".index-badge");
          if (badge) {{
            badge.classList.remove(
              "bg-slate-100",
              "dark:bg-slate-800",
              "text-slate-500",
              "dark:text-slate-400",
            );
            badge.classList.add(
              "bg-red-100",
              "dark:bg-blue-950/40",
              "text-[#be111c]",
              "dark:text-[#60a5fa]",
            );
          }}
        }}
      }}

      function copyCode(btn, elementId) {{
        const codeEl = document.getElementById(elementId);
        if (!codeEl) return;
        const text = codeEl.innerText;
        navigator.clipboard
          .writeText(text)
          .then(() => {{
            const originalText = btn.innerText;
            btn.innerText = "Đã chép!";
            btn.style.backgroundColor = "#be111c";
            btn.style.color = "white";
            setTimeout(() => {{
              btn.innerText = originalText;
              btn.style.backgroundColor = "";
              btn.style.color = "";
            }}, 2000);
          }})
          .catch((err) => {{
            console.error("Lỗi khi sao chép: ", err);
          }});
      }}

      // Toggle self-test questions
      document.addEventListener("click", function (e) {{
        const question = e.target.closest(".selftest-question");
        if (!question) return;

        const item = question.parentElement;
        const answer = item.querySelector(".selftest-answer");
        if (!answer) return;

        const isActive = item.classList.contains("active");
        if (isActive) {{
          item.classList.remove("active");
          answer.style.display = "none";
        }} else {{
          item.classList.add("active");
          answer.style.display = "block";
        }}
      }});
    </script>
  </body>
</html>
   

    """
    return session_html

def compile_session_mindmap(session_dir: Path, session_title: str):
    """
    Finds all lesson-level mindmap.md files in session_dir subfolders,
    and merges them into a single session-level mindmap_all.md file.
    """
    import re
    import mistune
    
    mindmap_files = sorted(list(session_dir.glob("*/Mindmap/mindmap.md")), key=lambda p: int(m.group(1)) if (m := re.search(r'Lesson\s*(\d+)', p.parent.parent.name, re.IGNORECASE)) else 999)
    if not mindmap_files:
        return
        
    print(f"  [Session Compiler] Merging {len(mindmap_files)} lesson mindmaps into mindmap_all.md...")
    
    mindmap_data = []
    for idx, path in enumerate(mindmap_files, 1):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            mindmap_data.append({
                "content": content,
                "title": None
            })
        except Exception as e:
            print(f"  [Session Compiler Warning] Failed to read mindmap {path}: {e}")
            
    if not mindmap_data:
        return
        
    compiled_markdown = compile_session_mindmap_markdown(session_title, mindmap_data)
    
    output_path = session_dir / "mindmap_all.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(compiled_markdown)
    print(f"  [Session Compiler] Successfully compiled {output_path.name}")

def render_inline(node):
    ntype = node.get('type')
    if ntype == 'text':
        return node.get('raw', '')
    elif ntype == 'strong':
        return f"**{render_inline_list(node.get('children', []))}**"
    elif ntype == 'emphasis':
        return f"*{render_inline_list(node.get('children', []))}*"
    elif ntype == 'codespan':
        return f"`{node.get('raw', '')}`"
    elif ntype == 'link':
        url = node.get('attrs', {}).get('url', '')
        return f"[{render_inline_list(node.get('children', []))}]({url})"
    elif ntype == 'image':
        url = node.get('attrs', {}).get('url', '')
        alt = node.get('attrs', {}).get('alt', '') or render_inline_list(node.get('children', []))
        return f"![{alt}]({url})"
    elif ntype == 'softbreak':
        return "\n"
    elif ntype == 'linebreak':
        return "  \n"
    elif ntype == 'inline_html':
        return node.get('raw', '')
    else:
        if 'children' in node:
            return render_inline_list(node['children'])
        return node.get('raw', '')

def render_inline_list(nodes):
    return "".join(render_inline(n) for n in nodes)

def render_block(node, level_shift=0):
    ntype = node.get('type')
    if ntype == 'heading':
        level = node.get('attrs', {}).get('level', 1) + level_shift
        title = render_inline_list(node.get('children', []))
        return f"{'#' * level} {title}"
    elif ntype == 'paragraph':
        return render_inline_list(node.get('children', []))
    elif ntype == 'block_text':
        return render_inline_list(node.get('children', []))
    elif ntype == 'block_code':
        info = node.get('attrs', {}).get('info', '')
        raw_code = node.get('raw', '')
        return f"```{info}\n{raw_code}```"
    elif ntype == 'list':
        ordered = node.get('attrs', {}).get('ordered', False)
        bullet = node.get('bullet', '-')
        lines = []
        for idx, item in enumerate(node.get('children', []), 1):
            item_text = render_block(item, level_shift)
            indented_item_text = "\n".join(
                ("  " + l if i > 0 else l)
                for i, l in enumerate(item_text.splitlines())
            )
            prefix = f"{idx}. " if ordered else f"{bullet} "
            lines.append(f"{prefix}{indented_item_text}")
        return "\n".join(lines)
    elif ntype == 'list_item':
        children = node.get('children', [])
        has_sublist = any(c.get('type') == 'list' for c in children)
        join_str = "\n" if has_sublist else "\n\n"
        return render_block_list(children, level_shift, join_str)
    elif ntype == 'thematic_break':
        return "---"
    elif ntype == 'block_quote':
        quote_text = render_block_list(node.get('children', []), level_shift)
        return "\n".join(f"> {l}" for l in quote_text.splitlines())
    elif ntype == 'blank_line':
        return ""
    else:
        if 'children' in node:
            return render_block_list(node['children'], level_shift)
        return node.get('raw', '')

def render_block_list(nodes, level_shift=0, join_str="\n\n"):
    parts = []
    for node in nodes:
        rendered = render_block(node, level_shift)
        if rendered is not None:
            parts.append(rendered)
    return join_str.join(parts)

def strip_yaml_frontmatter(content: str) -> str:
    content = re.sub(r'^\s*---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    return content.strip()

def clean_markmap_content(content: str) -> str:
    content = content.strip()
    if not content.startswith("```"):
        return content

    lines = content.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines.pop(0)

    while lines and lines[-1].strip() == "":
        lines.pop()

    while lines:
        last_line = lines[-1].strip()
        if last_line == "```":
            num_open = 0
            num_close = 0
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("```"):
                    if len(stripped) > 3 and stripped[3].isalnum():
                        num_open += 1
                    elif stripped == "```":
                        num_close += 1
            if num_close > num_open:
                lines.pop()
                while lines and lines[-1].strip() == "":
                    lines.pop()
            else:
                break
        else:
            break

    return "\n".join(lines).strip()

def extract_and_remove_objectives(nodes):
    objectives = []
    nodes_to_remove = []
    for i, node in enumerate(nodes):
        if node.get('type') == 'heading':
            title = render_inline_list(node.get('children', [])).strip().lower()
            if title == 'mục tiêu bài học':
                nodes_to_remove.append(node)
                if i + 1 < len(nodes) and nodes[i+1].get('type') == 'list':
                    list_node = nodes[i+1]
                    nodes_to_remove.append(list_node)
                    for item in list_node.get('children', []):
                        item_text = render_block(item).strip()
                        if item_text:
                            item_text_clean = re.sub(r'^[-*\d\.\s]+', '', item_text).strip()
                            objectives.append(item_text_clean)
                break
    cleaned_nodes = [n for n in nodes if n not in nodes_to_remove]
    return cleaned_nodes, objectives

def process_lesson_nodes(nodes, lesson_title_fallback):
    cleaned_nodes = []
    replaced_first_header = False
    
    for node in nodes:
        if node.get('type') == 'heading':
            level = node.get('attrs', {}).get('level', 1)
            if level == 1 and not replaced_first_header:
                title = render_inline_list(node.get('children', []))
                title_to_use = lesson_title_fallback or title
                
                if ":" in title_to_use:
                    parts = title_to_use.split(":", 1)
                    first_part_lower = parts[0].strip().lower()
                    if "session" in first_part_lower or "lesson" in first_part_lower:
                        title_to_use = parts[1].strip()
                        
                cleaned_title = re.sub(
                    r'^(?:Lesson\s*\d+|\d+)\s*(?:[:\-\.]\s*)?', 
                    '', 
                    title_to_use, 
                    flags=re.IGNORECASE
                ).strip()
                
                cleaned_nodes.append({
                    'type': 'heading',
                    'attrs': {'level': 2},
                    'children': [{'type': 'text', 'raw': cleaned_title}]
                })
                replaced_first_header = True
            else:
                new_level = level + 1
                cleaned_nodes.append({
                    'type': 'heading',
                    'attrs': {'level': new_level},
                    'children': node.get('children', [])
                })
        else:
            cleaned_nodes.append(node)
            
    return cleaned_nodes

def compile_session_mindmap_markdown(session_title: str, mindmap_data: list) -> str:
    """
    Combines individual lesson mindmap Markdown content into a single session-level mindmap.
    """
    import re
    import mistune
    
    session_objectives = []
    lesson_contents = []
    
    parser = mistune.create_markdown(renderer='ast')

    for idx, item in enumerate(mindmap_data, 1):
        try:
            content = item.get("content", "")
            if not content:
                continue
            
            content = clean_markmap_content(content)
            content = strip_yaml_frontmatter(content)
            
            ast_nodes = parser(content)
            cleaned_nodes, objs = extract_and_remove_objectives(ast_nodes)
            session_objectives.extend(objs)
            
            lesson_title_fallback = item.get("title") or f"Lesson {idx}"
            processed_nodes = process_lesson_nodes(cleaned_nodes, lesson_title_fallback)
            
            lesson_markdown = render_block_list(processed_nodes)
            lesson_contents.append(lesson_markdown)
        except Exception as e:
            print(f"  [Session Compiler Warning] Failed to parse mindmap data for lesson {idx}: {e}")

    merged_lines = [
        "---",
        "markmap:",
        "  colorFreezeLevel: 3",
        "---",
        f"# {session_title}",
        ""
    ]

    if session_objectives:
        merged_lines.append("## Mục tiêu bài học")
        seen = set()
        deduped_objectives = []
        for obj in session_objectives:
            if obj not in seen:
                seen.add(obj)
                deduped_objectives.append(obj)
        for obj in deduped_objectives:
            merged_lines.append(f"- {obj}")
        merged_lines.append("")

    for l_content in lesson_contents:
        if l_content:
            merged_lines.append(l_content)
            merged_lines.append("")

    final_content = "\n".join(merged_lines).strip()
    return f"```markmap\n{final_content}\n```"

