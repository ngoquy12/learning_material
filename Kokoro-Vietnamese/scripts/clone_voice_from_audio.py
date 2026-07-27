from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.parametrizations import spectral_norm


def librosa_mel_fn(sr: int = 24000, n_fft: int = 2048, n_mels: int = 80, fmin: float = 0.0, fmax: float = 12000.0) -> torch.Tensor:
    """Computes Mel filterbank matrix without requiring librosa or torchaudio."""
    weights = np.zeros((n_mels, int(1 + n_fft // 2)), dtype=np.float32)
    m_min = 2595.0 * np.log10(1.0 + fmin / 700.0)
    m_max = 2595.0 * np.log10(1.0 + fmax / 700.0)
    m_pts = np.linspace(m_min, m_max, n_mels + 2)
    f_pts = 700.0 * (10.0 ** (m_pts / 2595.0) - 1.0)
    bin_pts = np.floor((n_fft + 1) * f_pts / sr).astype(int)

    for i in range(1, n_mels + 1):
        b_prev, b_curr, b_next = bin_pts[i - 1], bin_pts[i], bin_pts[i + 1]
        if b_curr > b_prev:
            for j in range(b_prev, b_curr):
                if j < weights.shape[1]:
                    weights[i - 1, j] = (j - b_prev) / (b_curr - b_prev)
        if b_next > b_curr:
            for j in range(b_curr, b_next):
                if j < weights.shape[1]:
                    weights[i - 1, j] = (b_next - j) / (b_next - b_curr)
    return torch.from_numpy(weights).float()


def compute_mel_spectrogram(
    audio_tensor: torch.Tensor,
    sr: int = 24000,
    n_fft: int = 2048,
    win_length: int = 1200,
    hop_length: int = 300,
    n_mels: int = 80,
) -> torch.Tensor:
    """Computes normalized log-mel spectrogram using native PyTorch STFT."""
    window = torch.hann_window(win_length).to(audio_tensor.device)
    stft = torch.stft(
        audio_tensor,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        return_complex=True,
    )
    magnitudes = torch.abs(stft)
    mel_basis = librosa_mel_fn(sr, n_fft, n_mels, 0.0, sr / 2.0).to(audio_tensor.device)
    mel = torch.matmul(mel_basis, magnitudes)
    return mel


class LearnedDownSample(nn.Module):
    def __init__(self, layer_type, dim_in):
        super().__init__()
        self.layer_type = layer_type
        if self.layer_type == "none":
            self.conv = nn.Identity()
        elif self.layer_type == "timepreserve":
            self.conv = spectral_norm(
                nn.Conv2d(dim_in, dim_in, kernel_size=(3, 1), stride=(2, 1), groups=dim_in, padding=(1, 0))
            )
        elif self.layer_type == "half":
            self.conv = spectral_norm(
                nn.Conv2d(dim_in, dim_in, kernel_size=(3, 3), stride=(2, 2), groups=dim_in, padding=1)
            )
        else:
            raise RuntimeError(f"Unexpected downsample type: {self.layer_type}")

    def forward(self, x):
        return self.conv(x)


class DownSample(nn.Module):
    def __init__(self, layer_type):
        super().__init__()
        self.layer_type = layer_type

    def forward(self, x):
        if self.layer_type == "none":
            return x
        elif self.layer_type == "timepreserve":
            return F.avg_pool2d(x, (2, 1))
        elif self.layer_type == "half":
            if x.shape[-1] % 2 != 0:
                x = torch.cat([x, x[..., -1].unsqueeze(-1)], dim=-1)
            return F.avg_pool2d(x, 2)
        else:
            raise RuntimeError(f"Unexpected downsample type: {self.layer_type}")


class ResBlk(nn.Module):
    def __init__(self, dim_in, dim_out, actv=nn.LeakyReLU(0.2), normalize=False, downsample="none"):
        super().__init__()
        self.actv = actv
        self.normalize = normalize
        self.downsample = DownSample(downsample)
        self.downsample_res = LearnedDownSample(downsample, dim_in)
        self.learned_sc = dim_in != dim_out
        self.conv1 = spectral_norm(nn.Conv2d(dim_in, dim_in, 3, 1, 1))
        self.conv2 = spectral_norm(nn.Conv2d(dim_in, dim_out, 3, 1, 1))
        if self.normalize:
            self.norm1 = nn.InstanceNorm2d(dim_in, affine=True)
            self.norm2 = nn.InstanceNorm2d(dim_in, affine=True)
        if self.learned_sc:
            self.conv1x1 = spectral_norm(nn.Conv2d(dim_in, dim_out, 1, 1, 0, bias=False))

    def _shortcut(self, x):
        if self.learned_sc:
            x = self.conv1x1(x)
        if self.downsample:
            x = self.downsample(x)
        return x

    def _residual(self, x):
        if self.normalize:
            x = self.norm1(x)
        x = self.actv(x)
        x = self.conv1(x)
        x = self.downsample_res(x)
        if self.normalize:
            x = self.norm2(x)
        x = self.actv(x)
        x = self.conv2(x)
        return x

    def forward(self, x):
        x = self._shortcut(x) + self._residual(x)
        return x / math.sqrt(2)


class StyleEncoder(nn.Module):
    def __init__(self, dim_in=64, style_dim=128, max_conv_dim=512):
        super().__init__()
        blocks = []
        blocks += [spectral_norm(nn.Conv2d(1, dim_in, 3, 1, 1))]
        repeat_num = 4
        for _ in range(repeat_num):
            dim_out = min(dim_in * 2, max_conv_dim)
            blocks += [ResBlk(dim_in, dim_out, downsample="half")]
            dim_in = dim_out
        blocks += [nn.LeakyReLU(0.2)]
        blocks += [spectral_norm(nn.Conv2d(dim_out, dim_out, 5, 1, 0))]
        blocks += [nn.AdaptiveAvgPool2d(1)]
        blocks += [nn.LeakyReLU(0.2)]
        self.shared = nn.Sequential(*blocks)
        self.unshared = nn.Linear(dim_out, style_dim)

    def forward(self, x):
        h = self.shared(x)
        h = h.view(h.size(0), -1)
        s = self.unshared(h)
        return s


def slice_audio_into_clips(audio_data: np.ndarray, sample_rate: int, clip_duration_sec: float = 6.0, max_clips: int = 20) -> list[np.ndarray]:
    """Slices audio into clean non-silent speech segments."""
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)  # convert stereo to mono

    clip_samples = int(clip_duration_sec * sample_rate)
    total_samples = len(audio_data)

    clips = []
    step = clip_samples

    for start in range(0, total_samples - clip_samples, step):
        chunk = audio_data[start : start + clip_samples]
        rms = np.sqrt(np.mean(chunk**2))
        # Filter out quiet/silent sections
        if rms > 0.01:
            clips.append(chunk)
            if len(clips) >= max_clips:
                break

    print(f"Extracted {len(clips)} active speech audio segments (6s duration each)")
    return clips


def clone_voicepack_from_mp3(
    mp3_path: str,
    output_pt_path: str,
    reference_voicepack_path: str | None = None,
    device: str = "cpu",
):
    print(f"Loading audio recording: {mp3_path}")
    audio_data, sr = sf.read(mp3_path, dtype="float32")
    print(f"Audio loaded successfully. Duration: {len(audio_data) / sr:.2f} seconds ({sr} Hz)")

    # Step 1: Slice into 20 clean 6-second clips
    clips = slice_audio_into_clips(audio_data, sr, clip_duration_sec=6.0, max_clips=20)

    # Step 2: Initialize StyleEncoder
    encoder = StyleEncoder(dim_in=64, style_dim=128, max_conv_dim=512).to(device).eval()

    mel_mean = -4.0
    mel_std = 4.0

    style_vectors = []
    with torch.no_grad():
        for i, clip in enumerate(clips):
            wav_tensor = torch.from_numpy(clip).unsqueeze(0)  # [1, samples]
            if sr != 24000:
                # Simple linear interpolation resampling for exact 24kHz
                num_samples_target = int(len(clip) * 24000 / sr)
                wav_tensor = F.interpolate(
                    wav_tensor.unsqueeze(0), size=num_samples_target, mode="linear", align_corners=False
                ).squeeze(0)

            wav_tensor = wav_tensor.to(device)

            mel = compute_mel_spectrogram(wav_tensor, sr=24000)
            mel = (torch.log(1e-5 + mel) - mel_mean) / mel_std
            mel_input = mel
            while mel_input.ndim < 4:
                mel_input = mel_input.unsqueeze(0)
            while mel_input.ndim > 4:
                mel_input = mel_input.squeeze(0)

            s_vec = encoder(mel_input)  # [1, 128]
            style_vectors.append(s_vec.cpu())

    avg_extracted_style = torch.cat(style_vectors, dim=0).mean(dim=0)  # [128]

    # Step 4: Blend / Align with Reference Male Voicepack Embedding for maximum naturalness
    if reference_voicepack_path and Path(reference_voicepack_path).exists():
        print(f"Blending extracted style with base reference voicepack: {reference_voicepack_path}")
        ref_vp = torch.load(reference_voicepack_path, map_location="cpu")  # [510, 1, 256]
        base_style = ref_vp[0, 0, :]  # [256]

        # First 128 dims: acoustic style, Last 128 dims: prosodic style
        acoustic_part = 0.5 * avg_extracted_style + 0.5 * base_style[:128]
        prosodic_part = 0.5 * avg_extracted_style + 0.5 * base_style[128:]
        combined = torch.cat([acoustic_part, prosodic_part], dim=0)  # [256]
    else:
        combined = torch.cat([avg_extracted_style, avg_extracted_style], dim=0)  # [256]

    voicepack_tensor = combined.unsqueeze(0).unsqueeze(0).expand(510, 1, 256).clone()

    # Step 5: Save .pt voicepack
    out_path = Path(output_pt_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(voicepack_tensor, str(out_path))
    print(f"Successfully generated Voicepack 'Anh Quang': {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone Voicepack from MP3/WAV recording")
    parser.add_argument("--mp3", required=True, help="Path to MP3/WAV recording")
    parser.add_argument("--output", required=True, help="Output .pt voicepack path")
    parser.add_argument("--ref-voice", default=None, help="Optional reference voicepack path")

    args = parser.parse_args()
    clone_voicepack_from_mp3(args.mp3, args.output, args.ref_voice)
