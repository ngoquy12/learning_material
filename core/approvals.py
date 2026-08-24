"""
core/approvals.py — Hồ sơ duyệt học liệu của giảng viên (E2).

Pipeline đã biết gắn nhãn "cần người rà lại" (PENDING_HUMAN_REVIEW, APPROVED_WITH_
SCOPE_WARNINGS, FAILED), nhưng nhãn đó chết ở đó: không có chỗ nào ghi nhận ai đã
rà, rà khi nào, kết luận ra sao. Hai hệ quả:

  1. Chạy lại pipeline ghi đè thẳng lên bản mà giảng viên đã sửa tay và duyệt —
     công rà soát mất trắng, và không ai biết cho tới khi mở file ra xem.
  2. Không xuất được hồ sơ "ai duyệt cái gì, khi nào" — thứ mà kiểm định chất
     lượng đào tạo (AUN-QA và kiểm định trong nước) bắt buộc phải có.

Module này lưu hồ sơ duyệt vào kho tri thức dùng chung và cung cấp phép tra cứu để
pipeline biết artifact nào KHÔNG được ghi đè.
"""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

_SCHEMA = """
CREATE TABLE IF NOT EXISTS artifact_approvals (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    course       TEXT NOT NULL DEFAULT '',
    session_id   TEXT NOT NULL DEFAULT '',
    lesson_id    TEXT NOT NULL DEFAULT '',
    artifact     TEXT NOT NULL,
    reviewer     TEXT NOT NULL,
    decision     TEXT NOT NULL DEFAULT 'APPROVED',
    note         TEXT DEFAULT '',
    approved_at  REAL NOT NULL
)
"""

_INDEX = """
CREATE INDEX IF NOT EXISTS idx_approval_target
ON artifact_approvals(course, session_id, lesson_id, artifact, approved_at)
"""

DECISION_APPROVED = "APPROVED"
DECISION_REJECTED = "REJECTED"


@dataclass(frozen=True)
class Approval:
    course: str
    session_id: str
    lesson_id: str
    artifact: str
    reviewer: str
    decision: str
    note: str
    approved_at: float

    @property
    def approved_at_iso(self) -> str:
        return datetime.fromtimestamp(self.approved_at, tz=timezone.utc).isoformat(timespec="seconds")

    @property
    def is_approved(self) -> bool:
        return self.decision == DECISION_APPROVED


