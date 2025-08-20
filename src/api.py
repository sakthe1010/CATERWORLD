from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import subprocess
from pathlib import Path
from src.tts.tts_kokoro import synthesize_kokoro

app = FastAPI()

@app.post("/generate")
async def generate(
    metadata: UploadFile = File(...),
    logo: UploadFile = File(...),
    image_1: UploadFile = File(...),
    image_2: UploadFile = File(...),
    image_3: UploadFile = File(...),
    bgm: UploadFile = File(...)
):
    input_dir = Path("input")
    audio_dir = Path("audio")
    output_file = Path("output/final_promo.mp4")

    # Save input files
    files = {
        "input.json": metadata,
        "caterworld_logo.png": logo,
        "image_1.jpeg": image_1,
        "image_2.jpeg": image_2,
        "image_3.jpeg": image_3,
    }
    for name, upload in files.items():
        with open(input_dir / name, "wb") as f:
            f.write(await upload.read())

    with open(audio_dir / "bgm.wav", "wb") as f:
        f.write(await bgm.read())

    # Run TTS
    synthesize_kokoro(
        metadata_path=input_dir / "input.json",
        out_wav=audio_dir / "voiceover.wav",
        voice="af_heart",
        lang="a",
        target_ms=20000
    )

    # Run video generation shell script
    subprocess.run(["bash", "scripts/make_video.sh"], check=True)

    # Return generated video
    return FileResponse(output_file, media_type="video/mp4", filename="final_promo.mp4")
