"""
core/review_dashboard.py — Trang rà soát học liệu cho giảng viên (E1).

Pipeline gắn nhãn rất cẩn thận: APPROVED, APPROVED_WITH_SCOPE_WARNINGS,
PENDING_HUMAN_REVIEW, FAILED, SKIPPED (kèm lý do). Nhưng toàn bộ nhãn đó chỉ tồn tại
trong console và trong checkpoint nhị phân. Sau một lượt chạy 20 buổi học, console
đã cuộn qua hàng nghìn dòng và không ai còn dựng lại được câu hỏi đơn giản nhất:

    "Bài nào cần tôi rà lại trước khi phát cho sinh viên?"

Trang này gom trạng thái mọi artifact của một khoá học vào một chỗ, nổi bật đúng
những mục cần người can thiệp, kèm liên kết mở thẳng file và phản hồi cuối cùng của
reviewer.

LƯU Ý PHẠM VI: đây là trang QUẢN TRỊ NỘI BỘ, không phải học liệu. Nó không dùng và
không được phép ảnh hưởng tới bộ template bài đọc/bài thực hành — vùng thiết kế đã
đóng băng.
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.artifact_status import (
    ArtifactStatus,
    base_status,
    is_failed,
    is_skipped,
    needs_human_review,
    normalize,
    reason_of,
)

# Thứ tự ưu tiên hiển thị: thứ cần người can thiệp phải nằm trên cùng, luôn luôn.
# Người rà soát mở trang này để tìm việc phải làm, không phải để ngắm thứ đã xong.
_PRIORITY = {
    "failed": 0,
    "needs_review": 1,
    "pending": 2,
    "approved": 3,
    "skipped": 4,
}

_CATEGORY_LABEL = {
    "failed": "Hỏng — cần xử lý",
    "needs_review": "Cần người rà lại",
    "pending": "Chưa hoàn tất",
    "approved": "Đạt chuẩn",
    "skipped": "Không áp dụng",
}


def categorize(status: Any) -> str:
    """Xếp một trạng thái artifact vào nhóm hiển thị."""
    if is_failed(status):
        return "failed"
    if needs_human_review(status):
        return "needs_review"
    if is_skipped(status):
        return "skipped"
    normalized = normalize(status)
    if normalized in (ArtifactStatus.APPROVED, ArtifactStatus.APPROVED_WITH_WARNINGS,
                      ArtifactStatus.PUBLISHED):
        return "approved"
    return "pending"


@dataclass
class ArtifactRow:
    session_id: str
    lesson_id: str
    title: str
    artifact: str
    status: str
    category: str
    reason: str = ""
    feedback: str = ""
    file_path: str = ""
    approved_by: str = ""
    approved_at: str = ""


@dataclass
class DashboardData:
    course: str
    rows: List[ArtifactRow] = field(default_factory=list)

    def counts(self) -> Dict[str, int]:
        result = {k: 0 for k in _CATEGORY_LABEL}
        for row in self.rows:
            result[row.category] = result.get(row.category, 0) + 1
        return result

    @property
    def needs_attention(self) -> int:
        c = self.counts()
        return c.get("failed", 0) + c.get("needs_review", 0) + c.get("pending", 0)


def _last_feedback(state: Dict[str, Any], artifact: str) -> str:
    """Phản hồi reviewer gần nhất liên quan tới artifact này."""
    logs = state.get("review_logs") or []
    if not isinstance(logs, list):
        return ""
    for log in reversed(logs):
        if not isinstance(log, dict):
            continue
        if log.get("artifact") and log["artifact"] != artifact:
            continue
        source = str(log.get("source", ""))
        if log.get("artifact") == artifact or artifact.lower() in source.lower():
            return str(log.get("feedback", ""))[:400]
    # Không có log gắn đúng artifact thì lấy phản hồi cuối cùng bất kỳ.
    for log in reversed(logs):
        if isinstance(log, dict) and log.get("feedback"):
            return str(log["feedback"])[:400]
    return ""


def build_dashboard_data(
    course: str,
    states: List[Dict[str, Any]],
    file_paths: Optional[Dict[str, Dict[str, str]]] = None,
) -> DashboardData:
    """
    Dựng dữ liệu trang rà soát từ danh sách state của các bài học.

    Args:
        course: Tên khoá học.
        states: Mỗi phần tử là AgentState cuối cùng của một lesson/session.
        file_paths: Tuỳ chọn — {"<session>|<lesson>": {"<artifact>": "<đường dẫn>"}}.
    """
    file_paths = file_paths or {}
    rows: List[ArtifactRow] = []

    for state in states:
        if not isinstance(state, dict):
            continue
        session_id = str(state.get("session_id", ""))
        lesson_id = str(state.get("lesson_id", ""))
        ssot = state.get("core_ssot") if isinstance(state.get("core_ssot"), dict) else {}
        title = str((ssot or {}).get("session_title", "")) or lesson_id or session_id
        key = f"{session_id}|{lesson_id}"
        paths_for_unit = file_paths.get(key, {})

        statuses = state.get("artifacts_status") or {}
        if not isinstance(statuses, dict):
            continue

        scope_audits = state.get("scope_audits") or {}

        for artifact, status in sorted(statuses.items()):
            category = categorize(status)
            reason = reason_of(status)

            feedback = ""
            if category in ("failed", "needs_review", "pending"):
                feedback = _last_feedback(state, artifact)
            audit = scope_audits.get(artifact) if isinstance(scope_audits, dict) else None
            if isinstance(audit, dict) and audit.get("violations"):
                violated = ", ".join(str(v) for v in audit["violations"])
                feedback = (f"Dùng khái niệm chưa dạy: {violated}. " + feedback).strip()

            approved_by = approved_at = ""
            try:
                from core.approvals import get_latest_approval

                latest = get_latest_approval(artifact, course, session_id, lesson_id)
                if latest and latest.is_approved:
                    approved_by = latest.reviewer
                    approved_at = latest.approved_at_iso
            except Exception:
                pass

            rows.append(
                ArtifactRow(
                    session_id=session_id,
                    lesson_id=lesson_id,
                    title=title,
                    artifact=artifact,
                    status=base_status(status) or str(status),
                    category=category,
                    reason=reason,
                    feedback=feedback,
                    file_path=paths_for_unit.get(artifact, ""),
                    approved_by=approved_by,
                    approved_at=approved_at,
                )
            )

    rows.sort(key=lambda r: (_PRIORITY.get(r.category, 9), r.session_id, r.lesson_id, r.artifact))
    return DashboardData(course=course, rows=rows)


# ─────────────────────────────────────────────────────────────────────────────
# Kết xuất HTML
# ─────────────────────────────────────────────────────────────────────────────

_CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin:0; padding:32px; font-family: system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
       background:#f8fafc; color:#0f172a; }
h1 { font-size:22px; margin:0 0 4px; }
.sub { color:#64748b; font-size:13px; margin-bottom:24px; }
.cards { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; }
.card { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:14px 18px; min-width:150px; }
.card .n { font-size:26px; font-weight:700; line-height:1.1; }
.card .l { font-size:12px; color:#64748b; margin-top:2px; }
.card.failed .n { color:#b91c1c; }
.card.needs_review .n { color:#b45309; }
.card.pending .n { color:#0369a1; }
.card.approved .n { color:#15803d; }
.card.skipped .n { color:#64748b; }
.wrap { overflow-x:auto; background:#fff; border:1px solid #e2e8f0; border-radius:10px; }
table { border-collapse:collapse; width:100%; font-size:13px; min-width:900px; }
th { text-align:left; padding:10px 12px; background:#f1f5f9; font-weight:600;
     border-bottom:1px solid #e2e8f0; white-space:nowrap; }
td { padding:10px 12px; border-bottom:1px solid #f1f5f9; vertical-align:top; }
tr:last-child td { border-bottom:none; }
.badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px;
         font-weight:600; white-space:nowrap; }
.badge.failed { background:#fee2e2; color:#b91c1c; }
.badge.needs_review { background:#fef3c7; color:#b45309; }
.badge.pending { background:#e0f2fe; color:#0369a1; }
.badge.approved { background:#dcfce7; color:#15803d; }
.badge.skipped { background:#f1f5f9; color:#64748b; }
.fb { color:#475569; font-size:12px; max-width:520px; }
.mono { font-family:ui-monospace,"JetBrains Mono",Menlo,monospace; font-size:12px; }
a { color:#0369a1; }
.empty { padding:40px; text-align:center; color:#64748b; }
footer { margin-top:20px; font-size:12px; color:#94a3b8; }
"""


