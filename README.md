# CATERWORLD

CATERWORLD is an AI-powered toolkit for generating, scoring, and producing promotional scripts and videos for catering services. It combines prompt engineering, reward modeling, TTS, and video automation, and is fully API-enabled and Dockerized for easy deployment.

---

## Project Structure

```
CATERWORLD/
├── src/
│   ├── api.py                # FastAPI/Flask API endpoints for all core features
│   ├── config.py             # Central configuration and paths
│   ├── orchestrate.py        # Orchestrates the workflow
│   ├── pipeline/
│   │   ├── critic_ranker.py      # Ranks script variants using Gemini API
│   │   ├── detect_tone_clip.py   # Detects tone from images using CLIP
│   │   ├── prompt_generator.py   # Generates scriptwriting prompts
│   │   ├── score_visualizer.py   # Visualizes scores and embeddings
│   │   ├── scorer.py             # Scores script variants with reward model
│   │   ├── script_variants.py    # Generates script variants for different tones
│   ├── tools/
│   │   ├── compare_scores.py     # Compares Gemini and reward model scores
│   │   ├── train_reward_model.py # Trains the reward model
│   ├── tts/
│   │   ├── tts_edge.py           # Synthesizes voiceover using Edge TTS
│   │   ├── tts_kokoro.py         # Synthesizes voiceover using Kokoro TTS
├── scripts/                  # Shell scripts (e.g., make_video.sh)
├── audio/                    # Audio files (bgm, temp, voiceover)
├── input/                    # Input assets (logo, images, prompts, scripts)
├── output/                   # Output files (videos, scores, plots)
├── subtitles/                # Subtitle files
├── variants/                 # Script variants for scoring
├── models/                   # Trained model files (reward model)
├── ffmpeg/                   # FFmpeg binaries and docs
├── temp/                     # Temporary files (intermediate video/audio)
├── kokoro/                   # External library/package (with its own structure)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Containerization support
├── README.md                 # Project documentation
```

---

## Detailed Module Explanations

### src/pipeline/
- **critic_ranker.py**: Ranks script variants using Gemini API based on clarity, emotional impact, and call to action.
- **detect_tone_clip.py**: Uses CLIP to analyze images and suggest the best tone for the script.
- **prompt_generator.py**: Generates a prompt for scriptwriting from input metadata.
- **score_visualizer.py**: Visualizes script scores and embeddings using t-SNE and matplotlib.
- **scorer.py**: Scores all script variants using a trained reward model and selects the best script.
- **script_variants.py**: Generates multiple script variants for different tones using Gemini API.

### src/tools/
- **compare_scores.py**: Compares Gemini and reward model scores, calculates improvements, and prints summary statistics.
- **train_reward_model.py**: Trains a Ridge Regression reward model using SBERT embeddings and script scores.

### src/tts/
- **tts_edge.py**: Synthesizes voiceover from the best script using Microsoft Edge TTS, adjusting speed for target duration.
- **tts_kokoro.py**: Synthesizes voiceover using Kokoro TTS pipeline, supporting different voices and languages.

### Other Key Files
- **api.py**: Exposes all major features (prompt generation, scoring, TTS, etc.) as RESTful API endpoints.
- **config.py**: Centralizes all file paths and configuration options.
- **orchestrate.py**: Orchestrates the end-to-end workflow, calling pipeline modules in sequence.
- **Dockerfile**: Containerizes the application for easy deployment.

---

## Usage (Step-by-Step)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare input data
- Place your input JSON, images, and scripts in `input/`.
- Place audio files in `audio/`.
- Place script variants in `variants/`.

### 3. Train the reward model (optional)
```bash
python3 src/tools/train_reward_model.py
```

### 4. Generate prompt for scriptwriting
```bash
python3 src/pipeline/prompt_generator.py
```

### 5. Generate script variants for different tones
```bash
python3 src/pipeline/script_variants.py
```

### 6. Score script variants and select the best
```bash
python3 src/pipeline/scorer.py
```

### 7. Visualize script scores and embeddings
```bash
python3 src/pipeline/score_visualizer.py
```

### 8. Compare Gemini and reward model scores
```bash
python3 src/tools/compare_scores.py
```

### 9. Synthesize TTS audio
You must run one of the TTS scripts before generating the final video:
- For Edge TTS:
  ```bash
  python3 src/tts/tts_edge.py
  ```
- For Kokoro TTS (recommended for high-quality voiceover):
  ```bash
  python3 src/tts/tts_kokoro.py
  ```
  > **Note:** Run this before executing `make_video.sh` to ensure the generated audio is available for video creation.

### 10. Generate video
```bash
bash scripts/make_video.sh
```

---

## API Usage

Start the API server:
```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

You can then use the API endpoints to:
- Generate prompts
- Generate script variants
- Score scripts
- Visualize scores
- Synthesize TTS audio
- Compare scores

---

## Docker Deployment

### 1. Build Docker image
```bash
docker build -t caterworld .
```

### 2. Run Docker container
```bash
docker run --rm -it -p 8000:8000 -v $(pwd):/app caterworld
```

The API will be available at `http://localhost:8000`.

---

## Requirements
See `requirements.txt` for all Python dependencies.

---
