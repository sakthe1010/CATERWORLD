# File: explain_scores.py

import os
import csv
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer

# --- Paths ---
VARIANT_DIR = "variants"
MODEL_PATH = "models/reward_model.pkl"
SCORES_CSV = "output/scores.csv"
TSNE_PLOT = "output/tsne_plot.png"

# --- Setup ---
os.makedirs("output", exist_ok=True)
model = joblib.load(MODEL_PATH)
sbert = SentenceTransformer("all-MiniLM-L6-v2")

# --- Score scripts ---
rows = []
embeddings = []
filenames = []

for file in sorted(os.listdir(VARIANT_DIR)):
    path = os.path.join(VARIANT_DIR, file)
    if not file.endswith(".txt"): continue

    with open(path, "r", encoding="utf-8") as f:
        script = f.read().strip()

    emb = sbert.encode([script])[0]
    score = model.predict([emb])[0]

    rows.append([file, script, score])
    embeddings.append(emb)
    filenames.append(file)

# --- Save scores to CSV ---
df = pd.DataFrame(rows, columns=["filename", "script", "score"])
df.to_csv(SCORES_CSV, index=False)
print(f"[✅] Scores saved to {SCORES_CSV}")

# --- Optional: t-SNE plot ---
print("[INFO] Generating t-SNE visualization...")
tsne = TSNE(n_components=2, perplexity=2, random_state=42)
emb_2d = tsne.fit_transform(np.array(embeddings))

plt.figure(figsize=(10, 6))
sc = plt.scatter(emb_2d[:, 0], emb_2d[:, 1], c=df["score"], cmap="coolwarm", s=100, edgecolors='k')
plt.colorbar(sc, label="Predicted Quality Score")
for i, txt in enumerate(filenames):
    plt.annotate(txt.replace(".txt", ""), (emb_2d[i, 0]+0.5, emb_2d[i, 1]), fontsize=8)

plt.title("t-SNE of Script Variants (Colored by Score)")
plt.tight_layout()
plt.savefig(TSNE_PLOT)
print(f"[📊] t-SNE plot saved to {TSNE_PLOT}")
