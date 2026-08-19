"""
core/sanitizers/diacritics_sanitizer.py
Vietnamese diacritics normalization, AI cliché filtering, and buzzword cleaners.
"""

import re

VIETNAMESE_REPLACEMENTS = {
    r"\btai sao\b": "tại sao",
    r"\bTai sao\b": "Tại sao",
    r"\bnguoi dung\b": "người dùng",
    r"\bNguoi dung\b": "Người dùng",
    r"\bchuoi\b": "chuỗi",
    r"\bChuoi\b": "Chuỗi",
    r"\bket qua\b": "kết quả",
    r"\bKet qua\b": "Kết quả",
    r"\btoan tu\b": "toán tử",
    r"\bToan tu\b": "Toán tử",
    r"\bdoanh nghiep\b": "doanh nghiệp",
    r"\bDoanh nghiep\b": "Doanh nghiệp",
    r"\bbai doc\b": "bài đọc",
    r"\bBai doc\b": "Bài đọc",
    r"\bngon ngu\b": "ngôn ngữ",
    r"\bNgon ngu\b": "Ngôn ngữ",
    r"\blap trinh\b": "lập trình",
    r"\bLap trinh\b": "Lập trình",
    r"\bkhoang trang\b": "khoảng trắng",
    r"\bKhoang trang\b": "Khoảng trắng",
    r"\bdu thua\b": "dư thừa",
    r"\bDu thua\b": "Dư thừa",
    r"\bvi sao\b": "vì sao",
    r"\bVi sao\b": "Vì sao",
    r"\bthuc te\b": "thực tế",
    r"\bThuc te\b": "Thực tế",
    r"\bhieu nang\b": "hiệu năng",
    r"\bHieu nang\b": "Hiệu năng",
    r"\bnguy co\b": "nguy cơ",
    r"\bNguy co\b": "Nguy cơ",
    r"\bhe thong\b": "hệ thống",
    r"\bHe thong\b": "Hệ thống",
    r"\bco so du lieu\b": "cơ sở dữ liệu",
    r"\bCo so du lieu\b": "Cơ sở dữ liệu",
    r"\bphep so sanh\b": "phép so sánh",
    r"\bPhep so sanh\b": "Phép so sánh",
    r"\bxac thuc\b": "xác thực",
    r"\bXac thuc\b": "Xác thực",
    r"\btrung lap\b": "trùng lặp",
    r"\bTrung lap\b": "Trùng lặp",
    r"\bbien\b": "biến",
    r"\bBien\b": "Biến",
    r"\bgia tri\b": "giá trị",
    r"\bGia tri\b": "Giá trị",
    r"\bdu lieu\b": "dữ liệu",
    r"\bDu lieu\b": "Dữ liệu",
    r"\bmo ta\b": "mô tả",
    r"\bMo ta\b": "Mô tả",
    r"\bgiai thich\b": "giải thích",
    r"\bGiai thich\b": "Giải thích",
    r"\bphan tich\b": "phân tích",
    r"\bPhan tich\b": "Phân tích",
    r"\bcho biet\b": "cho biết",
    r"\bCho biet\b": "Cho biết",
    r"\btrinh bay\b": "trình bày",
    r"\bTrinh bay\b": "Trình bày",
    r"\bso sanh\b": "so sánh",
    r"\bSo sanh\b": "So sánh",
    r"\bkhai niem\b": "khái niệm",
    r"\bKhai niem\b": "Khái niệm",
    r"\bcot loi\b": "cốt lõi",
    r"\bCot loi\b": "Cốt lõi",
    r"\bnguyen ly\b": "nguyên lý",
    r"\bNguyen ly\b": "Nguyên lý",
    r"\bhoat dong\b": "hoạt động",
    r"\bHoat dong\b": "Hoạt động",
    r"\bphong tranh\b": "phòng tránh",
    r"\bPhong tranh\b": "Phòng tránh",
    r"\blam chu\b": "làm chủ",
    r"\bLam chu\b": "Làm chủ",
    r"\bnen tang\b": "nền tảng",
    r"\bNen tang\b": "Nền tảng",
    r"\bchinh xac\b": "chính xác",
    r"\bChinh xac\b": "Chính xác",
    r"\btuan thu\b": "tuân thủ",
    r"\bTuan thu\b": "Tuân thủ",
    r"\bquy tac\b": "quy tắc",
    r"\bQuy tac\b": "Quy tắc",
    r"\bcu phap\b": "cú pháp",
    r"\bCu phap\b": "Cú pháp",
    r"\bdinh dang\b": "định dạng",
    r"\bDinh dang\b": "Định dạng",
    r"\bkiem tra\b": "kiểm tra",
    r"\bKiem tra\b": "Kiểm tra",
    r"\bdau ra\b": "đầu ra",
    r"\bDau ra\b": "Đầu ra",
    r"\bdau vao\b": "đầu vào",
    r"\bDau vao\b": "Đầu vào",
    r"\bcan than\b": "cẩn thận",
    r"\bCan than\b": "Cẩn thận",
    r"\bvan dung\b": "vận dụng",
    r"\bVan dung\b": "Vận dụng",
    r"\bluong\b": "luồng",
    r"\bLuong\b": "Luồng",
    r"\btinh toan\b": "tính toán",
    r"\bTinh toan\b": "Tính toán",
    r"\bbieu thuc\b": "biểu thức",
    r"\bBieu thuc\b": "Biểu thức",
    r"\bhien thi\b": "hiển thị",
    r"\bHien thi\b": "Hiển thị",
    r"\btruc quan\b": "trực quan",
    r"\bTruc quan\b": "Trực quan"
}

