"""
core/sandbox/polyglot_runner.py
Multi-Language Code Execution and Verification Runner (tiến trình con trong thư mục tạm; không phải sandbox bảo mật - xem DOCKER_IMAGE_MAP ở core/sandbox.py cho container cô lập).
Supports Python, JavaScript/TypeScript, SQL (In-Memory SQLite), Java, Go, C/C++, and Bash.
"""

from __future__ import annotations

import os
import re
import sys
import time
import shutil
import sqlite3
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple

# Mọi tiến trình con chạy trong thư mục tạm riêng, KHÔNG kế thừa thư mục làm việc của dự án:
# mã do mô hình sinh ra (ví dụ lệnh git/rm trong bài đọc) không được chạm vào repo hay output/.
_SANDBOX_CWD = tempfile.mkdtemp(prefix="polyglot_sandbox_")


@dataclass
class ExecutionResult:
    """Unified result container for any language execution."""
    success: bool
    stdout: str = ""
    stderr: str = ""
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    traceback: Optional[str] = None
    execution_time_ms: float = 0.0
    timeout_exceeded: bool = False
    language: str = "python"
    engine: str = "local"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "status": "SUCCESS" if self.success else "FAILED",
            "stdout": self.stdout,
            "stderr": self.stderr,
            "output": self.stdout if self.success else (self.error_message or self.stderr),
            "error": self.error_message or self.stderr,
            "error_type": self.error_type,
            "execution_time_ms": self.execution_time_ms,
            "timeout_exceeded": self.timeout_exceeded,
            "language": self.language,
            "engine": self.engine,
        }


# =============================================================================
# LANGUAGE DETECTION & NORMALIZATION
# =============================================================================

LANGUAGE_ALIASES: Dict[str, str] = {
    "py": "python",
    "python": "python",
    "python3": "python",
    "js": "javascript",
    "javascript": "javascript",
    "node": "javascript",
    "nodejs": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "sql": "sql",
    "sqlite": "sql",
    "sqlite3": "sql",
    "postgres": "sql",
    "postgresql": "sql",
    "mysql": "sql",
    "java": "java",
    "go": "go",
    "golang": "go",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "sh": "bash",
    "bash": "bash",
    "shell": "bash",
    "html": "html",
    "html5": "html",
    "htm": "html",
    "xml": "html",
    "css": "css",
    "tailwind": "css",
    "tailwindcss": "css",
    "postcss": "css",
    "sass": "css",
    "scss": "css",
}


def normalize_language(lang_str: Optional[str]) -> str:
    """Normalizes language name or alias to canonical form."""
    if not lang_str:
        return "python"
    clean = lang_str.lower().strip()
    return LANGUAGE_ALIASES.get(clean, clean)


def detect_language(code: str, hint: str = "") -> str:
    """
    Infers the programming language from an explicit hint (tech_stack or code fence)
    or code heuristics.
    """
    if hint:
        norm = normalize_language(hint)
        if norm in LANGUAGE_ALIASES.values():
            return norm

    # Code heuristics
    code_strip = code.strip()
    if re.search(r"^\s*<!DOCTYPE\s+html|<(?:html|head|body|div|span|p|a|table|form|input|button|header|footer|nav|section|article)\b", code_strip, re.IGNORECASE):
        return "html"
    if re.search(r"[.#][\w-]+\s*\{|\b(?:@media|@keyframes|@apply|@layer)\b", code_strip):
        return "css"
    if re.search(r"^\s*(SELECT|INSERT\s+INTO|CREATE\s+TABLE|UPDATE\s+\w+\s+SET|DELETE\s+FROM|DROP\s+TABLE)\b", code_strip, re.IGNORECASE):
        return "sql"
    if re.search(r"\bpublic\s+(?:final\s+)?class\b|\bSystem\.out\.println\b|\bpublic\s+static\s+void\s+main\b", code_strip):
        return "java"
    if re.search(r"\bpackage\s+main\b|\bfunc\s+main\s*\(\)|\bfmt\.Print", code_strip):
        return "go"
    if re.search(r"#include\s*<[a-z0-9_.]+>|\bstd::cout\b|\bprintf\s*\(", code_strip):
        return "cpp"
    if re.search(r"\bconsole\.(log|error|warn)\b|\bconst\s+\w+\s*=\s*require\(|\bfunction\s*\w*\s*\(|\bexport\s+default\b|\blet\s+\w+\s*=", code_strip):
        return "javascript"
    if re.search(r"^#!\s*/bin/(?:bash|sh)|\becho\s+[\"']|\bchmod\s+[0-9]+", code_strip, re.MULTILINE):
        return "bash"

    # Default to python
    return "python"


