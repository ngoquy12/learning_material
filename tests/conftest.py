"""
tests/conftest.py — Hermetic Test Isolation Layer.

Mục tiêu: unit test TUYỆT ĐỐI không được gọi LLM thật hay mở kết nối mạng.

Trước khi có file này, nhiều test gọi thẳng call_llm() ra proxy LLM (127.0.0.1:8045).
Khi proxy không chạy, mỗi test tốn ~20s retry (4 lần, backoff 3s→12s) rồi mới fail —
khiến toàn bộ suite không thể dùng làm CI gate. Tệ hơn: khi proxy CÓ chạy, kết quả test
phụ thuộc vào output ngẫu nhiên của LLM, tức là test không còn tính xác định.

Cơ chế 2 lớp:
    1. Chặn LLM: mọi call_llm/call_llm_with_images bị thay bằng stub raise ngay lập tức.
    2. Chặn mạng: socket.connect bị vô hiệu hoá, bắt mọi đường vòng (requests, httpx, SDK).

Test nào thực sự cần LLM/mạng thật thì đánh dấu @pytest.mark.integration — mặc định
những test này bị skip, chỉ chạy khi truyền cờ --run-integration.

Test nào cần LLM giả lập thì dùng fixture `mock_llm` để nạp response mẫu xác định.
"""

import socket
import sys

import pytest

# Các package thuộc dự án — chỉ patch trong phạm vi này, không đụng thư viện bên thứ ba.
_PROJECT_PACKAGES = ("agents", "core", "cli", "web")

# Tên các hàm gọi LLM cần chặn (đã được bind vào module khác qua `from core.llm import ...`).
_LLM_FUNCTION_NAMES = ("call_llm", "call_llm_with_images")


class LLMCallBlockedError(RuntimeError):
    """Raise khi unit test cố gọi LLM thật mà không khai báo mock hoặc marker integration."""


class NetworkCallBlockedError(RuntimeError):
    """Raise khi unit test cố mở kết nối mạng."""


# =============================================================================
# SECTION 1: PYTEST CONFIGURATION & MARKERS
# =============================================================================

def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Chạy cả test integration (cần LLM/mạng thật). Mặc định các test này bị skip.",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: test cần LLM hoặc mạng thật; bị skip trừ khi có --run-integration.",
    )
    config.addinivalue_line(
        "markers",
        "allow_network: cho phép test này mở socket (vẫn chặn LLM).",
    )


def pytest_collection_modifyitems(config, items):
    """Skip toàn bộ test integration trừ khi người dùng chủ động yêu cầu."""
    if config.getoption("--run-integration"):
        return
    skip_marker = pytest.mark.skip(
        reason="Test integration (cần LLM/mạng thật). Chạy với --run-integration để bật."
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_marker)


# =============================================================================
# SECTION 2: LLM BLOCKER
# =============================================================================

def _iter_project_modules():
    """Duyệt các module đã import thuộc dự án (snapshot để tránh lỗi dict thay đổi khi lặp)."""
    for module_name, module in list(sys.modules.items()):
        if module is None:
            continue
        if module_name.split(".")[0] in _PROJECT_PACKAGES:
            yield module


def _patch_llm_everywhere(replacement_factory):
    """
    Thay thế mọi tham chiếu tới hàm gọi LLM trong phạm vi dự án.

    Bắt buộc phải quét sys.modules chứ không chỉ patch core.llm: hầu hết agent dùng
    `from core.llm import call_llm` ở đầu file, nên đã giữ tham chiếu riêng tới object gốc.
    Chỉ patch core.llm sẽ bỏ sót toàn bộ những module đó.

    Trả về danh sách (tên_hàm, hàm_gốc, hàm_thay_thế) để _restore() khôi phục sau test.
    """
    import core.llm as llm_module

    patches = []
    for func_name in _LLM_FUNCTION_NAMES:
        original_func = getattr(llm_module, func_name, None)
        if original_func is None:
            continue

        replacement = replacement_factory(func_name)
        patches.append((func_name, original_func, replacement))

        # Patch tại nguồn — bắt các lệnh `from core.llm import call_llm` gọi trễ trong hàm.
        setattr(llm_module, func_name, replacement)

        # Patch tại mọi module đã bind sẵn tham chiếu tới object gốc.
        for module in _iter_project_modules():
            if module is llm_module:
                continue
            if getattr(module, func_name, None) is original_func:
                setattr(module, func_name, replacement)

    return patches


