import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


# ── DANH SÁCH TỪ NGỮ BỊ CẤM (Section 4.3 — Academic Lecturer Tone) ──────────

_FORBIDDEN_GROUPS: List[Tuple[str, List[str]]] = [
    (
        "Từ sến súa / thân mật quá mức",
        [
            r"\bnhé\b", r"\bnha\b", r"\bnhen\b", r"\bnghen\b",
            r"các em ơi", r"các em thân mến", r"các bạn ơi",
            r"các bạn thân mến", r"mọi người ơi",
            r"chúc các em", r"chúc các bạn",
            r"cố lên\s+nhé", r"cố gắng nhé",
            r"học tốt nhé", r"thành công nhé",
        ],
    ),
    (
        "Từ xưng hô sai chuẩn đại học",
        [
            # "các em" đơn lẻ (không phải "các em đã", "các em sẽ" trong câu học thuật)
            r"các em\s+ơi",
            r"các em\s+thân",
            r"các em\s+nhé",
            r"các em\s+nha",
            r"(?<!\w)ơi các em(?!\w)",
        ],
    ),
    (
        "Từ kích động / chết chóc",
        [
            r"\bchết chóc\b", r"\bchết người\b", r"\btiêu tùng\b", r"\btiêu rồi\b",
            r"\bthảm họa\b", r"\bthảm khốc\b", r"\bthảm bại\b",
            r"\bkhủng khiếp\b", r"\bhãi hùng\b", r"\bkinh khủng\b",
            r"\bnguy hiểm chết\b", r"\blỗi chết người\b",
            r"\bsụp đổ hoàn toàn\b",
        ],
    ),
    (
        "Từ phóng đại / thiếu nghiêm túc",
        [
            r"\bđỉnh của đỉnh\b", r"\bhuyền thoại\b", r"\bthần thánh\b",
            r"\bvô địch\b", r"\bbá đạo\b", r"\bảo diệu\b",
            r"\bxịn xò\b", r"\bngầu lòi\b", r"\bhack não\b",
            r"\bcháy hết mình\b",
        ],
    ),
    (
        "Lời kêu gọi mạng xã hội",
        [
            r"\blike\b", r"\bsubscribe\b",
            r"đăng ký kênh", r"nhấn chuông",
            r"ủng hộ kênh", r"comment bên dưới",
            r"nếu thích thì", r"nếu hay thì",
            r"hãy chia sẻ",
        ],
    ),
]


def _check_narration_tone(text: str) -> List[str]:
    """
    Quét toàn bộ văn bản lời thoại, phát hiện các vi phạm Giọng văn Giảng viên Đại học.
    Trả về danh sách mô tả vi phạm (rỗng = không vi phạm).
    """
    violations: List[str] = []
    for group_name, patterns in _FORBIDDEN_GROUPS:
        for pattern in patterns:
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                sample = matches[0][:40]
                violations.append(
                    f"[{group_name}] Tìm thấy từ bị cấm: \"{sample}\""
                )
    return violations


