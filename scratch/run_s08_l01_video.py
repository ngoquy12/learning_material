"""
run_s08_l01_video.py
Chạy toàn bộ pipeline HyperFrames để tạo lại video bài học:
  Session 08 - Hàm (Function) và Phạm vi biến
  Lesson 01 - Giới thiệu hàm và cách định nghĩa
"""

import sys, os, json
from pathlib import Path

import sys, os, json
from pathlib import Path

# ── resolve workspace root (parent of scratch/) ────────────────────────────────
WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE))
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.chdir(WORKSPACE)  # ensure relative paths resolve correctly

from agents.creator_agents import video_script_agent
from agents.hyperframes_writer_agent import hyperframes_writer_agent
from hyperframes.video_pipeline_engine import VoiceDrivenVideoEngine
from core.state import AgentState



# ── 1. Xác định thư mục output ────────────────────────────────────────────────
OUTPUT_BASE = WORKSPACE / "output" / "PM_Python"
SESSION_DIR = OUTPUT_BASE / "Session 08 - Hàm (Function) va Phạm vi biến"
LESSON_DIR = SESSION_DIR / "Lesson 01 - Giới thiệu hàm và cách định nghĩa"
VIDEO_DIR = LESSON_DIR / "Video"
PROJECT_DIR = VIDEO_DIR / "session_08_lesson_01"

# Đọc bài đọc HTML SSOT nếu có
reading_html = ""
reading_candidates = [
    LESSON_DIR / "Bài đọc" / "reading.html",
    LESSON_DIR / "Bài đọc" / "reading.md",
    LESSON_DIR / "reading.html",
]
for rc in reading_candidates:
    if rc.exists():
        reading_html = rc.read_text(encoding="utf-8")
        print(f"[SSOT] Đọc bài đọc từ: {rc.relative_to(WORKSPACE)}")
        break
else:
    print("[SSOT] Không tìm thấy bài đọc. Sẽ dùng lesson_details làm nguồn.")

# ── 2. Thiết lập AgentState ────────────────────────────────────────────────────
state = AgentState({
    "session_id": "Session 08",
    "lesson_id": "Lesson 01",
    "technology_stack": "python/core",
    "html_content": reading_html,
    "core_ssot": {
        "session_title": "Giới thiệu hàm và cách định nghĩa",
        "lesson_details": (
            "Khái niệm hàm (Function) trong Python — tại sao cần dùng hàm. "
            "Cú pháp khai báo hàm với từ khóa def. "
            "Quy tắc đặt tên hàm chuẩn snake_case. "
            "Thụt lề (indentation) 4 khoảng trắng trong khối thân hàm. "
            "Docstring — tài liệu hóa hàm chuyên nghiệp với cặp nháy ba. "
            "Cơ chế vận hành bên dưới: Function Object trên Heap, Stack Frame khi gọi hàm. "
            "Luồng thực thi: định nghĩa hàm vs lời gọi hàm. "
            "Lỗi thường gặp: IndentationError, gọi hàm trước khi định nghĩa."
        ),
        "expected_output": "Video bài giảng HyperFrames 5-8 phút"
    },
    "course_dir_name": "PM_Python",
    "review_logs": [],
})

# ── 3. Stage 1: Sinh kịch bản với video_script_agent ──────────────────────────
print("\n" + "="*60)
print("[STAGE 1] Sinh kịch bản Blueprint JSON với Video Director Agent...")
print("="*60)
state = video_script_agent(state)

blueprint = state.get("video_script_json", {})
scenes = blueprint.get("scenes", [])
lesson_slug = state.get("video_lesson_slug", "session_08_lesson_01")
lesson_title = blueprint.get("lesson_title", "Giới thiệu hàm và cách định nghĩa")

print(f"\n✓ Blueprint: {len(scenes)} scenes, {blueprint.get('total_duration', 0):.1f}s tổng thời lượng")

# Ghi SCRIPT.md ra thư mục Video
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
script_md = state.get("video_script_markdown", "")
if script_md:
    script_md_path = VIDEO_DIR / "SCRIPT.md"
    script_md_path.write_text(script_md, encoding="utf-8")
    print(f"✓ SCRIPT.md → {script_md_path.relative_to(WORKSPACE)}")

# ── Gate: Kiểm định giọng văn narration trước khi TTS ────────────────────────
print("\n[NARRATION GATE] Kiểm định Section 4.3 Forbidden Words...")
from agents.video_qa_reviewer_agent import _check_narration_tone
all_narr = " ".join(sc.get("narration", "") for sc in scenes)
tone_violations = _check_narration_tone(all_narr)
if tone_violations:
    print(f"  ⚠️  Phát hiện {len(tone_violations)} vi phạm giọng văn:")
    for v in tone_violations[:5]:
        print(f"    → {v}")
    print("  → Pipeline tiếp tục nhưng cần chỉnh sửa narration trước khi xuất MP4.")
else:
    print("  ✓ Narration đạt chuẩn Giảng viên Đại học (không từ bị cấm).")

# ── 4. Stage 2-5: Chạy VoiceDrivenVideoEngine ─────────────────────────────────
print("\n" + "="*60)
print(f"[STAGE 2-5] VoiceDrivenVideoEngine → {PROJECT_DIR.relative_to(WORKSPACE)}")
print("="*60)

engine = VoiceDrivenVideoEngine(workspace_root=WORKSPACE)

# Xuất blueprint review trước
engine.export_blueprint_for_review(
    output_dir=PROJECT_DIR,
    lesson_slug=lesson_slug,
    lesson_title=lesson_title,
    scenes=scenes
)

result = engine.build_video_project(
    output_dir=PROJECT_DIR,
    lesson_slug=lesson_slug,
    lesson_title=lesson_title,
    scenes=scenes,
    tts_voice="hung_thinh",
    tts_speed=0.95,
)

print("\n" + "="*60)
print(f"[DONE] Pipeline hoàn tất!")
print(f"  Status : {result.get('status', 'unknown')}")
print(f"  Project : {PROJECT_DIR.relative_to(WORKSPACE)}")
print("="*60)
