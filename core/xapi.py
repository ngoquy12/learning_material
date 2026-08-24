"""
core/xapi.py — Phát biểu xAPI (Experience API) cho học liệu xuất bản (F1).

Vì sao cần, khi đã có SCORM 1.2: SCORM 1.2 chỉ báo về LMS được vài trường nghèo nàn
(`lesson_status`, `score.raw`, `session_time`). Với chúng, câu hỏi duy nhất trả lời
được là "sinh viên đã xong chưa và được mấy điểm". Những câu hỏi thực sự dùng để cải
tiến học liệu thì không:

    - Bài đọc nào sinh viên mở rồi bỏ giữa chừng?
    - Câu quiz nào cả lớp cùng sai?
    - Phần nào tốn nhiều thời gian bất thường so với thời lượng thiết kế?

xAPI ghi từng sự kiện học tập thành một phát biểu độc lập (actor - verb - object) gửi
về LRS, nên trả lời được. Đây là mảnh ghép để dữ liệu người học chảy ngược về
knowledge_memory_agent và khép vòng tự cải tiến.

RÀNG BUỘC PHẠM VI — quan trọng:
Toàn bộ mã theo dõi nằm ở lớp BỌC NGOÀI (`lesson.html` do bộ xuất bản sinh ra), không
bao giờ đi vào `reading.html`. Thiết kế bài đọc là vùng đóng băng, và
tests/test_golden_design.py sẽ đỏ ngay nếu có gì lọt vào. Bài đọc được nhúng nguyên
vẹn trong iframe; lớp bọc theo dõi vòng đời (mở bài, thời lượng, đánh dấu hoàn thành)
và mở sẵn một API để nội dung TỰ NGUYỆN gọi nếu sau này muốn — chứ lớp bọc không
thò tay vào trong.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

# Định danh động từ theo từ vựng ADL chuẩn — LRS nào cũng hiểu.
VERB_INITIALIZED = "http://adlnet.gov/expapi/verbs/initialized"
VERB_EXPERIENCED = "http://adlnet.gov/expapi/verbs/experienced"
VERB_COMPLETED = "http://adlnet.gov/expapi/verbs/completed"
VERB_ANSWERED = "http://adlnet.gov/expapi/verbs/answered"
VERB_TERMINATED = "http://adlnet.gov/expapi/verbs/terminated"

_VERB_DISPLAY = {
    VERB_INITIALIZED: "initialized",
    VERB_EXPERIENCED: "experienced",
    VERB_COMPLETED: "completed",
    VERB_ANSWERED: "answered",
    VERB_TERMINATED: "terminated",
}

ACTIVITY_TYPE_LESSON = "http://adlnet.gov/expapi/activities/lesson"
ACTIVITY_TYPE_QUESTION = "http://adlnet.gov/expapi/activities/question"


def build_activity_id(base_iri: str, course: str, session_id: str, lesson_id: str = "") -> str:
    """
    Dựng IRI định danh một bài học.

    IRI phải ỔN ĐỊNH giữa các lần xuất bản: nếu mỗi lần xuất lại sinh một id khác,
    dữ liệu học tập của cùng một bài sẽ nằm rải rác thành nhiều hoạt động rời rạc
    trong LRS và không cộng lại được.
    """
    base = (base_iri or "http://rikkei.edu.vn/xapi").rstrip("/")
    parts = [p.strip().replace(" ", "_") for p in (course, session_id, lesson_id) if p and p.strip()]
    return base + "/" + "/".join(parts)


def build_statement(
    actor_name: str,
    actor_email: str,
    verb_id: str,
    activity_id: str,
    activity_name: str,
    activity_type: str = ACTIVITY_TYPE_LESSON,
    result: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Dựng một phát biểu xAPI 1.0.3 hợp lệ."""
    statement: Dict[str, Any] = {
        "actor": {
            "objectType": "Agent",
            "name": actor_name or "Học viên",
            "mbox": f"mailto:{actor_email}" if actor_email else "mailto:unknown@example.org",
        },
        "verb": {
            "id": verb_id,
            "display": {"en-US": _VERB_DISPLAY.get(verb_id, "experienced")},
        },
        "object": {
            "objectType": "Activity",
            "id": activity_id,
            "definition": {
                "name": {"vi-VN": activity_name},
                "type": activity_type,
            },
        },
    }
    if result:
        statement["result"] = result
    if timestamp:
        statement["timestamp"] = timestamp
    return statement


