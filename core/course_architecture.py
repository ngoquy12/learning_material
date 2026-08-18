# core/course_architecture.py
"""
Systemic Course Architecture & Pedagogy Governance Engine.
Dynamically resolves architecture archetypes from syllabus metadata and
strictly enforces scope boundaries to prevent concept leakage between courses and sessions.
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
    generalized architectural rules, dynamic SRS headers, and forbidden concepts.
    Prioritizes session-specific scope and title over course-wide tech stack
    to prevent premature leakage of future topics.
    """
    title_lower = (session_title or "").lower()
    stack_lower = (tech_stack or "").lower()
    forbidden_lower = (forbidden_scope or "").lower()
    allowed_lower = (allowed_scope or "").lower()
    
    # 1. Determine Architecture Pattern based on Session Context & Allowed Scope
    is_explicit_cli = any(kw in title_lower for kw in ["console", "cli", "terminal", "cốt lõi", "core"]) and not any(kw in title_lower for kw in ["web", "dashboard", "fetch", "api", "dom", "frontend", "ui", "giao diện"])
    
    if is_explicit_cli:
        pattern = ARCH_CLI_CORE
    elif any(kw in title_lower for kw in ["backend", "fastapi", "express", "spring boot", "django rest", "nest", "asp.net", "microservice"]):
        pattern = ARCH_WEB_BACKEND
    elif any(kw in title_lower for kw in ["frontend", "ui", "ux", "react", "vue", "angular", "dom", "web", "dashboard", "giao diện", "single page", "spa", "fetch"]):
        pattern = ARCH_WEB_FRONTEND
    elif any(kw in title_lower for kw in ["mobile", "app", "flutter", "react native", "android", "ios"]):
        pattern = ARCH_MOBILE_APP
    elif any(kw in title_lower for kw in ["sql", "database", "postgres", "mysql", "csdl", "truy vấn"]):
        pattern = ARCH_DATABASE_SQL
    elif any(kw in title_lower for kw in ["devops", "cloud", "docker", "k8s", "kubernetes", "aws", "ci/cd"]):
        pattern = ARCH_DEVOPS_CLOUD
    elif any(kw in title_lower for kw in ["api", "rest api"]):
        pattern = ARCH_WEB_BACKEND
    elif any(kw in stack_lower for kw in ["fastapi", "express", "spring boot", "nest", "django rest"]) and "backend" in allowed_lower:
        pattern = ARCH_WEB_BACKEND
    elif any(kw in stack_lower for kw in ["react", "vue", "angular"]) and ("frontend" in allowed_lower or "dom" in allowed_lower):
        pattern = ARCH_WEB_FRONTEND
    else:
        # Default to CLI Core for foundational programming sessions across all languages
        pattern = ARCH_CLI_CORE

    # 2. Build Naming Conventions dynamically based on tech stack
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

    # 3. Define Architecture Guidelines, SRS Headers & Generic Runtime Error Models
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
        error_model = """MÔ HÌNH KIỂM SOÁT LỖI MÔI TRƯỜNG DÒNG LỆNH (CLI / RUNTIME CORE):
- Sử dụng các ngoại lệ ngôn ngữ nguyên bản (Native Language Exceptions: ValueError, KeyError, TypeError, Error...) hoặc giá trị trả về (booleans/tuples/objects/messages).
- Tương tác nhập xuất và hiển thị phản hồi trực tiếp qua màn hình Console/Terminal chuẩn.
- Bắt lỗi và khôi phục luồng an toàn qua cấu trúc try-catch / try-except nguyên bản của ngôn ngữ.
- TUYỆT ĐỐI CẤM sử dụng các kiến trúc hạ tầng chưa được học hoặc nằm trong danh mục CẤM DÙNG (FORBIDDEN SCOPE).
"""
        forbidden_concepts = [
            "response_envelope", "status_code", "http status", "swagger", "redoc", "dto mapping",
            "controller", "endpoint", "rest api"
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
        "forbidden_concepts": forbidden_concepts,
        "allowed_scope": allowed_scope,
        "tech_stack": tech_stack
    }

def lint_document_architecture(doc_title: str, content: str, arch_info: Dict[str, Any], forbidden_scope: str = "") -> List[str]:
    """
    Systemically lints generated markdown content against dynamically provided forbidden scope
    and general architecture principles without rigid hardcoded technology lists.
    """
    violations = []
    c_text = content or ""
    c_text_lower = c_text.lower()
    
    # 1. Clean disclaimers/prohibitions so sentences like "Cấm sử dụng DOM/Class" don't trigger false positives
    clean_text = re.sub(r'(?:cấm|không|tuyệt đối|chưa được|lưu ý|chú ý|note|forbid|forbidden|without|do not use)[^.\n]*', '', c_text_lower, flags=re.IGNORECASE)
    
    # 2. Check Unaccented Vietnamese Code Identifiers (English naming rule)
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
            if not re.search(rf"(?:cấm|không|ví dụ cấm|vd cấm).*?{re.escape(matched_str)}", c_text, re.IGNORECASE):
                violations.append(f"Tài liệu '{doc_title}' chứa tên biến/hàm tiếng Việt không dấu ('{matched_str}'). Quy chuẩn mã nguồn yêu cầu 100% TIẾNG ANH CÓ NGHĨA.")
                break

    # 3. Dynamic Scope Checks (Derived from Syllabus / PM metadata)
    allowed_text_lower = (arch_info.get("allowed_scope") or "").lower()
    stack_text_lower = (arch_info.get("tech_stack") or "").lower()
    common_allowlist = {"css", "html", "js", "web", "dom", "api", "code", "app", "ui", "ux", "data", "file", "json", "giao diện", "hệ thống", "dữ liệu", "bài tập", "dự án"}

    if forbidden_scope:
        terms = [t.strip().lower() for t in re.split(r'[,;\n/•\-]', forbidden_scope) if t.strip() and len(t.strip()) > 3]
        for term in terms:
            if "kiến thức buổi sau" in term or "tuyệt đối chưa được dùng" in term:
                continue
            if term in common_allowlist:
                continue
            # If the term is already introduced in prior taught sessions (allowed_scope) or course tech stack, ignore it
            if allowed_text_lower and term in allowed_text_lower:
                continue
            if stack_text_lower and term in stack_text_lower:
                continue
            # Regex word-boundary search in cleaned text
            pattern_term = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern_term, clean_text):
                violations.append(f"Tài liệu '{doc_title}' vi phạm phạm vi kiến thức: Chứa khái niệm '{term}' bị cấm trong phạm vi buổi học hiện tại.")

    # 4. Pattern-specific forbidden concepts
    for concept in arch_info.get("forbidden_concepts", []):
        if concept in clean_text:
            violations.append(f"Tài liệu '{doc_title}' vi phạm kiến trúc: Chứa khái niệm '{concept}' không phù hợp với mô hình {arch_info['arch_name']}.")

    return violations
