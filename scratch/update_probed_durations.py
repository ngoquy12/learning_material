"""
scratch/update_probed_durations.py
"""

import json
from pathlib import Path

proj_dir = Path('output/test_javascript_functions')
durations = json.loads((proj_dir / 'assets' / 'tts' / 'durations.json').read_text(encoding='utf-8'))

intro_dur = 9.24
outro_dur = 12.15
current_start = intro_dur

scene_clips = []
audio_clips = []

scenes_info = [
    ('Scene_01', 'scene-01', 1, 20),
    ('Scene_02', 'scene-02', 2, 21),
    ('Scene_03', 'scene-03', 3, 22),
    ('Scene_04', 'scene-04', 4, 23),
    ('Scene_05', 'scene-05', 5, 24),
    ('Scene_06', 'scene-06', 6, 25),
]

for sc_id, sc_slug, trk, aud_trk in scenes_info:
    dur = durations[sc_id]
    num = sc_id.replace('Scene_', '')
    scene_clips.append(f'      <div class="clip" data-composition-src="src/compositions/{sc_id}.html" data-composition-id="{sc_slug}" data-start="{round(current_start, 2)}" data-duration="{dur}" data-track-index="{trk}"></div>')
    audio_clips.append(f'      <audio id="tts-{num}" data-start="{round(current_start, 2)}" data-duration="{dur}" data-track-index="{aud_trk}" data-volume="1" src="assets/tts/{sc_id}.wav"></audio>')
    
    # Update scene file data-duration
    sc_file = proj_dir / 'src' / 'compositions' / f'{sc_id}.html'
    content = sc_file.read_text(encoding='utf-8')
    for old_d in ["32.5", "35.0", "34.0", "32.0", "36.0", "25.0"]:
        content = content.replace(f'data-duration="{old_d}"', f'data-duration="{dur}"')
    sc_file.write_text(content, encoding='utf-8')
    
    current_start += dur

outro_start = round(current_start, 2)
total_duration = round(intro_dur + sum(durations.values()) + outro_dur, 2)

index_html = f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0f172a; }}
      .clip {{ position: absolute; visibility: hidden; }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="test-javascript-functions"
      data-start="0"
      data-duration="{total_duration}"
      data-width="1920"
      data-height="1080"
    >
      <!-- Intro Composition Clip (9.24s) -->
      <div class="clip" data-composition-src="src/compositions/Intro.html"
           data-composition-id="scene-intro" data-start="0" data-duration="9.24" data-track-index="0"></div>

      <!-- Scene Clips -->
{chr(10).join(scene_clips)}

      <!-- Outro Composition Clip (12.15s) -->
      <div class="clip" data-composition-src="src/compositions/Outro.html"
           data-composition-id="scene-outro" data-start="{outro_start}" data-duration="12.15" data-track-index="0"></div>

      <!-- Background Music Kênh 99 -->
      <audio id="bg-music"
             data-start="0"
             data-duration="{total_duration}"
             data-track-index="99"
             data-volume="0.12"
             data-loop="true"
             src="assets/bg-music.mp3"></audio>

      <!-- TTS Audio Elements -->
{chr(10).join(audio_clips)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["test-javascript-functions"] = tl;
    </script>
  </body>
</html>"""

(proj_dir / 'index.html').write_text(index_html, encoding='utf-8')
print("Successfully updated index.html & scene durations! Total:", total_duration, "s")
