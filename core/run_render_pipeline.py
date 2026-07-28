"""
core/run_render_pipeline.py

1-Click Automated E-learning Video Production Pipeline:
Connects all 6 stages into a seamless automated runner:
  Stage 1: Input & SSOT (reading.md / lesson_details)
  Stage 2: video_script_agent (5-Tier Pedagogy + 6 Professional Features)
  Stage 3: video_script_reviewer_agent (14-Point Quality Audit & Retry)
  Stage 4: hyperframes_writer_agent & gen_tts.py (Director Cues & Kokoro Audio Engine)
  Stage 5: Sub-compositions Scaffolding (Hero Welcome Banner & Outro Banner)
  Stage 6: HyperFrames CLI Batch Render (MP4 1080p60 Output)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.creator_agents import video_script_agent
from agents.reviewer_agents import video_script_reviewer_agent
from agents.hyperframes_writer_agent import hyperframes_writer_agent


def run_render_pipeline(state: Dict[str, Any], max_retries: int = 3, execute_render: bool = False) -> Dict[str, Any]:
    """
    Executes the full 1-Click Video Generation & Render Pipeline.
    
    Args:
        state: AgentState dict containing session_id, lesson_id, technology_stack, core_ssot.
        max_retries: Max retry attempts if reviewer rejects blueprint.
        execute_render: If True, invokes HyperFrames CLI render command.
        
    Returns:
        Updated AgentState with project path and status.
    """
    print("=" * 80)
    print("🚀 [1-CLICK VIDEO PIPELINE] Starting E-learning Video Generation & Render Flow")
    print("=" * 80)

    # ── STAGE 1 & 2: Script Generation ───────────────────────────────────────
    attempts = 0
    approved = False
    
    while attempts < max_retries and not approved:
        attempts += 1
        print(f"\n🎬 [STAGE 2] Script Generation (Attempt {attempts}/{max_retries})...")
        state = video_script_agent(state)
        
        # ── STAGE 3: Reviewer Quality Check ─────────────────────────────────
        print(f"🔍 [STAGE 3] Reviewer Quality Audit...")
        review_result = video_script_reviewer_agent(state)
        
        if review_result.get("status") == "APPROVED":
            approved = True
            print("  ✓ Blueprint APPROVED by Reviewer!")
        else:
            feedback = review_result.get("feedback", "Kịch bản chưa đạt chuẩn.")
            print(f"  ❌ Reviewer REJECTED: {feedback}")
            state["reviewer_feedback"] = feedback

    if not approved:
        print("  ⚠️ Warning: Reviewer did not approve after max attempts. Proceeding with current blueprint.")

    # ── STAGE 4 Audio: Sinh âm thanh Voiceover TTS & Đo thời lượng thực tế (VOICE-FIRST) ──
    print("\n🎙️ [STAGE 4 Voice-First] Sinh giọng đọc TTS Audio & Đo thời lượng khớp khung hình...")
    from agents.hyperframes_writer_agent import _build_gen_tts_py_script, extract_director_cues
    from agents.creator_agents import get_lesson_dir
    import subprocess
    
    blueprint = state.get("video_script_json", {})
    scenes = blueprint.get("scenes", [])
    lesson_slug = blueprint.get("lesson_slug", "session_01_lesson_01")
    
    try:
        lesson_dir = get_lesson_dir(state)
    except Exception:
        course = state.get("course_dir_name", "PM_Python")
        session = state.get("session_id", "Session 06")
        lesson = state.get("lesson_id", "Lesson 01")
        lesson_dir = Path("output") / course / session / lesson

    video_dir = lesson_dir / "Video" / lesson_slug
    assets_tts_dir = video_dir / "assets" / "tts"
    assets_tts_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Ghi tệp kịch bản thoại sạch & director_cues.json
    director_cues_all = {}
    for scene in scenes:
        sc_id = scene["scene_id"]
        narration = scene.get("narration", "")
        clean_text, cues = extract_director_cues(narration)
        (assets_tts_dir / f"{sc_id}_script.txt").write_text(clean_text, encoding="utf-8")
        if cues:
            director_cues_all[sc_id] = cues

    (assets_tts_dir / "director_cues.json").write_text(json.dumps(director_cues_all, indent=2, ensure_ascii=False), encoding="utf-8")
    
    # 2. Ghi và thực thi gen_tts.py
    gen_tts_code = _build_gen_tts_py_script(blueprint, lesson_slug)
    (video_dir / "gen_tts.py").write_text(gen_tts_code, encoding="utf-8")
    
    try:
        res = subprocess.run([sys.executable, "gen_tts.py"], cwd=str(video_dir), capture_output=True, text=True, check=False)
        if res.returncode == 0:
            print("  ✓ TTS Audio generated & durations.json updated!")
        else:
            print(f"  ⚠️ gen_tts.py note: {res.stdout[:150] or res.stderr[:150]}")
    except Exception as te:
        print(f"  ⚠️ TTS execution warning: {te}")

    # 3. Nạp lại durations.json nếu có để cập nhật thời lượng chính xác cho từng scene
    durations_json_path = assets_tts_dir / "durations.json"
    if durations_json_path.exists():
        try:
            dur_map = json.loads(durations_json_path.read_text(encoding="utf-8"))
            cumulative = 0.0
            for sc in scenes:
                sc_id = sc["scene_id"]
                if sc_id in dur_map:
                    sc["duration"] = dur_map[sc_id]
                sc["start_at_root"] = round(cumulative, 2)
                cumulative += sc.get("duration", 25.0)
            blueprint["total_duration"] = round(cumulative, 2)
            state["video_script_json"] = blueprint
            print(f"  ✓ Đã cập nhật khớp thời lượng thoại Voiceover với GSAP Timeline ({len(dur_map)} scenes)!")
        except Exception as de:
            print(f"  ⚠️ Could not parse durations.json: {de}")

    # ── STAGE 5: Dựng giao diện GSAP HTML Sub-Compositions dựa trên thời lượng Voice chính xác ──
    print("\n💻 [STAGE 5 GSAP UI] Dựng HyperFrames Project Files & Sub-Compositions theo khớp voice...")
    state = hyperframes_writer_agent(state)
    
    project_path = state.get("hyperframes_project_path")
    if not project_path or not os.path.exists(project_path):
        print("❌ Pipeline Failed: Project path not generated.")
        state["pipeline_status"] = "FAILED"
        return state

    print(f"  ✓ Project Scaffolded successfully at: {project_path}")

    # ── STAGE 5.5: Video QA Reviewer Agent ──────────────────────────────────────
    print("\n🔍 [STAGE 5.5] Khởi chạy Video QA Reviewer Agent...")
    from agents.video_qa_reviewer_agent import video_qa_reviewer_agent
    qa_res = video_qa_reviewer_agent(project_path)
    state["video_qa_status"] = qa_res.get("status")
    state["video_qa_feedback"] = qa_res.get("feedback")
    
    if qa_res.get("status") == "REJECTED":
        print(f"  ❌ Video QA Rejected: {qa_res.get('feedback')}")
        state["pipeline_status"] = "FAILED_QA"
        return state

    # ── STAGE 6: Render MP4 Video via HyperFrames CLI & Mix BG Music ─────────────
    if execute_render:
        print("\n🎬 [STAGE 6 MP4 RENDER] Executing HyperFrames CLI Render...")
        import subprocess
        clean_path = str(project_path).replace("\\\\?\\", "").replace("//?/", "")
        try:
            subprocess.run("npx hyperframes render -o renders/video.mp4", cwd=clean_path, check=True, shell=True)
            _mix_background_music(Path(clean_path))
        except Exception as e:
            print(f"⚠️ Render step warning: {e}")

    state["pipeline_status"] = "SUCCESS"
    return state

def _mix_background_music(project_path: Path):
    """Mix assets/bg-music.mp3 at 12% volume into the rendered MP4 video using ffmpeg."""
    renders_dir = project_path / "renders"
    bg_music_path = project_path / "assets" / "bg-music.mp3"
    
    if not renders_dir.exists() or not bg_music_path.exists():
        return
        
    mp4_files = list(renders_dir.glob("*.mp4"))
    if not mp4_files:
        return
        
    latest_mp4 = max(mp4_files, key=lambda f: f.stat().st_mtime)
    temp_mixed = renders_dir / f"mixed_{latest_mp4.name}"
    
    print(f"🎵 [FFmpeg Audio Mixer] Blending bg-music.mp3 into {latest_mp4.name} (volume=0.05)...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(latest_mp4),
        "-stream_loop", "-1",
        "-i", str(bg_music_path),
        "-filter_complex", "[1:a]volume=0.05[bg];[0:a][bg]amix=inputs=2:duration=first[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac",
        str(temp_mixed)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode == 0 and temp_mixed.exists() and temp_mixed.stat().st_size > 0:
        try:
            temp_mixed.replace(latest_mp4)
            print(f"  🎉 [FFmpeg Audio Mixer] Successfully merged background music into {latest_mp4.name}!")
        except Exception as e:
            print(f"  ⚠️ FFmpeg merge replacement warning: {e}")
    else:
        print(f"  ⚠️ FFmpeg Audio Mixer warning: {res.stderr[:200] if res.stderr else 'Unknown error'}")


    # ── STAGE 6: HyperFrames CLI Render ─────────────────────────────────────────
    if execute_render:
        print("\n🎬 [STAGE 6] Launching HyperFrames CLI Render Engine (npx hyperframes render)...")
        try:
            # Execute npx hyperframes render with Puppeteer flags
            clean_cwd = str(project_path).replace("\\\\?\\", "")
            render_cmd = ["npx", "--yes", "hyperframes@0.6.63", "render"]
            res = subprocess.run(render_cmd, cwd=clean_cwd, shell=True, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                print("  🎉 [SUCCESS] Video rendered successfully! MP4 output saved.")
                _mix_background_music(project_path)
                state["pipeline_status"] = "SUCCESS_RENDERED"
            else:
                print(f"  ⚠️ Render output: {res.stdout or res.stderr}")
                state["pipeline_status"] = "SCAFFOLDED_RENDER_READY"
        except Exception as re_err:
            print(f"  ⚠️ Render execution error: {re_err}")
            state["pipeline_status"] = "SCAFFOLDED_RENDER_READY"
    else:
        print("\n✅ [STAGE 6 Ready] Project is 100% Render-Ready!")
        print(f"   To preview run: cd '{project_path}' && npm run dev")
        print(f"   To render run:  cd '{project_path}' && npm run render")
        state["pipeline_status"] = "SCAFFOLDED_RENDER_READY"

    return state


if __name__ == "__main__":
    sample_state = {
        "session_id": "Session 01",
        "lesson_id": "Lesson 02",
        "technology_stack": "Python Core",
        "core_ssot": {
            "session_title": "Tổng quan về List trong Python",
            "lesson_details": "Cách khởi tạo list, các phương thức cơ bản append, pop, remove, slide slicing và ứng dụng thực tế trong quản lý dữ liệu kho hàng.",
            "expected_output": "Học viên nắm vững cách tạo và thao tác trên List Python chuẩn PEP 8"
        }
    }
    res = run_render_pipeline(sample_state, max_retries=2, execute_render=False)
    print("\nFinal Pipeline Status:", res.get("pipeline_status"))
