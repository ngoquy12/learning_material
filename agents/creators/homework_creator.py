"""
agents/creators/homework_creator.py
Modular Homework Creator Agent for Elearning Content Factory.
Generates role-based enterprise coding exercises adhering to:
- Rikkei Education Pedagogical Standards (Bloom Taxonomy: Basic, Advanced, Analysis, Creative).
- Type-Safe Schema Validation with Pydantic v2 (EnhancedHomeworkExerciseSchema).
- Template-driven prompt generation via Jinja2 (homework_creator.j2).
- Strict No-Emoji, 100% Accented Vietnamese Output Contract.
"""

import os
import re
import random
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor

from core.llm import call_llm
from core.prompts import render_prompt
from core.domain_adapters import get_domain_rules
from core.domain_knowledge import (
    BUSINESS_DOMAINS,
    select_random_domain,
    format_domain_rules_for_prompt
)
from core.schemas.course_schemas import EnhancedHomeworkExerciseSchema
from core.utils.schema_validator import validate_schema

def slugify_vietnamese(text: str, max_words: int = 6) -> str:
    """Converts Vietnamese text to a clean snake_case slug."""
    if not text:
        return "bai_tap"
    vn_map = {
        'à':'a','á':'a','ả':'a','ã':'a','ạ':'a','ă':'a','ằ':'a','ắ':'a','ẳ':'a','ẵ':'a','ặ':'a','â':'a','ầ':'a','ấ':'a','ẩ':'a','ẫ':'a','ậ':'a',
        'è':'e','é':'e','ẻ':'e','ẽ':'e','ẹ':'e','ê':'e','ề':'e','ế':'e','ể':'e','ễ':'e','ệ':'e',
        'ì':'i','í':'i','ỉ':'i','ĩ':'i','ị':'i',
        'ò':'o','ó':'o','ỏ':'o','õ':'o','ọ':'o','ô':'o','ồ':'o','ố':'o','ổ':'o','ỗ':'o','ộ':'o','ơ':'o','ờ':'o','ớ':'o','ở':'o','ỡ':'o','ợ':'o',
        'ù':'u','ú':'u','ủ':'u','ũ':'u','ụ':'u','ư':'u','ừ':'u','ứ':'u','ử':'u','ữ':'u','ự':'u',
        'ỳ':'y','ý':'y','ỷ':'y','ỹ':'y','ỵ':'y',
        'đ':'d',
        'À':'a','Á':'a','Ả':'a','Ã':'a','Ạ':'a','Ă':'a','Ằ':'a','Ắ':'a','Ẳ':'a','Ẵ':'a','Ặ':'a','Â':'a','Ầ':'a','Ấ':'a','Ẩ':'a','Ẫ':'a','Ậ':'a',
        'È':'e','É':'e','Ẻ':'e','Ẽ':'e','Ẹ':'e','Ê':'e','Ề':'e','Ế':'e','Ể':'e','Ễ':'e','Ệ':'e',
        'Ì':'i','Í':'i','Ỉ':'i','Ĩ':'i','Ị':'i',
        'Ò':'o','Ó':'o','Ỏ':'o','Õ':'o','Ọ':'o','Ô':'o','Ồ':'o','Ố':'o','Ổ':'o','Ỗ':'o','Ộ':'o','Ơ':'o','Ờ':'o','Ớ':'o','Ở':'o','Ỡ':'o','Ợ':'o',
        'Ù':'u','Ú':'u','Ủ':'u','Ũ':'u','Ụ':'u','Ư':'u','Ừ':'u','Ứ':'u','Ử':'u','Ữ':'u','Ự':'u',
        'Ỳ':'y','Ý':'y','Ỷ':'y','Ỹ':'y','Ỵ':'y',
        'Đ':'d'
    }
    for k, v in vn_map.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).lower()
    words = text.split()[:max_words]
    slug = "_".join(words)
    return slug or "bai_tap"

