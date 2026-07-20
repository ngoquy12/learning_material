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
    "text": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong lập trình, tính toán là yêu cầu cốt lõi. Ngoài các phép tính cơ bản, làm sao để chia lấy dư phân loại chẵn lẻ, chia lấy nguyên để phân trang, hay tính lũy thừa hiệu suất cao? Hãy cùng tìm hiểu ngay sau đây."
  },
  {
    "id": "Scene_02",
    "text": "Python cung cấp các toán tử số học cơ bản gồm cộng, trừ, nhân, chia. Đặc biệt, ta có toán tử phần trăm để chia lấy dư, hai dấu gạch chéo để chia lấy phần nguyên, và hai dấu sao để thực hiện phép tính lũy thừa một cách nhanh chóng và tối ưu."
  },
  {
    "id": "Scene_03",
    "text": "Hãy quan sát ví dụ sau. Khi khai báo hai biến a và b, ta dễ dàng tính toán các giá trị tổng, thương thực, thương nguyên, số dư và lũy thừa. Lưu ý, khi nhận dữ liệu từ bàn phím qua hàm input, ta bắt buộc phải ép sang kiểu số nguyên int hoặc số thực float trước khi tính."
  },
  {
    "id": "Scene_04",
    "text": "Khi làm việc với toán tử, hãy tránh ba sai lầm phổ biến: Chia cho số không gây lỗi ZeroDivisionError, quên ép kiểu gây TypeError, và tính sai thứ tự ưu tiên do thiếu dấu ngoặc đơn. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
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
