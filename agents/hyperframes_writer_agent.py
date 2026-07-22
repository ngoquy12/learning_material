"""
agents/hyperframes_writer_agent.py

HyperFrames Composition Writer Agent:
Takes the approved video_script_json (Production Blueprint) from video_script_agent
and writes the actual HyperFrames project files:
  - index.html (root composition with absolute audio timestamps)
  - src/compositions/Scene_XX.html (sub-compositions with GSAP timelines)
  - meta.json
  - package.json
  - durations.json (placeholder until TTS runs)

Follows the dev-tutorial-video standard and hyperframes_composer/SKILL.md rules.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict

from core.state import AgentState


# ── Helper ─────────────────────────────────────────────────────────────────

def _sanitize_id(text: str) -> str:
    """Create a valid HTML id from text."""
    text = text.lower().strip()
    text = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", text)
    text = re.sub(r"[èéẹẻẽêềếệểễ]", "e", text)
    text = re.sub(r"[ìíịỉĩ]", "i", text)
    text = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", text)
    text = re.sub(r"[ùúụủũưừứựửữ]", "u", text)
    text = re.sub(r"[ỳýỵỷỹ]", "y", text)
    text = re.sub(r"[đ]", "d", text)
    text = re.sub(r"[^a-z0-9\s_-]", "", text)
    return re.sub(r"[\s]+", "-", text).strip("-")


def _build_root_index_html(blueprint: Dict[str, Any], lesson_slug: str) -> str:
    """Build the root index.html (master timeline) following HyperFrames audio-first architecture."""
    scenes = blueprint["scenes"]
    
    # Calculate exact total duration including intro (9.24s) and outro (12.15s)
    outro_start = round(scenes[-1]["start_at_root"] + scenes[-1]["duration"], 2) if scenes else 9.24
    total_dur = round(outro_start + 12.15, 2)

    # Scene clip divs
    scene_clips = []
    for scene in scenes:
        scene_id = scene["scene_id"]
        scene_slug = scene_id.replace("_", "-").lower()
        start = scene["start_at_root"]
        dur = scene["duration"]
        track = scene["track_index"]
        clip = (
            f'      <div class="clip"\n'
            f'           data-composition-src="src/compositions/{scene_id}.html"\n'
            f'           data-composition-id="{scene_slug}"\n'
            f'           data-start="{start}"\n'
            f'           data-duration="{dur}"\n'
            f'           data-track-index="{track}"></div>'
        )
        scene_clips.append(clip)

    # Audio elements with absolute timestamps — ALWAYS in root index.html
    audio_elements = []
    for i, scene in enumerate(scenes):
        scene_id = scene["scene_id"]
        scene_num = scene_id.replace("Scene_", "").zfill(2)
        start = scene["start_at_root"]
        dur = scene["duration"]
        audio_track_idx = 20 + i  # Audio tracks start at 20
        audio = (
            f'      <audio id="tts-{scene_num}"\n'
            f'             data-start="{start}"\n'
            f'             data-duration="{dur}"\n'
            f'             data-track-index="{audio_track_idx}"\n'
            f'             data-volume="1"\n'
            f'             src="assets/tts/{scene_id}.mp3"></audio>'
        )
        audio_elements.append(audio)

    scene_clips_str = "\n\n".join(scene_clips)
    audio_str = "\n\n".join(audio_elements)

    return f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0d1117; }}
      .clip {{ position: absolute; visibility: hidden; }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="{lesson_slug}"
      data-start="0"
      data-duration="{total_dur}"
      data-width="1920"
      data-height="1080"
    >
      <!-- ── Media Assets (Intro Video, Outro Video, Background Music) ── -->
      <video id="intro-video"
             data-start="0"
             data-duration="9.24"
             data-track-index="0"
             data-has-audio="true"
             data-volume="1"
             src="assets/intro.mp4"></video>

      <video id="outro-video"
             data-start="{outro_start}"
             data-duration="12.15"
             data-track-index="0"
             data-has-audio="true"
             data-volume="1"
             src="assets/outro.mp4"></video>

      <audio id="bg-music"
             data-start="0"
             data-duration="{total_dur}"
             data-track-index="30"
             data-volume="0.12"
             data-loop="true"
             src="assets/bg-music.mp3"></audio>

      <!-- ── Scene Clips ── -->
{scene_clips_str}

      <!-- ── TTS Audio Tracks (absolute root timestamps) ── -->
{audio_str}

    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["{lesson_slug}"] = tl;
    </script>
  </body>
</html>
"""


