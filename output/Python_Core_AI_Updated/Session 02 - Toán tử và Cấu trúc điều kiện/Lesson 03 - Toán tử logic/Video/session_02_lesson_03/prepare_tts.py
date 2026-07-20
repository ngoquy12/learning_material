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
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, chúng ta thường cần kiểm tra nhiều điều kiện cùng lúc để đưa ra quyết định, ví dụ như kiểm tra độ tuổi và sức khỏe. Làm thế nào để viết code ngắn gọn, tối ưu thay vì lồng nhiều câu lệnh phức tạp? Hôm nay chúng ta sẽ tìm hiểu về các toán tử logic trong Python."
  },
  {
    "id": "Scene_02",
    "text": "Python cung cấp ba toán tử logic chính gồm and, or và not. Để hiểu rõ cách chúng hoạt động, chúng ta sử dụng bảng chân trị. Hãy xem cách viết code tự động xuất bảng chân trị cho biểu thức A and not B bằng cách lặp qua các giá trị True và False để kiểm tra kết quả."
  },
  {
    "id": "Scene_03",
    "text": "Khi kết hợp nhiều toán tử, Python đánh giá theo thứ tự ưu tiên mặc định. Đầu tiên là các phép so sánh toán học, tiếp theo là toán tử not, sau đó đến and, và cuối cùng là or. Hiểu rõ thứ tự này giúp các em tránh được lỗi logic nghiêm trọng khi viết biểu thức phức tạp."
  },
  {
    "id": "Scene_04",
    "text": "Hãy lưu ý ba lỗi phổ biến: sai thứ tự ưu tiên do thiếu ngoặc đơn, ngăn mạch ngoài ý muốn, và nhầm lẫn các giá trị Falsy như số không hoặc chuỗi rỗng. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
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
