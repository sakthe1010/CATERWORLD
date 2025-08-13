import json

# --- Config ---
INPUT_FILE = "input/input.json"
PROMPT_FILE = "input/gen_prompt.txt"

# --- Load Metadata ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

name = data.get("caterer_name", "Our catering service")
tagline = data.get("tagline", "")
desc_lines = data.get("description", [])
cuisine = data.get("cuisine", [])
services = data.get("services", [])
tone = data.get("tone_preference", "elegant")  # default tone
location = data.get("location", "")

# --- Build Prompt ---
prompt = f"""You are a professional scriptwriter for marketing videos.

Generate a short, engaging 3-line promotional script for a catering service. The tone should be **{tone}**.

Details:
- Name: {name}
- Tagline: {tagline}
- Cuisine: {', '.join(cuisine)}
- Location: {location}
- Description: {" ".join(desc_lines)}
- Services: {', '.join(services)}

Ensure the script is clear, culturally relevant, emotionally resonant, and ends with a strong call to action.
Only output the 3-line script."""

# --- Save Prompt ---
with open(PROMPT_FILE, "w", encoding="utf-8") as f:
    f.write(prompt)

print(f"[✅] Prompt saved to {PROMPT_FILE}")
