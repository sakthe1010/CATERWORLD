import os
import json
import google.generativeai as genai

# --- Config ---
INPUT_FILE = "input/input.json"
VARIANT_DIR = "variants"
os.makedirs(VARIANT_DIR, exist_ok=True)

TONE_LIST = ["elegant", "emotional", "fun", "youthful", "luxurious"]

# --- Set API Key ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# --- Load Input ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

name = data.get("caterer_name", "")
tagline = data.get("tagline", "")
desc_lines = data.get("description", [])
cuisine = data.get("cuisine", [])
services = data.get("services", [])
location = data.get("location", "")

desc_text = " ".join(desc_lines)
cuisine_text = ", ".join(cuisine)
services_text = ", ".join(services)

# --- Generate Variants ---
for i, tone in enumerate(TONE_LIST, 1):
    prompt = f"""
Generate a short, 3-line promotional video script for a catering service.
Use a **{tone}** tone and end with a strong call to action.

Details:
- Name: {name}
- Tagline: {tagline}
- Cuisine: {cuisine_text}
- Location: {location}
- Description: {desc_text}
- Services: {services_text}

Only output the 3-line script without extra text.
"""

    try:
        response = model.generate_content(prompt)
        output_text = response.text.strip()

        out_path = os.path.join(VARIANT_DIR, f"variant_{i}_{tone}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output_text)

        print(f"[✅] Saved: {out_path}")

    except Exception as e:
        print(f"[❌] Failed for tone '{tone}': {e}")
