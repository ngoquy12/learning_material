"""
tests/test_semantic_scope_audit.py — Tầng kiểm định phạm vi ngữ nghĩa (C1).

Tầng 1 (`validate_text_against_scope`) so khớp CHÍNH XÁC tên khái niệm bị cấm theo
ranh giới từ. Nó bỏ lọt ba dạng vi phạm mà học viên vẫn gặp y hệt nhau:

  1. Từ đồng nghĩa tiếng Việt — "tập hợp" thay cho `set`.
  2. Dùng khái niệm mà không gọi tên — viết `{1, 2, 3}` trong bài chưa dạy set.
  3. Giải thích vòng vo cơ chế của bài sau mà tránh dùng thuật ngữ.

Tầng 2 dùng chính model Gemini đang cấu hình để soi ba dạng đó. Test ở đây mock
`call_llm`: mục tiêu là khoá HỢP ĐỒNG của tầng 2 (khi nào chạy, lọc kết quả ra sao,
hỏng thì cư xử thế nào), không phải đo chất lượng phán đoán của model.
"""

import pytest

from core import scope_gate


@pytest.fixture
def fake_llm(monkeypatch):
    """Thay call_llm bằng hàm trả về JSON dựng sẵn, ghi lại prompt đã gửi."""
    calls = []

    def _install(response: str):
        def fake_call_llm(system_prompt, user_prompt, **kwargs):
            calls.append({"system": system_prompt, "user": user_prompt, "kwargs": kwargs})
            return response

        import core.llm

        monkeypatch.setattr(core.llm, "call_llm", fake_call_llm)
        return calls

    _install.calls = calls
    return _install


FORBIDDEN = {"set", "dictionary", "list comprehension"}

# Nội dung phải đủ dài (>200 ký tự sau khi bóc thẻ) mới được đưa xuống tầng 2.
CONTENT_SYNONYM = (
    "<p>Trong bài học này chúng ta sẽ làm việc với một cấu trúc dữ liệu đặc biệt: "
    "tập hợp các phần tử không trùng lặp. Khi thêm một phần tử đã tồn tại, cấu trúc "
    "này tự động bỏ qua và giữ nguyên số lượng phần tử. Đây là tính chất rất hữu ích "
    "khi cần loại bỏ các giá trị trùng nhau trong danh sách đơn hàng của cửa hàng.</p>"
)


class TestOptIn:
    def test_mac_dinh_tat(self):
        """
        Tầng 2 tốn thêm một lượt gọi LLM cho mỗi artifact mà tầng 1 cho qua. Bật mặc
        định là tự ý tăng chi phí vận hành, nên phải là lựa chọn có ý thức.
        """
        assert scope_gate.SEMANTIC_SCOPE_AUDIT_ENABLED is False

    def test_khong_goi_llm_khi_tat(self, fake_llm):
        calls = fake_llm('{"violations": [{"concept": "set", "evidence": "tập hợp"}]}')
        state = {"forbidden_scope": list(FORBIDDEN), "technology_stack": "Python 3.12"}

        result = scope_gate.audit_artifact_scope(
            CONTENT_SYNONYM, state, "html", check_domain=False, semantic=False
        )

        assert calls == [], "Tầng 2 bị tắt nhưng vẫn gọi LLM"
        assert result.is_clean

    def test_bat_theo_tham_so_cho_rieng_lan_goi(self, fake_llm):
        calls = fake_llm('{"violations": [{"concept": "set", "evidence": "tập hợp"}]}')
        state = {"forbidden_scope": list(FORBIDDEN), "technology_stack": "Python 3.12"}

        result = scope_gate.audit_artifact_scope(
            CONTENT_SYNONYM, state, "html", check_domain=False, semantic=True
        )

        assert len(calls) == 1
        assert "set" in result.violations


class TestCatchesWhatKeywordsMiss:
    def test_bat_duoc_tu_dong_nghia_tieng_viet(self, fake_llm):
        """Tiền đề: tầng 1 phải THẬT SỰ bỏ lọt ca này, nếu không test vô nghĩa."""
        from core.scope_calculator import validate_text_against_scope

        assert validate_text_against_scope(CONTENT_SYNONYM, FORBIDDEN, "Python") == [], (
            "Tầng 1 đã bắt được ca này rồi — hãy chọn ca khác để chứng minh giá trị tầng 2"
        )

        fake_llm('{"violations": [{"concept": "set", "evidence": "tập hợp các phần tử không trùng lặp"}]}')
        hits = scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python 3.12")

        assert hits == ["set"]

    def test_noi_dung_sach_thi_khong_bao_gi(self, fake_llm):
        fake_llm('{"violations": []}')
        hits = scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python 3.12")
        assert hits == []


class TestRefusesToInventViolations:
    def test_loai_bo_khai_niem_ngoai_danh_sach_cam(self, fake_llm):
        """
        Bộ thẩm định là một mô hình ngôn ngữ: nó có thể trả về khái niệm nghe hợp lý
        nhưng không nằm trong phạm vi cấm. Tin theo là bắt hệ thống sinh lại một bài
        học vốn không có lỗi — cổng kiểm định tự bịa vi phạm còn tệ hơn không có cổng.
        """
        fake_llm(
            '{"violations": ['
            '{"concept": "decorator", "evidence": "..."},'
            '{"concept": "set", "evidence": "tập hợp"}]}'
        )
        hits = scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python")

        assert hits == ["set"], "Khái niệm ngoài danh sách cấm phải bị loại bỏ"

    def test_khong_phan_biet_hoa_thuong_nhung_tra_ve_dang_chuan(self, fake_llm):
        fake_llm('{"violations": [{"concept": "SET", "evidence": "x"}]}')
        hits = scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python")
        assert hits == ["set"]

    def test_khong_tra_ve_trung_lap(self, fake_llm):
        fake_llm('{"violations": [{"concept": "set"}, {"concept": "set"}]}')
        hits = scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python")
        assert hits == ["set"]


