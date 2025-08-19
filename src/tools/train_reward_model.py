# File: train_reward_model.py

import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

# --- Paths ---
DATA_PATH = "input/script_scores.csv"
MODEL_PATH = "models/reward_model.pkl"

# --- Load dataset ---
df = pd.read_csv(DATA_PATH)
scripts = df["script"].tolist()
scores = df["score"].tolist()

# --- Embed using SBERT ---
print("[INFO] Loading SBERT model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(scripts)

# --- Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(embeddings, scores, test_size=0.2, random_state=42)

# --- Train reward model ---
print("[INFO] Training Ridge Regression model...")
reg = Ridge(alpha=1.0)
reg.fit(X_train, y_train)

# --- Evaluate ---
y_pred = reg.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"[INFO] Test RMSE: {mse**0.5:.3f}")
print(f"[INFO] Test R^2: {r2_score(y_test, y_pred):.3f}")

# --- Save model ---
os.makedirs("models", exist_ok=True)
joblib.dump(reg, MODEL_PATH)
print(f"[✅] Model saved to {MODEL_PATH}")
