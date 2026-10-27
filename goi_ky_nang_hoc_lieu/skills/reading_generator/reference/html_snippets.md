# Component markup for readings

Reminders of the component structure, in the light style of the approved frame. Copy the real classes, scripts and helper functions from an approved reading; do not invent new visuals. Replace `{...}` placeholders with real content and never leave them in the output. No emoji, no `dark:` variants, no ALL CAPS labels.

## 1. Callouts (short text only; never put a code block inside)

```html
<!-- Lưu ý, cảnh báo -->
<div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">{text}</div>
<!-- Lỗi -->
<div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">{text}</div>
<!-- Cách làm tốt -->
<div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/60 text-slate-800 my-4">{text}</div>
<!-- Mẹo, thông tin, yêu cầu bài toán -->
<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
  <p class="font-bold text-sky-900 mb-1">Yêu cầu bài toán</p>
  <p>{context, constraints, expected output}</p>
</div>
```

## 2. Hero illustration (Section 1) and caption

```html
<figure class="my-6">
  <img src="{image}" alt="{description}" class="w-full max-w-3xl h-auto mx-auto rounded-xl shadow-sm" />
  <figcaption class="text-center text-sm text-slate-500 italic mt-3">{caption}</figcaption>
</figure>
<!-- or an inline 16:9 SVG: <svg viewBox="0 0 800 450" class="w-full h-auto">...</svg> with the same figcaption -->
```

## 3. Static code card (syntax templates, commands)

```html
<div class="my-4 rounded-xl overflow-hidden border border-slate-700 bg-slate-900">
  <div class="flex items-center gap-2 px-4 py-2 bg-slate-800 text-slate-200 text-xs">
    <span class="w-3 h-3 rounded-full" style="background:#ff5f56"></span>
    <span class="w-3 h-3 rounded-full" style="background:#ffbd2e"></span>
    <span class="w-3 h-3 rounded-full" style="background:#27c93f"></span>
    <span class="ml-2 font-semibold">{Descriptive title in Title Case}</span>
    <button type="button" onclick="copySandboxCode('{code-id}', this)" class="ml-auto" title="Sao chép"><i class="ph-bold ph-copy"></i></button>
  </div>
  <pre><code id="{code-id}" class="hljs language-{lang}">{code, newlines preserved, < and > encoded}</code></pre>
</div>
```

## 4. Executable sandbox (only where an engine exists, see R11)

```html
{requirement box from section 1 above}
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-6">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-3 right-3 flex items-center gap-1.5 z-10 bg-white/90 px-2 py-1 rounded-lg border border-slate-200">
      <button type="button" onclick="clearSandbox('code-{n}', 'output-{n}', 'container-{n}')" title="Khôi phục mã gốc"><i class="ph-bold ph-x"></i></button>
      <button type="button" onclick="runPythonCode('code-{n}', 'output-{n}', 'container-{n}')" title="Chạy chương trình"><i class="ph-bold ph-play"></i></button>
      <button type="button" onclick="copySandboxCode('code-{n}', this)" title="Sao chép"><i class="ph-bold ph-copy"></i></button>
    </div>
    <pre id="code-{n}" contenteditable="true" spellcheck="false" data-original="{escaped code}"
         class="w-full min-h-24 bg-transparent p-4 outline-none pr-28 whitespace-pre-wrap">{code}</pre>
  </div>
  <div id="container-{n}" class="hidden p-4 bg-slate-900 font-mono text-sm text-emerald-400">
    <p class="text-slate-400 text-xs mb-2">Kết quả</p>
    <pre id="output-{n}"></pre>
  </div>
</div>
```
The runner function depends on the stack (`runPythonCode` for Pyodide, a JavaScript worker for browser JS). Do not include a runner for a stack that has no engine.

## 5. Good versus bad comparison (Section 2; complete code in both columns)

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <div class="bg-rose-50 border border-rose-200 rounded-xl p-4">
    <div class="flex items-center gap-2 text-rose-700 font-bold text-sm mb-3"><i class="ph-bold ph-x-circle"></i><span>Cách sai cần tránh</span></div>
    <pre><code class="language-{lang}">{wrong code}</code></pre>
    <p class="text-sm text-rose-700 mt-2">{drawback}</p>
  </div>
  <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
    <div class="flex items-center gap-2 text-emerald-700 font-bold text-sm mb-3"><i class="ph-bold ph-check-circle"></i><span>Cách nên dùng</span></div>
    <pre><code class="language-{lang}">{right code}</code></pre>
    <p class="text-sm text-emerald-700 mt-2">{benefit}</p>
  </div>
