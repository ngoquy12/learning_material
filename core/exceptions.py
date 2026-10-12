"""Lỗi dùng chung của pipeline sinh học liệu."""


class GenerationError(RuntimeError):
    """
    Creator không sinh được nội dung hợp lệ.

    Dùng thay cho việc ghi nội dung mẫu/placeholder rồi báo thành công: nội dung giả
    qua được reviewer (reviewer chỉ đọc cấu trúc) và đến tay học viên như bài thật.
    """
