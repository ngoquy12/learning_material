"""Mô hình kết quả kiểm chứng: Finding, GateResult, Report."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Literal

Severity = Literal["error", "warning", "info"]
UNKNOWN_KIND = "unknown"


@dataclass(frozen=True)
class Finding:
    severity: Severity
    gate: str
    message: str
    location: str = ""

    def to_dict(self) -> dict:
        return {"severity": self.severity, "gate": self.gate,
                "message": self.message, "location": self.location}


@dataclass
class GateResult:
    kind: str
    path: str
    gate: str
    findings: list[Finding] = field(default_factory=list)
    skipped_reason: str = ""
    duration_s: float = 0.0
    detail: dict = field(default_factory=dict)

    @property
    def status(self) -> str:
        if any(f.severity == "error" for f in self.findings):
            return "fail"
        if self.kind == UNKNOWN_KIND:
            return "unknown"  # tệp không nhận diện được: chỉ liệt kê, không tính là đạt
        if self.skipped_reason:
            return "skipped"
        return "pass"

    def to_dict(self) -> dict:
        return {"kind": self.kind, "path": self.path, "gate": self.gate,
                "status": self.status, "skipped_reason": self.skipped_reason,
                "duration_s": self.duration_s, "detail": self.detail,
                "findings": [f.to_dict() for f in self.findings]}


@dataclass
class Report:
    target: str
    results: list[GateResult]
    started_at: str

    def counts(self) -> dict[str, int]:
        c = {"pass": 0, "fail": 0, "skipped": 0, "unknown": 0}
        for r in self.results:
            c[r.status] += 1
        return c

    @property
    def exit_code(self) -> int:
        c = self.counts()
        if c["fail"]:
            return 1
        if c["skipped"]:
            return 2
        return 0

    def to_dict(self) -> dict:
        return {"target": self.target, "started_at": self.started_at,
                "exit_code": self.exit_code, "counts": self.counts(),
                "results": [r.to_dict() for r in self.results]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, default=str)

    def to_markdown(self) -> str:
        c = self.counts()
        lines = [f"# Báo cáo kiểm chứng: {self.target}", "",
                 f"Thời điểm bắt đầu: {self.started_at}", "",
                 "| Trạng thái | Số cổng |", "| --- | --- |",
                 f"| fail | {c['fail']} |", f"| skipped | {c['skipped']} |",
                 f"| pass | {c['pass']} |", f"| unknown | {c['unknown']} |", ""]
        order = {"fail": 0, "skipped": 1, "pass": 2, "unknown": 3}
        for r in sorted(self.results, key=lambda r: order[r.status]):
            lines.append(f"## [{r.status}] {r.kind}: {r.path} ({r.gate})")
            if r.skipped_reason:
                lines.append(f"Bỏ qua: {r.skipped_reason}")
            for f in r.findings:
                loc = f" ({f.location})" if f.location else ""
                lines.append(f"- [{f.severity}] {f.message}{loc}")
            lines.append("")
        return "\n".join(lines)