def extract_exercise_slug(de_bai_content: str, fallback_domain: str = "bai_tap") -> str:
    """Extracts a descriptive slug from exercise title or context."""
    if not de_bai_content:
        return slugify_vietnamese(fallback_domain, max_words=4)
    # 1. Try finding centered H2 title
    m = re.search(r"##\s*<center>(.*?)</center>", de_bai_content, re.IGNORECASE)
    if m:
        return slugify_vietnamese(m.group(1), max_words=5)
    # 2. Try finding H1/H2 with exercise title
    m = re.search(r"#+\s*Bài tập\s*\d*[:\-]?\s*([^\n]+)", de_bai_content, re.IGNORECASE)
    if m:
        return slugify_vietnamese(m.group(1), max_words=5)
    # 3. Try finding Section 2 Context first sentence
    m = re.search(r"###\s*2\.\s*Bối cảnh[^\n]*\n+([^\n]+)", de_bai_content, re.IGNORECASE)
    if m:
        first_sentence = m.group(1).split(".")[0]
        return slugify_vietnamese(first_sentence, max_words=5)
    return slugify_vietnamese(fallback_domain, max_words=4)

LEVEL_PREFIXES = {
    1: "1_van_dung_co_ban_1",
    2: "2_van_dung_co_ban_2",
    3: "3_van_dung_co_ban_3",
    4: "4_van_dung_co_ban_4",
    5: "5_van_dung_co_ban_5",
    6: "6_van_dung_co_ban_6",
    7: "7_van_dung_nang_cao_1",
    8: "8_van_dung_nang_cao_2",
    9: "9_van_dung_nang_cao_3",
    10: "10_phan_tich_1",
    11: "11_phan_tich_2",
    12: "12_phan_tich_3",
    13: "13_sang_tao_1",
    14: "14_sang_tao_2",
    15: "15_sang_tao_3",
    16: "16_tong_hop_demo_giang_vien_tren_lop",
    17: "17_tong_hop_he_thong_kien_thuc_mindmap"
}

def clean_markdown_formulas(text: str) -> str:
    """Removes broken or unnecessary formula characters in homework descriptions."""
    if not text:
        return ""
    # Normalize markdown bold / headers
    text = re.sub(r'#{4,}', '###', text)
    return text.strip()

def sanitize_homework_markdown(content: str, level_name: str = "") -> str:
    """Sanitizes markdown content according to Rikkei Education formatting standards."""
    if not content:
        return ""
    # Strip emojis using unicode ranges
    content = re.sub(r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]', '', content)
    content = re.sub(r'\n(#{1,4}\s+)', r'\n\n\1', content)
    return content.strip()

