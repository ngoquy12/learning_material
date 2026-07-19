"""
core/scorm_exporter.py

SCORM 1.2 Package Exporter
===========================
Mục tiêu: Cho phép xuất toàn bộ học liệu đã biên dịch sang định dạng
SCORM 1.2 — chuẩn eLearning quốc tế để nạp vào Moodle, Canvas, Blackboard LMS.

Hoạt động độc lập, KHÔNG đụng vào bất kỳ agent hay pipeline nào.
Chỉ đọc các file đã được sinh ra bởi session_compiler_agent từ thư mục output/.

Cấu trúc SCORM Package (.zip):
  /imsmanifest.xml           — Manifest mô tả cấu trúc khóa học
  /adlcp_rootv1p2.xsd        — Schema SCORM 1.2
  /ims_xml.xsd
  /imscp_rootv1p1p2.xsd
  /imsmd_rootv1p2p1.xsd
  /course/                   — Tất cả nội dung bài học
    /session_XX/
      /lesson_YY/
        reading.html         — Bài đọc (từ output/)
        quiz.json            — Quiz data
        lesson.html          — Wrapper page
  /shared/
    scorm_api.js             — SCORM 1.2 API wrapper
    style.css                — Global styles

Cách chạy:
  python -m core.scorm_exporter --output output/MyCourseName --course-name "Tên Khóa Học"
  hoặc qua main.py: python main.py --pm ... --approve-pm --scorm
"""

import os
import json
import zipfile
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


# ─────────────────────────────────────────────────────
# SCORM 1.2 XML Templates
# ─────────────────────────────────────────────────────

_MANIFEST_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{course_id}" version="1.2"
    xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
    xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                        http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd
                        http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
    <lom xmlns="http://www.imsglobal.org/xsd/imsmd_rootv1p2p1">
      <general>
        <title><langstring xml:lang="vi">{course_title}</langstring></title>
        <description><langstring xml:lang="vi">{course_description}</langstring></description>
      </general>
      <technical>
        <format>text/html</format>
      </technical>
    </lom>
  </metadata>
  <organizations default="{org_id}">
    <organization identifier="{org_id}" structure="hierarchical">
      <title>{course_title}</title>
{items}
    </organization>
  </organizations>
  <resources>
{resources}
  </resources>
</manifest>
"""

_ITEM_TEMPLATE = """\
      <item identifier="{item_id}" identifierref="{res_id}" isvisible="true">
        <title>{title}</title>
        <adlcp:prerequisites type="aicc_script">{prereqs}</adlcp:prerequisites>
      </item>"""

_RESOURCE_TEMPLATE = """\
    <resource identifier="{res_id}" type="webcontent" adlcp:scormtype="sco" href="{href}">
      <file href="{href}"/>
      <file href="shared/scorm_api.js"/>
      <file href="shared/style.css"/>
    </resource>"""

_LESSON_WRAPPER_TEMPLATE = """\
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{lesson_title}</title>
<link rel="stylesheet" href="../../shared/style.css">
<script src="../../shared/scorm_api.js"></script>
</head>
<body>
<div id="scorm-header">
  <div class="breadcrumb">{session_id} &rsaquo; {lesson_id}</div>
  <h1>{lesson_title}</h1>
  <div class="scorm-status" id="status-bar">Đang tải...</div>
</div>
<div id="content-frame-container">
  <iframe id="content-frame" src="reading.html" title="Nội dung bài học"></iframe>
</div>
<div id="scorm-footer">
  <button onclick="SCORM.completeCourse()" class="btn-complete">✅ Đánh dấu hoàn thành bài học</button>
  <button onclick="window.history.back()" class="btn-back">← Bài trước</button>
</div>
<script>
  document.addEventListener('DOMContentLoaded', function() {{
    SCORM.init();
    document.getElementById('status-bar').textContent = 'Đang học: {lesson_title}';
    SCORM.setStatus('incomplete');
  }});
