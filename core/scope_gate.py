"""
core/scope_gate.py — Cổng kiểm định Phạm vi kiến thức & Bối cảnh nghiệp vụ.

Hai hợp đồng sư phạm cốt lõi của hệ thống:

  1. Scope Boundary Contract — bài học thứ N tuyệt đối không được dùng khái niệm chỉ
     được dạy ở bài thứ N+k. Vi phạm điều này là dạy cái chưa dạy: học viên gặp thuật
     ngữ lạ giữa bài và mất mạch, còn bài kiểm tra thì đánh giá thứ chưa hề được dạy.

  2. Domain Persistence Contract — một session chỉ dùng MỘT bối cảnh nghiệp vụ xuyên
     suốt. Mỗi bài tự bịa một bối cảnh khác nhau buộc học viên nạp lại ngữ cảnh liên
     tục, làm loãng phần kiến thức thật sự cần học.

Trước đây hai hợp đồng này chỉ được kiểm tra bằng lệnh print rải rác trong từng
creator: phát hiện được vi phạm nhưng KHÔNG làm gì cả — cảnh báo trôi qua console
rồi biến mất, học liệu lỗi vẫn được xuất bản. Module này gom logic kiểm định về một
chỗ và trả kết quả có cấu trúc để pipeline có thể sinh lại nội dung, thay vì chỉ log.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

# Tầng kiểm định ngữ nghĩa là OPT-IN. Nó tốn thêm một lượt gọi LLM cho mỗi artifact
# mà tầng từ khoá đã cho qua, nên bật hay không là quyết định về chi phí của người
# vận hành, không phải mặc định do hệ thống tự áp.
SEMANTIC_SCOPE_AUDIT_ENABLED = os.getenv("SCOPE_AUDIT_SEMANTIC", "").strip().lower() in (
    "1",
    "true",
    "yes",
)

# Cắt bớt nội dung gửi cho bộ thẩm định: một bài đọc HTML đầy đủ có thể dài hàng
# chục nghìn ký tự, phần lớn là khung giao diện chứ không phải nội dung dạy học.
_SEMANTIC_AUDIT_MAX_CHARS = 12000

from core.artifact_status import ArtifactStatus

# Trạng thái artifact khi đã hết số lần sinh lại mà vẫn còn vi phạm phạm vi.
# Cố ý KHÁC "Approved": artifact vẫn được xuất bản để không chặn cả tiến trình,
# nhưng phải nhìn thấy được trong báo cáo là nó cần người rà lại.
# Định nghĩa gốc nằm ở core/artifact_status.py; tên này giữ lại làm alias tương
# thích ngược cho các module đang import STATUS_SCOPE_WARNING từ đây.
STATUS_SCOPE_WARNING = ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS


@dataclass(frozen=True)
class ScopeAuditResult:
    """Kết quả kiểm định một artifact."""

    artifact: str
    violations: List[str] = field(default_factory=list)
    domain_drift: bool = False
    expected_domain: str = ""

    @property
    def is_clean(self) -> bool:
        return not self.violations and not self.domain_drift

    def as_feedback(self) -> str:
        """Diễn giải vi phạm thành phản hồi để nạp lại cho LLM khi sinh lại."""
        parts = []
        if self.violations:
            parts.append(
                "Nội dung đã dùng các khái niệm CHƯA được dạy tính đến bài này: "
                + ", ".join(self.violations)
                + ". Hãy viết lại chỉ bằng những kiến thức đã học, tuyệt đối không "
                "nhắc tới các khái niệm trên (kể cả trong chú thích hay tên biến)."
            )
        if self.domain_drift:
            parts.append(
                f"Nội dung đã lệch khỏi bối cảnh nghiệp vụ thống nhất của session "
                f"('{self.expected_domain}'). Hãy viết lại toàn bộ ví dụ và bài tập "
                f"trong đúng bối cảnh '{self.expected_domain}'."
            )
        return " ".join(parts)


def extract_forbidden_scope(state: Dict[str, Any]) -> Set[str]:
    """Lấy tập khái niệm bị cấm từ state, đã chuẩn hoá về chữ thường."""
    raw = state.get("forbidden_scope") or []
    if not isinstance(raw, list):
        return set()
    return {str(x).strip().lower() for x in raw if str(x).strip()}


def _strip_markup(text: str) -> str:
    """
    Bỏ thẻ HTML và khối <script>/<style> trước khi đưa cho bộ thẩm định.

    Khung giao diện chiếm phần lớn độ dài một bài đọc nhưng không mang nội dung dạy
    học nào. Gửi nguyên cả trang vừa tốn token vừa làm loãng thứ cần soi.
    """
    without_code = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    without_tags = re.sub(r"<[^>]+>", " ", without_code)
    return re.sub(r"\s+", " ", without_tags).strip()


def semantic_scope_audit(
    text: str,
    forbidden_scope: Set[str],
    tech_stack: str = "",
    session_id: str = "",
    lesson_id: str = "",
) -> List[str]:
    """
    TẦNG 2: bắt vi phạm phạm vi mà đối sánh từ khoá không thể thấy.

    Tầng 1 (`validate_text_against_scope`) so khớp chính xác tên khái niệm bị cấm
    theo ranh giới từ. Nó bỏ lọt ba dạng vi phạm phổ biến:

      1. Diễn đạt bằng từ đồng nghĩa tiếng Việt — "tập hợp" thay cho `set`,
         "từ điển" thay cho `dictionary`.
      2. Dùng khái niệm mà không hề gọi tên nó — viết `{1, 2, 3}` hay
         `[x for x in items]` trong bài chưa dạy set / list comprehension.
      3. Giải thích vòng vo về cơ chế của bài sau mà tránh dùng thuật ngữ.

    Cả ba đều là "dạy cái chưa dạy" y hệt nhau dưới góc nhìn của học viên.

    Trả về danh sách khái niệm bị cấm mà bộ thẩm định khẳng định là có xuất hiện.
    KHÔNG bao giờ ném lỗi và không bao giờ trả về khái niệm nằm ngoài danh sách cấm
    (xem phần lọc bên dưới) — một cổng kiểm định tự bịa ra vi phạm còn tệ hơn là
    không có cổng nào.
    """
    if not text or not forbidden_scope:
        return []

    content = _strip_markup(text)[:_SEMANTIC_AUDIT_MAX_CHARS]
    if len(content) < 200:
        return []

    forbidden_list = sorted(forbidden_scope)

    system_prompt = (
        "You are a strict curriculum scope auditor for programming course materials. "
        "You are given a list of concepts that have NOT been taught yet at this point "
        "in the syllabus, and a piece of lesson content. "
        "Report every forbidden concept that the content actually uses, teaches, or "
        "demonstrates — INCLUDING when it is expressed indirectly: a Vietnamese "
        "synonym, a paraphrase, or working code that relies on the concept without "
        "naming it. "
        "Do NOT report a concept merely because the content warns learners against it "
        "or says it will be covered later. "
        "Do NOT report anything that is not in the provided forbidden list. "
        'Answer with JSON only: {"violations": [{"concept": "<exact item from the '
        'forbidden list>", "evidence": "<short quote from the content>"}]}. '
        'If there is no violation, answer {"violations": []}.'
    )

    user_prompt = (
        f"Technology stack: {tech_stack or 'unspecified'}\n"
        f"Concepts NOT yet taught (forbidden): {', '.join(forbidden_list)}\n\n"
        f"Lesson content to audit:\n{content}"
    )

    try:
        from core.llm import call_llm
        from core.utils.llm_parser import extract_json_from_response

        raw = call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=True,
            agent_name="Scope_Auditor",
            session_id=session_id,
            lesson_id=lesson_id,
        )
        parsed = extract_json_from_response(raw, default={}) or {}
    except Exception as e:
        # Giữ đúng hợp đồng của module: trục trặc ở khâu kiểm định không được làm
        # chết tiến trình sinh học liệu.
        print(f"  [Scope Gate] Bỏ qua kiểm định ngữ nghĩa (lỗi gọi LLM): {e}")
        return []

    if not isinstance(parsed, dict):
        return []

    # Chỉ chấp nhận khái niệm CÓ THẬT trong danh sách cấm. Bộ thẩm định là một mô
    # hình ngôn ngữ: nó hoàn toàn có thể trả về một khái niệm nghe hợp lý nhưng
    # không hề nằm trong phạm vi cấm, và khi đó ta sẽ bắt hệ thống sinh lại một bài
    # học vốn không có lỗi gì.
    lowered = {c.lower(): c for c in forbidden_list}
    confirmed: List[str] = []
    for item in parsed.get("violations") or []:
        if isinstance(item, dict):
            concept = str(item.get("concept", "")).strip()
        else:
            concept = str(item).strip()
        canonical = lowered.get(concept.lower())
        if canonical and canonical not in confirmed:
            confirmed.append(canonical)

    return confirmed


def audit_artifact_scope(
    text: str,
    state: Dict[str, Any],
    artifact: str,
    check_domain: bool = True,
    semantic: Optional[bool] = None,
) -> ScopeAuditResult:
    """
    Kiểm định một artifact đã sinh xong.

    Args:
        text: Nội dung artifact (HTML hoặc Markdown đều được).
        state: AgentState, để lấy forbidden_scope / chosen_domain / technology_stack.
        artifact: Tên artifact, dùng cho log và báo cáo (vd "html", "practical_lab").
        check_domain: Tắt khi artifact không mang bối cảnh nghiệp vụ (vd kịch bản video
            dẫn nhập) — kiểm tra domain ở đó chỉ tạo báo động giả.
        semantic: Bật/tắt tầng kiểm định ngữ nghĩa cho riêng lần gọi này. Để None thì
            theo biến môi trường SCOPE_AUDIT_SEMANTIC.

    Không bao giờ ném lỗi: kiểm định hỏng thì coi như sạch, vì để một trục trặc ở
    khâu kiểm định làm chết cả tiến trình sinh học liệu là cái giá quá đắt.
    """
    if not text:
        return ScopeAuditResult(artifact=artifact)

    violations: List[str] = []
    forbidden = extract_forbidden_scope(state)
    tech_stack = state.get("technology_stack") or state.get("tech_stack") or ""

    if forbidden:
        # TẦNG 1 — đối sánh từ khoá: rẻ, tất định, chạy mọi lần.
        try:
            from core.scope_calculator import validate_text_against_scope
            violations = validate_text_against_scope(text, forbidden, tech_stack)
        except Exception as e:
            print(f"  [Scope Gate] Không chạy được kiểm định phạm vi cho '{artifact}': {e}")

        # TẦNG 2 — kiểm định ngữ nghĩa, CHỈ chạy khi tầng 1 không thấy gì. Tầng 1 đã
        # bắt được thì nội dung chắc chắn phải sinh lại, tốn thêm một lượt gọi LLM để
        # khẳng định lại điều đã biết là vô nghĩa.
        use_semantic = SEMANTIC_SCOPE_AUDIT_ENABLED if semantic is None else semantic
        if use_semantic and not violations:
            semantic_hits = semantic_scope_audit(
                text,
                forbidden,
                tech_stack,
                session_id=str(state.get("session_id", "")),
                lesson_id=str(state.get("lesson_id", "")),
            )
            if semantic_hits:
                print(
                    f"  [Scope Gate] Kiểm định ngữ nghĩa bắt được vi phạm mà đối sánh "
                    f"từ khoá bỏ lọt ở '{artifact}': {semantic_hits}"
                )
                violations = semantic_hits

    expected_domain = str(state.get("chosen_domain") or "").strip()
    domain_drift = bool(
        check_domain
        and expected_domain
        and expected_domain.lower() not in text.lower()
    )

    return ScopeAuditResult(
        artifact=artifact,
        violations=violations,
        domain_drift=domain_drift,
        expected_domain=expected_domain,
    )


def record_scope_audit(state: Dict[str, Any], result: ScopeAuditResult) -> None:
    """
    Ghi kết quả kiểm định vào state để nó hiện ra ở báo cáo cuối, không chỉ ở console.

    Cảnh báo chỉ in ra màn hình thì không ai đọc — đó chính là lý do các vi phạm
    phạm vi trước đây trôi lọt tới tận sản phẩm cuối.
    """
    if result.is_clean:
        return

    session_id = state.get("session_id", "Session")
    lesson_id = state.get("lesson_id", "")

    if result.violations:
        print(
            f"  [Scope Gate] {session_id} - {lesson_id} | '{result.artifact}' dùng khái "
            f"niệm chưa học: {result.violations}"
        )
    if result.domain_drift:
        print(
            f"  [Scope Gate] {session_id} - {lesson_id} | '{result.artifact}' lệch khỏi "
            f"bối cảnh thống nhất '{result.expected_domain}'"
        )

    audits = state.setdefault("scope_audits", {})
    audits[result.artifact] = {
        "violations": list(result.violations),
        "domain_drift": result.domain_drift,
        "expected_domain": result.expected_domain,
    }

    state.setdefault("review_logs", []).append({
        "source": "Scope_Gate",
        "artifact": result.artifact,
        "feedback": result.as_feedback(),
    })
