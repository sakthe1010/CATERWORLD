import pandas as pd

# --- Load scores ---
gemini = pd.read_csv("output/gemini_scores.csv")
reward = pd.read_csv("output/reward_scores.csv")

# --- Merge on filename ---
merged = pd.merge(gemini, reward[["filename", "score"]], on="filename", suffixes=("_gemini", "_reward"))

# --- Average scores ---
avg_gemini = merged["score_gemini"].mean()
avg_reward = merged["score_reward"].mean()
improvement = ((avg_reward - avg_gemini) / avg_gemini) * 100

# --- Low-quality threshold ---
threshold = 7.0
low_gemini = (merged["score_gemini"] < threshold).sum()
low_reward = (merged["score_reward"] < threshold).sum()

if low_gemini > 0:
    reduction = ((low_gemini - low_reward) / low_gemini) * 100
else:
    reduction = 0.0

# --- Print results ---
print(f"📊 Average Gemini Score: {avg_gemini:.3f}")
print(f"📈 Average Reward Model Score: {avg_reward:.3f}")
print(f"✅ Improvement: {improvement:.2f}%")
print(f"🧹 Low-Quality Scripts (Score < {threshold}): Gemini = {low_gemini}, Reward = {low_reward}")
print(f"🚀 Reduction in Low-Quality Outputs: {reduction:.2f}%")
