import unittest

from cli.curriculum_parser import is_practice_session, is_project_or_hackathon_session
from core.session_types import SessionType, detect_session_type
from core.utils.text_match import has_any_term


class TestTermMatching(unittest.TestCase):
    def test_khong_bat_nham_chuoi_con(self):
        self.assertFalse(has_any_term("Identifier và provide", ["ide"]))
        self.assertFalse(has_any_term("Label và table", ["lab"]))
        self.assertTrue(has_any_term("Cài đặt IDE", ["ide"]))

    def test_cum_tieng_viet(self):
        self.assertTrue(has_any_term("Buổi thực hành số 2", ["thực hành"]))


class TestSessionClassification(unittest.TestCase):
    def test_tieu_de_co_chu_lab_trong_tu_khac_van_la_ly_thuyet(self):
        self.assertIs(detect_session_type({"title": "Label và table trong HTML"}), SessionType.THEORY)

    def test_buoi_thuc_hanh_that(self):
        self.assertIs(detect_session_type({"title": "Lab: Làm việc với mảng"}), SessionType.PRACTICE)

    def test_lesson_ten_du_an_trong_buoi_ly_thuyet_khong_bi_xep_la_du_an(self):
        session = {"title": "Cấu trúc thư mục", "session_type": "Lý thuyết", "session_code": "THEORY"}
        self.assertFalse(is_project_or_hackathon_session(session))
        self.assertFalse(is_practice_session(session))


if __name__ == "__main__":
    unittest.main()
