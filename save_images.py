import os
from pdf2image import convert_from_path

# CONFIG
PDF_FILE = "Final List of Constituencies (125)(1).pdf"
OUTPUT_FOLDER = "scanned_pages"

# Create folder if not exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

print(f"🚀 Converting '{PDF_FILE}' to images...")

# Convert all pages (300 DPI is best for Drive OCR)
images = convert_from_path(PDF_FILE, dpi=300)

for i, image in enumerate(images):
    page_num = i + 1
    filename = f"{OUTPUT_FOLDER}/Page_{page_num:03}.jpg"
    image.save(filename, "JPEG")
    print(f"✅ Saved {filename}")

print("\n🎉 All pages saved! Now upload the 'scanned_pages' folder to Google Drive.")