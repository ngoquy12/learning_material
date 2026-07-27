# core/course_architecture.py
"""
Systemic Course Architecture & Pedagogy Governance Engine.
Classifies sessions into strict Architecture Patterns and enforces 
architecture boundaries to prevent concept leakage between courses.
"""

import re
from typing import Dict, Any, List

# Core Architecture Patterns
ARCH_CLI_CORE = "CLI_CORE"
ARCH_WEB_BACKEND = "WEB_BACKEND"
ARCH_WEB_FRONTEND = "WEB_FRONTEND"
ARCH_MOBILE_APP = "MOBILE_APP"
ARCH_DATABASE_SQL = "DATABASE_SQL"
ARCH_DEVOPS_CLOUD = "DEVOPS_CLOUD"

def resolve_course_architecture(session_title: str, tech_stack: str, forbidden_scope: str = "", allowed_scope: str = "") -> Dict[str, Any]:
    """
    Classifies a session into a specific Architecture Pattern and returns
    strict architectural rules, dynamic SRS headers, and forbidden concepts.
    """
    title_lower = (session_title or "").lower()
    stack_lower = (tech_stack or "").lower()
    forbidden_lower = (forbidden_scope or "").lower()
    allowed_lower = (allowed_scope or "").lower()
    
    # Combined context for classification
    context = f"{title_lower} {stack_lower} {allowed_lower}"
    
    # 1. Determine Architecture Pattern
    if any(kw in context for kw in ["fastapi", "express", "spring boot", "django rest", "nest", "asp.net", "rest api", "backend api"]):
        pattern = ARCH_WEB_BACKEND
    elif any(kw in context for kw in ["react", "vue", "angular", "html", "css", "frontend", "dom", "ui component"]):
        pattern = ARCH_WEB_FRONTEND
    elif any(kw in context for kw in ["flutter", "react native", "android", "ios", "mobile"]):
        pattern = ARCH_MOBILE_APP
    elif any(kw in context for kw in ["sql", "postgres", "mysql", "database management", "csdl"]):
        pattern = ARCH_DATABASE_SQL
    elif any(kw in context for kw in ["docker", "k8s", "kubernetes", "devops", "aws", "ci/cd"]):
        pattern = ARCH_DEVOPS_CLOUD
    else:
        # Default to CLI Core for foundational programming sessions (Python Core, Java Core, C++ Core, C# Core)
        pattern = ARCH_CLI_CORE
        
    # Check if REST API / Web / File I/O / Class are explicitly forbidden in PM
    is_rest_forbidden = any(kw in forbidden_lower for kw in ["rest api", "web api", "fastapi", "swagger", "file i/o", "class"])
    if is_rest_forbidden and pattern == ARCH_WEB_BACKEND:
        pattern = ARCH_CLI_CORE
        
    # 2. Build Naming Conventions
    if any(k in stack_lower for k in ["javascript", "js", "typescript", "ts", "java", "c#", "csharp", "dart", "flutter", "go", "golang", "kotlin", "swift"]):
        case_style = "camelCase (hoặc PascalCase cho Class/Type/Component)"
        fn_example = "addItem(), filterByCategory(), calculateTotal()"
        var_example = "itemId, itemName, totalAmount"
    else:
        case_style = "snake_case"
        fn_example = "add_item(), filter_by_category(), calculate_total()"
        var_example = "item_id, item_name, total_amount"

    fn_first = fn_example.split(',')[0].strip()
    fn_second = fn_example.split(',')[1].strip()

    naming_guidelines = f"""QUY CHUẨN ĐẶT TÊN CODE CHUẨN MỰC ({tech_stack.upper()}):
1. 100% TIẾNG ANH CÓ NGHĨA: Tất cả tên biến, tên hàm, tên lớp, tên thuộc tính, khóa Dictionary/JSON (dict keys / JSON fields), và tham số BẮT BUỘC là TIẾNG ANH CÓ NGHĨA 100% (VD: `{var_example}`).
2. NGUYÊN TẮC CÚ PHÁP ({case_style}):
   - Tên hàm/phương thức: Dùng tiếng Anh chuẩn {case_style} (VD: `{fn_example}`).
   - Tên biến/khóa dữ liệu: Dùng tiếng Anh chuẩn {case_style} (VD: `{var_example}`).
3. CỘT 'TÊN CHỨC NĂNG/HÀM' TRONG BẢNG HTML:
   - Hiển thị Tên tiếng Việt rõ ràng bôi đậm, kèm tên hàm Tiếng Anh chuẩn bọc trong `<code>`.
   - Ví dụ đúng: <b>[Tên chức năng Tiếng Việt]</b><br><code>{fn_first}</code> hoặc <b>[Tên chức năng Tiếng Việt]</b><br><code>{fn_second}</code>.
   - CẤM viết tên chức năng bằng tiếng Việt không dấu dạng hàm (VD CẤM: 'them_san_pham', 'loc_theo_loai').
"""

    # 3. Define Architecture-Specific Guidelines, SRS Headers & Forbidden Leakage Concepts
    if pattern == ARCH_CLI_CORE:
        arch_name = "Ứng dụng Console / Lập trình Cốt lõi (CLI Core Application)"
        srs_headers = [
            "### **1. Tổng quan hệ thống**",
            "### **2. Đặc tả chức năng (Functional Requirements)**",
            "### **3. Đặc tả phi chức năng (Non-Functional Requirements)**",
            "### **4. Đặc tả dữ liệu (Data Model / Schemas)**",
            "### **5. Quy tắc kiểm soát lỗi và Xử lý ngoại lệ (Exception Handling & Error Rules)**",
            "### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)**",
            "### **7. Quy trình chạy thử nghiệm Console (Console Execution & Test Scenarios)**"
        ]
        error_model = """MÔ HÌNH KIỂM SOÁT LỖI MÔN CONSOLE CLI:
- Sử dụng các ngoại lệ ngôn ngữ nguyên bản (Native Language Exceptions: ValueError, KeyError, TypeError...) hoặc giá trị trả về (booleans/tuples/dicts/messages).
- TUYỆT ĐỐI CẤM sử dụng JSON Response Envelope của REST API (VD CẤM: {"status": "success", "code": "ERR_xxx", "data": {}}).
- TUYỆT ĐỐI CẤM sử dụng HTTP Status Codes (200, 400, 404, 500), Swagger UI, ReDoc, Controllers, DTO Mappings, Web Service Endpoints.
- Phản hồi lỗi ra màn hình Console bằng thông báo văn bản (print) rõ nghĩa và khôi phục luồng qua `try-except`.
"""
        forbidden_concepts = [
            "response_envelope", "status_code", "http status", "swagger", "redoc", "dto mapping",
            "controller", "endpoint", "rest api", "fastapi", "flask", "django rest", "express.js"
        ]
        
    elif pattern == ARCH_WEB_BACKEND:
        arch_name = "Dịch vụ Web Backend REST API (Web Backend REST API Service)"
        srs_headers = [
            "### **1. Tổng quan hệ thống**",
            "### **2. Đặc tả chức năng (Functional Requirements)**",
            "### **3. Đặc tả phi chức năng (Non-Functional Requirements)**",
            "### **4. Đặc tả dữ liệu (Data Model / Schemas)**",
            "### **5. Danh mục lỗi và Mã thông báo (Error Codes & Unified Envelope)**",
            "### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)**",
            "### **7. Giao diện kiểm thử và Phản hồi hệ thống (API Specifications & Interface)**"
        ]
        error_model = """MÔ HÌNH KIỂM SOÁT LỖI WEB BACKEND REST API:
- Định nghĩa rõ HTTP Status Codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error).
- Sử dụng cấu trúc JSON Unified Response Envelope đồng nhất.
- Đặc tả kiểm thử qua Swagger UI / ReDoc / Postman.
"""
        forbidden_concepts = []
        
    elif pattern == ARCH_WEB_FRONTEND:
        arch_name = "Ứng dụng Web Frontend UI/UX (Single Page Web Application)"
        srs_headers = [
            "### **1. Tổng quan hệ thống**",
            "### **2. Đặc tả chức năng (Functional Requirements)**",
            "### **3. Đặc tả phi chức năng (Non-Functional Requirements)**",
            "### **4. Đặc tả dữ liệu & State Management (State & Component Models)**",
            "### **5. Quy tắc Kiểm chuẩn Giao diện & Cảnh báo UI (UI Validation & Toast Notifications)**",
            "### **6. Bảng tổng hợp tình huống lỗi UI (UI Edge Cases Mapping)**",
            "### **7. Kịch bản Kiểm thử Tương tác Người dùng (User Interaction Test Flows)**"
        ]
        error_model = """MÔ HÌNH KIỂM SOÁT LỖI WEB FRONTEND:
- Cảnh báo lỗi trên giao diện (UI Form Validations, Inline Errors, Toast Notifications).
- Quản lý trạng thái lỗi trong Component State / Redux / Context.
- TUYỆT ĐỐI CẤM định nghĩa HTTP API Response Envelopes hay Backend Controller logic tại đây.
"""
        forbidden_concepts = ["backend controller", "database isolation level", "sql transaction"]
        
    else:
        arch_name = f"Ứng dụng {tech_stack.upper()}"
        srs_headers = [
            "### **1. Tổng quan hệ thống**",
            "### **2. Đặc tả chức năng (Functional Requirements)**",
            "### **3. Đặc tả phi chức năng (Non-Functional Requirements)**",
            "### **4. Đặc tả dữ liệu (Data Model / Schemas)**",
            "### **5. Quy tắc kiểm soát lỗi và Xử lý ngoại lệ (Exception Handling & Error Rules)**",
            "### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)**",
            "### **7. Kịch bản chạy thử nghiệm (Execution Test Scenarios)**"
        ]
        error_model = "Mô hình xử lý lỗi nguyên bản phù hợp với công nghệ."
        forbidden_concepts = []
        
    return {
        "pattern": pattern,
        "arch_name": arch_name,
        "srs_headers": srs_headers,
        "error_model": error_model,
        "naming_guidelines": naming_guidelines,
        "forbidden_concepts": forbidden_concepts
    }

