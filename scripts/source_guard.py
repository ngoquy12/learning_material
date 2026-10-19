"""
scripts/source_guard.py - Chụp và so sánh trạng thái mã nguồn quanh một lượt tạo học liệu.

Dùng khi giao việc cho tác tử trong IDE (ví dụ Antigravity), nơi lệnh chạy không đi qua main.py:

  python scripts/source_guard.py snapshot      # TRƯỚC khi giao việc
  python scripts/source_guard.py verify        # SAU khi tác tử xong; mã thoát 1 nếu có thay đổi
  python scripts/source_guard.py status        # thay đổi chưa commit trong vùng cấm (theo Git)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.source_guard import (  # noqa: E402
    PROTECTED_DIRS,
    PROTECTED_FILES,
    project_root,
    save_snapshot,
    verify_snapshot,
)

SNAPSHOT_PATH = project_root() / "storage" / "source_guard_snapshot.json"


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "status"
    root = project_root()

    if cmd == "snapshot":
        n = save_snapshot(SNAPSHOT_PATH, root)
        print(f"Đã chụp {n} tệp vùng cấm vào {SNAPSHOT_PATH}")
        return 0

    if cmd == "verify":
        if not SNAPSHOT_PATH.exists():
            print("Chưa có ảnh chụp. Chạy: python scripts/source_guard.py snapshot")
            return 2
        changes = verify_snapshot(SNAPSHOT_PATH, root)
        if changes.any:
            print("Mã nguồn đã thay đổi kể từ lúc chụp:")
            print(changes.summary(limit=40))
            return 1
        print("Mã nguồn không đổi kể từ lúc chụp.")
        return 0

    if cmd == "status":
        paths = list(PROTECTED_DIRS) + list(PROTECTED_FILES)
        out = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", *paths],
            cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        lines = [l for l in out.stdout.splitlines() if l.strip() and "__pycache__" not in l]
        if lines:
            print(f"{len(lines)} thay đổi chưa commit trong vùng cấm:")
            print("\n".join(lines))
            return 1
        print("Vùng cấm sạch (không có thay đổi chưa commit).")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
