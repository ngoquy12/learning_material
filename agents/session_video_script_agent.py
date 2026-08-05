# agents/session_video_script_agent.py
import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List
from core.llm import call_llm
from core.skills import load_skill_content

def extract_lesson_slides(session_html: str, lesson_title: str) -> str:
    """
    Trích xuất các section slide liên quan đến bài học cụ thể từ file Session Slide HTML.
    Giả định các slide được bọc trong <section class="slide">...</section>.
    Sử dụng heuristic đơn giản: Nếu slide chứa tên bài học hoặc thuộc cụm bài học đó.
    """
    slides = re.findall(r'<section\s+class="[^"]*slide[^"]*".*?</section>', session_html, flags=re.IGNORECASE | re.DOTALL)
    
    lesson_slides = []
    # Tìm kiếm slide bắt đầu của bài học này
    started = False
    
    # Rút gọn lesson title để matching dễ hơn
    clean_title = re.sub(r'^(Bài|Lesson)\s*\d+[\s\-\:]+', '', lesson_title, flags=re.IGNORECASE).strip()
    clean_title_lower = clean_title.lower()
    
    for slide in slides:
        slide_text = re.sub(r'<[^>]+>', ' ', slide).lower()
        if clean_title_lower in slide_text:
            started = True
            
        if started:
            lesson_slides.append(slide)
    
    if lesson_slides:
        return "\n".join(lesson_slides[:8]) # Max 8 slides per lesson to avoid context bloat
    
    return session_html[:5000] # Fallback: return first part of session if not found