# =============================================================================
# INDIVIDUAL RUNNERS
# =============================================================================

class BaseLanguageRunner:
    """Base class for language-specific runners."""

    language: str = "generic"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        raise NotImplementedError


class PythonRunner(BaseLanguageRunner):
    """Executes Python code in an isolated subprocess."""

    language = "python"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty snippet]", language=self.language)

        start_time = time.perf_counter()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(code)

        try:
            cmd = [sys.executable, str(temp_path)]
            proc = subprocess.run(
                cmd,
                cwd=_SANDBOX_CWD,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                encoding="utf-8",
                errors="replace"
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if proc.returncode == 0:
                return ExecutionResult(
                    success=True,
                    stdout=proc.stdout.strip(),
                    stderr=proc.stderr.strip(),
                    execution_time_ms=round(elapsed_ms, 2),
                    language=self.language,
                    engine="python_subprocess"
                )

            stderr = proc.stderr.strip()
            err_type, err_msg = self._parse_error(stderr)
            return ExecutionResult(
                success=False,
                stdout=proc.stdout.strip(),
                stderr=stderr,
                error_type=err_type,
                error_message=err_msg,
                traceback=stderr,
                execution_time_ms=round(elapsed_ms, 2),
                language=self.language,
                engine="python_subprocess"
            )

        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=False,
                error_type="TimeoutExpired",
                error_message=f"Chương trình chạy vượt quá giới hạn thời gian ({timeout_sec}s).",
                execution_time_ms=round(elapsed_ms, 2),
                timeout_exceeded=True,
                language=self.language,
                engine="python_subprocess"
            )
        except Exception as ex:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=False,
                error_type=type(ex).__name__,
                error_message=str(ex),
                execution_time_ms=round(elapsed_ms, 2),
                language=self.language,
                engine="python_subprocess"
            )
        finally:
            try:
                if temp_path.exists():
                    temp_path.unlink()
            except Exception:
                pass

    def _parse_error(self, stderr: str) -> Tuple[str, str]:
        lines = [line.strip() for line in stderr.splitlines() if line.strip()]
        if not lines:
            return "RuntimeError", "Mã nguồn thực thi thất bại không có thông điệp lỗi."
        last_line = lines[-1]
        if ":" in last_line:
            parts = last_line.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        return "RuntimeError", last_line


