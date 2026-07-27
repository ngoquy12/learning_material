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
    
    # Automatic Compiled Session Validation Check
    from core.validators.session_compiler_validator import validate_compiled_session_html
    is_valid, comp_errors = validate_compiled_session_html(output_path)
    if is_valid:
        print(f"  [Session Compiler Validator] PASSED 100% (DOM & JS Isolation Verified)")
    else:
        print(f"  [Session Compiler Validator Warning] {'; '.join(comp_errors)}")

def _build_session_reading_html(session_title: str, html_files: list, is_static: bool = False) -> str:
    """
    Builds a 100% faithful Master Session Reading Hub (reading_all.html)
    using isolated lesson viewports in a clean white light theme with official Rikkei Education logo,
    automatically hides redundant inner lesson headers, and preserves active lesson tab state on auto-reload.
    """
    import json
    import re
    from pathlib import Path

    desktop_nav_buttons = []
    frames = []

    for idx, item in enumerate(html_files, 1):
        try:
            if isinstance(item, dict):
                raw_title = item.get("title") or f"Bài học {idx}"
                rel_path = f"Lesson {idx:02d}/Bài đọc/reading.html"
            else:
                p = Path(item)
                with open(p, "r", encoding="utf-8") as f:
                    file_text = f.read()
                title_match = re.search(r"<title>(.*?)</title>", file_text)
                raw_title = title_match.group(1).replace(" - Trực quan hóa & Tương tác Động", "").strip() if title_match else f"Bài học {idx}"
                rel_path = f"{p.parent.parent.name}/Bài đọc/reading.html"

            m = re.search(r'Lesson\s+(\d+)\s*[:-]\s*(.*)', raw_title, re.IGNORECASE)
            if m:
                full_lesson_name = f'Lesson {m.group(1).zfill(2)} - {m.group(2).strip()}'
                clean_name = m.group(2).strip()
            else:
                full_lesson_name = raw_title
                clean_name = raw_title

            active_btn_cls = "active" if idx == 1 else ""
            active_frame_cls = "active" if idx == 1 else ""

            btn_desktop = f"""
            <button type="button" onclick="switchLesson({idx})" id="sidebar-btn-{idx}" class="sidebar-nav-btn {active_btn_cls} w-full flex items-center gap-3 px-3.5 py-3 rounded-xl text-left text-xs font-semibold border border-transparent transition-all duration-200 cursor-pointer hover:bg-slate-100 hover:text-[#be111c]">
              <span class="flex items-center justify-center w-7 h-7 rounded-lg bg-red-50 text-[#be111c] font-black text-xs shrink-0 border border-red-100 badge-num">
                {idx:02d}
              </span>
              <span class="truncate text-slate-700 font-semibold text-xs leading-snug flex-grow">{full_lesson_name}</span>
            </button>"""
            desktop_nav_buttons.append(btn_desktop)

            frame = f"""
            <iframe id="frame-{idx}" src="{rel_path}" class="lesson-frame {active_frame_cls}" onload="hideIframeHeader(this)" style="width:100%;height:100%;border:none;display:{'block' if idx == 1 else 'none'};"></iframe>"""
            frames.append(frame)
        except Exception as e:
            print(f"  [Session Compiler Warning] Failed to prepare lesson {item}: {e}")

    nav_str = "\n".join(desktop_nav_buttons)
    frames_str = "\n".join(frames)

    session_html = f"""<!doctype html>
<!-- =========================================================================
     CẢNH BÁO: ĐÂY LÀ FILE ĐƯỢC TẠO TỰ ĐỘNG (COMPILED SESSION MASTER HUB).
     VUI LÒNG KHÔNG CHỈNH SỬA TRỰC TIẾP FILE NÀY ĐỂ TRÁNH MẤT DỮ LIỆU.
     ========================================================================= -->
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Tài liệu học tập tổng hợp - {session_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet" />
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{ font-family: 'Inter', sans-serif; background: #f8fafc; color: #0f172a; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }}
      .session-header-bar {{ height: 64px; background: #ffffff; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; flex-shrink: 0; z-index: 20; box-shadow: 0 1px 3px rgba(0,0,0,0.03); }}
      .main-container {{ display: flex; flex: 1; height: calc(100vh - 64px); overflow: hidden; }}
      .sidebar-panel {{ width: 340px; background: #ffffff; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; flex-shrink: 0; }}
      .sidebar-hdr {{ padding: 18px 20px; border-bottom: 1px solid #e2e8f0; font-size: 12px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; display: flex; align-items: center; gap: 8px; }}
      .nav-scroll {{ overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 8px; flex: 1; }}
      .viewport-panel {{ flex: 1; height: 100%; background: #ffffff; position: relative; }}
      .lesson-frame {{ width: 100%; height: 100%; border: none; }}
      .sidebar-nav-btn.active {{ background: rgba(190, 17, 28, 0.08) !important; border-color: rgba(190, 17, 28, 0.25) !important; color: #be111c !important; font-weight: 800 !important; }}
      .sidebar-nav-btn.active .badge-num {{ background: #be111c !important; color: #ffffff !important; border-color: #be111c !important; }}
      .sidebar-nav-btn.active span {{ color: #be111c !important; font-weight: 800 !important; }}
    </style>
  </head>
  <body>
    <div class="session-header-bar">
      <div style="display:flex;align-items:center;gap:16px;">
        <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Rikkei Education" style="height:36px;width:auto;object-fit:contain;" />
        <div style="height:20px;width:1px;background:#e2e8f0;"></div>
        <h1 style="font-family:'Montserrat',sans-serif;font-weight:800;font-size:16px;color:#0f172a;margin:0;">Tài liệu học tập tổng hợp — {session_title}</h1>
      </div>
      <div style="font-size:12px;font-weight:700;color:#64748b;background:#f1f5f9;padding:6px 16px;border-radius:999px;border:1px solid #e2e8f0;">
        {len(html_files)} Bài học hoàn chỉnh
      </div>
    </div>

    <div class="main-container">
      <div class="sidebar-panel">
        <div class="sidebar-hdr">
          <i class="ph-bold ph-list-bullets" style="color:#be111c;font-size:16px;"></i>
          Danh sách Bài học Session
        </div>
        <div class="nav-scroll">
          {nav_str}
        </div>
      </div>

      <div class="viewport-panel">
        {frames_str}
      </div>
    </div>

    <script>
      function hideIframeHeader(iframe) {{
        try {{
          const doc = iframe.contentDocument || iframe.contentWindow.document;
          if (doc && doc.head) {{
            let style = doc.getElementById('hide-inner-header-style');
            if (!style) {{
              style = doc.createElement('style');
              style.id = 'hide-inner-header-style';
              style.textContent = '#sticky-header, header, .sticky-nav {{ display: none !important; }} body {{ padding-top: 0 !important; }}';
              doc.head.appendChild(style);
            }}
          }}
        }} catch(e) {{}}
      }}

      function getInitialLesson() {{
        const hash = window.location.hash;
        if (hash && hash.startsWith('#lesson-')) {{
          const num = parseInt(hash.replace('#lesson-', ''), 10);
          if (num && document.getElementById('frame-' + num)) return num;
        }}
        const saved = localStorage.getItem('active_session_lesson_' + encodeURIComponent(window.location.pathname));
        if (saved) {{
          const num = parseInt(saved, 10);
          if (num && document.getElementById('frame-' + num)) return num;
        }}
        return 1;
      }}

      function switchLesson(idx) {{
        document.querySelectorAll('.sidebar-nav-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.lesson-frame').forEach(frame => {{
          frame.classList.remove('active');
          frame.style.display = 'none';
        }});

        const activeBtn = document.getElementById('sidebar-btn-' + idx);
        const activeFrame = document.getElementById('frame-' + idx);

        if (activeBtn) activeBtn.classList.add('active');
        if (activeFrame) {{
          activeFrame.classList.add('active');
          activeFrame.style.display = 'block';
          hideIframeHeader(activeFrame);
        }}

        try {{
          history.replaceState(null, null, '#lesson-' + idx);
          localStorage.setItem('active_session_lesson_' + encodeURIComponent(window.location.pathname), idx);
        }} catch(e) {{}}
      }}

      document.addEventListener('DOMContentLoaded', () => {{
        const initIdx = getInitialLesson();
        switchLesson(initIdx);
      }});
    </script>
  </body>
</html>"""
    return session_html


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


