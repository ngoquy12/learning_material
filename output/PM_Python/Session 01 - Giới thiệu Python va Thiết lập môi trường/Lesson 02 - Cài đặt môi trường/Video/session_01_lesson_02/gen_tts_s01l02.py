import sys
import os
import json
import soundfile as sf

# UTF-8 stdout configuration
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add Kokoro-Vietnamese path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../.."))
sys.path.insert(0, os.path.join(root_dir, "Kokoro-Vietnamese/src"))

from kokoro_vietnamese import KokoroVietnamese
from kokoro_vietnamese.text_norm import normalize_vietnamese_text

base_dir = os.path.dirname(os.path.abspath(__file__))
tts_dir = os.path.join(base_dir, "assets", "tts")
os.makedirs(tts_dir, exist_ok=True)

print("Initializing Kokoro-Vietnamese TTS model with Smart Automated G2P...")
tts = KokoroVietnamese(device="cpu", voice="hung_thinh")

narrations = [
    ("Scene_01", "Chào mừng các bạn đã quay trở lại với Bài 2: Cài đặt môi trường Python và Visual Studio Code. Trong phát triển phần mềm chuyên nghiệp, việc chạy đồng thời nhiều dự án có phiên bản thư viện khác nhau trên cùng một thiết bị là thử thách lớn. Nếu cài đặt trực tiếp mọi thứ lên môi trường toàn cục, xung đột phiên bản sẽ xuất hiện tức thì, gây ra hiện tượng địa ngục phụ thuộc hay còn gọi là dependency hell. Liệu có giải pháp nào giúp cô lập dự án hoàn toàn?"),
    ("Scene_02", "Để giải quyết vấn đề này, bước đầu tiên là cài đặt chuẩn hóa. Khi tải bản cài đặt Python chính thức từ website python.org, tùy chọn Add Python to PATH là bắt buộc. Điều này giúp đăng ký đường dẫn chứa tệp thực thi vào danh sách tìm kiếm của hệ điều hành, cho phép bạn kích hoạt lệnh python trực tiếp từ bất kỳ cửa sổ dòng lệnh terminal nào."),
    ("Scene_03", "Sau khi cài đặt Python, ta cần cấu hình môi trường lập trình Visual Studio Code. Làm việc với Python hiệu quả đòi hỏi cài đặt tiện ích mở rộng Python Extension chính thức từ Microsoft. Tiện ích này đóng vai trò phân tích cú pháp, tự động gợi ý code thông minh và giúp VS Code kết nối chuẩn xác với các môi trường ảo cục bộ."),
    ("Scene_04", "Kế tiếp, ta tạo lập và kích hoạt môi trường ảo venv. Môi trường ảo thực chất là một thư mục cô lập hoàn toàn chứa bản sao gọn nhẹ của trình thông dịch Python. Tại cửa sổ terminal của dự án, hãy chạy lệnh python -m venv app_env. Sau đó, trên Windows PowerShell ta kích hoạt bằng lệnh scripts/activate, hoặc dùng source bin/activate trên macOS."),
    ("Scene_05", "Cuối cùng, hãy lưu ý 3 lỗi phổ biến: ModuleNotFoundError phát sinh khi quên kích hoạt môi trường ảo trước khi pip install, FileNotFoundError do terminal mở sai vị trí thư mục, và PermissionError khi thiếu đặc quyền quản trị. Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu Bài 3: Khai báo Biến và Kiểu dữ liệu cơ bản trong Python. Cảm ơn các bạn đã theo dõi, hẹn gặp lại!")
]

durations = {}

for scene_id, raw_text in narrations:
    norm_text = normalize_vietnamese_text(raw_text)
    print(f"\n[{scene_id}] Raw: {raw_text[:65]}...")
    print(f"[{scene_id}] Norm: {norm_text[:65]}...")
    
    # Save script text
    script_path = os.path.join(tts_dir, f"{scene_id}_script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(norm_text)
        
    out_file = os.path.join(tts_dir, f"{scene_id}.mp3")
    
    # Generate audio using KokoroVietnamese
    audio_samples, phonemes = tts.synthesize(text=norm_text, speed=0.95)
    sf.write(out_file, audio_samples, 24000)
    
    dur = round(len(audio_samples) / 24000.0, 2)
    durations[scene_id] = dur
    print(f"Synthesized {scene_id}.mp3 -> Duration: {dur}s")

durations_path = os.path.join(tts_dir, "durations.json")
with open(durations_path, "w", encoding="utf-8") as f:
    json.dump(durations, f, indent=2, ensure_ascii=False)

print("\n=== TTS GENERATION COMPLETED SUCCESSFULLY ===")
print(json.dumps(durations, indent=2))