</script>
</body>
</html>
"""

_SCORM_API_JS = """\
/**
 * SCORM 1.2 API Wrapper — Elearning Content Factory
 * Tương thích: Moodle, Canvas, Blackboard, TalentLMS, SCORM Cloud
 */
const SCORM = (function() {
    let _apiHandle = null;
    let _initialized = false;

    function _findAPI(win) {
        let tries = 0;
        while (win.API == null && win.parent != null && win.parent != win) {
            tries++;
            if (tries > 7) return null;
            win = win.parent;
        }
        return win.API;
    }

    function _getAPI() {
        if (_apiHandle) return _apiHandle;
        _apiHandle = _findAPI(window);
        if (!_apiHandle && window.opener) {
            _apiHandle = _findAPI(window.opener);
        }
        return _apiHandle;
    }

    return {
        init: function() {
            const api = _getAPI();
            if (!api) { console.warn('[SCORM] API not found (running outside LMS)'); return false; }
            const result = api.LMSInitialize('');
            _initialized = result === 'true' || result === true;
            if (_initialized) console.log('[SCORM] Initialized successfully.');
            return _initialized;
        },

        setStatus: function(status) {
            // status: 'passed' | 'failed' | 'completed' | 'incomplete' | 'not attempted' | 'browsed'
            const api = _getAPI();
            if (!api || !_initialized) return;
            api.LMSSetValue('cmi.core.lesson_status', status);
            api.LMSCommit('');
        },

        completeCourse: function() {
            const api = _getAPI();
            if (!api || !_initialized) {
                alert('Bài học đã được đánh dấu hoàn thành!');
                return;
            }
            api.LMSSetValue('cmi.core.lesson_status', 'completed');
            api.LMSSetValue('cmi.core.score.raw', '100');
            api.LMSSetValue('cmi.core.score.max', '100');
            api.LMSSetValue('cmi.core.score.min', '0');
            api.LMSCommit('');
            api.LMSFinish('');
            document.getElementById('status-bar').textContent = '✅ Đã hoàn thành!';
            document.getElementById('status-bar').style.color = '#22c55e';
        },

        finish: function() {
            const api = _getAPI();
            if (api && _initialized) {
                api.LMSFinish('');
                _initialized = false;
            }
        }
    };
})();

window.addEventListener('beforeunload', function() { SCORM.finish(); });
"""

_SCORM_CSS = """\
:root {
    --primary: #6366f1;
    --bg: #0f172a;
    --surface: #1e293b;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --success: #22c55e;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}
#scorm-header {
    padding: 12px 24px;
    background: var(--surface);
    border-bottom: 1px solid rgba(99,102,241,0.3);
    display: flex;
    align-items: center;
    gap: 16px;
}
#scorm-header h1 { font-size: 1.1rem; color: var(--text); flex: 1; }
.breadcrumb { font-size: 0.75rem; color: var(--muted); white-space: nowrap; }
.scorm-status { font-size: 0.8rem; color: var(--primary); white-space: nowrap; }
#content-frame-container { flex: 1; overflow: hidden; }
#content-frame { width: 100%; height: 100%; border: none; background: white; }
#scorm-footer {
    padding: 10px 24px;
    background: var(--surface);
    border-top: 1px solid rgba(99,102,241,0.2);
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}
.btn-complete {
    background: var(--primary);
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}
.btn-complete:hover { opacity: 0.85; }
.btn-back {
    background: transparent;
    color: var(--muted);
    border: 1px solid var(--muted);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
}
.btn-back:hover { color: var(--text); border-color: var(--text); }
"""

_SCORM_INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>{course_title} — SCORM Package</title>
<style>
    body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px; }}
    h1 {{ color: #6366f1; margin-bottom: 8px; }}
    p {{ color: #94a3b8; margin-bottom: 32px; }}
    .session {{ margin-bottom: 24px; }}
    .session-title {{ font-size: 1.1rem; font-weight: 600; color: #818cf8; margin-bottom: 8px; }}
    .lesson-link {{ display: block; padding: 8px 16px; color: #e2e8f0; text-decoration: none;
                    border: 1px solid #334155; border-radius: 6px; margin: 4px 0;
                    transition: all 0.2s; }}
    .lesson-link:hover {{ background: #1e293b; border-color: #6366f1; }}
</style>
</head>
<body>
<h1>📚 {course_title}</h1>
<p>Danh sách bài học trong SCORM Package. Mở từng bài học để học trực tuyến.</p>
{toc}
</body>
</html>
"""


