"""
cli/commands/generate_pm_cmd.py
CLI handler for AI automated curriculum design & PM generation (--generate-pm).
"""

import os
import re
import json
from pathlib import Path
from cli.curriculum_parser import parse_program_structure_from_ptit, parse_all_sessions
from agents.pm_generator_agent import (
    generate_curriculum_pm,
    export_pm_to_markdown,
    export_pm_to_excel,
)

def handle_generate_pm(args):
    """Executes AI Automated Curriculum Design pipeline (SCAA / PM Generator Agent)."""
    print("\n=======================================================")
    print(">>> Giai đoạn -1: Thiết kế Chương trình Tự động (SPGA) <<<")
    print("=======================================================")
    
    config_path = Path(args.pm_config)
    if not config_path.exists():
        print(f"❌ Lỗi: Không tìm thấy file cấu hình tại {config_path}")
        return
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as err:
        print(f"❌ Lỗi khi đọc file cấu hình: {err}")
        return
        
    curriculum_excel = config_data.get("curriculum_excel_path")
    course_id = config_data.get("course_id")
    student_profile = config_data.get("student_profile", {})
    session_budget = config_data.get("session_budget", {})
    tech_stack = config_data.get("tech_stack")
    tech_stack_versions = config_data.get("tech_stack_versions", {})
    coding_standards = config_data.get("coding_standards", "")
    class_configuration = config_data.get("class_configuration", {
        "session_duration_hours": 2.0,
        "delivery_mode": "offline",
        "sessions_per_day": 1,
        "weekly_frequency": 3
    })

    if tech_stack_versions:
        version_parts = [f"{lib} {ver}" for lib, ver in tech_stack_versions.items()]
        tech_stack_display = ", ".join(version_parts)
        if coding_standards:
            tech_stack_display += f" ({coding_standards})"
    else:
        tech_stack_display = tech_stack or ""

    if not tech_stack_display or not tech_stack_display.strip():
        print("❌ Lỗi: Thiếu 'tech_stack' trong file cấu hình JSON hoặc cờ '--tech-stack'. Hệ thống TUYỆT ĐỐI KHÔNG tự động fallback công nghệ.")
        return
        
    if not curriculum_excel or not course_id:
        print("❌ Lỗi: Thiếu 'curriculum_excel_path' hoặc 'course_id' trong file cấu hình.")
        return
        
    print(f"Đang trích xuất thông tin chuẩn đầu ra (PLO/CLO) cho môn {course_id}...")
    course_info = parse_program_structure_from_ptit(curriculum_excel, course_id)
    if not course_info:
        print(f"❌ Không tìm thấy thông tin môn {course_id} trong tệp Excel {curriculum_excel}")
        return
        
    print(f"Môn học được tìm thấy: {course_info['course_name']} ({course_info['semester_id']})")
    print(f"Số chuẩn đầu ra đã trích xuất: PLOs={len(course_info['plos'])}, CLOs={len(course_info['clos'])}")
    if tech_stack_versions:
        print(f"Tech Stack (có phiên bản): {tech_stack_display}")
    
    output_base_dir = Path("output") / "pms"
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    raw_name = course_info["course_name"]
    match = re.search(r'\(([^)]+)\)', raw_name)
    vi_name = match.group(1).strip() if match else raw_name.strip()
    
    course_dir_name = vi_name.replace(" ", "_").replace("-", "_").replace("/", "_")
    course_dir = output_base_dir / course_dir_name
    course_dir.mkdir(parents=True, exist_ok=True)
    
    output_xlsx_path = course_dir / f"{args.output_pm_name}.xlsx"
    output_md_path = course_dir / f"{args.output_pm_name}.md"
    
    existing_pm = None
    is_update = False
    
    if output_xlsx_path.exists():
        print(f"  [Refactor Mode] Phát hiện tệp PM cũ tại {output_xlsx_path}. Đang phân tích cấu trúc cũ...")
        try:
            existing_pm = parse_all_sessions(str(output_xlsx_path))
            is_update = True
        except Exception as parse_err:
            print(f"  [Warning] Không thể đọc tệp PM cũ để làm mẫu: {parse_err}")
            
    if course_info.get("hours") and course_info["hours"].get("total", 0) > 0:
        h = course_info["hours"]
        session_budget = {
            "total_sessions": h["total"],
            "theory_sessions": h["theory"],
            "practice_sessions": h.get("practice_total", h.get("practice_offline", 0) + h.get("practice_online", 0)),
            "mini_projects": h.get("mini_project", 0),
            "final_exam": h.get("exam", 0),
            "capstone_project": h.get("project", 0)
        }
        print(f"Session Budget từ Excel: Total={session_budget['total_sessions']} (Lý thuyết={session_budget['theory_sessions']}, Thực hành={session_budget['practice_sessions']}, MiniProj={session_budget['mini_projects']}, Thi={session_budget['final_exam']}, Dự án={session_budget['capstone_project']})")

    print("Đang gọi AI Agent (SCAA) để thiết kế chương trình học chi tiết...")
    pm_data = generate_curriculum_pm(
        course_id=course_id,
        course_name=course_info["course_name"],
        clos=course_info["clos"],
        plos=course_info["plos"],
        student_profile=student_profile,
        session_budget=session_budget,
        tech_stack=tech_stack_display,
        class_configuration=class_configuration,
        existing_pm=existing_pm,
        main_content=course_info.get("main_content", ""),
        exam_type=course_info.get("exam_type", "")
    )
    
    if not pm_data:
        print("❌ Lỗi: Agent không thể tạo ra chương trình học hợp lệ.")
        return
        
    target_xlsx = str(course_dir / f"{args.output_pm_name}_Updated.xlsx") if is_update else str(output_xlsx_path)
    target_md = str(course_dir / f"{args.output_pm_name}_Updated.md") if is_update else str(output_md_path)
    
    export_pm_to_markdown(pm_data, course_id, course_info["course_name"], course_info["clos"], course_info["plos"], target_md, tech_stack=tech_stack_display)
    export_pm_to_excel(
        pm_data, course_id, course_info["course_name"], target_xlsx,
        template_path="templates/PM_Template_Standard.xlsx",
        clos=course_info["clos"],
        plos=course_info["plos"],
        student_profile=student_profile,
        tech_stack=tech_stack_display,
    )
    
    print(f"🎉 Thiết kế chương trình học thành công!")
    print(f"  - Bản thảo Markdown: {target_md}")
    print(f"  - Tệp Excel PM: {target_xlsx}")
