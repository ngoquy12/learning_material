"""Gộp checkpoint cũ với cấu hình của lần chạy hiện tại."""

from __future__ import annotations

from typing import Any, Dict

# Các trường mô tả YÊU CẦU của lần chạy này, không phải kết quả đã sinh. Lấy từ
# checkpoint thì lần chạy `--parts quiz` sau lần `--parts html` sẽ thừa hưởng
# requested_parts cũ và bỏ qua quiz; phạm vi kiến thức mới cũng bị bỏ.
RUN_CONFIG_FIELDS = (
    "requested_parts",
    "pm_input",
    "full_curriculum",
    "allowed_scope",
    "forbidden_scope",
    "scope_source",
    "session_kind",
    "chosen_domain",
    "session_domain",
    "technology_stack",
    "time_reference",
    "pm_approved",
    "force_rebuild",
)


def merge_resume_state(cached: Dict[str, Any], fresh: Dict[str, Any]) -> Dict[str, Any]:
    """Giữ kết quả đã sinh trong `cached`, nhưng cấu hình chạy lấy từ `fresh`."""
    merged = dict(cached)
    for key in RUN_CONFIG_FIELDS:
        if key in fresh:
            merged[key] = fresh[key]
    # Chạy lại phần không được yêu cầu lần trước: trạng thái SKIPPED cũ không được
    # chặn phần giờ được yêu cầu.
    cached_status = dict(cached.get("artifacts_status") or {})
    fresh_status = fresh.get("artifacts_status") or {}
    for part, value in fresh_status.items():
        old = str(cached_status.get(part, ""))
        if part not in cached_status or old.lower().startswith("skipped"):
            cached_status[part] = value
    merged["artifacts_status"] = cached_status
    return merged
