import os
import time
import random
from google import genai
from google.genai import types
import streamlit as st

# --- CONFIGURATION ---
IMAGE_FOLDER = "Urdu_Scans"
OUTPUT_FILE = "New_Data_Extracted.txt"
MODEL_ID = "gemini-2.5-pro"  # If this keeps failing, change to "gemini-1.5-flash"

# Setup Client
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    print("❌ Error: Could not find API Key in .streamlit/secrets.toml")
    exit()

client = genai.Client(api_key=api_key)

def transcribe_with_retry(image_path, retries=5):
    """Tries to transcribe. If 503 error, waits and tries again."""
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    You are an expert Data Entry Clerk. 
    Look at this image of an Election Commission Form-09.
    1. Extract the text exactly as it is (Urdu and English).
    2. Format it STRICTLY in this layout:
    === UC [Number]: [Name] ===
    EXTENT:
    1. GW-01: [Urdu/English Text]
    ...
    CENSUS BLOCKS: [List of numbers]
    3. Correct obvious Urdu spelling errors.
    """

    for attempt in range(retries):
        try:
            # Try sending to Google
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                ]
            )
            return response.text
            
        except Exception as e:
            # Check if it is a 503 (Overloaded) error
            error_str = str(e)
            if "503" in error_str or "429" in error_str:
                wait_time = (2 ** attempt) + random.uniform(0, 1) # Exponential backoff (2s, 4s, 8s...)
                print(f"   ⚠️ Server busy (503). Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                # If it's a different error, stop trying
                print(f"   ❌ Fatal Error: {e}")
                return None
    
    print("   ❌ Failed after multiple attempts.")
    return None

def main():
    print(f"🚀 Starting Transcription using {MODEL_ID}...")
    
    valid_extensions = (".jpg", ".jpeg", ".png")
    # Only pick files that start with "Page_" to avoid random images
    files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(valid_extensions) and f.startswith("Page_")]
    files.sort()

    if not files:
        print(f"❌ No 'Page_*.jpg' images found in '{IMAGE_FOLDER}'")
        return

    # append mode 'a' so we don't overwrite if we restart
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f: 
        for i, filename in enumerate(files):
            filepath = os.path.join(IMAGE_FOLDER, filename)
            print(f"[{i+1}/{len(files)}] Processing {filename}...", end=" ", flush=True)
            
            text = transcribe_with_retry(filepath)
            
            if text:
                f.write(text + "\n\n")
                print("✅ Done.")
                f.flush() # Save progress immediately
            else:
                f.write(f"\n=== FAILED PAGE: {filename} ===\n\n")
            
            # Standard pause between pages
            time.sleep(2)

    print(f"\n🎉 All done! Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()