"""
scripts/clean_logs.py
CLI Administration script for cleaning, vacuuming, and rotating log files and storage metrics.
Usage:
    python scripts/clean_logs.py --status
    python scripts/clean_logs.py --rotate
    python scripts/clean_logs.py --vacuum 5000
    python scripts/clean_logs.py --clean-old 30
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.storage.log_rotator import (
    rotate_trace_logs,
    clean_old_logs,
    vacuum_trace_logs,
    get_storage_metrics,
)

def main():
    parser = argparse.ArgumentParser(description="Log and Storage Administration Utility for Elearning Content Factory.")
    parser.add_argument("--status", action="store_true", help="Print storage and log metrics")
    parser.add_argument("--rotate", action="store_true", help="Force trace log rotation")
    parser.add_argument("--max-size", type=float, default=10.0, help="Max log size in MB before rotation (default: 10.0)")
    parser.add_argument("--vacuum", type=int, default=0, help="Trim trace log to the specified max number of entries")
    parser.add_argument("--clean-old", type=int, default=0, help="Delete logs older than N days")

    args = parser.parse_args()

    print("==========================================================")
    print("📊 Elearning Factory — Storage & Log Administration Utility")
    print("==========================================================")

    if args.rotate:
        rotated = rotate_trace_logs("storage/trace_logs.jsonl", max_size_mb=0.0) # force
        if rotated:
            print("✅ Đã xoay vòng tệp trace_logs.jsonl thành công!")
        else:
            print("ℹ️ Tệp log chưa tồn tại hoặc không cần xoay vòng.")

    if args.vacuum > 0:
        pruned = vacuum_trace_logs("storage/trace_logs.jsonl", max_entries=args.vacuum)
        print(f"🧹 Đã cắt tỉa {pruned} dòng log cũ. Giữ lại {args.vacuum} dòng mới nhất.")

    if args.clean_old > 0:
        removed = clean_old_logs("storage", max_age_days=args.clean_old)
        print(f"🗑️ Đã dọn dẹp {removed} tệp log cũ quá {args.clean_old} ngày.")

    # Always show metrics summary
    metrics = get_storage_metrics("storage", "output")
    print("\n📈 Báo cáo Dung lượng Lưu trữ:")
    print(f"  - Thư mục Storage: {metrics['storage_size_mb']} MB ({metrics['storage_size_bytes']} bytes)")
    print(f"  - Tệp Trace Logs:  {metrics['trace_log_size_mb']} MB ({metrics['trace_log_size_bytes']} bytes)")
    print(f"  - Thư mục Output:  {metrics['output_size_mb']} MB ({metrics['output_size_bytes']} bytes)")
    print("==========================================================")

if __name__ == "__main__":
    main()
