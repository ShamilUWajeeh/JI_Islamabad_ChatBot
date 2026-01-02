import easyocr
from pdf2image import convert_from_path
import pandas as pd
import os

# --- CONFIGURATION ---
PDF_FILE = "Constituencies_Part_1.pdf"  # Your split file name
OUTPUT_CSV = "free_extracted_data.csv"

def extract_free():
    print("🚀 Loading Free OCR Engine (might take a minute)...")
    # 'ur' = Urdu, 'en' = English
    reader = easyocr.Reader(['ur', 'en'], gpu=False) 

    print(f"📸 Converting {PDF_FILE} to images...")
    try:
        images = convert_from_path(PDF_FILE)
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        print("💡 Hint: You might need to install 'Poppler' on Windows.")
        return

    all_data = []

    for i, image in enumerate(images):
        print(f"🔍 Scanning Page {i+1}...")
        
        # detail=0 gives simple text list
        result = reader.readtext(image, detail=0, paragraph=False)
        
        # EasyOCR returns a list of text chunks. 
        # We try to join them into a single string for the row
        page_text = " ".join(result)
        
        # Basic logic to try and find UC numbers (e.g., "10", "UC-10")
        # This is a bit "blind" because we lost the table structure
        all_data.append({
            "page": i+1,
            "raw_text": page_text
        })

    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"✅ Done! Check {OUTPUT_CSV}")
    print("👉 Note: Since this is free OCR, the columns might be mixed up.")
    print("   You will need to open the CSV and manually clean the data.")

if __name__ == "__main__":
    extract_free()