def build_cmi5_course_structure(
    course_name: str,
    lessons: List[Dict[str, Any]],
    base_iri: str = "http://rikkei.edu.vn/xapi",
) -> str:
    """
    Dựng file cmi5.xml — bản kê cấu trúc khoá học cho LMS hỗ trợ cmi5.

    cmi5 là "hồ sơ" chuẩn hoá cách dùng xAPI trong LMS, đóng vai trò như
    imsmanifest.xml của SCORM. Xuất kèm cả hai để gói học liệu nạp được vào cả LMS
    đời cũ (SCORM 1.2) lẫn LMS hỗ trợ xAPI, mà không phải chọn một bỏ một.
    """
    from xml.sax.saxutils import escape

    base = (base_iri or "http://rikkei.edu.vn/xapi").rstrip("/")
    course_id = build_activity_id(base, course_name, "")

    au_blocks = []
    for lesson in lessons:
        session_id = str(lesson.get("session_id", ""))
        lesson_id = str(lesson.get("lesson_id", ""))
        title = str(lesson.get("title", "")) or lesson_id or session_id
        rel_path = str(lesson.get("rel_path", "")).replace("\\", "/")
        au_id = build_activity_id(base, course_name, session_id, lesson_id)

        au_blocks.append(
            f'''    <au id="{escape(au_id)}" moveOn="CompletedOrPassed">
        <title><langstring lang="vi-VN">{escape(title)}</langstring></title>
        <description><langstring lang="vi-VN">{escape(session_id)} - {escape(lesson_id)}</langstring></description>
        <url>course/{escape(rel_path)}/lesson.html</url>
    </au>'''
        )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<courseStructure xmlns="https://w3id.org/xapi/profiles/cmi5/v1/CourseStructure.xsd">
    <course id="{escape(course_id)}">
        <title><langstring lang="vi-VN">{escape(course_name)}</langstring></title>
        <description><langstring lang="vi-VN">Học liệu sinh tự động — {escape(course_name)}</langstring></description>
    </course>
{chr(10).join(au_blocks)}
</courseStructure>
'''


def build_xapi_client_js(endpoint: str = "", auth_token: str = "") -> str:
    """
    Sinh mã JS phát xAPI, nhúng vào lớp BỌC của gói xuất bản.

    Ba lựa chọn thiết kế đáng nói:

    1. Không có endpoint thì bộ phát chạy ở chế độ ghi log (in ra console). Gói học
       liệu vẫn dùng được bình thường, chỉ là không gửi đi đâu — tốt hơn nhiều so
       với việc gói hỏng vì thiếu cấu hình.
    2. Danh tính người học lấy từ tham số URL do LMS truyền vào (`actor`), theo đúng
       cách cmi5 khởi chạy một AU. Tuyệt đối không tự đoán hay tự bịa danh tính.
    3. Gửi bằng `navigator.sendBeacon` khi rời trang, vì `fetch` thường bị huỷ giữa
       chừng lúc trang đóng — đó đúng là lúc phát biểu `terminated` và thời lượng
       học được gửi đi.
    """
    endpoint_js = json.dumps((endpoint or "").rstrip("/"))
    auth_js = json.dumps(auth_token or "")

    return """/**
 * xAPI emitter — Elearning Content Factory
 *
 * Nằm ở lớp bọc ngoài của gói xuất bản. KHÔNG bao giờ được nhúng vào reading.html:
 * thiết kế bài đọc là vùng đóng băng và có test golden canh giữ.
 */
(function (global) {
  var ENDPOINT = __ENDPOINT__;
  var AUTH = __AUTH__;

  function queryParam(name) {
    var m = new RegExp("[?&]" + name + "=([^&]*)").exec(global.location.search);
    return m ? decodeURIComponent(m[1].replace(/\\+/g, " ")) : "";
  }

  // Danh tính do LMS truyền vào theo cách cmi5 khởi chạy AU. Không tự đoán.
  function resolveActor() {
    var raw = queryParam("actor");
    if (raw) {
      try {
        var parsed = JSON.parse(raw);
        if (parsed && (parsed.mbox || parsed.account)) return parsed;
      } catch (e) { /* rơi xuống nhánh mặc định */ }
    }
    return {
      objectType: "Agent",
      name: queryParam("actorName") || "Học viên",
      mbox: "mailto:" + (queryParam("actorEmail") || "unknown@example.org")
    };
  }

  var VERBS = {
    initialized: "http://adlnet.gov/expapi/verbs/initialized",
    experienced: "http://adlnet.gov/expapi/verbs/experienced",
    completed: "http://adlnet.gov/expapi/verbs/completed",
    answered: "http://adlnet.gov/expapi/verbs/answered",
    terminated: "http://adlnet.gov/expapi/verbs/terminated"
  };

  var startedAt = Date.now();

  function isoDuration(ms) {
    return "PT" + Math.max(0, Math.round(ms / 1000)) + "S";
  }

  function buildStatement(verbKey, activityId, activityName, result) {
    var st = {
      actor: resolveActor(),
      verb: { id: VERBS[verbKey] || VERBS.experienced, display: { "en-US": verbKey } },
      object: {
        objectType: "Activity",
        id: activityId,
        definition: {
          name: { "vi-VN": activityName || "" },
          type: "http://adlnet.gov/expapi/activities/lesson"
        }
      },
      timestamp: new Date().toISOString()
    };
    if (result) st.result = result;
    return st;
  }

  function send(statement, useBeacon) {
    // Không cấu hình endpoint thì chạy ở chế độ ghi log. Gói học liệu vẫn dùng
    // được bình thường thay vì hỏng vì thiếu cấu hình.
    if (!ENDPOINT) {
      if (global.console && console.debug) console.debug("[xAPI]", statement);
      return;
    }
    var url = ENDPOINT + "/statements";
    var body = JSON.stringify(statement);

    // sendBeacon khi rời trang: fetch hay bị huỷ giữa chừng lúc trang đóng, mà đó
    // đúng là lúc gửi 'terminated' kèm thời lượng học.
    if (useBeacon && global.navigator && navigator.sendBeacon) {
      try {
        navigator.sendBeacon(url, new Blob([body], { type: "application/json" }));
        return;
      } catch (e) { /* rơi xuống fetch */ }
    }

    try {
      var headers = { "Content-Type": "application/json", "X-Experience-API-Version": "1.0.3" };
      if (AUTH) headers["Authorization"] = AUTH;
      global.fetch(url, { method: "POST", headers: headers, body: body, keepalive: true })
        .catch(function () { /* mất thống kê không được phép làm hỏng bài học */ });
    } catch (e) { /* im lặng */ }
  }

  var XAPI = {
    activityId: "",
    activityName: "",

    configure: function (activityId, activityName) {
      this.activityId = activityId;
      this.activityName = activityName;
    },

    initialized: function () {
      startedAt = Date.now();
      send(buildStatement("initialized", this.activityId, this.activityName));
    },

    experienced: function () {
      send(buildStatement("experienced", this.activityId, this.activityName));
    },

    completed: function (scoreScaled) {
      var result = { completion: true, duration: isoDuration(Date.now() - startedAt) };
      if (typeof scoreScaled === "number") result.score = { scaled: scoreScaled };
      send(buildStatement("completed", this.activityId, this.activityName, result));
    },

    // Mở sẵn cho nội dung TỰ NGUYỆN gọi. Lớp bọc không thò tay vào trong iframe.
    answered: function (questionId, questionText, isCorrect, response) {
      var st = buildStatement("answered", this.activityId + "/q/" + questionId, questionText, {
        success: !!isCorrect,
        response: String(response == null ? "" : response)
      });
      st.object.definition.type = "http://adlnet.gov/expapi/activities/question";
      send(st);
    },

    terminated: function () {
      send(
        buildStatement("terminated", this.activityId, this.activityName, {
          duration: isoDuration(Date.now() - startedAt)
        }),
        true
      );
    }
  };

  global.XAPI = XAPI;
})(window);
""".replace("__ENDPOINT__", endpoint_js).replace("__AUTH__", auth_js)


def build_wrapper_tracking_snippet(activity_id: str, activity_name: str) -> str:
    """
    Đoạn script gắn vòng đời bài học vào bộ phát, đặt trong lớp BỌC.

    Chỉ theo dõi những gì lớp bọc thực sự sở hữu: mở bài, rời bài, thời lượng, và
    nút đánh dấu hoàn thành có sẵn của lớp bọc.
    """
    return f"""<script src="../../shared/xapi.js"></script>
<script>
  (function () {{
    if (!window.XAPI) return;
    XAPI.configure({json.dumps(activity_id)}, {json.dumps(activity_name)});
    document.addEventListener('DOMContentLoaded', function () {{
      XAPI.initialized();
      XAPI.experienced();
    }});
    window.addEventListener('pagehide', function () {{ XAPI.terminated(); }});
  }})();
</script>"""


__all__ = [
    "VERB_INITIALIZED",
    "VERB_EXPERIENCED",
    "VERB_COMPLETED",
    "VERB_ANSWERED",
    "VERB_TERMINATED",
    "ACTIVITY_TYPE_LESSON",
    "ACTIVITY_TYPE_QUESTION",
    "build_activity_id",
    "build_statement",
    "build_cmi5_course_structure",
    "build_xapi_client_js",
    "build_wrapper_tracking_snippet",
]
