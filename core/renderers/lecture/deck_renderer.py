"""
core/renderers/lecture/deck_renderer.py
Master HTML Presentation Slide Deck Renderer for Classroom Lectures.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.renderers.lecture.text_sanitizer import sanitize_slide_text, clean_title_string

LOGO_URL = "https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"

def extract_session_summary_bullets(lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> List[str]:
    """Extract summary bullets directly from actual lesson scenes and content."""
    raw_bullets = []
    seen_keys = set()

    def clean_and_add(txt: str):
        if not txt:
            return
        cleaned = str(txt).strip()
        cleaned = re.sub(r'^\s*[\-\•\*\d\.]+\s*', '', cleaned).strip()
        cleaned = re.sub(r'<[^>]+>', '', cleaned).strip()
        cleaned = re.sub(r'^\s*(Nguyên lý|Quy chuẩn|Phòng tránh|Chuẩn hóa|Bẫy lỗi|Gotchas|Lưu ý)\s*[\&A-Za-z\s]*\:\s*', '', cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r'\.+$', '', cleaned) + '.'

        words = cleaned.split()
        if len(words) > 28:
            cleaned = " ".join(words[:28]) + "..."

        key = cleaned.lower()[:30]
        if len(cleaned) > 10 and key not in seen_keys:
            seen_keys.add(key)
            raw_bullets.append(cleaned)

    for l_data in lessons_data:
        if not isinstance(l_data, dict):
            continue
        scenes = l_data.get("scenes", [])
        for scene in scenes:
            if not isinstance(scene, dict):
                continue
            sc_bullets = scene.get("bullets") or scene.get("summary_bullets") or scene.get("key_takeaways")
            if isinstance(sc_bullets, list):
                for b in sc_bullets:
                    b_str = str(b).strip()
                    if ':' in b_str and not b_str.startswith("http"):
                        parts = b_str.split(':', 1)
                        clean_and_add(f"{parts[0].strip()} - {parts[1].strip()}")
                    else:
                        clean_and_add(b_str)

    if len(raw_bullets) < 3 and core_ssot and isinstance(core_ssot, dict):
        concepts = core_ssot.get("concepts")
        if isinstance(concepts, dict):
            for cname, cdesc in concepts.items():
                clean_and_add(f"{cname}: {cdesc}")
        elif isinstance(concepts, list):
            for c in concepts:
                clean_and_add(str(c))

    if len(raw_bullets) < 3:
        for l_data in lessons_data:
            l_title = l_data.get("lesson_title") or ""
            clean_lt = clean_title_string(l_title)
            clean_lt = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_lt, flags=re.IGNORECASE).strip()
            clean_lt = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_lt, flags=re.IGNORECASE).strip()
            if clean_lt:
                clean_and_add(f"Thực hành thành thạo: {clean_lt}")

    return raw_bullets[:4]

def render_scene_content_html(scene: Dict[str, Any], clean_stitle: str, is_cli_or_tooling: bool = False) -> str:
    """Renders inner HTML slide content matching Bento Grid layout archetypes."""
    layout_type = str(scene.get("layout_type") or "").upper()
    
    if layout_type == "CUSTOM_RAW" and scene.get("html_content"):
        return scene.get("html_content")

    narration = scene.get("narration") or scene.get("explanation") or ""
    bullets = scene.get("bullets", [])
    code_sample = scene.get("code_sample") or scene.get("code") or ""
    mermaid_code = scene.get("mermaid") or scene.get("diagram") or ""
    image_url = scene.get("image_url") or scene.get("image_path") or scene.get("image") or ""
    image_caption = scene.get("image_caption") or scene.get("caption") or "Hình minh họa bối cảnh kỹ thuật thực tế"

    if not bullets and narration:
        raw_sentences = [s.strip() for s in re.split(r'[\.\;\n]', narration) if len(s.strip()) > 10]
        bullets = raw_sentences[:4]

    # 1. IMAGE EXPLAINER LAYOUT
    if "IMAGE" in layout_type or image_url:
        bullet_items_html = ""
        if bullets:
            for b in bullets[:4]:
                parts = b.split(':', 1) if ':' in b else [b, ""]
                title_p = sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[0]).strip())
                desc_p = sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[1] if len(parts) > 1 else parts[0]).strip())
                bullet_items_html += f"""
            <div class="flex items-start gap-3">
              <i class="ph-bold ph-check-circle text-rikkei-red text-xl shrink-0 mt-0.5"></i>
              <div>
                <div class="font-bold text-slate-900 text-[17px] mb-1">{title_p}</div>
                <p class="text-slate-700 text-[15px] leading-relaxed font-normal">{desc_p}</p>
              </div>
            </div>"""
        else:
            bullet_items_html = f"""
            <div class="text-slate-700 text-[15px] leading-relaxed">
              {sanitize_slide_text(narration[:300]) if narration else 'Hình ảnh minh họa bối cảnh thực tế và quy trình vận hành hệ thống.'}
            </div>"""

        image_caption_clean = sanitize_slide_text(image_caption)
        return f"""
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
        <div class="flex flex-col justify-start items-center w-full h-fit">
          <img src="{image_url}" alt="{clean_stitle}" class="w-full max-h-[440px] object-contain rounded-xl" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80';"/>
          <p class="text-slate-500 text-[14px] italic mt-3 text-center font-medium">{image_caption_clean}</p>
        </div>
        <div class="bento-card p-6 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-start gap-4 text-left h-fit shadow-sm">
          <div>
            <h5 class="font-bold text-slate-900 text-[20px] mb-4 flex items-center gap-2.5">
              <i class="ph-bold ph-lightbulb text-rikkei-red text-2xl"></i> Bối cảnh &amp; phân tích dự án
            </h5>
            <div class="space-y-4">
              {bullet_items_html}
            </div>
          </div>
          <div class="mt-2 p-3 bg-white border border-slate-200 rounded-xl flex items-center gap-2.5 text-slate-800 text-[14px] font-semibold shadow-sm">
            <i class="ph-bold ph-shield-check text-emerald-600 text-lg shrink-0"></i>
            <span>Quy trình vận hành &amp; tự động hóa hệ thống.</span>
          </div>
        </div>
      </div>
