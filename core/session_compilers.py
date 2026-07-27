
def _clean_slide_raw(raw_text: str) -> str:
    if not raw_text:
        return ""
    raw_text = re.sub(r'<style[^>]*>.*?</style>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    raw_text = re.sub(r'<script[^>]*>.*?</script>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    raw_text = re.sub(r'<!DOCTYPE[^>]*>', '', raw_text, flags=re.IGNORECASE)
    raw_text = re.sub(r'</?(html|head|body|meta|title|link)[^>]*>', '', raw_text, flags=re.IGNORECASE)
    return raw_text.strip()

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
    using isolated lesson viewports in a clean white light theme with official Rikkei Education logo.
    Uses opacity/z-index instead of display:none to guarantee 100% flawless Mermaid diagram layout rendering on all tabs.
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
            <iframe id="frame-{idx}" src="{rel_path}" class="lesson-frame {active_frame_cls}"></iframe>"""
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
      .lesson-frame {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; opacity: 0; pointer-events: none; z-index: 1; transition: opacity 0.15s ease-in-out; }}
      .lesson-frame.active {{ opacity: 1; pointer-events: auto; z-index: 10; }}
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
          if (doc && doc.head && !doc.getElementById('hide-inner-hdr')) {{
            const style = doc.createElement('style');
            style.id = 'hide-inner-hdr';
            style.textContent = '#sticky-header, header, .sticky-nav {{ display: none !important; }} body {{ padding-top: 0 !important; }}';
            doc.head.appendChild(style);
          }}
        }} catch(e) {{}}
      }}

      function switchLesson(idx) {{
        const btns = document.querySelectorAll('.sidebar-nav-btn');
        const frames = document.querySelectorAll('.lesson-frame');
        
        btns.forEach((btn, i) => {{
          if (i + 1 === idx) {{
            btn.classList.add('active');
          }} else {{
            btn.classList.remove('active');
          }}
        }});

        frames.forEach((frame, i) => {{
          if (i + 1 === idx) {{
            frame.classList.add('active');
            hideIframeHeader(frame);
            try {{
              if (frame.contentWindow && frame.contentWindow.mermaid && typeof frame.contentWindow.mermaid.run === 'function') {{
                frame.contentWindow.mermaid.run();
              }}
            }} catch(e) {{}}
          }} else {{
            frame.classList.remove('active');
          }}
        }});
      }}
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
    Tìm tất cả các file slides.html hoặc slides.md của từng Lesson trong session_dir,
    tách các slide thành các cảnh (scenes) và xuất ra file session_slides.html tổng hợp.
    Khử hoàn toàn các thẻ HTML lồng <!DOCTYPE html>, <head>, <style> gây trắng màn hình.
    """
    lesson_dirs = sorted(
        [d for d in session_dir.iterdir() if d.is_dir() and (d / "Bài giảng").exists()],
        key=lambda p: int(m.group(1)) if (m := re.search(r'Lesson\s*(\d+)', p.name, re.IGNORECASE)) else 999
    )
    if not lesson_dirs:
        return

    print(f"  [Session Compiler] Merging {len(lesson_dirs)} lesson slide decks into session_slides.html...")
    from agents.slide_generator_agent import slide_generator_agent

    lessons_data = []
    for idx, l_dir in enumerate(lesson_dirs, 1):
        slide_html_p = l_dir / "Bài giảng" / "slides.html"
        slide_md_p = l_dir / "Bài giảng" / "slides.md"
        
        file_to_read = slide_html_p if slide_html_p.exists() else (slide_md_p if slide_md_p.exists() else None)
        if not file_to_read:
            continue

        m_name = re.search(r'Lesson\s+(\d+)\s*[:-]\s*(.*)', l_dir.name, re.IGNORECASE)
        if m_name:
            full_lesson_name = f'Lesson {m_name.group(1).zfill(2)} - {m_name.group(2).strip()}'
        else:
            full_lesson_name = l_dir.name

        scenes = []
        try:
            file_text = file_to_read.read_text(encoding="utf-8")
            if "<!DOCTYPE" in file_text or "<html" in file_text or 'class="slide"' in file_text or 'id="deck-container"' in file_text:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(file_text, "html.parser")
                deck = soup.find("div", id="deck-container")
                slide_divs = deck.find_all("div", class_="slide") if deck else soup.find_all("div", class_="slide")

                for s_div in slide_divs:
                    stype = s_div.get("data-type", "")
                    stitle = s_div.get("data-title", "")
                    if stype in ["cover", "agenda", "summary"]:
                        continue
                    
                    # Clean duplicate header & badge elements from inner slide HTML
                    for el in s_div.find_all(class_=["content-header-title", "content-top-accent-bar", "top-right-logo", "corner-page-badge", "footer-copyright"]):
                        el.decompose()
                    
                    inner_html = "".join([str(c) for c in s_div.children]).strip()
                    # Strip emojis
                    inner_html = re.sub(r'[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF]', '', inner_html)
                    
                    # Clean any lingering <!DOCTYPE or <html> or <head> or <style> tags inside inner_html
                    inner_html = re.sub(r'<!DOCTYPE[^>]*>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'<html[^>]*>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'</html>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'<head[^>]*>.*?</head>', '', inner_html, flags=re.DOTALL | re.IGNORECASE)
                    inner_html = re.sub(r'<style[^>]*>.*?</style>', '', inner_html, flags=re.DOTALL | re.IGNORECASE)
                    inner_html = re.sub(r'<body[^>]*>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'</body>', '', inner_html, flags=re.IGNORECASE)

                    clean_stitle = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', stitle).strip()
                    if not clean_stitle or clean_stitle.startswith("<!DOCTYPE") or clean_stitle.startswith("<html"):
                        clean_stitle = f"Chủ đề trọng tâm {len(scenes) + 1}"

                    scenes.append({
                        "scene_title": clean_stitle,
                        "short_title": clean_stitle,
                        "action_title": clean_stitle,
                        "html_content": inner_html,
                        "layout_type": "CUSTOM_RAW"
                    })
            else:
                # Parse pure markdown slide deck
                blocks = file_text.split('---')
                for b_idx, block in enumerate(blocks, 1):
                    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
                    if not lines:
                        continue
                    stitle = lines[0].lstrip("#").strip()
                    if any(k in stitle.lower() for k in ["mục lục", "tổng quan", "trang bìa", "slide tổng hợp"]):
                        continue
                    scenes.append({
                        "scene_title": stitle,
                        "short_title": stitle,
                        "action_title": stitle,
                        "html_content": f"<div style='padding:20px;'><h3 style='font-size:20px;font-weight:700;color:#0f172a;'>{stitle}</h3><div style='margin-top:12px;font-size:15px;color:#334155;'>{'<br>'.join(lines[1:])}</div></div>",
                        "layout_type": "CUSTOM_RAW"
                    })
        except Exception as e:
            print(f"  [Warning] Error parsing {file_to_read}: {e}")

        lessons_data.append({
            "lesson_id": f"Lesson {idx:02d}",
            "lesson_title": full_lesson_name,
            "scenes": scenes
        })

    if lessons_data:
        master_slide_html = slide_generator_agent.generate_session_deck_html(
            session_title=session_title,
            module_name="Lập trình Python",
            lessons_data=lessons_data
        )
        output_path = session_dir / "session_slides.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(master_slide_html)
        print(f"  [Session Compiler] Successfully compiled master session slides: {output_path.name}")


def _build_session_reading_html(session_title: str, html_files: list, is_static: bool = False) -> str:
    """
    Builds a 100% faithful Master Session Reading Hub (reading_all.html)
    using isolated lesson viewports in a clean white light theme with official Rikkei Education logo.
    Uses opacity/z-index instead of display:none to guarantee 100% flawless Mermaid diagram layout rendering on all tabs.
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
            <iframe id="frame-{idx}" src="{rel_path}" class="lesson-frame {active_frame_cls}"></iframe>"""
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
      .lesson-frame {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; opacity: 0; pointer-events: none; z-index: 1; transition: opacity 0.15s ease-in-out; }}
      .lesson-frame.active {{ opacity: 1; pointer-events: auto; z-index: 10; }}
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
          if (doc && doc.head && !doc.getElementById('hide-inner-hdr')) {{
            const style = doc.createElement('style');
            style.id = 'hide-inner-hdr';
            style.textContent = '#sticky-header, header, .sticky-nav {{ display: none !important; }} body {{ padding-top: 0 !important; }}';
            doc.head.appendChild(style);
          }}
        }} catch(e) {{}}
      }}

      function switchLesson(idx) {{
        const btns = document.querySelectorAll('.sidebar-nav-btn');
        const frames = document.querySelectorAll('.lesson-frame');
        
        btns.forEach((btn, i) => {{
          if (i + 1 === idx) {{
            btn.classList.add('active');
          }} else {{
            btn.classList.remove('active');
          }}
        }});

        frames.forEach((frame, i) => {{
          if (i + 1 === idx) {{
            frame.classList.add('active');
            hideIframeHeader(frame);
            try {{
              if (frame.contentWindow && frame.contentWindow.mermaid && typeof frame.contentWindow.mermaid.run === 'function') {{
                frame.contentWindow.mermaid.run();
              }}
            }} catch(e) {{}}
          }} else {{
            frame.classList.remove('active');
          }}
        }});
      }}
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
    Tìm tất cả các file slides.html hoặc slides.md của từng Lesson trong session_dir,
    tách các slide thành các cảnh (scenes) và xuất ra file session_slides.html tổng hợp.
    Khử hoàn toàn các thẻ HTML lồng <!DOCTYPE html>, <head>, <style> gây trắng màn hình.
    """
    lesson_dirs = sorted(
        [d for d in session_dir.iterdir() if d.is_dir() and (d / "Bài giảng").exists()],
        key=lambda p: int(m.group(1)) if (m := re.search(r'Lesson\s*(\d+)', p.name, re.IGNORECASE)) else 999
    )
    if not lesson_dirs:
        return

    print(f"  [Session Compiler] Merging {len(lesson_dirs)} lesson slide decks into session_slides.html...")
    from agents.slide_generator_agent import slide_generator_agent

    lessons_data = []
    for idx, l_dir in enumerate(lesson_dirs, 1):
        slide_html_p = l_dir / "Bài giảng" / "slides.html"
        slide_md_p = l_dir / "Bài giảng" / "slides.md"
        
        file_to_read = slide_html_p if slide_html_p.exists() else (slide_md_p if slide_md_p.exists() else None)
        if not file_to_read:
            continue

        m_name = re.search(r'Lesson\s+(\d+)\s*[:-]\s*(.*)', l_dir.name, re.IGNORECASE)
        if m_name:
            full_lesson_name = f'Lesson {m_name.group(1).zfill(2)} - {m_name.group(2).strip()}'
        else:
            full_lesson_name = l_dir.name

        scenes = []
        try:
            file_text = file_to_read.read_text(encoding="utf-8")
            if "<!DOCTYPE" in file_text or "<html" in file_text or 'class="slide"' in file_text or 'id="deck-container"' in file_text:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(file_text, "html.parser")
                deck = soup.find("div", id="deck-container")
                slide_divs = deck.find_all("div", class_="slide") if deck else soup.find_all("div", class_="slide")

                for s_div in slide_divs:
                    stype = s_div.get("data-type", "")
                    stitle = s_div.get("data-title", "")
                    if stype in ["cover", "agenda", "summary"]:
                        continue
                    
                    # Clean duplicate header & badge elements from inner slide HTML
                    for el in s_div.find_all(class_=["content-header-title", "content-top-accent-bar", "top-right-logo", "corner-page-badge", "footer-copyright"]):
                        el.decompose()
                    
                    inner_html = "".join([str(c) for c in s_div.children]).strip()
                    # Strip emojis
                    inner_html = re.sub(r'[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF]', '', inner_html)
                    
                    # Clean any lingering <!DOCTYPE or <html> or <head> or <style> tags inside inner_html
                    inner_html = re.sub(r'<!DOCTYPE[^>]*>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'<html[^>]*>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'</html>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'<head[^>]*>.*?</head>', '', inner_html, flags=re.DOTALL | re.IGNORECASE)
                    inner_html = re.sub(r'<style[^>]*>.*?</style>', '', inner_html, flags=re.DOTALL | re.IGNORECASE)
                    inner_html = re.sub(r'<body[^>]*>', '', inner_html, flags=re.IGNORECASE)
                    inner_html = re.sub(r'</body>', '', inner_html, flags=re.IGNORECASE)

                    clean_stitle = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', stitle).strip()
                    if not clean_stitle or clean_stitle.startswith("<!DOCTYPE") or clean_stitle.startswith("<html"):
                        clean_stitle = f"Chủ đề trọng tâm {len(scenes) + 1}"

                    scenes.append({
                        "scene_title": clean_stitle,
                        "short_title": clean_stitle,
                        "action_title": clean_stitle,
                        "html_content": inner_html,
                        "layout_type": "CUSTOM_RAW"
                    })
            else:
                # Parse pure markdown slide deck
                blocks = file_text.split('---')
                for b_idx, block in enumerate(blocks, 1):
                    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
                    if not lines:
                        continue
                    stitle = lines[0].lstrip("#").strip()
                    if any(k in stitle.lower() for k in ["mục lục", "tổng quan", "trang bìa", "slide tổng hợp"]):
                        continue
                    scenes.append({
                        "scene_title": stitle,
                        "short_title": stitle,
                        "action_title": stitle,
                        "html_content": f"<div style='padding:20px;'><h3 style='font-size:20px;font-weight:700;color:#0f172a;'>{stitle}</h3><div style='margin-top:12px;font-size:15px;color:#334155;'>{'<br>'.join(lines[1:])}</div></div>",
                        "layout_type": "CUSTOM_RAW"
                    })
        except Exception as e:
            print(f"  [Warning] Error parsing {file_to_read}: {e}")

        lessons_data.append({
            "lesson_id": f"Lesson {idx:02d}",
            "lesson_title": full_lesson_name,
            "scenes": scenes
        })

    if lessons_data:
        master_slide_html = slide_generator_agent.generate_session_deck_html(
            session_title=session_title,
            module_name="Lập trình Python",
            lessons_data=lessons_data
        )
        output_path = session_dir / "session_slides.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(master_slide_html)
        print(f"  [Session Compiler] Successfully compiled master session slides: {output_path.name}")


def _build_session_reading_html(session_title: str, html_files: list, is_static: bool = False) -> str:
    """
    Builds a 100% faithful Master Session Reading Hub (reading_all.html)
    using isolated lesson viewports in a clean white light theme with official Rikkei Education logo.
    Uses opacity/z-index instead of display:none to guarantee 100% flawless Mermaid diagram layout rendering on all tabs.
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
            <iframe id="frame-{idx}" src="{rel_path}" class="lesson-frame {active_frame_cls}"></iframe>"""
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
      .lesson-frame {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; opacity: 0; pointer-events: none; z-index: 1; transition: opacity 0.15s ease-in-out; }}
      .lesson-frame.active {{ opacity: 1; pointer-events: auto; z-index: 10; }}
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
          if (doc && doc.head && !doc.getElementById('hide-inner-hdr')) {{
            const style = doc.createElement('style');
            style.id = 'hide-inner-hdr';
            style.textContent = '#sticky-header, header, .sticky-nav {{ display: none !important; }} body {{ padding-top: 0 !important; }}';
            doc.head.appendChild(style);
          }}
        }} catch(e) {{}}
      }}

      function switchLesson(idx) {{
        const btns = document.querySelectorAll('.sidebar-nav-btn');
        const frames = document.querySelectorAll('.lesson-frame');
        
        btns.forEach((btn, i) => {{
          if (i + 1 === idx) {{
            btn.classList.add('active');
          }} else {{
            btn.classList.remove('active');
          }}
        }});

        frames.forEach((frame, i) => {{
          if (i + 1 === idx) {{
            frame.classList.add('active');
            hideIframeHeader(frame);
            try {{
              if (frame.contentWindow && frame.contentWindow.mermaid && typeof frame.contentWindow.mermaid.run === 'function') {{
                frame.contentWindow.mermaid.run();
              }}
            }} catch(e) {{}}
          }} else {{
            frame.classList.remove('active');
          }}
        }});
      }}
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


def _build_session_reading_html(session_title: str, html_files: list, is_static: bool = False) -> str:
    """
    Builds a 100% faithful Master Session Reading Hub (reading_all.html)
    using isolated lesson viewports in a clean white light theme with official Rikkei Education logo.
    Uses opacity/z-index instead of display:none to guarantee 100% flawless Mermaid diagram layout rendering on all tabs.
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
            <iframe id="frame-{idx}" src="{rel_path}" class="lesson-frame {active_frame_cls}"></iframe>"""
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
      .lesson-frame {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; opacity: 0; pointer-events: none; z-index: 1; transition: opacity 0.15s ease-in-out; }}
      .lesson-frame.active {{ opacity: 1; pointer-events: auto; z-index: 10; }}
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
          if (doc && doc.head && !doc.getElementById('hide-inner-hdr')) {{
            const style = doc.createElement('style');
            style.id = 'hide-inner-hdr';
            style.textContent = '#sticky-header, header, .sticky-nav {{ display: none !important; }} body {{ padding-top: 0 !important; }}';
            doc.head.appendChild(style);
          }}
        }} catch(e) {{}}
      }}

      function switchLesson(idx) {{
        const btns = document.querySelectorAll('.sidebar-nav-btn');
        const frames = document.querySelectorAll('.lesson-frame');
        
        btns.forEach((btn, i) => {{
          if (i + 1 === idx) {{
            btn.classList.add('active');
          }} else {{
            btn.classList.remove('active');
          }}
        }});

        frames.forEach((frame, i) => {{
          if (i + 1 === idx) {{
            frame.classList.add('active');
            hideIframeHeader(frame);
            try {{
              if (frame.contentWindow && frame.contentWindow.mermaid && typeof frame.contentWindow.mermaid.run === 'function') {{
                frame.contentWindow.mermaid.run();
              }}
            }} catch(e) {{}}
          }} else {{
            frame.classList.remove('active');
          }}
        }});
      }}
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