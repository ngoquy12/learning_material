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

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

# Trạng thái artifact khi đã hết số lần sinh lại mà vẫn còn vi phạm phạm vi.
# Cố ý KHÁC "Approved": artifact vẫn được xuất bản để không chặn cả tiến trình,
# nhưng phải nhìn thấy được trong báo cáo là nó cần người rà lại.
STATUS_SCOPE_WARNING = "Approved with Scope Warnings"


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


def audit_artifact_scope(
    text: str,
    state: Dict[str, Any],
    artifact: str,
    check_domain: bool = True,
) -> ScopeAuditResult:
    """
    Kiểm định một artifact đã sinh xong.

    Args:
        text: Nội dung artifact (HTML hoặc Markdown đều được).
        state: AgentState, để lấy forbidden_scope / chosen_domain / technology_stack.
        artifact: Tên artifact, dùng cho log và báo cáo (vd "html", "practical_lab").
        check_domain: Tắt khi artifact không mang bối cảnh nghiệp vụ (vd kịch bản video
            dẫn nhập) — kiểm tra domain ở đó chỉ tạo báo động giả.

    Không bao giờ ném lỗi: kiểm định hỏng thì coi như sạch, vì để một trục trặc ở
    khâu kiểm định làm chết cả tiến trình sinh học liệu là cái giá quá đắt.
    """
    if not text:
        return ScopeAuditResult(artifact=artifact)

    violations: List[str] = []
    forbidden = extract_forbidden_scope(state)
    tech_stack = state.get("technology_stack") or state.get("tech_stack") or ""

    if forbidden:
        try:
            from core.scope_calculator import validate_text_against_scope
            violations = validate_text_against_scope(text, forbidden, tech_stack)
        except Exception as e:
            print(f"  [Scope Gate] Không chạy được kiểm định phạm vi cho '{artifact}': {e}")

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