</div>
```

## 6. Step-by-step simulator (sub-section 2.4; light panel)

Heading: "Mô phỏng cơ chế vận hành từng bước". Controls, all with Vietnamese labels and `type="button"`:

```html
<div class="w-full my-8 rounded-2xl bg-white border border-slate-200 overflow-hidden shadow-sm" id="viz-{id}">
  <div class="flex flex-wrap items-center gap-2 p-3 border-b border-slate-200 bg-slate-50">
    <button type="button" onclick="visualizerTogglePlay('{id}')"><i class="ph-bold ph-play"></i> Tự động chạy</button>
    <button type="button" onclick="visualizerPrev('{id}')"><i class="ph-bold ph-skip-back"></i> Lùi lại</button>
    <button type="button" onclick="visualizerNext('{id}')"><i class="ph-bold ph-skip-forward"></i> Tiếp theo</button>
    <button type="button" onclick="visualizerReset('{id}')"><i class="ph-bold ph-arrow-counter-clockwise"></i> Thử lại</button>
    <select aria-label="Tốc độ"><option>1.5s</option><option>1.0s</option><option>0.5s</option></select>
    <input type="range" aria-label="Giá trị đầu vào" />  <!-- slider or input for the value being traced -->
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">
    <div class="p-4 font-mono text-sm" id="tracker-code-{id}"><!-- one .tracker-line per code line, syntax highlighted, no line numbers --></div>
    <div class="p-4">
      <p class="text-xs font-bold text-slate-600 mb-2">Bảng bộ nhớ và trạng thái biến</p>
      <table class="w-full text-sm"><thead><tr><th class="text-left">Biến</th><th class="text-left">Kiểu</th><th class="text-left">Giá trị</th></tr></thead><tbody id="tracker-vars-{id}" class="font-mono"></tbody></table>
    </div>
  </div>
  <div class="p-3 border-t border-slate-200 bg-slate-900 font-mono text-sm text-emerald-400" id="tracker-console-{id}"></div>
</div>
```
Condition badges use text and Phosphor icons, for example `<i class="ph-bold ph-check-circle"></i> Đúng, khớp` and `<i class="ph-bold ph-x-circle"></i> Sai, bỏ qua`; never emoji.

```css
.tracker-line { color: #475569; font-weight: 500; padding: 2px 4px; border-radius: 4px; border-left: 3px solid transparent; transition: all .2s ease; }
.tracker-line.active-step { background: rgba(190, 17, 28, .10); border-left-color: #be111c; color: #0f172a; font-weight: 700; }
.var-updated { animation: pulse-var 1s ease; }
@keyframes pulse-var { 0% { background: rgba(16, 185, 129, .25); } 100% { background: transparent; } }
```
The simulator must declare its step array before the controls read it; ids must match the selectors one to one.

## 7. Decision table (Section 4)

```html
<div class="overflow-x-auto my-6">
  <table class="w-full text-sm border-collapse">
    <thead class="bg-rikkei-red text-white"><tr><th class="px-4 py-3 text-left">Tình huống</th><th class="px-4 py-3 text-left">Lựa chọn nên dùng</th><th class="px-4 py-3 text-left">Lý do</th></tr></thead>
    <tbody class="divide-y divide-slate-200">
      <tr class="hover:bg-slate-50"><td class="px-4 py-3">{...}</td><td class="px-4 py-3 font-mono text-emerald-700 font-semibold">{...}</td><td class="px-4 py-3 text-slate-600">{...}</td></tr>
    </tbody>
  </table>
</div>
```

## 8. Self-test (Section 5)

```html
<section id="section-5" class="mb-10 scroll-mt-24">
  <h2 class="font-montserrat font-bold text-2xl text-slate-900 mb-6">5. Khảo thí tự đánh giá</h2>
  <div class="border border-slate-200 rounded-xl p-5 mb-4 bg-slate-50">
    <p class="font-semibold text-slate-900 mb-3">{scenario question on concrete data from the reading}</p>
    <div class="space-y-2">
      <label class="flex items-center gap-3 p-3 rounded-lg border border-slate-200 cursor-pointer"><input type="radio" name="q1" value="A" class="accent-rikkei-red" /><span>A. {option}</span></label>
      <!-- B, C, D with the same length and structure -->
    </div>
    <div id="feedback-q1" class="hidden mt-3 p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-sm text-emerald-800">
      <i class="ph-bold ph-check-circle"></i> <strong>Đáp án: {X}</strong> — {explanation using the reading's own data}
    </div>
  </div>
  <button type="button" id="btn-check-answers" onclick="checkSelfTest()" class="w-full py-3 bg-rikkei-red text-white font-bold text-sm rounded-xl">Kiểm tra đáp án</button>
  <div id="selftest-result" class="hidden mt-4 p-4 rounded-xl border border-slate-200 text-sm font-semibold text-center"></div>
</section>
```
The correct-answer map inside `checkSelfTest()` must list exactly the options present in the HTML.
