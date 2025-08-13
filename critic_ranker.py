import os
import google.generativeai as genai

# --- Config ---
VARIANT_DIR = "variants"
BEST_SCRIPT_FILE = "input/script_2.txt"

# --- Setup Gemini ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# --- Scoring Prompt Template ---
def build_critic_prompt(script: str) -> str:
    return f"""
Evaluate the following 3-line promotional script for a catering video.

Script:
\"\"\"
{script}
\"\"\"

Rate the script from 1 to 10 on:
1. Clarity
2. Emotional impact
3. Strength of call to action

Only return the average score out of 10 as a number.
"""

# --- Score All Variants ---
best_score = -1
best_script = ""
variant_files = sorted(os.listdir(VARIANT_DIR))

for file in variant_files:
    with open(os.path.join(VARIANT_DIR, file), "r", encoding="utf-8") as f:
        script = f.read().strip()

    prompt = build_critic_prompt(script)

    try:
        response = model.generate_content(prompt)
        score_text = response.text.strip()

        score = float(score_text)
        print(f"[{file}] Score: {score:.2f}")

        if score > best_score:
            best_score = score
            best_script = script

    except Exception as e:
        print(f"[❌] Failed to score {file}: {e}")

# --- Save Best Script ---
if best_script:
    with open(BEST_SCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write(best_script)
    print(f"\n[✅] Best script saved to: {BEST_SCRIPT_FILE} (Score: {best_score:.2f})")
else:
    print("[⚠️] No script selected.")
