"""
core/course_version.py — Phiên bản học liệu và nhật ký thay đổi giữa hai lần sinh (F3).

Một khoá học được sinh lại nhiều lần: sửa PM, đổi tech stack, nâng prompt, chạy lại
sau khi giảng viên rà soát. Nhưng hệ thống không lưu lại gì giữa các lần, nên ba câu
hỏi vận hành cơ bản đều không trả lời được:

    - "Lớp K18 học bản nào, lớp K19 học bản nào?"
    - "Lần chạy hôm nay đổi những gì so với hôm qua?"
    - "Bài này tôi rà tuần trước, giờ nó còn nguyên như lúc tôi duyệt không?"

Câu thứ ba là câu đắt nhất: giảng viên phải mở từng file đọc lại mới biết. Với 20
buổi × 3 bài × 5 tài nguyên thì việc đó không ai làm.

Module này chụp trạng thái (ảnh chụp băm nội dung từng artifact) mỗi lần sinh, so
hai ảnh chụp để ra nhật ký thay đổi, và đánh số phiên bản theo mức độ thay đổi.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCHEMA = """
CREATE TABLE IF NOT EXISTS course_snapshots (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    course       TEXT NOT NULL,
    version      TEXT NOT NULL,
    created_at   REAL NOT NULL,
    commit_sha   TEXT DEFAULT '',
    note         TEXT DEFAULT '',
    digests_json TEXT NOT NULL DEFAULT '{}'
)
"""

_INDEX = """
CREATE INDEX IF NOT EXISTS idx_snapshot_course
ON course_snapshots(course, created_at)
"""

# Các đuôi file được coi là học liệu. Ảnh và tệp tạm bị bỏ qua: chúng đổi vì lý do
# kỹ thuật (nén lại, đổi timestamp) chứ không phải vì nội dung dạy học đổi, và đưa
# vào sẽ khiến mọi lần sinh đều báo "có thay đổi".
TRACKED_SUFFIXES = (".html", ".md", ".json", ".xlsx", ".pptx")

# Tên file bị bỏ qua vì là sản phẩm phụ của chính hệ thống, không phải học liệu.
#
# CHANGELOG.md nằm trong danh sách này vì một lý do cụ thể: chính module này ghi ra
# nó. Không loại trừ thì nó tự theo dõi chính mình — mỗi lần sinh, nội dung nhật ký
# đổi, nên lần sinh KẾ TIẾP luôn thấy "có 1 tài nguyên sửa đổi" và tăng số phiên bản
# dù học liệu không đổi gì. Số phiên bản khi đó mất hết ý nghĩa.
IGNORED_NAMES = ("review_dashboard.html", "pm_review_report.md", "CHANGELOG.md")


@dataclass
class Snapshot:
    course: str
    version: str
    created_at: float
    commit_sha: str = ""
    note: str = ""
    digests: Dict[str, str] = field(default_factory=dict)

    @property
    def artifact_count(self) -> int:
        return len(self.digests)


@dataclass
class Changelog:
    """Khác biệt giữa hai ảnh chụp."""

    course: str
    from_version: str
    to_version: str
    added: List[str] = field(default_factory=list)
    modified: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.modified or self.removed)

    @property
    def total_changes(self) -> int:
        return len(self.added) + len(self.modified) + len(self.removed)

    def to_markdown(self) -> str:
        lines = [
            f"# Nhật ký thay đổi học liệu — {self.course}",
            "",
            f"**Từ phiên bản** `{self.from_version}` → **`{self.to_version}`**",
            "",
        ]

        if self.is_empty:
            lines.append("Không có thay đổi nào so với phiên bản trước.")
            return "\n".join(lines)

        lines.append(
            f"Tổng cộng **{self.total_changes}** thay đổi: "
            f"{len(self.added)} thêm mới, {len(self.modified)} sửa đổi, "
            f"{len(self.removed)} gỡ bỏ."
        )
        lines.append("")

        for title, items in (
            ("Thêm mới", self.added),
            ("Sửa đổi", self.modified),
            ("Gỡ bỏ", self.removed),
        ):
            if not items:
                continue
            lines.append(f"## {title} ({len(items)})")
            lines.append("")
            for item in sorted(items):
                lines.append(f"- `{item}`")
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"


def _digest_file(path: Path) -> str:
    """
    Băm nội dung một file, đã chuẩn hoá ký tự xuống dòng.

    Không chuẩn hoá thì cùng một nội dung sinh trên Windows và trên Linux cho hai mã
    băm khác nhau, và mọi lần chạy đổi máy đều báo "toàn bộ học liệu đã thay đổi".
    """
    data = path.read_bytes()
    if path.suffix.lower() in (".html", ".md", ".json"):
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()[:16]


def scan_course_digests(course_dir: str) -> Dict[str, str]:
    """Quét thư mục khoá học, trả về {đường dẫn tương đối: mã băm}."""
    root = Path(course_dir)
    if not root.exists():
        return {}

    digests: Dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TRACKED_SUFFIXES:
            continue
        if path.name in IGNORED_NAMES:
            continue
        try:
            rel = path.relative_to(root).as_posix()
            digests[rel] = _digest_file(path)
        except Exception:
            continue
    return digests


def compare_digests(
    old: Dict[str, str], new: Dict[str, str]
) -> Tuple[List[str], List[str], List[str]]:
    """Trả về (thêm mới, sửa đổi, gỡ bỏ)."""
    old_keys, new_keys = set(old), set(new)
    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    modified = sorted(k for k in (old_keys & new_keys) if old[k] != new[k])
    return added, modified, removed


def next_version(previous: Optional[str], changes: Tuple[List[str], List[str], List[str]]) -> str:
    """
    Tính số phiên bản kế tiếp theo mức độ thay đổi.

    Quy ước, cố ý đơn giản và đoán được:
      - Thêm hoặc gỡ tài nguyên  -> tăng số MINOR (cấu trúc khoá học đã đổi).
      - Chỉ sửa nội dung sẵn có  -> tăng số PATCH.
      - Không thay đổi gì        -> giữ nguyên phiên bản cũ. Sinh ra một phiên bản
        mới mà nội dung y hệt sẽ làm số phiên bản mất hết ý nghĩa.
    """
    added, modified, removed = changes

    if previous is None:
        return "v1.0.0"

    try:
        major, minor, patch = (int(x) for x in previous.lstrip("v").split("."))
    except (ValueError, AttributeError):
        return "v1.0.0"

    if added or removed:
        return f"v{major}.{minor + 1}.0"
    if modified:
        return f"v{major}.{minor}.{patch + 1}"
    return previous


def _connect() -> sqlite3.Connection:
    from core.paths import get_knowledge_db_path

    conn = sqlite3.connect(str(get_knowledge_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    conn.execute(_INDEX)
    return conn


def get_latest_snapshot(course: str) -> Optional[Snapshot]:
    try:
        conn = _connect()
    except Exception:
        return None
    try:
        row = conn.execute(
            "SELECT * FROM course_snapshots WHERE course = ? ORDER BY created_at DESC LIMIT 1",
            (course,),
        ).fetchone()
    except Exception:
        return None
    finally:
        conn.close()

    if row is None:
        return None
    return Snapshot(
        course=row["course"],
        version=row["version"],
        created_at=row["created_at"],
        commit_sha=row["commit_sha"] or "",
        note=row["note"] or "",
        digests=json.loads(row["digests_json"] or "{}"),
    )


def list_snapshots(course: str, limit: int = 20) -> List[Snapshot]:
    try:
        conn = _connect()
    except Exception:
        return []
    try:
        rows = conn.execute(
            "SELECT * FROM course_snapshots WHERE course = ? ORDER BY created_at DESC LIMIT ?",
            (course, limit),
        ).fetchall()
    except Exception:
        return []
    finally:
        conn.close()

    return [
        Snapshot(
            course=r["course"],
            version=r["version"],
            created_at=r["created_at"],
            commit_sha=r["commit_sha"] or "",
            note=r["note"] or "",
            digests=json.loads(r["digests_json"] or "{}"),
        )
        for r in rows
    ]


def record_snapshot(
    course: str, digests: Dict[str, str], version: str, commit_sha: str = "", note: str = ""
) -> Snapshot:
    snapshot = Snapshot(
        course=course,
        version=version,
        created_at=time.time(),
        commit_sha=commit_sha,
        note=note,
        digests=digests,
    )
    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO course_snapshots (course, version, created_at, commit_sha, note, digests_json) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                snapshot.course,
                snapshot.version,
                snapshot.created_at,
                snapshot.commit_sha,
                snapshot.note,
                json.dumps(snapshot.digests, ensure_ascii=False),
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return snapshot


def find_changed_since_approval(course: str, digests: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Các tài nguyên đã được giảng viên duyệt NHƯNG đã đổi nội dung kể từ đó.

    Đây là câu hỏi đắt nhất mà module này trả lời: không có nó, giảng viên phải mở
    từng file đọc lại mới biết bản mình duyệt còn nguyên hay không — với 20 buổi ×
    3 bài × 5 tài nguyên thì không ai làm.
    """
    try:
        from core.approvals import list_approvals
    except Exception:
        return []

    approvals = [a for a in list_approvals(course) if a.is_approved]
    if not approvals:
        return []

    # Ảnh chụp gần nhất TẠI HOẶC TRƯỚC thời điểm duyệt mới là bản mà giảng viên đã
    # nhìn thấy. So với ảnh chụp mới nhất là so nhầm mốc.
    history = list_snapshots(course, limit=50)
    stale: List[Dict[str, str]] = []
    seen = set()

    for approval in approvals:
        key = (approval.session_id, approval.lesson_id, approval.artifact)
        if key in seen:
            continue
        seen.add(key)

        baseline = next(
            (s for s in history if s.created_at <= approval.approved_at), None
        )
        if baseline is None:
            continue

        for rel_path, digest in digests.items():
            if approval.session_id and approval.session_id not in rel_path:
                continue
            if approval.lesson_id and approval.lesson_id not in rel_path:
                continue
            old_digest = baseline.digests.get(rel_path)
            if old_digest and old_digest != digest:
                stale.append(
                    {
                        "path": rel_path,
                        "reviewer": approval.reviewer,
                        "approved_at": approval.approved_at_iso,
                        "artifact": approval.artifact,
                    }
                )

    return stale


