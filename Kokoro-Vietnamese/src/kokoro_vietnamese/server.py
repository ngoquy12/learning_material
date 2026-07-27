from __future__ import annotations

import asyncio
import base64
import io
import json
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from kokoro_vietnamese.core import (
    DEFAULT_NORMALIZE_PEAK,
    DEFAULT_VOICE,
    SAMPLE_RATE,
    VOICES,
    KokoroVietnamese,
    list_voices,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    import torch
    if not torch.cuda.is_available():
        num_threads = max(1, (os.cpu_count() or 4) - 1)
        torch.set_num_threads(num_threads)
    try:
        await asyncio.to_thread(get_tts_engine, DEFAULT_VOICE)
    except Exception as exc:
        print(f"Warning during model pre-warming: {exc}")
    yield


app = FastAPI(
    title="Kokoro Vietnamese TTS Server",
    description="High-performance Vietnamese Text-to-Speech REST & Streaming Server",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Phonemes", "X-Sample-Rate", "X-Audio-Format", "Content-Disposition"],
)

# Cache loaded model instances by (engine_type, device, voice)
import torch
_MODELS: Dict[str, Any] = {}
_DEFAULT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_tts_engine(voice: str = DEFAULT_VOICE, device: str = _DEFAULT_DEVICE, engine_type: str = "torch") -> Any:
    cache_key = f"{engine_type}:{device}:{voice}"
    if cache_key not in _MODELS:
        if engine_type.lower() == "onnx":
            from .onnx_cli import KokoroVietnameseONNX
            _MODELS[cache_key] = KokoroVietnameseONNX(device=device, voice=voice)
        else:
            _MODELS[cache_key] = KokoroVietnamese(device=device, voice=voice)
    return _MODELS[cache_key]


class SynthesizeRequest(BaseModel):
    text: str = Field(..., description="Vietnamese text to synthesize")
    voice: str = Field(default=DEFAULT_VOICE, description="Voice identifier")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    normalize_peak: Optional[float] = Field(default=DEFAULT_NORMALIZE_PEAK, description="Peak normalization target")
    engine: Optional[str] = Field(default="torch", description="Inference engine: torch or onnx")


def audio_to_wav_bytes(audio: np.ndarray, sample_rate: int = SAMPLE_RATE) -> bytes:
    buffer = io.BytesIO()
    sf.write(buffer, audio, sample_rate, format="WAV", subtype="PCM_16")
    return buffer.getvalue()


@app.get("/api/v1/voices")
def get_voices():
    """Returns all available Vietnamese voices."""
    result = []
    for key, info in VOICES.items():
        result.append({
            "id": key,
            "label": info["label"],
            "filename": info["filename"],
        })
    return {"voices": result, "default": DEFAULT_VOICE}


@app.post("/api/v1/synthesize")
def synthesize(req: SynthesizeRequest):
    """Synthesizes complete audio for the input text and returns a WAV file."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text parameter cannot be empty.")
    
    try:
        engine = get_tts_engine(voice=req.voice, engine_type=req.engine or "torch")
        audio, phonemes = engine.synthesize(
            req.text,
            speed=req.speed,
            normalize_peak=req.normalize_peak,
        )
        wav_data = audio_to_wav_bytes(audio)
        return Response(
            content=wav_data,
            media_type="audio/wav",
            headers={
                "X-Phonemes": base64.b64encode(phonemes.encode("utf-8")).decode("ascii"),
                "Content-Disposition": 'attachment; filename="kokoro_vietnamese.wav"',
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/v1/synthesize")
def synthesize_get(
    text: str = Query(..., description="Text to synthesize"),
    voice: str = Query(DEFAULT_VOICE, description="Voice name"),
    speed: float = Query(1.0, description="Speed factor"),
    normalize_peak: Optional[float] = Query(DEFAULT_NORMALIZE_PEAK, description="Normalization peak"),
    engine: str = Query("torch", description="Engine type: torch or onnx"),
):
    """GET endpoint to synthesize audio directly as a downloadable WAV file."""
    return synthesize(SynthesizeRequest(text=text, voice=voice, speed=speed, normalize_peak=normalize_peak, engine=engine))


@app.get("/api/v1/stream")
def stream_audio(
    text: str = Query(..., description="Text to synthesize"),
    voice: str = Query(DEFAULT_VOICE, description="Voice name"),
    speed: float = Query(1.0, description="Speed factor"),
    normalize_peak: Optional[float] = Query(DEFAULT_NORMALIZE_PEAK, description="Normalization peak"),
    engine: str = Query("torch", description="Engine type: torch or onnx"),
):
    """HTTP Chunked transfer encoding audio stream (raw 16-bit 24kHz PCM chunks)."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    def audio_generator():
        tts_engine = get_tts_engine(voice=voice, engine_type=engine)
        for chunk_audio, _, _ in tts_engine.synthesize_stream(text, speed=speed, normalize_peak=normalize_peak):
            # Convert float32 array (-1.0 to 1.0) to int16 PCM bytes
            pcm_data = (np.clip(chunk_audio, -1.0, 1.0) * 32767).astype(np.int16).tobytes()
            yield pcm_data

    return StreamingResponse(
        audio_generator(),
        media_type="audio/pcm",
        headers={
            "X-Sample-Rate": str(SAMPLE_RATE),
            "X-Audio-Format": "PCM_16_LE",
        },
    )




def pcm_to_opus_bytes(pcm_int16: np.ndarray, sample_rate: int = SAMPLE_RATE) -> bytes:
    """Encodes 16-bit PCM audio samples to highly compressed OGG/Opus bytes."""
    buffer = io.BytesIO()
    sf.write(buffer, pcm_int16, sample_rate, format="OGG", subtype="OPUS")
    return buffer.getvalue()


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time text-to-speech streaming."""
    await websocket.accept()
    try:
        while True:
            raw_msg = await websocket.receive_text()
            data = json.loads(raw_msg)
            text = data.get("text", "").strip()
            voice = data.get("voice", DEFAULT_VOICE)
            speed = float(data.get("speed", 1.0))
            normalize_peak = data.get("normalize_peak", DEFAULT_NORMALIZE_PEAK)
            engine_type = data.get("engine", "torch")
            audio_format = str(data.get("format", "pcm")).lower()
            binary_mode = bool(data.get("binary", False)) or (audio_format == "opus")

            if not text:
                await websocket.send_json({"type": "error", "message": "Text cannot be empty"})
                continue

            await websocket.send_json({"type": "start", "voice": voice, "sample_rate": SAMPLE_RATE})

            engine = get_tts_engine(voice=voice, engine_type=engine_type)
            loop = asyncio.get_running_loop()

            generator = engine.synthesize_stream(text, speed=speed, normalize_peak=normalize_peak)

            index = 1
            while True:
                # Fetch next chunk incrementally in thread pool so client receives chunk 1 immediately!
                item = await loop.run_in_executor(None, lambda: next(generator, None))
                if item is None:
                    break

                chunk_audio, phonemes, text_chunk = item
                pcm_int16 = (np.clip(chunk_audio, -1.0, 1.0) * 32767).astype(np.int16)

                if audio_format == "opus":
                    # Ultra High-Efficiency OGG/Opus compressed binary stream (~90% bandwidth savings)
                    opus_bytes = pcm_to_opus_bytes(pcm_int16, SAMPLE_RATE)
                    await websocket.send_json({
                        "type": "chunk_info",
                        "index": index,
                        "text_chunk": text_chunk,
                        "phonemes": phonemes,
                        "sample_rate": SAMPLE_RATE,
                        "format": "opus",
                    })
                    await websocket.send_bytes(opus_bytes)
                elif binary_mode:
                    # High-speed Zero-Copy Binary WebSocket Protocol (PCM 16-bit)
                    await websocket.send_json({
                        "type": "chunk_info",
                        "index": index,
                        "text_chunk": text_chunk,
                        "phonemes": phonemes,
                        "sample_rate": SAMPLE_RATE,
                        "format": "pcm",
                    })
                    await websocket.send_bytes(pcm_int16.tobytes())
                else:
                    # Legacy Base64 JSON Protocol
                    audio_b64 = base64.b64encode(pcm_int16.tobytes()).decode("ascii")
                    await websocket.send_json({
                        "type": "chunk",
                        "index": index,
                        "text_chunk": text_chunk,
                        "phonemes": phonemes,
                        "audio_b64": audio_b64,
                        "sample_rate": SAMPLE_RATE,
                        "format": "pcm",
                    })

                index += 1
                await asyncio.sleep(0.001)

            await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        try:
            await websocket.send_json({"type": "error", "message": str(exc)})
        except Exception:
            pass


# Mount demo frontend directory if present
DEMO_DIR = Path(__file__).resolve().parents[2] / "demo"
if DEMO_DIR.exists():
    app.mount("/demo", StaticFiles(directory=str(DEMO_DIR), html=True), name="demo")

    @app.get("/")
    def index():
        return FileResponse(DEMO_DIR / "index.html")


def main():
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="Kokoro Vietnamese TTS Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--device", type=str, default="cuda", help="Device (cuda or cpu)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    global _DEFAULT_DEVICE
    _DEFAULT_DEVICE = args.device

    print(f"Starting Kokoro Vietnamese TTS Server on http://{args.host}:{args.port}")
    uvicorn.run("kokoro_vietnamese.server:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
