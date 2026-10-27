"""Cổng slide pptx: kiểm tĩnh bộ slide đã dựng, lint slides.json cùng thư mục, đo chữ tràn bằng PowerPoint (render)."""
from __future__ import annotations

import shutil
import sys
import tempfile
import time
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.gates import GATES
from core.harness.gates._skill_loader import REPO, load_skill_script
from core.harness.options import VerifyOptions

GATE = "slide_pptx"
RENDER_ROOT = REPO / "storage" / "harness_cache" / "render"


def _check_deck():
    return load_skill_script("slide_deck", "check_deck")


def _deck_lint():
    return load_skill_script("slide_deck", "deck_lint")


def _add(result: GateResult, severity: str, messages) -> None:
    result.findings += [Finding(severity, GATE, m) for m in messages]


def _lint_json(result: GateResult, path: Path) -> None:
    slides_json = path.parent / "slides.json"
    if not slides_json.exists():
        return
    lint = _deck_lint()
    try:
        errors, warnings = lint.lint_slides(lint.load_slides(slides_json))
    except Exception as exc:  # noqa: BLE001
        result.findings.append(Finding("error", GATE, f"Không đọc được slides.json: {exc}", "slides.json"))
        return
    for m in errors:
        result.findings.append(Finding("error", GATE, m, "slides.json"))
    for m in warnings:
        result.findings.append(Finding("warning", GATE, m, "slides.json"))
    result.detail["slides_json"] = True


def _render(result: GateResult, path: Path) -> None:
    if sys.platform != "win32":
        result.skipped_reason = "Đo bằng PowerPoint chỉ chạy trên Windows"
        return
    deck = _check_deck()
    out_dir = None
    try:
        RENDER_ROOT.mkdir(parents=True, exist_ok=True)
        out_dir = Path(tempfile.mkdtemp(prefix="deck_", dir=RENDER_ROOT))
        probe = deck.render_with_powerpoint(path, out_dir)
    except Exception as exc:  # noqa: BLE001
        probe = {"status": "FAILED", "reason": str(exc)}
    if probe.get("status") != "OK":
        if out_dir is not None:
            shutil.rmtree(out_dir, ignore_errors=True)
        result.skipped_reason = f"Không đo được bằng PowerPoint: {probe.get('reason', probe.get('status'))}"
        return
    measured = deck.measured_checks(probe)
    _add(result, "error", measured.get("errors", []))
    _add(result, "warning", measured.get("warnings", []))
    result.detail["render_dir"] = str(out_dir)


def check_slide_pptx(path: Path, opts: VerifyOptions) -> GateResult:
    start = time.perf_counter()
    path = Path(path)
    result = GateResult(kind="slide_pptx", path=str(path), gate=GATE)
    try:
        static = _check_deck().static_checks(path)
    except Exception as exc:  # noqa: BLE001
        result.findings.append(Finding("error", GATE, f"Không mở được tệp pptx: {exc}"))
        result.duration_s = time.perf_counter() - start
        return result
    result.detail["slides"] = static["slides"]
    _add(result, "error", static["errors"])
    _add(result, "warning", static["warnings"])
    _add(result, "warning", static.get("estimates", []))
    _lint_json(result, path)
    if opts.render:
        _render(result, path)
    result.duration_s = time.perf_counter() - start
    return result


GATES["slide_pptx"] = check_slide_pptx
