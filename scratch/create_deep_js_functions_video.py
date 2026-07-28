"""
scratch/create_deep_js_functions_video.py

Tạo dự án video bài học CHUYÊN SÂU 9 Scenes:
"Cú pháp khai báo và sử dụng hàm trong JavaScript"

Tuân thủ 100% quy chuẩn HyperFrames:
- 9 Scenes phân tích chuyên sâu (Bối cảnh -> Cú pháp -> Hoisting -> Parameters/Arguments -> Return -> Function Expression -> Arrow Function -> Rest Params -> Summary)
- Sub-compositions Intro.html (9.24s) & Outro.html (12.15s) tách biệt
- Light Theme Standard (Be Vietnam Pro, Rikkei Logo, Rikkei Red #ba252a, Fira Code)
- UIManager.render_scene Engine
- Voice-First Audio Generation (Kokoro-Vietnamese hung_thinh voice)
"""

import os
import json
import shutil
import soundfile as sf
from pathlib import Path
from hyperframes.ui_manager import UIManager
from kokoro_vietnamese import KokoroVietnamese

ROOT_DIR = Path.cwd()
OUTPUT_DIR = ROOT_DIR / "output" / "test_javascript_functions"
HYPERFRAMES_ASSETS = ROOT_DIR / "hyperframes" / "assets"
DEV_TUTORIAL_COMPS = ROOT_DIR / "hyperframes" / "dev-tutorial-video" / "src" / "compositions"

ui_mgr = UIManager()

