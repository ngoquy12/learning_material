"""
core/artifact_status.py — Bộ từ vựng DUY NHẤT mô tả trạng thái một artifact học liệu.

Bối cảnh: trạng thái artifact trước đây là chuỗi tự do, viết thẳng tại chỗ. Khảo sát
toàn repo tìm ra 12 biến thể đang cùng tồn tại:

    "Approved"                          "Skipped"
    "Approved with Warnings"            "Skipped (Session 01 Orientation)"
    "Approved with Scope Warnings"      "Skipped (Exam Session)"
    "Pending"                           "Skipped (Project/Practice)"
    "Pending Human Review"              "Skipped (Moved to Session Level)"
    "PUBLISHED"                         "Skipped (Temporarily Commented Out)"

Ba vấn đề thật của cách làm cũ:

  1. **Lý do bị hàn vào giá trị.** Năm biến thể "Skipped (...)" không phải là năm
     trạng thái khác nhau — chúng là MỘT trạng thái kèm năm lý do khác nhau. Hệ quả:
     bất kỳ ai viết `status == "Skipped"` đều bỏ sót cả 5 biến thể, và câu hỏi đơn
     giản "bài này có bị bỏ qua không?" không trả lời được bằng một phép so sánh.

  2. **Ba mức "Approved" không phân biệt được bằng máy.** "Approved with Scope
     Warnings" nghĩa là học liệu ĐÃ XUẤT BẢN nhưng vi phạm phạm vi kiến thức và cần
     người rà lại — nghiêm trọng hơn hẳn "Approved". Nhưng cả hai đều bắt đầu bằng
     "Approved" và không có hàm nào phân loại, nên báo cáo cuối cùng chỉ in ra chuỗi
     và để người đọc tự nhận ra.

  3. **Không có trạng thái THẤT BẠI.** Khi một nhánh sản xuất song song ném exception,
     hệ thống chỉ print rồi đi tiếp; artifact đó giữ nguyên trạng thái cũ (thường là
     "Pending") và biến mất khỏi tầm nhìn. `cli/commands/workflow_cmd.py` đã dùng
     chuỗi "FAILED" như giá trị mặc định khi đọc không ra trạng thái — nhưng không có
     chỗ nào GHI ra nó.

Thiết kế: `ArtifactStatus` kế thừa `str` nên mọi so sánh `status == "Approved"` và mọi
checkpoint JSON cũ vẫn hoạt động nguyên vẹn — đây là điều kiện bắt buộc vì hệ thống có
sẵn các file checkpoint chứa chuỗi thô. Lý do bỏ qua được tách khỏi trạng thái qua
`skipped(reason)`, và mọi câu hỏi phân loại đi qua các hàm `is_*` thay vì so chuỗi.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional


class ArtifactStatus(str, Enum):
    """
    Trạng thái vòng đời của một artifact học liệu.

    Kế thừa `str` một cách CÓ CHỦ Ý: giá trị enum so sánh bằng và tuần tự hoá JSON
    y hệt chuỗi cũ, nên có thể thay thế dần từng call site mà không phá checkpoint
    đã ghi trên đĩa hay các test đang so với chuỗi thô.
    """

    # --- Chưa xử lý ---
    PENDING = "Pending"

    # --- Đạt chuẩn, có thể xuất bản ---
    APPROVED = "Approved"
    APPROVED_WITH_WARNINGS = "Approved with Warnings"
    # Xuất bản được nhưng vi phạm phạm vi kiến thức / lệch bối cảnh nghiệp vụ.
    # Cố ý KHÁC APPROVED: đây là lỗi sư phạm, phải nhìn thấy được trong báo cáo.
    APPROVED_WITH_SCOPE_WARNINGS = "Approved with Scope Warnings"

    # --- Cần người can thiệp ---
    PENDING_HUMAN_REVIEW = "Pending Human Review"

    # --- Không sản xuất ---
    SKIPPED = "Skipped"

    # --- Hỏng ---
    # Dùng khi một nhánh sản xuất ném exception. Trước đây không tồn tại, nên lỗi
    # nhánh chỉ hiện ra ở console rồi trôi mất.
    FAILED = "FAILED"

    # --- Cấp session: đã biên dịch và xuất bản xong ---
    PUBLISHED = "PUBLISHED"

    # Enum có mixin `str` in ra "ArtifactStatus.APPROVED" khi dùng str()/format().
    # Ép về giá trị thật để log và f-string giữ nguyên diện mạo như thời dùng chuỗi.
    def __str__(self) -> str:
        return self.value

    def __format__(self, format_spec: str) -> str:
        return format(self.value, format_spec)


# Ký tự phân tách lý do khỏi trạng thái trong dạng "Skipped (lý do)".
_REASON_OPEN = " ("
_REASON_CLOSE = ")"


def skipped(reason: str = "") -> str:
    """
    Dựng trạng thái BỎ QUA kèm lý do, ví dụ: `skipped("Exam Session")`.

    Trả về `str` chứ không phải thành viên enum, vì lý do là dữ liệu tự do không thể
    liệt kê hết. Cặp `skipped()` / `is_skipped()` mới là hợp đồng: ghi qua hàm này,
    đọc qua hàm kia, không nơi nào phải tự ghép chuỗi.
    """
    reason = (reason or "").strip()
    if not reason:
        return ArtifactStatus.SKIPPED.value
    return f"{ArtifactStatus.SKIPPED.value}{_REASON_OPEN}{reason}{_REASON_CLOSE}"


def base_status(value: Any) -> str:
    """
    Bóc phần lý do, trả về trạng thái gốc.

    "Skipped (Exam Session)" -> "Skipped"; "Approved" -> "Approved".
    """
    text = str(value or "").strip()
    head, sep, _ = text.partition(_REASON_OPEN)
    return head.strip() if sep else text


def reason_of(value: Any) -> str:
    """Trả về phần lý do trong ngoặc, hoặc chuỗi rỗng nếu không có."""
    text = str(value or "").strip()
    _, sep, tail = text.partition(_REASON_OPEN)
    if not sep or not tail.endswith(_REASON_CLOSE):
        return ""
    return tail[: -len(_REASON_CLOSE)].strip()


def normalize(value: Any) -> Optional[ArtifactStatus]:
    """
    Ánh xạ một giá trị trạng thái bất kỳ (kể cả chuỗi thô từ checkpoint cũ) về đúng
    thành viên enum. Trả None nếu không nhận diện được — cố ý KHÔNG đoán bừa, vì đoán
    sai một trạng thái là xuất bản nhầm học liệu chưa đạt.
    """
    if isinstance(value, ArtifactStatus):
        return value
    head = base_status(value)
    if not head:
        return None
    for member in ArtifactStatus:
        if member.value.lower() == head.lower():
            return member
    return None


def is_skipped(value: Any) -> bool:
    """Đúng với cả "Skipped" lẫn mọi biến thể "Skipped (lý do)"."""
    return normalize(value) is ArtifactStatus.SKIPPED


def is_approved(value: Any) -> bool:
    """
    Đúng với CẢ BA mức đạt chuẩn (kể cả có cảnh báo).

    Dùng khi câu hỏi là "có cần sinh lại không?". Nếu câu hỏi là "có sạch hoàn toàn
    không?" thì phải so trực tiếp với `ArtifactStatus.APPROVED`.
    """
    return normalize(value) in {
        ArtifactStatus.APPROVED,
        ArtifactStatus.APPROVED_WITH_WARNINGS,
        ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS,
    }


def needs_human_review(value: Any) -> bool:
    """
    Artifact đã xuất bản nhưng PHẢI có người rà lại.

    Gồm cả `APPROVED_WITH_SCOPE_WARNINGS`: vi phạm phạm vi kiến thức là lỗi sư phạm,
    không phải cảnh báo trình bày — gộp nó vào nhóm "đã duyệt" là giấu mất vấn đề.
    """
    return normalize(value) in {
        ArtifactStatus.PENDING_HUMAN_REVIEW,
        ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS,
    }


def is_failed(value: Any) -> bool:
    """Artifact hỏng do exception, không phải do bị bỏ qua có chủ đích."""
    return normalize(value) is ArtifactStatus.FAILED


def is_terminal(value: Any) -> bool:
    """
    Trạng thái đã chốt, pipeline không cần đụng lại: đạt chuẩn, bỏ qua, hoặc đã
    xuất bản. `PENDING`, `PENDING_HUMAN_REVIEW` và `FAILED` đều KHÔNG phải terminal.
    """
    status = normalize(value)
    return (
        is_approved(status)
        or status is ArtifactStatus.SKIPPED
        or status is ArtifactStatus.PUBLISHED
    )


__all__ = [
    "ArtifactStatus",
    "skipped",
    "base_status",
    "reason_of",
    "normalize",
    "is_skipped",
    "is_approved",
    "needs_human_review",
    "is_failed",
    "is_terminal",
]