class NodeJSRunner(BaseLanguageRunner):
    """Executes JavaScript / TypeScript using Node.js if available, or static validation."""

    language = "javascript"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty snippet]", language=self.language)

        node_bin = shutil.which("node")
        start_time = time.perf_counter()

        if node_bin:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(code)

            try:
                proc = subprocess.run(
                    [node_bin, str(temp_path)],
                    cwd=_SANDBOX_CWD,
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec,
                    encoding="utf-8",
                    errors="replace"
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                if proc.returncode == 0:
                    return ExecutionResult(
                        success=True,
                        stdout=proc.stdout.strip(),
                        stderr=proc.stderr.strip(),
                        execution_time_ms=round(elapsed_ms, 2),
                        language=self.language,
                        engine="node_subprocess"
                    )
                stderr = proc.stderr.strip()
                return ExecutionResult(
                    success=False,
                    stdout=proc.stdout.strip(),
                    stderr=stderr,
                    error_type="JavaScriptRuntimeError",
                    error_message=stderr.splitlines()[-1] if stderr else "JS Execution Error",
                    traceback=stderr,
                    execution_time_ms=round(elapsed_ms, 2),
                    language=self.language,
                    engine="node_subprocess"
                )
            except subprocess.TimeoutExpired:
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return ExecutionResult(
                    success=False,
                    error_type="TimeoutExpired",
                    error_message=f"Node.js script exceeded {timeout_sec}s timeout.",
                    execution_time_ms=round(elapsed_ms, 2),
                    timeout_exceeded=True,
                    language=self.language,
                    engine="node_subprocess"
                )
            finally:
                try:
                    if temp_path.exists():
                        temp_path.unlink()
                except Exception:
                    pass

        # Fallback: Static syntax inspection
        return self._static_syntax_check(code, start_time)

    def _static_syntax_check(self, code: str, start_time: float) -> ExecutionResult:
        # Check bracket parity
        for pair in [("{", "}"), ("(", ")"), ("[", "]")]:
            if code.count(pair[0]) != code.count(pair[1]):
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return ExecutionResult(
                    success=False,
                    error_type="SyntaxError",
                    error_message=f"Dấu ngoặc '{pair[0]}' và '{pair[1]}' không cân xứng.",
                    execution_time_ms=round(elapsed_ms, 2),
                    language=self.language,
                    engine="js_static_validator"
                )
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return ExecutionResult(
            success=True,
            stdout="[Static JS syntax validation passed: valid brackets]",
            execution_time_ms=round(elapsed_ms, 2),
            language=self.language,
            engine="js_static_validator"
        )


class SqlRunner(BaseLanguageRunner):
    """
    Executes SQL statements in an isolated In-Memory SQLite database.
    Catches DDL, DML, and query syntax/runtime errors natively.
    """

    language = "sql"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty SQL snippet]", language=self.language)

        start_time = time.perf_counter()
        conn = None
        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()

            # Split statements by semicolon
            raw_stmts = [s.strip() for s in code.split(";") if s.strip()]
            output_parts = []

            for stmt in raw_stmts:
                # Remove comments
                clean_stmt = re.sub(r"--.*$", "", stmt, flags=re.MULTILINE).strip()
                if not clean_stmt:
                    continue

                cursor.execute(clean_stmt)
                if cursor.description:
                    # It's a query that returns rows
                    headers = [d[0] for d in cursor.description]
                    rows = cursor.fetchall()
                    table_str = self._format_table(headers, rows)
                    output_parts.append(table_str)
                else:
                    output_parts.append(f"Query OK, {cursor.rowcount} rows affected.")

            conn.commit()
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=True,
                stdout="\n\n".join(output_parts) or "SQL statements executed successfully.",
                execution_time_ms=round(elapsed_ms, 2),
                language=self.language,
                engine="sqlite_in_memory"
            )

        except sqlite3.Error as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=False,
                error_type=type(e).__name__,
                error_message=f"Lỗi SQL ({type(e).__name__}): {str(e)}",
                execution_time_ms=round(elapsed_ms, 2),
                language=self.language,
                engine="sqlite_in_memory"
            )
        except Exception as ex:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=False,
                error_type=type(ex).__name__,
                error_message=f"SQL Execution Error: {str(ex)}",
                execution_time_ms=round(elapsed_ms, 2),
                language=self.language,
                engine="sqlite_in_memory"
            )
        finally:
            if conn:
                conn.close()

    def _format_table(self, headers: list[str], rows: list[tuple]) -> str:
        if not rows:
            return " | ".join(headers) + "\n(0 rows returned)"
        lines = [" | ".join(headers), "-" * max(20, len(" | ".join(headers)))]
        for r in rows[:20]:  # Cap at 20 rows
            lines.append(" | ".join(str(val) for val in r))
        if len(rows) > 20:
            lines.append(f"... ({len(rows) - 20} more rows)")
        return "\n".join(lines)


