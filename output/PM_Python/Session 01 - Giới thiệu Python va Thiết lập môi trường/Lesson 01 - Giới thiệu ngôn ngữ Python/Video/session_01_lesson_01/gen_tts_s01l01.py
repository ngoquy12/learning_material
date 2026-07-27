import sys
import os
import json
import soundfile as sf
from kokoro_vietnamese import KokoroVietnamese
from kokoro_vietnamese.text_norm import normalize_vietnamese_text

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
tts_dir = os.path.join(base_dir, "assets", "tts")
os.makedirs(tts_dir, exist_ok=True)

print("Initializing Kokoro-Vietnamese TTS model (Voice: hung_thinh)...")
tts = KokoroVietnamese(device="cpu", voice="hung_thinh")

scenes = [
    ("Scene_01", "Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong ngành sản xuất phần mềm hiện đại, có bao giờ bạn tự hỏi điều gì quyết định sự thành bại của một sản phẩm công nghệ? Đó chính là tốc độ bàn giao time-to-market. Các ngôn ngữ lập trình thế hệ cũ đòi hỏi hàng trăm dòng lệnh phức tạp chỉ để xử lý các tác vụ cơ bản, làm tăng nguy cơ phát sinh lỗi logic và kéo dài thời gian thử nghiệm. Nhu cầu về một ngôn ngữ có cú pháp tường minh, giúp kỹ sư tập trung hoàn toàn vào nghiệp vụ cốt lõi đã trở nên cấp bách. Và Python chính là câu trả lời hàng đầu được các tập đoàn công nghệ lớn tin dùng."),
    ("Scene_02", "Để giải quyết triệt để thách thức đó, nhà toán học Guido van Rossum tại Viện Toán Tin học CWI Hà Lan đã chính thức giới thiệu ngôn ngữ Python vào năm 1991. Tên gọi Python được lấy cảm hứng từ chương trình hài kịch Monty Python. Triết lý thiết kế cốt lõi của ngôn ngữ này được đúc kết trong tài liệu Zen of Python với các nguyên tắc nền tảng: tường minh tốt hơn ẩn ý, đơn giản tốt hơn phức tạp, và dễ đọc tốt hơn dễ viết. Đặc biệt, Python áp dụng quy chuẩn thụt lề bắt buộc để duy trì tính đồng bộ tuyệt đối khi làm việc nhóm."),
    ("Scene_03", "Nhưng đằng sau sự tối giản đó, Python làm thế nào để chạy mượt mà trên mọi hệ điều hành? Khác với các ngôn ngữ biên dịch như C hay C++ chuyển thẳng mã nguồn thành mã máy của riêng từng phần cứng, Python sử dụng cơ chế thông dịch lai. Trình biên dịch ngầm sẽ chuyển mã nguồn .py thành định dạng mã trung gian Bytecode .pyc. Kế tiếp, máy ảo Python PVM tiếp nhận Bytecode này và dịch trực tiếp sang các chỉ thị mã máy tương thích với hệ điều hành đang sử dụng."),
    ("Scene_04", "Khi phát triển phần mềm trong doanh nghiệp, nếu mỗi kỹ sư viết mã theo một phong cách riêng thì dự án sẽ rất khó bảo trì. Đó là lý do quy chuẩn PEP 8 được thiết lập. Trong một chương trình Python chuẩn, chúng ta định nghĩa hàm main và bảo vệ điểm khởi chạy bằng điều kiện if name bằng main. Mọi tên biến và tên hàm như user_name hay birth_year_input phải viết thường hoàn toàn và phân tách bằng dấu gạch dưới, gọi là quy tắc snake_case."),
    ("Scene_05", "Hãy cùng xét một tình huống thực tế: Khi xây dựng tính năng nhập năm sinh để tính tuổi cho khách hàng. Hàm input() luôn nhận dữ liệu đầu vào dưới dạng chuỗi ký tự. Nếu không thực hiện ép kiểu, phép toán sẽ bị lỗi hoặc ghép chuỗi sai lệch. Do đó, chúng ta bắt buộc phải dùng hàm int() để chuyển đổi chuỗi thành số nguyên trước khi thực hiện phép trừ. Sau khi tính toán thành công, lệnh print() sẽ xuất kết quả rõ ràng ra màn hình console."),
    ("Scene_06", "Trong quá trình mới bắt đầu lập trình Python, có ba cạm bẫy lỗi phổ biến mà bạn rất dễ mắc phải: TypeError khi thực hiện phép toán trên kiểu dữ liệu không tương thích, ValueError khi ép kiểu chuỗi chữ cái sang số, và IndentationError do thụt lề sai quy chuẩn PEP 8. Tóm lại, Python là ngôn ngữ mạnh mẽ, tối giản và vô cùng linh hoạt. Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu về Lesson 02: Cài đặt môi trường Python và phần mềm Visual Studio Code. Cảm ơn các bạn đã theo dõi, hẹn gặp lại!")
]

durations = {}
for scene_id, text in scenes:
    script_path = os.path.join(tts_dir, f"{scene_id}_script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Pre-TTS Phonetic Analysis & Tech Dictionary Normalization
    normalized_text = normalize_vietnamese_text(text)
    print(f"\n[{scene_id}] Raw: {text[:65]}...")
    print(f"[{scene_id}] Norm: {normalized_text[:65]}...")

    output_path = os.path.join(tts_dir, f"{scene_id}.mp3")
    audio_samples, phonemes = tts.synthesize(text=normalized_text, speed=0.95)
    sf.write(output_path, audio_samples, 24000)

    duration = round(len(audio_samples) / 24000, 2)
    durations[scene_id] = duration
    print(f"Synthesized {scene_id}.mp3 -> Duration: {duration}s")

json_path = os.path.join(tts_dir, "durations.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(durations, f, indent=2, ensure_ascii=False)

print("\nAll 6 pedagogical TTS audio tracks generated successfully!")
print(f"Durations: {durations}")
