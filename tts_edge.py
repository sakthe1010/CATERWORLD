import asyncio
import edge_tts
from pydub import AudioSegment
import os

SCRIPT_FILE = "input/script_2.txt"
TEMP_AUDIO = "audio/temp.mp3"
FINAL_AUDIO = "audio/voiceover.wav"
TARGET_DURATION_MS = 15000
MAX_ATTEMPTS = 5

# Step 1: Load script
with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
    script_text = " ".join(line.strip() for line in f if line.strip())

# Step 2: Helper to generate and return audio duration in ms
async def generate_and_get_duration(rate_tag):
    communicate = edge_tts.Communicate(text=script_text, voice="en-US-JennyNeural", rate=rate_tag)
    with open(TEMP_AUDIO, "wb") as out_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                out_file.write(chunk["data"])
    audio = AudioSegment.from_file(TEMP_AUDIO, format="mp3")
    return audio, len(audio)

# Step 3: Try different speeds to get close to 15s
base_rate_percent = -20
attempt = 0
final_audio = None

while attempt < MAX_ATTEMPTS:
    rate_tag = f"{base_rate_percent:+d}%"
    print(f"[INFO] Attempt {attempt + 1} with rate {rate_tag}")
    audio, duration = asyncio.run(generate_and_get_duration(rate_tag))
    print(f"[INFO] Audio duration: {duration / 1000:.2f}s")

    if duration > TARGET_DURATION_MS + 500:
        base_rate_percent += 10  # speak faster
    elif duration < TARGET_DURATION_MS - 1500:
        base_rate_percent -= 10  # speak slower
    else:
        final_audio = audio
        break
    attempt += 1

# Step 4: Use final audio or last attempt
if final_audio is None:
    print("[WARN] Could not converge to 15s. Using closest attempt.")
    final_audio = audio

# Step 5: Pad if necessary
if len(final_audio) < TARGET_DURATION_MS:
    pad_ms = TARGET_DURATION_MS - len(final_audio)
    final_audio += AudioSegment.silent(duration=pad_ms)
    print(f"[INFO] Added {pad_ms} ms of silence.")
else:
    print(f"[INFO] No padding needed.")

# Step 6: Export final audio
final_audio.export(FINAL_AUDIO, format="wav")
print(f"[DONE] Final voiceover saved to: {FINAL_AUDIO}")

# Optional cleanup
os.remove(TEMP_AUDIO)

