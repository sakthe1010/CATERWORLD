#!/usr/bin/env python3
import argparse, os, json
import soundfile as sf
from pydub import AudioSegment
from kokoro import KPipeline
from pathlib import Path

def build_script(metadata: dict, name_fallback="Our catering service") -> str:
    name = metadata.get("caterer_name", name_fallback)
    tagline = metadata.get("tagline", "").strip()
    lines = metadata.get("description", [])
    cuisine = metadata.get("cuisine", [])

    intro = f"We are {name}, {tagline.lower()}." if tagline else f"We are {name}, here to make your events truly unforgettable."
    body = " ".join(lines)
    cuisine_line = f"Specialising in {', '.join(cuisine)} cuisine. " if cuisine else ""
    outro = f"{cuisine_line}{name} — proudly showcased on CaterWorld."

    return f"{intro} {body} {outro}"

def synthesize_kokoro(
    metadata_path: Path,
    out_wav: Path,
    voice: str = "af_heart",
    lang: str = "a",
    target_ms: int = 20_000,
    max_attempts: int = 5,
    samplerate: int = 24000
) -> None:
    metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    script_text = build_script(metadata)
    base_speed = 1.0
    temp_wav = Path("audio/temp_kokoro.wav")
    final_audio = None

    print(f"[INFO] Generating TTS using Kokoro | Target: {target_ms/1000:.1f}s | Voice: {voice} | Lang: {lang}")
    for attempt in range(max_attempts):
        print(f"[INFO] Attempt {attempt+1} with speed {base_speed:.2f}")
        pipeline = KPipeline(lang_code=lang)
        generator = pipeline(script_text, voice=voice, speed=base_speed)
        _, _, audio_data = next(generator)

        sf.write(temp_wav, audio_data, samplerate=samplerate)
        audio = AudioSegment.from_file(temp_wav)
        duration = len(audio)
        print(f"[INFO] Duration: {duration/1000:.2f}s")

        if duration > target_ms + 500:
            base_speed += 0.1
        elif duration < target_ms - 1500:
            base_speed -= 0.1
        else:
            final_audio = audio
            break

    if final_audio is None:
        final_audio = audio
        print("[WARN] Couldn't match target duration closely. Using closest match.")

    if len(final_audio) < target_ms:
        pad_ms = target_ms - len(final_audio)
        final_audio += AudioSegment.silent(duration=pad_ms)
        print(f"[INFO] Padded {pad_ms} ms of silence.")

    out_wav.parent.mkdir(parents=True, exist_ok=True)
    final_audio.export(out_wav, format="wav")
    temp_wav.unlink(missing_ok=True)

    print(f"[DONE] Saved voiceover to {out_wav.resolve()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate voiceover using Kokoro TTS")
    parser.add_argument("--metadata", default="input/input.json", help="Path to metadata JSON file")
    parser.add_argument("--out", default="audio/voiceover.wav", help="Path to save final WAV")
    parser.add_argument("--voice", default=os.getenv("VOICE", "af_heart"))
    parser.add_argument("--lang", default=os.getenv("LANG_CODE", "a"))
    parser.add_argument("--target-sec", type=float, default=float(os.getenv("TARGET_DURATION_SEC", "20")))
    args = parser.parse_args()

    synthesize_kokoro(
        metadata_path=Path(args.metadata),
        out_wav=Path(args.out),
        voice=args.voice,
        lang=args.lang,
        target_ms=int(args.target_sec * 1000)
    )