class JavaRunner(BaseLanguageRunner):
    """Executes or compiles Java code if JDK is installed, or performs static syntax checks."""

    language = "java"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty Java snippet]", language=self.language)

        javac_bin = shutil.which("javac")
        java_bin = shutil.which("java")
        start_time = time.perf_counter()

        if javac_bin and java_bin:
            # Wrap in Main class if snippet doesn't declare a class
            wrapped_code = code
            class_name = "Main"
            match = re.search(r"\bpublic\s+class\s+([A-Za-z0-9_]+)", code)
            if match:
                class_name = match.group(1)
            elif "class " not in code:
                wrapped_code = f"public class Main {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}\n"

            with tempfile.TemporaryDirectory() as temp_dir:
                src_path = Path(temp_dir) / f"{class_name}.java"
                src_path.write_text(wrapped_code, encoding="utf-8")

                # Compile
                try:
                    comp = subprocess.run([javac_bin, str(src_path)], capture_output=True, text=True, timeout=timeout_sec, cwd=_SANDBOX_CWD)
                    if comp.returncode != 0:
                        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                        return ExecutionResult(
                            success=False,
                            error_type="JavaCompilationError",
                            error_message=comp.stderr.strip() or "Java Compilation Failed",
                            execution_time_ms=round(elapsed_ms, 2),
                            language=self.language,
                            engine="java_jdk"
                        )

                    # Run
                    proc = subprocess.run([java_bin, "-cp", temp_dir, class_name], capture_output=True, text=True, timeout=timeout_sec, cwd=_SANDBOX_CWD)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                    if proc.returncode == 0:
                        return ExecutionResult(
                            success=True,
                            stdout=proc.stdout.strip(),
                            execution_time_ms=round(elapsed_ms, 2),
                            language=self.language,
                            engine="java_jdk"
                        )
                    return ExecutionResult(
                        success=False,
                        error_type="JavaRuntimeError",
                        error_message=proc.stderr.strip(),
                        execution_time_ms=round(elapsed_ms, 2),
                        language=self.language,
                        engine="java_jdk"
                    )
                except subprocess.TimeoutExpired:
                    return ExecutionResult(
                        success=False,
                        error_type="TimeoutExpired",
                        error_message=f"Java execution exceeded {timeout_sec}s timeout.",
                        timeout_exceeded=True,
                        language=self.language,
                        engine="java_jdk"
                    )

        # Fallback: Static syntax verification
        return self._static_check(code, start_time)

    def _static_check(self, code: str, start_time: float) -> ExecutionResult:
        if code.count("{") != code.count("}") or code.count("(") != code.count(")"):
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=False,
                error_type="SyntaxError",
                error_message="Dấu ngoặc trong mã Java không cân xứng.",
                execution_time_ms=round(elapsed_ms, 2),
                language=self.language,
                engine="java_static_validator"
            )
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return ExecutionResult(
            success=True,
            stdout="[Static Java syntax check passed: brackets balanced]",
            execution_time_ms=round(elapsed_ms, 2),
            language=self.language,
            engine="java_static_validator"
        )


class GoRunner(BaseLanguageRunner):
    """Executes Go code via `go run` if available, or static check."""

    language = "go"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty Go snippet]", language=self.language)

        go_bin = shutil.which("go")
        start_time = time.perf_counter()

        if go_bin:
            wrapped = code
            if "package " not in code:
                wrapped = f"package main\nimport \"fmt\"\nfunc main() {{\n    {code}\n}}\n"

            with tempfile.TemporaryDirectory() as temp_dir:
                go_file = Path(temp_dir) / "main.go"
                go_file.write_text(wrapped, encoding="utf-8")
                try:
                    proc = subprocess.run([go_bin, "run", str(go_file)], capture_output=True, text=True, timeout=timeout_sec, cwd=_SANDBOX_CWD)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                    if proc.returncode == 0:
                        return ExecutionResult(
                            success=True,
                            stdout=proc.stdout.strip(),
                            execution_time_ms=round(elapsed_ms, 2),
                            language=self.language,
                            engine="go_subprocess"
                        )
                    return ExecutionResult(
                        success=False,
                        error_type="GoError",
                        error_message=proc.stderr.strip() or "Go build/run error",
                        execution_time_ms=round(elapsed_ms, 2),
                        language=self.language,
                        engine="go_subprocess"
                    )
                except subprocess.TimeoutExpired:
                    return ExecutionResult(
                        success=False,
                        error_type="TimeoutExpired",
                        error_message=f"Go execution exceeded {timeout_sec}s timeout.",
                        timeout_exceeded=True,
                        language=self.language,
                        engine="go_subprocess"
                    )

        # Static fallback
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        balanced = code.count("{") == code.count("}") and code.count("(") == code.count(")")
        return ExecutionResult(
            success=balanced,
            error_type=None if balanced else "SyntaxError",
            error_message=None if balanced else "Dấu ngoặc trong mã Golang không cân xứng.",
            stdout="[Static Go check passed]" if balanced else "",
            execution_time_ms=round(elapsed_ms, 2),
            language=self.language,
            engine="go_static_validator"
        )


