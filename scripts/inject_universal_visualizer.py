import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = Path(__file__).resolve().parent.parent / "output"
reading_files = list(base_dir.glob("**/Bài đọc/reading.html")) + list(base_dir.glob("**/reading.html"))

universal_engine_script = """
    <!-- Smart Self-Healing Interactive Visualizer Engine -->
    <script>
    class InteractiveVisualizerEngine {
        constructor() {
            this.currentStep = 0;
            this.isPlaying = false;
            this.speed = 500;
            this.steps = [];
            this.inputText = '';
            this.timer = null;
        }

        init() {
            const container = document.getElementById('visualizer-canvas');
            if (!container) return;

            const inputEl = document.getElementById('custom-data-input');
            if (inputEl && inputEl.value) {
                this.inputText = inputEl.value.trim();
            } else {
                this.inputText = "10, 20, 30, 40, 50";
                if (inputEl) inputEl.value = this.inputText;
            }

            this.applyCustomData();
        }

        log(msg) {
            const history = document.getElementById('log-messages');
            if (history) {
                const line = document.createElement('div');
                line.className = 'log-entry log-info';
                line.style.padding = '4px 0';
                line.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                line.innerHTML = `<span style="color: #64748b;">[${new Date().toLocaleTimeString()}]</span> <span style="color: #38bdf8;">&gt;</span> ${msg}`;
                history.appendChild(line);
                history.scrollTop = history.scrollHeight;
            }
        }

        clearLog() {
            const history = document.getElementById('log-messages');
            if (history) history.innerHTML = '<div class="log-entry log-info">ℹ [Hệ thống] Đã xóa nhật ký thuật toán.</div>';
        }

        applyCustomData() {
            const inputEl = document.getElementById('custom-data-input');
            if (inputEl && inputEl.value) {
                this.inputText = inputEl.value.trim();
            }
            this.reset();
        }

        reset() {
            this.pause();
            this.currentStep = 0;
            this.steps = [];
            this.buildExecutionSteps();
            this.clearLog();
            this.log('Khởi tạo mô phỏng trực quan hóa cho dữ liệu: ' + this.inputText);
            this.render();
        }

        buildExecutionSteps() {
            const pageTitle = document.title || '';
            const items = this.inputText.split(',').map(s => s.trim()).filter(Boolean);
            const dataList = items.length > 0 ? items : ["Phần tử 1", "Phần tử 2", "Phần tử 3"];
            
            let steps = [];

            // Step 0: Initial State
            steps.push({
                highlightLines: ['line-0', 'line-1', 'line-2'],
                status: 'Khởi tạo',
                mode: 'Khởi đầu',
                result: 'Sẵn sàng',
                log: 'Khởi tạo cấu trúc mảng bộ nhớ RAM và thiết lập thông số ban đầu.',
                items: dataList.map((val, idx) => ({ val, state: 'idle', idx }))
            });

            // Step 1: Memory Allocation
            steps.push({
                highlightLines: ['line-3', 'line-4', 'line-5'],
                status: 'Cấp phát bộ nhớ',
                mode: 'Bộ nhớ RAM',
                result: 'Đã cấp phát',
                log: `Cấp phát ${dataList.length} ô nhớ liên tiếp cho các phần tử mảng dữ liệu.`,
                items: dataList.map((val, idx) => ({ val, state: 'active', idx }))
            });

            // Step 2: Processing Loop (Item by Item)
            dataList.forEach((val, i) => {
                steps.push({
                    highlightLines: [`line-${6 + (i % 4)}`],
                    status: `Xử lý phần tử [${i}]`,
                    mode: 'Tuần tự',
                    result: 'Đang duyệt',
                    log: `Duyệt qua phần tử thứ ${i + 1}: giá trị = "${val}" tại chỉ mục index ${i}.`,
                    items: dataList.map((v, idx) => ({
                        val: v,
                        state: idx === i ? 'comparing' : (idx < i ? 'done' : 'idle'),
                        idx
                    }))
                });
            });

            # Step Final: Completed
            steps.push({
                highlightLines: ['line-10', 'line-11', 'line-12'],
                status: 'Hoàn thành',
                mode: 'Kết quả',
                result: 'Thành công',
                log: 'Hoàn tất toàn bộ chu trình xử lý dữ liệu. Kết quả sẵn sàng trả về.',
                items: dataList.map((val, idx) => ({ val, state: 'done', idx }))
            });

            this.steps = steps;
        }

        start() {
            if (this.isPlaying) return;
            this.isPlaying = true;
            this.timer = setInterval(() => {
                if (this.currentStep < this.steps.length - 1) {
                    this.step();
                } else {
                    this.pause();
                }
            }, this.speed);
        }

        pause() {
            this.isPlaying = false;
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        }

        step() {
            if (this.currentStep < this.steps.length - 1) {
                this.currentStep++;
                this.render();
            } else {
                this.log('Đã đến bước cuối cùng của tiến trình.');
            }
        }

        scrubStep(e) {
            const barContainer = e.currentTarget;
            if (!barContainer || !this.steps.length) return;
            const rect = barContainer.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const percentage = Math.max(0, Math.min(1, clickX / rect.width));
            const targetStep = Math.floor(percentage * this.steps.length);
            this.currentStep = Math.min(this.steps.length - 1, targetStep);
            this.render();
        }

        setSpeed(val) {
            this.speed = parseInt(val, 10) || 500;
            const disp = document.getElementById('speed-display');
            if (disp) disp.textContent = this.speed;
            if (this.isPlaying) {
                this.pause();
                this.start();
            }
        }

        render() {
            if (!this.steps || !this.steps.length) return;
            const current = this.steps[this.currentStep] || this.steps[0];

            // 1. Update Stepper UI
            const stepProgress = document.getElementById('stepper-progress');
            const stepDesc = document.getElementById('stepper-desc');
            const stepBar = document.getElementById('stepper-bar');

            if (stepProgress) stepProgress.textContent = `Bước ${this.currentStep + 1}/${this.steps.length}`;
            if (stepDesc) stepDesc.textContent = current.log;
            if (stepBar) stepBar.style.width = `${((this.currentStep + 1) / this.steps.length) * 100}%`;

            // 2. Update Realtime Stats
            const statMode = document.getElementById('stat-mode');
            const statLength = document.getElementById('stat-length');
            const statMatch = document.getElementById('stat-match-count');
            const statRes = document.getElementById('stat-result');

            if (statMode) statMode.textContent = current.mode || '-';
            if (statLength) statLength.textContent = (current.items || []).length;
            if (statMatch) statMatch.textContent = this.currentStep;
            if (statRes) {
                statRes.textContent = current.result || 'Đang duyệt';
                statRes.className = current.result === 'Thành công' ? 'text-emerald-400 font-bold' : 'text-amber-400 font-semibold';
            }

            // 3. Highlight Code Tracker Line
            document.querySelectorAll('.code-line').forEach(line => line.classList.remove('active', 'active-line', 'bg-yellow-200'));
            if (current.highlightLines) {
                current.highlightLines.forEach(lineId => {
                    const el = document.getElementById(lineId);
                    if (el) el.classList.add('active', 'active-line');
                });
            }

            // 4. Render Items on Visualizer Canvas
            const canvas = document.getElementById('visualizer-canvas');
            if (canvas && current.items) {
                let itemsMarkup = current.items.map(item => {
                    let borderBgClass = 'border-slate-700 bg-slate-800/90 text-slate-200';
                    if (item.state === 'active') {
                        borderBgClass = 'border-sky-500 bg-sky-900/60 text-sky-200 font-bold scale-105';
                    } else if (item.state === 'comparing') {
                        borderBgClass = 'border-amber-400 bg-amber-500/40 text-amber-200 font-bold animate-pulse scale-110';
                    } else if (item.state === 'done') {
                        borderBgClass = 'border-emerald-500 bg-emerald-600/30 text-emerald-200 font-bold';
                    }

                    return `
                        <div class="flex flex-col items-center transition-all duration-300 transform">
                            <div class="border rounded-lg px-4 py-3 font-mono text-center min-w-[64px] shadow-md transition-all duration-300 ${borderBgClass}">
                                ${item.val}
                            </div>
                            <small class="text-slate-400 font-mono text-xs mt-1.5">[Index ${item.idx}]</small>
                        </div>
                    `;
                }).join('');

                canvas.innerHTML = `
                    <div class="flex flex-wrap gap-3 justify-center items-center p-4 rounded-xl bg-slate-900/90 border border-slate-700/80 w-full min-h-[160px] shadow-inner">
                        ${itemsMarkup}
                    </div>
                `;
            }

            this.log(current.log);
        }
    }

    // Auto-initialize when DOM loaded
    let visualizerApp;
    function initVisualizerApp() {
        if (typeof InteractiveVisualizerEngine !== 'undefined') {
            visualizerApp = new InteractiveVisualizerEngine();
            visualizerApp.init();
        }
    }

    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        initVisualizerApp();
    } else {
        document.addEventListener('DOMContentLoaded', initVisualizerApp);
    }
    </script>
"""

injected_count = 0
for file_path in reading_files:
    if not file_path.is_file():
        continue
    content = file_path.read_text(encoding='utf-8')
    
    # Check if the engine script is stubbed or missing buildExecutionSteps
    if "buildExecutionSteps" in content:
        continue
        
    # Replace stubbed script or inject before </body>
    if "class InteractiveVisualizerEngine {" in content:
        # Replace broken/stubbed engine block with Universal Engine
        content = re.sub(r'<script>\s*class InteractiveVisualizerEngine[\s\S]*?</script>', universal_engine_script, content, flags=re.IGNORECASE)
        file_path.write_text(content, encoding='utf-8')
        injected_count += 1
        print(f"  ✓ Fixed visualizer engine: {file_path.name}")
    elif "</body>" in content:
        content = content.replace("</body>", universal_engine_script + "\n</body>", 1)
        file_path.write_text(content, encoding='utf-8')
        injected_count += 1
        print(f"  ✓ Injected visualizer engine: {file_path.name}")

print(f"\n🎉 Successfully injected Self-Healing Universal Visualizer Engine into {injected_count} reading.html files!")
