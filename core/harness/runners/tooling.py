"""Tìm công cụ trên máy (Chrome, mysqld, npm...), lấy cổng trống, chạy lệnh có giới hạn thời gian."""
from __future__ import annotations

import glob
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from core.harness.runners import RunnerError

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
MYSQLD_GLOBS = [
    r"C:\Program Files\MySQL\MySQL Server *\bin\mysqld.exe",
    "/usr/sbin/mysqld",
    "/usr/local/mysql/bin/mysqld",
]
# Cổng mặc định của MySQL (và X Protocol) trên máy người dùng: không bao giờ dùng.
RESERVED_PORTS = frozenset({3306, 33060})


def which(name: str) -> str | None:
    return shutil.which(name)


def find_chrome() -> str | None:
    return next((p for p in CHROME_PATHS if Path(p).exists()), None)


def find_mysqld() -> str | None:
    """mysqld trên PATH, rồi các thư mục cài đặt quen thuộc (thư mục trên PATH có thể không tồn tại)."""
    found = shutil.which("mysqld")
    if found and Path(found).exists():
        return found
    for pattern in MYSQLD_GLOBS:
        hits = sorted(glob.glob(pattern), reverse=True)  # phiên bản mới nhất trước
        for hit in hits:
            if Path(hit).is_file():
                return hit
    return None


def free_port(exclude=frozenset({3306})) -> int:
    """Cổng TCP trống trên 127.0.0.1, không bao giờ là 3306 dù `exclude` không liệt kê."""
    banned = set(exclude) | RESERVED_PORTS
    for _ in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        if port not in banned:
            return port
    raise RunnerError("Không tìm được cổng trống")


def kill_tree(proc: subprocess.Popen) -> None:
    """Tắt tiến trình cùng mọi tiến trình con (npx.cmd trên Windows sinh node con)."""
    if proc.poll() is not None:
        return
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.kill()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def run_command(cmd: list[str], cwd: Path, env: dict | None = None, timeout: float = 300) -> tuple[int, str]:
    """Chạy lệnh, gom stdout+stderr vào tệp tạm (tránh treo vì ống dẫn bị tiến trình cháu giữ).

    Quá `timeout` giây → tắt cả cây tiến trình và `raise RunnerError`.
    """
    with tempfile.TemporaryFile(mode="w+b") as log:
        proc = subprocess.Popen(cmd, cwd=str(cwd), env=env, stdout=log, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL)
        try:
            code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill_tree(proc)
            shown = " ".join([Path(cmd[0]).name, *cmd[1:3]])
            raise RunnerError(f"Lệnh `{shown}` chạy quá {int(timeout)} giây") from None
        log.seek(0)
        out = log.read().decode("utf-8", errors="replace")
    return code, out


def child_env(extra: dict | None = None) -> dict:
    env = dict(os.environ)
    env.update(extra or {})
    return env


def rmtree(path: Path, attempts: int = 5) -> None:
    """Xóa thư mục; thử lại vài lần vì Windows có thể còn giữ tệp ngay sau khi tiến trình tắt."""
    def retry(func, p, _exc):
        try:
            Path(p).chmod(0o700)
            func(p)
        except OSError:
            pass

    kw = {"onexc": retry} if sys.version_info >= (3, 12) else {"onerror": retry}
    for i in range(attempts):
        if not Path(path).exists():
            return
        shutil.rmtree(path, **kw)
        if Path(path).exists():
            time.sleep(0.5 * (i + 1))