"""

    # 2. MERMAID DIAGRAM LAYOUT
    elif "MERMAID" in layout_type or mermaid_code:
        clean_mermaid = mermaid_code.strip()
        return f"""
      <div class="w-full flex justify-center bg-slate-50 p-6 rounded-xl border border-slate-200 mt-9 mb-auto items-center h-fit">
        <div class="mermaid w-full max-w-4xl scale-105">
          {clean_mermaid}
        </div>
      </div>
"""

    # 3. CODE EXPLAINER LAYOUT
    elif code_sample or "CODE" in layout_type:
        lang = "bash" if is_cli_or_tooling else "python"
        bullet_items_html = ""
        if bullets:
            for b in bullets[:4]:
                parts = b.split(':', 1) if ':' in b else [b, ""]
                title_p = sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[0]).strip())
                desc_p = sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[1] if len(parts) > 1 else parts[0]).strip())
                bullet_items_html += f"""
            <div>
              <div class="font-bold text-slate-900 text-[17px] mb-1 flex items-center gap-2">
                <i class="ph-bold ph-caret-right text-rikkei-red"></i> {title_p}:
              </div>
              <p class="text-slate-600 text-[14px] leading-relaxed pl-5">{desc_p}</p>
            </div>"""
        else:
            bullet_items_html = f"""
            <div>
              <div class="font-bold text-slate-900 text-[17px] mb-1 flex items-center gap-2">
                <i class="ph-bold ph-caret-right text-rikkei-red"></i> Nguyên lý thực thi thực tế:
              </div>
              <p class="text-slate-600 text-[14px] leading-relaxed pl-5">{sanitize_slide_text(narration[:240]) if narration else 'Mã nguồn minh họa cơ chế hoạt động của hệ thống.'}</p>
            </div>"""

        safe_code = code_sample.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f"""
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
        <div class="bento-card p-6 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-start gap-4 text-left h-fit shadow-sm">
          <div>
            <h5 class="font-bold text-slate-900 text-[20px] mb-4 flex items-center gap-2.5">
              <i class="ph-bold ph-book-open text-rikkei-red text-2xl"></i> Nguyên lý &amp; lưu ý thực thi
            </h5>
            <div class="space-y-4 text-slate-800 text-[15px]">
              {bullet_items_html}
            </div>
          </div>
          <div class="mt-2 p-3 bg-white border border-slate-200 rounded-xl flex items-center gap-2.5 text-slate-800 text-[14px] font-semibold shadow-sm">
            <i class="ph-bold ph-terminal-window text-rikkei-red text-lg shrink-0"></i>
            <span>Thao tác thực thi theo quy chuẩn kỹ thuật.</span>
          </div>
        </div>
        <div class="flex flex-col h-fit">
          <pre class="bg-slate-900 text-emerald-400 p-6 rounded-xl font-mono text-[14px] overflow-auto border border-slate-800 shadow-xl leading-relaxed max-h-[380px] h-fit"><code class="language-{lang}">{safe_code}</code></pre>
        </div>
      </div>
