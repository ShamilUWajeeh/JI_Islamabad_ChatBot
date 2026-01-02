import os
from docx import Document

# --- CONFIG ---
# Folder where you extracted the ZIP file
SOURCE_FOLDER = "Urdu_Scans" 
OUTPUT_FILE = "Master_Constituency_List.txt"

def get_text_from_docx(path):
    """Reads ONLY text from a .docx file, ignoring images."""
    try:
        doc = Document(path)
        # extracting text from paragraphs
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip(): # Only keep lines that have text
                full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"⚠️ Warning: Could not read {path}. Error: {e}")
        return ""

def main():
    if not os.path.exists(SOURCE_FOLDER):
        print(f"❌ Error: Folder '{SOURCE_FOLDER}' not found.")
        return

    all_files = os.listdir(SOURCE_FOLDER)
    
    # 1. SMART FILTER: Only keep .docx files
    docx_files = [f for f in all_files if f.endswith(".docx") and not f.startswith("~$")]
    
    if not docx_files:
        print("❌ No .docx files found! Did you unzip the Google Drive download?")
        return

    # 2. NUMERIC SORT: Ensures Page_2 comes before Page_10
    # This finds the numbers in filenames like "Page_001.jpg_OCR.docx"
    try:
        docx_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    except:
        print("⚠️ Sorting by name (couldn't find numbers in filenames).")
        docx_files.sort()

    print(f"🚀 Found {len(docx_files)} Word documents. Merging text only...")
    print(f"🗑️ Ignoring {len(all_files) - len(docx_files)} image files (JPG/PNG).")

    full_content = "OFFICIAL CONSTITUENCY DATA (ISLAMABAD)\nMerged Data\n\n"

    # 3. MERGE LOOP
    for filename in docx_files:
        file_path = os.path.join(SOURCE_FOLDER, filename)
        print(f"   📄 Processing: {filename}...", end="")
        
        page_text = get_text_from_docx(file_path)
        
        # Add markers so the AI knows where a page starts/ends
        full_content += f"=== START OF PAGE: {filename} ===\n"
        full_content += page_text + "\n"
        full_content += "=== END OF PAGE ===\n\n"
        print(" Done.")

    # 4. SAVE
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"\n🎉 SUCCESS! Clean text saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()