def video_qa_reviewer_agent(project_path: str) -> Dict[str, Any]:
    """
    Video QA Reviewer Agent:
    Validates scaffolded project files and assets on disk to ensure 100% correctness:
      - Cổng 1: Kiểm định File & Assets (intro, outro, bg-music, voiceovers .wav).
      - Cổng 2: Kiểm định Timing (Đồng bộ thời lượng, dịch chuyển mốc intro 9.24s).
      - Cổng 3: Kiểm định HTML (Nhạc nền track 99, Phosphor Icons, No ALL CAPS).
      - Cổng 4: Kiểm định Giọng văn Narration (Section 4.3 — Forbidden Words Policy).
    """
    print(f"\n🚀 [Video_QA_Reviewer] Bắt đầu quét kiểm định chất lượng dự án tại:\n📍 {project_path}")
    
    p = Path(project_path)
    index_html_path = p / "index.html"
    tts_dir = p / "assets" / "tts"
    assets_dir = p / "assets"
    
    # ── CỔNG 1: KIỂM ĐỊNH FILE & ASSETS ─────────────────────────────────────
    if not index_html_path.exists():
        msg = "Thiếu tệp tin cấu trúc chính index.html."
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    # Check templates
    for file in ["intro.mp4", "outro.mp4", "bg-music.mp3"]:
        f_path = assets_dir / file
        if not f_path.exists() or f_path.stat().st_size == 0:
            msg = f"Thiếu tệp hoặc tệp trống trong thư mục assets: {file}"
            print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    # Check durations.json
    durations_path = tts_dir / "durations.json"
    if not durations_path.exists():
        msg = "Không tìm thấy tệp durations.json trong assets/tts/."
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    try:
        durations = json.loads(durations_path.read_text(encoding="utf-8"))
    except Exception as e:
        msg = f"Lỗi đọc file durations.json: {e}"
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    if not durations:
        msg = "durations.json bị rỗng. Chưa chạy tts hoặc lỗi sinh âm thanh."
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    # Check voice wav files
    for scene_id in durations.keys():
        wav_file = tts_dir / f"{scene_id}.wav"
        mp3_file = tts_dir / f"{scene_id}.mp3"
        if not wav_file.exists() and not mp3_file.exists():
            msg = f"Thiếu tệp âm thanh voiceover (.wav/.mp3) cho scene: {scene_id}"
            print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    print("  ✓ Cổng 1 đạt yêu cầu: Đầy đủ tệp tin assets & âm thanh thoại.")

    # ── CỔNG 2: KIỂM ĐỊNH TIMING & ĐỒNG BỘ ──────────────────────────────────
    index_html = index_html_path.read_text(encoding="utf-8")
    
    # Check Intro video duration (must be 9.24)
    if 'id="intro-video"' in index_html and 'data-duration="9.24"' not in index_html:
        msg = "Video Intro bắt buộc có thời lượng chuẩn data-duration=\"9.24\"."
        print(f"  ❌ CỔNG 2 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    # Check first scene start time (must be 9.24s, shifted after intro)
    scene_clips = re.findall(r'class="clip"\s+data-composition-src="src/compositions/Scene_01\.html"\s+data-composition-id="scene-01"\s+data-start="([^"]+)"', index_html)
    if scene_clips:
        start_val = float(scene_clips[0])
        if start_val != 9.24:
            msg = f"Mốc thời gian của Scene_01 bắt đầu ở {start_val}s thay vì lùi sau Intro 9.24s."
            print(f"  ❌ CỔNG 2 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    print("  ✓ Cổng 2 đạt yêu cầu: Mốc thời gian được dịch chuyển khớp Intro/Outro.")

    # ── CỔNG 3: KIỂM ĐỊNH HTML & CHUẨN HOÁ GIAO DIỆN ───────────────────────
    # Check bg-music track
    bg_music_matches = re.findall(r'id="bg-music"\s+data-start="0"\s+data-duration="([^"]+)"\s+data-track-index="([^"]+)"', index_html)
    if bg_music_matches:
        music_dur, music_track = bg_music_matches[0]
        if music_track != "99":
            msg = f"Kênh nhạc nền bg-music đang gán track-index='{music_track}' thay vì track-index='99'."
            print(f"  ❌ CỔNG 3 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    # Check ALL CAPS in HTML headings or visual badges
    auto_fixed_files = []
    for sc_id in durations.keys():
        scene_html_path = p / "src" / "compositions" / f"{sc_id}.html"
        if scene_html_path.exists():
            sc_html = scene_html_path.read_text(encoding="utf-8")
            original = sc_html

            # Check Phosphor Icons import
            if "unpkg.com/@phosphor-icons/web" not in sc_html:
                msg = f"Tệp {sc_id}.html chưa nạp thư viện Phosphor Icons."
                print(f"  ❌ CỔNG 3 THẤT BẠI: {msg}")
                return {"status": "REJECTED", "feedback": msg}

            # AUTO-FIX: text-transform: uppercase → remove
            if "text-transform: uppercase" in sc_html or "text-transform:uppercase" in sc_html:
                sc_html = re.sub(r';\s*text-transform\s*:\s*uppercase', '', sc_html)
                sc_html = re.sub(r'text-transform\s*:\s*uppercase\s*;?', '', sc_html)
                print(f"  🔧 Auto-fixed text-transform:uppercase in {sc_id}.html")

            # AUTO-FIX: ALL CAPS text in h-tags → Sentence case
            def _fix_caps_htag(m):
                tag_open, text, tag_close = m.group(1), m.group(2), m.group(3)
                if text.strip() and text.strip() == text.strip().upper() and len(text.strip()) > 5 and any(c.isalpha() for c in text):
                    words = text.strip().split()
                    fixed = words[0].capitalize() + (' ' + ' '.join(w.lower() for w in words[1:]) if len(words) > 1 else '')
                    print(f"  🔧 Auto-fixed ALL CAPS title in {sc_id}.html: '{text.strip()}' → '{fixed}'")
                    return f'<{tag_open}>{fixed}</{tag_close}>'
                return m.group(0)
            sc_html = re.sub(r'<(h[1-6][^>]*)>([^<]+)</(h[1-6])>', _fix_caps_htag, sc_html)

            # Save if changed
            if sc_html != original:
                scene_html_path.write_text(sc_html, encoding="utf-8")
                auto_fixed_files.append(sc_id)

    if auto_fixed_files:
        print(f"  ✓ Cổng 3: Đã tự động sửa {len(auto_fixed_files)} tệp vi phạm chuẩn hoá.")
    print("  ✓ Cổng 3 đạt yêu cầu: Nhạc nền ở kênh 99, đầy đủ Phosphor Icons và không viết hoa toàn bộ.")


    # ── CỔNG 4: KIỂM ĐỊNH GIỌNG VĂN NARRATION (Section 4.3 — Zero Tolerance) ──
    # Quét SCRIPT.md (kịch bản lời thoại) nếu tồn tại
    script_paths_to_check: List[Path] = []

    # Tìm SCRIPT.md trong thư mục gốc hoặc thư mục con (Video/)
    for candidate in [p / "SCRIPT.md", p.parent / "SCRIPT.md", p / "Video" / "SCRIPT.md"]:
        if candidate.exists():
            script_paths_to_check.append(candidate)

    # Nếu không có SCRIPT.md, quét cả tts_dir *.txt nếu có
    if not script_paths_to_check:
        for txt_file in tts_dir.glob("*.txt"):
            script_paths_to_check.append(txt_file)

    all_narration_violations: List[str] = []
    for script_path in script_paths_to_check:
        try:
            script_text = script_path.read_text(encoding="utf-8")
            violations = _check_narration_tone(script_text)
            if violations:
                all_narration_violations.extend([f"[{script_path.name}] {v}" for v in violations])
        except Exception as e:
            print(f"  ⚠️  Không thể đọc {script_path.name} để kiểm định giọng văn: {e}")

    if all_narration_violations:
        summary = "; ".join(all_narration_violations[:5])  # hiển thị tối đa 5 vi phạm đầu
        msg = (
            f"Vi phạm quy tắc Giọng văn Giảng viên Đại học (Section 4.3). "
            f"Phát hiện {len(all_narration_violations)} lỗi:\n  → " + "\n  → ".join(all_narration_violations[:5])
        )
        print(f"  ❌ CỔNG 4 THẤT BẠI:\n  → {summary}")
        return {"status": "REJECTED", "feedback": msg}

    if script_paths_to_check:
        print(f"  ✓ Cổng 4 đạt yêu cầu: Giọng văn narration chuẩn Giảng viên Đại học (không từ bị cấm).")
    else:
        print(f"  ⚠️  Cổng 4: Không tìm thấy SCRIPT.md để kiểm định giọng văn narration.")

    print("🏆 [Video_QA_Reviewer] KIỂM ĐỊNH HOÀN TOÀN ĐẠT CHUẨN! Dự án video đủ điều kiện xuất MP4.")
    return {"status": "APPROVED", "feedback": "Dự án video đạt 100% tiêu chí chuẩn hóa."}

    
    p = Path(project_path)
    index_html_path = p / "index.html"
    tts_dir = p / "assets" / "tts"
    assets_dir = p / "assets"
    
    # ── CỔNG 1: KIỂM ĐỊNH FILE & ASSETS ─────────────────────────────────────
    if not index_html_path.exists():
        msg = "Thiếu tệp tin cấu trúc chính index.html."
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    # Check templates
    for file in ["intro.mp4", "outro.mp4", "bg-music.mp3"]:
        f_path = assets_dir / file
        if not f_path.exists() or f_path.stat().st_size == 0:
            msg = f"Thiếu tệp hoặc tệp trống trong thư mục assets: {file}"
            print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    # Check durations.json
    durations_path = tts_dir / "durations.json"
    if not durations_path.exists():
        msg = "Không tìm thấy tệp durations.json trong assets/tts/."
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    try:
        durations = json.loads(durations_path.read_text(encoding="utf-8"))
    except Exception as e:
        msg = f"Lỗi đọc file durations.json: {e}"
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    if not durations:
        msg = "durations.json bị rỗng. Chưa chạy tts hoặc lỗi sinh âm thanh."
        print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    # Check voice wav files
    for scene_id in durations.keys():
        wav_file = tts_dir / f"{scene_id}.wav"
        mp3_file = tts_dir / f"{scene_id}.mp3"
        if not wav_file.exists() and not mp3_file.exists():
            msg = f"Thiếu tệp âm thanh voiceover (.wav/.mp3) cho scene: {scene_id}"
            print(f"  ❌ CỔNG 1 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    print("  ✓ Cổng 1 đạt yêu cầu: Đầy đủ tệp tin assets & âm thanh thoại.")

    # ── CỔNG 2: KIỂM ĐỊNH TIMING & ĐỒNG BỘ ──────────────────────────────────
    index_html = index_html_path.read_text(encoding="utf-8")
    
    # Check Intro video duration (must be 9.24)
    if 'id="intro-video"' in index_html and 'data-duration="9.24"' not in index_html:
        msg = "Video Intro bắt buộc có thời lượng chuẩn data-duration=\"9.24\"."
        print(f"  ❌ CỔNG 2 THẤT BẠI: {msg}")
        return {"status": "REJECTED", "feedback": msg}
        
    # Check first scene start time (must be 9.24s, shifted after intro)
    scene_clips = re.findall(r'class="clip"\s+data-composition-src="src/compositions/Scene_01\.html"\s+data-composition-id="scene-01"\s+data-start="([^"]+)"', index_html)
    if scene_clips:
        start_val = float(scene_clips[0])
        if start_val != 9.24:
            msg = f"Mốc thời gian của Scene_01 bắt đầu ở {start_val}s thay vì lùi sau Intro 9.24s."
            print(f"  ❌ CỔNG 2 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    print("  ✓ Cổng 2 đạt yêu cầu: Mốc thời gian được dịch chuyển khớp Intro/Outro.")

    # ── CỔNG 3: KIỂM ĐỊNH HTML & CHUẨN HOÁ GIAO DIỆN ───────────────────────
    # Check bg-music track
    bg_music_matches = re.findall(r'id="bg-music"\s+data-start="0"\s+data-duration="([^"]+)"\s+data-track-index="([^"]+)"', index_html)
    if bg_music_matches:
        music_dur, music_track = bg_music_matches[0]
        if music_track != "99":
            msg = f"Kênh nhạc nền bg-music đang gán track-index='{music_track}' thay vì track-index='99'."
            print(f"  ❌ CỔNG 3 THẤT BẠI: {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
    # Check ALL CAPS in HTML headings or visual badges
    for sc_id in durations.keys():
        scene_html_path = p / "src" / "compositions" / f"{sc_id}.html"
        if scene_html_path.exists():
            sc_html = scene_html_path.read_text(encoding="utf-8")
            
            # Check Phosphor Icons import
            if "unpkg.com/@phosphor-icons/web" not in sc_html:
                msg = f"Tệp {sc_id}.html chưa nạp thư viện Phosphor Icons."
                print(f"  ❌ CỔNG 3 THẤT BẠI: {msg}")
                return {"status": "REJECTED", "feedback": msg}
                
            # Check ALL CAPS text transform
            if "text-transform: uppercase" in sc_html or "text-transform:uppercase" in sc_html:
                msg = f"Tệp {sc_id}.html vi phạm quy chuẩn: sử dụng text-transform: uppercase."
                print(f"  ❌ CỔNG 3 THẤT BẠI: {msg}")
                return {"status": "REJECTED", "feedback": msg}
                
            # Check actual uppercase Vietnamese words in header tags
            h_tags = re.findall(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', sc_html)
            for text in h_tags:
                if text.isupper() and len(text.strip()) > 5:
                    msg = f"Tệp {sc_id}.html vi phạm quy chuẩn: tiêu đề viết IN HOA TOÀN BỘ '{text}'."
                    print(f"  ❌ CỔNG 3 THẤT BẠI: {msg}")
                    return {"status": "REJECTED", "feedback": msg}

    print("  ✓ Cổng 3 đạt yêu cầu: Nhạc nền ở kênh 99, đầy đủ Phosphor Icons và không viết hoa toàn bộ.")
    
    print("🏆 [Video_QA_Reviewer] KIỂM ĐỊNH HOÀN TOÀN ĐẠT CHUẨN! Dự án video đủ điều kiện xuất MP4.")
    return {"status": "APPROVED", "feedback": "Dự án video đạt 100% tiêu chí chuẩn hóa."}
