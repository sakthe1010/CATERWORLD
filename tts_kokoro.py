import os
import json
import soundfile as sf
from pydub import AudioSegment
from kokoro import KPipeline

# --- Config ---
METADATA_FILE = "input/input.json"
TEMP_AUDIO = "audio/temp.wav"
FINAL_AUDIO = "audio/voiceover.wav"
TARGET_DURATION_MS = 20000
MAX_ATTEMPTS = 5
LANG_CODE = "a"           # English (American)
VOICE_ID = "af_heart"     # Good female voice

# --- Load metadata ---
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

name = metadata.get("caterer_name", "Our catering service")
tagline = metadata.get("tagline", "").strip()
lines = metadata.get("description", [])
cuisine = metadata.get("cuisine", [])

if tagline:
    intro = f"We are {name}, {tagline.lower()}."
else:
    intro = f"We are {name}, here to make your events truly unforgettable."

body = " ".join(lines)
cuisine_sentence = f"Specialising in {', '.join(cuisine)} cuisine. " if cuisine else ""
outro = f"{cuisine_sentence}{name} — proudly showcased on CaterWorld."

script_text = f"{intro} {body} {outro}"

# --- Generate voiceover with dynamic speed adjustment ---
base_speed = 1.0
final_audio = None

for attempt in range(MAX_ATTEMPTS):
    print(f"[INFO] Attempt {attempt+1} with speed {base_speed:.2f}")

    # Setup Kokoro pipeline
    pipeline = KPipeline(lang_code=LANG_CODE)
    generator = pipeline(script_text, voice=VOICE_ID, speed=base_speed)

    # Get first chunk only
    _, _, audio_data = next(generator)

    # Save to wav
    sf.write(TEMP_AUDIO, audio_data, samplerate=24000)
    audio = AudioSegment.from_file(TEMP_AUDIO)
    duration = len(audio)
    print(f"[INFO] Duration: {duration / 1000:.2f}s")

    if duration > TARGET_DURATION_MS + 500:
        base_speed += 0.1
    elif duration < TARGET_DURATION_MS - 1500:
        base_speed -= 0.1
    else:
        final_audio = audio
        break

if final_audio is None:
    final_audio = audio

# Pad to match 20s if short
if len(final_audio) < TARGET_DURATION_MS:
    final_audio += AudioSegment.silent(duration=TARGET_DURATION_MS - len(final_audio))

os.makedirs(os.path.dirname(FINAL_AUDIO), exist_ok=True)
final_audio.export(FINAL_AUDIO, format="wav")
os.remove(TEMP_AUDIO)
print(f"[DONE] Final voiceover saved to {FINAL_AUDIO}")