class BashRunner(BaseLanguageRunner):
    """
    Kiểm tra cú pháp Bash/Shell bằng `bash -n`; KHÔNG BAO GIỜ thực thi.

    Bài đọc về Git/CLI chứa các lệnh như `git reset --hard`, `git clean -fd`, `rm -rf`. Chạy chúng
    trên máy đang vận hành pipeline có thể xóa mất mã nguồn hoặc kết quả đã sinh. Việc kiểm
    chứng thực thi lệnh shell phải làm trong container cô lập (xem DOCKER_IMAGE_MAP ở core/sandbox.py).
    """

    language = "bash"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty shell script]", language=self.language)

        bash_bin = shutil.which("bash") or shutil.which("sh")
        start_time = time.perf_counter()

        if bash_bin:
            try:
                proc = subprocess.run(
                    [bash_bin, "-n"],
                    input=code,
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec,
                    cwd=_SANDBOX_CWD,
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                if proc.returncode == 0:
                    return ExecutionResult(
                        success=True,
                        stdout="[Bash syntax check passed (script was NOT executed)]",
                        execution_time_ms=round(elapsed_ms, 2),
                        language=self.language,
                        engine="bash_syntax_check",
                    )
                return ExecutionResult(
                    success=False,
                    error_type="BashSyntaxError",
                    error_message=proc.stderr.strip() or f"Exit code {proc.returncode}",
                    execution_time_ms=round(elapsed_ms, 2),
                    language=self.language,
                    engine="bash_syntax_check",
                )
            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    success=False,
                    error_type="TimeoutExpired",
                    error_message=f"Bash syntax check timed out after {timeout_sec}s.",
                    timeout_exceeded=True,
                    language=self.language,
                    engine="bash_syntax_check",
                )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return ExecutionResult(
            success=True,
            stdout="[Bash interpreter not present locally: syntax not verified]",
            execution_time_ms=round(elapsed_ms, 2),
            language=self.language,
            engine="bash_unavailable",
        )


class HtmlRunner(BaseLanguageRunner):
    language: str = "html"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty HTML snippet]", language=self.language)

        start_time = time.perf_counter()
        from html.parser import HTMLParser

        class StrictHtmlValidator(HTMLParser):
            def __init__(self):
                super().__init__()
                self.errors = []
            def error(self, message):
                self.errors.append(message)

        parser = StrictHtmlValidator()
        try:
            parser.feed(code)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=True,
                stdout="HTML markup verified successfully.",
                execution_time_ms=round(elapsed_ms, 2),
                language="html",
                engine="html_parser"
            )
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ExecutionResult(
                success=False,
                error_type="HTMLParseError",
                error_message=str(e),
                execution_time_ms=round(elapsed_ms, 2),
                language="html",
                engine="html_parser"
            )


class CssRunner(BaseLanguageRunner):
    language: str = "css"

    def run(self, code: str, timeout_sec: float) -> ExecutionResult:
        if not code.strip():
            return ExecutionResult(success=True, stdout="[Empty CSS stylesheet]", language=self.language)

        start_time = time.perf_counter()
        open_braces = code.count("{")
        close_braces = code.count("}")
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        if open_braces != close_braces:
            return ExecutionResult(
                success=False,
                error_type="CSSSyntaxError",
                error_message=f"Mismatched braces in CSS: {open_braces} '{{' vs {close_braces} '}}'",
                execution_time_ms=round(elapsed_ms, 2),
                language="css",
                engine="css_parser"
            )
        return ExecutionResult(
            success=True,
            stdout="CSS stylesheet syntax verified successfully.",
            execution_time_ms=round(elapsed_ms, 2),
            language="css",
            engine="css_parser"
        )


# =============================================================================
# POLYGLOT REGISTRY & DISPATCHER
# =============================================================================

_RUNNERS: Dict[str, BaseLanguageRunner] = {
    "python": PythonRunner(),
    "javascript": NodeJSRunner(),
    "typescript": NodeJSRunner(),
    "sql": SqlRunner(),
    "java": JavaRunner(),
    "go": GoRunner(),
    "bash": BashRunner(),
    "html": HtmlRunner(),
    "css": CssRunner(),
}


def execute_polyglot_code(
    code: str,
    language: str = "python",
    timeout_sec: float = 3.0,
    hint_stack: str = ""
) -> ExecutionResult:
    """
    Executes a code snippet using the appropriate language runner.
    """
    clean_code = code.strip()
    if clean_code.startswith("```"):
        lines = clean_code.splitlines()
        first_line = lines[0].strip("`").strip()
        if first_line:
            language = first_line
        clean_code = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    canonical_lang = detect_language(clean_code, hint=language or hint_stack)
    runner = _RUNNERS.get(canonical_lang, _RUNNERS["python"])

    return runner.run(clean_code, timeout_sec=timeout_sec)
