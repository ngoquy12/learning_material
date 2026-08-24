"""
core/run_metrics.py — Sổ đo chi phí và hiệu quả cache cho MỘT lượt chạy sinh học liệu.

Bối cảnh: hệ thống đã ghi trace từng lượt gọi LLM ra JSONL (core/observability.py) và
đã đếm được cache theo agent (core/semantic_cache.py), nhưng KHÔNG nơi nào trả lời
được câu hỏi mà người vận hành thực sự hỏi sau mỗi lần chạy:

    "Sinh xong buổi này tốn bao nhiêu token, bao nhiêu lượt gọi, cache đỡ được mấy
     phần, và tiền chủ yếu đi vào khâu nào?"

Trace JSONL trả lời được nhưng phải tự đọc và tự cộng hàng nghìn dòng; còn thống kê
cache thì cộng dồn từ mọi lượt chạy trong 30 ngày qua chứ không phải lượt vừa rồi.

Module này gom số liệu của ĐÚNG lượt chạy hiện tại, cộng dồn tại hai chỗ thắt cổ chai
sẵn có (log_agent_call cho lượt gọi thật, cache_lookup cho lượt được cache phục vụ),
rồi in bảng tổng kết và ghi vào kho tri thức để so sánh giữa các lần chạy.

Nguyên tắc: đo đạc TUYỆT ĐỐI không được làm hỏng việc chính. Mọi hàm ở đây nuốt lỗi
và không bao giờ ném ra ngoài — một sổ đo hỏng không đáng để mất cả buổi sinh học liệu.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentMetrics:
    """Số liệu cộng dồn của một agent trong lượt chạy."""

    agent_name: str
    llm_calls: int = 0
    cache_hits: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration_seconds: float = 0.0

    @property
    def attempts(self) -> int:
        """Tổng số lần cần tới một phản hồi, dù lấy từ LLM hay từ cache."""
        return self.llm_calls + self.cache_hits

    @property
    def cache_hit_rate(self) -> float:
        return (self.cache_hits / self.attempts) if self.attempts else 0.0


class RunMetrics:
    """
    Sổ đo của một lượt chạy. An toàn với đa luồng vì 5 nhánh sản xuất chạy song song
    và cùng ghi vào đây.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._agents: Dict[str, AgentMetrics] = {}
        self._started_at: float = time.time()
        self._label: str = ""

    # ── Ghi nhận ────────────────────────────────────────────────────────────
    def start_run(self, label: str = "") -> None:
        with self._lock:
            self._agents.clear()
            self._started_at = time.time()
            self._label = label

    def record_llm_call(
        self,
        agent_name: str,
        tokens: Optional[Dict[str, int]] = None,
        duration_seconds: float = 0.0,
    ) -> None:
        """Một lượt gọi LLM THẬT (đã tốn tiền)."""
        tokens = tokens or {}
        with self._lock:
            m = self._agents.setdefault(agent_name or "Unknown", AgentMetrics(agent_name or "Unknown"))
            m.llm_calls += 1
            m.prompt_tokens += int(tokens.get("prompt_tokens", 0) or 0)
            m.completion_tokens += int(tokens.get("completion_tokens", 0) or 0)
            m.total_tokens += int(tokens.get("total_tokens", 0) or 0)
            m.duration_seconds += max(0.0, float(duration_seconds or 0.0))

    def record_cache_hit(self, agent_name: str) -> None:
        """Một lượt được cache phục vụ (KHÔNG tốn tiền)."""
        with self._lock:
            m = self._agents.setdefault(agent_name or "Unknown", AgentMetrics(agent_name or "Unknown"))
            m.cache_hits += 1

    # ── Đọc ─────────────────────────────────────────────────────────────────
    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            agents = sorted(self._agents.values(), key=lambda m: m.total_tokens, reverse=True)
            total_calls = sum(m.llm_calls for m in agents)
            total_hits = sum(m.cache_hits for m in agents)
            attempts = total_calls + total_hits
            return {
                "label": self._label,
                "elapsed_seconds": round(time.time() - self._started_at, 2),
                "llm_calls": total_calls,
                "cache_hits": total_hits,
                "cache_hit_rate": round(total_hits / attempts, 4) if attempts else 0.0,
                "prompt_tokens": sum(m.prompt_tokens for m in agents),
                "completion_tokens": sum(m.completion_tokens for m in agents),
                "total_tokens": sum(m.total_tokens for m in agents),
                "by_agent": [
                    {
                        "agent_name": m.agent_name,
                        "llm_calls": m.llm_calls,
                        "cache_hits": m.cache_hits,
                        "cache_hit_rate": round(m.cache_hit_rate, 4),
                        "total_tokens": m.total_tokens,
                        "duration_seconds": round(m.duration_seconds, 2),
                    }
                    for m in agents
                ],
            }

    def is_empty(self) -> bool:
        with self._lock:
            return not self._agents


# Sổ đo dùng chung cho tiến trình. Một lượt chạy CLI là một tiến trình.
_RUN_METRICS = RunMetrics()