DEEP_SCENES = [
    {
        "scene_id": "Scene_01",
        "scene_title": "Thách thức trùng lặp mã nguồn trong dự án thực tế",
        "duration": 45.0,
        "narration": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong nội dung bài học này, chúng ta sẽ cùng nhau tìm hiểu về cú pháp khai báo và sử dụng hàm trong JavaScript. Hãy cùng tưởng tượng một tình huống thực tế khi xây dựng hệ thống thương mại điện tử: Bạn có hàng chục tính năng cần tính thuế VAT và phí vận chuyển cho đơn hàng. Nếu không sử dụng hàm, mỗi khi cần tính toán, bạn phải chép lại cùng một công thức ở khắp nơi trong codebase. Hậu quả là khi chính sách thuế thay đổi, bạn phải đi tìm và sửa tay từng file một, gây ra thảm họa về bảo trì và rủi ro lỗi logic cực kỳ nghiêm trọng. Hàm ra đời như một cơ chế đóng gói, giúp gom nhóm các câu lệnh xử lý vào một nơi duy nhất để tái sử dụng.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-red-50 border-l-6 border-red-500 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-red-700 mb-4">❌ Không dùng Hàm (Code cồng kềnh, dễ lỗi)</h3>
                <pre><code class="language-javascript"><span class="cm">// Đơn hàng 1: Tính VAT + Ship</span>
<span class="kw">let</span> total1 = 100 * 1.1 + 15;

<span class="cm">// Đơn hàng 2: Phải lặp lại công thức</span>
<span class="kw">let</span> total2 = 250 * 1.1 + 15;

<span class="cm">// Đơn hàng 3: Lặp lại công thức lần 3...</span>
<span class="kw">let</span> total3 = 500 * 1.1 + 15;</code></pre>
            </div>
            <div class="bg-emerald-50 border-l-6 border-emerald-500 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-emerald-700 mb-4">✅ Đóng gói Hàm (Tái sử dụng 100%)</h3>
                <pre><code class="language-javascript"><span class="cm">// Đóng gói logic tại 1 nơi duy nhất</span>
<span class="kw">function</span> <span class="fn">calculateTotalOrder</span>(amount) {
    <span class="kw">const</span> VAT = 0.1;
    <span class="kw">const</span> SHIPPING = 15;
    <span class="kw">return</span> amount * (1 + VAT) + SHIPPING;
}

<span class="kw">let</span> total1 = <span class="fn">calculateTotalOrder</span>(100);
<span class="kw">let</span> total2 = <span class="fn">calculateTotalOrder</span>(250);</code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_02",
        "scene_title": "Giải phẫu cú pháp Function Declaration",
        "duration": 40.0,
        "narration": "Đầu tiên, hãy cùng giải phẫu cú pháp khai báo hàm truyền thống. Chúng ta bắt đầu bằng từ khóa function để thông báo cho trình biên dịch JavaScript. Tiếp theo là Tên hàm viết theo quy tắc camelCase đại diện cho hành động nghiệp vụ. Sau tên hàm là cặp ngoặc tròn chứa danh sách Tham số đầu vào. Cuối cùng là cặp ngoặc nhọn chứa Khối lệnh thực thi. Các em lưu ý: Tên hàm phải bắt đầu bằng động từ thể hiện mục đích như calculate, process, hoặc render. Việc đặt tên rõ ràng giúp mã nguồn trở nên tự giải thích.",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <ul class="flex flex-col gap-4">
                <li><span class="font-bold text-[#ba252a]">1. Từ khóa function:</span> Khai báo cho JS Engine tạo một function object mới.</li>
                <li><span class="font-bold text-[#ba252a]">2. Tên hàm (Identifier):</span> Đặt theo quy tắc camelCase bắt đầu bằng động từ (vd: calculateTotal, sendEmail).</li>
                <li><span class="font-bold text-[#ba252a]">3. Tham số & Khối lệnh:</span> Danh sách tham số trong ( ) và các dòng lệnh xử lý trong { }.</li>
            </ul>
            <pre><code class="language-javascript"><span class="kw">function</span> <span class="fn">sendWelcomeEmail</span>(userEmail, userName) {
    console.<span class="fn">log</span>(<span class="str">`Đã gửi email chào mừng tới ${userName} (${userEmail})`</span>);
}

<span class="cm">// Gọi hàm thực thi lời chào</span>
<span class="fn">sendWelcomeEmail</span>(<span class="str">"student@rikkei.edu.vn"</span>, <span class="str">"Nguyễn Văn A"</span>);</code></pre>
        </div>
        """
    },
    {
        "scene_id": "Scene_03",
        "scene_title": "Cơ chế Hoisting của Function Declaration",
        "duration": 42.0,
        "narration": "Một đặc tính cực kỳ quan trọng trong JavaScript Engine là cơ chế Hoisting. Khi chương trình khởi chạy, JavaScript Engine như V8 sẽ trải qua bước biên dịch. Toàn bộ định nghĩa hàm khai báo bằng từ khóa function sẽ được đưa lên đầu phạm vi bộ nhớ. Điều này đồng nghĩa với việc bạn có thể gọi hàm trước cả vị trí mà nó được định nghĩa trong mã nguồn mà không gặp bất kỳ lỗi ReferenceError nào. Đây là điểm khác biệt rất lớn so với khai báo biến thông thường.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-blue-50 border-l-6 border-blue-600 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-blue-700 mb-4">🚀 Gọi hàm trước khi Khai báo (Hoisting)</h3>
                <pre><code class="language-javascript"><span class="cm">// Lời gọi hàm diễn ra ở dòng 1</span>
<span class="fn">greetUser</span>(); <span class="cm">// Vẫn chạy thành công!</span>

<span class="cm">// Định nghĩa hàm ở dòng 5</span>
<span class="kw">function</span> <span class="fn">greetUser</span>() {
    console.<span class="fn">log</span>(<span class="str">"Xin chào từ Hoisting!"</span>);
}</code></pre>
            </div>
            <div class="bg-amber-50 border-l-6 border-amber-500 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-amber-800 mb-4">🧠 Bản chất dưới Hood (V8 Engine)</h3>
                <p class="text-xl text-slate-700 leading-relaxed mb-4">
                    Trong giai đoạn <strong>Creation Phase</strong>, V8 Engine quét toàn bộ mã nguồn và đưa định danh <code>greetUser</code> cùng thân hàm vào Memory Heap trước khi thực thi lệnh.
                </p>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_04",
        "scene_title": "Phân biệt Tham số (Parameters) & Đối số (Arguments)",
        "duration": 42.0,
        "narration": "Tiếp theo, hãy phân biệt rõ hai thuật ngữ rất hay bị nhầm lẫn: Tham số và Đối số. Tham số là các biến đại diện khai báo trong ngoặc tròn khi định nghĩa hàm. Còn Đối số là những giá trị dữ liệu thực tế được truyền vào khi chúng ta thực hiện lời gọi hàm. Nếu số lượng đối số truyền vào ít hơn số tham số khai báo, các tham số thiếu sẽ nhận giá trị undefined. Để tránh lỗi này, JavaScript ES6 cho phép chúng ta thiết lập Giá trị mặc định ngay trong phần khai báo.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-white p-6 border-l-6 border-[#ba252a] rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-[#ba252a] mb-3">📌 Tham số mặc định (Default Parameters)</h3>
                <pre><code class="language-javascript"><span class="kw">function</span> <span class="fn">createProduct</span>(name, price = <span class="str">0</span>, tax = <span class="str">0.1</span>) {
    <span class="kw">return</span> price * (1 + tax);
}

<span class="cm">// Không truyền tax -> Dùng mặc định 0.1</span>
console.<span class="fn">log</span>(<span class="fn">createProduct</span>(<span class="str">"Laptop"</span>, <span class="str">1000</span>));</code></pre>
            </div>
            <div class="bg-white p-6 border-l-6 border-sky-600 rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-sky-600 mb-3">⚠️ Rủi ro Thiếu Đối số</h3>
                <pre><code class="language-javascript"><span class="kw">function</span> <span class="fn">add</span>(a, b) {
    <span class="kw">return</span> a + b;
}

<span class="cm">// Chỉ truyền 1 đối số: b = undefined</span>
console.<span class="fn">log</span>(<span class="fn">add</span>(<span class="str">5</span>)); <span class="cm">// In ra: NaN</span></code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_05",
        "scene_title": "Giá trị trả về và Luồng điều khiển với từ khóa return",
        "duration": 40.0,
        "narration": "Mặc định, mọi hàm trong JavaScript nếu không khai báo return sẽ luôn trả về giá trị undefined. Từ khóa return đảm nhận hai nhiệm vụ sống còn: Một là trích xuất giá trị kết quả tính toán ra bên ngoài để truyền cho các biến hoặc biểu thức khác. Hai là ngay lập tức ngắt luồng thực thi và thoát khỏi hàm. Mọi dòng lệnh nằm phía sau từ khóa return trong cùng khối lệnh sẽ bị coi là Dead Code và bị ngắt hoàn toàn. Hãy luôn tận dụng điều này để viết các câu lệnh kiểm tra điều kiện sớm.",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <pre><code class="language-javascript"><span class="kw">function</span> <span class="fn">checkEligibility</span>(age) {
    <span class="kw">if</span> (age < <span class="str">18</span>) {
        <span class="kw">return</span> <span class="str">"Không đủ tuổi tham gia"</span>; <span class="cm">// Thoát sớm (Guard Clause)</span>
    }
    
    <span class="cm">// Xử lý logic phức tạp khi đủ tuổi</span>
    <span class="kw">return</span> <span class="str">"Đăng ký thành công tài khoản!"</span>;
}

console.<span class="fn">log</span>(<span class="fn">checkEligibility</span>(<span class="str">16</span>)); <span class="cm">// In ra: Không đủ tuổi tham gia</span></code></pre>
        </div>
        """
    },
    {
        "scene_id": "Scene_06",
        "scene_title": "Khai báo Hàm dạng Biểu thức (Function Expression)",
        "duration": 40.0,
        "narration": "Bên cạnh Function Declaration, JavaScript còn hỗ trợ cú pháp Function Expression — tức là gán một hàm ẩn danh vào một biến hằng số const hoặc let. Điểm khác biệt quan trọng nhất ở đây là Function Expression KHÔNG ĐƯỢC Hoisting. Nếu bạn gọi hàm trước khi dòng lệnh gán biến chạy, JavaScript Engine sẽ ném ra lỗi Cannot access before initialization. Cú pháp này giúp bảo vệ luồng thực thi, đảm bảo hàm chỉ được gọi sau khi đã khởi tạo an toàn.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-red-50 border-l-6 border-red-500 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-red-700 mb-3">❌ Không thể gọi trước (No Hoisting)</h3>
                <pre><code class="language-javascript"><span class="cm">// Lỗi: Cannot access before initialization</span>
<span class="fn">calculateTax</span>(<span class="str">500</span>);

<span class="kw">const</span> <span class="fn">calculateTax</span> = <span class="kw">function</span>(amount) {
    <span class="kw">return</span> amount * 0.1;
};</code></pre>
            </div>
            <div class="bg-white p-6 border-l-6 border-emerald-500 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-emerald-700 mb-3">✅ Khởi tạo và Gọi đúng thứ tự</h3>
                <pre><code class="language-javascript"><span class="kw">const</span> <span class="fn">calculateTax</span> = <span class="kw">function</span>(amount) {
    <span class="kw">return</span> amount * 0.1;
};

<span class="cm">// Đúng luồng tuần tự</span>
console.<span class="fn">log</span>(<span class="fn">calculateTax</span>(<span class="str">500</span>)); <span class="cm">// 50</span></code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_07",
        "scene_title": "Tối ưu mã nguồn với Arrow Function (ES6)",
        "duration": 42.0,
        "narration": "Từ phiên bản ES6, Arrow Function ra đời mang lại cú pháp ngắn gọn và hiện đại hơn rất nhiều. Ta thay thế từ khóa function bằng dấu mũi tên tạo bởi dấu bằng và dấu lớn hơn. Nếu hàm chỉ có duy nhất 1 câu lệnh return, ta có thể bỏ hoàn toàn cặp ngoặc nhọn và từ khóa return để viết hàm trên một dòng duy nhất. Cú pháp này được sử dụng cực kỳ phổ biến khi xử lý mảng với map, filter, hay trong các thư viện như React.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-white p-6 border-l-6 border-slate-400 rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-slate-700 mb-3">Cú pháp truyền thống</h3>
                <pre><code class="language-javascript"><span class="kw">const</span> numbers = [<span class="str">1</span>, <span class="str">2</span>, <span class="str">3</span>, <span class="str">4</span>];
<span class="kw">const</span> doubled = numbers.<span class="fn">map</span>(<span class="kw">function</span>(n) {
    <span class="kw">return</span> n * 2;
});</code></pre>
            </div>
            <div class="bg-white p-6 border-l-6 border-[#ba252a] rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-[#ba252a] mb-3">Arrow Function (Implicit Return)</h3>
                <pre><code class="language-javascript"><span class="kw">const</span> numbers = [<span class="str">1</span>, <span class="str">2</span>, <span class="str">3</span>, <span class="str">4</span>];
<span class="cm">// Ngắn gọn trên 1 dòng duy nhất</span>
<span class="kw">const</span> doubled = numbers.<span class="fn">map</span>(n => n * 2);

console.<span class="fn">log</span>(doubled); <span class="cm">// [2, 4, 6, 8]</span></code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_08",
        "scene_title": "Tham số gom nhóm với Rest Parameters (...args)",
        "duration": 40.0,
        "narration": "Trong thực tế phát triển phần mềm, sẽ có lúc bạn cần viết một hàm nhận số lượng đối số không cố định — ví dụ như tính tổng của 3 số, 5 số hoặc hàng trăm số. Khi đó, cú pháp Rest Parameters với dấu ba chấm (...numbers) sẽ gom tất cả các đối số truyền vào thành một mảng Array chính quy. Nhờ đó, ta dễ dàng sử dụng các phương thức xử lý mảng như reduce hoặc forEach để tính toán dữ liệu một cách linh hoạt.",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <pre><code class="language-javascript"><span class="cm">// Rest Parameter gom tất cả đối số thành mảng numbers</span>
<span class="kw">function</span> <span class="fn">sumAll</span>(...numbers) {
    <span class="kw">return</span> numbers.<span class="fn">reduce</span>((acc, curr) => acc + curr, <span class="str">0</span>);
}

console.<span class="fn">log</span>(<span class="fn">sumAll</span>(<span class="str">10</span>, <span class="str">20</span>));             <span class="cm">// In ra: 30</span>
console.<span class="fn">log</span>(<span class="fn">sumAll</span>(<span class="str">1</span>, <span class="str">2</span>, <span class="str">3</span>, <span class="str">4</span>, <span class="str">5</span>));    <span class="cm">// In ra: 15</span></code></pre>
        </div>
        """
    },
    {
        "scene_id": "Scene_09",
        "scene_title": "Tóm tắt bài học & Hướng dẫn thực hành",
        "duration": 30.0,
        "narration": "Tóm lại, hàm là trái tim của ngôn ngữ JavaScript. Qua bài học này, các em đã làm chủ từ Function Declaration, Hoisting, Tham số, từ khóa return cho tới Arrow Function và Rest Parameters. Hãy mở VS Code lên và thực hành ngay việc đóng gói các hàm tính toán nghiệp vụ. Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu về Scope - Phạm vi truy cập của biến Global vs Local. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <ul class="flex flex-col gap-4">
                <li>✅ <strong>Function Declaration vs Expression:</strong> Hiểu rõ bản chất Hoisting của V8 Engine.</li>
                <li>✅ <strong>Parameters & Return:</strong> Truyền tham số mặc định và thoát hàm sớm với return.</li>
                <li>✅ <strong>ES6 Arrow Function & Rest Params:</strong> Viết code hiện đại, ngắn gọn và linh hoạt.</li>
            </ul>
            <div class="bg-red-50 border-l-6 border-[#ba252a] p-5 rounded-xl text-xl text-[#ba252a] font-bold">
                🚀 Bài học tiếp theo: Scope & Closure trong JavaScript!
            </div>
        </div>
        """
    }
]

