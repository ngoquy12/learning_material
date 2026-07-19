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
    total_dur = blueprint["total_duration"]

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
            f'             src="assets/tts/scene_{scene_num}.mp3"></audio>'
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
    scene_title_raw = scene.get("scene_title", f"Scene {scene_n}")
    dur = scene["duration"]
    html_desc = scene.get("html_structure", "intro title, content area")
    visual_desc = scene.get("visual_description", "")
    anim_steps = scene.get("animation_timeline", [])

    # Build the animation steps as JS comments for reference
    anim_comments = "\n      // ".join(anim_steps)

    # Determine if there's a code block needed
    needs_code = any(kw in visual_desc.lower() for kw in ["code", "syntax", "function", "class", "terminal"])

    code_section = ""
    if needs_code:
        code_section = f"""
    <!-- Code block -->
    <div id="code-block-{scene_n}" class="clip code-card" data-start="0" data-duration="{dur}" data-track-index="2">
      <div class="code-header">
        <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
        <span class="code-lang">python</span>
      </div>
      <pre class="code-content"><code id="code-content-{scene_n}"><span class="keyword">def</span> <span class="function">example</span>():
    <span class="string">"Nội dung sẽ được render theo visual_description"</span>
    <span class="keyword">pass</span></code></pre>
    </div>"""

    # Pre-compute optional JS for code block reveal (avoids complex expressions in f-string)
    if needs_code:
        code_reveal_js = f"tl.to('#code-block-{scene_n}', {{ autoAlpha: 1, x: 0, duration: 0.6, ease: \"power3.out\" }}, 5.5);"
    else:
        code_reveal_js = "// No code block in this scene"

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
      position: absolute;
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
  </style>
</head>
<body>
  <!-- ═══ {scene_id}: {scene_title_raw} ═══ -->
  <!--  Visual: {visual_desc}  -->
  <!--  HTML Structure: {html_desc}  -->
  <div id="scene-{scene_n}" class="clip" data-start="0" data-duration="{dur}" data-track-index="0">

    <!-- Section badge -->
    <div class="section-badge clip" data-start="0" data-duration="{dur}" data-track-index="1">
      {lesson_title}
    </div>

    <!-- Intro title (xuất hiện 0.2s, kết thúc/lên góc lúc 3.2s) -->
    <div id="intro-title-{scene_n}" class="clip" data-start="0" data-duration="{dur}" data-track-index="10">
      <span>{scene_title_raw}</span>
    </div>

    <!-- ── MAIN CONTENT (bắt đầu từ 4.0s+) ── -->
    <div id="main-content-{scene_n}" class="clip content-card"
         data-start="0" data-duration="{dur}" data-track-index="3"
         style="left: 200px; top: 180px; width: 1520px; min-height: 400px;">
      <p style="color: var(--text-secondary); font-size: 28px; line-height: 1.7;">
        <!-- Nội dung sẽ được render theo visual_description -->
        {visual_desc}
      </p>
    </div>
{code_section}

  </div><!-- /#scene-{scene_n} -->

  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["{scene_id.lower()}"] = tl;

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
      tl.set("#main-content-{scene_n}", {{ autoAlpha: 0, y: 40 }}, 0);
      {"tl.set('#code-block-" + scene_n + "', { autoAlpha: 0, x: 60 }, 0);" if needs_code else ""}

      // PHASE 1: Intro title (0.2s → 3.2s)
      tl.to("#intro-title-{scene_n}", {{
        autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)"
      }}, 0.2);
      tl.to("#intro-title-{scene_n}", {{
        scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut"
      }}, 3.2);

      // PHASE 2: Nội dung chính (từ 4.2s — KHÔNG BAO GIỜ trước 4.0s)
      tl.to("#main-content-{scene_n}", {{
        autoAlpha: 1, y: 0, duration: 0.7, ease: "power3.out"
      }}, 4.2);

      {code_reveal_js}

      // KHÓA CUỐI TIMELINE (bắt buộc)
      tl.set({{}}, {{}}, {dur});
    }}, 50);
  </script>
</body>
</html>
"""


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
        scene_num = f"scene_{scene_id.replace('Scene_', '').zfill(2)}"
        durations[scene_num] = scene.get("duration", 30.0)
    return json.dumps(durations, indent=2, ensure_ascii=False)


# ── Main Agent ──────────────────────────────────────────────────────────────

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

    video_dir = lesson_dir / "Video" / lesson_slug
    compositions_dir = video_dir / "src" / "compositions"
    assets_tts_dir = video_dir / "assets" / "tts"

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
