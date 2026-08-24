"""
cli/publisher.py — Publishing, output formatting, and summary reporting for compiled learning assets.
"""

import os
import re
from pathlib import Path

def generate_obsidian_vault(excel_path: str, sessions: list, tech_stack: str = ""):
    """Generates Obsidian Knowledge Vault for the curriculum structure."""
    print(f"Loaded {len(sessions)} sessions for Obsidian Knowledge Vault generation.")

    prerequisite_data = None
    try:
        from agents.prerequisite_guard_agent import run_prerequisite_check_for_pm
        stack = tech_stack.strip() if tech_stack else ""
        if not stack and isinstance(sessions, list) and sessions:
            stack = str(sessions[0].get("technology_stack") or sessions[0].get("tech_stack") or "").strip()
            
        if stack:
            _, prerequisite_data = run_prerequisite_check_for_pm(sessions, stack)
            print(f"  [Obsidian] Prerequisite analysis complete: "
                  f"{prerequisite_data.get('stats', {}).get('total_violations', 0)} violations found.")
    except Exception as e:
        print(f"  [Obsidian] Prerequisite check skipped: {e}")

    try:
        from core.obsidian_knowledge_linker import generate_knowledge_vault
        vault_path = generate_knowledge_vault(excel_path, sessions, prerequisite_data=prerequisite_data)
        print(f"\n=====================================================================")
        print(f"  [Obsidian Vault Generated] Complete Knowledge Graph created at:")
        print(f"  --> {vault_path}")
        print(f"=====================================================================\n")
    except Exception as e:
        print(f"[Obsidian Vault Generation Error] {e}")

def export_scorm_package_cli(excel_path: str):
    """Exports compiled lessons to SCORM 1.2 zip package."""
    course_dir_name = Path(excel_path).stem.strip().replace(" ", "_").replace("-", "_")
    output_course_dir = os.path.join("output", course_dir_name)
    if not os.path.exists(output_course_dir):
        print(f"[SCORM] Lỗi: Thư mục output chưa tồn tại: {output_course_dir}")
        print("Hãy chạy pipeline biên dịch học liệu trước: python main.py --pm ... --approve-pm")
        return
    try:
        from core.scorm_exporter import export_scorm_package
        export_scorm_package(
            output_course_dir=output_course_dir,
            course_name=course_dir_name.replace("_", " "),
        )
    except Exception as e:
        print(f"[SCORM Export Error] {e}")

def show_cache_statistics():
    """Shows semantic cache statistics."""
    try:
        from core.semantic_cache import get_cache_stats, cache_invalidate_old
        cache_invalidate_old()
        stats = get_cache_stats()
        print("\n====== 📊 Semantic Cache Statistics ======")
        print(f"  Tổng response đã cache : {stats['total_cached_responses']}")
        print(f"  Tổng lần cache HIT     : {stats['total_cache_hits']}")
        print(f"  Ước tính tokens tiết kiệm: ~{stats['estimated_tokens_saved']:,}")
        print("  Phân tích theo Agent:")
        for agent, info in stats.get("by_agent", {}).items():
            print(f"    {agent}: {info['cached']} cached, {info['hits']} hits")
        print("==========================================\n")
    except Exception as e:
        print(f"[Cache Stats Error] {e}")