def ensure_vietnamese_diacritics(text: str) -> str:
    """Ensures unaccented Vietnamese phrases are converted to standard accented Vietnamese."""
    if not text or not isinstance(text, str):
        return text

    for pattern, repl in VIETNAMESE_REPLACEMENTS.items():
        text = re.sub(pattern, repl, text)

    return text

def clean_unwanted_text(text: str) -> str:
    """Removes W3Schools references, bracketed labels, and hyperbolic AI clichés."""
    if not text or not isinstance(text, str):
        return text
    text = re.sub(r"\bW3Schools\b", "Chuẩn Sư Phạm Quốc Tế", text, flags=re.IGNORECASE)
    text = re.sub(r"\[W3SCHOOLS\s+NOTE\]:?", "Lưu ý:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[NOTE\]:?", "Lưu ý:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[WARNING\]:?", "Cảnh báo:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[TIP\]:?", "Mẹo:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[BEST\s+PRACTICE\]:?", "Thực hành tốt:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[ANTI-PATTERN\]:?", "Mẫu nên tránh:", text, flags=re.IGNORECASE)
    text = re.sub(r"\[YÊU\s+CẦU\]:?", "Yêu cầu:", text, flags=re.IGNORECASE)
    
    # Scrub AI cliché words and buzzwords
    text = re.sub(r"\bbẫy lập trình\b", "Lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy cú pháp\b", "Lỗi cú pháp phổ biến", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy logic\b", "Lỗi logic phổ biến", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy lỗi\b", "Lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbẫy\b", "lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bBẫy\b", "Lỗi thường gặp", text)
    text = re.sub(r"\bGotcha\b", "Lỗi thường gặp", text, flags=re.IGNORECASE)
    text = re.sub(r"\bAnti-pattern\b", "Mẫu nên tránh", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbí kíp\b", "mẹo thực hành", text, flags=re.IGNORECASE)
    text = re.sub(r"\bthần thánh\b", "hiệu quả", text, flags=re.IGNORECASE)
    text = re.sub(r"\btất tần tật\b", "tổng quan đầy đủ", text, flags=re.IGNORECASE)

    text = re.sub(r"\bTIẾN TRÌNH LUỒNG CHẠY\b", "Tiến trình luồng chạy", text)
    text = re.sub(r"\bTỐC ĐỘ THỰC THI\b", "Tốc độ thực thi", text)
    text = re.sub(r"\bCODE TRACKER\b", "Code Tracker", text)
    text = re.sub(r"\bNHẬT KÝ THUẬT TOÁN\b", "Nhật ký thuật toán", text)
    text = re.sub(r"\bBẢNG SO SÁNH ĐẶC TÍNH KỸ THUẬT CHI TIẾT\b", "Bảng so sánh đặc tính kỹ thuật chi tiết", text)
    return text
