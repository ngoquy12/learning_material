# core/graph.py
from typing import Dict, Any
from antigravity import Workflow, parallel, component
from core.state import AgentState
from core.persistence import save_checkpoint
from agents import (
    objective_architect_agent, scheduler_agent, knowledge_base_agent,
    html_writer_agent, html_ux_reviewer,
    slide_agent, academic_reviewer,
    quiz_agent, sandbox_testing_agent,
    session_compiler_agent, video_script_agent, mindmap_agent,
    lessons_learned_agent, knowledge_memory_agent, get_relevant_memories_for_creator,
    pm_reviewer_agent, objective_reviewer_agent,
    mindmap_reviewer
)

def save_state_checkpoint(state: AgentState):
    """Helper to save checkpoint with lesson-specific key if lesson_id is present."""
    key = f"{state.get('session_id', 'default')}_{state.get('lesson_id', '')}".strip("_")
    save_checkpoint(key, state)

@component
def node_pm_review(state: AgentState) -> AgentState:
    """Giai đoạn 0: Review PM Input trước khi cho phép chạy"""
    if not state.get("pm_approved", False):
        import os
        full_curriculum = state.get("full_curriculum", state.get("pm_input"))
        report = pm_reviewer_agent(full_curriculum, state.get("technology_stack", "python/core"))
        
        course_dir_name = state.get("course_dir_name", "Unknown_Course")
        out_dir = os.path.join("output", course_dir_name)
        os.makedirs(out_dir, exist_ok=True)
        
        report_path = os.path.join(out_dir, "pm_review_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        raise ValueError(
            f"\n[CHỜ DUYỆT PM] Hệ thống đã đánh giá file PM và xuất báo cáo tại {report_path}.\n"
            f"Hãy xem báo cáo và điều chỉnh file PM. Sau khi PM đã duyệt, hãy truyền tham số pm_approved=True vào state để tiếp tục tiến trình!"
        )
    return state

@component
def node_prerequisite_check(state: AgentState) -> AgentState:
    """
    Giai đoạn 0.5: Kiểm tra tính tuần tự tri thức (Prerequisite Guard)
    Phân tích toàn bộ curriculum, xây dựng dependency graph và phát hiện
    vi phạm tiên quyết trước khi tốn bất kỳ token nào sinh nội dung.
    BLOCKER violations → dừng pipeline và yêu cầu sửa PM.
    """
    import json
    import os

    # Chỉ chạy khi được yêu cầu hoặc ở lần đầu tiên của session
    if state.get("prerequisite_checked"):
        return state

    full_curriculum_str = state.get("full_curriculum", "[]")
    try:
        sessions = json.loads(full_curriculum_str)
    except Exception:
        sessions = []

    if not sessions:
        return state

    tech_stack = state.get("technology_stack", "python/fastapi")
    course_dir_name = state.get("course_dir_name", "Unknown_Course")
    report_path = os.path.join("output", course_dir_name, "prerequisite_report.md")

    from agents.prerequisite_guard_agent import run_prerequisite_check_for_pm
    is_valid, prereq_result = run_prerequisite_check_for_pm(
        sessions=sessions,
        tech_stack=tech_stack,
        output_report_path=report_path,
    )

    # Lưu dependency graph vào state để Obsidian Linker dùng sau
    state["prerequisite_data"] = prereq_result
    state["prerequisite_checked"] = True

    if not is_valid:
        blocker_count = prereq_result.get("stats", {}).get("blocker_count", 0)
        raise ValueError(
            f"\n[PM CHƯA ĐẠT CHUẨN TUẦN TỰ] PrerequisiteGuardAgent phát hiện {blocker_count} vi phạm BLOCKER.\n"
            f"Báo cáo chi tiết: {report_path}\n"
            f"Vui lòng sửa PM để đảm bảo tính tuần tự tri thức trước khi biên dịch học liệu!"
        )

    return state