def handle_approval_command(args) -> bool:
    """
    Xử lý cờ --approve / --export-approvals. Trả True nếu đã xử lý và cần thoát.

    Tách khỏi luồng sinh học liệu vì đây là thao tác quản trị: người dùng chạy nó
    sau khi đã đọc trang rà soát, không phải trong lúc sinh nội dung.
    """
    from core.approvals import (
        DECISION_APPROVED,
        DECISION_REJECTED,
        export_approvals_csv,
        record_approval,
    )

    export_path = getattr(args, "export_approvals", "")
    if export_path:
        count = export_approvals_csv(export_path)
        print(f"Đã xuất {count} bản ghi hồ sơ kiểm định ra: {export_path}")
        return True

    target = getattr(args, "approve", "")
    if not target:
        return False

    reviewer = (getattr(args, "reviewer", "") or "").strip()
    if not reviewer:
        print(
            "Thiếu --reviewer. Hồ sơ kiểm định không chấp nhận quyết định vô danh:\n"
            '  python main.py --approve "Session 02/Lesson 01/html" --reviewer "Nguyen Van A"'
        )
        return True

    # "<Buổi>/<Bài>/<tài nguyên>" hoặc "<Buổi>/<tài nguyên>"
    parts = [p.strip() for p in str(target).split("/") if p.strip()]
    if len(parts) == 3:
        session_id, lesson_id, artifact = parts
    elif len(parts) == 2:
        session_id, lesson_id, artifact = parts[0], "", parts[1]
    else:
        print(
            f"Không hiểu tham số --approve: {target!r}. Định dạng đúng:\n"
            '  "<Buổi>/<Bài>/<tài nguyên>"  hoặc  "<Buổi>/<tài nguyên>"'
        )
        return True

    course = ""
    if getattr(args, "pm", None):
        from pathlib import Path as _Path

        course = _Path(args.pm).stem.replace("PM_Generated_", "").replace("_Updated", "").strip()

    decision = DECISION_REJECTED if getattr(args, "reject", False) else DECISION_APPROVED
    approval = record_approval(
        artifact=artifact,
        reviewer=reviewer,
        course=course,
        session_id=session_id,
        lesson_id=lesson_id,
        decision=decision,
        note=getattr(args, "approve_note", "") or "",
    )

    verb = "TỪ CHỐI" if decision == DECISION_REJECTED else "DUYỆT"
    print(
        f"Đã ghi nhận {verb}: {approval.session_id}"
        + (f"/{approval.lesson_id}" if approval.lesson_id else "")
        + f"/{approval.artifact} — bởi {approval.reviewer} lúc {approval.approved_at_iso}"
    )
    if decision == DECISION_APPROVED:
        print("  Tài nguyên này sẽ không bị ghi đè ở lần chạy sau (trừ khi dùng --force).")
    return True


def write_review_dashboard(course: str, states: list, course_dir) -> None:
    """Dựng trang rà soát cuối lượt chạy và in đường dẫn cho người vận hành."""
    try:
        from pathlib import Path as _Path

        from core.review_dashboard import build_dashboard_data, write_dashboard

        destination = _Path(course_dir) / "review_dashboard.html"
        written = write_dashboard(course, states, destination)
        if not written:
            return

        data = build_dashboard_data(course, states)
        if data.needs_attention:
            print(
                f"\n[Rà soát] {data.needs_attention} tài nguyên cần người xử lý. "
                f"Mở: {written}"
            )
        else:
            print(f"\n[Rà soát] Không có tài nguyên nào cần xử lý. Trang tổng hợp: {written}")
    except Exception as e:
        print(f"[Review Dashboard Error] {e}")


def print_run_cost_report():
    """In bảng chi phí của lượt chạy vừa xong và lưu lại để so sánh giữa các lần."""
    try:
        from core.run_metrics import format_run_report, persist_run_metrics

        report = format_run_report()
        if report:
            print(report)
            persist_run_metrics()
    except Exception as e:
        print(f"[Run Cost Report Error] {e}")


def print_generation_summary(summary: list):
    """Prints final generation summary report."""
    print("\n=====================================================================")
    print("ALL SESSIONS COMPILED! FINAL GENERATION REPORT:")
    print("=====================================================================")
    for s in summary:
        lbl = f"{s['session_id']} - {s['lesson_id']}" if s['lesson_id'] else s['session_id']
        print(f"Unit: {lbl} - {s['title']}")
        print(f"  - Status: {s['status']}")
        print(f"  - Critique Reviews Attempted: {s['review_count']}")
        print(f"  - HTML Reading: {s['html_file']}")
        print(f"  - Slide Deck:   {s['slides_file']}")
        print(f"  - Quiz JSON:    {s['quiz_file']}")
        print(f"  - Video Script: {s['video_script_file']}")
        print()