"""

    # 4. GOOD VS BAD COMPARISON LAYOUT
    elif "COMPARISON" in layout_type or scene.get("bad_practice") or scene.get("good_practice"):
        bad = scene.get("bad_practice") or {}
        good = scene.get("good_practice") or {}
        
        bad_raw = bad.get("title") or "Thao tác thủ công"
        bad_clean = sanitize_slide_text(re.sub(r'^(Anti-Pattern|Cách làm sai)\s*[\:\-]?\s*', '', re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', bad_raw).strip(), flags=re.IGNORECASE).strip())
        bad_code = bad.get("code") or (bullets[0] if len(bullets) > 0 else "Thao tác thủ công không qua kiểm thử")
        bad_reason = sanitize_slide_text(bad.get("reason") or "Dễ phát sinh lỗi hệ thống và rò rỉ dữ liệu.")

        good_raw = good.get("title") or "Quy trình tự động hóa"
        good_clean = sanitize_slide_text(re.sub(r'^(Best Practice|Quy chuẩn đúng)\s*[\:\-]?\s*', '', re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', good_raw).strip(), flags=re.IGNORECASE).strip())
        good_code = good.get("code") or (bullets[1] if len(bullets) > 1 else "Chuẩn hóa quy trình vận hành tự động")
        good_reason = sanitize_slide_text(good.get("reason") or "Đảm bảo tính ổn định và tối ưu hiệu năng làm việc.")

        return f"""
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
        <div class="bento-card p-6 rounded-xl border border-red-200 bg-red-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
          <div class="select-none">
            <h5 class="font-bold text-red-900 text-[20px] flex items-center gap-2.5 mb-3.5">
              <i class="ph-bold ph-x-circle text-2xl text-red-600 shrink-0"></i> <span>Anti-Pattern: {bad_clean}</span>
            </h5>
            <pre class="bg-red-100/60 text-red-950 p-4 rounded-xl font-mono text-sm mb-3.5 border border-red-200 shadow-sm"><code>{bad_code}</code></pre>
            <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
              {bad_reason}
            </p>
          </div>
          <div class="p-3 bg-red-100/70 border border-red-200 rounded-xl text-red-900 text-xs font-semibold flex items-center gap-2 mt-1">
            <i class="ph-bold ph-warning text-red-600 text-base shrink-0"></i>
            <span>Cảnh báo rủi ro phát sinh sự cố.</span>
          </div>
        </div>
        <div class="bento-card p-6 rounded-xl border border-emerald-200 bg-emerald-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
          <div class="select-none">
            <h5 class="font-bold text-emerald-900 text-[20px] flex items-center gap-2.5 mb-3.5">
              <i class="ph-bold ph-check-circle text-2xl text-emerald-600 shrink-0"></i> <span>Best Practice: {good_clean}</span>
            </h5>
            <pre class="bg-emerald-100/60 text-emerald-950 p-4 rounded-xl font-mono text-sm mb-3.5 border border-emerald-200 shadow-sm"><code>{good_code}</code></pre>
            <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
              {good_reason}
            </p>
          </div>
          <div class="p-3 bg-emerald-100/70 border border-emerald-200 rounded-xl text-emerald-900 text-xs font-semibold flex items-center gap-2 mt-1">
            <i class="ph-bold ph-seal-check text-emerald-600 text-base shrink-0"></i>
            <span>Quy trình chuẩn hóa thực tế.</span>
          </div>
        </div>
      </div>
