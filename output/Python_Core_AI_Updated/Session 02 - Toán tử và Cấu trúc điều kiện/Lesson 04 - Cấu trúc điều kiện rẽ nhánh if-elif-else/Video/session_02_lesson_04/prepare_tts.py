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
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, đôi khi chúng ta cần chương trình đưa ra quyết định thông minh dựa trên dữ liệu thực tế, thay vì chỉ thực thi các dòng lệnh tuần tự từ trên xuống dưới. Đó là lúc cấu trúc rẽ nhánh xuất hiện."
  },
  {
    "id": "Scene_02",
    "text": "Chúng ta sử dụng các từ khóa if, elif và else kết hợp với toán tử so sánh để phân loại điều kiện. Hãy xem ví dụ phân loại chỉ số BMI sau đây. Nếu điều kiện đầu tiên sai, chương trình sẽ tiếp tục kiểm tra các điều kiện tiếp theo trước khi thực thi nhánh else."
  },
  {
    "id": "Scene_03",
    "text": "Khi sử dụng cấu trúc rẽ nhánh, các em cần lưu ý ba lỗi phổ biến. Đó là thiếu dấu hai chấm ở cuối điều kiện gây lỗi cú pháp, thụt lề không đồng nhất dẫn đến lỗi logic, và sắp xếp sai thứ tự điều kiện khiến mã nguồn bị che khuất và không thể thực thi."
  },
  {
    "id": "Scene_04",
    "text": "Tóm lại, cấu trúc rẽ nhánh giúp điều khiển dòng chạy ứng dụng một cách linh hoạt dựa trên Boolean. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
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
