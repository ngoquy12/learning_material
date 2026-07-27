from __future__ import annotations

import time
from pathlib import Path
import numpy as np
import soundfile as sf
import gradio as gr

from kokoro_vietnamese.core import (
    DEFAULT_NORMALIZE_PEAK,
    DEFAULT_VOICE,
    SAMPLE_RATE,
    VOICES,
    KokoroVietnamese,
    list_voices,
)
from kokoro_vietnamese.text_norm import normalize_vietnamese_text
from kokoro_vietnamese.server import get_tts_engine

SAMPLE_TEXTS = [
    "Hôm nay 21/07/2026, tôi vừa học xong khóa học AI và API trị giá 100k USD.",
    "Trụ sở công ty nằm ở TP.HCM với tổng doanh thu đạt 2.5 tỷ VNĐ trong năm 2025.",
    "Xin chào! Đây là mô hình tổng hợp tiếng nói tiếng Việt Kokoro-Vietnamese siêu tự nhiên.",
    "PGS.TS Nguyễn Văn A sẽ chủ trì hội thảo CNTT vào ngày 15/08/2026 tại Hà Nội.",
]


def gradio_synthesize(
    text: str,
    voice_id: str,
    speed: float,
    normalize_peak: bool,
    engine_type: str,
):
    if not text.strip():
        return None, "", "", "Vui lòng nhập văn bản tiếng Việt."

    start_time = time.time()

    # Step 1: Text Normalization
    normalized_text = normalize_vietnamese_text(text)

    # Step 2: Inference
    peak = 0.95 if normalize_peak else None
    engine = get_tts_engine(voice=voice_id, engine_type=engine_type)
    audio, phonemes = engine.synthesize(normalized_text, speed=speed, normalize_peak=peak)

    duration = time.time() - start_time
    audio_length_sec = len(audio) / SAMPLE_RATE
    rtf = duration / max(audio_length_sec, 0.01)

    stats_msg = f"⏱️ Thời gian xử lý: {duration:.2f}s | 🔊 Thời lượng Audio: {audio_length_sec:.2f}s | ⚡ RTF: {rtf:.3f}x ({engine_type.upper()})"

    return (SAMPLE_RATE, audio), normalized_text, phonemes, stats_msg


def build_app() -> gr.Blocks:
    voice_choices = [(f"{info['label']} ({k})", k) for k, info in VOICES.items()]

    with gr.Blocks(title="Kokoro Vietnamese TTS Studio") as app:
        gr.Markdown(
            """
            # 🇻🇳 Kokoro-Vietnamese TTS Studio
            **Mô hình Tổng Hợp Tiếng Nói Tiếng Việt Siêu Tự Nhiên & Nhanh Nhất (PyTorch & ONNX Runtime)**
            *Tích hợp Chuẩn hóa văn bản Tiếng Việt tự động (Số, Ngày tháng, Tiền tệ, Thuật ngữ CNTT & AI)*
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                text_input = gr.Textbox(
                    label="Văn bản đầu vào (Tiếng Việt)",
                    placeholder="Nhập văn bản tiếng Việt cần đọc...",
                    lines=4,
                    value=SAMPLE_TEXTS[0],
                )

                gr.Examples(
                    examples=SAMPLE_TEXTS,
                    inputs=text_input,
                    label="Văn bản mẫu thử nghiệm",
                )

                voice_dropdown = gr.Dropdown(
                    choices=voice_choices,
                    value=DEFAULT_VOICE,
                    label="Giọng đọc (Voicepack)",
                )

                with gr.Row():
                    speed_slider = gr.Slider(
                        minimum=0.5,
                        maximum=2.0,
                        step=0.1,
                        value=1.0,
                        label="Tốc độ đọc (Speed)",
                    )
                    engine_radio = gr.Radio(
                        choices=[("PyTorch (CUDA/CPU)", "torch"), ("ONNX Runtime (Siêu nhẹ)", "onnx")],
                        value="torch",
                        label="Inference Engine",
                    )

                normalize_cb = gr.Checkbox(
                    value=True,
                    label="Peak Normalization (0.95)",
                )

                btn_generate = gr.Button("▶ Bắt đầu tổng hợp giọng nói", variant="primary", size="lg")

            with gr.Column(scale=1):
                audio_output = gr.Audio(
                    label="Kết quả Audio (24kHz WAV)",
                    type="numpy",
                    autoplay=True,
                )
                stats_output = gr.Markdown(value="*Nhấn Bắt đầu để tổng hợp giọng nói*")

                with gr.Accordion("Văn bản đã qua Chuẩn hóa (Text Normalization)", open=True):
                    normalized_output = gr.Textbox(
                        label="Văn bản chuẩn hóa",
                        interactive=False,
                        lines=2,
                    )

                with gr.Accordion("Danh sách Âm vị (G2P Phonemes Log)", open=False):
                    phonemes_output = gr.Textbox(
                        label="Phonemes",
                        interactive=False,
                        lines=4,
                    )

        btn_generate.click(
            fn=gradio_synthesize,
            inputs=[text_input, voice_dropdown, speed_slider, normalize_cb, engine_radio],
            outputs=[audio_output, normalized_output, phonemes_output, stats_output],
        )

    return app


if __name__ == "__main__":
    demo = build_app()
    demo.launch(server_name="0.0.0.0", server_port=7865, theme=gr.themes.Soft(), share=False)