def generate_homework_exercise(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str,
    idx: int,
    level_name: str,
    chosen_domain: str,
    forbidden_scope: str = "",
    total_exercises: int = 15
) -> Dict[str, Any]:
    """
    Generates a single homework assignment (de_bai_content and tieu_chi_content)
    using Jinja2 prompt rendering and Pydantic v2 schema validation.
    """
    from core.domain_knowledge import get_domain_blueprint
    domain_info = get_domain_blueprint(chosen_domain)
    domain_rules_text = format_domain_rules_for_prompt(domain_info)

    # 1. Render prompt from Jinja2 template
    user_prompt = render_prompt(
        "homework_creator.j2",
        {
            "idx": idx,
            "total_exercises": total_exercises,
            "level_name": level_name,
            "chosen_domain": chosen_domain,
            "session_id": session_id,
            "session_title": session_title,
            "tech_stack": tech_stack,
            "previous_lessons_text": previous_lessons_text,
            "forbidden_scope": forbidden_scope,
            "domain_rules_text": domain_rules_text
        }
    )

    system_prompt = (
        "You are an Expert Technical Curriculum Author at Rikkei Education. "
        "Generate realistic, production-grade homework assignments in 100% Accented Vietnamese. "
        "Strictly adhere to the required XML schema with <de_bai_content> and <tieu_chi_content>."
    )

    # 2. Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        agent_name=f"Homework_Creator_Ex_{idx}",
        session_id=session_id
    )

    de_bai = ""
    tieu_chi = ""

    if response:
        xml_clean = response.strip()
        if xml_clean.startswith("```xml"):
            xml_clean = xml_clean[6:]
        if xml_clean.startswith("```"):
            xml_clean = xml_clean[3:]
        if xml_clean.endswith("```"):
            xml_clean = xml_clean[:-3]
        xml_clean = xml_clean.strip()

        de_bai_match = re.search(r"<de_bai_content>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</de_bai_content>", xml_clean, re.DOTALL | re.IGNORECASE)
        if de_bai_match:
            de_bai = de_bai_match.group(1).strip()

        rubric_match = re.search(r"<tieu_chi_content>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</tieu_chi_content>", xml_clean, re.DOTALL | re.IGNORECASE)
        if rubric_match:
            tieu_chi = rubric_match.group(1).strip()

    # Fallback if empty
    if not de_bai:
        de_bai = f"""### 1. Mục tiêu bài tập
- Nắm vững cú pháp và áp dụng {tech_stack} vào bài toán {chosen_domain}.

### 2. Bối cảnh & Mô tả bài toán
Trong hệ thống {chosen_domain}, kỹ sư cần xây dựng mô-đun xử lý dữ liệu cho bài toán thực tế #{idx}.

### 3. Quy tắc nghiệp vụ (Business Rules)
- Kiểm tra tính hợp lệ của dữ liệu đầu vào.
- Tính toán và xuất kết quả theo đúng định dạng.

### 4. Yêu cầu kỹ thuật & Triển khai
- Viết mã nguồn bằng {tech_stack} tuân thủ chuẩn đặt tên.
- Xử lý các trường hợp ngoại lệ cơ bản.

### 5. Quy chuẩn nộp bài
- Đẩy toàn bộ mã nguồn lên GitHub repository theo cấu trúc chuẩn.
"""

    if not tieu_chi:
        tieu_chi = f"""### Tiêu chuẩn Đánh giá & Thang điểm (100đ)
| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| Cấu trúc & Phong cách mã nguồn | 20đ | Chuẩn đặt tên, thụt lề, comment rõ ràng |
| Xử lý Logic đúng nghiệp vụ | 40đ | Đạt 100% test cases cơ bản & nâng cao |
| Xử lý Biên & Ngoại lệ | 20đ | Kiểm soát lỗi dữ liệu đầu vào |
| Tối ưu hiệu năng | 20đ | Thuật toán tối ưu, không dư thừa tài nguyên |
"""

    # 3. Validate with Pydantic v2 schema
    raw_payload = {
        "idx": idx,
        "level_name": level_name,
        "chosen_domain": chosen_domain,
        "de_bai_content": sanitize_homework_markdown(de_bai, level_name),
        "tieu_chi_content": clean_markdown_formulas(tieu_chi)
    }
    is_valid, validated_obj, errs = validate_schema(EnhancedHomeworkExerciseSchema, raw_payload)

    if not is_valid or not validated_obj:
        return {
            "idx": idx,
            "level_name": level_name,
            "chosen_domain": chosen_domain,
            "de_bai_content": raw_payload["de_bai_content"],
            "tieu_chi_content": raw_payload["tieu_chi_content"],
            "title": f"Bài tập {idx}: {chosen_domain} ({level_name})"
        }

    return {
        "idx": validated_obj.idx,
        "level_name": validated_obj.level_name,
        "chosen_domain": validated_obj.chosen_domain,
        "de_bai_content": validated_obj.de_bai_content,
        "tieu_chi_content": validated_obj.tieu_chi_content,
        "title": f"Bài tập {idx}: {chosen_domain} ({level_name})"
    }


