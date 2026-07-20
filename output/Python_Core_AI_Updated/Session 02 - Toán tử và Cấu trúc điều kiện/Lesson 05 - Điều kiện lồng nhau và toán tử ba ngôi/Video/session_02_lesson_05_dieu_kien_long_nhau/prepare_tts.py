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
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay, chúng ta sẽ tìm hiểu cách tối ưu hóa các cấu trúc rẽ nhánh phức tạp. Khi viết quá nhiều if-else lồng nhau, mã nguồn sẽ bị đẩy sâu về bên phải, tạo ra cấu trúc Arrow Anti-pattern cực kỳ khó đọc."
  },
  {
    "id": "Scene_02",
    "text": "Để giải quyết vấn đề này, giải pháp đầu tiên là áp dụng Guard Clauses. Chúng ta sẽ kiểm tra và loại bỏ các điều kiện lỗi ngay ở đầu hàm bằng lệnh return. Kỹ thuật này giúp giải phóng các khối block lồng nhau, đưa mã nguồn về dạng phẳng, dễ dàng theo dõi."
  },
  {
    "id": "Scene_03",
    "text": "Tiếp theo, với các quyết định trả về kết quả đơn giản ở cuối luồng, ta sử dụng toán tử ba ngôi. Hãy xem ví dụ trực quan trên màn hình. Hàm check payment status được rút gọn tối đa bằng cách kết hợp cả Guard Clauses và toán tử ba ngôi một cách tinh tế."
  },
  {
    "id": "Scene_04",
    "text": "Khi tối ưu rẽ nhánh, hãy đặc biệt tránh ba lỗi: lồng quá ba tầng if-else, lạm dụng toán tử ba ngôi lồng nhau, và quên return trong Guard Clauses. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
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
