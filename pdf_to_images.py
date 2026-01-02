import fitz  # PyMuPDF
import os

# --- CONFIGURATION ---
PDF_FILE = "Mansoona e Amal 36 pages-1.pdf"    # Name of your PDF file
OUTPUT_FOLDER = "Urdu_Scans"    # Folder to save images
ZOOM_LEVEL = 2                  # 2 = High Quality (200 DPI), 1 = Standard

def pdf_to_images():
    # 1. Check if PDF exists
    if not os.path.exists(PDF_FILE):
        print(f"❌ Error: Could not find '{PDF_FILE}'. Please check the name.")
        return

    # 2. Create Output Folder if not exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"📁 Created folder: {OUTPUT_FOLDER}")

    # 3. Open PDF
    print(f"📄 Opening {PDF_FILE}...")
    doc = fitz.open(PDF_FILE)
    total_pages = len(doc)
    print(f"✅ Found {total_pages} pages. Starting conversion...")

    # 4. Loop through pages
    for i in range(total_pages):
        page = doc.load_page(i)
        
        # Set Zoom (Matrix) for higher quality
        mat = fitz.Matrix(ZOOM_LEVEL, ZOOM_LEVEL)
        pix = page.get_pixmap(matrix=mat)
        
        # Define Filename (e.g., Page_001.jpg)
        page_num = i + 1
        output_filename = f"Page_{page_num:03d}.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Save
        pix.save(output_path)
        print(f"   Saved: {output_filename}")

    print(f"\n🎉 Success! {total_pages} images saved in '{OUTPUT_FOLDER}'.")

if __name__ == "__main__":
    pdf_to_images()