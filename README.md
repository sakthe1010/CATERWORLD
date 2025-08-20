# CATERWORLD

CATERWORLD is a toolkit for generating, scoring, and producing promotional scripts and videos for catering services using AI models and automation.

## Project Structure

```
CATERWORLD/
├── src/                  # Main Python scripts
│   ├── compare.py        # Compare Gemini and Reward model scores
│   ├── config.py         # Configuration and paths
│   ├── scorer.py         # Score script variants using a reward model
│   ├── prompt_generator.py # Generate prompts for scriptwriting
│   ├── train_reward_model.py # Train the reward model
│   ├── critic_ranker.py  # (Other script)
│   ├── detect_tone_clip.py
│   ├── explain_scores.py
│   ├── script_variants.py
│   ├── tts_edge.py
│   ├── tts_kokoro.py
├── data/
│   ├── input/            # Input files (JSON, prompts, scores)
│   ├── output/           # Output files (scores, videos)
│   ├── audio/            # Audio files
│   ├── subtitles/        # Subtitle files
├── models/               # Trained model files
├── assets/
│   ├── images/           # Images and logos
│   ├── videos/           # Video assets
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## Features
- **Prompt Generation**: Automatically creates marketing prompts for catering services.
- **Script Scoring**: Uses a trained reward model to score and select the best promotional scripts.
- **Score Comparison**: Compares scores from different models and reports improvements.
- **Audio & Video Automation**: Integrates with TTS and video generation scripts.
- **Configurable**: All paths and settings are managed via `src/config.py`.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare input data**:
   - Place your input JSON and other files in `data/input/`.
   - Place audio files in `data/audio/`.
   - Place images/logos in `assets/images/`.

3. **Train the reward model** (optional):
   ```bash
   python3 src/train_reward_model.py
   ```

4. **Generate prompt**:
   ```bash
   python3 src/prompt_generator.py
   ```

5. **Score script variants**:
   ```bash
   python3 src/scorer.py
   ```

6. **Compare scores**:
   ```bash
   python3 src/compare.py
   ```

## Usage
- All main scripts are in the `src/` directory. Run them as shown above.
- Outputs (scores, videos) are saved in `data/output/`.
- Models are stored in `models/`.

## Requirements
See `requirements.txt` for all Python dependencies.

## License
See individual folders for license information.

## Contributing
Pull requests and suggestions are welcome!

---
For more details, see comments in each script or reach out to the project maintainer.
