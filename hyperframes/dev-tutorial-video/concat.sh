#!/usr/bin/env bash
set -euo pipefail

ASSETS="courses/fundamental_python/assets"
RENDERS="renders"

# Find the most recent render
RENDER=$(ls -t "$RENDERS"/*.mp4 2>/dev/null | grep -v '\.meta\.json' | head -1)

if [[ -z "$RENDER" ]]; then
  echo "Error: no .mp4 found in $RENDERS/" >&2
  exit 1
fi

INTRO="$ASSETS/intro.mp4"
OUTRO="$ASSETS/outro.mov"
OUTPUT="${RENDER%.mp4}_final.mp4"

echo "Intro:  $INTRO"
echo "Main:   $RENDER"
echo "Outro:  $OUTRO"
echo "Output: $OUTPUT"

# Re-encode all segments to a common format before concat
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

ffmpeg -y -i "$INTRO" \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -r 30 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -c:a aac -ar 44100 -ac 2 \
  "$TMP/intro.mp4"

ffmpeg -y -i "$RENDER" \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -r 30 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -c:a aac -ar 44100 -ac 2 \
  "$TMP/main.mp4"

ffmpeg -y -i "$OUTRO" \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -r 30 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -c:a aac -ar 44100 -ac 2 \
  "$TMP/outro.mp4"

# Write concat list
printf "file '%s'\nfile '%s'\nfile '%s'\n" \
  "$TMP/intro.mp4" "$TMP/main.mp4" "$TMP/outro.mp4" \
  > "$TMP/list.txt"

ffmpeg -y -f concat -safe 0 -i "$TMP/list.txt" \
  -c copy \
  "$OUTPUT"

echo "Done: $OUTPUT"
