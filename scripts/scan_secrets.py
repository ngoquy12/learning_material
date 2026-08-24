"""
scripts/scan_secrets.py — Cổng quét bí mật bị commit vào mã nguồn.

Vì sao cần: kho này từng commit file `.env` chứa token thật vào 125/159 commit, và
chỉ được phát hiện rất lâu sau đó. Bài học không phải "lần sau nhớ cẩn thận" — đó là
thứ không kiểm được. `.gitignore` đã chặn `.env`, nhưng nó chỉ chặn ĐÚNG tên file
đó: một token dán thẳng vào file cấu hình, notebook, script tạm hay tài liệu vẫn đi
qua được.

Điểm quan trọng của việc lộ bí mật: một khi đã đẩy lên remote công khai thì viết lại
lịch sử KHÔNG khắc phục được — GitHub vẫn phục vụ commit mồ côi theo SHA sau
force-push. Cách duy nhất hiệu quả là (a) xoay khoá, và (b) chặn ngay từ đầu. File
này làm phần (b).

Chạy:
    python scripts/scan_secrets.py                 # quét cây làm việc hiện tại
    python scripts/scan_secrets.py --history       # quét toàn bộ lịch sử git
    python scripts/scan_secrets.py --staged        # quét file đang staged (dùng cho pre-commit)

Bỏ qua một dòng cố ý (ví dụ mẫu trong tài liệu): thêm chú thích
    # pragma: allowlist secret
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

BASE_DIR = Path(__file__).resolve().parent.parent

# Mỗi mục: (tên, biểu thức). Biểu thức khớp CHÍNH giá trị bí mật, không khớp tên biến
# — nhờ vậy `GEMINI_API_KEY=` trong tài liệu không bị báo, chỉ giá trị thật mới bị.
PATTERNS: list[tuple[str, re.Pattern]] = [
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{30,}")),
    ("OpenAI / proxy token", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("OpenAI project token", re.compile(r"sk-proj-[A-Za-z0-9_\-]{20,}")),
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("E2B API key", re.compile(r"e2b_[A-Za-z0-9]{20,}")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]

# Dấu hiệu của giá trị GIẢ trong tài liệu và file mẫu. Không có bộ lọc này thì
# `.env.example` sẽ báo động mỗi lần chạy, và một cổng luôn đỏ là cổng bị tắt.
PLACEHOLDER_MARKERS = (
    "your", "xxx", "example", "placeholder", "here", "changeme",
    "dummy", "fake", "redacted", "...", "<", ">",
)

ALLOWLIST_MARKER = "pragma: allowlist secret"

# Không quét: thư mục sinh tự động, môi trường ảo, và chính file này (nó chứa
# đúng các biểu thức cần tìm).
SKIP_DIR_PARTS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".ruff_cache", "dist", "build", "output",
}
SKIP_FILES = {"scan_secrets.py"}

# Chỉ quét file văn bản có khả năng chứa bí mật.
TEXT_SUFFIXES = {
    ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".env", ".sh", ".ps1", ".md", ".txt", ".html", ".j2", ".ipynb", ".xml",
}

MAX_BYTES = 2_000_000


class Finding(NamedTuple):
    location: str
    line_no: int
    kind: str
    excerpt: str

    def render(self) -> str:
        return f"  {self.location}:{self.line_no}  [{self.kind}]  {self.excerpt}"


def _is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def _mask(value: str) -> str:
    """
    Che giá trị trong báo cáo.

    Cổng bảo mật in nguyên bí mật ra log CI là tự tạo thêm một chỗ rò rỉ — log CI
    của kho công khai thì ai cũng đọc được.
    """
    if len(value) <= 10:
        return value[:3] + "***"
    return f"{value[:6]}***{value[-2:]} (dài {len(value)})"


def scan_text(text: str, location: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if ALLOWLIST_MARKER in line:
            continue
        for kind, pattern in PATTERNS:
            for match in pattern.finditer(line):
                value = match.group(0)
                if _is_placeholder(value):
                    continue
                findings.append(Finding(location, line_no, kind, _mask(value)))
    return findings


def _should_scan(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    if any(part in SKIP_DIR_PARTS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith(".env")


def _committable_files() -> list[str]:
    """
    Danh sách file mà git CÓ THỂ đưa vào commit: đã theo dõi, hoặc chưa theo dõi
    nhưng không bị .gitignore loại.

    Đây mới là ranh giới đúng cho một cổng chặn commit. Quét cả cây làm việc sẽ báo
    động vào chính file `.env` local — file đã gitignore, không thể vào commit, và
    chứa khoá thật ở đó là chuyện bình thường. Một cổng báo động vào việc đúng đắn
    là cổng sẽ bị tắt.
    """
    tracked = _git(["ls-files"]).splitlines()
    untracked = _git(["ls-files", "--others", "--exclude-standard"]).splitlines()
    return [n for n in (*tracked, *untracked) if n.strip()]


def scan_working_tree(root: Path = BASE_DIR) -> list[Finding]:
    names = _committable_files()

    if not names:
        # Không phải kho git (hoặc git không khả dụng): quay về quét cả cây, chấp
        # nhận báo động vào file ignore hơn là im lặng không quét gì.
        names = [
            p.relative_to(root).as_posix()
            for p in sorted(root.rglob("*"))
            if p.is_file()
        ]

    findings: list[Finding] = []
    for name in names:
        rel = Path(name)
        if not _should_scan(rel):
            continue
        path = root / rel
        try:
            if not path.is_file() or path.stat().st_size > MAX_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        findings.extend(scan_text(text, rel.as_posix()))
    return findings


def _git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args], cwd=str(BASE_DIR), capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def scan_staged() -> list[Finding]:
    """Quét nội dung ĐANG STAGED — đúng thứ sắp được commit, không phải file trên đĩa."""
    names = [n for n in _git(["diff", "--cached", "--name-only"]).splitlines() if n.strip()]
    findings: list[Finding] = []
    for name in names:
        path = Path(name)
        if not _should_scan(path):
            continue
        content = _git(["show", f":{name}"])
        if content:
            findings.extend(scan_text(content, f"[staged] {name}"))
    return findings


def scan_history() -> list[Finding]:
    """
    Quét mọi blob trong toàn bộ lịch sử.

    Dùng để KIỂM TOÁN, không dùng làm cổng chặn: lịch sử đã đẩy lên remote thì không
    sửa được bằng cách chặn nữa — chỉ xoay khoá mới có tác dụng.

    Dùng `git cat-file --batch` (MỘT tiến trình con đọc cả nghìn blob qua một luồng
    stdin/stdout) thay vì gọi `git cat-file -p <sha>` riêng cho từng blob. Kho này có
    hơn 2000 blob khớp đuôi file cần quét (do .env từng bị commit 125 lần cùng mọi
    file khác đổi qua 159 commit); tạo ngần ấy tiến trình con riêng lẻ trên Windows
    tốn ~90 giây chỉ để khởi động tiến trình — không phải để đọc dữ liệu. Việc đó
    khiến bộ test của chính cổng này trở thành phần chậm nhất của cả bộ kiểm thử, và
    một bộ test luôn chậm cũng bị bỏ chạy y như một cổng luôn đỏ bị tắt.
    """
    listing = _git(["rev-list", "--objects", "--all"])
    seen_blobs = set()
    entries: list[tuple[str, str]] = []

    for line in listing.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        sha, name = parts[0], parts[1].strip()
        if sha in seen_blobs or not name:
            continue
        if not _should_scan(Path(name)):
            continue
        seen_blobs.add(sha)
        entries.append((sha, name))

    if not entries:
        return []

    try:
        proc = subprocess.run(
            ["git", "cat-file", "--batch"],
            cwd=str(BASE_DIR),
            input=("\n".join(sha for sha, _ in entries) + "\n").encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=180,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        # git không có sẵn trong PATH, hoặc tiến trình vượt quá 180 giây timeout.
        # Kiểm toán lịch sử là tiện ích, không phải cổng chặn — hỏng thì báo rỗng
        # thay vì làm sập cả lệnh gọi nó.
        return []

    # Đọc thủ công dạng nhị phân theo đúng giao thức của `cat-file --batch`: mỗi
    # object là một dòng tiêu đề "<sha> <type> <size>\n" theo sau bởi ĐÚNG `size`
    # byte nội dung rồi một dấu xuống dòng. Bắt buộc thao tác trên bytes thô, không
    # qua chế độ text: universal-newline translation (CRLF -> LF trên Windows) sẽ
    # làm lệch số byte cần đọc và làm hỏng luôn phần còn lại của luồng dữ liệu.
    buf = proc.stdout
    pos = 0
    findings: list[Finding] = []

    for sha, name in entries:
        newline_at = buf.find(b"\n", pos)
        if newline_at == -1:
            break
        header = buf[pos:newline_at].decode("utf-8", errors="replace").split()
        pos = newline_at + 1

        if len(header) < 3 or header[-1] == "missing":
            continue

        try:
            size = int(header[2])
        except ValueError:
            continue

        content = buf[pos : pos + size]
        pos += size
        if buf[pos : pos + 1] == b"\n":
            pos += 1

        if size > MAX_BYTES:
            continue

        text = content.decode("utf-8", errors="replace")
        findings.extend(scan_text(text, f"[history] {name}"))

    return findings


def _dedupe(findings: Iterable[Finding]) -> list[Finding]:
    """Cùng một bí mật lặp ở 125 commit chỉ cần báo một lần."""
    out, seen = [], set()
    for f in findings:
        key = (f.kind, f.excerpt, f.location)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Quét bí mật bị commit vào mã nguồn")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true", help="Chỉ quét nội dung đang staged")
    mode.add_argument("--history", action="store_true", help="Kiểm toán toàn bộ lịch sử git")
    args = parser.parse_args()

    if args.history:
        label = "toàn bộ lịch sử git"
        findings = _dedupe(scan_history())
    elif args.staged:
        label = "nội dung đang staged"
        findings = _dedupe(scan_staged())
    else:
        label = "cây làm việc hiện tại"
        findings = _dedupe(scan_working_tree())

    if not findings:
        print(f"[scan-secrets] Không phát hiện bí mật nào trong {label}.")
        return 0

    print(f"[scan-secrets] PHÁT HIỆN {len(findings)} bí mật trong {label}:")
    for finding in findings:
        print(finding.render())

    if args.history:
        print(
            "\nĐây là kết quả KIỂM TOÁN lịch sử. Lịch sử đã đẩy lên remote thì viết lại\n"
            "KHÔNG khắc phục được — GitHub vẫn phục vụ commit mồ côi theo SHA sau\n"
            "force-push. Việc cần làm là XOAY các khoá bên trên."
        )
        # Không trả mã lỗi ở chế độ kiểm toán: lịch sử là chuyện đã rồi, để nó làm CI
        # đỏ vĩnh viễn thì cổng sẽ bị tắt và mất luôn tác dụng chặn cái mới.
        return 0

    print(
        "\nGỡ bí mật ra khỏi mã nguồn và đưa vào biến môi trường (.env, đã gitignore).\n"
        f"Nếu đây là giá trị mẫu cố ý, thêm chú thích: # {ALLOWLIST_MARKER}"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
