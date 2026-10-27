"""MySQL tạm cho bước chạy thật: một tiến trình mysqld riêng, dữ liệu riêng, xóa sạch sau khi dùng.

- `--no-defaults`: không đọc my.ini/my.cnf của máy (tránh cổng, datadir của dịch vụ MySQL đang có).
- `--initialize-insecure`: root@localhost không mật khẩu, chỉ tồn tại trong datadir tạm; không tạo user nào.
- Chỉ nghe 127.0.0.1, cổng trống khác 3306; tắt X Protocol (33060) và binlog.
- Sẵn sàng khi nhật ký có "ready for connections" kèm đúng cổng (không mở kết nối thử).
"""
from __future__ import annotations

import subprocess
import sys
import time
import uuid
from pathlib import Path

from core.harness.runners import CACHE_ROOT, RunnerError, ToolUnavailable, tooling

INIT_TIMEOUT_S = 120
START_TIMEOUT_S = 60


class MySQLSandbox:
    def __init__(self, run_root: Path | None = None):
        self.run_root = Path(run_root) if run_root else CACHE_ROOT / "runs"
        self.root: Path | None = None
        self.datadir: Path | None = None
        self.port: int | None = None
        self._proc: subprocess.Popen | None = None
        self.cleanup_ok = True

    def _log_tail(self, name: str) -> str:
        try:
            return (self.root / name).read_text(encoding="utf-8", errors="replace").strip()[-600:]
        except OSError:
            return ""

    def __enter__(self) -> dict:
        mysqld = tooling.find_mysqld()
        if not mysqld:
            raise ToolUnavailable("Không tìm thấy mysqld (cần MySQL Server để chạy test có cơ sở dữ liệu)")
        self.root = self.run_root / f"mysql_{uuid.uuid4().hex[:10]}"
        self.datadir = self.root / "data"
        self.datadir.mkdir(parents=True)
        try:
            self._start(mysqld)
        except BaseException:
            self._cleanup()
            raise
        return {"host": "127.0.0.1", "port": self.port, "user": "root", "password": ""}

    def _start(self, mysqld: str) -> None:
        basedir = Path(mysqld).resolve().parent.parent
        common = [mysqld, "--no-defaults", f"--basedir={basedir}", f"--datadir={self.datadir}"]
        code, out = tooling.run_command(
            [*common, "--initialize-insecure", f"--log-error={self.root / 'init.log'}"],
            self.root, env=tooling.child_env(), timeout=INIT_TIMEOUT_S)
        if code != 0:
            raise RunnerError(f"mysqld --initialize-insecure thất bại (mã {code}): "
                              f"{self._log_tail('init.log') or out.strip()[-600:]}")
        self.port = tooling.free_port()
        log = self.root / "mysqld.log"
        cmd = [*common, f"--port={self.port}", "--bind-address=127.0.0.1", "--mysqlx=OFF", "--skip-log-bin",
               f"--log-error={log}", f"--pid-file={self.root / 'mysqld.pid'}"]
        if sys.platform != "win32":
            cmd.append(f"--socket={self.root / 'mysqld.sock'}")
        self._proc = subprocess.Popen(cmd, cwd=str(self.root), env=tooling.child_env(), stdin=subprocess.DEVNULL,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic() + START_TIMEOUT_S
        while time.monotonic() < deadline:
            if self._proc.poll() is not None:
                raise RunnerError(f"mysqld tạm dừng ngay khi khởi động: {self._log_tail('mysqld.log')}")
            try:
                text = log.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            if "ready for connections" in text and f"port: {self.port}" in text:
                return
            time.sleep(0.25)
        raise RunnerError(f"mysqld tạm không sẵn sàng sau {START_TIMEOUT_S} giây: {self._log_tail('mysqld.log')}")

    def _cleanup(self) -> None:
        if self._proc is not None:
            tooling.kill_tree(self._proc)
            self._proc = None
        if self.root is not None and self.root.exists():
            self.cleanup_ok = tooling.rmtree(self.root)

    def __exit__(self, *exc) -> bool:
        self._cleanup()
        return False
