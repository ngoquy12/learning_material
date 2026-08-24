"""
cli/args.py — Command-line argument parsing for Elearning Content Factory.
"""

import argparse
import os

def parse_cli_arguments():
    """Parses and returns command line arguments for the Elearning Content Factory."""
    parser = argparse.ArgumentParser(description="Multi-Agent Learning Content Factory")
    parser.add_argument(
        "--pm",
        type=str,
        default=None,
        help="Path to PM Excel sheet (required for content generation)"
    )
    parser.add_argument(
        "--session",
        type=str,
        default="all",
        help="Session ID to run (e.g. 'Session 01', 'Session 02', or 'all')"
    )
    parser.add_argument(
        "--parts",
        type=str,
        default="all",
        help="Comma-separated parts to generate (html,quiz,practical_lab,video_script or all)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild artifacts even if already approved in checkpoint"
    )
    parser.add_argument(
        "--approve-pm",
        action="store_true",
        help="Approve the PM program and bypass the PM review blocker"
    )
    parser.add_argument(
        "--obsidian",
        action="store_true",
        help="Generate Obsidian Vault for the entire course structure"
    )
    parser.add_argument(
        "--scorm",
        action="store_true",
        help="Export compiled lessons to SCORM 1.2 .zip package for LMS import (Moodle, Canvas, etc.)"
    )
    parser.add_argument(
        "--approve",
        type=str,
        default="",
        help=(
            "Ghi nhận giảng viên đã rà và duyệt một tài nguyên. "
            "Định dạng: '<Buổi>/<Bài>/<tài nguyên>' hoặc '<Buổi>/<tài nguyên>'. "
            "Tài nguyên đã duyệt sẽ không bị ghi đè ở lần chạy sau (trừ khi --force)."
        )
    )
    parser.add_argument(
        "--reviewer",
        type=str,
        default="",
        help="Tên người rà soát, bắt buộc khi dùng --approve (hồ sơ kiểm định không nhận quyết định vô danh)"
    )
    parser.add_argument(
        "--approve-note",
        type=str,
        default="",
        help="Ghi chú kèm quyết định rà soát"
    )
    parser.add_argument(
        "--reject",
        action="store_true",
        help="Dùng cùng --approve để ghi nhận quyết định TỪ CHỐI thay vì duyệt"
    )
    parser.add_argument(
        "--export-approvals",
        type=str,
        default="",
        help="Xuất hồ sơ kiểm định (ai duyệt gì, khi nào) ra file CSV rồi thoát"
    )
    parser.add_argument(
        "--xapi-endpoint",
        type=str,
        default="",
        help="Địa chỉ LRS nhận phát biểu xAPI khi xuất gói (--scorm). Để trống thì chỉ kèm cmi5.xml."
    )
    parser.add_argument(
        "--xapi-auth",
        type=str,
        default="",
        help="Chuỗi Authorization gửi kèm khi gọi LRS (nếu LRS yêu cầu)"
    )
    parser.add_argument(
        "--ingest-xapi",
        type=str,
        default="",
        help=(
            "Nạp file phát biểu xAPI do LRS xuất ra (JSON hoặc JSONL), rút tín hiệu "
            "học tập và ghi vào kho kinh nghiệm để lần sinh sau tránh lặp lại lỗi."
        )
    )
    parser.add_argument(
        "--ingest-dry-run",
        action="store_true",
        help="Dùng cùng --ingest-xapi: chỉ xem sẽ rút ra luật gì, KHÔNG ghi vào kho kinh nghiệm"
    )
    parser.add_argument(
        "--min-cohort",
        type=int,
        default=0,
        help=(
            "Cỡ mẫu tối thiểu để một tín hiệu học tập được coi là có thật (mặc định 15). "
            "Hạ ngưỡng khi thử nghiệm thì được, nhưng đừng hạ khi chạy thật."
        )
    )
    parser.add_argument(
        "--cache-stats",
        action="store_true",
        help="Show Semantic Cache statistics and exit"
    )
    parser.add_argument(
        "--tech-stack",
        type=str,
        default="",
        help="Explicit technology stack (e.g. 'python/core', 'typescript/nestjs', 'typescript/react', 'java/springboot')"
    )
    parser.add_argument(
        "--generate-pm",
        action="store_true",
        help="Enable automatic PM/Syllabus design from PLO/CLO via AI Agent"
    )
    parser.add_argument(
        "--pm-config",
        type=str,
        default=r"config/pm_generator_config.json",
        help="Path to student profile and target course configuration for PM generation"
    )
    parser.add_argument(
        "--output-pm-name",
        type=str,
        default="PM_Generated",
        help="Custom name for the generated Excel and Markdown files"
    )
    parser.add_argument(
        "--init-config",
        type=str,
        metavar="COURSE_ID",
        default=None,
        help="Tạo file config mẫu cho môn mới (ví dụ: --init-config IT-106)"
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Khởi tạo nhanh toàn bộ cây cấu trúc thư mục và tài nguyên rỗng cho môn học từ file PM Excel mà không chạy LLM sinh chi tiết."
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Enable async parallel batch execution of independent lessons within sessions"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Maximum concurrent worker threads for parallel batch execution (default: 4)"
    )
    return parser.parse_args()

