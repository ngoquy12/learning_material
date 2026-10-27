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
from contextlib import contextmanager
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
        except BaseException:  # Ctrl+C...: không để lại tiến trình con
            kill_tree(proc)
            raise
        log.seek(0)
        out = log.read().decode("utf-8", errors="replace")
    return code, out


_SECRET_MARKERS = ("API_KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL")


def _inherited_ok(key: str) -> bool:
    up = key.upper()
    return not up.startswith("DB_") and not any(m in up for m in _SECRET_MARKERS)


def child_env(extra: dict | None = None) -> dict:
    """Môi trường cho tiến trình con: bỏ DB_* và khóa/bí mật kế thừa; `extra` của người gọi luôn thắng."""
    env = {k: v for k, v in os.environ.items() if _inherited_ok(k)}
    env.update(extra or {})
    return env


def pid_alive(pid: int) -> bool:
    """Tiến trình `pid` còn chạy không (Windows: OpenProcess + GetExitCodeProcess; nơi khác: kill 0)."""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        kernel32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        process_query_limited_information, still_active, access_denied = 0x1000, 259, 5
        handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
        if not handle:
            # Không mở được vì thiếu quyền: tiến trình vẫn tồn tại (của người dùng khác).
            return ctypes.get_last_error() == access_denied
        try:
            code = wintypes.DWORD()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return True
            return code.value == still_active
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _lock_owner(path: Path) -> int | None:
    """PID chủ khóa ghi trong tệp (`<pid> <timestamp>`); None nếu không đọc/không hiểu được."""
    try:
        first = path.read_text(encoding="utf-8", errors="replace").split()[0]
        return int(first)
    except (OSError, IndexError, ValueError):
        return None


def _lock_is_stale(path: Path, stale_after: float) -> bool:
    owner = _lock_owner(path)
    if owner is not None and not pid_alive(owner):
        return True  # chủ khóa đã chết: chiếm ngay, không chờ hết hạn
    return time.time() - path.stat().st_mtime > stale_after


@contextmanager
def file_lock(path: Path, timeout: float = 900, stale_after: float = 1800):
    """Khóa liên tiến trình bằng tệp tạo độc quyền, ghi `<pid> <timestamp>` của chủ khóa.

    Khóa coi như bỏ rơi khi tiến trình chủ không còn chạy, hoặc (không đọc được PID) cũ hơn `stale_after` giây.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()} {time.time():.0f}".encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if _lock_is_stale(path, stale_after):
                    path.unlink()
                    continue
            except OSError:
                if not path.exists():
                    continue  # chủ khóa vừa nhả: thử lấy lại ngay
            if time.monotonic() > deadline:
                raise RunnerError(f"Chờ khóa {path.name} quá {int(timeout)} giây") from None
            time.sleep(1)
    try:
        yield
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def rmtree(path: Path, attempts: int = 5) -> bool:
    """Xóa thư mục; thử lại vài lần vì Windows có thể còn giữ tệp. Trả False nếu vẫn còn sót."""
    def retry(func, p, _exc):
        try:
            Path(p).chmod(0o700)
            func(p)
        except OSError:
            pass

    kw = {"onexc": retry} if sys.version_info >= (3, 12) else {"onerror": retry}
    for i in range(attempts):
        if not Path(path).exists():
            return True
        shutil.rmtree(path, **kw)
        if Path(path).exists():
            time.sleep(0.5 * (i + 1))
    return not Path(path).exists()