def _build_scene_html(scene: Dict[str, Any], lesson_title: str) -> str:
    """Build a Scene_XX.html sub-composition following HyperFrames GSAP rules."""
    scene_id = scene["scene_id"]
    scene_n = scene_id.replace("Scene_", "")
    scene_slug = scene_id.replace("_", "-").lower()
    scene_title_raw = scene.get("scene_title", f"Scene {scene_n}")
    dur = scene["duration"]
    html_desc = scene.get("html_structure", "intro title, content area")
    visual_desc = scene.get("visual_description", "")
    anim_steps = scene.get("animation_timeline", [])

    # Build the animation steps as JS comments for reference
    anim_comments = "\n      // ".join(anim_steps)

    # ── FIX #2: Layout type comes from Creator Agent blueprint (layout_type field)
    # Priority: blueprint field > keyword fallback (never use cứng hardcoded mapping)
    blueprint_layout = scene.get("layout_type", "").lower().strip()
    desc_lower = (visual_desc.lower() + " " + scene_title_raw.lower())

    if blueprint_layout in ["terminal_cli", "code_editor", "comparison", "process_flow", "pitfall_alert",
                             "pitfall", "flow", "comparison", "code", "terminal"]:
        # Map blueprint names to internal layout keys
        _map = {
            "terminal_cli": "terminal", "code_editor": "code",
            "process_flow": "flow", "pitfall_alert": "pitfall",
        }
        layout_type = _map.get(blueprint_layout, blueprint_layout)
    else:
        # Fallback keyword detection (safety net only)
        if any(k in desc_lower for k in ["lỗi", "cảnh báo", "pitfall", "warning", "khắc phục"]):
            layout_type = "pitfall"
        elif any(k in desc_lower for k in ["terminal", "cli", "lệnh", "command", "pip ", "python ", "activate"]):
            layout_type = "terminal"
        elif any(k in desc_lower for k in ["so sánh", "global", "isolated", "client", "server"]):
            layout_type = "comparison"
        elif any(k in desc_lower for k in ["bước", "quy trình", "flow", "sơ đồ", "luồng"]):
            layout_type = "flow"
        else:
            layout_type = "code"

    # ── FIX #2: Extract CLEAN educational text — strip ALL meta-prompt instructions
    META_PROMPT_KEYWORDS = [
        "màn hình", "hiển thị", "sử dụng font", "nền tối", "xuất hiện",
        "giao diện", "thiết kế", "biểu tượng", "gradient", "phông nền",
        "văn bản", "layout", "animation", "slide", "mockup", "background",
        "screen shows", "display", "render"
    ]
    clean_desc = visual_desc
    if any(k in visual_desc.lower() for k in META_PROMPT_KEYWORDS):
        narration_raw = scene.get("narration", "")
        sentences = [s.strip() for s in re.split(r'[.!?:]', narration_raw) if len(s.strip()) > 10]
        if len(sentences) >= 2:
            clean_desc = f"{sentences[0]}. {sentences[1]}."
        elif len(sentences) == 1:
            clean_desc = f"{sentences[0]}."
        else:
            clean_desc = scene_title_raw

    # Generate Layout-Specific HTML & GSAP Script
    html_content = ""
    gsap_js = ""

    if layout_type == "terminal":
        # ── FIX #2: Terminal CLI layout — chuẩn Black UI với prompt '$'
        # Extract narration for command lines display
        narration_lines = scene.get("narration", "")
        cmd_lines = [l.strip() for l in visual_desc.split("\n") if l.strip()]
        if not cmd_lines:
            cmd_lines = ["$ python --version", "Python 3.11.x", "$ pip --version", "pip 23.x"]

        def _fmt_cmd(line: str) -> str:
            if line.startswith("$") or line.startswith("#"):
                color = "#8b949e" if line.startswith("#") else "#e6edf3"
                return f'<div style="color:{color};font-family:\'Fira Code\',monospace;font-size:20px;line-height:1.8;">{line}</div>'
            return f'<div style="color:#3fb950;font-family:\'Fira Code\',monospace;font-size:20px;line-height:1.8;">{line}</div>'

        cmd_html = "".join(_fmt_cmd(l) for l in cmd_lines[:10])

        html_content = f"""
    <!-- Terminal CLI Layout -->
    <div class="split-container clip" id="terminal-reveal-{scene_n}" style="display:flex;gap:40px;width:1760px;margin:0 auto;align-items:center;height:900px;">
      <div id="text-card-{scene_n}" style="flex:0 0 38%;background:rgba(9,9,11,0.75);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:48px;">
        <h3 style="font-size:32px;color:#e6edf3;margin-bottom:20px;">Khái Niệm Cốt Lõi</h3>
        <p style="color:#c9d1d9;font-size:22px;line-height:1.7;">{clean_desc}</p>
      </div>
      <div id="terminal-block-{scene_n}" style="flex:1;background:#0d1117;border:1px solid rgba(255,255,255,0.12);border-radius:12px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.6);">
        <div style="background:#1c1c1e;height:38px;display:flex;align-items:center;padding:0 16px;gap:8px;border-bottom:1px solid rgba(255,255,255,0.08);">
          <span style="width:12px;height:12px;border-radius:50%;background:#f85149;"></span>
          <span style="width:12px;height:12px;border-radius:50%;background:#ffa657;"></span>
          <span style="width:12px;height:12px;border-radius:50%;background:#3fb950;"></span>
          <span style="font-family:system-ui,sans-serif;font-size:13px;color:#8b949e;margin-left:8px;">Terminal — bash</span>
        </div>
        <div style="padding:28px 32px;">{cmd_html}</div>
      </div>
    </div>"""

        t1 = 1.5
        t2 = 2.8
        t3 = round(dur * 0.55, 2)
        t4 = round(dur * 0.80, 2)
        gsap_js = f"""
      // Ẩn ban đầu
      tl.set("#text-card-{scene_n}", {{ autoAlpha: 0, x: -40 }}, 0);
      tl.set("#terminal-block-{scene_n}", {{ autoAlpha: 0, y: 30 }}, 0);

      // Intro title (0.2s -> 1.8s)
      tl.to("#intro-title-{scene_n}", {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.4)" }}, 0.2);
      tl.to("#intro-title-{scene_n}", {{ scale: 0.38, x: -760, y: -460, duration: 0.6, ease: "power3.inOut" }}, 1.8);

      // Reveal text card then terminal (dynamic timing dur={dur:.2f}s)
      tl.to("#text-card-{scene_n}", {{ autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {t1});
      tl.to("#terminal-block-{scene_n}", {{ autoAlpha: 1, y: 0, duration: 0.7, ease: "back.out(1.2)" }}, {t2});
      
      // Dynamic visual highlights during voice narration
      tl.to("#terminal-block-{scene_n}", {{ borderColor: "#38bdf8", boxShadow: "0 0 30px rgba(56,189,248,0.3)", duration: 0.6, yoyo: true, repeat: 1 }}, {t3});
      tl.to("#text-card-{scene_n}", {{ borderColor: "rgba(56,189,248,0.4)", duration: 0.6, yoyo: true, repeat: 1 }}, {t4});"""

    elif layout_type == "comparison":
        # Use clean_desc as card content — no hardcoded topic-specific text
        left_title = "❌ Phương pháp Cũ"
        right_title = "✅ Phương pháp Mới"
        narration_parts = [s.strip() for s in re.split(r'[.!?]', scene.get("narration", "")) if len(s.strip()) > 15]
        left_desc = narration_parts[0] if narration_parts else clean_desc
        right_desc = narration_parts[1] if len(narration_parts) > 1 else clean_desc

        html_content = f"""
    <!-- Comparison Layout -->
    <div class="split-container clip" id="comparison-{scene_n}">
      <div class="column-left content-card bad-card" id="left-card-{scene_n}">
        <h3>{left_title}</h3>
        <p>{left_desc}</p>
      </div>
      <div class="column-right content-card good-card" id="right-card-{scene_n}">
        <h3>{right_title}</h3>
        <p>{right_desc}</p>
      </div>
    </div>"""

        t1 = 1.5
        t2 = round(1.5 + (dur - 3.0) * 0.45, 2)
        t3 = round(dur * 0.80, 2)
        gsap_js = f"""
      // Ẩn ban đầu
      tl.set("#left-card-{scene_n}", {{ autoAlpha: 0, x: -50 }}, 0);
      tl.set("#right-card-{scene_n}", {{ autoAlpha: 0, x: 50 }}, 0);

      // Intro title (0.2s -> 1.8s)
      tl.to("#intro-title-{scene_n}", {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.4)" }}, 0.2);
      tl.to("#intro-title-{scene_n}", {{ scale: 0.38, x: -760, y: -460, duration: 0.6, ease: "power3.inOut" }}, 1.8);

      // Reveal Cards (dynamic timing based on dur={dur:.2f}s)
      tl.to("#left-card-{scene_n}", {{ autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {t1});
      tl.to("#right-card-{scene_n}", {{ autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {t2});
      tl.to("#right-card-{scene_n}", {{ scale: 1.03, boxShadow: "0 0 50px rgba(63,185,80,0.3)", duration: 0.6, yoyo: true, repeat: 1 }}, {t3});"""

    elif layout_type == "flow":
        step1 = "Bước 1: Khởi tạo venv"
        step2 = "Bước 2: Kích hoạt venv"
        step3 = "Bước 3: Cài đặt Thư viện"

        if "client" in desc_lower or "http" in desc_lower:
            step1 = "1. Gửi HTTP Request"
            step2 = "2. Xử lý tại Endpoint"
            step3 = "3. Phản hồi Response"

        html_content = f"""
    <!-- Step-by-Step Flow Layout -->
    <div class="flow-container clip" id="flow-{scene_n}">
      <div class="flow-node content-card" id="node-{scene_n}-1">
        <div class="node-num">01</div>
        <h4>{step1}</h4>
      </div>
      <div class="flow-line" id="line-{scene_n}-1"></div>
      <div class="flow-node content-card" id="node-{scene_n}-2">
        <div class="node-num">02</div>
        <h4>{step2}</h4>
      </div>
      <div class="flow-line" id="line-{scene_n}-2"></div>
      <div class="flow-node content-card" id="node-{scene_n}-3">
        <div class="node-num">03</div>
        <h4>{step3}</h4>
      </div>
    </div>"""

        r_dur = max(dur - 3.0, 5.0)
        t1 = 1.6
        t2 = round(1.6 + r_dur * 0.18, 2)
        t3 = round(1.6 + r_dur * 0.38, 2)
        t4 = round(1.6 + r_dur * 0.58, 2)
        t5 = round(1.6 + r_dur * 0.78, 2)
        gsap_js = f"""
      // Ẩn ban đầu
      tl.set("#node-{scene_n}-1", {{ autoAlpha: 0, y: 30 }}, 0);
      tl.set("#line-{scene_n}-1", {{ scaleX: 0, transformOrigin: "left center" }}, 0);
      tl.set("#node-{scene_n}-2", {{ autoAlpha: 0, y: 30 }}, 0);
      tl.set("#line-{scene_n}-2", {{ scaleX: 0, transformOrigin: "left center" }}, 0);
      tl.set("#node-{scene_n}-3", {{ autoAlpha: 0, y: 30 }}, 0);

      // Intro title (0.2s -> 1.8s)
      tl.to("#intro-title-{scene_n}", {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.4)" }}, 0.2);
      tl.to("#intro-title-{scene_n}", {{ scale: 0.38, x: -760, y: -460, duration: 0.6, ease: "power3.inOut" }}, 1.8);

      // Stagger Steps (dynamic timing based on dur={dur:.2f}s)
      tl.to("#node-{scene_n}-1", {{ autoAlpha: 1, y: 0, duration: 0.5, ease: "power2.out" }}, {t1});
      tl.to("#line-{scene_n}-1", {{ scaleX: 1, duration: 0.4, ease: "power1.inOut" }}, {t2});
      tl.to("#node-{scene_n}-2", {{ autoAlpha: 1, y: 0, duration: 0.5, ease: "power2.out" }}, {t3});
      tl.to("#line-{scene_n}-2", {{ scaleX: 1, duration: 0.4, ease: "power1.inOut" }}, {t4});
      tl.to("#node-{scene_n}-3", {{ autoAlpha: 1, y: 0, duration: 0.5, ease: "power2.out" }}, {t5});"""

    elif layout_type == "pitfall":
        # Check which lesson warning to show
        w1, w2, w3 = "Quên kích hoạt Virtual Environment trước khi cài thư viện", "Đóng gói thiếu file requirements.txt làm sai lệch môi trường", "Nhầm lẫn cú pháp chạy script kích hoạt trên các HĐH khác nhau"
        gp = "Luôn kiểm tra tiền tố <code>(venv)</code> trên terminal và tự động hóa lưu dependency qua lệnh <code>pip freeze &gt; requirements.txt</code>."
        
        if "fastapi" in desc_lower or "khởi tạo" in desc_lower or "uvicorn" in desc_lower:
            w1 = "Quên cài đặt hoặc không khởi chạy Uvicorn khiến Server offline"
            w2 = "Sai lệch phương thức HTTP (Ví dụ: Khai báo POST nhưng gọi GET)"
            w3 = "Cấu hình sai cổng Port hoặc Host IP dẫn tới lỗi kết nối mạng"
            gp = "Luôn khởi chạy server qua <code>uvicorn main:app --reload</code>, kiểm tra chính xác method trong code và IP/cổng mặc định <code>8000</code>."

        html_content = f"""
    <!-- Pitfalls / Warnings Alert Layout -->
    <div class="pitfall-container clip" id="pitfall-box-{scene_n}">
      <div class="warning-card content-card" id="warning-card-{scene_n}">
        <div class="red-text">⚠️ LỖI PHỔ BIẾN CẦN TRÁNH (PITFALLS)</div>
        <ul class="bullet-list">
          <li>{w1}</li>
          <li>{w2}</li>
          <li>{w3}</li>
        </ul>
      </div>
      <div class="success-card content-card" id="success-card-{scene_n}">
        <div class="green-text">✅ GIẢI PHÁP KHẮC PHỤC (BEST PRACTICE)</div>
        <p>{gp}</p>
      </div>
    </div>"""

        t1 = 1.5
        t2 = round(1.5 + (dur - 3.0) * 0.45, 2)
        t3 = round(dur * 0.80, 2)
        gsap_js = f"""
      // Ẩn ban đầu
      tl.set("#warning-card-{scene_n}", {{ autoAlpha: 0, scale: 0.95 }}, 0);
      tl.set("#success-card-{scene_n}", {{ autoAlpha: 0, y: 30 }}, 0);

      // Intro title (0.2s -> 1.8s)
      tl.to("#intro-title-{scene_n}", {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.4)" }}, 0.2);
      tl.to("#intro-title-{scene_n}", {{ scale: 0.38, x: -760, y: -460, duration: 0.6, ease: "power3.inOut" }}, 1.8);

      // Reveal Pitfalls (dynamic timing based on dur={dur:.2f}s)
      tl.to("#warning-card-{scene_n}", {{ autoAlpha: 1, scale: 1, duration: 0.6, ease: "power3.out" }}, {t1});
      tl.to("#success-card-{scene_n}", {{ autoAlpha: 1, y: 0, duration: 0.6, ease: "back.out(1.2)" }}, {t2});
      tl.to("#success-card-{scene_n}", {{ scale: 1.02, boxShadow: "0 0 40px rgba(63,185,80,0.3)", duration: 0.5, yoyo: true, repeat: 1 }}, {t3});"""

    else:  # layout_type == "code"
        # Determine code & language dynamically based on context
        code_lang = "python"
        if "requirements" in desc_lower or "freeze" in desc_lower:
            code_lang = "bash"
            code_html = (
                '<span class="comment"># 1. Lưu danh sách thư viện hiện tại</span>\n'
                '<span class="keyword">pip</span> freeze > requirements.txt\n\n'
                '<span class="comment"># 2. Cài đặt lại trên máy mới</span>\n'
                '<span class="keyword">pip</span> install -r requirements.txt'
            )
        elif "venv" in desc_lower or "environment" in desc_lower or "môi trường" in desc_lower or "kích hoạt" in desc_lower:
            code_lang = "bash"
            code_html = (
                '<span class="comment"># 1. Tạo môi trường ảo venv</span>\n'
                '<span class="keyword">python</span> -m venv venv\n\n'
                '<span class="comment"># 2. Kích hoạt môi trường (Windows)</span>\n'
                'venv\\Scripts\\activate\n\n'
                '<span class="comment"># 3. Kích hoạt môi trường (macOS/Linux)</span>\n'
                '<span class="keyword">source</span> venv/bin/activate'
            )
        elif "interpreter" in desc_lower or "vs code" in desc_lower or "cấu hình" in desc_lower:
            code_lang = "python"
            code_html = (
                '<span class="keyword">import</span> sys\n\n'
                '<span class="comment"># Kiểm tra đường dẫn Python Interpreter thực thi</span>\n'
                '<span class="function">print</span>(<span class="string">"Python Path:"</span>, sys.executable)\n'
                '<span class="function">print</span>(<span class="string">"Python Version:"</span>, sys.version)'
            )
        elif "khai báo" in desc_lower or "biến" in desc_lower:
            code_lang = "python"
            code_html = (
                '<span class="comment"># Khai báo biến cơ bản trong Python</span>\n'
                'course_name = <span class="string">"Python Core AI"</span>\n'
                'lesson_number = <span class="variable">2</span>\n'
                'is_active = <span class="keyword">True</span>\n\n'
                '<span class="function">print</span>(<span class="string">f"Bài học: {course_name} - Bài {lesson_number}"</span>)'
            )
        else:
            code_lang = "bash"
            code_html = (
                '<span class="comment"># Kiểm tra phiên bản Python</span>\n'
                '<span class="keyword">python</span> --version\n'
                '<span class="keyword">pip</span> --version'
            )

        filename_display = "main.py" if code_lang == "python" else "install.sh"
        line_count = len(code_html.split('\n'))
        line_numbers_html = '<br/>'.join(str(i) for i in range(1, line_count + 1))

        html_content = f"""
    <!-- Code Reveal Layout (VS Code Theme) -->
    <div class="split-container clip" id="code-reveal-{scene_n}">
      <div class="column-left content-card" id="text-card-{scene_n}" style="flex: 0 0 40%; display: flex; flex-direction: column; justify-content: center;">
        <h3 style="font-size: 32px; color: var(--text-primary); margin-bottom: 20px;">Khái Niệm Cốt Lõi</h3>
        <p style="color: var(--text-secondary); font-size: 24px; line-height: 1.6;">{clean_desc}</p>
      </div>
      <!-- VS Code Window Block -->
      <div id="code-block-{scene_n}" class="code-card" style="flex: 0 0 56%; max-height: 620px; display: flex; flex-direction: column; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
        <!-- Titlebar -->
        <div class="code-header" style="background: #323233; height: 38px; padding: 0 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(0,0,0,0.2);">
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="dot red" style="width:12px; height:12px; border-radius:50%; background:#f85149;"></span>
            <span class="dot yellow" style="width:12px; height:12px; border-radius:50%; background:#ffa657;"></span>
            <span class="dot green" style="width:12px; height:12px; border-radius:50%; background:#3fb950;"></span>
          </div>
          <div style="font-family: system-ui, sans-serif; font-size: 13px; color: #cccccc; font-weight: 500;">Visual Studio Code — {filename_display}</div>
          <div class="code-lang" style="font-family: 'Fira Code', monospace; font-size: 12px; color: #858585; text-transform: uppercase;">{code_lang}</div>
        </div>
        
        <!-- Editor Body -->
        <div style="display: flex; flex: 1; overflow: hidden; background: #1e1e1e;">
          <!-- 1. Activity Bar -->
          <div style="width: 48px; background: #333333; display: flex; flex-direction: column; align-items: center; padding-top: 12px; gap: 18px; border-right: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 18px; color: #ffffff; border-left: 2px solid #007acc; padding-left: 8px; width: 100%;">📁</div>
            <div style="font-size: 18px; color: #858585; opacity: 0.6;">🔍</div>
            <div style="font-size: 18px; color: #858585; opacity: 0.6;">🌿</div>
            <div style="font-size: 18px; color: #858585; opacity: 0.6;">🐞</div>
            <div style="font-size: 18px; color: #858585; opacity: 0.6;">⚙️</div>
          </div>
          
          <!-- 2. Sidebar Explorer -->
          <div style="width: 150px; background: #252526; border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; font-size: 13px; color: #cccccc; padding: 12px 10px;">
            <div style="font-weight: 700; text-transform: uppercase; font-size: 11px; margin-bottom: 12px; color: #858585; letter-spacing: 0.8px;">Explorer</div>
            <div style="font-weight: 600; color: #ffffff; margin-bottom: 8px; display: flex; align-items: center; gap: 4px;">📂 PROJECT</div>
            <div style="margin-left: 12px; margin-bottom: 6px; color: #007acc; font-weight: 600; display: flex; align-items: center; gap: 6px;">🐍 {filename_display}</div>
            <div style="margin-left: 12px; margin-bottom: 6px; color: #757575;">📄 config.json</div>
            <div style="margin-left: 12px; margin-bottom: 6px; color: #757575;">📄 README.md</div>
          </div>
          
          <!-- 3. Main Workspace -->
          <div style="flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #1e1e1e;">
            <!-- Tab Bar -->
            <div style="height: 36px; background: #2d2d2d; display: flex; align-items: center;">
              <div style="background: #1e1e1e; color: #ffffff; padding: 0 16px; height: 100%; display: flex; align-items: center; gap: 8px; border-top: 2px solid #007acc; font-size: 13px; font-weight: 500;">
                <span>🐍 {filename_display}</span>
                <span style="opacity: 0.5; font-size: 11px;">✕</span>
              </div>
              <div style="color: #858585; padding: 0 16px; height: 100%; display: flex; align-items: center; gap: 8px; font-size: 13px;">
                <span>📄 config.json</span>
              </div>
            </div>
            
            <!-- Code content with Line Numbers -->
            <div style="display: flex; flex: 1; overflow-y: auto;">
              <div style="width: 44px; padding: 20px 8px 20px 0; text-align: right; color: #858585; font-family: 'Fira Code', monospace; font-size: 18px; line-height: 1.7; select-none: none; background: #1e1e1e; border-right: 1px solid rgba(255,255,255,0.05);">
                {line_numbers_html}
              </div>
              <pre class="code-content" style="padding: 20px 24px; margin: 0; background: #1e1e1e; flex: 1; font-size: 18px; line-height: 1.7;"><code id="code-content-{scene_n}">{code_html}</code></pre>
            </div>
          </div>
        </div>
        
        <!-- Status Bar -->
        <div style="height: 24px; background: #007acc; color: #ffffff; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; font-size: 12px; font-family: system-ui, sans-serif;">
          <div style="display: flex; gap: 16px;">
            <span>🟢 main*</span>
            <span>⚡ Python 3.11</span>
          </div>
          <div style="display: flex; gap: 16px;">
            <span>Ln 1, Col 1</span>
            <span>UTF-8</span>
          </div>
        </div>
      </div>
    </div>"""

        t1 = 1.5
        t2 = round(1.5 + (dur - 3.0) * 0.35, 2)
        t3 = round(dur * 0.75, 2)
        gsap_js = f"""
      // Ẩn ban đầu
      tl.set("#text-card-{scene_n}", {{ autoAlpha: 0, x: -50 }}, 0);
      tl.set("#code-block-{scene_n}", {{ autoAlpha: 0, x: 50 }}, 0);

      // Intro title (0.2s -> 1.8s)
      tl.to("#intro-title-{scene_n}", {{ autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.4)" }}, 0.2);
      tl.to("#intro-title-{scene_n}", {{ scale: 0.38, x: -760, y: -460, duration: 0.6, ease: "power3.inOut" }}, 1.8);

      // Reveal text and code (dynamic timing based on dur={dur:.2f}s)
      tl.to("#text-card-{scene_n}", {{ autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {t1});
      tl.to("#code-block-{scene_n}", {{ autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {t2});
      tl.to("#code-block-{scene_n}", {{ borderColor: "#38bdf8", boxShadow: "0 0 40px rgba(56,189,248,0.4)", duration: 0.5, yoyo: true, repeat: 1 }}, {t3});"""

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{scene_id} — {scene_title_raw}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>
    /* ── Reset ─────────────────────────────────────────── */
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      width: 1920px; height: 1080px; overflow: hidden;
      background-color: #0f1117;
      background-image: radial-gradient(rgba(255,255,255,0.25) 1.5px, transparent 1.5px);
      background-size: 32px 32px;
      font-family: 'Inter', sans-serif;
    }}
    body::before {{
      content: ''; position: absolute; border-radius: 50%; filter: blur(150px); z-index: -1;
      top: -200px; left: -200px; width: 800px; height: 800px;
      background: rgba(56,189,248,0.15);
    }}
    body::after {{
      content: ''; position: absolute; border-radius: 50%; filter: blur(150px); z-index: -1;
      bottom: -200px; right: -200px; width: 600px; height: 600px;
      background: rgba(168,85,247,0.15);
    }}

    /* ── Scene wrapper ─────────────────────────────────── */
    #scene-{scene_n} {{ width: 1920px; height: 1080px; position: relative; }}

    /* ── Design tokens ─────────────────────────────────── */
    :root {{
      --keyword:  #ff7b72;
      --string:   #a5d6ff;
      --variable: #79c0ff;
      --operator: #d2a8ff;
      --function: #d2a8ff;
      --comment:  #8b949e;
      --good:     #3fb950;
      --bad:      #f85149;
      --accent:   #ffa657;
      --text-primary:   #e6edf3;
      --text-secondary: #c9d1d9;
      --text-muted:     #8b949e;
    }}

    /* ── Intro title ───────────────────────────────────── */
    #intro-title-{scene_n} {{
      position: absolute; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-size: 72px; font-weight: 700;
      color: var(--text-primary); text-align: center;
      white-space: nowrap; z-index: 100; pointer-events: none;
    }}
    #intro-title-{scene_n} span {{
      background: linear-gradient(135deg, #38bdf8, #a855f7);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}

    /* ── Content card ──────────────────────────────────── */
    .content-card {{
      position: absolute;
      background: rgba(9,9,11,0.7);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 20px;
      backdrop-filter: blur(16px);
      padding: 40px;
    }}

    /* ── Code card ─────────────────────────────────────── */
    .code-card {{
      background: #0d1117;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px;
      overflow: hidden;
    }}
    .code-header {{
      background: #161b22;
      padding: 12px 20px;
      display: flex; align-items: center; gap: 8px;
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .dot.red    {{ background: #f85149; }}
    .dot.yellow {{ background: #ffa657; }}
    .dot.green  {{ background: #3fb950; }}
    .code-lang {{
      margin-left: auto;
      font-family: 'Fira Code', monospace;
      font-size: 12px; color: var(--text-muted);
    }}
    .code-content {{
      font-family: 'Fira Code', monospace;
      font-size: 22px; line-height: 1.7;
      color: var(--text-primary);
      padding: 28px 32px;
      overflow-x: auto;
    }}
    .keyword  {{ color: var(--keyword); }}
    .string   {{ color: var(--string); }}
    .variable {{ color: var(--variable); }}
    .function {{ color: var(--function); }}
    .comment  {{ color: var(--comment); font-style: italic; }}

    /* ── Section badge ─────────────────────────────────── */
    .section-badge {{
      position: absolute;
      top: 60px; right: 80px;
      font-size: 14px; font-weight: 600; color: var(--text-muted);
      letter-spacing: 2px; text-transform: uppercase;
    }}

    /* ── Layout Styles ─────────────────────────────────── */
    .split-container {{
      position: absolute;
      top: 220px; left: 100px; width: 1720px; height: 720px;
      display: flex; gap: 60px; align-items: stretch;
    }}
    .column-left, .column-right {{
      flex: 1;
      display: flex; flex-direction: column; justify-content: center;
    }}
    .bad-card {{
      border: 1px solid rgba(248, 81, 73, 0.3) !important;
      background: rgba(248, 81, 73, 0.03) !important;
      box-shadow: 0 0 40px rgba(248, 81, 73, 0.08);
    }}
    .bad-card h3 {{
      color: var(--bad); font-size: 32px; margin-bottom: 20px;
    }}
    .bad-card p {{
      color: var(--text-secondary); font-size: 24px; line-height: 1.6;
    }}
    .good-card {{
      border: 1px solid rgba(63, 185, 80, 0.3) !important;
      background: rgba(63, 185, 80, 0.03) !important;
      box-shadow: 0 0 40px rgba(63, 185, 80, 0.08);
    }}
    .good-card h3 {{
      color: var(--good); font-size: 32px; margin-bottom: 20px;
    }}
    .good-card p {{
      color: var(--text-secondary); font-size: 24px; line-height: 1.6;
    }}
    
    /* Flow Layout */
    .flow-container {{
      position: absolute;
      top: 350px; left: 100px; width: 1720px;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .flow-node {{
      position: relative;
      flex: 0 0 480px; height: 280px;
      padding: 30px; display: flex; flex-direction: column; justify-content: center;
      text-align: center;
    }}
    .node-num {{
      position: absolute; top: -30px; left: 50%; transform: translateX(-50%);
      width: 60px; height: 60px; border-radius: 50%;
      background: linear-gradient(135deg, #38bdf8, #a855f7);
      display: flex; align-items: center; justify-content: center;
      font-size: 24px; font-weight: 700; color: white;
      box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }}
    .flow-node h4 {{
      font-size: 28px; color: var(--text-primary); margin-top: 15px; line-height: 1.4;
    }}
    .flow-line {{
      flex: 1; height: 4px;
      background: linear-gradient(90deg, #38bdf8, #a855f7);
      border-radius: 2px; margin: 0 20px;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }}
    
    /* Pitfall Layout */
    .pitfall-container {{
      position: absolute;
      top: 220px; left: 150px; width: 1620px; height: 720px;
      display: flex; flex-direction: column; gap: 40px;
    }}
    .warning-card {{
      border: 1px solid rgba(248, 81, 73, 0.3) !important;
      background: rgba(248, 81, 73, 0.03) !important;
      box-shadow: 0 0 40px rgba(248, 81, 73, 0.08);
      padding: 35px;
    }}
    .success-card {{
      border: 1px solid rgba(63, 185, 80, 0.3) !important;
      background: rgba(63, 185, 80, 0.03) !important;
      box-shadow: 0 0 40px rgba(63, 185, 80, 0.08);
      padding: 35px;
    }}
    .red-text {{ color: var(--bad); font-size: 28px; font-weight: 700; margin-bottom: 20px; }}
    .green-text {{ color: var(--good); font-size: 28px; font-weight: 700; margin-bottom: 20px; }}
    .bullet-list {{
      list-style-type: none; margin-left: 20px;
    }}
    .bullet-list li {{
      font-size: 22px; color: var(--text-secondary); line-height: 1.8;
      position: relative; margin-bottom: 12px; padding-left: 30px;
    }}
    .bullet-list li::before {{
      content: '❌'; position: absolute; left: 0; top: 0; font-size: 18px;
    }}
    .success-card p {{
      font-size: 24px; color: var(--text-secondary); line-height: 1.6;
    }}
    .success-card code {{
      font-family: 'Fira Code', monospace;
      background: #161b22; padding: 4px 8px; border-radius: 6px;
      color: var(--variable); font-size: 20px;
    }}
  </style>
</head>
<body>
  <!-- ═══ {scene_id}: {scene_title_raw} ═══ -->
  <!--  Visual: {visual_desc}  -->
  <!--  HTML Structure: {html_desc}  -->
  <div id="scene-{scene_n}" class="clip" data-composition-id="scene-{scene_n}" data-start="0" data-duration="{dur}" data-track-index="0">

    <!-- Section badge -->
    <div class="section-badge clip" data-start="0" data-duration="{dur}" data-track-index="1">
      {lesson_title}
    </div>

    <!-- Intro title (xuất hiện 0.2s, kết thúc/lên góc lúc 3.2s) -->
    <div id="intro-title-{scene_n}" class="clip" data-start="0" data-duration="{dur}" data-track-index="10">
      <span>{scene_title_raw}</span>
    </div>

    <!-- ── MAIN CONTENT (bắt đầu từ 4.0s+) ── -->
    {html_content}

  </div><!-- /#scene-{scene_n} -->

  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["{scene_slug}"] = tl;

    const _build{scene_n} = setInterval(function() {{
      const root = document.getElementById("scene-{scene_n}");
      if (!root) return;
      clearInterval(_build{scene_n});

      // ── TIMELINE PLAN (from blueprint animation_timeline) ──────────────
      // {anim_comments}
      // ──────────────────────────────────────────────────────────────────

      // BƯỚC 1 (BẮT BUỘC ĐẦU TIÊN): Set toàn bộ .clip visible
      tl.set(".clip", {{ autoAlpha: 1 }}, 0);

      // BƯỚC 2: Ẩn các elements theo trạng thái ban đầu
      tl.set("#intro-title-{scene_n}", {{ autoAlpha: 0, scale: 0.8 }}, 0);
      {gsap_js}

      // KHÓA CUỐI TIMELINE (bắt buộc)
      tl.set({{}}, {{}}, {dur});
    }}, 50);
  </script>
</body>
</html>
"""


# ── UI Component Renderer Integration ─────────────────────────────────────────
# The old _build_scene_html with ~650 lines of inline HTML has been replaced.
# All layout logic is now inside UIComponentRenderer + component templates.

def _build_scene_html(scene: Dict[str, Any], lesson_title: str) -> str:
    """
    Render a scene HTML file by delegating to UIComponentRenderer.
    Reads the layout_type from the scene blueprint and renders the
    matching component template (ide/vscode.html, ide/terminal.html,
    cards/comparison.html, cards/warning_card.html, cards/process_flow.html).
    """
    from agents.ui_component_renderer import UIComponentRenderer
    renderer = UIComponentRenderer()
    return renderer.render(scene, lesson_title)





def _build_meta_json(lesson_slug: str, lesson_title: str) -> str:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return json.dumps({
        "id": lesson_slug,
        "name": lesson_title,
        "createdAt": now
    }, indent=2, ensure_ascii=False)


def _build_package_json(lesson_slug: str) -> str:
    return json.dumps({
        "name": lesson_slug,
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "npx --yes hyperframes@0.6.63 preview",
            "check": "npx --yes hyperframes@0.6.63 lint && npx --yes hyperframes@0.6.63 validate && npx --yes hyperframes@0.6.63 inspect",
            "render": "npx --yes hyperframes@0.6.63 render",
            "publish": "npx --yes hyperframes@0.6.63 publish"
        }
    }, indent=2, ensure_ascii=False)


def _build_durations_json(blueprint: Dict[str, Any]) -> str:
    """Build durations.json — placeholder until real TTS is generated."""
    durations = {}
    for scene in blueprint.get("scenes", []):
        scene_id = scene["scene_id"]
        durations[scene_id] = scene.get("duration", 30.0)
    return json.dumps(durations, indent=2, ensure_ascii=False)


# ── Main Agent ──────────────────────────────────────────────────────────────

def _to_long_path(path: Path) -> Path:
    abs_path = os.path.abspath(str(path))
    if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
        abs_path = '\\\\?\\' + abs_path
    return Path(abs_path)

def hyperframes_writer_agent(state: AgentState) -> AgentState:
    """
    HyperFrames Composition Writer Agent:
    Reads the approved video_script_json (Production Blueprint) and writes
    all HyperFrames project files to disk:
      - {output_dir}/index.html
      - {output_dir}/src/compositions/Scene_XX.html
      - {output_dir}/meta.json
      - {output_dir}/package.json
      - {output_dir}/assets/tts/durations.json
    """
    from agents.creator_agents import get_lesson_dir

    blueprint = state.get("video_script_json", {})
    if not blueprint or "scenes" not in blueprint:
        print("\n[HyperFrames_Writer] SKIPPED — No approved blueprint in state.")
        state["hyperframes_project_path"] = None
        return state

    lesson_slug = blueprint.get("lesson_slug", "lesson-video")
    lesson_title = blueprint.get("lesson_title", "Bài học")
    scenes = blueprint.get("scenes", [])

    print(f"\n[HyperFrames_Writer] Writing HyperFrames project for '{lesson_title}' ({len(scenes)} scenes)...")

    # Resolve output directory: {lesson_dir}/Video/{lesson_slug}/
    try:
        lesson_dir = get_lesson_dir(state)
    except Exception as e:
        print(f"  [HyperFrames_Writer Warning] Could not resolve lesson_dir: {e}. Using fallback.")
        lesson_dir = Path(__file__).resolve().parent.parent / "output" / "lessons" / lesson_slug

    video_base_dir = _to_long_path(lesson_dir / "Video")
    if video_base_dir.exists():
        import shutil
        for child in video_base_dir.iterdir():
            if child.is_dir() and child.name != lesson_slug:
                print(f"  [HyperFrames_Writer Clean] Removing redundant video directory: {child.name}")
                try:
                    shutil.rmtree(child, ignore_errors=True)
                except Exception as ce:
                    print(f"  [HyperFrames_Writer Clean Error] Could not remove {child.name}: {ce}")

    video_dir = _to_long_path(lesson_dir / "Video" / lesson_slug)
    compositions_dir = _to_long_path(video_dir / "src" / "compositions")
    assets_tts_dir = _to_long_path(video_dir / "assets" / "tts")

    # Create directories
    compositions_dir.mkdir(parents=True, exist_ok=True)
    assets_tts_dir.mkdir(parents=True, exist_ok=True)

    # Write root index.html
    index_html = _build_root_index_html(blueprint, lesson_slug)
    (video_dir / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  [HyperFrames_Writer] Written: index.html ({len(index_html)} chars)")

    # Write Scene sub-compositions
    for scene in scenes:
        scene_id = scene["scene_id"]
        scene_html = _build_scene_html(scene, lesson_title)
        scene_path = compositions_dir / f"{scene_id}.html"
        scene_path.write_text(scene_html, encoding="utf-8")
        print(f"  [HyperFrames_Writer] Written: src/compositions/{scene_id}.html ({len(scene_html)} chars)")

    # Write meta.json
    meta = _build_meta_json(lesson_slug, lesson_title)
    (video_dir / "meta.json").write_text(meta, encoding="utf-8")

    # Write package.json
    pkg = _build_package_json(lesson_slug)
    (video_dir / "package.json").write_text(pkg, encoding="utf-8")

    # Write durations.json (placeholder — actual values from TTS step)
    durs = _build_durations_json(blueprint)
    (assets_tts_dir / "durations.json").write_text(durs, encoding="utf-8")
    print(f"  [HyperFrames_Writer] Written: assets/tts/durations.json")

    # Write TTS scripts as text files for reference (actual TTS generation is separate)
    tts_scripts = blueprint.get("tts_scripts", {})
    for scene_id, narration in tts_scripts.items():
        scene_num = scene_id.replace("Scene_", "").zfill(2)
        script_path = assets_tts_dir / f"scene_{scene_num}_script.txt"
        script_path.write_text(narration, encoding="utf-8")

    project_path = str(video_dir.resolve())
    state["hyperframes_project_path"] = project_path
    state["artifacts_status"] = state.get("artifacts_status", {})
    state["artifacts_status"]["video_project"] = "SCAFFOLDED"

    print(f"  [HyperFrames_Writer] Project scaffolded at: {project_path}")
    print(f"  [HyperFrames_Writer] Next steps:")
    print(f"    1. Generate TTS audio: assets/tts/scene_XX.mp3")
    print(f"    2. Run: cd '{project_path}' && npm run check")
    print(f"    3. Run: npm run render")
    return state