def compile_session_slides(session_dir: Path, session_title: str):
    """
    Tìm tất cả các file slides.html của từng Lesson trong session_dir,
    tách các slide thành các cảnh (scenes), chèn các slide phân tách Lesson Divider,
    và xuất ra file session_slides.html tổng hợp cho toàn bộ Session.
    """
    slides_files = sorted(
        list(session_dir.glob("*/Bài giảng/slides.html")),
        key=lambda p: int(m.group(1)) if (m := re.search(r'Lesson\s*(\d+)', p.parent.parent.name, re.IGNORECASE)) else 999
    )
    if not slides_files:
        return

    print(f"  [Session Compiler] Merging {len(slides_files)} lesson slide decks into session_slides.html...")
    from agents.slide_generator_agent import slide_generator_agent

    lessons_data = []
    for idx, slide_path in enumerate(slides_files, 1):
        try:
            with open(slide_path, "r", encoding="utf-8") as f:
                content = f.read()

            title_match = re.search(r"<title>(.*?)</title>", content)
            raw_title = title_match.group(1).replace(" — Rikkei Master Slide Presentation", "").strip() if title_match else f"Bài học {idx}"

            m = re.search(r'Lesson\s+(\d+)\s*[:-]\s*(.*)', raw_title, re.IGNORECASE)
            if m:
                full_lesson_name = f'Lesson {m.group(1).zfill(2)} - {m.group(2).strip()}'
            else:
                full_lesson_name = raw_title

            # Parse slide divs from deck-container
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")
            deck = soup.find("div", id="deck-container")
            slide_divs = deck.find_all("div", class_="slide") if deck else []

            scenes = []
            for s_div in slide_divs:
                stype = s_div.get("data-type", "")
                stitle = s_div.get("data-title", "")
                # Skip standalone cover, agenda, and summary slides of individual lessons
                if stype in ["cover", "agenda", "summary"]:
                    continue

                scene_html = "".join([str(c) for c in s_div.children])
                scenes.append({
                    "scene_title": stitle,
                    "short_title": stitle,
                    "action_title": stitle,
                    "html_content": scene_html,
                    "layout_type": "CUSTOM_RAW"
                })

            lessons_data.append({
                "lesson_id": f"Lesson {idx:02d}",
                "lesson_title": full_lesson_name,
                "scenes": scenes
            })
        except Exception as e:
            print(f"  [Warning] Error parsing {slide_path}: {e}")

    if lessons_data:
        master_slide_html = slide_generator_agent.generate_session_deck_html(
            session_title=session_title,
            module_name="RIKKEI ACADEMY",
            lessons_data=lessons_data
        )
        output_path = session_dir / "session_slides.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(master_slide_html)
        print(f"  [Session Compiler] Successfully compiled master session slides: {output_path.name}")