def get_run_metrics() -> RunMetrics:
    return _RUN_METRICS


def start_run(label: str = "") -> None:
    try:
        _RUN_METRICS.start_run(label)
    except Exception:
        pass


def record_llm_call(agent_name: str, tokens: Optional[Dict[str, int]] = None, duration_seconds: float = 0.0) -> None:
    try:
        _RUN_METRICS.record_llm_call(agent_name, tokens, duration_seconds)
    except Exception:
        pass


def record_cache_hit(agent_name: str) -> None:
    try:
        _RUN_METRICS.record_cache_hit(agent_name)
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Báo cáo
# ─────────────────────────────────────────────────────────────────────────────

def format_run_report(snapshot: Optional[Dict[str, Any]] = None, top_n: int = 8) -> str:
    """Bảng tổng kết chi phí, dạng văn bản thuần để in ra cuối lượt chạy."""
    data = snapshot if snapshot is not None else _RUN_METRICS.snapshot()

    if not data.get("llm_calls") and not data.get("cache_hits"):
        return ""

    lines: List[str] = []
    label = f" — {data['label']}" if data.get("label") else ""
    lines.append("")
    lines.append("====== 📊 Chi phí lượt chạy" + label + " ======")
    lines.append(f"  Thời gian chạy       : {data['elapsed_seconds']:.0f}s")
    lines.append(f"  Lượt gọi LLM thật    : {data['llm_calls']}")
    lines.append(
        f"  Lượt cache phục vụ   : {data['cache_hits']} "
        f"({data['cache_hit_rate'] * 100:.1f}% tổng số lượt)"
    )
    lines.append(
        f"  Token                : {data['total_tokens']:,} "
        f"(vào {data['prompt_tokens']:,} / ra {data['completion_tokens']:,})"
    )

    by_agent = data.get("by_agent") or []
    if by_agent:
        lines.append("  Tốn nhiều token nhất:")
        for row in by_agent[:top_n]:
            lines.append(
                f"    {row['agent_name'][:34]:<34} "
                f"{row['total_tokens']:>9,} tokens  "
                f"{row['llm_calls']:>3} gọi  "
                f"{row['cache_hits']:>3} cache  "
                f"{row['duration_seconds']:>7.1f}s"
            )
        if len(by_agent) > top_n:
            lines.append(f"    ... và {len(by_agent) - top_n} agent khác")

    lines.append("=" * 46)
    lines.append("")
    return "\n".join(lines)


def persist_run_metrics(snapshot: Optional[Dict[str, Any]] = None) -> bool:
    """
    Ghi số liệu lượt chạy vào kho tri thức để so sánh giữa các lần.

    Không có bảng theo dõi xu hướng thì mỗi con số chỉ là một ảnh chụp rời rạc:
    không trả lời được "lần này có đắt hơn lần trước không".
    """
    data = snapshot if snapshot is not None else _RUN_METRICS.snapshot()
    if not data.get("llm_calls") and not data.get("cache_hits"):
        return False

    try:
        import json
        import sqlite3

        from core.paths import get_knowledge_db_path

        conn = sqlite3.connect(str(get_knowledge_db_path()))
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS run_cost_metrics (
                    id                INTEGER PRIMARY KEY AUTOINCREMENT,
                    recorded_at       REAL NOT NULL,
                    label             TEXT DEFAULT '',
                    elapsed_seconds   REAL DEFAULT 0,
                    llm_calls         INTEGER DEFAULT 0,
                    cache_hits        INTEGER DEFAULT 0,
                    cache_hit_rate    REAL DEFAULT 0,
                    prompt_tokens     INTEGER DEFAULT 0,
                    completion_tokens INTEGER DEFAULT 0,
                    total_tokens      INTEGER DEFAULT 0,
                    by_agent_json     TEXT DEFAULT '[]'
                )
                """
            )
            conn.execute(
                "INSERT INTO run_cost_metrics (recorded_at, label, elapsed_seconds, llm_calls, "
                "cache_hits, cache_hit_rate, prompt_tokens, completion_tokens, total_tokens, by_agent_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    time.time(),
                    data.get("label", ""),
                    data.get("elapsed_seconds", 0),
                    data.get("llm_calls", 0),
                    data.get("cache_hits", 0),
                    data.get("cache_hit_rate", 0),
                    data.get("prompt_tokens", 0),
                    data.get("completion_tokens", 0),
                    data.get("total_tokens", 0),
                    json.dumps(data.get("by_agent", []), ensure_ascii=False),
                ),
            )
            conn.commit()
            return True
        finally:
            conn.close()
    except Exception as e:
        print(f"  [Run Metrics Warning] Không ghi được số liệu lượt chạy: {e}")
        return False


__all__ = [
    "AgentMetrics",
    "RunMetrics",
    "get_run_metrics",
    "start_run",
    "record_llm_call",
    "record_cache_hit",
    "format_run_report",
    "persist_run_metrics",
]