def generate_session_video_scripts(
    session_id: str,
    session_title: str,
    session_dir_path: str,
    tech_stack: str,
    session_slides_html: str,
    lessons_data: List[Dict[str, Any]]
):
    """
    Session-Level Video Script Agent:
    Tự động biên soạn Kịch bản Video chuẩn HTML Teleprompter cho tất cả các bài học trong Session.
    Nguồn sự thật (SSOT) được lấy từ file Slide của Session.
    Lưu vào thư mục: Session XX/Tên Bài Học/Video/video_script.html
    """
    session_dir = Path(session_dir_path)
    
    print(f"\n  ---> [Session Video Script Agent] Đang tạo Kịch bản Studio Teleprompter HTML cho toàn bộ {session_id}...")
    
    template_path = Path("templates/video_script_template.html")
    if not template_path.exists():
        print("  [Warning] templates/video_script_template.html không tồn tại, sẽ sử dụng mã HTML tĩnh.")
        template_html = "<html><body><h1>{{LESSON_TITLE}}</h1>{{NAV_ITEMS}}{{SCENE_BLOCKS}}</body></html>"
    else:
        template_html = template_path.read_text(encoding="utf-8")

    for idx, lesson in enumerate(lessons_data):
        lesson_id = lesson.get("lesson_id", f"Lesson {idx+1:02d}")
        lesson_title = lesson.get("title", "")
        
        print(f"    - Bóc tách và tạo kịch bản cho: {lesson_id} - {lesson_title}")
        
        # 1. Bóc tách Slide của Lesson này
        relevant_slides = extract_lesson_slides(session_slides_html, lesson_title)
        
        system_prompt = f"""You are an Expert Studio Assistant Director & E-Learning Production Engineer at Rikkei Education.
Your mission is to generate a complete INTERACTIVE TELEPROMPTER STUDIO SCRIPT in JSON format, heavily based on the provided SLIDE PRESENTATION CONTENT.

MANDATORY PEDAGOGICAL & SPEECH DIRECTIVES:
1. **Source of Truth (SSOT)**: 100% of the speech and visual actions MUST be derived directly from the provided SLIDE CONTENT. Each slide in the presentation should correspond to exactly 1 Scene (scene_id).
2. **Speech Format**:
   - Short pause: `<span class="pause-tag">/</span>`
   - Long breath: `<span class="pause-tag">//</span>`
   - Keyword badge: `<span class="highlight-keyword">...</span>`
   - Emphasis badge: `<span class="highlight-emphasis">...</span>`
3. **Intro/Outro**:
   - Scene 1 MUST start with: "Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong bài học này, chúng ta sẽ cùng tìm hiểu về {lesson_title}."
   - Final Scene MUST conclude and thank the student.
4. **Visual Actions**: Array of UI badges showing what happens on screen (e.g. "Chuyển sang Slide 2", "Hiển thị code block").
5. **100% Accented Vietnamese**: All speech text MUST be in standard accented Vietnamese.

OUTPUT JSON SCHEMA:
{{
    "scenes": [
        {{
            "scene_id": 1,
            "title": "Tiêu đề Slide (Trích từ HTML)",
            "time_range": "00:00 - 00:45",
            "camera_type": "Cam 1 (Close-up) hoặc Cam 2 (IDE Screen)",
            "camera_icon": "ph-video-camera",
            "camera_color": "text-rikkei-red dark:text-rose-400",
            "visual_actions": [
                {{"icon": "ph-presentation", "text": "Hiển thị Slide 1", "color_theme": "indigo"}}
            ],
            "code_snippet": "Trích xuất code từ slide vào đây (nếu có), không có thì để trống",
            "speech_html": "Chào mừng các bạn <span class=\\"pause-tag\\">/</span> đã quay trở lại..."
        }}
    ]
}}
"""

        user_prompt = f"""Generate the Teleprompter JSON Script for:
Subject: {tech_stack}
Session: {session_id} - {session_title}
Lesson Title: {lesson_title}

--- RELEVANT SLIDES EXTRACTED FROM SESSION DECK (SSOT) ---
{relevant_slides}

MANDATORY: Return ONLY valid JSON matching the schema, with one scene per slide.
"""

        json_resp = call_llm(
            system_prompt,
            user_prompt,
            json_mode=True,
            agent_name="Session_Video_Script_Agent",
            session_id=session_id,
            lesson_id=lesson_id
        )
        
        try:
            data = json.loads(json_resp.replace('`json', '').replace('`', '').strip(), strict=False)
            scenes = data.get("scenes", [])
        except Exception as e:
            print(f"      [Error] parsing JSON for {lesson_id}: {e}")
            continue

        nav_items_html = ""
        scene_blocks_html = ""
        
        for i, s in enumerate(scenes):
            sc_title = s.get("title", f"Slide {i+1}")
            time_range = s.get("time_range", "00:00 - 01:00")
            cam_type = s.get("camera_type", "Cam 1 (Close-up)")
            cam_icon = s.get("camera_icon", "ph-video-camera")
            cam_color = s.get("camera_color", "text-rikkei-red")
            speech = s.get("speech_html", "")
            code = s.get("code_snippet", "")
            
            nav_class = "border-rikkei-red bg-rose-50/70 dark:bg-rose-950/40 text-rikkei-red dark:text-rose-400 font-bold shadow-xs" if i == 0 else "border-transparent text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60"
            
            nav_items_html += f"""
        <!-- Nav Item {i} -->
        <button onclick="scrollToScene({i})" id="nav-item-{i}" class="nav-item w-full text-left p-3 rounded-xl border-l-4 transition-all flex flex-col gap-1.5 {nav_class}">
          <div class="flex items-center justify-between">
            <span class="font-mono text-[11px] font-bold">Phân cảnh {i+1}</span>
            <span class="font-mono text-[11px] opacity-80">{time_range}</span>
          </div>
          <span class="text-xs font-bold leading-snug">{sc_title}</span>
          <div class="flex items-center gap-1.5 text-[10px] opacity-80 font-medium">
            <i class="ph-bold {cam_icon} {cam_color}"></i>
            <span>{cam_type}</span>
          </div>
        </button>"""
            
            visual_actions_html = ""
            for v in s.get("visual_actions", []):
                theme = v.get("color_theme", "indigo")
                v_icon = v.get("icon", "ph-presentation")
                v_text = v.get("text", "")
                visual_actions_html += f"""
                <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-semibold bg-{theme}-50 dark:bg-{theme}-950/60 text-{theme}-700 dark:text-{theme}-300 border border-{theme}-200 dark:border-{theme}-800">
                  <i class="ph-bold {v_icon}"></i> {v_text}
                </span>"""
                
            code_card = ""
            if code and len(code.strip()) > 0:
                code_card = f"""
            <div class="bg-slate-900 dark:bg-slate-950 rounded-xl p-4 border border-slate-800 font-mono text-xs text-slate-200 relative group shadow-inner mt-4">
              <pre class="whitespace-pre text-emerald-400 text-xs leading-relaxed"><code class="language-{tech_stack.split('/')[0].lower() if tech_stack else 'javascript'}">{code}</code></pre>
            </div>"""
            
            scene_blocks_html += f"""
      <!-- Scene Block {i} -->
      <div id="scene-{i}" class="scene-block bg-white dark:bg-rikkei-cardDark border border-slate-200 dark:border-slate-800 rounded-2xl p-5 md:p-7 shadow-xs scroll-mt-24 transition-all duration-300">
        <div class="flex flex-col lg:flex-row gap-6">
          <div class="lg:w-[400px] shrink-0 flex flex-col gap-4">
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-rose-100 dark:bg-rose-950/70 text-rikkei-red dark:text-rose-400 text-xs font-bold font-mono">
                <i class="ph-bold ph-film-strip"></i> Phân cảnh {i+1:02d}
              </span>
              <span class="text-slate-500 dark:text-slate-400 font-mono text-xs font-bold flex items-center gap-1">
                <i class="ph-bold ph-clock text-slate-400"></i> {time_range}
              </span>
            </div>
            <div>
              <h3 class="text-slate-900 dark:text-slate-100 font-montserrat font-bold text-base leading-snug">{sc_title}</h3>
            </div>
            <div class="flex flex-col gap-2 bg-slate-50 dark:bg-slate-900/60 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800/80">
              <span class="text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Chỉ dẫn thao tác studio</span>
              <div class="flex items-center gap-2 text-xs font-bold text-slate-700 dark:text-slate-200">
                <i class="ph-bold {cam_icon} {cam_color} text-base"></i>
                <span>{cam_type}</span>
              </div>
              <div class="flex flex-wrap gap-1.5 mt-2">
                {visual_actions_html}
              </div>
            </div>
            {code_card}
          </div>
          <div class="flex-1 bg-slate-50 dark:bg-slate-900/70 p-5 md:p-6 rounded-2xl border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 mb-4 select-none">
                <span class="text-xs text-slate-600 dark:text-slate-300 font-bold flex items-center gap-1.5">
                  <i class="ph-bold ph-microphone-stage text-emerald-600 dark:text-emerald-400 text-base"></i>
                  Lời thoại Teleprompter
                </span>
                <span class="text-[11px] text-slate-400 dark:text-slate-500 font-mono font-medium hidden sm:inline">
                  / : ngắt nhịp ngắn &bull; // : ngắt hơi nghỉ
                </span>
              </div>
              <p class="teleprompter-text text-slate-900 dark:text-slate-100 text-[20px] leading-[1.85] font-semibold tracking-wide">
                {speech}
              </p>
            </div>
          </div>
        </div>
      </div>"""

        final_html = template_html.replace("{{LESSON_TITLE}}", lesson_title)
        final_html = final_html.replace("{{NAV_ITEMS}}", nav_items_html)
        final_html = final_html.replace("{{SCENE_BLOCKS}}", scene_blocks_html)
        
        lesson_folder = None
        clean_lesson_id = lesson_id.strip()
        for f in session_dir.iterdir():
            if f.is_dir() and f.name.startswith(clean_lesson_id):
                lesson_folder = f
                break
                
        if not lesson_folder:
            lesson_folder = session_dir / f"{lesson_id} - {lesson_title}".replace("/", "_")
            lesson_folder.mkdir(parents=True, exist_ok=True)
            
        video_dir = lesson_folder / "Video"
        video_dir.mkdir(exist_ok=True)
        
        out_file = video_dir / "video_script.html"
        out_file.write_text(final_html, encoding="utf-8")
        
        old_md = video_dir / "SCRIPT.md"
        if old_md.exists():
            old_md.unlink()
            
        print(f"      [Success] Saved HTML Teleprompter Script: {out_file}")
