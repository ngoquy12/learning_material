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
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Hôm nay chúng ta học cách định dạng chuỗi bằng f-string trong Python. Cách ghép chuỗi cũ bằng dấu cộng hoặc dùng format rất rườm rà, dễ gây lỗi ép kiểu thủ công."
  },
  {
    "id": "Scene_02",
    "text": "Để giải quyết, f-string ra đời. Chúng ta chỉ cần thêm ký tự f trước dấu nháy của chuỗi. Khi đó, mọi biến số hoặc biểu thức nằm trong cặp ngoặc nhọn sẽ tự động được định dạng và hiển thị trực quan."
  },
  {
    "id": "Scene_03",
    "text": "Ngoài ra, f-string hỗ trợ định dạng nâng cao sau dấu hai chấm. Ví dụ, dấu hai chấm chấm hai f giúp làm tròn số thập phân, hoặc ký tự bé hơn, lớn hơn kết hợp độ rộng giúp định hình căn lề cột dữ liệu."
  },
  {
    "id": "Scene_04",
    "text": "Hãy tránh ba sai lầm: quên viết chữ f, trùng dấu nháy bao ngoài và bên trong biểu thức, và thiếu ký tự nhân đôi ngoặc nhọn khi muốn in trực tiếp chúng. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
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