def _connect() -> sqlite3.Connection:
    from core.paths import get_knowledge_db_path

    conn = sqlite3.connect(str(get_knowledge_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    conn.execute(_INDEX)
    return conn


def record_approval(
    artifact: str,
    reviewer: str,
    course: str = "",
    session_id: str = "",
    lesson_id: str = "",
    decision: str = DECISION_APPROVED,
    note: str = "",
) -> Approval:
    """
    Ghi một quyết định rà soát.

    Không ghi đè bản ghi cũ mà ghi THÊM: hồ sơ kiểm định cần thấy được cả lịch sử,
    kể cả trường hợp một artifact bị từ chối rồi sửa rồi duyệt lại.
    """
    if not artifact or not str(artifact).strip():
        raise ValueError("Thiếu tên artifact cần duyệt.")
    if not reviewer or not str(reviewer).strip():
        raise ValueError(
            "Thiếu tên người duyệt. Hồ sơ kiểm định không chấp nhận quyết định vô danh."
        )

    decision = (decision or DECISION_APPROVED).strip().upper()
    if decision not in (DECISION_APPROVED, DECISION_REJECTED):
        raise ValueError(f"Quyết định không hợp lệ: {decision!r}")

    approval = Approval(
        course=str(course or "").strip(),
        session_id=str(session_id or "").strip(),
        lesson_id=str(lesson_id or "").strip(),
        artifact=str(artifact).strip(),
        reviewer=str(reviewer).strip(),
        decision=decision,
        note=str(note or "").strip(),
        approved_at=time.time(),
    )

    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO artifact_approvals "
            "(course, session_id, lesson_id, artifact, reviewer, decision, note, approved_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                approval.course,
                approval.session_id,
                approval.lesson_id,
                approval.artifact,
                approval.reviewer,
                approval.decision,
                approval.note,
                approval.approved_at,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return approval


def get_latest_approval(
    artifact: str, course: str = "", session_id: str = "", lesson_id: str = ""
) -> Optional[Approval]:
    """Quyết định GẦN NHẤT cho một artifact, hoặc None nếu chưa ai rà."""
    try:
        conn = _connect()
    except Exception:
        return None

    try:
        row = conn.execute(
            "SELECT * FROM artifact_approvals "
            "WHERE course = ? AND session_id = ? AND lesson_id = ? AND artifact = ? "
            "ORDER BY approved_at DESC LIMIT 1",
            (
                str(course or "").strip(),
                str(session_id or "").strip(),
                str(lesson_id or "").strip(),
                str(artifact or "").strip(),
            ),
        ).fetchone()
    except Exception:
        return None
    finally:
        conn.close()

    if row is None:
        return None
    return Approval(
        course=row["course"],
        session_id=row["session_id"],
        lesson_id=row["lesson_id"],
        artifact=row["artifact"],
        reviewer=row["reviewer"],
        decision=row["decision"],
        note=row["note"] or "",
        approved_at=row["approved_at"],
    )


def is_locked_by_reviewer(
    artifact: str,
    course: str = "",
    session_id: str = "",
    lesson_id: str = "",
    force_rebuild: bool = False,
) -> bool:
    """
    Artifact này đã được giảng viên duyệt và KHÔNG được ghi đè?

    `force_rebuild` là lối thoát có chủ đích: người vận hành nói rõ họ muốn bỏ bản
    đã duyệt. Không có lối thoát này thì một artifact duyệt nhầm sẽ khoá vĩnh viễn.
    """
    if force_rebuild:
        return False
    latest = get_latest_approval(artifact, course, session_id, lesson_id)
    return bool(latest and latest.is_approved)


def list_approvals(course: str = "") -> List[Approval]:
    """Toàn bộ hồ sơ duyệt, mới nhất trước. Lọc theo khoá học nếu có."""
    try:
        conn = _connect()
    except Exception:
        return []

    try:
        if course:
            rows = conn.execute(
                "SELECT * FROM artifact_approvals WHERE course = ? ORDER BY approved_at DESC",
                (course.strip(),),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM artifact_approvals ORDER BY approved_at DESC"
            ).fetchall()
    except Exception:
        return []
    finally:
        conn.close()

    return [
        Approval(
            course=r["course"],
            session_id=r["session_id"],
            lesson_id=r["lesson_id"],
            artifact=r["artifact"],
            reviewer=r["reviewer"],
            decision=r["decision"],
            note=r["note"] or "",
            approved_at=r["approved_at"],
        )
        for r in rows
    ]


def export_approvals_csv(destination: str, course: str = "") -> int:
    """
    Xuất hồ sơ kiểm định ra CSV. Trả về số dòng đã ghi.

    Đây là đầu ra mà kiểm định chất lượng đào tạo yêu cầu: ai duyệt cái gì, khi nào,
    kết luận ra sao.
    """
    import csv
    from pathlib import Path

    rows = list_approvals(course)
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Khoá học", "Buổi", "Bài", "Tài nguyên", "Người duyệt", "Quyết định", "Ghi chú", "Thời điểm (UTC)"]
        )
        for a in rows:
            writer.writerow(
                [a.course, a.session_id, a.lesson_id, a.artifact, a.reviewer,
                 a.decision, a.note, a.approved_at_iso]
            )
    return len(rows)


__all__ = [
    "Approval",
    "DECISION_APPROVED",
    "DECISION_REJECTED",
    "record_approval",
    "get_latest_approval",
    "is_locked_by_reviewer",
    "list_approvals",
    "export_approvals_csv",
]