def _restore(patches):
    """
    Khôi phục hàm gốc bằng cách QUÉT LẠI sys.modules theo identity, không dựa vào
    snapshot chụp lúc patch.

    Lý do: một module có thể được import LẦN ĐẦU ngay giữa lúc test đang chạy. Khi đó
    dòng `from core.llm import call_llm` của nó bind trúng hàm thay thế, nhưng module
    này lại không có trong snapshot nên sẽ không bao giờ được khôi phục — nó giữ luôn
    stub của test cũ và làm hỏng mọi test chạy sau (lỗi này đã thực sự xảy ra và bị
    test_hermetic_guard bắt được).
    """
    import core.llm as llm_module

    for func_name, original_func, replacement in patches:
        setattr(llm_module, func_name, original_func)
        for module in _iter_project_modules():
            if module is llm_module:
                continue
            if getattr(module, func_name, None) is replacement:
                setattr(module, func_name, original_func)


@pytest.fixture(autouse=True)
def block_real_llm(request):
    """
    Chặn mọi lời gọi LLM thật trong unit test.

    Stub raise ngay lập tức (không retry, không chờ mạng) kèm thông báo nêu rõ agent nào
    đã gọi — biến "test treo 20s rồi fail khó hiểu" thành "fail tức thì, chỉ đúng chỗ".
    """
    if "integration" in request.keywords:
        yield
        return

    # Test dùng fixture mock_llm sẽ tự cài stub riêng, không áp dụng blocker ở đây.
    if "mock_llm" in request.fixturenames:
        yield
        return

    def _make_blocker(func_name):
        def _blocked(*args, **kwargs):
            agent_name = kwargs.get("agent_name") or "Unknown Agent"
            raise LLMCallBlockedError(
                f"❌ [LLM BỊ CHẶN TRONG UNIT TEST] {func_name}() được gọi bởi agent "
                f"'{agent_name}' trong test '{request.node.nodeid}'.\n"
                f"Unit test không được gọi LLM thật (kết quả không xác định + chậm).\n"
                f"Cách xử lý:\n"
                f"  - Dùng fixture 'mock_llm' để nạp response mẫu xác định, HOẶC\n"
                f"  - Đánh dấu @pytest.mark.integration nếu test bắt buộc cần LLM thật."
            )
        return _blocked

    originals = _patch_llm_everywhere(_make_blocker)
    try:
        yield
    finally:
        _restore(originals)


@pytest.fixture
def mock_llm():
    """
    Nạp response LLM giả lập, xác định.

    Cách dùng:
        def test_something(mock_llm):
            mock_llm.set_response('{"key": "value"}')
            ...
            assert mock_llm.call_count == 1

        # Nhiều response theo thứ tự gọi:
        mock_llm.set_responses(['{"a": 1}', '{"b": 2}'])

        # Tuỳ biến theo agent gọi:
        mock_llm.set_handler(lambda **kw: '{}' if kw.get('json_mode') else 'Nội dung mẫu')
    """
    class _MockLLM:
        def __init__(self):
            self._responses = []
            self._handler = None
            self._default = ""
            self.calls = []

        @property
        def call_count(self):
            return len(self.calls)

        def set_response(self, response):
            self._default = response
            self._responses = []

        def set_responses(self, responses):
            self._responses = list(responses)

        def set_handler(self, handler):
            self._handler = handler

        def _dispatch(self, *args, **kwargs):
            self.calls.append({"args": args, "kwargs": kwargs})
            if self._handler is not None:
                return self._handler(*args, **kwargs)
            if self._responses:
                return self._responses.pop(0)
            return self._default

    mock = _MockLLM()
    originals = _patch_llm_everywhere(lambda func_name: mock._dispatch)
    try:
        yield mock
    finally:
        _restore(originals)