def snapshot_course(
    course: str,
    course_dir: str,
    note: str = "",
    write_changelog: bool = True,
) -> Dict[str, Any]:
    """
    Chụp trạng thái khoá học, so với lần trước và ghi nhật ký thay đổi.

    Returns:
        dict gồm version, changelog, danh sách tài nguyên đã đổi sau khi được duyệt,
        và đường dẫn file nhật ký (nếu có ghi).
    """
    digests = scan_course_digests(course_dir)
    if not digests:
        return {"version": None, "changelog": None, "stale_approvals": [], "changelog_path": None}

    previous = get_latest_snapshot(course)
    old_digests = previous.digests if previous else {}
    changes = compare_digests(old_digests, digests)
    added, modified, removed = changes

    version = next_version(previous.version if previous else None, changes)

    changelog = Changelog(
        course=course,
        from_version=previous.version if previous else "(chưa có)",
        to_version=version,
        added=added,
        modified=modified,
        removed=removed,
    )

    stale = find_changed_since_approval(course, digests)

    # Không có thay đổi thì không ghi thêm một ảnh chụp trùng lặp: lịch sử phiên bản
    # đầy những mốc y hệt nhau sẽ không tra cứu được.
    if previous is None or not changelog.is_empty:
        try:
            from core.evals.trend_store import current_commit_sha

            commit_sha = current_commit_sha()
        except Exception:
            commit_sha = ""
        record_snapshot(course, digests, version, commit_sha=commit_sha, note=note)

    changelog_path = None
    if write_changelog and not changelog.is_empty:
        try:
            target = Path(course_dir) / "CHANGELOG.md"
            target.write_text(changelog.to_markdown(), encoding="utf-8")
            changelog_path = str(target)
        except Exception as e:
            print(f"  [Version Warning] Không ghi được nhật ký thay đổi: {e}")

    return {
        "version": version,
        "changelog": changelog,
        "stale_approvals": stale,
        "changelog_path": changelog_path,
    }


