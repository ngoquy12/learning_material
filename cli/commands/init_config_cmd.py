"""
cli/commands/init_config_cmd.py
CLI handler for generating course configuration template (--init-config).
"""

import json
from pathlib import Path
from cli.curriculum_parser import parse_program_structure_from_ptit

def handle_init_config(course_id: str):
    """Generates a starter config file for a new course."""
    print(f"\n>>> Khởi tạo file cấu hình cho môn {course_id}...")

    default_excel = r"CLO-PLO\PM_PTIT_2026_Chương trình đào tạo.xlsx"
    course_info = None
    try:
        course_info = parse_program_structure_from_ptit(default_excel, course_id)
    except Exception:
        pass

    course_name = course_info["course_name"] if course_info else f"Tên môn ({course_id})"

    if course_info and course_info.get("hours"):
        h = course_info["hours"]
        dynamic_budget = {
            "total_sessions": h.get("total", 0),
            "theory_sessions": h.get("theory", 0),
            "practice_sessions": h.get("practice_total", 0),
            "mini_projects": h.get("mini_project", 0),
            "final_exam": h.get("exam", 0),
            "capstone_project": h.get("project", 0)
        }
    else:
        dynamic_budget = {}

    config_template = {
        "curriculum_excel_path": default_excel,
        "course_id": course_id,
        "student_profile": {
            "entry_level": "beginner",
            "background": "non-it",
            "cognitive_speed": 1.0
        },
        "session_budget": dynamic_budget,
        "class_configuration": {
            "session_duration_hours": 2.0,
            "delivery_mode": "offline",
            "sessions_per_day": 2,
            "weekly_frequency": 3
        },
        "tech_stack": "",
        "tech_stack_versions": {
            "_EXAMPLE_Library": "x.y"
        },
        "coding_standards": ""
    }

    safe_id = course_id.lower().replace("-", "").replace(" ", "_")
    config_path = Path(f"config/pm_generator_config_{safe_id}.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_template, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã tạo file cấu hình: {config_path}")
    if course_info:
        print(f"   Môn học: {course_name}")
        print(f"   PLOs: {len(course_info.get('plos', []))}, CLOs: {len(course_info.get('clos', []))}")
        if dynamic_budget:
            print(f"   Session Budget (từ Excel): {dynamic_budget['total_sessions']} buổi")
    print(f"\n📝 Hướng dẫn tiếp theo:")
    print(f"   1. Mở file {config_path} và điều chỉnh:")
    print(f"      - 'tech_stack': Công nghệ mục tiêu (ví dụ: 'python/core', 'typescript/nestjs', 'java/springboot')")
    print(f"      - 'student_profile': Trình độ đầu vào của sinh viên")
    print(f"   2. Chạy lệnh sinh PM:")
    print(f"      python main.py --generate-pm --pm-config {config_path} --tech-stack <tech> --output-pm-name PM_Generated_{safe_id.upper()} --approve-pm")
