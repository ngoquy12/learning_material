"""Bộ chạy thật (Vitest, MySQL tạm, trình duyệt) và phần runtime của cổng exercise, slide_html.

Mọi test ở đây giả lập subprocess/Playwright; không cần Node, mysqld hay Chrome.
Riêng test cuối đánh dấu integration chạy thật trên dữ liệu môn đã duyệt.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.harness.gates import exercise as exercise_gate
from core.harness.gates import slide_html as slide_gate
from core.harness.gates.exercise import check_exercise
from core.harness.gates.slide_html import check_slide_html
from core.harness.options import VerifyOptions
from core.harness.runners import RunnerError, ToolUnavailable, browser, mysql_sandbox, tooling, vitest

RUNTIME = VerifyOptions(runtime=True)


def errors(r):
    return [f.message for f in r.findings if f.severity == "error"]


# --- tooling ---------------------------------------------------------------

def test_free_port_never_3306(monkeypatch):
    ports = iter([3306, 3306, 45123])

    class FakeSocket:
        def __init__(self, *a, **k):
            self.port = next(ports)

        def bind(self, addr):
            pass

        def getsockname(self):
            return ("127.0.0.1", self.port)

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            self.close()

    monkeypatch.setattr(tooling.socket, "socket", FakeSocket)
    assert tooling.free_port() == 45123


def test_free_port_excludes_3306_even_if_not_listed(monkeypatch):
    ports = iter([3306, 5000, 41000])

    class FakeSocket:
        def __init__(self, *a, **k):
            self.port = next(ports)

        def bind(self, addr):
            pass

        def getsockname(self):
            return ("127.0.0.1", self.port)

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

    monkeypatch.setattr(tooling.socket, "socket", FakeSocket)
    assert tooling.free_port(exclude={5000}) == 41000


def test_find_mysqld_glob(monkeypatch, tmp_path):
    exe = tmp_path / "MySQL" / "MySQL Server 8.0" / "bin" / "mysqld.exe"
    exe.parent.mkdir(parents=True)
    exe.write_text("")
    monkeypatch.setattr(tooling.shutil, "which", lambda name: None)
    monkeypatch.setattr(tooling, "MYSQLD_GLOBS", [str(tmp_path / "MySQL" / "MySQL Server *" / "bin" / "mysqld.exe")])
    assert tooling.find_mysqld() == str(exe)


def test_find_chrome_none(monkeypatch):
    monkeypatch.setattr(tooling, "CHROME_PATHS", [])
    assert tooling.find_chrome() is None


# --- NodeWorkspace / run_vitest -------------------------------------------

def _pkg(path: Path, deps: dict, dev: dict) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / "package.json").write_text(json.dumps({"name": "x", "dependencies": deps, "devDependencies": dev}),
                                       encoding="utf-8")
    return path / "package.json"


def test_workspace_key_ignores_order_and_installs_once(monkeypatch, tmp_path):
    calls = []

    def fake_run(cmd, cwd, env=None, timeout=None):
        calls.append(cmd)
        (Path(cwd) / "node_modules").mkdir(exist_ok=True)
        return 0, ""

    monkeypatch.setattr(tooling, "which", lambda name: name)
    monkeypatch.setattr(tooling, "run_command", fake_run)
    a = _pkg(tmp_path / "a", {"express": "4.21.2", "mysql2": "3.11.5"}, {"vitest": "3.1.4"})
    b = _pkg(tmp_path / "b", {"mysql2": "3.11.5", "express": "4.21.2"}, {"vitest": "3.1.4"})
    ws = vitest.NodeWorkspace(tmp_path / "cache")
    assert ws.key(a) == ws.key(b)
    wa = ws.prepare(a)
    wb = ws.prepare(b)
    assert wa == wb
    assert (wa / "node_modules").is_dir()
    assert len(calls) == 1
    assert "install" in calls[0]


def test_workspace_different_deps_different_key(tmp_path):
    a = _pkg(tmp_path / "a", {"react": "18.3.1"}, {"vitest": "3.1.4"})
    b = _pkg(tmp_path / "b", {"react": "18.3.0"}, {"vitest": "3.1.4"})
    ws = vitest.NodeWorkspace(tmp_path / "cache")
    assert ws.key(a) != ws.key(b)


def test_workspace_install_failure_raises(monkeypatch, tmp_path):
    monkeypatch.setattr(tooling, "which", lambda name: name)
    monkeypatch.setattr(tooling, "run_command", lambda *a, **k: (1, "npm ERR! network"))
    a = _pkg(tmp_path / "a", {"react": "18.3.1"}, {})
    with pytest.raises(RunnerError):
        vitest.NodeWorkspace(tmp_path / "cache").prepare(a)


def test_workspace_without_npm_is_tool_unavailable(monkeypatch, tmp_path):
    monkeypatch.setattr(tooling, "which", lambda name: None)
    a = _pkg(tmp_path / "a", {"react": "18.3.1"}, {})
    with pytest.raises(ToolUnavailable):
        vitest.NodeWorkspace(tmp_path / "cache").prepare(a)


VITEST_JSON = {
    "numPassedTests": 7, "numFailedTests": 3, "numTotalTests": 10, "success": False,
    "testResults": [
        {"name": "/x/tests/a.test.js", "status": "failed", "message": "",
         "assertionResults": [{"status": "failed", "fullName": "GET /products trả 200", "title": "trả 200"}]},
        {"name": "/x/tests/b.test.js", "status": "failed", "message": "Cannot find module './db'",
         "assertionResults": []},
    ],
}


def test_run_vitest_parses_json(monkeypatch, tmp_path):
    project = tmp_path / "proj"
    _pkg(project, {}, {"vitest": "3.1.4"})
    (project / "node_modules").mkdir()
    (project / "node_modules" / "junk.js").write_text("x")
    workspace = tmp_path / "ws"
    workspace.mkdir()
    seen = {}

    def fake_run(cmd, cwd, env=None, timeout=None):
        seen["cwd"] = Path(cwd)
        seen["env"] = env
        seen["timeout"] = timeout
        assert not (Path(cwd) / "node_modules").exists()
        out = next(a for a in cmd if a.startswith("--outputFile=")).split("=", 1)[1]
        Path(out).write_text(json.dumps(VITEST_JSON), encoding="utf-8")
        return 1, ""

    monkeypatch.setattr(tooling, "which", lambda name: name)
    monkeypatch.setattr(tooling, "run_command", fake_run)
    r = vitest.run_vitest(project, workspace, env={"DB_PORT": "40000"})
    assert {k: r[k] for k in ("passed", "failed", "total", "ok")} == {"passed": 7, "failed": 3, "total": 10, "ok": False}
    assert r["failed_tests"] == ["GET /products trả 200"]
    assert r["suite_errors"] and "Cannot find module" in r["suite_errors"][0]
    assert seen["cwd"].parent.parent == workspace
    assert seen["env"]["DB_PORT"] == "40000"
    assert seen["timeout"] == vitest.VITEST_TIMEOUT_S
    assert not seen["cwd"].exists(), "thư mục chạy tạm phải được xóa"
    assert (project / "node_modules" / "junk.js").exists(), "không được đụng vào dự án gốc"


def test_run_vitest_without_report_is_zero_tests(monkeypatch, tmp_path):
    project = tmp_path / "proj"
    _pkg(project, {}, {"vitest": "3.1.4"})
    monkeypatch.setattr(tooling, "which", lambda name: name)
    monkeypatch.setattr(tooling, "run_command", lambda *a, **k: (1, "SyntaxError: Unexpected token"))
    r = vitest.run_vitest(project, tmp_path / "ws")
    assert r["total"] == 0 and r["ok"] is False
    assert "SyntaxError" in r["error"]


def test_run_command_timeout_raises(tmp_path):
    import sys
    with pytest.raises(RunnerError):
        tooling.run_command([sys.executable, "-c", "import time; time.sleep(30)"], cwd=tmp_path, timeout=1)


def test_child_env_strips_db_and_secrets(monkeypatch):
    monkeypatch.setenv("DB_PORT", "3306")
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setenv("GITHUB_TOKEN", "t")
    monkeypatch.setenv("MY_SECRET", "s")
    monkeypatch.setenv("HARNESS_PLAIN", "ok")
    env = tooling.child_env({"DB_PORT": "45000"})
    assert env["DB_PORT"] == "45000"
    assert "GEMINI_API_KEY" not in env and "GITHUB_TOKEN" not in env and "MY_SECRET" not in env
    assert env["HARNESS_PLAIN"] == "ok"


def test_rmtree_reports_leftover(monkeypatch, tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    monkeypatch.setattr(tooling.shutil, "rmtree", lambda *a, **k: None)
    monkeypatch.setattr(tooling.time, "sleep", lambda s: None)
    assert tooling.rmtree(d) is False
    monkeypatch.undo()
    assert tooling.rmtree(d) is True


def test_file_lock_is_exclusive(tmp_path):
    lock = tmp_path / "x.lock"
    with tooling.file_lock(lock):
        assert lock.exists()
        with pytest.raises(RunnerError):
            with tooling.file_lock(lock, timeout=0):
                pass
    assert not lock.exists()


def test_run_command_kills_on_interrupt(monkeypatch, tmp_path):
    killed = []

    class P:
        pid = 1

        def __init__(self, *a, **k):
            pass

        def wait(self, timeout=None):
            raise KeyboardInterrupt

    monkeypatch.setattr(tooling.subprocess, "Popen", P)
    monkeypatch.setattr(tooling, "kill_tree", lambda proc: killed.append(proc))
    with pytest.raises(KeyboardInterrupt):
        tooling.run_command(["x"], tmp_path, timeout=5)
    assert killed


# --- MySQL sandbox ---------------------------------------------------------

def test_mysql_sandbox_unavailable(monkeypatch):
    monkeypatch.setattr(tooling, "find_mysqld", lambda: None)
    with pytest.raises(ToolUnavailable):
        with mysql_sandbox.MySQLSandbox():
            pass


def test_mysql_sandbox_args_and_cleanup(monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setattr(tooling, "find_mysqld", lambda: "mysqld")
    monkeypatch.setattr(tooling, "free_port", lambda exclude=frozenset({3306}): 45555)
    init_cmds, started = [], {}

    def fake_run(cmd, cwd, env=None, timeout=None):
        init_cmds.append(cmd)
        return 0, ""

    class FakeProc:
        pid = 1

        def __init__(self, cmd, **kw):
            started["cmd"] = cmd
            started["env"] = kw.get("env")
            log = next(a for a in cmd if a.startswith("--log-error=")).split("=", 1)[1]
            Path(log).write_text("mysqld: ready for connections. Version: '8.0'  socket: ''  port: 45555", encoding="utf-8")

        def poll(self):
            return None

    killed = []
    monkeypatch.setattr(tooling, "run_command", fake_run)
    monkeypatch.setattr(mysql_sandbox.subprocess, "Popen", FakeProc)
    monkeypatch.setattr(tooling, "kill_tree", lambda proc: killed.append(proc))
    sb = mysql_sandbox.MySQLSandbox(run_root=tmp_path / "runs")
    with sb as db:
        assert db == {"host": "127.0.0.1", "port": 45555, "user": "root", "password": ""}
        datadir = sb.datadir
        assert datadir.exists()
    assert "--initialize-insecure" in init_cmds[0]
    assert init_cmds[0][1] == "--no-defaults"
    cmd = started["cmd"]
    assert "--bind-address=127.0.0.1" in cmd and "--port=45555" in cmd
    assert not any("3306" in a for a in cmd)
    env = started["env"]
    assert env is not None and "GEMINI_API_KEY" not in env
    assert killed
    assert not sb.root.exists()


def _sandbox_env(monkeypatch, proc_cls):
    killed = []
    monkeypatch.setattr(tooling, "find_mysqld", lambda: "mysqld")
    monkeypatch.setattr(tooling, "free_port", lambda exclude=frozenset({3306}): 45556)
    monkeypatch.setattr(tooling, "run_command", lambda *a, **k: (0, ""))
    monkeypatch.setattr(mysql_sandbox.subprocess, "Popen", proc_cls)
    monkeypatch.setattr(tooling, "kill_tree", lambda proc: killed.append(proc))
    monkeypatch.setattr(mysql_sandbox.time, "sleep", lambda s: None)
    return killed


def test_mysql_sandbox_process_exits_cleans_up(monkeypatch, tmp_path):
    class Dead:
        pid = 1

        def __init__(self, cmd, **kw):
            pass

        def poll(self):
            return 1

    killed = _sandbox_env(monkeypatch, Dead)
    sb = mysql_sandbox.MySQLSandbox(run_root=tmp_path / "runs")
    with pytest.raises(RunnerError):
        with sb:
            pass
    assert killed and not sb.root.exists()


def test_mysql_sandbox_readiness_timeout_cleans_up(monkeypatch, tmp_path):
    class Silent:
        pid = 1

        def __init__(self, cmd, **kw):
            pass

        def poll(self):
            return None

    killed = _sandbox_env(monkeypatch, Silent)
    monkeypatch.setattr(mysql_sandbox, "START_TIMEOUT_S", 0)
    sb = mysql_sandbox.MySQLSandbox(run_root=tmp_path / "runs")
    with pytest.raises(RunnerError):
        with sb:
            pass
    assert killed and not sb.root.exists()


# --- browser ---------------------------------------------------------------

class FakePage:
    def __init__(self, evaluate, wait_fn=None):
        self._evaluate = evaluate
        self._wait_fn = wait_fn

    def on(self, event, fn):
        pass

    def goto(self, url):
        pass

    def wait_for_timeout(self, ms):
        pass

    def evaluate(self, js, *args):
        return self._evaluate(js, *args)

    def wait_for_function(self, js, timeout=None):
        if self._wait_fn:
            self._wait_fn()

    def screenshot(self, path):
        pass

    def close(self):
        pass


def fake_playwright(monkeypatch, page_factory):
    class Browser:
        def new_page(self, **kw):
            return page_factory(kw.get("viewport"))

        def close(self):
            pass

    class Ctx:
        def __enter__(self):
            return object()

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(browser, "_sync_playwright", lambda: Ctx)
    monkeypatch.setattr(browser, "launch_browser", lambda p: Browser())


def test_run_tests_html_without_report_is_runner_error(monkeypatch, tmp_path):
    fake_playwright(monkeypatch, lambda vp: FakePage(lambda js, *a: False))
    with pytest.raises(RunnerError):
        browser.run_tests_html(tmp_path / "tests.html")


def test_run_tests_html_timeout_is_runner_error(monkeypatch, tmp_path):
    def never():
        raise TimeoutError("Timeout 30000ms exceeded")
    fake_playwright(monkeypatch, lambda vp: FakePage(lambda js, *a: True, never))
    with pytest.raises(RunnerError):
        browser.run_tests_html(tmp_path / "tests.html")


def test_run_tests_html_report_throws_is_runner_error(monkeypatch, tmp_path):
    def ev(js, *a):
        if "typeof" in js:
            return True
        raise RuntimeError("Error: script.js is broken")
    fake_playwright(monkeypatch, lambda vp: FakePage(ev))
    with pytest.raises(RunnerError):
        browser.run_tests_html(tmp_path / "tests.html")


def test_run_tests_html_results(monkeypatch, tmp_path):
    data = {"passed": 1, "total": 2, "done": True,
            "results": [{"name": "a", "ok": True}, {"name": "b", "ok": False, "msg": "x"}]}

    def ev(js, *a):
        if "typeof" in js:
            return True
        if "__results" in js:
            return data
        return None
    fake_playwright(monkeypatch, lambda vp: FakePage(ev))
    r = browser.run_tests_html(tmp_path / "tests.html")
    assert (r["passed"], r["total"], r["ok"], r["failed_tests"]) == (1, 2, False, ["b"])


def test_measure_slides_records_worst_overflow(monkeypatch, tmp_path):
    state = {"slide": 0, "clicked": False}

    def make(vp):
        h = vp["height"]

        def ev(js, *a):
            if js.startswith("document.querySelectorAll('.slide').length"):
                return 2
            if js == browser.SMALL_FONT_JS:
                return {"18": 10}
            if js.startswith("typeof go"):
                return True
            if js.startswith("go("):
                state["slide"] = int(js[3:-1])
                state["clicked"] = False
                return None
            if js == browser.CLICKABLE_JS:
                return [0] if state["slide"] == 1 else []
            if "click()" in js:
                state["clicked"] = True
                return None
            if js.startswith("!!"):
                return True
            if js == browser.MEASURE_JS:
                extra = 40 if (state["slide"] == 1 and state["clicked"] and h == 720) else 0
                return {"sh": h + extra, "ch": h, "sw": 100, "cw": 100, "dw": 100, "iw": 100}
            return None
        return FakePage(ev)

    fake_playwright(monkeypatch, make)
    m = browser.measure_slides(tmp_path / "slides.html")
    assert m["slides"] == 2 and m["has_go"]
    assert m["slide_overflow"] == [{"slide": 2, "viewport": "1280x720", "over_px": 40, "state": "sau khi bấm nút 0"}]
    assert m["horizontal_overflow"] == [] and m["console_errors"] == []


def test_launch_browser_falls_back_to_system_chrome(monkeypatch):
    calls = []

    class Chromium:
        def launch(self, **kw):
            calls.append(kw)
            if "executable_path" not in kw:
                raise RuntimeError("Executable doesn't exist")
            return "browser"

    class P:
        chromium = Chromium()

    monkeypatch.setattr(tooling, "find_chrome", lambda: "C:/chrome.exe")
    assert browser.launch_browser(P()) == "browser"
    assert calls[-1]["executable_path"] == "C:/chrome.exe"


def test_launch_browser_no_chrome_is_tool_unavailable(monkeypatch):
    class Chromium:
        def launch(self, **kw):
            raise RuntimeError("Executable doesn't exist")

    class P:
        chromium = Chromium()

    monkeypatch.setattr(tooling, "find_chrome", lambda: None)
    with pytest.raises(ToolUnavailable):
        browser.launch_browser(P())


def test_check_slides_script_reuses_browser_constants():
    from core.harness.gates._skill_loader import load_skill_script
    mod = load_skill_script("slide_html", "check_slides_html")
    assert mod.MEASURE_JS is browser.MEASURE_JS


# --- cổng exercise (runtime) -----------------------------------------------

def make_exercise(tmp_path, with_db=False, vitest_dep=True) -> Path:
    from tests.harness.test_gate_exercise import de_bai
    base = tmp_path / "Bai tap"
    ex = base / "1_co_ban_1_demo"
    sol = base / "tai_lieu_giang_vien" / "dap_an_mau" / "bai_1"
    for proj in (ex / "starter", sol):
        _pkg(proj, {"express": "4.21.2"}, {"vitest": "3.1.4"} if vitest_dep else {})
        if with_db:
            (proj / "db").mkdir()
            (proj / "db" / "schema.sql").write_text("CREATE TABLE t (id INT);", encoding="utf-8")
    (ex / "de_bai_bai_tap.md").write_text(de_bai(), encoding="utf-8")
    (ex / "tieu_chi_cham_diem_ai.md").write_text("tiêu chí", encoding="utf-8")
    (base / "tai_lieu_giang_vien" / "huong_dan_bai_1.md").write_text("hd", encoding="utf-8")
    return ex


def fake_runner(monkeypatch, solution, starter, seen=None):
    def run(proj, db=None):
        if seen is not None:
            seen.append((Path(proj), db))
        r = solution if "dap_an_mau" in Path(proj).parts else starter
        if isinstance(r, Exception):
            raise r
        return dict(r)
    monkeypatch.setattr(exercise_gate, "run_project", run)


def res(passed, total):
    return {"passed": passed, "failed": total - passed, "total": total, "ok": total > 0 and passed == total,
            "runner": "vitest", "suite_errors": [], "failed_tests": []}


def test_runtime_ok(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, res(10, 10), res(3, 10))
    r = check_exercise(ex, RUNTIME)
    assert errors(r) == [], errors(r)
    assert r.status == "pass"
    assert r.detail["runtime"]["solution"]["passed"] == 10
    assert r.detail["runtime"]["starter"]["total"] == 10


def test_runtime_starter_passes_all(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, res(10, 10), res(10, 10))
    r = check_exercise(ex, RUNTIME)
    assert any("starter đã đạt hết" in m for m in errors(r))


def test_runtime_starter_crash_zero_tests(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, res(10, 10), res(0, 0))
    r = check_exercise(ex, RUNTIME)
    assert any("starter" in m.lower() and "0 test" in m for m in errors(r))


def test_runtime_solution_not_full(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, res(9, 10), res(3, 10))
    r = check_exercise(ex, RUNTIME)
    assert any("Đáp án mẫu" in m and "9/10" in m for m in errors(r))


def test_runtime_tool_unavailable_is_skipped(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, ToolUnavailable("Không tìm thấy npm"), ToolUnavailable("Không tìm thấy npm"))
    r = check_exercise(ex, RUNTIME)
    assert r.status == "skipped"
    assert "npm" in r.skipped_reason


def test_runtime_runner_error_is_error(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, RunnerError("vitest chạy quá 300 giây"), res(3, 10))
    r = check_exercise(ex, RUNTIME)
    assert any("300 giây" in m for m in errors(r))


def test_runtime_no_runner_is_skipped(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path, vitest_dep=False)
    fake_runner(monkeypatch, res(10, 10), res(3, 10))
    r = check_exercise(ex, RUNTIME)
    assert r.status == "skipped"
    assert r.skipped_reason == "Không có bộ test chạy được"


def test_runtime_off_does_not_run(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    seen = []
    fake_runner(monkeypatch, res(10, 10), res(3, 10), seen)
    check_exercise(ex, VerifyOptions())
    assert seen == []


def test_runtime_with_db_uses_fresh_sandbox_per_project(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path, with_db=True)
    entered = []

    class FakeSandbox:
        cleanup_ok = True

        def __enter__(self):
            entered.append(self)
            return {"host": "127.0.0.1", "port": 45000 + len(entered), "user": "root", "password": ""}

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(exercise_gate, "MySQLSandbox", FakeSandbox)
    seen = []
    fake_runner(monkeypatch, res(10, 10), res(3, 10), seen)
    r = check_exercise(ex, RUNTIME)
    assert errors(r) == []
    assert len(entered) == 2 and entered[0] is not entered[1]
    assert sorted(db["port"] for _, db in seen) == [45001, 45002]


def test_runtime_unexpected_exception_is_error_not_crash(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    fake_runner(monkeypatch, OSError("đường dẫn quá dài"), res(3, 10))
    r = check_exercise(ex, RUNTIME)
    assert any("Đáp án mẫu" in m and "đường dẫn quá dài" in m for m in errors(r))
    assert r.detail["runtime"]["starter"]["total"] == 10


def test_runtime_cleanup_warning(monkeypatch, tmp_path):
    ex = make_exercise(tmp_path)
    sol = res(10, 10)
    sol["cleanup_warning"] = "không xóa hết thư mục chạy tạm X"
    fake_runner(monkeypatch, sol, res(3, 10))
    r = check_exercise(ex, RUNTIME)
    assert r.status == "pass"
    assert any(f.severity == "warning" and "không xóa hết" in f.message for f in r.findings)


def test_tests_html_skips_node_modules(tmp_path):
    nm = tmp_path / "node_modules" / "pkg"
    nm.mkdir(parents=True)
    (nm / "tests.html").write_text("")
    (nm / "harness.js").write_text("")
    assert exercise_gate._tests_html(tmp_path) is None
    sub = tmp_path / "web"
    sub.mkdir()
    (sub / "tests.html").write_text("")
    (sub / "harness.js").write_text("")
    assert exercise_gate._tests_html(tmp_path) == sub / "tests.html"


def test_select_runner(tmp_path):
    p = _pkg(tmp_path / "v", {}, {"vitest": "3.1.4"}).parent
    assert exercise_gate.select_runner(p) == "vitest"
    assert not exercise_gate.needs_mysql(p)
    (p / ".env.example").write_text("PORT=3000\nDB_HOST=127.0.0.1\n", encoding="utf-8")
    assert exercise_gate.needs_mysql(p)
    b = tmp_path / "b"
    b.mkdir()
    (b / "tests.html").write_text("<html></html>")
    (b / "harness.js").write_text("")
    assert exercise_gate.select_runner(b) == "browser"
    n = tmp_path / "n"
    n.mkdir()
    (n / "index.js").write_text("")
    assert exercise_gate.select_runner(n) is None


def test_env_from_db():
    env = exercise_gate.db_env({"host": "127.0.0.1", "port": 45000, "user": "root", "password": ""})
    assert env == {"DB_HOST": "127.0.0.1", "DB_PORT": "45000", "DB_USER": "root", "DB_PASSWORD": ""}


# --- cổng slide_html (runtime) ---------------------------------------------

SLIDES = "<html><body><div class='slide active'><h2>Mở đầu</h2></div></body></html>"


def test_slide_runtime_overflow_error(monkeypatch, tmp_path):
    f = tmp_path / "slides.html"
    f.write_text(SLIDES, encoding="utf-8")
    monkeypatch.setattr(browser, "measure_slides", lambda html, **kw: {
        "slides": 18,
        "slide_overflow": [{"slide": 4, "viewport": "1366x768", "over_px": 37, "state": "mặc định"},
                           {"slide": 5, "viewport": "1920x1080", "over_px": 2, "state": "mặc định"}],
        "horizontal_overflow": [], "console_errors": []})
    r = check_slide_html(f, RUNTIME)
    errs = errors(r)
    assert len(errs) == 1
    assert "slide 4" in errs[0] and "1366x768" in errs[0]


def test_slide_runtime_console_error(monkeypatch, tmp_path):
    f = tmp_path / "slides.html"
    f.write_text(SLIDES, encoding="utf-8")
    monkeypatch.setattr(browser, "measure_slides", lambda html, **kw: {
        "slides": 18, "slide_overflow": [], "horizontal_overflow": [],
        "console_errors": ["[1366x768] ReferenceError: x is not defined"]})
    r = check_slide_html(f, RUNTIME)
    assert any("console" in m and "ReferenceError" in m for m in errors(r))


def test_slide_runtime_console_errors_deduped_across_viewports(monkeypatch, tmp_path):
    f = tmp_path / "slides.html"
    f.write_text(SLIDES, encoding="utf-8")
    monkeypatch.setattr(browser, "measure_slides", lambda html, **kw: {
        "slides": 18, "slide_overflow": [], "horizontal_overflow": [],
        "console_errors": ["[1366x768] ReferenceError: x", "[1920x1080] ReferenceError: x",
                           "[1280x720] TypeError: y"]})
    errs = errors(check_slide_html(f, RUNTIME))
    assert len(errs) == 2
    assert any("ReferenceError" in m and "1366x768" in m and "1920x1080" in m for m in errs)


def test_slide_runtime_tool_unavailable(monkeypatch, tmp_path):
    f = tmp_path / "slides.html"
    f.write_text(SLIDES, encoding="utf-8")

    def boom(html, **kw):
        raise ToolUnavailable("Chưa cài Playwright")
    monkeypatch.setattr(browser, "measure_slides", boom)
    r = check_slide_html(f, RUNTIME)
    assert r.status == "skipped" and "Playwright" in r.skipped_reason


def test_slide_runtime_off_does_not_measure(monkeypatch, tmp_path):
    f = tmp_path / "slides.html"
    f.write_text(SLIDES, encoding="utf-8")

    def boom(html, **kw):
        raise AssertionError("không được đo khi runtime tắt")
    monkeypatch.setattr(browser, "measure_slides", boom)
    assert check_slide_html(f, VerifyOptions()).status == "pass"


# --- tích hợp --------------------------------------------------------------

def _node_course_root() -> Path | None:
    """Thư mục `output/` nằm ở gốc kho; từ worktree thì tìm lên các thư mục cha."""
    from core.harness.gates._skill_loader import REPO
    for base in (REPO, *REPO.parents):
        cand = base / "output" / "pms" / "nodejs_ai_driven" / "Session 01 - Ly thuyet NodeJS Express MySQL" / "Bai tap"
        if cand.is_dir():
            return cand
    return None


@pytest.mark.integration
def test_integration_node_exercise_with_mysql():
    base = _node_course_root()
    dirs = sorted(base.glob("1_*")) if base else []
    if not dirs:
        pytest.skip("Không có thư mục output của môn nodejs_ai_driven")
    if not tooling.which("node") or not tooling.which("npm") or not tooling.find_mysqld():
        pytest.skip("Thiếu node/npm hoặc mysqld")
    r = check_exercise(dirs[0], RUNTIME)
    rt = r.detail["runtime"]
    assert rt["solution"]["total"] > 0 and rt["solution"]["passed"] == rt["solution"]["total"], r.findings
    assert rt["starter"]["total"] > 0 and rt["starter"]["passed"] < rt["starter"]["total"], r.findings
    assert not [f for f in r.findings if f.severity == "error"], r.findings
