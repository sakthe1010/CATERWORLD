from pathlib import Path
import os

# Repo root regardless of where code runs
ROOT = Path(__file__).resolve().parents[1]

# Inputs
INPUT_DIR = ROOT / "input"
IMAGE_DIR = INPUT_DIR / "images"
LOGO_PATH = INPUT_DIR / "logo.png"
METADATA_FILE = INPUT_DIR / "input.json"

# Audio
AUDIO_DIR = ROOT / "audio"
AUDIO_DIR.mkdir(exist_ok=True)
TEMP_AUDIO = AUDIO_DIR / "temp.mp3"
FINAL_AUDIO = AUDIO_DIR / "voiceover.wav"

# Video & subs
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
SUBTITLES_DIR = ROOT / "subtitles"
SUBTITLES_DIR.mkdir(exist_ok=True)
FINAL_VIDEO = OUTPUT_DIR / "final_promo.mp4"

# Other dirs
MODELS_DIR = ROOT / "models"
VARIANTS_DIR = ROOT / "variants"
TEMP_DIR = ROOT / "temp"

# Runtime knobs (env‑overridable)
TTS_ENGINE = os.getenv("CW_TTS", "kokoro")       # "kokoro" | "edge"
TARGET_DURATION_MS = int(os.getenv("CW_DURATION_MS", "20000"))
VOICE = os.getenv("CW_TTS_VOICE", "en-US-JennyNeural")
WHISPER_MODEL = os.getenv("CW_WHISPER_MODEL", "small")
