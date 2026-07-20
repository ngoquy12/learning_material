import os
import json
import subprocess
import sys
import io
import urllib.request
from pathlib import Path

# Set console encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', write_through=True)

# ElevenLabs configuration
ELEVENLABS_API_KEY = "d5663f484bf69915d3dc6cc35b22b5856365a9ba68f64b2f6e1067e80cc70c52"
ELEVENLABS_VOICE_ID = "6adFm46eyy74snVn6YrT"
BASE_URL = "https://api.elevenlabs.io"

scenes = [
  {
    "id": "Scene_01",
    "text": "Chào mừng tất cả các em đã quay trở lại với hệ thống học tập trực tuyến của Rikkei Education. Hôm nay, chúng ta sẽ chính thức bước vào hành trình khám phá và làm chủ Python - một trong những ngôn ngữ lập trình phổ biến, mạnh mẽ và được yêu thích nhất trên toàn thế giới hiện nay. Khi tiếp cận với Python, điều quan trọng nhất không chỉ là học cú pháp, mà là thấu hiểu triết lý thiết kế đằng sau nó. Triết lý thiết kế cốt lõi của ngôn ngữ này đề cao tính rõ ràng, sự ngắn gọn và khả năng đọc hiểu tối đa của con người. Điều này được thể hiện rõ nét qua các nguyên tắc dẫn đường trong tài liệu Zen of Python. Những nguyên lý nổi tiếng như đẹp đẽ tốt hơn xấu xí, tường minh tốt hơn ngầm định, và đơn giản tốt hơn phức tạp đã giúp Python trở thành ngôn ngữ được lựa chọn hàng đầu cho việc giảng dạy lập trình, phân tích dữ liệu, tự động hóa và phát triển các mô hình trí tuệ nhân tạo chuyên sâu. Triết lý này không chỉ là những dòng chữ lý thuyết, mà nó thực sự thấm nhuần vào từng dòng mã Python mà chúng ta viết mỗi ngày, tạo nên sự đồng bộ và nhất quán giữa tất cả các lập trình viên trên toàn thế giới."
  },
  {
    "id": "Scene_02",
    "text": "Để hiểu rõ cơ chế vận hành bên dưới của Python, các em cần phân biệt chính xác hai mô hình thực thi ngôn ngữ phổ biến: ngôn ngữ biên dịch và ngôn ngữ thông dịch. Khác biệt với các ngôn ngữ biên dịch như C++ hay Java - nơi toàn bộ mã nguồn của chương trình phải được chuyển đổi hoàn toàn thành mã máy trước khi chạy, Python là một ngôn ngữ thông dịch thuần túy. Khi chúng ta thực hiện chạy một script Python trực tiếp từ Terminal, trình thông dịch của Python sẽ quét mã nguồn, chuyển đổi nó sang định dạng mã bytecode trung gian để tối ưu hóa hiệu năng, và sau đó máy ảo Python hay còn gọi là PVM sẽ thực thi từng dòng bytecode này tại thời điểm runtime. Mặc dù tốc độ thực thi có thể chậm hơn một chút so với ngôn ngữ biên dịch, cơ chế thông dịch này mang lại sự linh hoạt đáng kinh ngạc, giúp lập trình viên chạy thử và gỡ lỗi nhanh chóng, đồng thời đảm bảo tính đa nền tảng tuyệt đối của mã nguồn trên mọi hệ điều hành từ Windows, Linux cho đến macOS. Máy ảo Python PVM hoạt động như một lớp trừu tượng trung gian, giúp che giấu đi sự phức tạp của phần cứng bên dưới, cho phép mã nguồn viết một lần và chạy được ở bất kỳ đâu mà không cần chỉnh sửa."
  },
  {
    "id": "Scene_03",
    "text": "Một đặc tính vô cùng quan trọng mang lại sự linh hoạt vượt trội cho Python chính là cơ chế định kiểu động, hay còn gọi là Dynamic Typing. Trong các ngôn ngữ lập trình định kiểu tĩnh truyền thống như Java hay C++, các em bắt buộc phải khai báo rõ ràng kiểu dữ liệu của biến số trước khi chương trình được biên dịch và chạy. Tuy nhiên, đối với Python, kiểu dữ liệu của biến số sẽ được trình thông dịch tự động phát hiện và quyết định tại thời điểm chạy chương trình dựa trên giá trị được gán cho biến số đó. Các em có thể dễ dàng gán một biến x bằng số nguyên mười, và ngay dòng tiếp theo có thể gán lại biến x đó bằng một chuỗi ký tự dài mà không hề gặp bất kỳ lỗi cú pháp nào. Tuy nhiên, sự linh hoạt này cũng đòi hỏi các em phải hết sức cẩn trọng, tránh việc thay đổi kiểu dữ liệu tùy tiện trong cùng một phạm vi để ngăn ngừa các lỗi TypeError phát sinh khi tính toán thực tế trong dự án lớn. Chính vì kiểu dữ liệu có thể thay đổi linh hoạt trong suốt vòng đời của chương trình, các em cần thiết lập thói quen đặt tên biến rõ ràng, có ý nghĩa và ghi chú đầy đủ để tránh gây nhầm lẫn cho bản thân và đồng đội."
  },
  {
    "id": "Scene_04",
    "text": "Tiếp theo, chúng ta sẽ cùng tìm hiểu về quy tắc thụt lề bắt buộc - một đặc trưng cú pháp vô cùng độc đáo và cũng là kỷ luật nghiêm khắc nhất trong Python. Nếu như hầu hết các ngôn ngữ họ C sử dụng cặp dấu ngoặc nhọn để phân chia và nhóm các khối lệnh con, thì Python hoàn toàn sử dụng khoảng trắng thụt lề đầu dòng để xác định cấu trúc logic của chương trình. Theo chuẩn khuyến nghị của cộng đồng lập trình viên Python và quy chuẩn PEP 8, chúng ta luôn sử dụng bốn khoảng trắng cho mỗi cấp độ thụt lề. Bất kỳ sự thiếu nhất quán nào trong việc căn lề, hoặc việc sử dụng lẫn lộn giữa phím Tab và dấu cách Space, sẽ lập tức kích hoạt lỗi IndentationError và chương trình sẽ dừng hoạt động ngay tại dòng đó. Kỷ luật cú pháp nghiêm ngặt này buộc lập trình viên phải viết code cực kỳ sạch sẽ, rõ ràng, dễ bảo trì và có cấu trúc trực quan cực kỳ đồng bộ giữa tất cả các thành viên trong dự án. Hãy luôn thiết lập trình biên soạn mã VS Code của các em tự động chuyển đổi phím Tab thành bốn dấu cách để đảm bảo tính nhất quán tuyệt đối, ngăn ngừa triệt để các lỗi thụt lề khó chịu có thể xảy ra."
  },
  {
    "id": "Scene_05",
    "text": "Cuối cùng, điều làm nên sức mạnh vĩ đại và vị thế dẫn đầu của Python trong kỷ nguyên công nghệ hiện nay chính là hệ sinh thái thư viện chuẩn vô cùng đồ sộ kết hợp với các ứng dụng thực chiến đa dạng. Từ việc xử lý các phép toán khoa học phức tạp bằng module math, tương tác với hệ điều hành thông qua các module hệ thống os, cho đến lập trình tự động hóa hay phân tích dữ liệu chuyên sâu, Python đều cung cấp sẵn các công cụ mạnh mẽ để rút ngắn tối đa thời gian phát triển phần mềm. Tổng kết lại bài học hôm nay, các em cần ghi nhớ bốn kiến thức trọng tâm bao gồm: triết lý thiết kế Zen tối giản, cơ chế thông dịch đa nền tảng, định kiểu động linh hoạt, và quy tắc thụt lề bắt buộc. Cảm ơn tất cả các em đã chú ý theo dõi bài học ngày hôm nay của Rikkei Education, chúc các em học tốt và hẹn gặp lại các em trong các bài giảng tiếp theo! Bằng cách tận dụng tối đa sức mạnh của hệ sinh thái phong phú này, các em có thể dễ dàng hiện thực hóa các ý tưởng phần mềm đột phá, từ các ứng dụng web thông minh đến các mô hình học máy phức tạp nhất."
  }
]

