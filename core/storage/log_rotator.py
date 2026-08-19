"""
core/storage/log_rotator.py
Log rotation, trace log pruning, and storage administration utilities.
"""

import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

def rotate_trace_logs(
    log_path: str = "storage/trace_logs.jsonl",
    max_size_mb: float = 10.0,
    backup_count: int = 5
) -> bool:
    """
    Checks if trace_logs.jsonl exceeds max_size_mb. If so, rotates existing log files:
    trace_logs.jsonl -> trace_logs.jsonl.1 -> trace_logs.jsonl.2 ... up to backup_count.
    Returns True if rotation occurred, False otherwise.
    """
    p = Path(log_path)
    if not p.exists() or not p.is_file():
        return False

    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb < max_size_mb:
        return False

    # Delete oldest backup if it exceeds backup_count
    oldest = Path(f"{log_path}.{backup_count}")
    if oldest.exists():
        oldest.unlink(missing_ok=True)

    # Shift backups: .4 -> .5, .3 -> .4, .2 -> .3, .1 -> .2
    for i in range(backup_count - 1, 0, -1):
        src = Path(f"{log_path}.{i}")
        dst = Path(f"{log_path}.{i + 1}")
        if src.exists():
            shutil.move(str(src), str(dst))

    # Move current log to .1
    first_backup = Path(f"{log_path}.1")
    shutil.move(str(p), str(first_backup))

    # Create new empty log file
    p.touch()
    return True

def clean_old_logs(
    log_dir: str = "storage",
    max_age_days: int = 30,
    pattern: str = "*.jsonl*"
) -> int:
    """
    Removes log files older than max_age_days in log_dir.
    Returns count of removed files.
    """
    p = Path(log_dir)
    if not p.exists() or not p.is_dir():
        return 0

    now = time.time()
    max_age_seconds = max_age_days * 86400
    removed_count = 0

    for file_path in p.glob(pattern):
        if file_path.is_file():
            age_seconds = now - file_path.stat().st_mtime
            if age_seconds > max_age_seconds:
                try:
                    file_path.unlink()
                    removed_count += 1
                except Exception:
                    pass

    return removed_count

def vacuum_trace_logs(
    log_path: str = "storage/trace_logs.jsonl",
    max_entries: int = 10000
) -> int:
    """
    Trims trace log to retain only the most recent max_entries lines.
    Returns number of pruned lines.
    """
    p = Path(log_path)
    if not p.exists() or not p.is_file():
        return 0

    try:
        lines = p.read_text(encoding="utf-8").splitlines()
        total_lines = len(lines)
        if total_lines <= max_entries:
            return 0

        retained = lines[-max_entries:]
        p.write_text("\n".join(retained) + "\n", encoding="utf-8")
        return total_lines - max_entries
    except Exception:
        return 0

def get_storage_metrics(
    storage_dir: str = "storage",
    output_dir: str = "output"
) -> Dict[str, Any]:
    """Calculates disk usage metrics for storage and output directories."""
    def get_dir_size_bytes(directory: Path) -> int:
        if not directory.exists() or not directory.is_dir():
            return 0
        total = 0
        for entry in directory.rglob("*"):
            if entry.is_file():
                try:
                    total += entry.stat().st_size
                except Exception:
                    pass
        return total

    s_path = Path(storage_dir)
    o_path = Path(output_dir)

    storage_bytes = get_dir_size_bytes(s_path)
    output_bytes = get_dir_size_bytes(o_path)

    trace_file = s_path / "trace_logs.jsonl"
    trace_size_bytes = trace_file.stat().st_size if trace_file.exists() else 0

    return {
        "storage_dir": str(s_path),
        "storage_size_bytes": storage_bytes,
        "storage_size_mb": round(storage_bytes / (1024 * 1024), 2),
        "trace_log_size_bytes": trace_size_bytes,
        "trace_log_size_mb": round(trace_size_bytes / (1024 * 1024), 2),
        "output_dir": str(o_path),
        "output_size_bytes": output_bytes,
        "output_size_mb": round(output_bytes / (1024 * 1024), 2),
    }
