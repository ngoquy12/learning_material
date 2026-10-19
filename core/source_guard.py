"""
core/source_guard.py - Phát hiện mã nguồn bị sửa trong lúc chạy tạo học liệu.

Vì sao cần: khi tạo tài nguyên cho một môn, mọi thứ được phép ghi chỉ nằm trong `output/`
(và `storage/`, `dist/` đã bị Git bỏ qua). Mã nguồn, skill, template, cấu hình, test là
"vùng cấm" trong lượt chạy đó. Một tác tử tự trị (ví dụ trong Antigravity) gặp lỗi khi sinh
học liệu thường "sửa luôn" mã nguồn để vượt qua lỗi - làm đổi hành vi của cả hệ thống mà
người dùng không hay biết. Guard này chụp băm nội dung vùng cấm trước lượt chạy và so sánh
sau lượt chạy, để mọi thay đổi đều hiện ra ngay thay vì nằm lẫn trong `git status`.

Chỉ dùng thư viện chuẩn, không gọi LLM, không phụ thuộc Git.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional

# Vùng cấm: thay đổi ở đây KHÔNG phải là một phần của việc tạo học liệu.
PROTECTED_DIRS = (
    "agents",
    "core",
    "cli",
    "config",
    "skills",
    "templates",
    "scripts",
    "tests",
    ".agents",
    ".github",
)
PROTECTED_FILES = (
    "main.py",
    "antigravity.py",
    "requirements.txt",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yaml",
    ".env.example",
)
_IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
_IGNORED_SUFFIXES = (".pyc", ".pyo", ".db", ".db-wal", ".db-shm", ".log")


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _iter_protected_files(root: Path) -> Iterable[Path]:
    for name in PROTECTED_FILES:
        path = root / name
        if path.is_file():
            yield path
    for d in PROTECTED_DIRS:
        base = root / d
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x not in _IGNORED_PARTS]
            for fn in filenames:
                if fn.endswith(_IGNORED_SUFFIXES):
                    continue
                yield Path(dirpath) / fn


def _digest(path: Path) -> str:
    h = hashlib.sha1()
    try:
        # Chuẩn hóa xuống dòng: CRLF/LF khác nhau không được tính là "sửa".
        h.update(path.read_bytes().replace(b"\r\n", b"\n"))
    except OSError:
        return "unreadable"
    return h.hexdigest()


def take_snapshot(root: Optional[Path] = None) -> Dict[str, str]:
    """{đường dẫn tương đối (dấu /): băm nội dung} của toàn bộ vùng cấm."""
    root = root or project_root()
    return {p.relative_to(root).as_posix(): _digest(p) for p in _iter_protected_files(root)}


@dataclass
class SourceChanges:
    added: List[str] = field(default_factory=list)
    modified: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)

    @property
    def any(self) -> bool:
        return bool(self.added or self.modified or self.removed)

    def summary(self, limit: int = 15) -> str:
        lines = []
        for label, items in (("Thêm mới", self.added), ("Đã sửa", self.modified), ("Đã xóa", self.removed)):
            if items:
                shown = ", ".join(items[:limit]) + (f" và {len(items) - limit} tệp khác" if len(items) > limit else "")
                lines.append(f"  - {label} ({len(items)}): {shown}")
        return "\n".join(lines)


def diff_snapshots(before: Dict[str, str], after: Dict[str, str]) -> SourceChanges:
    return SourceChanges(
        added=sorted(set(after) - set(before)),
        modified=sorted(k for k in before.keys() & after.keys() if before[k] != after[k]),
        removed=sorted(set(before) - set(after)),
    )


class SourceGuard:
    """Dùng quanh một lượt chạy: `guard = SourceGuard.start()` ... `guard.report()`."""

    def __init__(self, before: Dict[str, str], root: Optional[Path] = None):
        self.before = before
        self.root = root or project_root()

    @classmethod
    def start(cls, root: Optional[Path] = None) -> "SourceGuard":
        return cls(take_snapshot(root), root)

    def check(self) -> SourceChanges:
        return diff_snapshots(self.before, take_snapshot(self.root))

    def report(self) -> SourceChanges:
        changes = self.check()
        if changes.any:
            print(
                "\n[SOURCE GUARD] CẢNH BÁO: mã nguồn/skill/template/cấu hình đã thay đổi trong lượt chạy "
                "tạo học liệu này. Lượt chạy chỉ được ghi vào output/. Hãy xem lại các thay đổi sau:"
            )
            print(changes.summary())
            print("  Hoàn tác bằng: git diff <tệp> để xem, git checkout -- <tệp> để bỏ (nếu không cần giữ).\n")
        else:
            print("[SOURCE GUARD] Mã nguồn không bị thay đổi trong lượt chạy.")
        return changes


def save_snapshot(path: Path, root: Optional[Path] = None) -> int:
    snap = take_snapshot(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snap, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    return len(snap)


def verify_snapshot(path: Path, root: Optional[Path] = None) -> SourceChanges:
    before = json.loads(path.read_text(encoding="utf-8"))
    return diff_snapshots(before, take_snapshot(root))
