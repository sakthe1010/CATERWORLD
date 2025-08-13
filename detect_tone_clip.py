# File: detect_tone_clip.py

import os
import json
import torch
import clip
from PIL import Image
from tqdm import tqdm

# --- Paths ---
IMAGE_DIR = "input"
METADATA_FILE = "input/input.json"

# --- Tone options ---
TONE_LABELS = ["elegant", "emotional", "fun", "youthful", "luxurious"]
TONE_TEXTS = [f"A {tone} catering photo" for tone in TONE_LABELS]

# --- Load CLIP ---
print("[INFO] Loading CLIP model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# --- Encode tone descriptions ---
with torch.no_grad():
    text_tokens = clip.tokenize(TONE_TEXTS).to(device)
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

# --- Process images ---
image_scores = []

for fname in tqdm(os.listdir(IMAGE_DIR)):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    path = os.path.join(IMAGE_DIR, fname)
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)

    with torch.no_grad():
        image_feat = model.encode_image(image)
        image_feat /= image_feat.norm(dim=-1, keepdim=True)

        sims = (image_feat @ text_features.T).squeeze().cpu().numpy()
        image_scores.append(sims)

# --- Average similarity and pick best tone ---
avg_score = sum(image_scores) / len(image_scores)
best_idx = int(avg_score.argmax())
predicted_tone = TONE_LABELS[best_idx]

print(f"[✅] Predicted tone: {predicted_tone}")

# --- Update input.json ---
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

metadata["tone_preference"] = predicted_tone

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"[💾] Updated tone_preference in input.json to: {predicted_tone}")