def format_version_report(result: Dict[str, Any], course: str) -> str:
    """Tóm tắt phiên bản dạng văn bản để in cuối lượt chạy."""
    version = result.get("version")
    if not version:
        return ""

    changelog: Optional[Changelog] = result.get("changelog")
    lines = ["", f"====== 🏷️ Phiên bản học liệu — {course} ======"]
    lines.append(f"  Phiên bản: {version}")

    if changelog and not changelog.is_empty:
        lines.append(
            f"  Thay đổi : {len(changelog.added)} thêm, "
            f"{len(changelog.modified)} sửa, {len(changelog.removed)} gỡ "
            f"(so với {changelog.from_version})"
        )
        if result.get("changelog_path"):
            lines.append(f"  Nhật ký  : {result['changelog_path']}")
    else:
        lines.append("  Thay đổi : không có gì đổi so với lần trước")

    stale = result.get("stale_approvals") or []
    if stale:
        # Cảnh báo quan trọng nhất trong báo cáo này.
        lines.append("")
        lines.append(f"  ⚠️ {len(stale)} tài nguyên ĐÃ ĐỔI sau khi được duyệt:")
        for item in stale[:10]:
            lines.append(f"    - {item['path']} (duyệt bởi {item['reviewer']} lúc {item['approved_at']})")
        if len(stale) > 10:
            lines.append(f"    ... và {len(stale) - 10} tài nguyên khác")

    lines.append("=" * 46)
    lines.append("")
    return "\n".join(lines)


__all__ = [
    "TRACKED_SUFFIXES",
    "Snapshot",
    "Changelog",
    "scan_course_digests",
    "compare_digests",
    "next_version",
    "record_snapshot",
    "get_latest_snapshot",
    "list_snapshots",
    "find_changed_since_approval",
    "snapshot_course",
    "format_version_report",
]
