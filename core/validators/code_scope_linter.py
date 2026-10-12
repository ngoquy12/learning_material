"""
core/validators/code_scope_linter.py

Kiểm tra MÃ của bài tập/lab có dùng cấu trúc ngôn ngữ mà môn học chưa dạy hay không, và
các hàm dùng chung giữa các bài có bị lệch chữ ký hay không.

Vì sao cần: phạm vi kiến thức trước đây chỉ được kiểm bằng cách so từ khóa trong VĂN BẢN
(`core/scope_calculator.py`). Một đáp án mẫu vẫn có thể dùng closure, `class` hay `this`
mà không có từ khóa nào lọt qua, nên lỗi chỉ lộ ra khi người đọc tự phát hiện (ví dụ bài 6
môn JS nâng cao trả về các hàm dùng lại biến cục bộ của hàm cha trong khi môn đã cam kết
không dạy closure).

Module thuần Python, không gọi LLM, chạy được cả trong pipeline lẫn từ dòng lệnh
(`scripts/check_exercise_scope.py`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence, Tuple

# Mã cấu trúc có thể bị cấm. Tên ổn định để khai báo trong PM/skill/CLI.
JS_CONSTRUCTS = ("class", "this", "module", "closure")
PY_CONSTRUCTS = ("class", "global", "lambda", "comprehension", "decorator", "closure")


@dataclass
class ScopeFinding:
    construct: str
    line: int
    snippet: str

    def __str__(self) -> str:
        return f"dòng {self.line}: dùng '{self.construct}' chưa được dạy -> {self.snippet.strip()[:90]}"


@dataclass
class SymbolDrift:
    name: str
    signatures: Dict[str, List[str]] = field(default_factory=dict)  # tham số -> các file

    def __str__(self) -> str:
        parts = "; ".join(f"({sig}) ở {', '.join(files)}" for sig, files in self.signatures.items())
        return f"hàm '{self.name}' có nhiều chữ ký khác nhau: {parts}"


# ─────────────────────────────────────────────────────────────────────────────
# Làm sạch: bỏ chú thích và chuỗi để từ khóa trong chú thích không gây báo động giả
# ─────────────────────────────────────────────────────────────────────────────

def _strip_js(code: str) -> str:
    code = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), code, flags=re.S)
    code = re.sub(r"//[^\n]*", "", code)
    code = re.sub(r"`(?:\\.|[^`\\])*`", lambda m: "``" + "\n" * m.group(0).count("\n"), code, flags=re.S)
    code = re.sub(r'"(?:\\.|[^"\\\n])*"', '""', code)
    code = re.sub(r"'(?:\\.|[^'\\\n])*'", "''", code)
    return code


def _strip_py(code: str) -> str:
    code = re.sub(r'"""(?:.|\n)*?"""|\'\'\'(?:.|\n)*?\'\'\'', lambda m: '""' + "\n" * m.group(0).count("\n"), code)
    code = re.sub(r"#[^\n]*", "", code)
    code = re.sub(r'"(?:\\.|[^"\\\n])*"', '""', code)
    code = re.sub(r"'(?:\\.|[^'\\\n])*'", "''", code)
    return code


def _dedupe(findings: List[ScopeFinding]) -> List[ScopeFinding]:
    seen, out = set(), []
    for f in sorted(findings, key=lambda f: (f.line, f.construct)):
        if (f.line, f.construct) not in seen:
            seen.add((f.line, f.construct))
            out.append(f)
    return out


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


# ─────────────────────────────────────────────────────────────────────────────
# JavaScript
# ─────────────────────────────────────────────────────────────────────────────

_JS_FUNC_HEAD = re.compile(
    r"(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{"
    r"|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>\s*\{"
    r"|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(\w+)\s*=>\s*\{"
)


def _matching_brace(text: str, open_index: int) -> int:
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return len(text) - 1


def _top_level_functions_js(code: str) -> List[Tuple[str, str, int, int]]:
    """(tên, tham số, vị trí '{', vị trí '}') của các hàm KHÔNG lồng trong hàm khác."""
    found: List[Tuple[str, str, int, int]] = []
    pos = 0
    while True:
        m = _JS_FUNC_HEAD.search(code, pos)
        if not m:
            break
        name = m.group(1) or m.group(3) or m.group(5)
        params = (m.group(2) if m.group(1) else m.group(4) if m.group(3) else m.group(6)) or ""
        open_i = m.end() - 1
        close_i = _matching_brace(code, open_i)
        found.append((name, params.strip(), open_i, close_i))
        pos = close_i + 1
    return found


def _js_closure_findings(code: str) -> List[ScopeFinding]:
    """
    Closure ngầm: hàm cha khai báo biến/hàm cục bộ rồi TRẢ VỀ (hoặc đăng ký) một hàm con dùng
    lại các biến đó sau khi hàm cha kết thúc. Heuristic bắt dạng phổ biến nhất của bài tập:
    hàm cha có biến cục bộ và `return { tên, ... }` / `return () =>` chứa hàm con tham chiếu biến đó.
    Interceptor axios đăng ký bên trong hàm cha cũng được tính, nhưng chỉ khi biến cục bộ
    do chính hàm cha khai báo (không tính module-level).
    """
    findings: List[ScopeFinding] = []
    for name, _params, open_i, close_i in _top_level_functions_js(code):
        body = code[open_i + 1 : close_i]
        locals_ = set(re.findall(r"\b(?:const|let|var)\s+(\w+)\s*=", body))
        locals_ -= {name}
        if not locals_:
            continue

        # Hàm con khai báo trong thân hàm cha
        inner = [
            m for m in re.finditer(
                r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>"
                r"|(?:async\s+)?function\s+(\w+)\s*\(",
                body,
            )
        ]
        inner_names = {m.group(1) or m.group(2) for m in inner}
        returns_function = bool(
            re.search(r"return\s*\{[^}]*\}", body)
            and any(re.search(rf"\b{re.escape(n)}\b", re.search(r"return\s*\{([^}]*)\}", body).group(1)) for n in inner_names)
        ) or bool(re.search(r"return\s+(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>", body)) or bool(
            re.search(r"return\s+function\b", body)
        )
        if not returns_function:
            continue

        for im in inner:
            iname = im.group(1) or im.group(2)
            start = body.find("{", im.end() - 1)
            arrow_expr_end = body.find("\n", im.end())
            if start != -1 and (arrow_expr_end == -1 or start < arrow_expr_end + 400):
                end = _matching_brace(body, start)
                inner_body = body[start:end]
            else:
                inner_body = body[im.end() : arrow_expr_end if arrow_expr_end != -1 else len(body)]
            used = {v for v in locals_ - {iname} if re.search(rf"\b{re.escape(v)}\b", inner_body)}
            if used:
                line = _line_of(code, open_i + 1 + im.start())
                findings.append(
                    ScopeFinding(
                        "closure",
                        line,
                        f"hàm con '{iname}' trong '{name}' dùng lại biến cục bộ {sorted(used)} của hàm cha",
                    )
                )
    return findings


def find_js_scope_violations(code: str, forbidden: Iterable[str]) -> List[ScopeFinding]:
    forbidden = {f.lower() for f in forbidden}
    clean = _strip_js(code)
    findings: List[ScopeFinding] = []

    def scan(construct: str, pattern: str) -> None:
        if construct not in forbidden:
            return
        for m in re.finditer(pattern, clean):
            line = _line_of(clean, m.start())
            findings.append(ScopeFinding(construct, line, clean.splitlines()[line - 1]))

    scan("class", r"(?<![\w.])class\s+\w+")
    scan("this", r"(?<![\w.])this\b")
    scan("module", r"(?m)^\s*(?:import\s+[\w{*]|export\s+(?:default|const|function|class|\{))")
    if "closure" in forbidden:
        findings.extend(_js_closure_findings(clean))
    return _dedupe(findings)


# ─────────────────────────────────────────────────────────────────────────────
# Python
# ─────────────────────────────────────────────────────────────────────────────

def find_py_scope_violations(code: str, forbidden: Iterable[str]) -> List[ScopeFinding]:
    forbidden = {f.lower() for f in forbidden}
    clean = _strip_py(code)
    findings: List[ScopeFinding] = []

    def scan(construct: str, pattern: str) -> None:
        if construct not in forbidden:
            return
        for m in re.finditer(pattern, clean, flags=re.M):
            line = _line_of(clean, m.start())
            findings.append(ScopeFinding(construct, line, clean.splitlines()[line - 1]))

    scan("class", r"^\s*class\s+\w+")
    scan("global", r"^\s*(?:global|nonlocal)\s+\w+")
    scan("lambda", r"\blambda\b")
    scan("comprehension", r"[\[{(][^\n\[\]{}()]*\bfor\b[^\n\[\]{}()]*\bin\b[^\n]*[\]})]")
    scan("decorator", r"^\s*@\w+")
    if "closure" in forbidden:
        for m in re.finditer(r"^( *)def\s+(\w+)\s*\([^)]*\)\s*:\n((?:\1 +.*\n?|\n)+)", clean, flags=re.M):
            body = m.group(3)
            inner = re.search(r"^\s+def\s+(\w+)\s*\(", body, flags=re.M)
            locals_ = set(re.findall(r"^\s+(\w+)\s*=", body, flags=re.M))
            if inner and locals_ and re.search(rf"return\s+{inner.group(1)}\b", body):
                line = _line_of(clean, m.start())
                findings.append(ScopeFinding("closure", line, f"hàm '{m.group(2)}' trả về hàm con '{inner.group(1)}'"))
    return _dedupe(findings)


def find_scope_violations(code: str, language: str, forbidden: Iterable[str]) -> List[ScopeFinding]:
    lang = (language or "").lower()
    if lang in ("js", "javascript", "node", "ts", "typescript"):
        return find_js_scope_violations(code, forbidden)
    if lang in ("py", "python"):
        return find_py_scope_violations(code, forbidden)
    return []


# ─────────────────────────────────────────────────────────────────────────────
# Hàm dùng chung giữa các bài: cùng tên thì phải cùng chữ ký
# ─────────────────────────────────────────────────────────────────────────────

def _normalize_params(params: str) -> str:
    return re.sub(r"\s+", "", params.strip())


def collect_function_signatures(code: str, language: str = "javascript") -> Dict[str, str]:
    """{tên hàm cấp cao nhất: chuỗi tham số chuẩn hóa}."""
    lang = (language or "").lower()
    if lang in ("py", "python"):
        clean = _strip_py(code)
        return {m.group(1): _normalize_params(m.group(2)) for m in re.finditer(r"^def\s+(\w+)\s*\(([^)]*)\)", clean, flags=re.M)}
    clean = _strip_js(code)
    return {name: _normalize_params(params) for name, params, _o, _c in _top_level_functions_js(clean)}


def find_signature_drift(files: Dict[str, str], language: str = "javascript") -> List[SymbolDrift]:
    """
    `files`: {đường dẫn hiển thị: nội dung mã}. Trả về các hàm xuất hiện ở từ 2 file trở lên
    nhưng có HÌNH DẠNG tham số khác nhau (số lượng, có/không giá trị mặc định, có/không
    destructuring) - dấu hiệu bài sau dùng lại mã nền của bài trước nhưng hai bản đã lệch nhau.
    Chỉ khác tên tham số thì không tính (vô hại).
    """
    by_name: Dict[str, Dict[Tuple[str, ...], Dict[str, str]]] = {}
    for path, code in files.items():
        for name, sig in collect_function_signatures(code, language).items():
            by_name.setdefault(name, {}).setdefault(_param_shape(sig), {})[path] = sig
    drifts = []
    for name, shapes in sorted(by_name.items()):
        if len(shapes) > 1:
            drift = SymbolDrift(name)
            for shape, paths in shapes.items():
                sig = next(iter(paths.values()))
                drift.signatures.setdefault(sig, []).extend(paths)
            drifts.append(drift)
    return drifts


# ─────────────────────────────────────────────────────────────────────────────
# Mã nền (có sẵn, sinh viên không viết): không tính vào kiểm tra phạm vi
# ─────────────────────────────────────────────────────────────────────────────

_BASE_START = re.compile(r"^\s*(?://|#)\s*=*\s*(?:mã nền|phần có sẵn)", re.IGNORECASE)
_BASE_END = re.compile(
    r"^\s*(?://|#)\s*=*\s*(?:hết mã nền|bài làm|phần của bạn|phần cần viết|phần sinh viên)", re.IGNORECASE
)


def provided_code_lines(code: str) -> List[int]:
    """Số dòng (từ 1) thuộc khối mã nền, giữa dấu mở 'Mã nền/PHẦN CÓ SẴN' và dấu đóng."""
    lines = code.splitlines()
    inside = False
    result: List[int] = []
    for i, line in enumerate(lines, 1):
        if _BASE_END.match(line):
            inside = False
        elif _BASE_START.match(line):
            inside = True
        if inside:
            result.append(i)
    return result


def mask_lines(code: str, line_numbers: Iterable[int]) -> str:
    """Thay các dòng được chọn bằng dòng trống, giữ nguyên số dòng của phần còn lại."""
    skip = set(line_numbers)
    return "\n".join("" if i in skip else line for i, line in enumerate(code.splitlines(), 1))


def mask_lines_matching(code: str, reference_code: str) -> str:
    """Che mọi dòng của `code` trùng (sau strip) với một dòng nằm trong khối mã nền của `reference_code`."""
    ref = reference_code.splitlines()
    base = {ref[i - 1].strip() for i in provided_code_lines(reference_code) if ref[i - 1].strip()}
    return "\n".join("" if line.strip() in base else line for line in code.splitlines())


def _param_shape(params: str) -> Tuple[str, ...]:
    parts, depth, cur = [], 0, ""
    for ch in params:
        if ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    shape = []
    for p in parts:
        p = p.strip()
        if p.startswith("..."):
            shape.append("rest")
        elif p.startswith("{") or p.startswith("["):
            shape.append("destructured")
        elif "=" in p:
            shape.append("default")
        else:
            shape.append("plain")
    return tuple(shape)
