"""
tests/test_hermetic_guard.py — Meta-test bảo vệ lớp cô lập trong conftest.py.

Lớp chặn LLM/mạng là loại hạ tầng dễ hỏng âm thầm: chỉ cần một lần refactor
core/llm.py đổi tên hàm, hoặc một agent mới import call_llm theo kiểu khác,
là blocker mất tác dụng mà toàn bộ suite vẫn xanh — rồi test lại lặng lẽ gọi
LLM thật trở lại. Những test dưới đây đảm bảo guard còn sống.
"""

import socket

import pytest

from conftest import LLMCallBlockedError, NetworkCallBlockedError


class TestLLMBlocker:
    def test_direct_call_llm_is_blocked(self):
        """Gọi call_llm qua core.llm phải bị chặn tức thì."""
        from core.llm import call_llm

        with pytest.raises(LLMCallBlockedError):
            call_llm(system_prompt="x", user_prompt="y", agent_name="TestAgent")

    def test_module_bound_call_llm_is_blocked(self):
        """
        Tham chiếu call_llm đã bind sẵn trong agent cũng phải bị chặn.

        Đây là ca quan trọng nhất: các agent dùng `from core.llm import call_llm`
        ở đầu file nên giữ tham chiếu riêng. Nếu conftest chỉ patch core.llm,
        ca này sẽ lọt và test vẫn gọi LLM thật.
        """
        import agents.creators.homework_creator as homework_creator

        with pytest.raises(LLMCallBlockedError):
            homework_creator.call_llm(
                system_prompt="x", user_prompt="y", agent_name="TestAgent"
            )

    def test_blocked_error_names_the_agent(self):
        """Thông báo lỗi phải chỉ đúng agent nào đã gọi, để debug không phải mò."""
        from core.llm import call_llm

        with pytest.raises(LLMCallBlockedError, match="Homework_Creator_Ex_1"):
            call_llm(
                system_prompt="x", user_prompt="y", agent_name="Homework_Creator_Ex_1"
            )


class TestMockLLMFixture:
    def test_returns_canned_response(self, mock_llm):
        from core.llm import call_llm

        mock_llm.set_response('{"ok": true}')
        assert call_llm(system_prompt="x", user_prompt="y") == '{"ok": true}'
        assert mock_llm.call_count == 1

    def test_returns_sequenced_responses(self, mock_llm):
        import agents.creators.homework_creator as homework_creator

        mock_llm.set_responses(["first", "second"])
        assert homework_creator.call_llm(system_prompt="a", user_prompt="b") == "first"
        assert homework_creator.call_llm(system_prompt="a", user_prompt="b") == "second"
        assert mock_llm.call_count == 2

    def test_handler_sees_call_kwargs(self, mock_llm):
        from core.llm import call_llm

        mock_llm.set_handler(
            lambda **kw: "json" if kw.get("json_mode") else "text"
        )
        assert call_llm(system_prompt="x", user_prompt="y", json_mode=True) == "json"
        assert call_llm(system_prompt="x", user_prompt="y") == "text"


class TestNetworkBlocker:
    def test_external_connection_is_blocked(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            with pytest.raises(NetworkCallBlockedError):
                sock.connect(("93.184.216.34", 80))
        finally:
            sock.close()

    def test_create_connection_to_external_is_blocked(self):
        with pytest.raises(NetworkCallBlockedError):
            socket.create_connection(("93.184.216.34", 80), timeout=1)

    def test_loopback_is_allowed(self):
        """
        Loopback KHÔNG được chặn: asyncio trên Windows dựng self-pipe qua loopback,
        chặn luôn sẽ làm hỏng mọi test dùng asyncio.run() dù chúng không đụng mạng.
        """
        import asyncio

        async def _noop():
            await asyncio.sleep(0)
            return "done"

        assert asyncio.run(_noop()) == "done"
