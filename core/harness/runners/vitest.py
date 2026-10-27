"""Chạy Vitest cho một dự án Node (starter hoặc đáp án mẫu) bằng workspace `node_modules` dùng chung.

Workspace khóa theo tập dependency: `<cache_root>/<khóa>/package.json` + `node_modules/`, `npm install`
một lần. Mỗi lần chạy chép dự án vào `<workspace>/runs/<id>/` (bỏ node_modules, .env...) để Node và Vite
tìm thấy `node_modules` của workspace ở thư mục cha, chạy `npx vitest run --reporter=json`, rồi xóa thư mục.
Không chạy và không ghi gì trong thư mục dự án gốc.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from pathlib import Path

from core.harness.runners import RunnerError, ToolUnavailable, tooling

NPM_INSTALL_TIMEOUT_S = 600
VITEST_TIMEOUT_S = 300
_MARKER = ".harness_installed"
_COPY_IGNORE = shutil.ignore_patterns("node_modules", ".git", ".env", "dist", "coverage", "result.json")


def _read_package(package_json: Path) -> dict:
    try:
        return json.loads(Path(package_json).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RunnerError(f"Không đọc được {package_json}: {exc}") from exc


def _deps(pkg: dict) -> dict:
    return {sec: dict(sorted((pkg.get(sec) or {}).items())) for sec in ("dependencies", "devDependencies")}


class NodeWorkspace:
    def __init__(self, cache_root: Path):
        self.cache_root = Path(cache_root)

    def key(self, package_json: Path) -> str:
        blob = json.dumps(_deps(_read_package(package_json)), sort_keys=True, separators=(",", ":"))
        return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]

    def prepare(self, package_json: Path) -> Path:
        """Thư mục workspace có `node_modules` cho tập dependency của `package_json`."""
        deps = _deps(_read_package(package_json))
        ws = self.cache_root / self.key(package_json)
        if (ws / _MARKER).is_file() and (ws / "node_modules").is_dir():
            return ws
        npm = tooling.which("npm")
        if not npm:
            raise ToolUnavailable("Không tìm thấy npm (cần Node.js để chạy Vitest)")
        # Hai lượt verify song song không được cùng npm install vào một thư mục.
        with tooling.file_lock(self.cache_root / f"{ws.name}.lock", timeout=NPM_INSTALL_TIMEOUT_S + 60):
            if (ws / _MARKER).is_file() and (ws / "node_modules").is_dir():
                return ws
            ws.mkdir(parents=True, exist_ok=True)
            (ws / "package.json").write_text(
                json.dumps({"name": "harness-node-workspace", "private": True, **deps}, indent=2), encoding="utf-8")
            code, out = tooling.run_command([npm, "install", "--no-audit", "--no-fund", "--loglevel=error"], ws,
                                            env=tooling.child_env(), timeout=NPM_INSTALL_TIMEOUT_S)
            if code != 0 or not (ws / "node_modules").is_dir():
                raise RunnerError(f"npm install thất bại (mã {code}): {out.strip()[-600:]}")
            (ws / _MARKER).write_text("ok", encoding="utf-8")
        return ws


def parse_report(data: dict) -> dict:
    passed = int(data.get("numPassedTests", 0))
    failed = int(data.get("numFailedTests", 0))
    total = int(data.get("numTotalTests", 0))
    failed_tests, suite_errors = [], []
    for suite in data.get("testResults", []):
        if suite.get("status") == "failed" and not suite.get("assertionResults"):
            name = Path(suite.get("name", "")).name
            suite_errors.append(f"{name}: {(suite.get('message') or '').strip()[:300]}")
        for t in suite.get("assertionResults", []):
            if t.get("status") == "failed":
                failed_tests.append(t.get("fullName") or t.get("title") or "")
    return {"passed": passed, "failed": failed, "total": total,
            "ok": total > 0 and passed == total and failed == 0 and not suite_errors,
            "failed_tests": failed_tests, "suite_errors": suite_errors}


def run_vitest(project: Path, workspace: Path, env: dict | None = None) -> dict:
    """`{passed, failed, total, ok, failed_tests, suite_errors}`; không có báo cáo JSON → total 0 kèm `error`."""
    npx = tooling.which("npx")
    if not npx:
        raise ToolUnavailable("Không tìm thấy npx (cần Node.js để chạy Vitest)")
    run_dir = Path(workspace) / "runs" / uuid.uuid4().hex[:10]
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = _run_in(project, run_dir, npx, env)
    finally:
        cleaned = tooling.rmtree(run_dir)
    if not cleaned:
        result["cleanup_warning"] = f"không xóa hết thư mục chạy tạm {run_dir}"
    return result


def _run_in(project: Path, run_dir: Path, npx: str, env: dict | None) -> dict:
    shutil.copytree(project, run_dir, ignore=_COPY_IGNORE)
    out = run_dir / "result.json"
    cmd = [npx, "vitest", "run", "--reporter=json", f"--outputFile={out}"]
    code, log = tooling.run_command(cmd, run_dir, env=tooling.child_env(env), timeout=VITEST_TIMEOUT_S)
    if not out.is_file():
        return {"passed": 0, "failed": 0, "total": 0, "ok": False, "failed_tests": [], "suite_errors": [],
                "error": log.strip()[-800:] or f"vitest thoát mã {code} mà không có báo cáo"}
    try:
        data = json.loads(out.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise RunnerError(f"Báo cáo JSON của Vitest hỏng: {exc}") from exc
    return parse_report(data)