# ─────────────────────────────────────────────────────
# Core Export Function
# ─────────────────────────────────────────────────────

def export_scorm_package(
    output_course_dir: str,
    course_name: str,
    scorm_output_path: Optional[str] = None,
) -> str:
    """
    Xuất học liệu đã biên dịch thành SCORM 1.2 .zip package.

    Args:
        output_course_dir: Thư mục chứa kết quả từ session_compiler
                           (ví dụ: 'output/PM_Web_Application_With_FastAPI')
        course_name: Tên khóa học hiển thị trong LMS
        scorm_output_path: Đường dẫn file .zip đầu ra (tùy chọn)

    Returns:
        Đường dẫn tuyệt đối tới file .zip đã tạo
    """
    output_dir = Path(output_course_dir)
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_course_dir}")

    # Xác định đường dẫn đầu ra
    if not scorm_output_path:
        safe_name = re.sub(r'[^\w\-_]', '_', course_name)[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        scorm_output_path = str(output_dir.parent / f"SCORM_{safe_name}_{timestamp}.zip")

    print(f"\n[SCORM Exporter] Bắt đầu đóng gói SCORM cho: {course_name}")
    print(f"[SCORM Exporter] Nguồn: {output_course_dir}")
    print(f"[SCORM Exporter] Đích: {scorm_output_path}")

    # Thu thập danh sách bài học từ cấu trúc thư mục output/
    lessons = _scan_lessons(output_dir)
    print(f"[SCORM Exporter] Tìm thấy {len(lessons)} bài học.")

    if not lessons:
        raise ValueError(
            f"Không tìm thấy bài học nào trong {output_course_dir}. "
            "Hãy chạy pipeline biên dịch học liệu trước khi xuất SCORM."
        )

    # Build manifest XML
    course_id = f"course_{abs(hash(course_name)) % 10**8}"
    org_id = f"org_{course_id}"
    items_xml = []
    resources_xml = []
    toc_html = []

    for idx, lesson in enumerate(lessons):
        item_id = f"item_{idx:04d}"
        res_id = f"res_{idx:04d}"
        href = f"course/{lesson['rel_path']}/lesson.html"
        prereqs = f"res_{(idx-1):04d}" if idx > 0 else ""

        items_xml.append(_ITEM_TEMPLATE.format(
            item_id=item_id,
            res_id=res_id,
            title=lesson["title"],
            prereqs=prereqs,
        ))
        resources_xml.append(_RESOURCE_TEMPLATE.format(
            res_id=res_id,
            href=href,
        ))

    manifest = _MANIFEST_TEMPLATE.format(
        course_id=course_id,
        org_id=org_id,
        course_title=_xml_escape(course_name),
        course_description=_xml_escape(f"SCORM Package cho khóa học {course_name}"),
        items="\n".join(items_xml),
        resources="\n".join(resources_xml),
    )

    # Build TOC HTML
    current_session = None
    session_html = []
    for lesson in lessons:
        if lesson["session_id"] != current_session:
            if session_html:
                toc_html.append(f'<div class="session"><div class="session-title">{current_session}</div>{"".join(session_html)}</div>')
                session_html = []
            current_session = lesson["session_id"]
        session_html.append(f'<a class="lesson-link" href="course/{lesson["rel_path"]}/lesson.html">{lesson["lesson_id"]}: {lesson["title"]}</a>')
    if session_html:
        toc_html.append(f'<div class="session"><div class="session-title">{current_session}</div>{"".join(session_html)}</div>')

    index_html = _SCORM_INDEX_TEMPLATE.format(
        course_title=course_name,
        toc="\n".join(toc_html),
    )

    # Ghi zip file
    with zipfile.ZipFile(scorm_output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Manifest & root files
        zf.writestr("imsmanifest.xml", manifest)
        zf.writestr("index.html", index_html)

        # Shared assets
        zf.writestr("shared/scorm_api.js", _SCORM_API_JS)
        zf.writestr("shared/style.css", _SCORM_CSS)

        # Lesson content
        for lesson in lessons:
            base_path = f"course/{lesson['rel_path']}"

            # lesson.html wrapper
            wrapper_html = _LESSON_WRAPPER_TEMPLATE.format(
                lesson_title=lesson["title"],
                session_id=lesson["session_id"],
                lesson_id=lesson["lesson_id"],
            )
            zf.writestr(f"{base_path}/lesson.html", wrapper_html)

            # reading.html (nếu có)
            reading_path = lesson["abs_path"] / "reading.html"
            if reading_path.exists():
                zf.write(reading_path, f"{base_path}/reading.html")
            else:
                # Fallback: placeholder
                zf.writestr(f"{base_path}/reading.html",
                            f"<html><body><h1>{lesson['title']}</h1><p>Nội dung đang được cập nhật.</p></body></html>")

            # quiz.json (nếu có)
            quiz_path = lesson["abs_path"] / "quiz.json"
            if quiz_path.exists():
                zf.write(quiz_path, f"{base_path}/quiz.json")

            # slides.html (nếu có)
            slides_path = lesson["abs_path"] / "slides.html"
            if slides_path.exists():
                zf.write(slides_path, f"{base_path}/slides.html")

    size_mb = Path(scorm_output_path).stat().st_size / (1024 * 1024)
    print(f"\n[SCORM Exporter] ✅ Package đã tạo thành công!")
    print(f"  📦 File: {scorm_output_path}")
    print(f"  📏 Kích thước: {size_mb:.2f} MB")
    print(f"  📚 Số bài học: {len(lessons)}")
    print(f"  💡 Hướng dẫn: Nạp file .zip này trực tiếp vào Moodle, Canvas hoặc SCORM Cloud.")
    return scorm_output_path


# ─────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────

def _scan_lessons(output_dir: Path) -> List[Dict]:
    """
    Quét cấu trúc thư mục output/ để tìm tất cả bài học đã biên dịch.
    Hỗ trợ cấu trúc: output/course/Session_XX/Lesson_XX/reading.html
    """
    lessons = []
    for session_dir in sorted(output_dir.iterdir()):
        if not session_dir.is_dir():
            continue
        session_id = session_dir.name

        for lesson_dir in sorted(session_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue

            # Kiểm tra có nội dung không
            has_content = (
                (lesson_dir / "reading.html").exists()
                or (lesson_dir / "quiz.json").exists()
            )
            if not has_content:
                continue

            # Parse lesson title từ tên thư mục
            lesson_id = lesson_dir.name
            title = lesson_id.replace("_", " ")
            if " - " in title:
                parts = title.split(" - ", 1)
                lesson_id_clean = parts[0].strip()
                title = parts[1].strip() if len(parts) > 1 else title
            else:
                lesson_id_clean = lesson_id

            rel_path = f"{session_id}/{lesson_dir.name}"
            lessons.append({
                "session_id": session_id,
                "lesson_id": lesson_id_clean,
                "title": title,
                "rel_path": rel_path,
                "abs_path": lesson_dir,
            })

    return lessons


def _xml_escape(text: str) -> str:
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))


# ─────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SCORM 1.2 Package Exporter")
    parser.add_argument("--output", required=True, help="Thư mục output/ của khóa học đã biên dịch")
    parser.add_argument("--course-name", required=True, help="Tên khóa học hiển thị trong LMS")
    parser.add_argument("--dest", default=None, help="Đường dẫn file .zip đầu ra (tùy chọn)")
    args = parser.parse_args()

    export_scorm_package(
        output_course_dir=args.output,
        course_name=args.course_name,
        scorm_output_path=args.dest,
    )