"""

    # 5. DEFAULT 2-COLUMN BENTO GRID CARDS LAYOUT
    else:
        p_text1 = sanitize_slide_text(bullets[0] if len(bullets) > 0 else (narration[:240] if narration else f"Hạn chế khi phát triển hệ thống với {clean_stitle}."))
        p_text2 = sanitize_slide_text(bullets[1] if len(bullets) > 1 else (narration[240:480] if len(narration) > 240 else f"Giải pháp quy trình cho {clean_stitle}."))
        
        c1_title = sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', scene.get("col1_title") or "Vấn đề thực tế").strip())
        c2_title = sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', scene.get("col2_title") or "Giải pháp áp dụng").strip())

        return f"""
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
        <div class="bento-card p-6 rounded-xl border border-red-200 bg-red-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
          <div class="select-none">
            <h5 class="font-bold text-red-900 text-[20px] flex items-center gap-2.5 mb-3.5">
              <i class="ph-bold ph-x-circle text-2xl text-red-600 shrink-0"></i> <span>{c1_title}</span>
            </h5>
            <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
              {p_text1}
            </p>
          </div>
          <div class="p-3 bg-red-100/70 border border-red-200 rounded-xl text-red-900 text-xs font-semibold flex items-center gap-2 mt-1">
            <i class="ph-bold ph-warning text-red-600 text-base shrink-0"></i>
            <span>Rủi ro phát sinh lỗi và chậm tiến độ.</span>
          </div>
        </div>
        <div class="bento-card p-6 rounded-xl border border-emerald-200 bg-emerald-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
          <div class="select-none">
            <h5 class="font-bold text-emerald-900 text-[20px] flex items-center gap-2.5 mb-3.5">
              <i class="ph-bold ph-check-circle text-2xl text-emerald-600 shrink-0"></i> <span>{c2_title}</span>
            </h5>
            <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
              {p_text2}
            </p>
          </div>
          <div class="p-3 bg-emerald-100/70 border border-emerald-200 rounded-xl text-emerald-900 text-xs font-semibold flex items-center gap-2 mt-1">
            <i class="ph-bold ph-seal-check text-emerald-600 text-base shrink-0"></i>
            <span>Tối ưu hiệu năng và quy trình làm việc.</span>
          </div>
        </div>
      </div>
