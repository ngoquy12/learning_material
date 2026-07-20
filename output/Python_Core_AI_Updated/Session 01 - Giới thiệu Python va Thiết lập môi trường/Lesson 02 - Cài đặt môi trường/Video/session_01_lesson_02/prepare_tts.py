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
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong bài học hôm nay, chúng ta sẽ bắt đầu thiết lập môi trường lập trình Python. Hãy nhớ luôn tích chọn Add Python to PATH khi cài đặt để tránh lỗi hệ điều hành không nhận diện lệnh."
  },
  {
    "id": "Scene_02",
    "text": "Tiếp theo, chúng ta cài đặt VS Code và cài thêm Extension Python. Để quản lý các thư viện dự án độc lập, tránh xung đột phiên bản, ta dùng lệnh python -m venv venv_demo để tạo môi trường ảo chuyên biệt cho dự án."
  },
  {
    "id": "Scene_03",
    "text": "Kích hoạt môi trường bằng lệnh source activate trên Linux/macOS hoặc Scripts/activate trên Windows. Hãy chạy đoạn mã Python sau để xác minh hệ thống đang thực thi trong môi trường ảo hay global."
  },
  {
    "id": "Scene_04",
    "text": "Tóm lại, hãy tránh ba lỗi: quên chọn PATH, cài thiếu venv, hoặc đặt tên thư mục chứa dấu Tiếng Việt. Thiết lập môi trường sạch sẽ giúp các em phát triển dự án trơn tru. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
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