def build_deep_test_project():
    print("==========================================================")
    print("Creating Deep Pedagogical Video Project (9 Scenes)")
    print("Topic: Cú pháp khai báo và sử dụng hàm trong JavaScript")
    print("==========================================================")

    comp_dir = OUTPUT_DIR / "src" / "compositions"
    tts_dir = OUTPUT_DIR / "assets" / "tts"
    renders_dir = OUTPUT_DIR / "renders"

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    comp_dir.mkdir(parents=True, exist_ok=True)
    tts_dir.mkdir(parents=True, exist_ok=True)
    renders_dir.mkdir(parents=True, exist_ok=True)

    # Assets
    for asset in ["intro.mp4", "outro.mp4", "bg-music.mp3"]:
        src_file = HYPERFRAMES_ASSETS / asset
        dest_file = OUTPUT_DIR / "assets" / asset
        if src_file.exists():
            shutil.copy2(src_file, dest_file)
            print(f"[ASSET] Copied {asset}")

    # Intro & Outro compositions
    shutil.copy2(DEV_TUTORIAL_COMPS / "Intro.html", comp_dir / "Intro.html")
    shutil.copy2(DEV_TUTORIAL_COMPS / "Outro.html", comp_dir / "Outro.html")

    # Generate Scenes
    for scene in DEEP_SCENES:
        sc_id = scene["scene_id"]
        sc_dur = scene["duration"]
        html_content = ui_mgr.render_scene(scene, "JavaScript Functions")
        (comp_dir / f"{sc_id}.html").write_text(html_content, encoding="utf-8")
        print(f"[SCENE] Generated {sc_id}.html ({sc_dur}s)")

    # Kokoro TTS Synthesis
    print("\n[TTS] Synthesizing Kokoro-Vietnamese voiceover audio (hung_thinh)...")
    tts_model = KokoroVietnamese(device="cpu", voice="hung_thinh")
    probed_durations = {}

    for scene in DEEP_SCENES:
        sc_id = scene["scene_id"]
        text = scene["narration"]
        print(f"Synthesizing {sc_id}...")
        audio, _ = tts_model.synthesize(text, speed=0.95)
        wav_path = tts_dir / f"{sc_id}.wav"
        sf.write(str(wav_path), audio, 24000)
        dur = round(len(audio) / 24000, 2)
        probed_durations[sc_id] = dur
        print(f"[OK] {sc_id}.wav | Probed Duration: {dur}s")

        # Update scene HTML data-duration attribute
        sc_file = comp_dir / f"{sc_id}.html"
        content = sc_file.read_text(encoding="utf-8")
        content = content.replace(f'data-duration="{scene["duration"]}"', f'data-duration="{dur}"')
        sc_file.write_text(content, encoding="utf-8")

    (tts_dir / "durations.json").write_text(json.dumps(probed_durations, indent=2, ensure_ascii=False), encoding="utf-8")

    # Master index.html
    intro_dur = 9.24
    outro_dur = 12.15
    current_start = intro_dur
    scene_clips = []
    audio_clips = []

    for idx, scene in enumerate(DEEP_SCENES):
        sc_id = scene["scene_id"]
        num = str(idx + 1).zfill(2)
        dur = probed_durations[sc_id]
        trk = idx + 1
        aud_trk = 20 + idx

        scene_clips.append(f'      <div class="clip" data-composition-src="src/compositions/{sc_id}.html" data-composition-id="scene-{num}" data-start="{round(current_start, 2)}" data-duration="{dur}" data-track-index="{trk}"></div>')
        audio_clips.append(f'      <audio id="tts-{num}" data-start="{round(current_start, 2)}" data-duration="{dur}" data-track-index="{aud_trk}" data-volume="1" src="assets/tts/{sc_id}.wav"></audio>')
        current_start += dur

    outro_start = round(current_start, 2)
    total_duration = round(intro_dur + sum(probed_durations.values()) + outro_dur, 2)

    index_html = f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0f172a; }}
      .clip {{ position: absolute; visibility: hidden; }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="test-javascript-functions"
      data-start="0"
      data-duration="{total_duration}"
      data-width="1920"
      data-height="1080"
    >
      <!-- Intro Composition Clip (9.24s) -->
      <div class="clip" data-composition-src="src/compositions/Intro.html"
           data-composition-id="scene-intro" data-start="0" data-duration="9.24" data-track-index="0"></div>

      <!-- Scene Clips -->
{chr(10).join(scene_clips)}

      <!-- Outro Composition Clip (12.15s) -->
      <div class="clip" data-composition-src="src/compositions/Outro.html"
           data-composition-id="scene-outro" data-start="{outro_start}" data-duration="12.15" data-track-index="0"></div>

      <!-- Background Music Kênh 99 -->
      <audio id="bg-music"
             data-start="0"
             data-duration="{total_duration}"
             data-track-index="99"
             data-volume="0.12"
             data-loop="true"
             src="assets/bg-music.mp3"></audio>

      <!-- TTS Audio Elements -->
{chr(10).join(audio_clips)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["test-javascript-functions"] = tl;
    </script>
  </body>
</html>"""

    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # package.json & meta.json
    (OUTPUT_DIR / "package.json").write_text(json.dumps({
        "name": "test-javascript-functions",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "npx --yes hyperframes@0.6.63 preview",
            "check": "npx --yes hyperframes@0.6.63 lint && npx --yes hyperframes@0.6.63 validate && npx --yes hyperframes@0.6.63 inspect",
            "render": "npx --yes hyperframes@0.6.63 render",
            "publish": "npx --yes hyperframes@0.6.63 publish"
        }
    }, indent=2), encoding="utf-8")

    (OUTPUT_DIR / "meta.json").write_text(json.dumps({
        "id": "test-javascript-functions",
        "name": "JavaScript Functions - Deep Syntax, Hoisting, Arrow & Rest Params"
    }, indent=2), encoding="utf-8")

    # gen_tts.py
    (OUTPUT_DIR / "gen_tts.py").write_text(f"""import sys
import os
import json
import soundfile as sf
from kokoro_vietnamese import KokoroVietnamese

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

tts_dir = "assets/tts"
os.makedirs(tts_dir, exist_ok=True)

print("Initializing Kokoro-Vietnamese TTS model (Voice: hung_thinh)...")
tts = KokoroVietnamese(device="cpu", voice="hung_thinh")

scenes = {json.dumps([{"id": s["scene_id"], "text": s["narration"]} for s in DEEP_SCENES], indent=4, ensure_ascii=False)}

durations = {{}}
for scene in scenes:
    print(f"Synthesizing {{scene['id']}} with Kokoro-Vietnamese...")
    audio, _ = tts.synthesize(scene['text'], speed=0.95)
    audio_path = os.path.join(tts_dir, f"{{scene['id']}}.wav")
    sf.write(audio_path, audio, 24000)
    duration = round(len(audio) / 24000, 2)
    durations[scene['id']] = duration
    print(f"[OK] Generated {{scene['id']}}.wav | Duration: {{duration}}s")

durations_path = os.path.join(tts_dir, "durations.json")
with open(durations_path, "w", encoding="utf-8") as f:
    json.dump(durations, f, indent=2, ensure_ascii=False)

print(f"\\n[DONE] Successfully generated all audio files and saved durations to {{durations_path}}")
""", encoding="utf-8")

    print(f"==========================================================")
    print(f"SUCCESS: Deep Pedagogical Video Project Built! Total Duration: {total_duration}s")
    print(f"==========================================================")

if __name__ == "__main__":
    build_deep_test_project()
