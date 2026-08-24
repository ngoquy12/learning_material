"""
core/evals/trend_store.py — Lưu và so sánh điểm chất lượng sư phạm theo thời gian (G3).

PedagogicalBenchmarkEngine đã chấm được điểm một bài học, nhưng điểm đó chỉ tồn tại
trong một lần chạy rồi biến mất. Hệ quả: không ai trả lời được câu hỏi quan trọng
nhất về chất lượng của một hệ thống sinh nội dung bằng LLM —

    "Bản refactor hôm nay có làm học liệu tệ đi so với tuần trước không?"

Một điểm 82/100 tự nó chẳng nói lên gì. 82 sau khi tuần trước là 91 là một sự cố;
82 sau khi tuần trước là 74 là một tiến bộ. Không có đường cơ sở thì mọi con số đều
vô nghĩa, và chất lượng có thể trôi dần mà không ai nhận ra cho tới khi giảng viên
phàn nàn.

Module này lưu từng lần chấm kèm mã commit, rồi so lần mới nhất với lần trước để
phát hiện tụt điểm.
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

_SCHEMA = """
CREATE TABLE IF NOT EXISTS pedagogy_trend (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at   REAL NOT NULL,
    commit_sha    TEXT DEFAULT '',
    subject       TEXT NOT NULL,
    tech_stack    TEXT DEFAULT '',
    overall_score REAL NOT NULL,
    passed        INTEGER NOT NULL DEFAULT 0,
    metrics_json  TEXT DEFAULT '{}'
)
"""

_INDEX = """
CREATE INDEX IF NOT EXISTS idx_trend_subject
ON pedagogy_trend(subject, recorded_at)
"""

# Ngưỡng coi là TỤT ĐIỂM. Không đặt bằng 0 vì bộ chấm có vài tiêu chí phụ thuộc
# heuristic văn bản, dao động một vài điểm giữa các lần là bình thường; báo động vì
# nhiễu sẽ khiến người ta bỏ qua cả những lần tụt thật.
REGRESSION_THRESHOLD = 5.0


@dataclass(frozen=True)
class TrendPoint:
    recorded_at: float
    commit_sha: str
    subject: str
    tech_stack: str
    overall_score: float
    passed: bool
    metrics: Dict[str, Any]


@dataclass(frozen=True)
class Regression:
    subject: str
    previous_score: float
    current_score: float
    previous_commit: str
    current_commit: str

    @property
    def delta(self) -> float:
        return self.current_score - self.previous_score

    def message(self) -> str:
        return (
            f"'{self.subject}' tụt {abs(self.delta):.1f} điểm "
            f"({self.previous_score:.1f} -> {self.current_score:.1f}), "
            f"so với commit {self.previous_commit[:8] or '(không rõ)'}"
        )


def current_commit_sha() -> str:
    """Mã commit hiện tại; chuỗi rỗng nếu không nằm trong kho git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def _connect() -> sqlite3.Connection:
    from core.paths import get_knowledge_db_path

    conn = sqlite3.connect(str(get_knowledge_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    conn.execute(_INDEX)
    return conn


def record_scorecard(scorecard: Any, subject: str, commit_sha: Optional[str] = None) -> TrendPoint:
    """Lưu một lần chấm. `scorecard` là PedagogicalScorecard hoặc dict tương đương."""
    data = scorecard.to_dict() if hasattr(scorecard, "to_dict") else dict(scorecard)
    sha = commit_sha if commit_sha is not None else current_commit_sha()

    point = TrendPoint(
        recorded_at=time.time(),
        commit_sha=sha,
        subject=subject,
        tech_stack=str(data.get("tech_stack", "")),
        overall_score=float(data.get("overall_score", 0.0)),
        passed=bool(data.get("passed", False)),
        metrics=data.get("metrics", {}) or {},
    )

    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO pedagogy_trend "
            "(recorded_at, commit_sha, subject, tech_stack, overall_score, passed, metrics_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                point.recorded_at,
                point.commit_sha,
                point.subject,
                point.tech_stack,
                point.overall_score,
                int(point.passed),
                json.dumps(point.metrics, ensure_ascii=False),
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return point


def get_history(subject: str, limit: int = 20) -> List[TrendPoint]:
    """Lịch sử chấm điểm của một đối tượng, mới nhất trước."""
    try:
        conn = _connect()
    except Exception:
        return []

    try:
        rows = conn.execute(
            "SELECT * FROM pedagogy_trend WHERE subject = ? ORDER BY recorded_at DESC LIMIT ?",
            (subject, limit),
        ).fetchall()
    except Exception:
        return []
    finally:
        conn.close()

    return [
        TrendPoint(
            recorded_at=r["recorded_at"],
            commit_sha=r["commit_sha"] or "",
            subject=r["subject"],
            tech_stack=r["tech_stack"] or "",
            overall_score=r["overall_score"],
            passed=bool(r["passed"]),
            metrics=json.loads(r["metrics_json"] or "{}"),
        )
        for r in rows
    ]


def detect_regressions(
    subjects: Optional[List[str]] = None, threshold: float = REGRESSION_THRESHOLD
) -> List[Regression]:
    """
    So lần chấm mới nhất với lần liền trước, trả về các đối tượng bị tụt điểm.

    Cố ý so với lần LIỀN TRƯỚC chứ không phải điểm cao nhất từng đạt: mục tiêu là
    phát hiện thay đổi vừa gây hại, không phải kể lể một lần tụt đã biết và đã chấp
    nhận từ trước.
    """
    if subjects is None:
        try:
            conn = _connect()
            try:
                subjects = [r["subject"] for r in conn.execute(
                    "SELECT DISTINCT subject FROM pedagogy_trend"
                )]
            finally:
                conn.close()
        except Exception:
            return []

    regressions: List[Regression] = []
    for subject in subjects:
        history = get_history(subject, limit=2)
        if len(history) < 2:
            continue
        current, previous = history[0], history[1]
        if previous.overall_score - current.overall_score >= threshold:
            regressions.append(
                Regression(
                    subject=subject,
                    previous_score=previous.overall_score,
                    current_score=current.overall_score,
                    previous_commit=previous.commit_sha,
                    current_commit=current.commit_sha,
                )
            )
    return regressions


def format_trend_report(subjects: List[str]) -> str:
    """Bảng xu hướng dạng văn bản, dùng cho log CI."""
    lines = ["", "====== 📈 Xu hướng chất lượng sư phạm ======"]

    for subject in subjects:
        history = get_history(subject, limit=5)
        if not history:
            lines.append(f"  {subject}: chưa có dữ liệu")
            continue

        current = history[0]
        trail = " <- ".join(f"{p.overall_score:.0f}" for p in history)
        verdict = "ĐẠT" if current.passed else "CHƯA ĐẠT"
        lines.append(f"  {subject[:38]:<38} {current.overall_score:5.1f}  {verdict:<9} [{trail}]")

    regressions = detect_regressions(subjects)
    if regressions:
        lines.append("")
        lines.append("  ⚠️ TỤT ĐIỂM so với lần chấm trước:")
        for r in regressions:
            lines.append(f"    - {r.message()}")

    lines.append("=" * 44)
    lines.append("")
    return "\n".join(lines)


__all__ = [
    "REGRESSION_THRESHOLD",
    "TrendPoint",
    "Regression",
    "current_commit_sha",
    "record_scorecard",
    "get_history",
    "detect_regressions",
    "format_trend_report",
]
