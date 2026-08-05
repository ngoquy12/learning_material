
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
    [DISABLED] Cơ chế sinh reading_all.html đã được loại bỏ theo chỉ đạo hệ thống.
    Mỗi bài học sẽ giữ riêng file reading.html độc lập.
    """
    return

def _build_session_reading_html(session_title: str, html_files: list, is_static: bool = False) -> str:
    """
    Builds a 100% faithful Master Session Reading Hub (reading_all.html)
    using isolated lesson viewports in a clean white light theme with official Rikkei Education logo.
    Uses opacity/z-index instead of display:none to guarantee 100% flawless Mermaid diagram layout rendering on all tabs.
    Renders via Jinja2 Template (templates/session_reading_hub.html.jinja2).
    """
    import json
    import re
    from pathlib import Path
    from jinja2 import Environment, FileSystemLoader

    lessons_data = []

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

            lessons_data.append({
                "idx": idx,
                "full_name": full_lesson_name,
                "clean_name": clean_name,
                "rel_path": rel_path
            })
        except Exception as e:
            print(f"  [Session Compiler Warning] Failed to prepare lesson {item}: {e}")

    # Jinja2 Rendering
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=True)
    template = env.get_template("session_reading_hub.html.jinja2")

    return template.render(
        session_title=session_title,
        lessons=lessons_data
    )


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
            module_name="",
            lessons_data=lessons_data
        )
        output_path = session_dir / "session_slides.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(master_slide_html)
        print(f"  [Session Compiler] Successfully compiled master session slides: {output_path.name}")





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
            module_name="",
            lessons_data=lessons_data
        )
        output_path = session_dir / "session_slides.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(master_slide_html)
        print(f"  [Session Compiler] Successfully compiled master session slides: {output_path.name}")





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