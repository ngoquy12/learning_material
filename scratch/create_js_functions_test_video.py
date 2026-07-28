"""
scratch/create_js_functions_test_video.py

Tạo dự án video thử nghiệm bài học: "Cú pháp khai báo và sử dụng hàm trong JavaScript"
Tuân thủ 100% quy chuẩn HyperFrames:
- Sub-compositions Intro.html (9.24s) & Outro.html (12.15s) tách biệt
- Light Theme Standard (Be Vietnam Pro, Rikkei Logo, Rikkei Red #ba252a, Fira Code)
- UIManager.render_scene Engine
- Root index.html với absolute audio/composition clips
"""

import json
import shutil
from pathlib import Path
from hyperframes.ui_manager import UIManager

ROOT_DIR = Path.cwd()
OUTPUT_DIR = ROOT_DIR / "output" / "test_javascript_functions"
HYPERFRAMES_ASSETS = ROOT_DIR / "hyperframes" / "assets"
DEV_TUTORIAL_COMPS = ROOT_DIR / "hyperframes" / "dev-tutorial-video" / "src" / "compositions"

ui_mgr = UIManager()

SCENES_DATA = [
    {
        "scene_id": "Scene_01",
        "scene_title": "Tại sao phải sử dụng Hàm trong JavaScript?",
        "duration": 32.5,
        "narration": "Chào mừng các em đã quay trở lại với khóa học JavaScript tại Rikkei Education. Hãy tưởng tượng khi xây dựng một website bán hàng, bạn cần tính giá sau chiết khấu cho hàng chục sản phẩm khác nhau. Nếu không dùng hàm, bạn sẽ phải chép đi chép lại cùng một công thức tính toán ở khắp mọi nơi. Điều này khiến mã nguồn trở nên cồng kềnh, dễ phát sinh lỗi và cực kỳ khó bảo trì. Hàm ra đời như một chiếc hộp công cụ đóng gói các câu lệnh xử lý, giúp chúng ta tái sử dụng code một cách thông minh và chuyên nghiệp.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-red-50 border-l-6 border-red-500 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-red-700 mb-4">❌ Không dùng Hàm (Trùng lặp Code)</h3>
                <pre class="bg-white p-4 rounded-lg text-xl font-mono text-slate-800 border"><code>// Sản phẩm 1
let price1 = 100;
let final1 = price1 * (1 - 0.1);

// Sản phẩm 2
let price2 = 250;
let final2 = price2 * (1 - 0.1);</code></pre>
            </div>
            <div class="bg-emerald-50 border-l-6 border-emerald-500 p-6 rounded-xl shadow-sm">
                <h3 class="text-2xl font-bold text-emerald-700 mb-4">✅ Sử dụng Hàm (Tái sử dụng Code)</h3>
                <pre class="bg-white p-4 rounded-lg text-xl font-mono text-slate-800 border"><code>// Đóng gói logic vào 1 nơi
function calculateDiscount(price) {
    return price * 0.9;
}

let final1 = calculateDiscount(100);
let final2 = calculateDiscount(250);</code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_02",
        "scene_title": "Cú pháp khai báo Hàm (Function Declaration)",
        "duration": 35.0,
        "narration": "Để định nghĩa một hàm trong JavaScript, chúng ta sử dụng từ khóa function, theo sau là tên hàm mô tả đúng chức năng nghiệp vụ, cặp ngoặc tròn chứa các tham số truyền vào, và cặp ngoặc nhọn chứa các câu lệnh thực thi. Tên hàm nên tuân theo quy tắc camelCase và bắt đầu bằng một động từ chỉ hành động như calculate, show, hoặc process. Ví dụ: function sayHello() sẽ thực thi câu lệnh console.log để in ra lời chào.",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <ul class="flex flex-col gap-4">
                <li><span class="font-bold text-[#ba252a]">1. Từ khóa function:</span> Thông báo cho JavaScript biết chúng ta đang định nghĩa một hàm mới.</li>
                <li><span class="font-bold text-[#ba252a]">2. Tên hàm (Function Name):</span> Viết theo chuẩn camelCase đại diện cho hành động (vd: calculateTotal, getUserData).</li>
                <li><span class="font-bold text-[#ba252a]">3. Khối lệnh (Body Block):</span> Đặt trong cặp ngoặc nhọn { ... } thực thi các tác vụ tính toán.</li>
            </ul>
            <pre><code class="language-javascript"><span class="kw">function</span> <span class="fn">sayHello</span>() {
    console.<span class="fn">log</span>(<span class="str">"Chào mừng bạn đến với Rikkei Education!"</span>);
}

<span class="cm">// Gọi hàm để thực thi</span>
<span class="fn">sayHello</span>();</code></pre>
        </div>
        """
    },
    {
        "scene_id": "Scene_03",
        "scene_title": "Tham số (Parameters) và Đối số (Arguments)",
        "duration": 34.0,
        "narration": "Một hàm sẽ trở nên linh hoạt hơn rất nhiều khi nhận dữ liệu đầu vào. Trong JavaScript, Tham số (Parameters) là các biến đại diện được khai báo ở định nghĩa hàm. Còn Đối số (Arguments) là các giá trị thực tế mà chúng ta truyền vào khi gọi hàm thực thi. Hãy quan sát hàm calculateSum nhận 2 tham số a và b. Khi ta gọi calculateSum(5, 10), giá trị 5 và 10 chính là đối số được truyền trực tiếp vào hàm.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-white p-6 border-l-6 border-[#ba252a] rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-[#ba252a] mb-3">📌 Tham số (Parameters)</h3>
                <p class="text-xl text-slate-700 mb-4">Các biến đóng vai trò giữ chỗ khai báo trong cặp ngoặc tròn.</p>
                <pre><code>function calculateSum(<span class="kw">a</span>, <span class="kw">b</span>) {
    console.log(a + b);
}</code></pre>
            </div>
            <div class="bg-white p-6 border-l-6 border-sky-600 rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-sky-600 mb-3">📌 Đối số (Arguments)</h3>
                <p class="text-xl text-slate-700 mb-4">Giá trị cụ thể truyền vào hàm khi thực hiện lời gọi hàm.</p>
                <pre><code><span class="cm">// 5 gán cho a, 10 gán cho b</span>
calculateSum(<span class="str">5</span>, <span class="str">10</span>); <span class="cm">// In ra: 15</span></code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_04",
        "scene_title": "Trả về giá trị với từ khóa return",
        "duration": 32.0,
        "narration": "Mặc định, nếu một hàm không sử dụng từ khóa return, JavaScript sẽ tự động trả về giá trị undefined. Từ khóa return có hai nhiệm vụ quan trọng: Thứ nhất, nó trả về kết quả tính toán của hàm ra bên ngoài để tiếp tục sử dụng cho các biến khác. Thứ hai, nó ngay lập tức dừng việc thực thi hàm, tất cả các dòng lệnh đứng sau lệnh return trong khối hàm đều sẽ bị bỏ qua.",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <pre><code class="language-javascript"><span class="kw">function</span> <span class="fn">multiply</span>(x, y) {
    <span class="kw">return</span> x * y; <span class="cm">// Trả kết quả và thoát khỏi hàm</span>
    console.<span class="fn">log</span>(<span class="str">"Dòng lệnh này sẽ KHÔNG bao giờ chạy"</span>);
}

<span class="kw">let</span> result = <span class="fn">multiply</span>(<span class="str">4</span>, <span class="str">7</span>);
console.<span class="fn">log</span>(result); <span class="cm">// In ra: 28</span></code></pre>
            <div class="bg-amber-50 border-l-6 border-amber-500 p-5 rounded-xl text-xl text-amber-900">
                ⚠️ <strong>Lưu ý quan trọng:</strong> Luôn kiểm tra điều kiện trả về trước khi xử lý logic phức tạp để tránh lỗi tính toán.
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_05",
        "scene_title": "Arrow Function (Hàm mũi tên ES6)",
        "duration": 36.0,
        "narration": "Từ phiên bản ES6, JavaScript giới thiệu cú pháp Arrow Function giúp viết hàm ngắn gọn hơn rất nhiều. Thay vì dùng từ khóa function, chúng ta sử dụng dấu mũi tên được tạo bởi dấu bằng và dấu lớn hơn. Nếu hàm chỉ có một câu lệnh return duy nhất, ta thậm chí có thể bỏ cả cặp ngoặc nhọn và từ khóa return. Cú pháp này được sử dụng cực kỳ phổ biến trong các thư viện hiện đại như React hoặc Node.js.",
        "clean_content": """
        <div class="grid grid-cols-2 gap-8 w-full text-left">
            <div class="bg-white p-6 border-l-6 border-slate-400 rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-slate-700 mb-3">Cú pháp Function truyền thống</h3>
                <pre><code><span class="kw">function</span> <span class="fn">square</span>(n) {
    <span class="kw">return</span> n * n;
}</code></pre>
            </div>
            <div class="bg-white p-6 border-l-6 border-[#ba252a] rounded-xl shadow-md">
                <h3 class="text-2xl font-bold text-[#ba252a] mb-3">Arrow Function ES6 ngắn gọn</h3>
                <pre><code><span class="kw">const</span> <span class="fn">square</span> = (n) => n * n;

console.<span class="fn">log</span>(<span class="fn">square</span>(<span class="str">6</span>)); <span class="cm">// In ra: 36</span></code></pre>
            </div>
        </div>
        """
    },
    {
        "scene_id": "Scene_06",
        "scene_title": "Tổng kết bài học & Thực hành",
        "duration": 25.0,
        "narration": "Tóm lại, hàm là nền tảng cốt lõi trong JavaScript giúp tái sử dụng code, đóng gói logic và giữ mã nguồn sạch sẽ. Hãy nhớ kỹ cú pháp function declaration, cách truyền tham số và từ khóa return nhé. Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu về Phạm vi của biến hay Scope trong JavaScript. Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!",
        "clean_content": """
        <div class="flex flex-col gap-6 w-full text-left">
            <ul class="flex flex-col gap-4">
                <li>✅ <strong>Đóng gói Code:</strong> Giúp tránh lặp lại mã nguồn và dễ bảo trì.</li>
                <li>✅ <strong>Linh hoạt:</strong> Truyền tham số dữ liệu linh hoạt và nhận kết quả bằng `return`.</li>
                <li>✅ <strong>Hiện đại:</strong> Sử dụng Arrow Function ES6 cho cú pháp ngắn gọn.</li>
            </ul>
            <div class="bg-red-50 border-l-6 border-[#ba252a] p-5 rounded-xl text-xl text-[#ba252a] font-bold">
                🚀 Bài học tiếp theo: Scope (Phạm vi biến Global vs Local) trong JavaScript!
            </div>
        </div>
        """
    }
]

def build_test_project():
    print("==========================================================")
    print("Creating HyperFrames Video Project: JavaScript Functions Test")
    print("==========================================================")

    # 1. Prepare directory structure
    comp_dir = OUTPUT_DIR / "src" / "compositions"
    tts_dir = OUTPUT_DIR / "assets" / "tts"
    renders_dir = OUTPUT_DIR / "renders"

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    comp_dir.mkdir(parents=True, exist_ok=True)
    tts_dir.mkdir(parents=True, exist_ok=True)
    renders_dir.mkdir(parents=True, exist_ok=True)

    # 2. Copy Media Assets (intro.mp4, outro.mp4, bg-music.mp3)
    for asset in ["intro.mp4", "outro.mp4", "bg-music.mp3"]:
        src_file = HYPERFRAMES_ASSETS / asset
        dest_file = OUTPUT_DIR / "assets" / asset
        if src_file.exists():
            shutil.copy2(src_file, dest_file)
            print(f"[ASSET] Copied {asset} -> {dest_file.relative_to(ROOT_DIR)}")

    # 3. Copy/Create Intro.html and Outro.html Sub-compositions
    intro_src = DEV_TUTORIAL_COMPS / "Intro.html"
    outro_src = DEV_TUTORIAL_COMPS / "Outro.html"
    
    if intro_src.exists():
        shutil.copy2(intro_src, comp_dir / "Intro.html")
    if outro_src.exists():
        shutil.copy2(outro_src, comp_dir / "Outro.html")

    print("[SUB-COMP] Intro.html and Outro.html created in src/compositions/")

    # 4. Generate Scene Sub-compositions using UIManager
    durations = {}
    total_scene_dur = 0.0
    intro_dur = 9.24
    outro_dur = 12.15

    for scene in SCENES_DATA:
        sc_id = scene["scene_id"]
        sc_dur = scene["duration"]
        durations[sc_id] = sc_dur
        total_scene_dur += sc_dur

        html_content = ui_mgr.render_scene(scene, "JavaScript Functions")
        scene_file = comp_dir / f"{sc_id}.html"
        scene_file.write_text(html_content, encoding="utf-8")
        print(f"[SCENE] Generated {sc_id}.html ({sc_dur}s)")

        # Create placeholder WAV TTS file for verification
        dummy_wav = tts_dir / f"{sc_id}.wav"
        dummy_wav.write_bytes(b"RIFF....WAVEfmt ....data....")

    total_duration = round(intro_dur + total_scene_dur + outro_dur, 2)
    durations_json = tts_dir / "durations.json"
    durations_json.write_text(json.dumps(durations, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TTS] Saved durations.json | Total Scenes Duration: {total_scene_dur}s")

    # 5. Create Root index.html
    scene_clips_html = []
    audio_clips_html = []
    current_start = intro_dur

    for idx, scene in enumerate(SCENES_DATA):
        sc_id = scene["scene_id"]
        sc_num = str(idx + 1).zfill(2)
        sc_dur = scene["duration"]
        sc_slug = f"scene-{sc_num}"
        track_idx = idx + 1
        audio_track = 20 + idx

        clip_str = f'      <div class="clip" data-composition-src="src/compositions/{sc_id}.html" data-composition-id="{sc_slug}" data-start="{round(current_start, 2)}" data-duration="{sc_dur}" data-track-index="{track_idx}"></div>'
        audio_str = f'      <audio id="tts-{sc_num}" data-start="{round(current_start, 2)}" data-duration="{sc_dur}" data-track-index="{audio_track}" data-volume="1" src="assets/tts/{sc_id}.wav"></audio>'

        scene_clips_html.append(clip_str)
        audio_clips_html.append(audio_str)
        current_start += sc_dur

    outro_start = round(current_start, 2)

    index_html_content = f"""<!doctype html>
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
{chr(10).join(scene_clips_html)}

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
{chr(10).join(audio_clips_html)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["test-javascript-functions"] = tl;
    </script>
  </body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(index_html_content, encoding="utf-8")
    print(f"[INDEX] Generated root index.html | Total Duration: {total_duration}s")

    # 6. Create package.json and meta.json
    package_json = {
        "name": "test-javascript-functions",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "npx --yes hyperframes@0.6.63 preview",
            "check": "npx --yes hyperframes@0.6.63 lint && npx --yes hyperframes@0.6.63 validate && npx --yes hyperframes@0.6.63 inspect",
            "render": "npx --yes hyperframes@0.6.63 render",
            "publish": "npx --yes hyperframes@0.6.63 publish"
        }
    }
    (OUTPUT_DIR / "package.json").write_text(json.dumps(package_json, indent=2), encoding="utf-8")

    meta_json = {
        "id": "test-javascript-functions",
        "name": "JavaScript Functions - Syntax and Usage"
    }
    (OUTPUT_DIR / "meta.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")

    # 7. Create Kokoro gen_tts.py inside project
    gen_tts_py = f"""import sys
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

scenes = {json.dumps([{"id": s["scene_id"], "text": s["narration"]} for s in SCENES_DATA], indent=4, ensure_ascii=False)}

durations = {{}}
for scene in scenes:
    print(f"Synthesizing {{scene['id']}} with Kokoro-Vietnamese...")
    audio, _ = tts.synthesize(scene['text'], speed=1.0)
    audio_path = os.path.join(tts_dir, f"{{scene['id']}}.wav")
    sf.write(audio_path, audio, 24000)
    duration = round(len(audio) / 24000, 2)
    durations[scene['id']] = duration
    print(f"[OK] Generated {{scene['id']}}.wav | Duration: {{duration}}s")

durations_path = os.path.join(tts_dir, "durations.json")
with open(durations_path, "w", encoding="utf-8") as f:
    json.dump(durations, f, indent=2, ensure_ascii=False)

print(f"\\n[DONE] Successfully generated all audio files and saved durations to {{durations_path}}")
"""
    (OUTPUT_DIR / "gen_tts.py").write_text(gen_tts_py, encoding="utf-8")

    print("==========================================================")
    print(f"SUCCESS: Project created at {OUTPUT_DIR}")
    print("==========================================================")

if __name__ == "__main__":
    build_test_project()