class TestNeverBreaksPipeline:
    """Hợp đồng của cả module: trục trặc ở khâu kiểm định không được làm chết tiến trình."""

    def test_llm_nem_loi_thi_coi_nhu_sach(self, monkeypatch):
        import core.llm

        def boom(*args, **kwargs):
            raise RuntimeError("proxy 8045 không phản hồi")

        monkeypatch.setattr(core.llm, "call_llm", boom)
        assert scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python") == []

    def test_llm_tra_ve_rac_thi_coi_nhu_sach(self, fake_llm):
        fake_llm("Xin lỗi, tôi không thể trả lời câu hỏi này.")
        assert scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python") == []

    def test_llm_tra_ve_kieu_du_lieu_sai(self, fake_llm):
        fake_llm('["set", "dictionary"]')  # mảng thay vì object
        assert scope_gate.semantic_scope_audit(CONTENT_SYNONYM, FORBIDDEN, "Python") == []


class TestCostGuards:
    def test_khong_goi_llm_khi_khong_co_pham_vi_cam(self, fake_llm):
        calls = fake_llm('{"violations": []}')
        scope_gate.semantic_scope_audit(CONTENT_SYNONYM, set(), "Python")
        assert calls == []

    def test_khong_goi_llm_voi_noi_dung_qua_ngan(self, fake_llm):
        calls = fake_llm('{"violations": []}')
        scope_gate.semantic_scope_audit("<p>Ngắn quá.</p>", FORBIDDEN, "Python")
        assert calls == []

    def test_bo_qua_tang_2_khi_tang_1_da_bat_duoc(self, fake_llm):
        """
        Tầng 1 bắt được nghĩa là nội dung chắc chắn phải sinh lại. Gọi thêm LLM để
        khẳng định điều đã biết là đốt token vô ích.
        """
        calls = fake_llm('{"violations": []}')
        state = {"forbidden_scope": ["dictionary"], "technology_stack": "Python 3.12"}
        text = (
            "<p>Bài này dùng dictionary để lưu thông tin đơn hàng của khách. "
            "Mỗi đơn hàng gồm mã đơn, tên khách và tổng tiền cần thanh toán, "
            "được tra cứu nhanh theo khoá là mã đơn hàng đã cấp cho khách.</p>"
        )

        result = scope_gate.audit_artifact_scope(
            text, state, "html", check_domain=False, semantic=True
        )

        assert "dictionary" in result.violations
        assert calls == [], "Tầng 1 đã bắt được rồi mà vẫn gọi tầng 2"

    def test_cat_bot_noi_dung_qua_dai(self, fake_llm):
        calls = fake_llm('{"violations": []}')
        huge = "<p>" + ("Nội dung bài học rất dài. " * 5000) + "</p>"

        scope_gate.semantic_scope_audit(huge, FORBIDDEN, "Python")

        assert len(calls) == 1
        assert len(calls[0]["user"]) < scope_gate._SEMANTIC_AUDIT_MAX_CHARS + 2000


class TestMarkupStripping:
    def test_bo_the_html_va_khoi_script(self):
        raw = '<div class="x"><script>var a = 1;</script><style>p{color:red}</style><p>Nội  dung</p></div>'
        assert scope_gate._strip_markup(raw) == "Nội dung"

    def test_noi_dung_gui_di_khong_con_khung_giao_dien(self, fake_llm):
        calls = fake_llm('{"violations": []}')
        html = (
            '<html><head><script>var pyodide = null;</script></head><body>'
            + "<p>Nội dung dạy học thật sự về danh sách đơn hàng của cửa hàng. </p>" * 5
            + "</body></html>"
        )

        scope_gate.semantic_scope_audit(html, FORBIDDEN, "Python")

        sent = calls[0]["user"]
        assert "<p>" not in sent and "<script>" not in sent
        assert "Nội dung dạy học" in sent


class TestTruthfulReporting:
    def test_vi_pham_tang_2_duoc_ghi_vao_state(self, fake_llm):
        """Bắt được mà không ghi lại thì y hệt như không bắt."""
        fake_llm('{"violations": [{"concept": "set", "evidence": "tập hợp"}]}')
        state = {
            "forbidden_scope": list(FORBIDDEN),
            "technology_stack": "Python 3.12",
            "session_id": "Session 06",
            "lesson_id": "Lesson 01",
        }

        result = scope_gate.audit_artifact_scope(
            CONTENT_SYNONYM, state, "html", check_domain=False, semantic=True
        )
        scope_gate.record_scope_audit(state, result)

        assert state["scope_audits"]["html"]["violations"] == ["set"]
        assert any(log["source"] == "Scope_Gate" for log in state["review_logs"])

    def test_phan_hoi_du_de_sinh_lai(self, fake_llm):
        fake_llm('{"violations": [{"concept": "set", "evidence": "tập hợp"}]}')
        state = {"forbidden_scope": list(FORBIDDEN), "technology_stack": "Python 3.12"}

        result = scope_gate.audit_artifact_scope(
            CONTENT_SYNONYM, state, "html", check_domain=False, semantic=True
        )

        feedback = result.as_feedback()
        assert "set" in feedback
        assert "chưa được dạy" in feedback.lower() or "chưa" in feedback