def lint_document_architecture(doc_title: str, content: str, arch_info: Dict[str, Any], forbidden_scope: str = "") -> List[str]:
    """
    Systemically lints generated markdown content against forbidden architecture concepts
    and forbidden PM scope. Returns a list of explicit violation error messages.
    """
    violations = []
    c_text = content or ""
    c_text_lower = c_text.lower()
    pattern = arch_info["pattern"]
    
    # 1. Check Architecture Leakage
    if pattern == ARCH_CLI_CORE:
        # Prevent Web REST API / FastAPI leakage into CLI Core
        web_leakage_terms = [
            ("response_envelope", "Cấu trúc JSON Response Envelope của Web REST API (status, code, data, message)"),
            ("swagger", "Giao diện Swagger UI / ReDoc của Web REST API"),
            ("redoc", "Giao diện ReDoc của Web REST API"),
            ("dto mapping", "Mô hình DTO Mapping của Web Service"),
            ("http status", "Mã trạng thái HTTP Status (200, 400, 500)"),
            ("post /api", "Web REST API Endpoints (POST /api)"),
            ("get /api", "Web REST API Endpoints (GET /api)"),
            ("delete /api", "Web REST API Endpoints (DELETE /api)"),
            ("put /api", "Web REST API Endpoints (PUT /api)"),
        ]
        for term, desc in web_leakage_terms:
            if term in c_text_lower:
                violations.append(f"Tài liệu '{doc_title}' vi phạm rò rỉ kiến thức: Chứa {desc} không phù hợp với môn Console CLI Core.")
                
    # 2. Check Unaccented Vietnamese Code Identifiers
    vi_unaccented_patterns = [
        (r"\bthem_[a-z0-9_]+\b", "them_..."),
        (r"\bcap_nhat_[a-z0-9_]+\b", "cap_nhat_..."),
        (r"\bxoa_[a-z0-9_]+\b", "xoa_..."),
        (r"\btim_kiem_[a-z0-9_]+\b", "tim_kiem_..."),
        (r"\bloc_[a-z0-9_]+\b", "loc_..."),
        (r"\btinh_[a-z0-9_]+\b", "tinh_..."),
        (r"\bma_[a-z0-9_]{1,5}\b", "ma_..."),
        (r"\bten_[a-z0-9_]{1,5}\b", "ten_..."),
        (r"\bloai_[a-z0-9_]{1,5}\b", "loai_..."),
        (r"\bdon_gia\b", "don_gia"),
        (r"\bso_luong\b", "so_luong"),
        (r"\bgia_tien\b", "gia_tien")
    ]
    for pat, sample_name in vi_unaccented_patterns:
        m = re.search(pat, c_text, re.IGNORECASE)
        if m:
            matched_str = m.group(0)
            # Avoid triggering if it's inside an explicit warning/forbidden notice string
            if not re.search(rf"(?:cấm|không|ví dụ cấm|vd cấm).*?{re.escape(matched_str)}", c_text, re.IGNORECASE):
                violations.append(f"Tài liệu '{doc_title}' chứa tên biến/hàm tiếng Việt không dấu ('{matched_str}'). Quy chuẩn mã nguồn yêu cầu 100% TIẾNG ANH CÓ NGHĨA.")
                break

    # 3. Check Forbidden Scope keywords from PM spreadsheet
    if forbidden_scope:
        forbidden_lower = forbidden_scope.lower()
        clean_text = re.sub(r'class\s*=\s*"[^"]*"', '', c_text)
        clean_text = re.sub(r'class\s*=\s*\'[^\']*\'', '', clean_text)
        clean_text = re.sub(r'(?:cấm|không sử dụng|không được dùng|tránh)\s+class', '', clean_text, flags=re.IGNORECASE)
        
        terms = [t.strip().lower() for t in re.split(r'[,;\n/•\-]', forbidden_scope) if t.strip() and len(t.strip()) > 2]
        for term in terms:
            if term in ["class", "oop", "đối tượng"]:
                if re.search(r"\bclass\s+[A-Z][a-zA-Z0-9_]*\b", clean_text) or re.search(r"xây dựng (các |)class\b", clean_text, re.IGNORECASE) or re.search(r"tư duy lập trình hướng đối tượng", clean_text, re.IGNORECASE):
                    violations.append(f"Tài liệu '{doc_title}' chứa thiết kế Class/OOP vi phạm CẤM DÙNG ({forbidden_scope}) của PM.")
            elif term in ["file i/o", "file", "tệp tin"]:
                if re.search(r"đọc\s*[/và]*\s*ghi\s+tệp", clean_text, re.IGNORECASE) or re.search(r"tệp\s+tin\s+(json|csv)", clean_text, re.IGNORECASE) or re.search(r"\btasks\.json\b", clean_text, re.IGNORECASE):
                    violations.append(f"Tài liệu '{doc_title}' chứa thao tác đọc ghi tệp vi phạm CẤM DÙNG ({forbidden_scope}) của PM.")
            elif term in ["third-party modules", "third-party", "pydantic"]:
                if "pydantic" in clean_text.lower():
                    violations.append(f"Tài liệu '{doc_title}' chứa thư viện Pydantic vi phạm CẤM DÙNG ({forbidden_scope}) của PM.")

    return violations
