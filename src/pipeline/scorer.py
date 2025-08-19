# File: scorer.py

import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Config ---
VARIANT_DIR = "variants"
BEST_SCRIPT_FILE = "input/script_2.txt"
MODEL_PATH = "models/reward_model.pkl"

# --- Load Model ---
print("[INFO] Loading reward model and SBERT...")
model = joblib.load(MODEL_PATH)
sbert = SentenceTransformer("all-MiniLM-L6-v2")

# --- Score Variants ---
print("[INFO] Scoring variants...")
best_score = -1
best_script = ""

for file in sorted(os.listdir(VARIANT_DIR)):
    path = os.path.join(VARIANT_DIR, file)
    with open(path, "r", encoding="utf-8") as f:
        script = f.read().strip()

    embedding = sbert.encode([script])
    score = model.predict(embedding)[0]

    print(f"[{file}] Score: {score:.2f}")

    if score > best_score:
        best_score = score
        best_script = script

# --- Save Best ---
if best_script:
    with open(BEST_SCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write(best_script)
    print(f"\n[✅] Best script saved to: {BEST_SCRIPT_FILE} (Score: {best_score:.2f})")
else:
    print("[⚠️] No script selected.")
