# config.py

# Folder paths
INPUT_DIR = "input"
IMAGE_DIR = f"{INPUT_DIR}/images"
LOGO_PATH = f"{INPUT_DIR}/logo.png"
METADATA_FILE = f"{INPUT_DIR}/input.json"

AUDIO_DIR = "audio"
TEMP_AUDIO = f"{AUDIO_DIR}/temp.mp3"
FINAL_AUDIO = f"{AUDIO_DIR}/voiceover.wav"

SUBTITLE_FILE = "subtitles/subs.srt"
OUTPUT_DIR = "output"
FINAL_VIDEO = f"{OUTPUT_DIR}/final_promo.mp4"

# Video & TTS settings
TARGET_DURATION_MS = 20000  # Change this for 15s or 20s total
MAX_ATTEMPTS = 5
VOICE = "en-US-JennyNeural"