@component
def node_init_objectives(state: AgentState) -> AgentState:
    """Giai đoạn 1: ID Agent thiết lập chuẩn đầu ra dựa trên PM (Có vòng lặp phản biện sư phạm)"""
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("objectives") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
            
        previous_feedback = state.get("review_logs", [-1])[-1]["feedback"] if state.get("review_logs") and state["review_logs"][-1]["source"] == "Objective_Reviewer" else ""
        state["learning_outcomes"] = objective_architect_agent(state["pm_input"], state.get("technology_stack", "python/core"), previous_feedback)
        
        review = objective_reviewer_agent(state["learning_outcomes"], state["pm_input"], state.get("technology_stack", "python/core"))
        
        if review["status"] == "APPROVED":
            state.setdefault("artifacts_status", {})["objectives"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "Objective_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
            
    if not approved:
        print(
            f"\n[CẢNH BÁO SƯ PHẠM] Chuẩn đầu ra (Learning Outcomes) chưa hoàn toàn đạt yêu cầu ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và sử dụng bản nháp tốt nhất hiện tại để tiếp tục tiến hành!"
        )
        state.setdefault("artifacts_status", {})["objectives"] = "Approved with Warnings"
        save_state_checkpoint(state)
    return state

@component
def node_allocate_schedule(state: AgentState) -> AgentState:
    """Giai đoạn 2: Lập lịch và bóc tách cấu trúc thời gian của Session"""
    state["program_structure"] = scheduler_agent(state["learning_outcomes"], state["time_reference"], state.get("technology_stack", "python/core"))
    save_state_checkpoint(state)
    return state

@component
def node_lock_ssot(state: AgentState) -> AgentState:
    """Giai đoạn 3: Khóa dữ liệu gốc (SSOT) và ghi vào Persistence"""
    kb = knowledge_base_agent(state["program_structure"], state.get("technology_stack", "python/core"))
    
    # Merge existing core_ssot with kb
    state.setdefault("core_ssot", {}).update(kb)
    save_state_checkpoint(state)
    
    print(f"\n[SUCCESS] Đã thiết lập xong Lịch trình và Bản đồ Tri thức Gốc (SSOT)")
    return state

@component
def pipeline_html_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện (Critique Loop) tự động cho bài đọc HTML"""
    if "requested_parts" in state and "html" not in state["requested_parts"]:
        state["artifacts_status"]["html"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("html") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
        state = html_writer_agent(state)
        review = html_ux_reviewer(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["html"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state["review_logs"].append({"source": "UX_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Giao diện/Nội dung Bài đọc chưa hoàn toàn phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và tiếp tục tiến hành với bản nháp tốt nhất."
        )
        state["artifacts_status"]["html"] = "Approved with Warnings"
        save_state_checkpoint(state)
    return state

@component
def pipeline_slide_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện (Critique Loop) tự động cho Slide bài giảng"""
    if "requested_parts" in state and "slide" not in state["requested_parts"]:
        state["artifacts_status"]["slide"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("slide") == "Approved":
            approved = True
            break
        state = slide_agent(state)
        review = academic_reviewer(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["slide"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state["review_logs"].append({"source": "Academic_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Nội dung học thuật Slide chưa hoàn toàn phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và tiếp tục tiến hành với bản nháp tốt nhất."
        )
        state["artifacts_status"]["slide"] = "Approved with Warnings"
        save_state_checkpoint(state)
    return state

@component
def pipeline_quiz_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện cơ chế Sandbox cho cấu phần Quiz & Lab bài tập"""
    if "requested_parts" in state and "quiz" not in state["requested_parts"]:
        state["artifacts_status"]["quiz"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("quiz") == "Approved":
            approved = True
            break
        state = quiz_agent(state)
        review = sandbox_testing_agent(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["quiz"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state["review_logs"].append({"source": "Sandbox_Agent", "feedback": review["feedback"]})
            save_state_checkpoint(state)
    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Đáp án Quiz/Code Sandbox chưa hoàn toàn phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và tiếp tục tiến hành với bản nháp tốt nhất."
        )
        state["artifacts_status"]["quiz"] = "Approved with Warnings"
        save_state_checkpoint(state)
    return state

@component
def pipeline_video_script_production(state: AgentState) -> AgentState:
    """Vòng lặp phản biện (Critique Loop) tự động cho Video Script theo chuẩn HyperFrames"""
    if "requested_parts" in state and "video" not in state["requested_parts"] and "video_script" not in state["requested_parts"]:
        state["artifacts_status"]["video_script"] = "Skipped"
        return state
        
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("video_script") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
            
        state = video_script_agent(state)
        
        # Call the video script reviewer
        from agents.reviewer_agents import video_script_reviewer_agent
        review = video_script_reviewer_agent(state)
        
        if review["status"] == "APPROVED":
            state["artifacts_status"]["video_script"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "Video_Script_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
            
    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Kịch bản Video HyperFrames chưa hoàn toàn phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và tiếp tục tiến hành với bản nháp tốt nhất."
        )
        state["artifacts_status"]["video_script"] = "Approved with Warnings"
        save_state_checkpoint(state)
    return state

@component
def pipeline_mindmap_production(state: AgentState) -> AgentState:
    """Tự động tạo sơ đồ tư duy (mindmap) cho bài giảng với vòng lặp phản biện"""
    if "requested_parts" in state and "mindmap" not in state["requested_parts"]:
        state["artifacts_status"]["mindmap"] = "Skipped"
        return state
    approved = False
    for attempt in range(3):
        # Allow recovery if already approved in a previous execution
        if state.get("artifacts_status", {}).get("mindmap") == "Approved" and not state.get("force_rebuild", False):
            approved = True
            break
        state = mindmap_agent(state)
        review = mindmap_reviewer(state)
        if review["status"] == "APPROVED":
            state["artifacts_status"]["mindmap"] = "Approved"
            save_state_checkpoint(state)
            approved = True
            break
        else:
            state.setdefault("review_logs", []).append({"source": "Mindmap_Reviewer", "feedback": review["feedback"]})
            save_state_checkpoint(state)
            
    if not approved:
        print(
            f"\n[CẢNH BÁO TỪ PM] Nội dung Sơ đồ tư duy (Mindmap) chưa hoàn toàn phù hợp ở {state.get('session_id', 'Session')} - {state.get('lesson_id', 'Lesson')}.\n"
            f"Phản hồi phản biện: {state['review_logs'][-1]['feedback'] if state.get('review_logs') else 'Không có phản hồi.'}\n"
            f"Hệ thống BỎ QUA LỖI và tiếp tục tiến hành với bản nháp tốt nhất."
        )
        state["artifacts_status"]["mindmap"] = "Approved with Warnings"
        save_state_checkpoint(state)
    return state

@component
def pipeline_video_tts_and_render(state: AgentState) -> AgentState:
    """
    Cổng 3-7: TTS Audio Generation + HyperFrames Composition + Lint + Render + QA
    Tự động sản xuất video MP4 hoàn chỉnh từ blueprint đã được duyệt.
    """
    import subprocess
    import shutil
    from pathlib import Path

    if "requested_parts" in state and "video" not in state["requested_parts"]:
        state.setdefault("artifacts_status", {})["video_render"] = "Skipped"
        return state

    blueprint = state.get("video_script_json", {})
    if not blueprint or "scenes" not in blueprint:
        print("\n[Video_TTS_Render] SKIPPED — No approved blueprint in state.")
        state.setdefault("artifacts_status", {})["video_render"] = "Skipped"
        return state

    scenes = blueprint.get("scenes", [])
    lesson_slug = blueprint.get("lesson_slug", "lesson-video")
    lesson_title = blueprint.get("lesson_title", "Bài học")

    print(f"\n{'='*70}")
    print(f"🎬 VIDEO PRODUCTION PIPELINE: {lesson_title} ({len(scenes)} scenes)")
    print(f"{'='*70}")

    # ── Resolve output directory ──
    from agents.creator_agents import get_lesson_dir
    try:
        lesson_dir = get_lesson_dir(state)
    except Exception:
        lesson_dir = Path("output") / "lessons" / lesson_slug

    video_dir = lesson_dir / "Video" / lesson_slug
    compositions_dir = video_dir / "src" / "compositions"
    assets_dir = video_dir / "assets"
    assets_tts_dir = assets_dir / "tts"

    # Clean and recreate
    if video_dir.exists():
        shutil.rmtree(video_dir, ignore_errors=True)
    compositions_dir.mkdir(parents=True, exist_ok=True)
    assets_tts_dir.mkdir(parents=True, exist_ok=True)

    # Copy template media assets (intro.mp4, outro.mp4, bg-music.mp3) into assets_dir
    project_root = Path(__file__).resolve().parent.parent
    asset_search_paths = [
        project_root / "hyperframes" / "dev-tutorial-video" / "courses" / "fundamental_python" / "assets",
        project_root / "assets"
    ]
    for p in asset_search_paths:
        if p.exists():
            for asset_name in ["intro.mp4", "outro.mp4", "bg-music.mp3"]:
                src_file = p / asset_name
                dest_file = assets_dir / asset_name
                if src_file.exists() and not dest_file.exists():
                    try:
                        shutil.copy2(src_file, dest_file)
                        print(f"  ✓ Copied media asset: {asset_name}")
                    except Exception as e:
                        print(f"  ⚠️ Failed to copy asset {asset_name}: {e}")

    # ── GATE 3: TTS Audio Generation with Async Parallel Batching ──
    print("\n[Gate 3/7] Sinh giọng đọc TTS Audio song song (Async Batching)...")
    from core.tts_normalizer import normalize_tts_text
    import json
    import asyncio

    try:
        import edge_tts
        use_edge = True
    except ImportError:
        use_edge = False
        print("  ⚠️ edge_tts not available, using silent fallback")

    # Helper async task cho từng scene
    async def _async_gen_scene_tts(scene_item, voice="vi-VN-NamMinhNeural"):
        sc_id = scene_item["scene_id"]
        raw_text = scene_item.get("narration", "")
        norm_text = normalize_tts_text(raw_text)
        mp3 = assets_tts_dir / f"{sc_id}.mp3"
        if use_edge and norm_text:
            try:
                communicate = edge_tts.Communicate(norm_text, voice)
                await communicate.save(str(mp3))
                return sc_id, mp3, True
            except Exception as e:
                print(f"  ⚠️ TTS failed for {sc_id}: {e}, creating silent")
                _create_silent_mp3(mp3, max(8.0, len(raw_text.split()) / 2.5))
                return sc_id, mp3, False
        else:
            _create_silent_mp3(mp3, max(8.0, len(raw_text.split()) / 2.5))
            return sc_id, mp3, False

    async def _async_batch_tts_all():
        tasks = [_async_gen_scene_tts(s) for s in scenes]
        return await asyncio.gather(*tasks, return_exceptions=True)

    try:
        asyncio.run(_async_batch_tts_all())
    except Exception as batch_err:
        print(f"  ⚠️ Batch TTS fallback: {batch_err}")
        for scene in scenes:
            scene_id = scene["scene_id"]
            raw_narration = scene.get("narration", "")
            mp3_path = assets_tts_dir / f"{scene_id}.mp3"
            if not mp3_path.exists():
                _create_silent_mp3(mp3_path, max(8.0, len(raw_narration.split()) / 2.5))

    durations = {}
    cumulative_root = 9.24  # After intro

    for scene in scenes:
        scene_id = scene["scene_id"]
        mp3_path = assets_tts_dir / f"{scene_id}.mp3"
        dur = _probe_audio_duration(mp3_path)
        scene["duration"] = round(dur, 2)
        scene["start_at_root"] = round(cumulative_root, 2)
        durations[scene_id] = round(dur, 2)
        cumulative_root += round(dur, 2)

    # Write durations.json with actual TTS timings
    with open(assets_tts_dir / "durations.json", "w", encoding="utf-8") as f:
        json.dump(durations, f, indent=2, ensure_ascii=False)

    # Update blueprint total_duration
    blueprint["total_duration"] = round(cumulative_root + 12.15, 2)
    state["video_script_json"] = blueprint

    # Write TTS narration scripts as reference
    for scene in scenes:
        scene_id = scene["scene_id"]
        script_path = assets_tts_dir / f"{scene_id}_script.txt"
        script_path.write_text(scene.get("narration", ""), encoding="utf-8")

    print(f"  ✓ TTS hoàn tất song song: {len(durations)} audio files, tổng {sum(durations.values()):.1f}s")

    # ── GATE 4: HyperFrames Composition Writing ──
    print("\n[Gate 4/7] Dựng HyperFrames Project (Master Timeline + Sub-compositions)...")
    from agents.hyperframes_writer_agent import (
        _build_root_index_html, _build_scene_html,
        _build_meta_json, _build_package_json
    )

    # Root index.html
    root_html = _build_root_index_html(blueprint, lesson_slug)
    (video_dir / "index.html").write_text(root_html, encoding="utf-8")

    # Sub-compositions
    for scene in scenes:
        scene_html = _build_scene_html(scene, lesson_title)
        (compositions_dir / f"{scene['scene_id']}.html").write_text(scene_html, encoding="utf-8")

    # meta.json & package.json
    (video_dir / "meta.json").write_text(_build_meta_json(lesson_slug, lesson_title), encoding="utf-8")
    (video_dir / "package.json").write_text(_build_package_json(lesson_slug), encoding="utf-8")
    print(f"  ✓ HyperFrames Project scaffolded: {len(scenes)} scenes")

    # ── GATE 5: Lint Validation ──
    print("\n[Gate 5/7] Kiểm tra Validation (hyperframes lint)...")
    lint_res = subprocess.run(
        "npx --yes hyperframes@0.6.63 lint",
        shell=True, cwd=str(video_dir),
        capture_output=True, text=True, timeout=60
    )
    if lint_res.returncode == 0:
        print("  ✓ Lint PASSED")
    else:
        print(f"  ⚠️ Lint warnings (non-blocking): {lint_res.stdout[:200]}")

    # ── GATE 6: Controlled Heavy Render Execution ──
    import os
    enable_heavy_render = (
        os.getenv("ENABLE_HEAVY_VIDEO_RENDER", "false").lower() in ("true", "1", "yes")
        or state.get("render_video_mp4", False)
        or ("requested_parts" in state and "video_render" in state.get("requested_parts", []))
    )

    if not enable_heavy_render:
        print("\n[Gate 6/7] Bỏ qua Render MP4 nặng (Dự án HyperFrames HTML/TTS đã sẵn sàng cho Render khi cần).")
        print(f"  ✓ HyperFrames Scaffold hoàn tất tại: {video_dir}")
        state.setdefault("artifacts_status", {})["video_render"] = "SCAFFOLDED_READY"
        state["hyperframes_project_path"] = str(video_dir.resolve())
        save_state_checkpoint(state)
        return state

    print("\n[Gate 6/7] Render Video bằng HyperFrames Chromium Engine...")
    try:
        render_res = subprocess.run(
            "npx --yes hyperframes@0.6.63 render -o out.mp4",
            shell=True, cwd=str(video_dir),
            capture_output=True, text=True, timeout=600
        )
        out_mp4 = video_dir / "out.mp4"
        final_mp4 = video_dir / "final_render.mp4"

        if out_mp4.exists() and out_mp4.stat().st_size > 100000:
            shutil.copy(out_mp4, final_mp4)
            print(f"  ✓ Render SUCCESS: {final_mp4} ({final_mp4.stat().st_size / 1024 / 1024:.2f} MB)")

            # ── GATE 7: Post-render QA ──
            print("\n[Gate 7/7] Kiểm tra QA cuối cùng...")
            if final_mp4.stat().st_size > 500000:
                print("  ✓ QA PASSED — Video đạt chuẩn chất lượng")
                state.setdefault("artifacts_status", {})["video_render"] = "RENDERED"
            else:
                print("  ⚠️ QA WARNING — Video quá nhỏ, có thể thiếu nội dung")
                state.setdefault("artifacts_status", {})["video_render"] = "RENDERED_WITH_WARNINGS"
        else:
            print(f"  ❌ Render FAILED — output file missing or too small")
            state.setdefault("artifacts_status", {})["video_render"] = "RENDER_FAILED"
    except subprocess.TimeoutExpired:
        print("  ❌ Render TIMEOUT — exceeded 10 minutes")
        state.setdefault("artifacts_status", {})["video_render"] = "RENDER_TIMEOUT"
    except Exception as e:
        print(f"  ❌ Render ERROR: {e}")
        state.setdefault("artifacts_status", {})["video_render"] = "RENDER_ERROR"

    state["hyperframes_project_path"] = str(video_dir.resolve())
    save_state_checkpoint(state)
    return state


def _create_silent_mp3(path, dur: float):
    """Create a silent MP3 file of specified duration."""
    import subprocess
    cmd = f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t {dur} -q:a 2 "{path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _probe_audio_duration(path) -> float:
    """Get audio duration using ffprobe."""
    import subprocess
    try:
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
        probe = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        return float(probe) + 0.5
    except Exception:
        return 8.0


@component
def session_compiler_node(state: AgentState) -> AgentState:
    """Node 7: Tiến hành thu gom dữ liệu, tự động tạo cấu trúc cây thư mục vật lý bằng thư viện os, ghi file bài đọc HTML, ghi file Slide Markdown và dùng subprocess.run để gọi lệnh Marp CLI biên dịch slide ra HTML, xuất tệp câu hỏi JSON sạch ra ổ đĩa tại thư mục dist/"""
    state = session_compiler_agent(state)
    
    import os
    import json
    import subprocess
    
    # Create dist folder
    os.makedirs("dist", exist_ok=True)
    
    # Write reading.html
    html_content = state.get("html_content", "")
    if html_content:
        with open(os.path.join("dist", "reading.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
            
    # Write slides.md
    slide_md = state.get("slide_markdown", "")
    if slide_md:
        slides_path = os.path.join("dist", "slides.md")
        with open(slides_path, "w", encoding="utf-8") as f:
            f.write(slide_md)
        # Call Marp CLI to compile slide markdown to HTML
        try:
            print("  [Compiler] Compiling slide.md to slide.html via Marp CLI...")
            result = subprocess.run(
                "npx --yes @marp-team/marp-cli --no-stdin dist/slides.md -o dist/slides.html",
                shell=True,
                capture_output=True,
                encoding="utf-8",
                timeout=10
            )
            if result.returncode == 0:
                print("  [Compiler] Marp compiled slides successfully.")
            else:
                print(f"  [Compiler] Marp CLI exited with error code {result.returncode}: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("  [Compiler] Marp CLI compilation timed out after 10 seconds.")
        except Exception as e:
            print(f"  [Compiler] Marp CLI execution failed: {e}")
            
    # Write quiz.json
    quiz_data = state.get("quiz_json", {})
    if quiz_data:
        with open(os.path.join("dist", "quiz.json"), "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
            
    save_state_checkpoint(state)
    return state

@component
def lessons_learned_refiner(state: AgentState) -> AgentState:
    """
    Giai đoạn cuối: Đúc rút kinh nghiệm từ review_logs.
    - Gọi knowledge_memory_agent (SQLite-backed, phân loại có cấu trúc)
    - Vẫn gọi lessons_learned_agent (Markdown SKILL.md) để tương thích ngược
    """
    # Kho tri thức có cấu trúc mới (SQLite)
    state = knowledge_memory_agent(state)
    # Kho tri thức cũ (Markdown) — tương thích ngược với loader cũ
    state = lessons_learned_agent(state)
    save_state_checkpoint(state)
    return state

def compile_learning_content_workflow():
    workflow = Workflow()

    # Khai báo các Node trục dọc trong hệ thống Antigravity
    workflow.add_node("pm_review", node_pm_review)
    workflow.add_node("prerequisite_check", node_prerequisite_check)
    workflow.add_node("init_objectives", node_init_objectives)
    workflow.add_node("allocate_schedule", node_allocate_schedule)
    workflow.add_node("lock_ssot", node_lock_ssot)

    @component
    def node_generate_master_content(state: AgentState) -> AgentState:
        """Giai đoạn 3.5: Sinh Master Content tuần tự trước khi rẽ nhánh đa luồng để tránh lỗi Rate Limit và Cache Miss"""
        from agents.creator_agents import get_lesson_content
        session_id = state.get("session_id", "Session 01")
        lesson_id = state.get("lesson_id", "")
        core_ssot = state.get("core_ssot", {})
        lesson_title = core_ssot.get("session_title", "Course Session")
        lesson_details = core_ssot.get("lesson_details", "")
        expected_output = core_ssot.get("expected_output", "")
        
        # Call get_lesson_content to trigger LLM and populate state["master_content"]
        # It handles its own caching if already generated.
        get_lesson_content(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            lesson_details=lesson_details,
            expected_output=expected_output,
            attempt_num=1,
            core_ssot=core_ssot,
            state=state
        )
        return state

    @component
    def node_html_first_production(state: AgentState) -> AgentState:
        """
        Giai đoạn Reading-First:
        Tạo và duyệt Bài đọc HTML (`reading.html`) ĐẦU TIÊN làm cơ sở chuẩn ngữ cảnh cho tất cả tài nguyên dẫn xuất.
        """
        print("\n[Reading-First Pipeline] 📖 Đang khởi tạo sản xuất Bài đọc HTML chính làm Nguồn Sự Thật...")
        return pipeline_html_production(state)

    @component
    def node_parallel_derived_production(state: AgentState) -> AgentState:
        """
        Giai đoạn Parallel Derived Production:
        Cho phép 4 Creator Pipelines dẫn xuất (Slide, Quiz, Video Script, Mindmap)
        chạy song song sau khi Bài đọc HTML đã được phê duyệt làm SSOT.
        """
        import copy
        import time
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        print("\n[Parallel Engine] 🚀 Kích hoạt luồng sản xuất song song 4 tài nguyên dẫn xuất từ Bài đọc HTML...")
        start_t = time.time()
        
        # 4 Creator Pipelines dẫn xuất bám sát Bài đọc HTML
        pipelines = [
            ("Slide", pipeline_slide_production),
            ("Quiz", pipeline_quiz_production),
            ("VideoScript", pipeline_video_script_production),
            ("Mindmap", pipeline_mindmap_production),
        ]
        
        futures_map = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            for name, fn in pipelines:
                state_copy = copy.deepcopy(state)
                future = executor.submit(fn, state_copy)
                futures_map[future] = name
                
            for future in as_completed(futures_map):
                name = futures_map[future]
                try:
                    sub_state = future.result()
                    if sub_state.get("slide_markdown"):
                        state["slide_markdown"] = sub_state["slide_markdown"]
                    if sub_state.get("slide_html"):
                        state["slide_html"] = sub_state["slide_html"]
                    if sub_state.get("quiz_json"):
                        state["quiz_json"] = sub_state["quiz_json"]
                    if sub_state.get("video_script_markdown"):
                        state["video_script_markdown"] = sub_state["video_script_markdown"]
                    if sub_state.get("video_script_json"):
                        state["video_script_json"] = sub_state["video_script_json"]
                    if sub_state.get("mindmap_markdown"):
                        state["mindmap_markdown"] = sub_state["mindmap_markdown"]
                    
                    if "artifacts_status" in sub_state:
                        state.setdefault("artifacts_status", {}).update(sub_state["artifacts_status"])
                    if sub_state.get("review_logs"):
                        for log in sub_state["review_logs"]:
                            if log not in state.setdefault("review_logs", []):
                                state["review_logs"].append(log)
                    print(f"  ✓ [Parallel Engine] Nhánh dẫn xuất {name} hoàn tất.")
                except Exception as e:
                    print(f"  ❌ [Parallel Engine] Nhánh dẫn xuất {name} lỗi: {e}")
                    
        elapsed = time.time() - start_t
        print(f"[Parallel Engine] ✅ Tất cả tài nguyên dẫn xuất đã hoàn tất song song trong {elapsed:.2f}s!\n")
        save_state_checkpoint(state)
        return state

    workflow.add_node("generate_master_content", node_generate_master_content)
    workflow.add_node("html_first_production", node_html_first_production)
    workflow.add_node("parallel_derived_production", node_parallel_derived_production)
    workflow.add_node("video_tts_and_render", pipeline_video_tts_and_render)
    workflow.add_node("final_compiler_and_publish", session_compiler_node)
    workflow.add_node("lessons_learned_refiner", lessons_learned_refiner)

    # Thiết lập đồ thị liên kết (Edges)
    workflow.set_entry_point("pm_review")
    workflow.add_edge("pm_review", "prerequisite_check")
    workflow.add_edge("prerequisite_check", "init_objectives")
    workflow.add_edge("init_objectives", "allocate_schedule")
    workflow.add_edge("allocate_schedule", "lock_ssot")
    workflow.add_edge("lock_ssot", "generate_master_content")
    
    # BẮT BUỘC: Bài đọc HTML sản xuất & kiểm duyệt ĐẦU TIÊN -> sau đó 4 tài nguyên dẫn xuất chạy song song
    workflow.add_edge("generate_master_content", "html_first_production")
    workflow.add_edge("html_first_production", "parallel_derived_production")
    workflow.add_edge("parallel_derived_production", "video_tts_and_render")
    workflow.add_edge("video_tts_and_render", "final_compiler_and_publish")
    workflow.add_edge("final_compiler_and_publish", "lessons_learned_refiner")

    return workflow.compile()