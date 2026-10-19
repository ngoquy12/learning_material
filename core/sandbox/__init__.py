"""
core/sandbox package initialization.
"""
from typing import Dict, Any
from core.sandbox.code_executor import (
    CodeSandboxExecutor,
    ExecutionResult,
    execute_code_snippet
)

from core.sandbox.polyglot_runner import (
    detect_language,
    execute_polyglot_code,
    normalize_language
)

def execute_code_safely(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Chạy mã để kiểm chứng.

    Mặc định chạy bằng polyglot runner (tiến trình con trong thư mục tạm; Bash chỉ kiểm tra cú
    pháp). Đặt SANDBOX_PROVIDER=docker hoặc e2b để chạy trong container/đám mây cô lập
    (core/sandbox/isolated.py). Cố ý chọn theo biến môi trường rõ ràng thay vì mặc định Docker:
    chạy container kéo image từ mạng ở lần đầu, và lỗi kéo image sẽ bị hiểu nhầm là mã của bài
    bị lỗi.
    """
    import os

    if os.getenv("SANDBOX_PROVIDER", "").strip().lower() in ("docker", "e2b"):
        from core.sandbox.isolated import execute_code_safely as _isolated

        return _isolated(code, language=language)

    from core.sandbox.polyglot_runner import execute_polyglot_code

    res = execute_polyglot_code(code, language=language)
    return res.to_dict()

__all__ = [
    "CodeSandboxExecutor",
    "ExecutionResult",
    "execute_code_snippet",
    "execute_code_safely",
    "detect_language",
    "execute_polyglot_code",
    "normalize_language"
]
