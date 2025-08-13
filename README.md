# CaterWorld AI Promo Video Generator

## Overview
This project is an **end-to-end AI-powered pipeline** for generating **personalized promotional videos** for catering services.  
It combines **computer vision (CLIP)**, **LLM-based script generation (Gemini)**, **script ranking (SBERT + Reward Model)**, **Text-to-Speech (Edge TTS / Kokoro)**, and **FFmpeg video assembly** into a fully automated workflow.

---

## Features
- **Tone detection from images** using CLIP (`detect_tone_clip.py`).
- **Multi-tone script generation** with Gemini (`script_variants.py` / `prompt_generator.py`).
- **Script scoring and ranking** via:
  - LLM-based evaluation (`critic_ranker.py`).
  - SBERT embedding + trained reward model (`scorer.py`, `train_reward_model.py`).
- **t-SNE visualization of script quality** (`explain_scores.py`).
- **Comparison of evaluation methods** (`compare.py`).
- **Voiceover generation**:
  - Microsoft Edge TTS with dynamic speed adjustment (`tts_edge.py`).
  - Kokoro TTS for alternative voices (`tts_kokoro.py`).
- **Final video assembly** with animated slides, logos, background music, and optional subtitles (`make_video.sh`).

---

## Project Structure
```
├── input/
│   ├── images/               # Brand images
│   ├── logo.png               # Brand logo
│   ├── input.json             # Metadata (name, tagline, description, etc.)
│   ├── gen_prompt.txt         # Generated prompt for Gemini
│   └── script_2.txt           # Best-selected script
│
├── variants/                  # Script variants generated per tone
├── audio/
│   ├── temp.mp3
│   └── voiceover.wav
│
├── output/
│   ├── final_promo.mp4        # Final video output
│   ├── gemini_scores.csv
│   ├── reward_scores.csv
│   ├── scores.csv
│   └── tsne_plot.png
│
├── models/
│   └── reward_model.pkl       # Trained Ridge Regression model
│
├── scripts/                   # Main processing scripts
│   ├── detect_tone_clip.py
│   ├── prompt_generator.py
│   ├── script_variants.py
│   ├── critic_ranker.py
│   ├── scorer.py
│   ├── train_reward_model.py
│   ├── explain_scores.py
│   ├── compare.py
│   ├── tts_edge.py
│   ├── tts_kokoro.py
│   └── make_video.sh
│
├── subtitles/                 # Optional subtitle files
└── config.py                  # Centralized paths & settings
```

---

## Installation

### 1️Clone Repository & Install Requirements
```bash
git clone https://github.com/sakthe1010/CATERWORLD.git
cd CATERWORLD
pip install -r requirements.txt
```

### 2️Set Environment Variables
```bash
export GOOGLE_API_KEY="your_gemini_api_key"
```

### 3️Prepare Input Data
Place:
- Brand images in `input/`
- Logo at `input/logo.png`
- Metadata in `input/input.json`:
```json
{
  "caterer_name": "SpiceTrail Catering",
  "tagline": "15 Years of Culinary Excellence",
  "description": ["Delicious food", "Elegant presentation", "Exceptional service"],
  "cuisine": ["Indian", "Continental"],
  "services": ["Wedding Catering", "Corporate Events"],
  "location": "Chennai"
}
```

---

## Workflow

1. **Detect visual tone**  
   ```bash
   python detect_tone_clip.py
   ```

2. **Generate script variants**  
   ```bash
   python script_variants.py
   ```

3. **Evaluate scripts with Gemini (LLM scoring)**  
   ```bash
   python critic_ranker.py
   ```

4. **Train Reward Model (optional)**  
   ```bash
   python train_reward_model.py
   ```

5. **Evaluate scripts with Reward Model**  
   ```bash
   python scorer.py
   ```

6. **Visualize scores with t-SNE**  
   ```bash
   python explain_scores.py
   ```

7. **Compare scoring methods**  
   ```bash
   python compare.py
   ```

8. **Generate voiceover**  
   - Edge TTS:
     ```bash
     python tts_edge.py
     ```
   - Kokoro TTS:
     ```bash
     python tts_kokoro.py
     ```

9. **Assemble final video**  
   ```bash
   bash make_video.sh
   ```

---

## Example Output
- **Tone detected**: `elegant`
- **Best script**:
  ```
  SpiceTrail Catering: 15 Years of Culinary Excellence in Chennai
  From grand weddings to corporate feasts, we craft unforgettable menus.
  Book now and make your event a culinary masterpiece!
  ```
- **Final video**: `output/final_promo.mp4`

---

## Tech Stack
- **AI/ML**: Google Gemini API, SBERT, CLIP
- **ML Frameworks**: scikit-learn, sentence-transformers, PyTorch
- **Audio**: Microsoft Edge TTS, Kokoro TTS, pydub
- **Video**: FFmpeg
- **Visualization**: Matplotlib, t-SNE

---
