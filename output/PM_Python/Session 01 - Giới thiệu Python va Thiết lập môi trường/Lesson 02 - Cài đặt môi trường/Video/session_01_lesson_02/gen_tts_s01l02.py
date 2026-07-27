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

print("Initializing Kokoro-Vietnamese TTS model for 5-Minute Masterclass Lesson 02...")
tts = KokoroVietnamese(device="cpu", voice="hung_thinh")

narrations = [
    ("Scene_01", "Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education. Hãy cùng tưởng tượng một tình huống thực tế trong doanh nghiệp: Đội ngũ của bạn đang phát triển hai dự án cùng lúc. Dự án A sử dụng thư viện Django phiên bản 3.2 cũ, trong khi Dự án B bắt buộc dùng phiên bản Django 4.2 mới nhất. Nếu cài đặt trực tiếp mọi thứ lên phân vùng hệ thống toàn cục, xung đột phiên bản sẽ xuất hiện tức thì, làm ngưng trệ toàn bộ quy trình phát triển. Hiện tượng này được gọi là địa ngục phụ thuộc hay dependency hell. Liệu có giải pháp nào giúp cô lập từng dự án hoàn toàn?"),
    
    ("Scene_02", "Đó chính là lý do công nghệ Môi trường ảo Virtual Environment ra đời. Khác với cơ chế quản lý gói toàn cục của hệ điều hành, môi trường ảo venv tạo ra một không gian làm việc cô lập hoàn toàn cho từng dự án riêng biệt. Bên trong thư mục venv sẽ chứa một bản sao gọn nhẹ của trình thông dịch Python cùng thư mục site-packages độc lập. Nhờ đó, việc cài đặt hay gỡ bỏ thư viện ở dự án này sẽ tuyệt đối không gây ảnh hưởng đến bất kỳ ứng dụng nào khác trên máy tính của bạn."),
    
    ("Scene_03", "Để bắt đầu thiết lập, bước đầu tiên là cài đặt chuẩn hóa bộ diễn giải Python. Khi tải bản cài đặt chính thức từ website python.org, một tùy chọn cực kỳ quan trọng bắt buộc bạn phải đánh dấu chọn là Add Python to PATH. Biến môi trường PATH đóng vai trò như một bảng chỉ đường giúp hệ điều hành đăng ký vị trí chứa tệp thực thi python.exe. Nhờ có cấu hình này, bạn có thể gọi và kích hoạt lệnh python trực tiếp từ bất kỳ cửa sổ dòng lệnh terminal nào."),
    
    ("Scene_04", "Sau khi đã cài đặt Python, bước tiếp theo là cấu hình môi trường lập trình chuyên nghiệp Visual Studio Code. Để làm việc hiệu quả, bạn cần truy cập cửa sổ Extensions Marketplace và cài đặt tiện ích mở rộng Python Extension chính thức phát hành bởi Microsoft. Tiện ích này cung cấp tính năng phân tích cú pháp thông minh IntelliSense, hỗ trợ rà soát lỗi tự động và giúp editor nhận diện chính xác các trình thông dịch trong môi trường ảo."),
    
    ("Scene_05", "Bây giờ, chúng ta sẽ bắt tay vào thực hành khởi tạo môi trường ảo trực tiếp từ cửa sổ dòng lệnh. Hãy mở terminal tại thư mục gốc dự án của bạn và thực thi lệnh python -m venv app_env. Ở đây, cờ -m chỉ định Python chạy module venv có sẵn trong thư viện chuẩn, và app_env là tên thư mục sẽ chứa toàn bộ môi trường ảo. Sau khi lệnh chạy xong, một thư mục mới mang tên app_env sẽ tự động xuất hiện trong dự án."),
    
    ("Scene_06", "Tuy nhiên, tạo xong là chưa đủ, bạn bắt buộc phải kích hoạt môi trường ảo trước khi sử dụng. Trên hệ điều hành Windows PowerShell, bạn chạy file kịch bản bằng lệnh .\\app_env\\Scripts\\Activate.ps1. Nếu gặp lỗi Execution Policy về quyền thực thi, hãy mở PowerShell quyền Admin và chạy Set-ExecutionPolicy RemoteSigned. Còn trên hệ điều hành macOS hoặc Linux, bạn chỉ cần gõ lệnh source app_env/bin/activate. Tên môi trường app_env sẽ xuất hiện ở đầu dòng lệnh báo hiệu kích hoạt thành công."),
    
    ("Scene_07", "Để đảm bảo ứng dụng của bạn thực sự đang chạy trong môi trường ảo vừa tạo, hãy cùng viết một đoạn mã Python kiểm chứng. Chúng ta import thư viện hệ thống sys, sau đó in ra hai thuộc tính sys.executable và sys.prefix. Nếu đường dẫn trỏ thẳng vào thư mục app_env cục bộ thay vì thư mục cài đặt gốc của hệ điều hành, điều đó chứng minh môi trường ảo của bạn đã hoạt động chính xác 100%."),
    
    ("Scene_08", "Trong quá trình thiết lập môi trường, hãy luôn lưu ý 3 lỗi phổ biến: Lỗi ModuleNotFoundError do quên kích hoạt venv trước khi pip install, lỗi FileNotFoundError do mở terminal sai vị trí thư mục, và lỗi PermissionError do thiếu đặc quyền quản trị. Tóm lại, việc làm chủ môi trường ảo venv và VS Code là nền tảng cốt lõi của mọi lập trình viên Python. Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu Bài 3: Khai báo Biến và Các Kiểu Dữ Liệu Cơ Bản Trong Python. Cảm ơn các bạn đã theo dõi, hẹn gặp lại!")
]

durations = {}

for scene_id, raw_text in narrations:
    norm_text = normalize_vietnamese_text(raw_text)
    print(f"\n[{scene_id}] Raw ({len(raw_text)} chars): {raw_text[:70]}...")
    print(f"[{scene_id}] Norm: {norm_text[:70]}...")
    
    script_path = os.path.join(tts_dir, f"{scene_id}_script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(norm_text)
        
    out_file = os.path.join(tts_dir, f"{scene_id}.mp3")
    
    audio_samples, phonemes = tts.synthesize(text=norm_text, speed=0.95)
    sf.write(out_file, audio_samples, 24000)
    
    dur = round(len(audio_samples) / 24000.0, 2)
    durations[scene_id] = dur
    print(f"Synthesized {scene_id}.mp3 -> Duration: {dur}s")

durations_path = os.path.join(tts_dir, "durations.json")
with open(durations_path, "w", encoding="utf-8") as f:
    json.dump(durations, f, indent=2, ensure_ascii=False)

total_dur = sum(durations.values())
print(f"\n=== TTS MASTERCLASS GENERATION COMPLETED SUCCESSFULLY ===")
print(f"Total TTS Audio Duration: {total_dur:.2f}s (~{total_dur/60:.2f} mins)")
print(json.dumps(durations, indent=2))
