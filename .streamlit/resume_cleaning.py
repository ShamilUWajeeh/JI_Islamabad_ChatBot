import os
import time
import toml 
from google import genai
from google.genai import types

# --- CONFIG ---
INPUT_FILE = "Master_Constituency_List.txt"
OUTPUT_FILE = "Cleaned_Part_2.txt" # We save this as a separate part first
START_PAGE = 71  # We restart from here
DELAY_SECONDS = 15 # We increase delay to 15s to be 100% safe

# Load API Key
try:
    secrets = toml.load(".streamlit/secrets.toml")
    API_KEY = secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyDkBOYpa3Yd3D5LGmEHwOoM-bPI9Woxwu8"

MODEL_ID = "gemini-2.0-flash" 

def resume_cleaning():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: '{INPUT_FILE}' not found.")
        return

    client = genai.Client(api_key=API_KEY)
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    all_pages = raw_text.split("=== END OF PAGE ===")
    
    # SLICE THE LIST: Only take pages from 70 onwards (Index starts at 0, so 71 is index 70)
    pages_to_process = all_pages[START_PAGE-1:] 
    
    cleaned_part_2 = ""
    total_remaining = len(pages_to_process)

    print(f"🧹 Resuming cleaning from Page {START_PAGE}...")
    print(f"📄 Remaining Pages: {total_remaining}")
    print(f"⏳ Speed: 1 page every {DELAY_SECONDS} seconds (Slow & Safe mode)")

    for i, page_content in enumerate(pages_to_process):
        current_page_num = START_PAGE + i
        
        if not page_content.strip(): 
            continue

        print(f"   ✨ Cleaning Page {current_page_num}...", end="")
        
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
            cleaned_part_2 += response.text + "\n=== END OF PAGE ===\n"
            print(" Done.")
            
            # WAIT LONGER TO AVOID 429 ERROR
            time.sleep(DELAY_SECONDS) 

        except Exception as e:
            print(f"❌ Error on page {current_page_num}: {e}")
            if "429" in str(e):
                print("   ⚠️ Quota hit again! Waiting 60 seconds...")
                time.sleep(60) # Wait a full minute if we hit the limit
            
            cleaned_part_2 += page_content + "\n=== END OF PAGE ===\n"

    # Save Part 2
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(cleaned_part_2)
    
    print(f"\n🎉 Part 2 Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    resume_cleaning()