"""

def generate_session_deck_html(session_title: str, module_name: str, lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> str:
    """Master HTML Lecture Deck Compiler for 1 Session matching templates/slide_template.html."""
    current_year = datetime.now().year
    copyright_text = f"© {current_year} By Rikkei Education - All rights reserved."

    m_sess = re.search(r'(Session\s*\d+)', session_title, re.IGNORECASE)
    if m_sess:
        session_tag_text = m_sess.group(1).title()
    else:
        session_tag_text = "Session 01"

    main_title_text = clean_title_string(session_title)
    clean_session_title = f"{session_tag_text} - {main_title_text}"

    clean_module_name = module_name.strip()
    if not clean_module_name or clean_module_name.upper() in ["PYTHON", "GIT", "WEB", "IT"]:
        clean_module_name = "Chương trình Đào tạo Công nghệ Thông tin"

    ts_lower = (session_title + " " + module_name).lower()
    is_cli_or_tooling = any(k in ts_lower for k in ["git", "vcs", "terminal", "cli", "bash", "docker", "agile", "scrum", "uml", "figma", "ui", "design"])

    slide_wrappers_html = []

    # 1. Cover Slide
    slide_wrappers_html.append(f"""
  <!-- Slide 0: Cover Slide -->
  <div class="slide-wrapper" id="slide-1" data-slide-index="0">
    <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-16 overflow-hidden">
      <div class="absolute left-0 top-1/2 -translate-y-1/2 w-12 h-40 bg-rikkei-red" style="clip-path: polygon(0 0, 0 100%, 100% 50%)"></div>
      <div class="my-auto ml-10 space-y-5 text-left select-none max-w-none w-full pr-12">
        <h2 class="font-montserrat font-extrabold text-[38px] text-rikkei-red">
          {session_tag_text}:
        </h2>
        <h1 class="font-montserrat font-extrabold text-[52px] text-black leading-tight break-words w-full">
          {main_title_text}
        </h1>
        <div class="pt-8 space-y-2 text-slate-600 text-[22px] font-medium">
          <p>Môn học: {clean_module_name}</p>
        </div>
      </div>
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 w-full max-w-200 text-center">
        <img alt="Rikkei Academy Logo" class="h-10 object-contain" src="{LOGO_URL}"/>
        <span class="text-[16px] text-black font-normal">
          {copyright_text}
        </span>
      </div>
      <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
        <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">1</span>
      </div>
    </section>
  </div>""")

    # 2. Agenda Slide
    agenda_items_html = ""
    agenda_index = 1
    for l_data in lessons_data:
        l_title = l_data.get("lesson_title") or f"Bài học {agenda_index}"
        clean_l_title = clean_title_string(l_title)
        clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
        clean_l_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_l_title, flags=re.IGNORECASE).strip()
        agenda_items_html += f"""
        <div class="flex items-start gap-5 text-[30px] font-sans font-bold text-black leading-snug w-full">
          <span class="w-10 shrink-0 text-black">{agenda_index}.</span>
          <span class="flex-1 break-words">{clean_l_title}</span>
        </div>"""
        agenda_index += 1

    slide_wrappers_html.append(f"""
  <!-- Slide 1: Agenda Slide -->
  <div class="slide-wrapper" id="slide-2" data-slide-index="1">
    <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-12 overflow-hidden">
      <div class="w-full flex-1 flex flex-col justify-start">
        <div class="flex justify-between items-start select-none shrink-0 mb-9 w-full">
          <div class="text-[36px] font-montserrat font-extrabold text-rikkei-red leading-none">
            NỘI DUNG BÀI HỌC
          </div>
          <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{LOGO_URL}"/>
        </div>
        <div class="w-full flex flex-col justify-start pl-4 pr-4">
          <div class="space-y-8 text-left select-none w-full max-w-none">
            {agenda_items_html}
          </div>
        </div>
      </div>
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-center w-full max-w-200">
        <span class="text-[16px] text-black font-normal">
          {copyright_text}
        </span>
      </div>
      <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
        <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">2</span>
      </div>
    </section>
  </div>""")

    # 3..N. Content Slides
    page_counter = 3
    slide_wrapper_idx = 2

    for l_idx, l_data in enumerate(lessons_data, 1):
        l_title = l_data.get("lesson_title") or f"Bài học {l_idx}"
        clean_l_title = clean_title_string(l_title)
        clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
        clean_l_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_l_title, flags=re.IGNORECASE).strip()

        scenes = l_data.get("scenes", [])
        for s_idx, scene in enumerate(scenes, 1):
            raw_stitle = scene.get("action_title") or scene.get("short_title") or scene.get("scene_title") or f"Chủ đề {s_idx}"
            clean_stitle = clean_title_string(raw_stitle)
            clean_stitle = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', clean_stitle).strip()
            clean_stitle = re.sub(r'\s+(Trong|Dành cho|Với)\s+.*$', '', clean_stitle, flags=re.IGNORECASE).strip()
            
            main_large_title = f"{l_idx}. {clean_l_title}"
            inner_content = render_scene_content_html(scene, clean_stitle, is_cli_or_tooling=is_cli_or_tooling)

            slide_wrappers_html.append(f"""
  <!-- Slide {slide_wrapper_idx}: Content Slide -->
  <div class="slide-wrapper" id="slide-{page_counter}" data-slide-index="{slide_wrapper_idx}" data-lesson-id="lesson-{l_idx}">
    <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-12 overflow-hidden">
      <div class="w-full flex-1 flex flex-col justify-start h-full">
        <div class="flex justify-between items-start select-none shrink-0 mb-0 w-full">
          <div class="w-full pr-8">
            <div class="text-[34px] font-montserrat font-extrabold text-rikkei-red leading-snug w-full break-words">
              {main_large_title}
            </div>
            <div class="text-[24px] font-sans font-bold text-black mt-3 w-full break-words">
              {clean_stitle}
            </div>
          </div>
          <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{LOGO_URL}"/>
        </div>
        {inner_content}
      </div>
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-center w-full max-w-200">
        <span class="text-[16px] text-black font-normal">
          {copyright_text}
        </span>
      </div>
      <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
        <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">{page_counter}</span>
      </div>
    </section>
  </div>""")
            page_counter += 1
            slide_wrapper_idx += 1

    # 4. Summary Slide
    summary_bullets = extract_session_summary_bullets(lessons_data, core_ssot)
    summary_items_html = ""
    for s_bullet in summary_bullets:
        summary_items_html += f"""
        <div class="flex items-start gap-4 text-[26px] font-sans font-bold text-black leading-relaxed w-full">
          <i class="ph-bold ph-check-circle text-rikkei-red text-3xl shrink-0 mt-1"></i>
          <span class="flex-1 break-words">{s_bullet}</span>
        </div>"""

    slide_wrappers_html.append(f"""
  <!-- Slide {slide_wrapper_idx}: Summary Slide -->
  <div class="slide-wrapper" id="slide-{page_counter}" data-slide-index="{slide_wrapper_idx}">
    <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-12 overflow-hidden">
      <div class="w-full flex-1 flex flex-col justify-start">
        <div class="flex justify-between items-start select-none shrink-0 mb-9 w-full">
          <div class="text-[36px] font-montserrat font-extrabold text-rikkei-red leading-none">
            TỔNG KẾT BÀI HỌC
          </div>
          <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{LOGO_URL}"/>
        </div>
        <div class="w-full flex flex-col justify-start pl-4 pr-4">
          <div class="space-y-6 text-left select-none w-full max-w-none">
            {summary_items_html}
          </div>
        </div>
      </div>
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-center w-full max-w-200">
        <span class="text-[16px] text-black font-normal">
          {copyright_text}
        </span>
      </div>
      <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
        <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">{page_counter}</span>
      </div>
    </section>
  </div>""")

    template_file = Path("templates/html/slide_template.html")
    if not template_file.exists():
        template_file = Path("templates/slide_template.html")

    if template_file.exists():
        template_content = template_file.read_text(encoding="utf-8")
        nav_links_list = []
        current_slide_idx = 2
        for idx, l_data in enumerate(lessons_data, 1):
            l_title = l_data.get("lesson_title") or f"Bài học {idx}"
            clean_l_title = clean_title_string(l_title)
            clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
            
            nav_links_list.append(f"""
      <a id="nav-lesson-{idx}" href="#slide-{current_slide_idx + 1}" class="hover:text-rikkei-red transition-all border-b-2 border-transparent pb-1 text-slate-600">
        {clean_l_title}
      </a>""")
            num_scenes = len(l_data.get("scenes", [])) or 3
            current_slide_idx += num_scenes
            
        nav_links_html = "".join(nav_links_list)
        
        full_html = template_content
        full_html = full_html.replace("{{SESSION_TITLE}}", f"{clean_session_title} — Rikkei Master Presentation")
        full_html = full_html.replace("{{MODULE_NAME}}", clean_module_name)
        full_html = full_html.replace("{{NAV_LINKS}}", nav_links_html)
        full_html = full_html.replace("{{SLIDES_CONTENT}}", "".join(slide_wrappers_html))
        
        return full_html
    else:
        raise FileNotFoundError("Master slide template file not found at templates/html/slide_template.html")
