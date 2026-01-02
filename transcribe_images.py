import os
import time
from google import genai
from google.genai import types
import streamlit as st # Used only to grab secrets easily

# --- CONFIGURATION ---
IMAGE_FOLDER = "Urdu_Scans"       # Folder where your images are
OUTPUT_FILE = "New_Data_Extracted.txt" # File to save the text
MODEL_ID = "gemini-2.5-pro"      # Using the powerful model for best Urdu OCR

# 1. Setup Client (Grabs key from your .streamlit/secrets.toml)
# Note: Ensure you are running this from the main folder where secrets.toml exists
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    print("❌ Error: Could not find API Key in .streamlit/secrets.toml")
    exit()

client = genai.Client(api_key=api_key)

def transribe_image(image_path):
    """Sends image to Gemini and asks for formatted text extraction."""
    
    # Read image file
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
    2. GW-02: [Urdu/English Text]
    ...
    9. GW-09: [Urdu/English Text]
    CENSUS BLOCKS: [List of numbers separated by commas]
    
    3. Correct any obvious Urdu spelling errors (e.g. 'موٹی' to 'موتی').
    4. Do not include signature lines or header text like "ELECTION COMMISSION".
    """

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg") # Adjust mime_type if PNG
            ]
        )
        return response.text
    except Exception as e:
        print(f"⚠️ Error processing {image_path}: {e}")
        return None

# --- MAIN LOOP ---
def main():
    print(f"🚀 Starting Transcription using {MODEL_ID}...")
    
    # Get all images
    valid_extensions = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(valid_extensions)]
    files.sort() # Process in order

    if not files:
        print(f"❌ No images found in '{IMAGE_FOLDER}'")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, filename in enumerate(files):
            filepath = os.path.join(IMAGE_FOLDER, filename)
            print(f"[{i+1}/{len(files)}] Processing {filename}...", end=" ", flush=True)
            
            # Call AI
            text = transribe_image(filepath)
            
            if text:
                f.write(text + "\n\n")
                print("✅ Done.")
            else:
                print("❌ Failed.")
            
            # Small pause to be nice to the API
            time.sleep(2)

    print(f"\n🎉 All done! Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()