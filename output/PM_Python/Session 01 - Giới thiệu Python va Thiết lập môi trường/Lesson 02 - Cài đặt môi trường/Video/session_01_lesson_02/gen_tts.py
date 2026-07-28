"""
gen_tts.py — Kokoro-Vietnamese Audio Generator & Director Cue Processor
"""
import os
import sys
import json
import soundfile as sf

# Thêm đường dẫn Kokoro-Vietnamese
sys.path.insert(0, os.path.abspath("../../Kokoro-Vietnamese"))

try:
    from kokoro_vietnamese import KokoroVietnamese
except ImportError:
    KokoroVietnamese = None

CLEAN_TTS_SCRIPTS = {
  "Scene_01": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong bài học ngày hôm nay, chúng ta sẽ cùng nhau tìm hiểu chi tiết về Tổng quan về List trong Python. Đây là một chủ đề cực kỳ quan trọng và thiết yếu trong Python Core.",
  "Scene_02": "Tiếp theo, chúng ta sẽ tìm hiểu sâu hơn về: Tổng quan về List trong Python. Đây là kiến thức nền tảng mà mỗi lập trình viên đều cần nắm vững khi làm việc với Python Core. Các em lưu ý phần quan trọng này nhé: hãy chú ý quan sát từng bước thực hiện trên màn hình và ghi nhớ những điểm mấu chốt.",
  "Scene_03": "Tiếp theo, chúng ta sẽ tìm hiểu sâu hơn về: Kiến thức cốt lõi về Tổng quan về List trong Python. Đây là kiến thức nền tảng mà mỗi lập trình viên đều cần nắm vững khi làm việc với Python Core. Các em lưu ý phần quan trọng này nhé: hãy chú ý quan sát từng bước thực hiện trên màn hình và ghi nhớ những điểm mấu chốt.",
  "Scene_04": "Tiếp theo, chúng ta sẽ tìm hiểu sâu hơn về: Thực hành Tổng quan về List trong Python. Đây là kiến thức nền tảng mà mỗi lập trình viên đều cần nắm vững khi làm việc với Python Core. Các em lưu ý phần quan trọng này nhé: hãy chú ý quan sát từng bước thực hiện trên màn hình và ghi nhớ những điểm mấu chốt.",
  "Scene_05": "Trong thực tế phát triển phần mềm với Python Core, các em sẽ rất dễ gặp phải lỗi logic hoặc ngoại lệ khi xử lý Tổng quan về List trong Python. Hãy quan sát màn hình: nếu không kiểm tra kỹ dữ liệu đầu vào, ứng dụng sẽ báo lỗi ngay lập tức. Để khắc phục, chúng ta cần bổ sung câu lệnh kiểm tra điều kiện chặn lỗi và log thông báo rõ ràng.",
  "Scene_06": "Như vậy, chúng ta đã cùng nhau hoàn thành bài học về Tổng quan về List trong Python. Hãy nhớ rằng những kiến thức này là nền tảng cực kỳ quan trọng cho các bài học tiếp theo trong khóa Python Core. Các em hãy thực hành lại toàn bộ các bước trên máy cá nhân để củng cố kiến thức. Cảm ơn các em đã theo dõi, hẹn gặp lại trong các bài học tiếp theo!"
}
DIRECTOR_CUES = {
  "Scene_01": [],
  "Scene_02": [],
  "Scene_03": [],
  "Scene_04": [],
  "Scene_05": [],
  "Scene_06": []
}

def main():
    out_dir = os.path.join("assets", "tts")
    os.makedirs(out_dir, exist_ok=True)
    
    durations = {}
    
    if KokoroVietnamese:
        print("[TTS Pipeline] Initializing Kokoro-Vietnamese Engine (voice='hung_thinh')...")
        tts = KokoroVietnamese(device="cpu", voice="hung_thinh")
        for scene_id, text in CLEAN_TTS_SCRIPTS.items():
            wav_path = os.path.join(out_dir, f"{scene_id}.wav")
            audio, phonemes = tts.synthesize(text, speed=0.95, normalize_peak=0.95)
            sf.write(wav_path, audio, 24000)
            dur_sec = round(len(audio) / 24000.0, 2)
            durations[scene_id] = dur_sec
            print(f"  ✓ Synthesized {scene_id}: {dur_sec}s -> {wav_path}")
    else:
        print("[TTS Pipeline] Kokoro-Vietnamese engine fallback mode...")
        for scene_id, text in CLEAN_TTS_SCRIPTS.items():
            durations[scene_id] = round(max(len(text.split()) * 0.35, 15.0), 2)
            
    dur_file = os.path.join(out_dir, "durations.json")
    with open(dur_file, "w", encoding="utf-8") as f:
        json.dump(durations, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved audio durations to {dur_file}")

if __name__ == "__main__":
    main()
