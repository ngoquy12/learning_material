"""
core/learning_analytics.py — Đưa dữ liệu người học thật quay ngược về kho kinh nghiệm (F2).

Đây là mảnh ghép khép vòng tự cải tiến của hệ thống. Trước nó, vòng phản hồi chỉ có
MỘT chiều và chỉ nghe được chính mình:

    LLM sinh → reviewer chấm → lessons_learned → LLM sinh lần sau

Reviewer là một mô hình ngôn ngữ đọc học liệu, nên nó chỉ phát hiện được lỗi nhìn
thấy trên trang giấy: sai cú pháp, lệch phạm vi, sai định dạng. Có một loại vấn đề
nó KHÔNG BAO GIỜ thấy được, vì chỉ người học mới biết:

    - Bài đọc viết đúng hết nhưng 70% sinh viên bỏ giữa chừng.
    - Một câu quiz mà cả lớp cùng sai — hoặc đề mơ hồ, hoặc bài đọc chưa dạy tới nó.
    - Một bài thiết kế cho 10 phút nhưng thực tế người học mất 40 phút.

Module này đọc phát biểu xAPI do gói học liệu phát về (F1), rút ra tín hiệu học tập,
rồi ghi thành luật trong kho kinh nghiệm để lần sinh sau tránh lặp lại.

NGUYÊN TẮC THẬN TRỌNG: mọi ngưỡng ở đây đều đòi hỏi một cỡ mẫu tối thiểu. Sinh ra
một luật từ hai người học rồi bắt mọi bài sau tuân theo là biến nhiễu thống kê thành
quy định — tệ hơn hẳn việc không có luật nào.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# Cỡ mẫu tối thiểu để một tín hiệu được coi là có thật.
# Dưới ngưỡng này, dữ liệu chỉ đủ để báo cáo cho người xem, KHÔNG đủ để sinh ra luật
# ràng buộc mọi lần sinh học liệu về sau.
MIN_COHORT_SIZE = 15

# Tỷ lệ bỏ giữa chừng bị coi là bất thường. Một phần người học rời trang giữa chừng
# là bình thường ở mọi khoá học; chỉ khi quá nửa bỏ dở thì mới là vấn đề của bài đọc.
ABANDONMENT_THRESHOLD = 0.5

# Tỷ lệ trả lời sai bị coi là bất thường. 60% cả lớp cùng sai một câu thì vấn đề
# nằm ở câu hỏi hoặc ở bài đọc, không phải ở người học.
ERROR_RATE_THRESHOLD = 0.6

# Bội số thời lượng so với thiết kế. Gấp đôi thời gian dự kiến nghĩa là bài đọc khó
# hơn nhiều so với ý đồ thiết kế.
DURATION_OVERRUN_RATIO = 2.0


@dataclass
class ActivityStats:
    """Số liệu tổng hợp của một hoạt động (một bài học hoặc một câu hỏi)."""

    activity_id: str
    activity_name: str = ""
    initialized: int = 0
    completed: int = 0
    durations_seconds: List[float] = field(default_factory=list)
    answered_total: int = 0
    answered_wrong: int = 0
    learners: set = field(default_factory=set)

    @property
    def cohort_size(self) -> int:
        return len(self.learners)

    @property
    def abandonment_rate(self) -> Optional[float]:
        if not self.initialized:
            return None
        return 1.0 - (min(self.completed, self.initialized) / self.initialized)

    @property
    def error_rate(self) -> Optional[float]:
        if not self.answered_total:
            return None
        return self.answered_wrong / self.answered_total

    @property
    def median_duration(self) -> Optional[float]:
        if not self.durations_seconds:
            return None
        ordered = sorted(self.durations_seconds)
        mid = len(ordered) // 2
        if len(ordered) % 2:
            return ordered[mid]
        return (ordered[mid - 1] + ordered[mid]) / 2.0


@dataclass(frozen=True)
class LearningSignal:
    """Một tín hiệu rút ra từ hành vi người học."""

    kind: str            # "abandonment" | "hard_question" | "duration_overrun"
    activity_id: str
    activity_name: str
    cohort_size: int
    value: float
    rule_text: str
    severity: str = "MAJOR"

    def summary(self) -> str:
        return f"[{self.kind}] {self.activity_name or self.activity_id}: {self.rule_text}"


def _parse_iso_duration(text: Any) -> Optional[float]:
    """
    Đọc thời lượng ISO-8601 dạng 'PT123S' mà bộ phát xAPI sinh ra.

    Cố ý chỉ nhận đúng dạng mình phát ra, thay vì cài một bộ đọc ISO-8601 đầy đủ:
    phát biểu từ nguồn khác có thể dùng dạng phức tạp hơn, và đoán sai đơn vị thời
    gian sẽ tạo ra tín hiệu "quá giờ" hoàn toàn bịa.
    """
    if not isinstance(text, str) or not text.startswith("PT") or not text.endswith("S"):
        return None
    try:
        return float(text[2:-1])
    except ValueError:
        return None


def _actor_key(statement: Dict[str, Any]) -> str:
    actor = statement.get("actor") or {}
    if not isinstance(actor, dict):
        return ""
    return str(actor.get("mbox") or (actor.get("account") or {}).get("name") or actor.get("name") or "")


def aggregate_statements(statements: Iterable[Dict[str, Any]]) -> Dict[str, ActivityStats]:
    """Gom phát biểu xAPI thành số liệu theo từng hoạt động."""
    stats: Dict[str, ActivityStats] = {}

    for statement in statements:
        if not isinstance(statement, dict):
            continue

        obj = statement.get("object") or {}
        activity_id = str(obj.get("id", "")).strip()
        if not activity_id:
            continue

        definition = obj.get("definition") or {}
        names = definition.get("name") or {}
        activity_name = ""
        if isinstance(names, dict) and names:
            activity_name = str(next(iter(names.values()), ""))

        entry = stats.setdefault(activity_id, ActivityStats(activity_id, activity_name))
        if activity_name and not entry.activity_name:
            entry.activity_name = activity_name

        actor = _actor_key(statement)
        if actor:
            entry.learners.add(actor)

        verb_id = str((statement.get("verb") or {}).get("id", ""))
        result = statement.get("result") or {}

        if verb_id.endswith("/initialized"):
            entry.initialized += 1
        elif verb_id.endswith("/completed"):
            entry.completed += 1
        elif verb_id.endswith("/answered"):
            entry.answered_total += 1
            if result.get("success") is False:
                entry.answered_wrong += 1

        duration = _parse_iso_duration(result.get("duration"))
        if duration is not None and verb_id.endswith(("/terminated", "/completed")):
            entry.durations_seconds.append(duration)

    return stats


def derive_signals(
    stats: Dict[str, ActivityStats],
    expected_minutes: float = 10.0,
    min_cohort: int = MIN_COHORT_SIZE,
) -> List[LearningSignal]:
    """
    Rút tín hiệu học tập từ số liệu tổng hợp.

    Args:
        expected_minutes: Thời lượng thiết kế của một bài đọc. Mặc định 10 phút theo
            triết lý micro-learning ghi trong AGENTS.md.
        min_cohort: Cỡ mẫu tối thiểu. Hạ ngưỡng này để thử nghiệm thì được, nhưng
            đừng hạ khi chạy thật: một luật sinh ra từ vài người học sẽ ràng buộc
            mọi bài sinh về sau bằng nhiễu thống kê.
    """
    signals: List[LearningSignal] = []

    for entry in stats.values():
        if entry.cohort_size < min_cohort:
            continue

        label = entry.activity_name or entry.activity_id

        abandonment = entry.abandonment_rate
        if abandonment is not None and abandonment >= ABANDONMENT_THRESHOLD:
            signals.append(
                LearningSignal(
                    kind="abandonment",
                    activity_id=entry.activity_id,
                    activity_name=entry.activity_name,
                    cohort_size=entry.cohort_size,
                    value=abandonment,
                    severity="CRITICAL",
                    rule_text=(
                        f"Bài đọc '{label}' bị {abandonment * 100:.0f}% người học "
                        f"({entry.cohort_size} người) bỏ giữa chừng. Khi soạn lại bài "
                        f"cùng chủ đề, hãy rút ngắn phần lý thuyết mở đầu, đưa ví dụ "
                        f"chạy được lên sớm hơn, và chia nhỏ các đoạn văn dài."
                    ),
                )
            )

        error_rate = entry.error_rate
        if error_rate is not None and error_rate >= ERROR_RATE_THRESHOLD:
            signals.append(
                LearningSignal(
                    kind="hard_question",
                    activity_id=entry.activity_id,
                    activity_name=entry.activity_name,
                    cohort_size=entry.cohort_size,
                    value=error_rate,
                    severity="CRITICAL",
                    rule_text=(
                        f"Câu hỏi '{label}' bị {error_rate * 100:.0f}% người học "
                        f"({entry.cohort_size} người) trả lời sai. Tỷ lệ sai ở mức này "
                        f"thường do đề mơ hồ hoặc do bài đọc chưa dạy tới kiến thức "
                        f"cần thiết — hãy kiểm tra lại phạm vi kiến thức trước khi ra "
                        f"câu hỏi tương tự."
                    ),
                )
            )

        median = entry.median_duration
        if median is not None and expected_minutes > 0:
            ratio = median / (expected_minutes * 60.0)
            if ratio >= DURATION_OVERRUN_RATIO:
                signals.append(
                    LearningSignal(
                        kind="duration_overrun",
                        activity_id=entry.activity_id,
                        activity_name=entry.activity_name,
                        cohort_size=entry.cohort_size,
                        value=ratio,
                        severity="MAJOR",
                        rule_text=(
                            f"Bài đọc '{label}' mất trung vị {median / 60:.0f} phút, gấp "
                            f"{ratio:.1f} lần thời lượng thiết kế {expected_minutes:.0f} "
                            f"phút. Bài cùng chủ đề nên giảm số khái niệm mới trên mỗi "
                            f"mục hoặc tách thành hai bài."
                        ),
                    )
                )

    return signals


def load_statements(source: str) -> List[Dict[str, Any]]:
    """
    Nạp phát biểu xAPI từ file JSON hoặc JSONL do LRS xuất ra.

    Cố ý đọc từ FILE thay vì gọi thẳng LRS: mỗi LRS có một cách xác thực và phân
    trang riêng, và buộc module này biết hết chúng sẽ khiến nó không kiểm thử được
    và hỏng mỗi lần đổi nhà cung cấp. Xuất dữ liệu ra file là thao tác mà LRS nào
    cũng làm được.
    """
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file phát biểu xAPI: {source}")

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # Thử đọc TOÀN VĂN như một tài liệu JSON trước.
    #
    # Cố ý không phân biệt dạng bằng ký tự đầu tiên: file JSONL cũng bắt đầu bằng
    # '{', nên nhận dạng theo ký tự đầu sẽ đẩy JSONL vào nhánh JSON-đơn rồi chết với
    # lỗi "Extra data". Để bộ phân tích tự phán quyết là cách duy nhất chắc chắn.
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = None

    if isinstance(data, list):
        return [s for s in data if isinstance(s, dict)]
    if isinstance(data, dict):
        # Nhiều LRS xuất ra dạng {"statements": [...], "more": "..."}.
        if isinstance(data.get("statements"), list):
            return [s for s in data["statements"] if isinstance(s, dict)]
        return [data]

    # Dạng JSONL: mỗi dòng một phát biểu.
    statements = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                statements.append(parsed)
        except json.JSONDecodeError:
            continue
    return statements


def store_signals_as_memories(
    signals: List[LearningSignal], tech_stack: str = "*"
) -> int:
    """
    Ghi tín hiệu học tập vào kho kinh nghiệm để lần sinh sau đọc được.

    Trả về số luật MỚI đã ghi (luật trùng bị bỏ qua bởi chính store_memory).
    """
    if not signals:
        return 0

    from agents.knowledge_memory_agent import store_memory

    stored = 0
    for signal in signals:
        created = store_memory(
            rule_text=signal.rule_text,
            tech_stack=tech_stack,
            # Dùng chung từ vựng phân loại sẵn có thay vì thêm loại mới: đây vẫn là
            # lỗi sư phạm, chỉ khác ở chỗ người phát hiện là người học chứ không
            # phải reviewer.
            error_category="pedagogical_error",
            severity=signal.severity,
            scope="all",
            source_lesson=signal.activity_name or signal.activity_id,
            source_agent=f"Learning_Analytics::{signal.kind}",
        )
        if created:
            stored += 1
    return stored


def format_analytics_report(
    stats: Dict[str, ActivityStats],
    signals: List[LearningSignal],
    min_cohort: int = MIN_COHORT_SIZE,
) -> str:
    """Báo cáo dạng văn bản, nói rõ cả phần dữ liệu CHƯA đủ để kết luận."""
    lines = ["", "====== 🎓 Tín hiệu từ dữ liệu người học ======"]

    if not stats:
        lines.append("  Không có phát biểu xAPI nào.")
        lines.append("=" * 44)
        return "\n".join(lines)

    enough = [s for s in stats.values() if s.cohort_size >= min_cohort]
    thin = [s for s in stats.values() if s.cohort_size < min_cohort]

    lines.append(f"  Hoạt động có dữ liệu   : {len(stats)}")
    lines.append(f"  Đủ cỡ mẫu (>= {min_cohort})    : {len(enough)}")

    if thin:
        # Nói rõ phần chưa kết luận được, thay vì im lặng bỏ qua. Im lặng khiến
        # người đọc tưởng những bài đó không có vấn đề gì.
        lines.append(
            f"  Chưa đủ cỡ mẫu         : {len(thin)} "
            f"(có dữ liệu nhưng chưa đủ để kết luận)"
        )

    if signals:
        lines.append("")
        lines.append(f"  Phát hiện {len(signals)} vấn đề:")
        for s in signals:
            lines.append(f"    - {s.summary()[:150]}")
    else:
        lines.append("")
        lines.append("  Không phát hiện vấn đề nào ở các hoạt động đủ cỡ mẫu.")

    lines.append("=" * 44)
    lines.append("")
    return "\n".join(lines)


def ingest_xapi_export(
    source: str,
    tech_stack: str = "*",
    expected_minutes: float = 10.0,
    min_cohort: int = MIN_COHORT_SIZE,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Toàn bộ vòng: nạp phát biểu -> gom số liệu -> rút tín hiệu -> ghi kho kinh nghiệm.

    `dry_run` cho phép xem hệ thống sẽ rút ra luật gì TRƯỚC khi ghi. Luật trong kho
    kinh nghiệm ảnh hưởng tới mọi lần sinh về sau, nên xem trước là bước đáng có.
    """
    statements = load_statements(source)
    stats = aggregate_statements(statements)
    signals = derive_signals(stats, expected_minutes=expected_minutes, min_cohort=min_cohort)

    stored = 0
    if signals and not dry_run:
        stored = store_signals_as_memories(signals, tech_stack=tech_stack)

    return {
        "statements": len(statements),
        "activities": len(stats),
        "signals": signals,
        "stored_rules": stored,
        "report": format_analytics_report(stats, signals, min_cohort),
    }


__all__ = [
    "MIN_COHORT_SIZE",
    "ABANDONMENT_THRESHOLD",
    "ERROR_RATE_THRESHOLD",
    "DURATION_OVERRUN_RATIO",
    "ActivityStats",
    "LearningSignal",
    "aggregate_statements",
    "derive_signals",
    "load_statements",
    "store_signals_as_memories",
    "format_analytics_report",
    "ingest_xapi_export",
]
