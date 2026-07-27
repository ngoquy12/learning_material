#!/usr/bin/env python3
"""
Kokoro Vietnamese: Optimized Voice Cloning via Embedding Transfer
=================================================================
Creates a high-quality voicepack by finding the optimal blend of existing
trained voicepacks that best matches a target speaker's mel-spectrogram
characteristics.

This does NOT require a training checkpoint or CUDA GPU.
It works by leveraging the pre-trained voicepacks' embedding space.

Usage:
    python scripts/clone_voice_optimized.py \
        --audio "voice_example/speaker.mp3" \
        --output voicepacks/new_voice.pt \
        --name "New Voice"

    # With specific reference voices only
    python scripts/clone_voice_optimized.py \
        --audio "voice_example/speaker.mp3" \
        --output voicepacks/new_voice.pt \
        --ref-voices thanh_dat manh_dung phat_tai
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf
import torch
import torch.nn.functional as F


# ── Constants matching StyleTTS2 training pipeline ───────────────────────
SAMPLE_RATE = 24000
MEL_N_FFT = 2048
MEL_WIN_LENGTH = 1200
MEL_HOP_LENGTH = 300
MEL_N_MELS = 80
MEL_MEAN = -4.0
MEL_STD = 4.0


def _build_mel_filterbank(
    sr: int = SAMPLE_RATE,
    n_fft: int = MEL_N_FFT,
    n_mels: int = MEL_N_MELS,
    fmin: float = 0.0,
    fmax: float = None,
) -> torch.Tensor:
    """Build mel filterbank matrix (matches librosa/torchaudio output)."""
    if fmax is None:
        fmax = sr / 2.0
    n_freqs = 1 + n_fft // 2

    # Hz to mel
    def hz_to_mel(f):
        return 2595.0 * np.log10(1.0 + f / 700.0)

    def mel_to_hz(m):
        return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

    mel_min = hz_to_mel(fmin)
    mel_max = hz_to_mel(fmax)
    mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
    hz_points = mel_to_hz(mel_points)
    bin_points = np.floor((n_fft + 1) * hz_points / sr).astype(int)

    weights = np.zeros((n_mels, n_freqs), dtype=np.float32)
    for i in range(n_mels):
        b_start, b_center, b_end = bin_points[i], bin_points[i + 1], bin_points[i + 2]
        for j in range(b_start, b_center):
            if j < n_freqs:
                weights[i, j] = (j - b_start) / max(b_center - b_start, 1)
        for j in range(b_center, b_end):
            if j < n_freqs:
                weights[i, j] = (b_end - j) / max(b_end - b_center, 1)
    return torch.from_numpy(weights)


class MelSpectrogram:
    """Native PyTorch mel spectrogram matching torchaudio/StyleTTS2 training."""
    def __init__(self, device: str = "cpu"):
        self.device = device
        self.mel_basis = _build_mel_filterbank().to(device)
        self.window = torch.hann_window(MEL_WIN_LENGTH).to(device)

    def __call__(self, waveform: torch.Tensor) -> torch.Tensor:
        waveform = waveform.to(self.device)
        stft = torch.stft(
            waveform.squeeze(0) if waveform.ndim > 1 else waveform,
            n_fft=MEL_N_FFT,
            hop_length=MEL_HOP_LENGTH,
            win_length=MEL_WIN_LENGTH,
            window=self.window,
            return_complex=True,
        )
        magnitudes = torch.abs(stft)  # [n_freqs, T]
        if magnitudes.ndim == 3:
            magnitudes = magnitudes.squeeze(0)
        mel = torch.matmul(self.mel_basis, magnitudes)  # [n_mels, T]
        return mel.unsqueeze(0)  # [1, n_mels, T]


def build_mel_transform(device: str = "cpu"):
    """Build mel spectrogram transform matching StyleTTS2 training exactly."""
    return MelSpectrogram(device=device)


def compute_normalized_mel(waveform: torch.Tensor, mel_transform) -> torch.Tensor:
    """Compute log-mel spectrogram with StyleTTS2 normalization."""
    mel = mel_transform(waveform)  # [1, 80, T]
    mel = (torch.log(1e-5 + mel) - MEL_MEAN) / MEL_STD
    return mel


# ── Audio Preprocessing ─────────────────────────────────────────────────


def load_and_preprocess_audio(
    audio_path: str,
    target_sr: int = SAMPLE_RATE,
) -> np.ndarray:
    """Load audio file, convert to mono float32 at target sample rate."""
    print(f"Loading audio: {audio_path}")
    data, sr = sf.read(audio_path, dtype="float32")

    # Convert stereo to mono
    if data.ndim > 1:
        data = data.mean(axis=1)
        print(f"  Converted stereo -> mono")

    # Resample if needed
    if sr != target_sr:
        from scipy.signal import resample_poly
        from math import gcd
        g = gcd(sr, target_sr)
        up, down = target_sr // g, sr // g
        data = resample_poly(data, up, down).astype(np.float32)
        print(f"  Resampled {sr}Hz -> {target_sr}Hz")

    duration_sec = len(data) / target_sr
    print(f"  Duration: {duration_sec:.1f}s, Samples: {len(data):,}")
    return data


def extract_speech_segments(
    audio: np.ndarray,
    sr: int = SAMPLE_RATE,
    segment_duration_sec: float = 5.0,
    min_rms: float = 0.015,
    max_segments: int = 30,
) -> list[np.ndarray]:
    """Extract clean speech segments, filtering out silence."""
    segment_samples = int(segment_duration_sec * sr)
    segments = []

    # Use overlapping windows for better coverage
    step = segment_samples // 2

    for start in range(0, len(audio) - segment_samples, step):
        chunk = audio[start : start + segment_samples]
        rms = np.sqrt(np.mean(chunk ** 2))

        if rms > min_rms:
            # Additional check: peak amplitude should indicate speech
            peak = np.max(np.abs(chunk))
            if peak > 0.05:
                segments.append(chunk)
                if len(segments) >= max_segments:
                    break

    print(f"  Extracted {len(segments)} speech segments ({segment_duration_sec}s each)")
    return segments


# ── Mel Feature Statistics ───────────────────────────────────────────────


def compute_mel_statistics(
    segments: list[np.ndarray],
    mel_transform,
    device: str = "cpu",
) -> dict:
    """Compute comprehensive mel-spectrogram statistics for a speaker."""
    all_mel_means = []
    all_mel_stds = []
    all_mel_energy = []

    with torch.no_grad():
        for seg in segments:
            waveform = torch.from_numpy(seg).unsqueeze(0).to(device)
            mel = compute_normalized_mel(waveform, mel_transform)  # [1, 80, T]

            # Per-band statistics
            mel_np = mel.squeeze(0).cpu().numpy()  # [80, T]
            all_mel_means.append(mel_np.mean(axis=1))  # [80]
            all_mel_stds.append(mel_np.std(axis=1))    # [80]
            all_mel_energy.append(mel_np.mean())         # scalar

    stats = {
        "mel_mean_profile": np.stack(all_mel_means).mean(axis=0),  # [80] - average spectral shape
        "mel_std_profile": np.stack(all_mel_stds).mean(axis=0),    # [80] - spectral variation
        "mel_energy": np.mean(all_mel_energy),                      # scalar
        "n_segments": len(segments),
    }
    return stats


def compute_mel_distance(stats_a: dict, stats_b: dict) -> float:
    """Compute weighted distance between two mel statistic profiles."""
    # Spectral shape distance (most important for timbre)
    mean_dist = np.sqrt(np.mean((stats_a["mel_mean_profile"] - stats_b["mel_mean_profile"]) ** 2))

    # Spectral variation distance (prosody/dynamics)
    std_dist = np.sqrt(np.mean((stats_a["mel_std_profile"] - stats_b["mel_std_profile"]) ** 2))

    # Energy distance
    energy_dist = abs(stats_a["mel_energy"] - stats_b["mel_energy"])

    # Weighted combination
    return 0.6 * mean_dist + 0.3 * std_dist + 0.1 * energy_dist


# ── Reference Voicepack Analysis ────────────────────────────────────────


def get_male_voice_ids() -> list[str]:
    """Return voice IDs likely to be male voices."""
    return [
        "thanh_dat",    # Thành Đạt
        "manh_dung",    # Mạnh Dũng
        "phat_tai",     # Phát Tài
        "hung_thinh",   # Hưng Thịnh
        "tuan_ngoc",    # Tuấn Ngọc
        "duc_an",       # Đức An
        "duc_duy",      # đức duy
    ]


def download_reference_voicepack(voice_id: str) -> torch.Tensor:
    """Download a voicepack from HuggingFace."""
    from huggingface_hub import hf_hub_download

    local_path = Path(f"voicepacks/{voice_id}.pt")
    if local_path.exists():
        return torch.load(str(local_path), map_location="cpu", weights_only=True)

    path = hf_hub_download(
        repo_id="contextboxai/Kokoro-Vietnamese",
        filename=f"voicepacks/{voice_id}.pt",
    )
    return torch.load(path, map_location="cpu", weights_only=True)


def synthesize_with_voicepack(
    voicepack: torch.Tensor,
    text: str,
    device: str = "cpu",
) -> np.ndarray:
    """Synthesize audio using a voicepack to compute its mel characteristics."""
    from kokoro_vietnamese.core import KokoroVietnamese, phonemize

    # Load model (cached after first call)
    if not hasattr(synthesize_with_voicepack, "_model"):
        synthesize_with_voicepack._model = KokoroVietnamese(device=device)
        synthesize_with_voicepack._model.voicepack = voicepack

    model = synthesize_with_voicepack._model
    model.voicepack = voicepack

    ps = phonemize(text)
    if not ps:
        return np.array([], dtype=np.float32)

    with torch.no_grad():
        ref_s = voicepack[len(ps) - 1]
        audio = model.model(ps, ref_s, 1.0)

    return audio.detach().cpu().numpy()


# ── Optimization ─────────────────────────────────────────────────────────


def find_optimal_blend(
    target_stats: dict,
    ref_voicepacks: dict[str, torch.Tensor],
    ref_stats: dict[str, dict],
    device: str = "cpu",
) -> tuple[torch.Tensor, dict[str, float]]:
    """Find optimal weighted blend of reference voicepacks."""
    voice_ids = list(ref_voicepacks.keys())
    n_voices = len(voice_ids)

    print(f"\n{'='*60}")
    print(f"  OPTIMIZING VOICEPACK BLEND")
    print(f"{'='*60}")

    # Step 1: Compute individual distances
    distances = {}
    for vid in voice_ids:
        dist = compute_mel_distance(target_stats, ref_stats[vid])
        distances[vid] = dist
        print(f"  {vid:15s} → mel distance: {dist:.4f}")

    # Step 2: Convert distances to similarity weights (inverse distance)
    # Smaller distance = higher weight
    epsilon = 1e-8
    inv_distances = {vid: 1.0 / (dist + epsilon) for vid, dist in distances.items()}
    total_inv = sum(inv_distances.values())
    raw_weights = {vid: w / total_inv for vid, w in inv_distances.items()}

    # Step 3: Refine weights via grid search
    # Test many weight combinations to find the best blend
    best_weights = raw_weights.copy()
    best_distance = float("inf")

    print(f"\n  Running optimization grid search...")

    # Sort voices by distance (closest first)
    sorted_voices = sorted(distances.items(), key=lambda x: x[1])

    # Focus on top-3 closest voices for efficiency
    top_voices = [v[0] for v in sorted_voices[:min(4, n_voices)]]

    # Grid search over weight combinations for top voices
    grid_steps = 11  # 0.0, 0.1, ..., 1.0
    best_combo = None

    if len(top_voices) == 1:
        best_weights = {top_voices[0]: 1.0}
        best_combo = (1.0,)
    elif len(top_voices) == 2:
        for w0 in range(grid_steps):
            w0_f = w0 / (grid_steps - 1)
            w1_f = 1.0 - w0_f
            weights = {top_voices[0]: w0_f, top_voices[1]: w1_f}
            blended_stats = blend_mel_stats(ref_stats, weights)
            dist = compute_mel_distance(target_stats, blended_stats)
            if dist < best_distance:
                best_distance = dist
                best_combo = (w0_f, w1_f)
                best_weights = weights.copy()
    elif len(top_voices) >= 3:
        for w0 in range(grid_steps):
            w0_f = w0 / (grid_steps - 1)
            remaining = 1.0 - w0_f
            if remaining < 0:
                continue
            for w1 in range(grid_steps):
                w1_f = (w1 / (grid_steps - 1)) * remaining
                w2_f = remaining - w1_f
                if w2_f < 0:
                    continue

                weights = {
                    top_voices[0]: w0_f,
                    top_voices[1]: w1_f,
                    top_voices[2]: w2_f,
                }
                # Add remaining voices with weight 0
                if len(top_voices) > 3:
                    for v in top_voices[3:]:
                        weights[v] = 0.0

                blended_stats = blend_mel_stats(ref_stats, weights)
                dist = compute_mel_distance(target_stats, blended_stats)
                if dist < best_distance:
                    best_distance = dist
                    best_combo = tuple(weights[v] for v in top_voices)
                    best_weights = weights.copy()

    print(f"\n  ✅ Optimal blend found (mel distance: {best_distance:.4f}):")
    for vid in sorted(best_weights.keys(), key=lambda v: best_weights[v], reverse=True):
        w = best_weights[vid]
        if w > 0.001:
            print(f"     {vid:15s}: {w:.1%}")

    # Step 4: Build blended voicepack
    blended = torch.zeros(510, 1, 256)
    for vid, weight in best_weights.items():
        if weight > 0.001:
            blended += weight * ref_voicepacks[vid]

    return blended, best_weights


def blend_mel_stats(
    ref_stats: dict[str, dict], weights: dict[str, float]
) -> dict:
    """Blend mel statistics from multiple references."""
    blended_mean = np.zeros(MEL_N_MELS)
    blended_std = np.zeros(MEL_N_MELS)
    blended_energy = 0.0
    total_weight = 0.0

    for vid, weight in weights.items():
        if weight < 0.001 or vid not in ref_stats:
            continue
        blended_mean += weight * ref_stats[vid]["mel_mean_profile"]
        blended_std += weight * ref_stats[vid]["mel_std_profile"]
        blended_energy += weight * ref_stats[vid]["mel_energy"]
        total_weight += weight

    if total_weight > 0:
        blended_mean /= total_weight
        blended_std /= total_weight
        blended_energy /= total_weight

    return {
        "mel_mean_profile": blended_mean,
        "mel_std_profile": blended_std,
        "mel_energy": blended_energy,
    }


def refine_per_dimension(
    blended_voicepack: torch.Tensor,
    ref_voicepacks: dict[str, torch.Tensor],
    target_stats: dict,
    ref_stats: dict[str, dict],
    blend_weights: dict[str, float],
) -> torch.Tensor:
    """
    Per-dimension refinement of the voicepack embedding.

    Adjusts acoustic (first 128 dims) and prosodic (last 128 dims) separately
    based on the closest reference for each characteristic.
    """
    print(f"\n  Refining per-dimension (acoustic + prosodic)...")

    # Find best acoustic match and best prosodic match separately
    voice_ids = list(ref_voicepacks.keys())

    # Acoustic distance: emphasize mel_mean_profile (spectral shape = timbre)
    acoustic_distances = {}
    for vid in voice_ids:
        dist = np.sqrt(np.mean(
            (target_stats["mel_mean_profile"] - ref_stats[vid]["mel_mean_profile"]) ** 2
        ))
        acoustic_distances[vid] = dist

    # Prosodic distance: emphasize mel_std_profile (variation = dynamics/prosody)
    prosodic_distances = {}
    for vid in voice_ids:
        dist = np.sqrt(np.mean(
            (target_stats["mel_std_profile"] - ref_stats[vid]["mel_std_profile"]) ** 2
        ))
        prosodic_distances[vid] = dist

    best_acoustic = min(acoustic_distances, key=acoustic_distances.get)
    best_prosodic = min(prosodic_distances, key=prosodic_distances.get)

    print(f"    Best acoustic match (timbre):  {best_acoustic} (dist={acoustic_distances[best_acoustic]:.4f})")
    print(f"    Best prosodic match (rhythm):  {best_prosodic} (dist={prosodic_distances[best_prosodic]:.4f})")

    # Build refined voicepack
    refined = blended_voicepack.clone()
    base_vec = refined[0, 0, :]  # [256]

    # Increase weight of best acoustic match in first 128 dims
    acoustic_ref = ref_voicepacks[best_acoustic][0, 0, :128]
    current_acoustic = base_vec[:128]
    # Blend: 70% current optimal blend + 30% best acoustic match
    refined_acoustic = 0.7 * current_acoustic + 0.3 * acoustic_ref

    # Increase weight of best prosodic match in last 128 dims
    prosodic_ref = ref_voicepacks[best_prosodic][0, 0, 128:]
    current_prosodic = base_vec[128:]
    # Blend: 70% current optimal blend + 30% best prosodic match
    refined_prosodic = 0.7 * current_prosodic + 0.3 * prosodic_ref

    refined_vec = torch.cat([refined_acoustic, refined_prosodic], dim=0)

    # Normalize to match reference voicepack norms
    ref_norms = []
    for vid, vp in ref_voicepacks.items():
        ref_norms.append(vp[0, 0, :].norm().item())
    target_norm = np.mean(ref_norms)
    current_norm = refined_vec.norm().item()
    if current_norm > 0:
        refined_vec = refined_vec * (target_norm / current_norm)

    # Expand to full voicepack shape [510, 1, 256]
    refined = refined_vec.unsqueeze(0).unsqueeze(0).expand(510, 1, 256).clone()

    print(f"    Final voicepack norm: {refined[0,0,:].norm().item():.4f} (target: {target_norm:.4f})")
    print(f"    Acoustic norm: {refined[0,0,:128].norm().item():.4f}")
    print(f"    Prosodic norm: {refined[0,0,128:].norm().item():.4f}")

    return refined


# ── Reference voice mel profiling ────────────────────────────────────────


TEST_SENTENCES = [
    "Hôm nay trời trong xanh, gió thổi nhẹ qua hiên nhà.",
    "Chào các bạn, hôm nay chúng ta sẽ tìm hiểu về React Hooks.",
    "Đây là một ví dụ minh họa cách sử dụng useReducer trong dự án thực tế.",
    "Trước khi bắt đầu, các bạn cần cài đặt Node.js phiên bản mới nhất.",
    "Kết quả cuối cùng cho thấy hiệu suất tăng đáng kể so với phiên bản trước.",
]


def profile_voicepack_mel(
    voicepack: torch.Tensor,
    mel_transform,
    device: str = "cpu",
) -> dict:
    """Profile a voicepack by synthesizing test sentences and analyzing mel."""
    all_mel_means = []
    all_mel_stds = []
    all_mel_energy = []

    from kokoro_vietnamese.core import KokoroVietnamese, phonemize

    # Load model once
    if not hasattr(profile_voicepack_mel, "_model"):
        print("  Loading Kokoro model for profiling...")
        profile_voicepack_mel._model = KokoroVietnamese(device=device)

    model = profile_voicepack_mel._model
    model.voicepack = voicepack

    with torch.no_grad():
        for sentence in TEST_SENTENCES:
            ps = phonemize(sentence)
            if not ps or len(ps) > 510:
                continue

            ref_s = voicepack[len(ps) - 1]
            audio = model.model(ps, ref_s, 1.0)
            audio_np = audio.detach().cpu().numpy()

            if len(audio_np) < MEL_HOP_LENGTH * 10:
                continue

            waveform = torch.from_numpy(audio_np).unsqueeze(0).to(device)
            mel = compute_normalized_mel(waveform, mel_transform)
            mel_np = mel.squeeze(0).cpu().numpy()

            all_mel_means.append(mel_np.mean(axis=1))
            all_mel_stds.append(mel_np.std(axis=1))
            all_mel_energy.append(mel_np.mean())

    if not all_mel_means:
        return {
            "mel_mean_profile": np.zeros(MEL_N_MELS),
            "mel_std_profile": np.zeros(MEL_N_MELS),
            "mel_energy": 0.0,
            "n_segments": 0,
        }

    return {
        "mel_mean_profile": np.stack(all_mel_means).mean(axis=0),
        "mel_std_profile": np.stack(all_mel_stds).mean(axis=0),
        "mel_energy": np.mean(all_mel_energy),
        "n_segments": len(all_mel_means),
    }


# ── Main Pipeline ───────────────────────────────────────────────────────


def clone_voice_optimized(
    audio_path: str,
    output_path: str,
    voice_name: str = "Cloned Voice",
    ref_voice_ids: list[str] | None = None,
    device: str = "cpu",
):
    """Main pipeline: create optimized voicepack from reference audio."""
    start_time = time.time()

    print(f"\n{'='*60}")
    print(f"  KOKORO VIETNAMESE - OPTIMIZED VOICE CLONING")
    print(f"  Target: {voice_name}")
    print(f"{'='*60}\n")

    # ── Step 1: Audio Preprocessing ──────────────────────────────────
    print("━" * 40)
    print("STEP 1: Audio Preprocessing")
    print("━" * 40)

    audio = load_and_preprocess_audio(audio_path)
    segments = extract_speech_segments(audio)

    if not segments:
        print("ERROR: No speech segments found!")
        sys.exit(1)

    # ── Step 2: Compute target mel statistics ────────────────────────
    print("\n" + "━" * 40)
    print("STEP 2: Computing Target Mel Statistics")
    print("━" * 40)

    mel_transform = build_mel_transform(device)
    target_stats = compute_mel_statistics(segments, mel_transform, device)
    print(f"  Target mel energy: {target_stats['mel_energy']:.4f}")
    print(f"  Target spectral shape (first 5 bands): {target_stats['mel_mean_profile'][:5]}")

    # ── Step 3: Download & profile reference voicepacks ──────────────
    print("\n" + "━" * 40)
    print("STEP 3: Downloading & Profiling Reference Voices")
    print("━" * 40)

    if ref_voice_ids is None:
        ref_voice_ids = get_male_voice_ids()

    ref_voicepacks = {}
    ref_stats = {}

    for vid in ref_voice_ids:
        print(f"\n  Processing voice: {vid}")
        try:
            vp = download_reference_voicepack(vid)
            ref_voicepacks[vid] = vp
            print(f"    Voicepack loaded: {tuple(vp.shape)}")

            # Profile by synthesizing test sentences
            stats = profile_voicepack_mel(vp, mel_transform, device)
            ref_stats[vid] = stats
            print(f"    Mel profiled: energy={stats['mel_energy']:.4f}, segments={stats['n_segments']}")
        except Exception as e:
            print(f"    WARNING: Failed to process {vid}: {e}")
            continue

    if not ref_voicepacks:
        print("ERROR: No reference voicepacks loaded!")
        sys.exit(1)

    # ── Step 4: Find optimal blend ───────────────────────────────────
    print("\n" + "━" * 40)
    print("STEP 4: Finding Optimal Voicepack Blend")
    print("━" * 40)

    blended_vp, blend_weights = find_optimal_blend(
        target_stats, ref_voicepacks, ref_stats, device
    )

    # ── Step 5: Per-dimension refinement ─────────────────────────────
    print("\n" + "━" * 40)
    print("STEP 5: Per-Dimension Refinement")
    print("━" * 40)

    refined_vp = refine_per_dimension(
        blended_vp, ref_voicepacks, target_stats, ref_stats, blend_weights
    )

    # ── Step 6: Save voicepack ───────────────────────────────────────
    print("\n" + "━" * 40)
    print("STEP 6: Saving Voicepack")
    print("━" * 40)

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(refined_vp, str(out_path))

    elapsed = time.time() - start_time
    print(f"\n  ✅ Voicepack saved: {out_path}")
    print(f"     Shape: {tuple(refined_vp.shape)}")
    print(f"     Size: {out_path.stat().st_size / 1024:.1f} KB")
    print(f"     Total time: {elapsed:.1f}s")

    # ── Step 7: Quick validation ─────────────────────────────────────
    print("\n" + "━" * 40)
    print("STEP 7: Validation Synthesis")
    print("━" * 40)

    try:
        validation_text = "Xin chào các bạn, đây là giọng đọc mới được tối ưu hóa từ mô hình Kokoro Vietnamese."
        from kokoro_vietnamese.core import KokoroVietnamese

        tts = KokoroVietnamese(device=device)
        tts.voicepack = refined_vp
        audio_out, phonemes = tts.synthesize(validation_text)

        validation_path = out_path.parent / f"{out_path.stem}_validation.wav"
        sf.write(str(validation_path), audio_out, SAMPLE_RATE)
        print(f"  ✅ Validation audio saved: {validation_path}")
        print(f"     Duration: {len(audio_out) / SAMPLE_RATE:.2f}s")
        print(f"     Phonemes: {phonemes[:100]}...")
    except Exception as e:
        print(f"  ⚠ Validation synthesis failed: {e}")

    print(f"\n{'='*60}")
    print(f"  DONE! Voicepack '{voice_name}' ready at: {out_path}")
    print(f"{'='*60}\n")

    return refined_vp


def main():
    parser = argparse.ArgumentParser(
        description="Optimized Voice Cloning via Embedding Transfer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--audio",
        required=True,
        help="Path to reference audio file (MP3/WAV)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output voicepack path (.pt)",
    )
    parser.add_argument(
        "--name",
        default="Cloned Voice",
        help="Name for the cloned voice",
    )
    parser.add_argument(
        "--ref-voices",
        nargs="+",
        default=None,
        help="Specific reference voice IDs to use (default: all male voices)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to use (default: cpu)",
    )

    args = parser.parse_args()
    clone_voice_optimized(
        audio_path=args.audio,
        output_path=args.output,
        voice_name=args.name,
        ref_voice_ids=args.ref_voices,
        device=args.device,
    )


if __name__ == "__main__":
    main()
