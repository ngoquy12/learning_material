import unittest
from unittest import mock

from core import llm


class _HttpErr(Exception):
    def __init__(self, status):
        super().__init__(f"HTTP {status}")
        self.status_code = status


class _Client:
    def __init__(self, behaviour):
        self.behaviour = behaviour  # {model: exception | "ok"}
        self.calls = []
        outer = self

        class _Completions:
            def create(self, **kw):
                outer.calls.append(kw["model"])
                result = outer.behaviour[kw["model"]]
                if isinstance(result, Exception):
                    raise result
                return result

        class _Chat:
            completions = _Completions()

        self.chat = _Chat()


class TestModelFallback(unittest.TestCase):
    def test_mo_hinh_chinh_503_thi_thu_mo_hinh_cung_tier(self):
        client = _Client({"gemini-3.1-pro": _HttpErr(503), "gemini-1.5-flash": _HttpErr(503),
                          "gemini-2.0-flash-lite": _HttpErr(503), "gemini-3.8-flash-high": "OK", "gemini-1.5-pro": "OK"})
        with mock.patch("core.llm_router.AntigravityLLMRouter.get_fallback_candidates",
                        return_value=["gemini-3.8-flash-high", "gemini-1.5-pro"]):
            out = llm._create_with_model_fallback(client, {"model": "gemini-3.1-pro", "messages": []}, "Objective_Architect_Agent")
        self.assertEqual(out, "OK")
        self.assertEqual(client.calls, ["gemini-3.1-pro", "gemini-3.8-flash-high"])

    def test_loi_yeu_cau_400_khong_chuyen_mo_hinh(self):
        client = _Client({"m1": _HttpErr(400), "m2": "OK"})
        with mock.patch("core.llm_router.AntigravityLLMRouter.get_fallback_candidates", return_value=["m2"]):
            with self.assertRaises(_HttpErr):
                llm._create_with_model_fallback(client, {"model": "m1"}, "x")
        self.assertEqual(client.calls, ["m1"])

    def test_tat_ca_deu_hong_thi_nem_loi_cuoi(self):
        client = _Client({"m1": _HttpErr(503), "m2": _HttpErr(429)})
        with mock.patch("core.llm_router.AntigravityLLMRouter.get_fallback_candidates", return_value=["m2"]):
            with self.assertRaises(_HttpErr) as ctx:
                llm._create_with_model_fallback(client, {"model": "m1"}, "x")
        self.assertEqual(ctx.exception.status_code, 429)

    def test_thanh_cong_ngay_khong_goi_du_phong(self):
        client = _Client({"m1": "OK"})
        out = llm._create_with_model_fallback(client, {"model": "m1"}, "x")
        self.assertEqual(out, "OK")
        self.assertEqual(client.calls, ["m1"])


if __name__ == "__main__":
    unittest.main()
