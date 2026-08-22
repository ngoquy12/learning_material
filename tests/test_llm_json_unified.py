"""
tests/test_llm_json_unified.py — Bộ parser JSON dùng chung cho output LLM.

Hệ thống từng có 4 bộ parser JSON song song, mỗi creator một bản. Hệ quả: cùng một
response LLM có thể parse được ở creator này nhưng hỏng ở creator kia, và mỗi lần sửa
lỗi parse chỉ vá được một bản. Nay tất cả quy về một đường:

    json_sanitizer.clean_and_parse_json   (lõi, raise khi hỏng)
        <- llm_parser.extract_json_from_response  (bọc: sửa dấu phẩy thừa, trả default)
            <- text_sanitizer.extract_and_parse_json      (alias giữ chữ ký cũ)
            <- reading_creator.robust_parse_llm_json      (+ tier 3 riêng cho bài đọc)
"""

import pytest

from core.utils.json_sanitizer import clean_and_parse_json
from core.utils.llm_parser import extract_json_from_response
from core.utils.text_sanitizer import extract_and_parse_json


class TestCoreParser:
    def test_parses_plain_json(self):
        assert clean_and_parse_json('{"a": 1}') == {"a": 1}

    def test_strips_wrapping_code_fence(self):
        assert clean_and_parse_json('```json\n{"a": 1}\n```') == {"a": 1}

    def test_keeps_inner_code_fence_inside_string_value(self):
        """
        Code fence NẰM TRONG một giá trị chuỗi không được coi là fence bao ngoài.

        Đây là lỗi thật đã xảy ra: quiz có câu hỏi kèm ```python ...``` trong đề bài,
        parser cũ tìm cặp ``` đầu tiên ở BẤT KỲ đâu rồi cắt đúng đoạn code đó ra và
        coi như toàn bộ payload, làm hỏng response JSON vốn hoàn toàn hợp lệ.
        """
        raw = '{"question": "Đoạn code sau in ra gì?\\n```python\\nprint(1)\\n```"}'

        result = clean_and_parse_json(raw)

        assert "```python" in result["question"]

    def test_escapes_raw_newlines_inside_string_values(self):
        """LLM hay trả newline thô trong chuỗi — JSON chuẩn không cho phép."""
        raw = '{"html": "<div>\ndòng 2\n</div>"}'

        result = clean_and_parse_json(raw)

        assert "dòng 2" in result["html"]

    def test_handles_escaped_quotes_inside_html_payload(self):
        """
        Payload HTML đầy dấu " đã escape — ca phổ biến nhất của hệ thống này.

        Bản escape ký tự điều khiển cũ dựa vào lookbehind `: "` nên trượt ngay khi
        giá trị chứa dấu " escape.
        """
        raw = '{"html": "<div class=\\"box\\">\nnội dung\n</div>"}'

        result = clean_and_parse_json(raw)

        assert 'class="box"' in result["html"]

    def test_raises_on_unrecoverable_input(self):
        with pytest.raises(ValueError):
            clean_and_parse_json("hoàn toàn không phải json")

    def test_raises_on_empty_input(self):
        with pytest.raises(ValueError):
            clean_and_parse_json("")


class TestSafeWrapper:
    def test_repairs_trailing_comma(self):
        assert extract_json_from_response('{"a": 1,}') == {"a": 1}

    def test_returns_default_instead_of_raising(self):
        assert extract_json_from_response("không phải json", default={"fallback": True}) == {
            "fallback": True
        }

    def test_returns_none_default_when_unspecified(self):
        assert extract_json_from_response("không phải json") is None

    def test_parses_json_array(self):
        assert extract_json_from_response('[{"a": 1}]') == [{"a": 1}]


class TestAliasKeepsLegacyContract:
    """text_sanitizer.extract_and_parse_json nay uỷ quyền, nhưng chữ ký cũ phải giữ nguyên."""

    def test_defaults_to_empty_dict_not_none(self):
        assert extract_and_parse_json("không phải json") == {}

    def test_honours_explicit_default(self):
        assert extract_and_parse_json("không phải json", default=[]) == []

    def test_non_string_input_returns_default(self):
        assert extract_and_parse_json(None) == {}

    def test_now_handles_cases_the_old_duplicate_could_not(self):
        """
        Bản trùng lặp cũ không sửa dấu phẩy thừa và không escape newline thô.

        Đây chính là loại lệch khiến cùng một response parse được ở creator này
        nhưng hỏng ở creator khác.
        """
        assert extract_and_parse_json('{"a": 1,}') == {"a": 1}
        assert extract_and_parse_json('{"html": "<p>\ndòng 2</p>"}')["html"]


class TestConsistencyAcrossEntryPoints:
    @pytest.mark.parametrize(
        "raw",
        [
            '{"a": 1}',
            '```json\n{"a": 1}\n```',
            '{"a": 1,}',
            '{"html": "<div class=\\"x\\">\nnội dung</div>"}',
        ],
    )
    def test_all_entry_points_agree(self, raw):
        """Mọi cổng vào phải cho cùng kết quả — đó là mục đích của việc gộp parser."""
        via_wrapper = extract_json_from_response(raw, default=None)
        via_alias = extract_and_parse_json(raw, default=None)

        assert via_wrapper == via_alias
        assert via_wrapper is not None