def generate_inclass_synthesis_exercise(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str = "",
    chosen_domain: str = "E-Commerce",
    forbidden_scope: str = ""
) -> str:
    """
    Generates a standardized 30-minute in-class synthesis exercise
    following session_inclass_exercise_generator skill.
    """
    system_prompt = (
        "You are an Expert Technical Curriculum Author at Rikkei Education. "
        "Generate a standardized 30-minute In-Class Synthesis Exercise (Bài tập tổng hợp trên lớp) in 100% Accented Vietnamese. "
        "Strictly adhere to the 4-section layout: (1) Mục tiêu bài tập, (2) Mô tả bối cảnh & Yêu cầu bài toán (Input / Output kèm Bảng ví dụ minh họa), (3) Các bước thực hiện & Quy định kỹ thuật, (4) Checklist đánh giá kết quả (Nghiệm thu). "
        "Enforce Closed How - Open What & Why (specify Input/Output, NO code skeleton/spoilers). Zero text emojis."
    )
    user_prompt = f"""Tạo bài tập tổng hợp trên lớp (thời lượng 30 phút) cho buổi học:
- Khóa học/Buổi: {session_id} - {session_title}
- Công nghệ: {tech_stack}
- Các nội dung trọng tâm đã học: {previous_lessons_text or 'Kiến thức cốt lõi của Session'}
- Lĩnh vực nghiệp vụ doanh nghiệp: {chosen_domain}
- Phạm vi kiến thức bị cấm: {forbidden_scope or 'Không sử dụng kiến thức chưa học'}

Yêu cầu xuất ra định dạng Markdown chuẩn 4 phần như sau:
# Bài tập tổng hợp trên lớp: [Tên bài toán nghiệp vụ {chosen_domain}]

## 1. Mục tiêu bài tập
- [2-3 gạch đầu dòng mục tiêu kỹ năng tổng hợp]

## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: [Mô tả bối cảnh thực tế 2-3 câu]
- **Dữ liệu đầu vào (Input)**: [Quy định kiểu dữ liệu, cấu trúc tham số đầu vào]
- **Kết quả đầu ra (Output)**: [Quy định rõ kết quả trả về hoặc cập nhật hiển thị]

### Bảng ví dụ minh họa Input/Output:
| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | `...` | `...` | Luồng thành công bình thường. |
| **Trường hợp 2 (Ngoại lệ)** | `...` | `...` | Xử lý lỗi hoặc dữ liệu biên an toàn. |

## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: Thực thi trên {tech_stack}.
- **Yêu cầu kỹ thuật**:
  - Học viên tự chủ động thiết kế thuật toán và cấu trúc mã nguồn (Closed How).
  - Bắt lỗi dữ liệu biên và xử lý ngoại lệ an toàn.
  - Tuân thủ quy chuẩn đặt tên biến/hàm và Clean Code.

## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Xây dựng hoàn chỉnh chương trình đáp ứng đúng bối cảnh nghiệp vụ doanh nghiệp.
- [ ] Trả về kết quả Output chính xác theo đúng bảng ví dụ minh họa.
- [ ] Bắt lỗi ngoại lệ và xử lý dữ liệu biên an toàn không gây crash chương trình.
- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm đúng quy chuẩn và có chú thích rõ ràng.
"""
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        agent_name="InClass_Synthesis_Exercise_Agent",
        session_id=session_id
    )
    if response:
        content = response.strip()
        if content.startswith("```markdown"):
            content = content[11:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return sanitize_homework_markdown(content)

    return f"""# Bài tập tổng hợp trên lớp: Xây dựng Mô-đun {chosen_domain} cho {session_title}

## 1. Mục tiêu bài tập
- Vận dụng tổng hợp toàn bộ kiến thức trong {session_title} để giải quyết bài toán phần mềm thực tế.
- Triển khai chức năng nghiệp vụ hoàn chỉnh trên nền tảng {tech_stack}.

## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: Trong hệ thống {chosen_domain}, cần xây dựng mô-đun xử lý dữ liệu tích hợp theo các bài học đã học.
- **Dữ liệu đầu vào (Input)**: Dữ liệu đối tượng và tham số đầu vào hợp lệ.
- **Kết quả đầu ra (Output)**: Kết quả tính toán hoặc cập nhật giao diện chính xác.

### Bảng ví dụ minh họa Input/Output:
| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | Dữ liệu mẫu chuẩn | Kết quả xử lý thành công | Luồng bình thường |
| **Trường hợp 2 (Ngoại lệ)** | Dữ liệu không hợp lệ | Thông báo lỗi cụ thể | Kiểm soát ngoại lệ |

## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: Thực thi trên môi trường {tech_stack}.
- **Yêu cầu kỹ thuật**:
  - Tự chủ động xây dựng giải thuật xử lý logic theo chuẩn Clean Code.
  - Bắt lỗi dữ liệu biên an toàn.

## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Hoàn thành mã nguồn đáp ứng đúng 100% yêu cầu nghiệp vụ.
- [ ] Đạt kết quả chính xác theo bảng test cases mẫu.
- [ ] Xử lý ngoại lệ an toàn không crash ứng dụng.
"""


def generate_mindmap_exercise(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str = "",
    forbidden_scope: str = ""
) -> str:
    """
    Generates a mindmap architecture assignment following mindmap_generator skill.
    """
    system_prompt = (
        "You are an Expert Technical Curriculum Author at Rikkei Education. "
        "Generate a standardized Mindmap Architecture Exercise (Bài tập sơ đồ tư duy mindmap) in 100% Accented Vietnamese. "
        "The exercise guides students to construct a complete hierarchical Markmap / Mermaid mindmap synthesizing all core architectural concepts of the session."
    )
    user_prompt = f"""Tạo bài tập sơ đồ tư duy mindmap kiến trúc cho:
- Khóa học/Buổi: {session_id} - {session_title}
- Công nghệ: {tech_stack}
- Các nội dung trọng tâm của buổi học: {previous_lessons_text or 'Kiến thức cốt lõi của Session'}
- Phạm vi bị cấm: {forbidden_scope or 'Không sử dụng kiến thức chưa học'}

Yêu cầu xuất ra định dạng Markdown bài tập với cấu trúc sau:
# Bài tập sơ đồ tư duy mindmap: {session_title}

## 1. Mục tiêu bài tập
- Hệ thống hóa toàn diện tư duy kiến trúc và cấu trúc luồng dữ liệu của {session_title}.
- Xây dựng sơ đồ tư duy Markmap / Mermaid trực quan, súc tích, liên kết các nhánh tri thức cốt lõi.

## 2. Bối cảnh & Yêu cầu thiết kế Mindmap
- Học viên đóng vai trò Software Architect phân tích và trực quan hóa cấu trúc kiến thức của Session.
- Yêu cầu xây dựng sơ đồ dạng cây (Mindmap) thể hiện đầy đủ 5 nhánh kiến thức bắt buộc.

## 3. Cấu trúc các nhánh kiến thức bắt buộc
1. **Khái niệm & Vai trò**: Bản chất kỹ thuật, bài toán doanh nghiệp giải quyết (tối đa 10 từ/node).
2. **Cú pháp & Giải nghĩa**: Cú pháp chuẩn của {tech_stack}, giải nghĩa từng thành phần tham số.
3. **Ví dụ thực hành**: Đoạn mã nguồn thực tế ngắn gọn (5-8 dòng) minh họa cơ chế.
4. **Lưu ý triển khai / Lỗi thường gặp**: Các sai sót phổ biến và cách phòng tránh.
5. **Liên kết hệ thống**: Mối quan hệ luồng dữ liệu giữa các thành phần trong hệ thống.

## 4. Quy chuẩn định dạng & Nộp bài
- Định dạng nộp bài: File Markdown chứa cú pháp ```markmap hoặc ```mermaid mindmap.
- Quy định súc tích: Mỗi node lá không quá 15 từ, không viết văn bản dài dòng.

## 5. Checklist đánh giá sơ đồ tư duy
- [ ] Thể hiện đầy đủ 5 nhánh cấu trúc tri thức bắt buộc.
- [ ] Cú pháp mã nguồn trong ví dụ hoàn toàn chính xác theo {tech_stack}.
- [ ] Các lưu ý lỗi thường gặp thực tế, chuẩn kỹ thuật.
- [ ] Tuân thủ giới hạn độ dài node (< 15 từ/node), bố cục rõ ràng, dễ nhìn.
"""
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        agent_name="Mindmap_Exercise_Agent",
        session_id=session_id
    )
    if response:
        content = response.strip()
        if content.startswith("```markdown"):
            content = content[11:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return sanitize_homework_markdown(content)

    return f"""# Bài tập sơ đồ tư duy mindmap: {session_title}

## 1. Mục tiêu bài tập
- Hệ thống hóa toàn diện tư duy kiến trúc và cấu trúc luồng dữ liệu của {session_title}.
- Xây dựng sơ đồ tư duy Markmap / Mermaid trực quan, súc tích, liên kết các nhánh tri thức cốt lõi.

## 2. Bối cảnh & Yêu cầu thiết kế Mindmap
- Học viên đóng vai trò Software Architect phân tích và trực quan hóa cấu trúc kiến thức của Session.
- Yêu cầu xây dựng sơ đồ dạng cây (Mindmap) thể hiện đầy đủ 5 nhánh kiến thức bắt buộc.

## 3. Cấu trúc các nhánh kiến thức bắt buộc
1. **Khái niệm & Vai trò**: Bản chất kỹ thuật, bài toán doanh nghiệp giải quyết.
2. **Cú pháp & Giải nghĩa**: Cú pháp chuẩn của {tech_stack}, giải nghĩa tham số.
3. **Ví dụ thực hành**: Đoạn mã nguồn thực tế ngắn gọn (5-8 dòng).
4. **Lưu ý triển khai / Lỗi thường gặp**: Sai sót phổ biến và cách phòng ngừa.
5. **Liên kết hệ thống**: Mối quan hệ luồng dữ liệu trong hệ thống.

## 4. Quy chuẩn định dạng & Nộp bài
- Định dạng nộp bài: File Markdown chứa cú pháp Markmap hoặc Mermaid mindmap.
- Quy định súc tích: Mỗi node lá không quá 15 từ, không viết văn bản dài dòng.

## 5. Checklist đánh giá sơ đồ tư duy
- [ ] Thể hiện đầy đủ 5 nhánh cấu trúc tri thức bắt buộc.
- [ ] Cú pháp mã nguồn trong ví dụ chính xác theo {tech_stack}.
- [ ] Các lưu ý lỗi thường gặp thực tế, chuẩn kỹ thuật.
- [ ] Tuân thủ giới hạn độ dài node (< 15 từ/node), bố cục rõ ràng.
"""


def generate_session_homework_suite(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str = "",
    forbidden_scope: str = "",
    course_dir: Optional[Path] = None,
    session_dir_path: Optional[Union[str, Path]] = None,
    total_exercises: int = 15
) -> List[Dict[str, Any]]:
    """
    Generates a full suite of 15 homework assignments for a session
    distributed across 5 Bloom taxonomy levels (3 exercises per level),
    plus 1 in-class synthesis exercise and 1 mindmap architecture exercise.
    """
    # 15 exercises distributed across 5 Bloom cognitive levels (3 exercises per level)
    levels = [
        # Mức độ 1: Cơ bản 1 - Debug lỗi (Bài 1-3)
        ("Mức độ 1: Cơ bản - Debug lỗi", "E-Commerce"),
        ("Mức độ 1: Cơ bản - Debug lỗi", "Logistics"),
        ("Mức độ 1: Cơ bản - Debug lỗi", "FinTech"),
        # Mức độ 2: Cơ bản 2 - Kiểm thử I/O & Hoàn thiện luồng (Bài 4-6)
        ("Mức độ 2: Cơ bản - Kiểm thử I/O", "Healthcare"),
        ("Mức độ 2: Cơ bản - Kiểm thử I/O", "CRM"),
        ("Mức độ 2: Cơ bản - Kiểm thử I/O", "EdTech"),
        # Mức độ 3: Nâng cao 1 - Xây dựng tính năng mới (Bài 7-9)
        ("Mức độ 3: Nâng cao - Xây dựng tính năng mới", "E-Commerce"),
        ("Mức độ 3: Nâng cao - Xây dựng tính năng mới", "Logistics"),
        ("Mức độ 3: Nâng cao - Xây dựng tính năng mới", "FinTech"),
        # Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc & Trade-offs (Bài 10-12)
        ("Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc", "Healthcare"),
        ("Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc", "CRM"),
        ("Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc", "EdTech"),
        # Mức độ 5: Sáng tạo - Thiết kế Mini Module (Bài 13-15)
        ("Mức độ 5: Sáng tạo - Thiết kế Mini Module", "E-Commerce"),
        ("Mức độ 5: Sáng tạo - Thiết kế Mini Module", "FinTech"),
        ("Mức độ 5: Sáng tạo - Thiết kế Mini Module", "EdTech")
    ]

    exercises_data = []
    print(f"\n[Homework Creator] 🚀 Bắt đầu sinh bộ {total_exercises} bài tập về nhà + 1 bài tổng hợp + 1 bài mindmap cho {session_id} ({tech_stack})...")

    def _gen_one(i: int):
        level_name, domain = levels[(i - 1) % len(levels)]
        return generate_homework_exercise(
            session_id=session_id,
            session_title=session_title,
            tech_stack=tech_stack,
            previous_lessons_text=previous_lessons_text,
            idx=i,
            level_name=level_name,
            chosen_domain=domain,
            forbidden_scope=forbidden_scope,
            total_exercises=total_exercises
        )

    # Parallel generation of 15 homework exercises
    with ThreadPoolExecutor(max_workers=min(total_exercises, 8)) as executor:
        futures = [executor.submit(_gen_one, i) for i in range(1, total_exercises + 1)]
        for f in futures:
            try:
                res = f.result()
                exercises_data.append(res)
            except Exception as e:
                print(f"  ❌ Lỗi khi sinh bài tập về nhà: {e}")

    exercises_data.sort(key=lambda x: x.get("idx", 0))

    # Parallel generation of In-Class Synthesis Exercise and Mindmap Exercise
    inclass_ex_content = ""
    mindmap_ex_content = ""
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_inclass = executor.submit(
            generate_inclass_synthesis_exercise,
            session_id=session_id,
            session_title=session_title,
            tech_stack=tech_stack,
            previous_lessons_text=previous_lessons_text,
            chosen_domain="E-Commerce",
            forbidden_scope=forbidden_scope
        )
        f_mindmap = executor.submit(
            generate_mindmap_exercise,
            session_id=session_id,
            session_title=session_title,
            tech_stack=tech_stack,
            previous_lessons_text=previous_lessons_text,
            forbidden_scope=forbidden_scope
        )
        try:
            inclass_ex_content = f_inclass.result()
        except Exception as e:
            print(f"  ❌ Lỗi khi sinh bài tập tổng hợp trên lớp: {e}")
        try:
            mindmap_ex_content = f_mindmap.result()
        except Exception as e:
            print(f"  ❌ Lỗi khi sinh bài tập sơ đồ tư duy mindmap: {e}")

    # Determine target output directory
    target_homework_dir = None
    if session_dir_path:
        target_homework_dir = Path(session_dir_path) / "Bài tập"
    elif course_dir:
        target_homework_dir = course_dir / session_id / "Bài tập"

    # Export to disk if destination is provided
    if target_homework_dir:
        target_homework_dir.mkdir(parents=True, exist_ok=True)

        # 1. Cleanup legacy non-descriptive folders (e.g. bai_01, bai_02) and empty stub files
        for item in list(target_homework_dir.iterdir()):
            if item.is_dir() and re.match(r"^bai_\d+$", item.name):
                try:
                    shutil.rmtree(item)
                except Exception:
                    pass
            elif item.is_file() and item.stat().st_size < 200:
                try:
                    item.unlink()
                except Exception:
                    pass

        # 2. Export 15 tiered exercise subfolders with descriptive names
        for ex in exercises_data:
            idx = ex["idx"]
            prefix = LEVEL_PREFIXES.get(idx, f"{idx}_bai_tap")
            slug = extract_exercise_slug(ex["de_bai_content"], ex.get("chosen_domain", "bai_tap"))
            folder_name = f"{prefix}_{slug}"
            ex_folder = target_homework_dir / folder_name
            ex_folder.mkdir(parents=True, exist_ok=True)

            # Write standard student assignment files (both names supported)
            with open(ex_folder / "de_bai_bai_tap.md", "w", encoding="utf-8") as f:
                f.write(ex["de_bai_content"])
            with open(ex_folder / "de_bai.md", "w", encoding="utf-8") as f:
                f.write(ex["de_bai_content"])

            # Write standard grading rubric files (both names supported)
            with open(ex_folder / "tieu_chi_cham_diem_ai.md", "w", encoding="utf-8") as f:
                f.write(ex["tieu_chi_content"])
            with open(ex_folder / "tieu_chi.md", "w", encoding="utf-8") as f:
                f.write(ex["tieu_chi_content"])

            # Backward-compatible individual bài tập markdown in Bài tập root
            with open(target_homework_dir / f"bai_tap_{idx}.md", "w", encoding="utf-8") as f:
                f.write(f"# {ex['title']}\n\n{ex['de_bai_content']}\n\n{ex['tieu_chi_content']}")

        # 3. Export folder 16: In-Class Synthesis Exercise
        if inclass_ex_content:
            folder_16 = target_homework_dir / "16_tong_hop_demo_giang_vien_tren_lop"
            folder_16.mkdir(parents=True, exist_ok=True)
            with open(folder_16 / "de_bai_bai_tap.md", "w", encoding="utf-8") as f:
                f.write(inclass_ex_content)
            with open(folder_16 / "de_bai.md", "w", encoding="utf-8") as f:
                f.write(inclass_ex_content)
            rubric_16 = f"""### Tiêu chuẩn Đánh giá Bài tập Tổng hợp Trên lớp (100đ)
| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| Triển khai Logic Nghiệp vụ | 40đ | Đáp ứng đúng 100% yêu cầu Input/Output theo bảng ví dụ |
| Cấu trúc Mã nguồn & Clean Code | 30đ | Đặt tên đúng quy chuẩn, comment giải thích rõ ràng |
| Xử lý Dữ liệu Biên & Ngoại lệ | 30đ | Kiểm soát lỗi dữ liệu đầu vào, không crash ứng dụng |
"""
            with open(folder_16 / "tieu_chi_cham_diem_ai.md", "w", encoding="utf-8") as f:
                f.write(rubric_16)
            with open(folder_16 / "tieu_chi.md", "w", encoding="utf-8") as f:
                f.write(rubric_16)

            # Save in root as well
            with open(target_homework_dir / "bai_tap_tong_hop.md", "w", encoding="utf-8") as f:
                f.write(inclass_ex_content)

        # 4. Export folder 17: Mindmap Architecture Exercise
        if mindmap_ex_content:
            folder_17 = target_homework_dir / "17_tong_hop_he_thong_kien_thuc_mindmap"
            folder_17.mkdir(parents=True, exist_ok=True)
            with open(folder_17 / "de_bai_bai_tap.md", "w", encoding="utf-8") as f:
                f.write(mindmap_ex_content)
            with open(folder_17 / "de_bai.md", "w", encoding="utf-8") as f:
                f.write(mindmap_ex_content)
            rubric_17 = f"""### Tiêu chuẩn Đánh giá Bài tập Sơ đồ Tư duy Mindmap (100đ)
| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| Độ Bao phủ 5 Nhánh Kiến thức | 40đ | Đầy đủ: Khái niệm, Cú pháp, Ví dụ, Lỗi thường gặp, Liên kết |
| Tính Chính xác Kỹ thuật | 30đ | Cú pháp code chuẩn {tech_stack}, lưu ý lỗi chuẩn xác |
| Trực quan & Súc tích | 30đ | Cấu trúc cây rõ ràng, súc tích (<15 từ/node), dễ nhìn |
"""
            with open(folder_17 / "tieu_chi_cham_diem_ai.md", "w", encoding="utf-8") as f:
                f.write(rubric_17)
            with open(folder_17 / "tieu_chi.md", "w", encoding="utf-8") as f:
                f.write(rubric_17)

            # Save in root as well
            with open(target_homework_dir / "bai_tap_mindmap.md", "w", encoding="utf-8") as f:
                f.write(mindmap_ex_content)

        # 5. Save aggregated tieu_chi_danh_gia.md for all exercises
        with open(target_homework_dir / "tieu_chi_danh_gia.md", "w", encoding="utf-8") as f:
            f.write(f"# BẢNG TIÊU CHÍ ĐÁNH GIÁ TỔNG HỢP (100đ) - {session_title}\n\n")
            for ex in exercises_data:
                f.write(f"## {ex['title']}\n\n{ex['tieu_chi_content']}\n\n---\n\n")

        # 6. Automatic audit via HomeworkReviewerAgent
        try:
            from agents.reviewers.homework_reviewer import review_session_homework
            review_res = review_session_homework(target_homework_dir)
            print(f"  ✓ [Homework Reviewer] Trạng thái: {review_res['status']} ({review_res['score']}/100đ) - {review_res['total_folders']} thư mục, {review_res['total_root_files']} files gốc.")
        except Exception as e:
            print(f"  ! [Homework Reviewer] Cảnh báo kiểm định: {e}")

        print(f"  ✓ Đã lưu hoàn tất {len(exercises_data)} bài tập về nhà + 1 bài tổng hợp + 1 bài mindmap vào: {target_homework_dir}")

    return exercises_data
