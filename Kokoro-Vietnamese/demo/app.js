document.addEventListener("DOMContentLoaded", () => {
  // UI Elements
  const textInput = document.getElementById("text-input");
  const charCounter = document.getElementById("char-counter");
  const presetSelect = document.getElementById("preset-select");
  const voiceSelect = document.getElementById("voice-select");
  const modeSelect = document.getElementById("mode-select");
  const speedRange = document.getElementById("speed-range");
  const speedVal = document.getElementById("speed-val");
  const normalizeToggle = document.getElementById("normalize-toggle");
  const btnSynthesize = document.getElementById("btn-synthesize");
  const btnText = document.getElementById("btn-text");
  const statusBadge = document.getElementById("status-badge");
  const audioStats = document.getElementById("audio-stats");
  const phonemesBox = document.getElementById("phonemes-box");
  const btnCopyPhonemes = document.getElementById("btn-copy-phonemes");
  const btnPlayPause = document.getElementById("btn-play-pause");
  const playIcon = document.getElementById("play-icon");
  const progressFill = document.getElementById("progress-fill");
  const btnDownload = document.getElementById("btn-download");

  // Visualizer Canvas
  const canvas = document.getElementById("visualizer-canvas");
  const canvasCtx = canvas.getContext("2d");
  const visualizerOverlay = document.getElementById("visualizer-overlay");

  // Web Audio API State
  let audioCtx = null;
  let analyser = null;
  let audioQueue = [];
  let isPlaying = false;
  let currentSource = null;
  let startTime = 0;
  let totalDuration = 0;
  let animationFrameId = null;
  let ws = null;

  // Smart Base API URL resolution
  function getApiBase() {
    if (window.location.protocol === "file:") {
      return "http://127.0.0.1:8000";
    }
    if (window.location.port === "8000") {
      return window.location.origin;
    }
    const hostname = window.location.hostname || "127.0.0.1";
    return `http://${hostname}:8000`;
  }

  let API_BASE = getApiBase();
  let WS_BASE = API_BASE.replace(/^http/, "ws");

  // 1. Fetch Voices
  async function loadVoices() {
    try {
      const res = await fetch(`${API_BASE}/api/v1/voices`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      voiceSelect.innerHTML = "";
      data.voices.forEach((v) => {
        const opt = document.createElement("option");
        opt.value = v.id;
        opt.textContent = `${v.label} (${v.id})`;
        if (v.id === data.default) opt.selected = true;
        voiceSelect.appendChild(opt);
      });
      updateStatus("Sẵn sàng", "var(--success)");
    } catch (e) {
      console.warn(`Could not connect to FastAPI backend at ${API_BASE}:`, e);
      updateStatus(`Chưa kết nối Server (${API_BASE})`, "var(--warning)");
      // Fallback default voice option if server is not yet started
      voiceSelect.innerHTML =
        '<option value="diem_trinh">Diễm Trinh (Default)</option>';
    }
  }
  loadVoices();

  // 2. UI Event Listeners
  textInput.addEventListener("input", () => {
    charCounter.textContent = textInput.value.length;
  });

  presetSelect.addEventListener("change", () => {
    if (presetSelect.value) {
      textInput.value = presetSelect.value;
      charCounter.textContent = textInput.value.length;
    }
  });

  speedRange.addEventListener("input", () => {
    speedVal.textContent = `${parseFloat(speedRange.value).toFixed(1)}x`;
  });

  btnCopyPhonemes.addEventListener("click", () => {
    const text = phonemesBox.innerText;
    if (text && !text.includes("Các token âm vị")) {
      navigator.clipboard.writeText(text);
      btnCopyPhonemes.textContent = "Đã chép!";
      setTimeout(() => (btnCopyPhonemes.textContent = "Sao chép"), 2000);
    }
  });

  // 3. Web Audio API Init
  function initAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext({ sampleRate: 24000 });
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 128;
      analyser.connect(audioCtx.destination);
      setupVisualizer();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
  }

  // 4. Visualizer Rendering
  function setupVisualizer() {
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
      animationFrameId = requestAnimationFrame(draw);
      analyser.getByteFrequencyData(dataArray);

      const width = (canvas.width = canvas.parentElement.clientWidth);
      const height = (canvas.height = canvas.parentElement.clientHeight);

      canvasCtx.clearRect(0, 0, width, height);

      const barWidth = (width / bufferLength) * 2.2;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * height * 0.85;

        const gradient = canvasCtx.createLinearGradient(
          0,
          height,
          0,
          height - barHeight,
        );
        gradient.addColorStop(0, "#6366f1");
        gradient.addColorStop(1, "#c084fc");

        canvasCtx.fillStyle = gradient;
        canvasCtx.fillRect(x, height - barHeight, barWidth - 2, barHeight);

        x += barWidth;
      }
    }
    draw();
  }

  // 5. Audio Queue & Playback Management
  let nextStartTime = 0;
  let accumulatedPcm = [];

  function playAudioChunk(pcmBuffer, sampleRate = 24000) {
    initAudioContext();
    visualizerOverlay.style.display = "none";
    accumulatedPcm.push(pcmBuffer);

    const audioBuffer = audioCtx.createBuffer(1, pcmBuffer.length, sampleRate);
    const channelData = audioBuffer.getChannelData(0);
    for (let i = 0; i < pcmBuffer.length; i++) {
      channelData[i] = pcmBuffer[i] / 32768.0;
    }

    const source = audioCtx.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(analyser);

    const currentTime = audioCtx.currentTime;
    if (nextStartTime < currentTime) {
      nextStartTime = currentTime + 0.05; // 50ms buffer lag protection
    }

    source.start(nextStartTime);
    nextStartTime += audioBuffer.duration;
    totalDuration += audioBuffer.duration;

    audioStats.textContent = `${totalDuration.toFixed(1)}s / 24kHz`;
    btnPlayPause.disabled = false;
    playIcon.innerHTML =
      '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
  }

  function createWavBlob(pcmChunks, sampleRate = 24000) {
    let totalSamples = 0;
    for (const chunk of pcmChunks) totalSamples += chunk.length;

    const buffer = new ArrayBuffer(44 + totalSamples * 2);
    const view = new DataView(buffer);

    function writeString(v, offset, str) {
      for (let i = 0; i < str.length; i++) v.setUint8(offset + i, str.charCodeAt(i));
    }

    writeString(view, 0, "RIFF");
    view.setUint32(4, 36 + totalSamples * 2, true);
    writeString(view, 8, "WAVE");
    writeString(view, 12, "fmt ");
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(view, 36, "data");
    view.setUint32(40, totalSamples * 2, true);

    let offset = 44;
    for (const chunk of pcmChunks) {
      for (let i = 0; i < chunk.length; i++) {
        view.setInt16(offset, chunk[i], true);
        offset += 2;
      }
    }

    return new Blob([buffer], { type: "audio/wav" });
  }

  // 6. Synthesis Handling & Shortcuts
  textInput.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      btnSynthesize.click();
    }
  });

  phonemesBox.title = "Nhấp để sao chép danh sách âm vị";
  phonemesBox.addEventListener("click", () => {
    const text = phonemesBox.innerText.trim();
    if (text) {
      navigator.clipboard.writeText(text).then(() => {
        updateStatus("Đã sao chép âm vị!", "var(--accent-primary)");
        setTimeout(() => updateStatus("Sẵn sàng", "var(--success)"), 2000);
      });
    }
  });

  btnSynthesize.addEventListener("click", () => {
    const text = textInput.value.trim();
    if (!text) {
      alert("Vui lòng nhập văn bản tiếng Việt.");
      return;
    }

    initAudioContext();
    resetPlaybackState();

    const mode = modeSelect.value;
    const voice = voiceSelect.value;
    const speed = parseFloat(speedRange.value);
    const normalizePeak = normalizeToggle.checked ? 0.95 : null;

    updateStatus("Đang tạo...", "var(--warning)");
    btnSynthesize.classList.add("loading");
    btnText.textContent = "Đang xử lý...";
    phonemesBox.innerHTML = "";

    if (mode === "websocket") {
      synthesizeWebSocket(text, voice, speed, normalizePeak);
    } else if (mode === "http_stream") {
      synthesizeHTTPStream(text, voice, speed, normalizePeak);
    } else {
      synthesizeFullAudio(text, voice, speed, normalizePeak);
    }
  });

  function resetPlaybackState() {
    if (ws) {
      ws.close();
      ws = null;
    }
    nextStartTime = 0;
    totalDuration = 0;
    accumulatedPcm = [];
    progressFill.style.width = "0%";
    audioStats.textContent = "0.0s / 24kHz";
    btnDownload.removeAttribute("href");
  }

  function updateStatus(msg, color = "var(--success)") {
    statusBadge.style.color = color;
    statusBadge.innerHTML = `<span class="status-dot" style="background-color:${color}; box-shadow:0 0 8px ${color}"></span> ${msg}`;
  }

  function finishProcessing() {
    btnSynthesize.classList.remove("loading");
    btnText.textContent = "Bắt đầu tạo giọng nói";
    updateStatus("Sẵn sàng", "var(--success)");

    if (accumulatedPcm.length > 0) {
      const blob = createWavBlob(accumulatedPcm, 24000);
      btnDownload.href = URL.createObjectURL(blob);
      btnDownload.download = `kokoro_vi_${Date.now()}.wav`;
    }
  }

  // A. WebSocket Streaming (High-Speed Binary Protocol)
  function synthesizeWebSocket(text, voice, speed, normalizePeak) {
    ws = new WebSocket(`${WS_BASE}/ws/stream`);
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
      ws.send(
        JSON.stringify({
          text: text,
          voice: voice,
          speed: speed,
          normalize_peak: normalizePeak,
          binary: true,
        }),
      );
    };

    ws.onmessage = (event) => {
      if (typeof event.data === "string") {
        const msg = JSON.parse(event.data);
        if (msg.type === "start") {
          updateStatus("Binary Streaming...", "var(--accent-primary)");
        } else if (msg.type === "chunk_info") {
          // Append phonemes to log
          const p = document.createElement("div");
          p.textContent = `${msg.phonemes} (${msg.text_chunk})`;
          phonemesBox.appendChild(p);
          phonemesBox.scrollTop = phonemesBox.scrollHeight;
        } else if (msg.type === "chunk") {
          // Fallback legacy Base64 decode
          const binaryStr = atob(msg.audio_b64);
          const bytes = new Uint8Array(binaryStr.length);
          for (let i = 0; i < binaryStr.length; i++) {
            bytes[i] = binaryStr.charCodeAt(i);
          }
          const pcm16 = new Int16Array(bytes.buffer);
          playAudioChunk(pcm16, msg.sample_rate);
        } else if (msg.type === "done") {
          finishProcessing();
        } else if (msg.type === "error") {
          alert(`Lỗi tổng hợp: ${msg.message}`);
          finishProcessing();
        }
      } else if (event.data instanceof ArrayBuffer) {
        // Direct Zero-Copy Binary ArrayBuffer PCM 16-bit
        const pcm16 = new Int16Array(event.data);
        playAudioChunk(pcm16, 24000);
      }
    };

    ws.onerror = (err) => {
      console.error("WebSocket Error:", err);
      alert("Không thể kết nối đến WebSocket Server.");
      finishProcessing();
    };
  }

  // B. HTTP Chunked Streaming
  async function synthesizeHTTPStream(text, voice, speed, normalizePeak) {
    try {
      const url = new URL(`${API_BASE}/api/v1/stream`);
      url.searchParams.set("text", text);
      url.searchParams.set("voice", voice);
      url.searchParams.set("speed", speed);
      if (normalizePeak) url.searchParams.set("normalize_peak", normalizePeak);

      const res = await fetch(url.toString());
      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);

      const reader = res.body.getReader();
      updateStatus("HTTP Streaming...", "var(--accent-primary)");

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (value) {
          const pcm16 = new Int16Array(
            value.buffer,
            value.byteOffset,
            value.byteLength / 2,
          );
          playAudioChunk(pcm16, 24000);
        }
      }
      phonemesBox.innerHTML = "<i>(HTTP Stream Chunked Mode)</i>";
      finishProcessing();
    } catch (e) {
      alert(`Lỗi HTTP Streaming: ${e.message}`);
      finishProcessing();
    }
  }

  // C. Full Audio Download Synthesis
  async function synthesizeFullAudio(text, voice, speed, normalizePeak) {
    try {
      const res = await fetch(`${API_BASE}/api/v1/synthesize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          voice: voice,
          speed: speed,
          normalize_peak: normalizePeak,
        }),
      });

      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);

      const phonemesB64 = res.headers.get("X-Phonemes");
      if (phonemesB64) {
        phonemesBox.textContent = atob(phonemesB64);
      }

      const blob = await res.blob();
      const arrayBuffer = await blob.arrayBuffer();
      const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

      // Set Download Link
      btnDownload.href = URL.createObjectURL(blob);

      const source = audioCtx.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(analyser);
      source.start();

      visualizerOverlay.style.display = "none";
      btnPlayPause.disabled = false;
      playIcon.innerHTML =
        '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
      audioStats.textContent = `${audioBuffer.duration.toFixed(1)}s / 24kHz`;

      finishProcessing();
    } catch (e) {
      alert(`Lỗi tổng hợp audio: ${e.message}`);
      finishProcessing();
    }
  }
});
