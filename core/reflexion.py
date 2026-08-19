"""
core/reflexion.py
Multi-Turn Reflexion and Self-Healing Engine.
Categorizes pedagogical and technical violations into tiered severities:
- Tier 1: Auto-patchable via BeautifulSoup DOM AST (zero token cost).
- Tier 2: Code Runtime Errors from Sandbox -> Targeted code patch prompt.
- Tier 3: Scope / Pedagogical Violations -> Targeted instruction refinement prompt.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup
from core.sandbox.code_executor import execute_code_snippet, ExecutionResult

class ViolationSeverity(str, Enum):
    TIER_1_AST_AUTOPATCH = "TIER_1_AST_AUTOPATCH"
    TIER_2_RUNTIME_ERROR = "TIER_2_RUNTIME_ERROR"
    TIER_3_PEDAGOGICAL_SCOPE = "TIER_3_PEDAGOGICAL_SCOPE"
    TIER_4_FATAL_SCHEMA = "TIER_4_FATAL_SCHEMA"

@dataclass
class ReflexionViolation:
    rule_id: str
    severity: ViolationSeverity
    message: str
    target_section: Optional[str] = None
    suggested_patch: Optional[str] = None
    runtime_traceback: Optional[str] = None

@dataclass
class ReflexionPlan:
    is_valid: bool
    requires_llm_reprompt: bool
    violations: List[ReflexionViolation] = field(default_factory=list)
    auto_patched_content: Optional[str] = None
    targeted_feedback_prompt: str = ""


class ReflexionEngine:
    """
    Intelligent Reflexion Engine that decides whether to auto-patch locally
    or generate focused feedback for multi-turn LLM re-prompting.
    """

    MAX_REFLEXION_ATTEMPTS = 3

    @classmethod
    def auto_patch_ast_violations(cls, html_content: str) -> str:
        """
        Fixes Tier-1 formatting violations directly in DOM AST without LLM calls:
        1. Wraps raw <table> in <div class="overflow-x-auto my-4 ...">
        2. Wraps bare <img> captions in <i> or adds missing italics.
        3. Strips stray dark mode background classes from non-code containers.
        """
        if not html_content or "<" not in html_content:
            return html_content

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # 1. Auto-wrap tables in overflow containers
            for table in soup.find_all("table"):
                parent = table.parent
                if parent and "overflow-x-auto" not in parent.get("class", []):
                    wrapper = soup.new_tag("div", attrs={"class": "overflow-x-auto my-6 border border-slate-200 rounded-xl"})
                    table.wrap(wrapper)

            # 2. Ensure image captions have italic styling
            for figcaption in soup.find_all("figcaption"):
                if not figcaption.find("i") and not figcaption.find("em"):
                    inner_text = figcaption.get_text()
                    figcaption.string = ""
                    italic_tag = soup.new_tag("i")
                    italic_tag.string = inner_text
                    figcaption.append(italic_tag)

            # 3. Strip dark mode on normal containers (except pre/code/terminal)
            for div in soup.find_all(["div", "section", "article"]):
                classes = div.get("class", [])
                if any(k in classes for k in ["terminal", "code-tracker", "visualizer", "hljs"]):
                    continue
                if "bg-slate-900" in classes or "bg-black" in classes:
                    classes = [c for c in classes if c not in ["bg-slate-900", "bg-black", "bg-gray-900"]]
                    classes.append("bg-slate-50")
                    div["class"] = classes

            return str(soup)
        except Exception:
            return html_content

    @classmethod
    def verify_embedded_code_runtime(cls, html_or_text: str, tech_stack: str = "python") -> List[ReflexionViolation]:
        """
        Extracts code snippets from content and executes them in the sandbox.
        """
        import re
        import textwrap
        violations = []
        code_blocks = re.findall(r'```(?:python|py)?\n(.*?)```', html_or_text, re.DOTALL)

        for idx, code in enumerate(code_blocks, 1):
            clean_code = textwrap.dedent(code).strip()
            # Skip empty or partial code lines
            if len(clean_code.splitlines()) < 2:
                continue

            result: ExecutionResult = execute_code_snippet(clean_code, tech_stack=tech_stack, timeout_sec=3.0)
            if not result.success:
                violations.append(ReflexionViolation(
                    rule_id="CODE_RUNTIME_FAILURE",
                    severity=ViolationSeverity.TIER_2_RUNTIME_ERROR,
                    message=f"Mã nguồn ví dụ #{idx} phát sinh lỗi Runtime ({result.error_type}): {result.error_message}",
                    target_section=f"Section 3 - Code Block #{idx}",
                    runtime_traceback=result.traceback,
                    suggested_patch=f"Sửa lại mã nguồn để không gây ra {result.error_type}."
                ))

        return violations

    @classmethod
    def create_targeted_feedback(cls, violations: List[ReflexionViolation]) -> str:
        """
        Builds clear, focused feedback instructions for the next LLM revision turn.
        """
        if not violations:
            return ""

        feedback_lines = [
            "### PHẢN HỒI KIỂM ĐỊNH TỰ ĐỘNG & YÊU CẦU SỬA ĐỔI (REFLEXION AUDIT FEEDBACK):",
            "Vui lòng đọc kỹ các lỗi vi phạm dưới đây và chỉnh sửa chính xác trong lần sinh này:\n"
        ]

        for idx, v in enumerate(violations, 1):
            feedback_lines.append(f"{idx}. [{v.severity.value}] Tại {v.target_section or 'Nội dung'}:")
            feedback_lines.append(f"   - Lỗi: {v.message}")
            if v.runtime_traceback:
                feedback_lines.append(f"   - Traceback: `{v.runtime_traceback.splitlines()[-1]}`")
            if v.suggested_patch:
                feedback_lines.append(f"   - Hướng dẫn sửa: {v.suggested_patch}")
            feedback_lines.append("")

        return "\n".join(feedback_lines).strip()
