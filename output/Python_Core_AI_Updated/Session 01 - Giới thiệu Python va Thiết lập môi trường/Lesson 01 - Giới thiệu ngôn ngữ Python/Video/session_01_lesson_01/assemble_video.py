import subprocess
import os
import sys

ffmpeg_path = r"C:\Users\PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"

def run_cmd(cmd):
    print(f"Running command: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing command: {res.stderr}")
        sys.exit(res.returncode)
    else:
        print(res.stdout)

# Step 1: Mix bg-music.mp3 with out.mp4 audio (bgm mixed at 0.05 volume and looped)
print("Mixing background music...")
mix_cmd = f'"{ffmpeg_path}" -y -i out.mp4 -stream_loop -1 -i assets/bg-music.mp3 -filter_complex "[1:a]volume=0.05[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]" -map 0:v -map [a] -c:v copy -c:a aac -ar 44100 -ac 2 temp_main.mp4'
run_cmd(mix_cmd)

# Step 2: Normalize intro.mp4 (scale to 1920x1080, 30fps, 44100Hz audio, stereo)
print("Normalizing intro.mp4...")
norm_intro_cmd = f'"{ffmpeg_path}" -y -i assets/intro.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 30 -pix_fmt yuv420p -c:v libx264 -preset fast -crf 18 -c:a aac -ar 44100 -ac 2 temp_intro.mp4'
run_cmd(norm_intro_cmd)

# Step 3: Normalize outro.mp4
print("Normalizing outro.mp4...")
norm_outro_cmd = f'"{ffmpeg_path}" -y -i assets/outro.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 30 -pix_fmt yuv420p -c:v libx264 -preset fast -crf 18 -c:a aac -ar 44100 -ac 2 temp_outro.mp4'
run_cmd(norm_outro_cmd)

# Step 4: Concatenate normalized videos
print("Concatenating intro, main, and outro...")
with open("list.txt", "w") as f:
    f.write("file 'temp_intro.mp4'\n")
    f.write("file 'temp_main.mp4'\n")
    f.write("file 'temp_outro.mp4'\n")

concat_cmd = f'"{ffmpeg_path}" -y -f concat -safe 0 -i list.txt -c copy final_render.mp4'
run_cmd(concat_cmd)

# Step 5: Clean up temporary files
print("Cleaning up temporary files...")
for file in ["temp_intro.mp4", "temp_main.mp4", "temp_outro.mp4", "list.txt"]:
    if os.path.exists(file):
        os.remove(file)

print("Assembly complete! Final video saved to final_render.mp4")
