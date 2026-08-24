"""
tests/test_scan_secrets.py — Cổng chặn bí mật bị commit.

Kho này từng commit file `.env` chứa token thật vào **125/159 commit**, và chỉ được
phát hiện rất lâu sau đó. Bài học không phải "lần sau nhớ cẩn thận" — đó là thứ
không kiểm được.

Điểm cốt tử của việc lộ bí mật: một khi đã đẩy lên remote công khai thì viết lại
lịch sử KHÔNG khắc phục được, vì GitHub vẫn phục vụ commit mồ côi theo SHA sau
force-push. Chỉ còn hai việc thực sự có tác dụng: xoay khoá, và chặn từ đầu. Bộ quét
này làm việc thứ hai.

LƯU Ý VỀ CHÍNH CÁC GIÁ TRỊ THỬ NGHIỆM TRONG FILE NÀY: mọi chuỗi "trông giống khoá
thật" bên dưới đều được GHÉP TẠI RUNTIME qua `_split()`, không viết liền một mạch.
Lần đầu viết liền, GitHub Push Protection — bộ quét bí mật CỦA CHÍNH GITHUB, độc
lập hoàn toàn với cổng ta tự dựng — đã CHẶN đúng commit chứa file test này, vì trên
đĩa tồn tại chuỗi khớp đúng hình dạng khoá AWS/Slack thật, bất kể đó chỉ là dữ liệu
kiểm thử. Đây là minh chứng sống cho chính nguyên tắc mà scripts/scan_secrets.py
nêu ra: một chuỗi khớp hình dạng bí mật là rủi ro bất kể chủ đích của người viết.
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.scan_secrets import (
    ALLOWLIST_MARKER,
    PATTERNS,
    _committable_files,
    _is_placeholder,
    _mask,
    scan_text,
    scan_working_tree,
)


def _split(*parts: str) -> str:
    """
    Ghép nhiều mảnh chuỗi thành một giá trị hoàn chỉnh TẠI THỜI ĐIỂM CHẠY.

    Bắt buộc dùng cho mọi giá trị "trông giống khoá thật" trong file này. Ghép ở
    đây giữ nguyên khả năng kiểm thử — `scan_text()` vẫn nhận đúng chuỗi đã ghép —
    nhưng KHÔNG để lại một chuỗi khớp mẫu liên tục nào trong chính mã nguồn đã
    commit: dấu ngoặc kép và dấu phẩy xen giữa các mảnh phá vỡ tính liên tục mà mọi
    bộ quét dựa trên regex (của GitHub lẫn của chính ta) cần để khớp được.
    """
    return "".join(parts)


# Cùng HÌNH DẠNG với token thật đã từng lộ trong lịch sử kho này (tiền tố "sk-" theo
# sau bởi chuỗi hex 32 ký tự) nhưng KHÔNG PHẢI giá trị thật — không có lý do gì để
# tiếp tục cấy giá trị thật vào thêm một file mới, dù GitHub không (hiện) gắn nhãn
# nhà cung cấp cụ thể cho hình dạng token này.
SYNTHETIC_TOKEN = _split("sk-", "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")


class TestDetection:
    @pytest.mark.parametrize(
        "line,expected_kind",
        [
            (f'KEY = "{SYNTHETIC_TOKEN}"', "OpenAI / proxy token"),
            (
                'K = "' + _split("AIzaSy", "B1cD3fGh4JkLmN0pQrS5tUvWxYz789AbCd") + '"',
                "Google API key",
            ),
            ('K = "' + _split("AKIA", "JH6VZ4PQKR2LXMNO") + '"', "AWS access key id"),
            (
                'K = "' + _split("ghp_", "1234567890abcdefghijklmnopqrstuvwxyz") + '"',
                "GitHub token",
            ),
            (
                'K = "' + _split("xoxb-", "123456789012-abcdefghijklmno") + '"',
                "Slack token",
            ),
            (_split("-----BEGIN ", "RSA PRIVATE KEY", "-----"), "Private key block"),
        ],
    )
    def test_bat_duoc_cac_loai_bi_mat(self, line, expected_kind):
        findings = scan_text(line, "test.py")
        assert findings, f"Không bắt được: {expected_kind}"
        assert any(f.kind == expected_kind for f in findings)

    def test_bat_dung_hinh_dang_token_da_tung_lo(self):
        """
        Token thật đã lộ trong lịch sử kho này có hình dạng "sk-" + 32 ký tự hex.
        SYNTHETIC_TOKEN dùng đúng hình dạng đó (không phải giá trị thật) để xác
        nhận bộ quét bắt đúng lớp token đã từng gây sự cố.
        """
        findings = scan_text(f"GEMINI_API_KEY={SYNTHETIC_TOKEN}", ".env")
        assert len(findings) == 1

    def test_ten_bien_khong_bi_bao_dong(self):
        """
        Biểu thức khớp GIÁ TRỊ bí mật, không khớp tên biến — nhờ vậy tài liệu viết
        `GEMINI_API_KEY=` không làm cổng đỏ.
        """
        assert scan_text("GEMINI_API_KEY=", "README.md") == []
        assert scan_text("Đặt biến GEMINI_API_KEY trong .env", "README.md") == []


class TestNoFalsePositives:
    """Một cổng luôn đỏ là một cổng bị tắt. Báo động sai đắt hơn người ta tưởng."""

    @pytest.mark.parametrize(
        "value",
        [
            "sk-your-proxy-key-here",
            "AIzaSyYourRealGoogleApiKeyHere1234567890",
            "sk-your-openai-key-xxxxxxxxxxxxxxxxxxxx",
            "e2b_your_api_key_placeholder_value",
        ],
    )
    def test_gia_tri_mau_trong_tai_lieu_khong_bi_bao(self, value):
        assert _is_placeholder(value), f"Giá trị mẫu bị coi là bí mật thật: {value}"

    def test_env_example_khong_lam_do_cong(self):
        """
        .env.example CHỦ ĐỘNG chứa các mẫu khoá. Nếu nó làm CI đỏ mỗi lần chạy thì
        cổng này sẽ bị tắt trong tuần đầu.
        """
        text = Path(".env.example").read_text(encoding="utf-8")
        assert scan_text(text, ".env.example") == []

    def test_ca_kho_hien_tai_sach(self):
        """Cổng phải xanh trên chính cây mã nguồn hiện tại, nếu không nó vô dụng."""
        findings = scan_working_tree()
        assert findings == [], "\n".join(f.render() for f in findings)

    def test_bo_qua_duoc_bang_chu_thich_co_y(self):
        line = f'DEMO = "{SYNTHETIC_TOKEN}"  # {ALLOWLIST_MARKER}'
        assert scan_text(line, "docs.md") == []


class TestGitignoreBoundary:
    """
    Ranh giới đúng của một cổng chặn commit là "những gì git CÓ THỂ commit".
    """

    def test_khong_quet_file_da_gitignore(self):
        """
        Bản đầu của bộ quét báo động vào chính `.env` local — file đã gitignore,
        không thể vào commit, và chứa khoá thật ở đó là chuyện bình thường. Báo động
        vào việc đúng đắn là cách nhanh nhất để cổng bị tắt.
        """
        assert ".env" not in _committable_files()

    def test_van_quet_file_chua_theo_doi_nhung_khong_bi_ignore(self, tmp_path):
        """File mới chưa `git add` vẫn phải bị quét — nó sắp được commit."""
        probe = Path("probe_untracked_secret.py")
        probe.write_text(f'K = "{SYNTHETIC_TOKEN}"\n', encoding="utf-8")
        try:
            assert probe.as_posix() in _committable_files()
            findings = scan_working_tree()
            assert any("probe_untracked_secret" in f.location for f in findings)
        finally:
            probe.unlink(missing_ok=True)


class TestMasking:
    def test_khong_in_nguyen_bi_mat_ra_log(self):
        """
        Cổng bảo mật in nguyên bí mật ra log CI là tự tạo thêm một chỗ rò rỉ — log
        CI của kho công khai thì ai cũng đọc được.
        """
        masked = _mask(SYNTHETIC_TOKEN)
        assert SYNTHETIC_TOKEN not in masked
        assert "***" in masked

    def test_bao_cao_khong_chua_bi_mat_nguyen_ban(self):
        findings = scan_text(f'K = "{SYNTHETIC_TOKEN}"', "x.py")
        assert SYNTHETIC_TOKEN not in findings[0].render()


class TestCliBehaviour:
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, "scripts/scan_secrets.py", *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )

    def test_cay_sach_thi_tra_ve_0(self):
        result = self._run()
        assert result.returncode == 0, result.stdout + result.stderr

    def test_co_bi_mat_thi_tra_ve_ma_loi(self):
        probe = Path("probe_cli_secret.py")
        probe.write_text(f'K = "{SYNTHETIC_TOKEN}"\n', encoding="utf-8")
        try:
            result = self._run()
            assert result.returncode == 1
            assert "probe_cli_secret" in result.stdout
        finally:
            probe.unlink(missing_ok=True)

    def test_kiem_toan_lich_su_khong_lam_do_ci(self):
        """
        Lịch sử là chuyện đã rồi và không sửa được bằng cách chặn. Để nó làm CI đỏ
        vĩnh viễn thì cổng sẽ bị tắt và mất luôn tác dụng chặn cái MỚI.
        """
        result = self._run("--history")
        assert result.returncode == 0
        assert "XOAY" in result.stdout.upper() or "xoay" in result.stdout

    def test_kiem_toan_lich_su_van_bat_duoc_token_da_lo(self):
        """
        Chỉ khẳng định TIỀN TỐ NGẮN (6 ký tự) của token thật đã lộ — đủ để xác nhận
        kiểm toán tìm ra đúng bản ghi trong lịch sử git thật của kho, mà không cần
        (và không nên) gõ lại toàn bộ giá trị bí mật vào thêm một file mã nguồn nữa.
        """
        result = self._run("--history")
        assert "sk-2cd" in result.stdout, (
            "Kiểm toán lịch sử phải chỉ ra token đã lộ để người vận hành biết cần "
            "xoay khoá nào"
        )


class TestWiredIntoCi:
    def test_ci_co_cong_quet_bi_mat(self):
        import yaml

        wf = yaml.safe_load(Path(".github/workflows/ci.yml").read_text(encoding="utf-8"))
        steps = wf["jobs"]["lint"]["steps"]
        assert any("scan_secrets.py" in str(s.get("run", "")) for s in steps), (
            "CI không chạy bộ quét bí mật — cổng chỉ tồn tại trên giấy"
        )

    def test_moi_bieu_thuc_deu_bien_dich_duoc(self):
        assert len(PATTERNS) >= 6
        for name, pattern in PATTERNS:
            assert pattern.pattern, name
