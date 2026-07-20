import os
import json
import subprocess
import sys
import io
from pathlib import Path
from gtts import gTTS

# Set console encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', write_through=True)

scenes = [
  {
    "id": "Scene_01",
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ tìm hiểu về cấu trúc match-case nâng cao từ Python 3.10. Trước đây, khi kiểm tra điều kiện phức tạp, các em thường dùng chuỗi if-elif-else dài dòng, cồng kềnh và dễ gây ra lỗi logic. Cấu trúc match-case ra đời để giúp giải quyết triệt để vấn đề này."
  },
  {
    "id": "Scene_02",
    "text": "Hãy cùng xem ví dụ cụ thể này. Bằng cách sử dụng cấu trúc match-case mới, ta có thể so khớp trực tiếp status code một cách ngắn gọn. Ở đây, các case cụ thể như hai trăm, bốn trăm lẻ bốn được liệt kê rõ ràng, giúp mã nguồn tối giản hơn. Ký tự gạch dưới đại diện cho mọi trường hợp còn lại."
  },
  {
    "id": "Scene_03",
    "text": "Trước khi kết thúc, các em cần lưu ý ba điểm quan trọng: luôn đặt wildcard gạch dưới ở cuối cùng, tránh nhầm lẫn gán biến, và chỉ sử dụng từ phiên bản Python 3.10 trở lên để tránh lỗi phiên bản. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
  }
]

tts_dir = Path("assets/tts")
tts_dir.mkdir(parents=True, exist_ok=True)

all_durations = {}

for scene in scenes:
    scene_id = scene["id"]
    text = scene["text"]
    if not text:
        continue
        
    mp3_path = tts_dir / f"{scene_id}.mp3"
    print(f"Generating TTS for {scene_id} using gTTS...")
    try:
        tts = gTTS(text=text, lang="vi")
        if mp3_path.exists():
            mp3_path.unlink()
        tts.save(str(mp3_path))
    except Exception as e:
        print(f"Failed to generate TTS for {scene_id}: {e}.")
        if not mp3_path.exists():
            print("Generating fallback silent audio...")
            try:
                fallback_dur = max(5.0, len(text.split()) / 2.5)
                cmd = f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t {fallback_dur} -q:a 2 "{mp3_path}"'
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as fe:
                print(f"Failed to generate fallback silent audio: {fe}")
                
    if mp3_path.exists():
        try:
            cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{mp3_path}"'
            probe = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            duration = float(probe)
            all_durations[scene_id] = round(duration, 2) + 0.5
        except Exception as e:
            all_durations[scene_id] = max(5.0, len(text.split()) / 2.5)
    else:
        all_durations[scene_id] = max(5.0, len(text.split()) / 2.5)

with open(tts_dir / "durations.json", "w", encoding="utf-8") as f:
    json.dump(all_durations, f, indent=2, ensure_ascii=False)
print("TTS Generation Complete!")
