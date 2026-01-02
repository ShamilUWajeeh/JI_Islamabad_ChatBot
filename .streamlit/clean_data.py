import os
import time
import toml 
from google import genai
from google.genai import types

# --- CONFIG ---
INPUT_FILE = "Master_Constituency_List.txt"
OUTPUT_FILE = "Cleaned_Master_List.txt"

# Load API Key
try:
    secrets = toml.load(".streamlit/secrets.toml")
    API_KEY = secrets["GEMINI_API_KEY"]
except:
    print("❌ Could not find secrets.toml. Please paste your key manually in the code.")
    API_KEY = "AIzaSyBu5znNIizdEc874B6vFtBgwvwfGeGd6kY"

# ✅ UPDATED: Using the model explicitly found in your list
MODEL_ID = "gemini-2.0-flash" 

def clean_text_file():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: '{INPUT_FILE}' not found.")
        return

    # Initialize Client
    client = genai.Client(api_key=API_KEY)
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    pages = raw_text.split("=== END OF PAGE ===")
    cleaned_full_text = ""
    total_pages = len(pages)

    print(f"🧹 Starting cleaning using {MODEL_ID}...")
    print(f"📄 Total Pages: {total_pages}")

    for i, page_content in enumerate(pages):
        if not page_content.strip(): continue

        print(f"   ✨ Cleaning Page {i+1}/{total_pages}...", end="")
        
        prompt = """
        You are an Expert Urdu Editor.
        1. Fix Urdu spelling errors (e.g., 'گوکین' to 'گوکینہ').
        2. Do NOT change English codes (GW-01).
        3. Return ONLY the corrected text.
        """

        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=prompt),
                            types.Part.from_text(text=page_content)
                        ]
                    )
                ]
            )
            cleaned_full_text += response.text + "\n=== END OF PAGE ===\n"
            print(" Done.")
            time.sleep(4) # Keep safe distance for free tier

        except Exception as e:
            print(f"❌ Error on page {i+1}: {e}")
            cleaned_full_text += page_content + "\n=== END OF PAGE ===\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(cleaned_full_text)
    
    print(f"\n🎉 Success! Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_text_file()