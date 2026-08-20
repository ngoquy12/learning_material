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
