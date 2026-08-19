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
from pathlib import Path
from typing import Dict, Any, List, Optional
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


def generate_session_homework_suite(
    session_id: str,
    session_title: str,
    tech_stack: str,
    previous_lessons_text: str = "",
    forbidden_scope: str = "",
    course_dir: Optional[Path] = None,
    total_exercises: int = 6
) -> List[Dict[str, Any]]:
    """
    Generates a full suite of homework assignments for a session
    distributed across Bloom taxonomy levels.
    """
    levels = [
        ("Cơ bản 1 - Debug lỗi", "E-Commerce"),
        ("Cơ bản 2 - Kiểm thử I/O", "Logistics"),
        ("Nâng cao 1 - Tính năng mới", "FinTech"),
        ("Nâng cao 2 - Nghiệp vụ phức tạp", "Healthcare"),
        ("Tối ưu hóa - Tái cấu trúc", "CRM"),
        ("Sáng tạo - Thiết kế Mini Module", "EdTech")
    ]

    exercises_data = []
    print(f"\n[Homework Creator] 🚀 Bắt đầu sinh bộ {total_exercises} bài tập về nhà cho {session_id} ({tech_stack})...")

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

    with ThreadPoolExecutor(max_workers=min(total_exercises, 6)) as executor:
        futures = [executor.submit(_gen_one, i) for i in range(1, total_exercises + 1)]
        for f in futures:
            try:
                res = f.result()
                exercises_data.append(res)
            except Exception as e:
                print(f"  ❌ Lỗi khi sinh bài tập về nhà: {e}")

    exercises_data.sort(key=lambda x: x.get("idx", 0))

    # Export to disk if course_dir is provided
    if course_dir:
        homework_dir = course_dir / session_id / "Bài tập về nhà"
        homework_dir.mkdir(parents=True, exist_ok=True)

        for ex in exercises_data:
            idx = ex["idx"]
            ex_folder = homework_dir / f"bai_{idx:02d}"
            ex_folder.mkdir(parents=True, exist_ok=True)
            with open(ex_folder / "de_bai.md", "w", encoding="utf-8") as f:
                f.write(ex["de_bai_content"])
            with open(ex_folder / "tieu_chi.md", "w", encoding="utf-8") as f:
                f.write(ex["tieu_chi_content"])

        print(f"  ✓ Đã lưu {len(exercises_data)} bài tập về nhà vào: {homework_dir}")

    return exercises_data
