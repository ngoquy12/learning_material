# Multi-stage Dockerfile for Elearning Content Factory
FROM python:3.10-slim AS base

# Install system dependencies (Node.js 18, FFmpeg, Chromium for Puppeteer, fonts)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ffmpeg \
    chromium \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    git \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Puppeteer executable path for Linux container
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Copy dependency manifests
COPY requirements.txt package.json package-lock.json* ./

# Install Python & Node.js dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    npm install --omit=dev

# Copy application source code
COPY . .

# Create runtime storage directory
RUN mkdir -p storage output

# Default entrypoint
CMD ["python", "main.py", "--help"]