# =============================================================================
# SECTION 3: NETWORK BLOCKER
# =============================================================================

def _is_loopback(address):
    """
    Nhận diện địa chỉ loopback.

    Loopback KHÔNG bị chặn: asyncio trên Windows (ProactorEventLoop) tự dựng một
    self-pipe bằng socket loopback mỗi lần asyncio.run() chạy. Chặn luôn cả loopback
    sẽ làm hỏng mọi test dùng asyncio dù chúng không hề đụng tới mạng thật.
    Đường LLM chạy qua proxy localhost đã bị chặn sẵn ở SECTION 2 (tầng hàm),
    nên bỏ qua loopback ở đây không tạo lỗ hổng.
    """
    if not isinstance(address, (tuple, list)) or not address:
        return False
    host = address[0]
    if not isinstance(host, str):
        return False
    return host.startswith("127.") or host in ("::1", "localhost", "", "0.0.0.0")


@pytest.fixture(autouse=True)
def block_network(request):
    """
    Chặn kết nối mạng ra ngoài ở tầng socket.

    Đây là lưới an toàn lớp hai: kể cả khi một đường gọi LLM/HTTP nào đó chưa được
    blocker ở SECTION 2 bao phủ (SDK tự tạo client, thư viện gọi requests trực tiếp),
    nó vẫn không thể thoát ra Internet.
    """
    if "integration" in request.keywords or "allow_network" in request.keywords:
        yield
        return

    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex
    original_create_connection = socket.create_connection

    def _blocked_connect(self, address, *args, **kwargs):
        if _is_loopback(address):
            return original_connect(self, address, *args, **kwargs)
        raise NetworkCallBlockedError(
            f"❌ [MẠNG BỊ CHẶN TRONG UNIT TEST] Cố kết nối ra ngoài tới {address} "
            f"trong test '{request.node.nodeid}'.\n"
            f"Đánh dấu @pytest.mark.integration nếu test bắt buộc cần mạng thật."
        )

    def _blocked_connect_ex(self, address, *args, **kwargs):
        if _is_loopback(address):
            return original_connect_ex(self, address, *args, **kwargs)
        return _blocked_connect(self, address)

    def _blocked_create_connection(address, *args, **kwargs):
        if _is_loopback(address):
            return original_create_connection(address, *args, **kwargs)
        raise NetworkCallBlockedError(
            f"❌ [MẠNG BỊ CHẶN TRONG UNIT TEST] Cố kết nối ra ngoài tới {address} "
            f"trong test '{request.node.nodeid}'.\n"
            f"Đánh dấu @pytest.mark.integration nếu test bắt buộc cần mạng thật."
        )

    socket.socket.connect = _blocked_connect
    socket.socket.connect_ex = _blocked_connect_ex
    socket.create_connection = _blocked_create_connection
    try:
        yield
    finally:
        socket.socket.connect = original_connect
        socket.socket.connect_ex = original_connect_ex
        socket.create_connection = original_create_connection


# =============================================================================
# SECTION 4: ENVIRONMENT ISOLATION
# =============================================================================

@pytest.fixture(autouse=True)
def isolate_llm_env(request, monkeypatch):
    """
    Cô lập biến môi trường LLM khỏi .env thật của máy dev.

    Không có fixture này, kết quả test phụ thuộc vào việc máy chạy test có API key hay
    không — cùng một commit có thể pass trên máy này và fail trên máy khác.
    """
    if "integration" in request.keywords:
        return

    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    monkeypatch.setenv("GEMINI_BASE_URL", "http://127.0.0.1:9/v1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
