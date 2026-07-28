"""
gen_tts.py — Kokoro-Vietnamese Audio Generator & Director Cue Processor
"""
import os
import sys
import json
import soundfile as sf

# Thêm đường dẫn Kokoro-Vietnamese
sys.path.insert(0, os.path.abspath("../../Kokoro-Vietnamese"))

try:
    from kokoro_vietnamese import KokoroVietnamese
except ImportError:
    KokoroVietnamese = None

CLEAN_TTS_SCRIPTS = {
  "Scene_01": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong nội dung bài học này, chúng ta sẽ cùng nhau tìm hiểu về Khái niệm List và cách khởi tạo. Trong giải pháp phần mềm thực tế, việc quản lý một tập hợp danh sách các phần tử có cùng hoặc khác kiểu dữ liệu là vô cùng quan trọng. Python cung cấp cấu trúc dữ liệu List - hay còn gọi là mảng động - để giải quyết bài toán quản lý danh bạ, giỏ hàng, hay danh sách bài viết một cách linh hoạt nhất.",
  "Scene_02": "Thế nhưng trong thực tế, nếu không dùng list, chúng ta sẽ quản lý dữ liệu như thế nào? Giả lập một bài toán quản trị hệ thống: Nếu các em khai báo hàng chục luồng dữ liệu bằng các biến đơn lẻ như u-dơ một, u-dơ hai, mã nguồn sẽ trở nên cực kỳ cồng kềnh, khó bảo trì và bất khả thi khi số lượng phần tử tăng lên hàng nghìn. List xuất hiện như một cứu cánh, tích hợp toàn bộ phần tử vào một biến duy nhất để quản lý tập trung.",
  "Scene_03": "Về mặt bản chất hệ thống bên dưới, List trong Python là một mảng động lưu trữ các tham chiếu đối tượng. Điều này có nghĩa là bộ nhớ không cần cấp phát các ô nhớ liên tiếp cho giá trị thực, mà chỉ cần lưu địa chỉ trỏ tới các đối tượng đó. Nhờ vậy, List có thể chứa đa kiểu dữ liệu từ số nguyên, chuỗi cho đến cả list khác, đồng thời tự động tăng kích thước khi đầy.",
  "Scene_04": "Bây giờ chúng ta cùng chuyển sang phần tiếp theo là các cú pháp khởi tạo. Phương pháp phổ biến nhất là sử dụng cặp ngoặc vuông. Chúng ta khai báo biến bằng tên và gán giá trị nằm trong ngoặc vuông, phân tách bởi dấu phẩy. Ví dụ như danh sách rỗng, danh sách các số nguyên, hoặc danh sách hỗn hợp chứa cả chuỗi và kiểu logic. Đây là phương pháp tối ưu hiệu năng nhất khi khởi tạo trực tiếp.",
  "Scene_05": "Một cách khởi tạo khác rất mạnh mẽ khi các em cần chuyển đổi các cấu trúc dữ liệu như range, tuple hay string sang dạng danh sách đó là sử dụng hàm dựng list mở ngoặc đóng ngoặc. Ví dụ, gọi hàm list mở ngoặc range từ một đến sáu đóng ngoặc sẽ lập tức tạo ra một danh sách số nguyên từ một đến năm. Cú pháp này vô cùng hữu ích trong các giải thuật xử lý tập hợp dữ liệu động.",
  "Scene_06": "Các em lưu ý phần quan trọng này nhé: Một sai lầm kinh điển của lập trình viên Python mới là đặt tên biến trùng với từ khóa hệ thống list. Khi các em gán biến tên là list bằng giá trị nào đó, hàm dựng list mở ngoặc đóng ngoặc gốc sẽ bị ghi đè, dẫn đến lỗi tai hại về sau khi không thể khởi tạo list khác. Hãy luôn sử dụng tên biến mang ý nghĩa đặc thù như danh sách sản phẩm hay danh sách người dùng.",
  "Scene_07": "Tổng kết lại, chúng ta đã nắm vững khái niệm mảng động vô cùng linh hoạt của List trong Python cùng hai phương pháp khởi tạo chính thông qua ngoặc vuông và constructor list. Trong bài học tiếp theo, chúng ta sẽ đi sâu vào kỹ thuật truy xuất và cắt lát các phần tử của danh sách này. Cảm ơn các em đã theo dõi, hẹn gặp lại trong các bài học tiếp theo!"
}
DIRECTOR_CUES = {
  "Scene_01": [],
  "Scene_02": [],
  "Scene_03": [],
  "Scene_04": [],
  "Scene_05": [],
  "Scene_06": [],
  "Scene_07": []
}

def main():
    out_dir = os.path.join("assets", "tts")
    os.makedirs(out_dir, exist_ok=True)
    
    durations = {}
    
    if KokoroVietnamese:
        print("[TTS Pipeline] Initializing Kokoro-Vietnamese Engine (voice='hung_thinh')...")
        tts = KokoroVietnamese(device="cpu", voice="hung_thinh")
        for scene_id, text in CLEAN_TTS_SCRIPTS.items():
            wav_path = os.path.join(out_dir, f"{scene_id}.wav")
            audio, phonemes = tts.synthesize(text, speed=0.95, normalize_peak=0.95)
            sf.write(wav_path, audio, 24000)
            dur_sec = round(len(audio) / 24000.0, 2)
            durations[scene_id] = dur_sec
            print(f"  [OK] Synthesized {scene_id}: {dur_sec}s -> {wav_path}")
    else:
        print("[TTS Pipeline] Kokoro-Vietnamese engine fallback mode...")
        for scene_id, text in CLEAN_TTS_SCRIPTS.items():
            durations[scene_id] = round(max(len(text.split()) * 0.35, 15.0), 2)
            
    dur_file = os.path.join(out_dir, "durations.json")
    with open(dur_file, "w", encoding="utf-8") as f:
        json.dump(durations, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved audio durations to {dur_file}")

if __name__ == "__main__":
    main()