def render_dashboard_html(data: DashboardData) -> str:
    """Kết xuất trang rà soát thành HTML tĩnh, không phụ thuộc mạng."""
    e = html.escape
    counts = data.counts()

    cards = "".join(
        f'<div class="card {cat}"><div class="n">{counts.get(cat, 0)}</div>'
        f'<div class="l">{e(label)}</div></div>'
        for cat, label in sorted(_CATEGORY_LABEL.items(), key=lambda kv: _PRIORITY.get(kv[0], 9))
    )

    if data.rows:
        body = []
        for r in data.rows:
            status_text = r.status + (f" ({r.reason})" if r.reason else "")
            link = (
                f'<a href="{e(r.file_path)}" target="_blank">mở file</a>'
                if r.file_path
                else '<span style="color:#cbd5e1">—</span>'
            )
            approved = (
                f"{e(r.approved_by)}<br><span class='mono'>{e(r.approved_at)}</span>"
                if r.approved_by
                else '<span style="color:#cbd5e1">chưa rà</span>'
            )
            body.append(
                "<tr>"
                f"<td class='mono'>{e(r.session_id)}</td>"
                f"<td class='mono'>{e(r.lesson_id)}</td>"
                f"<td>{e(r.title)}</td>"
                f"<td class='mono'>{e(r.artifact)}</td>"
                f"<td><span class='badge {r.category}'>{e(_CATEGORY_LABEL.get(r.category, r.category))}</span>"
                f"<br><span class='mono' style='color:#64748b'>{e(status_text)}</span></td>"
                f"<td class='fb'>{e(r.feedback)}</td>"
                f"<td>{link}</td>"
                f"<td>{approved}</td>"
                "</tr>"
            )
        table = (
            "<div class='wrap'><table><thead><tr>"
            "<th>Buổi</th><th>Bài</th><th>Tiêu đề</th><th>Tài nguyên</th>"
            "<th>Trạng thái</th><th>Phản hồi kiểm định</th><th>File</th><th>Người duyệt</th>"
            "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>"
        )
    else:
        table = "<div class='wrap'><div class='empty'>Chưa có dữ liệu artifact nào.</div></div>"

    attention = data.needs_attention
    headline = (
        f"{attention} tài nguyên cần bạn xử lý"
        if attention
        else "Không có tài nguyên nào cần xử lý"
    )

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Rà soát học liệu — {e(data.course)}</title>
<style>{_CSS}</style>
</head>
<body>
<h1>Rà soát học liệu — {e(data.course)}</h1>
<div class="sub">{e(headline)}. Mục cần can thiệp được xếp lên đầu bảng.</div>
<div class="cards">{cards}</div>
{table}
<footer>
Duyệt một tài nguyên:
<span class="mono">python main.py --approve "&lt;buổi&gt;/&lt;bài&gt;/&lt;tài nguyên&gt;" --reviewer "&lt;tên&gt;"</span>
<br>Tài nguyên đã duyệt sẽ không bị ghi đè ở lần chạy sau, trừ khi dùng <span class="mono">--force-rebuild</span>.
</footer>
</body>
</html>"""


def write_dashboard(
    course: str,
    states: List[Dict[str, Any]],
    destination: Path,
    file_paths: Optional[Dict[str, Dict[str, str]]] = None,
) -> Optional[Path]:
    """Dựng và ghi trang rà soát. Trả về đường dẫn đã ghi, hoặc None nếu lỗi."""
    try:
        data = build_dashboard_data(course, states, file_paths)
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_dashboard_html(data), encoding="utf-8")
        return destination
    except Exception as e:
        print(f"  [Review Dashboard Warning] Không dựng được trang rà soát: {e}")
        return None


def dashboard_data_as_json(data: DashboardData) -> str:
    """Bản JSON của cùng dữ liệu, để công cụ khác dùng lại."""
    return json.dumps(
        {
            "course": data.course,
            "counts": data.counts(),
            "rows": [vars(r) for r in data.rows],
        },
        ensure_ascii=False,
        indent=2,
    )


__all__ = [
    "ArtifactRow",
    "DashboardData",
    "categorize",
    "build_dashboard_data",
    "render_dashboard_html",
    "write_dashboard",
    "dashboard_data_as_json",
]