tts_dir = Path("assets/tts")
tts_dir.mkdir(parents=True, exist_ok=True)

all_durations = {}
ffprobe_path = r"C:\Users\PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffprobe.exe"

for scene in scenes:
    scene_id = scene["id"]
    text = scene["text"]
    if not text:
        continue
        
    mp3_path = tts_dir / f"{scene_id}.mp3"
    print(f"Generating TTS for {scene_id} using ElevenLabs...")
    
    url = f"{BASE_URL}/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.65,
            "use_speaker_boost": True
        }
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            if mp3_path.exists():
                mp3_path.unlink()
            with open(mp3_path, "wb") as f:
                f.write(audio_data)
        print(f"✓ Successfully generated ElevenLabs audio for {scene_id}")
    except Exception as e:
        print(f"❌ ElevenLabs failed for {scene_id}: {e}. Falling back to offline silence...")
        # Fallback to silence if ElevenLabs API key has errors
        if not mp3_path.exists():
            fallback_dur = max(5.0, len(text.split()) / 2.2)
            cmd = f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t {fallback_dur} -q:a 2 "{mp3_path}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    if mp3_path.exists():
        try:
            cmd = f'"{ffprobe_path}" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{mp3_path}"'
            probe = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            duration = float(probe)
            all_durations[scene_id] = round(duration, 2) + 0.5
        except Exception as e:
            all_durations[scene_id] = max(5.0, len(text.split()) / 2.2)
    else:
        all_durations[scene_id] = max(5.0, len(text.split()) / 2.2)

with open(tts_dir / "durations.json", "w", encoding="utf-8") as f:
    json.dump(all_durations, f, indent=2, ensure_ascii=False)
print("TTS Generation Complete!")
