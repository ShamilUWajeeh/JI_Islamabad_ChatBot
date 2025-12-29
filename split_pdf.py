from pypdf import PdfReader, PdfWriter

# CONFIGURATION
INPUT_FILE = "Final List of Constituencies (125)(1).pdf"
PAGES_PER_CHUNK = 7  # Changed from 20 to 7

def safe_split():
    try:
        reader = PdfReader(INPUT_FILE)
        total_pages = len(reader.pages)
        print(f"📄 Found {total_pages} pages. Splitting into chunks of {PAGES_PER_CHUNK}...")
        
        for i in range(0, total_pages, PAGES_PER_CHUNK):
            writer = PdfWriter()
            # Calculate where this chunk ends (don't go past the last page)
            end_page = min(i + PAGES_PER_CHUNK, total_pages)
            
            # Add pages to the new PDF
            for page_num in range(i, end_page):
                writer.add_page(reader.pages[page_num])
            
            # Save the new file
            # Example: Constituencies_Part_1.pdf, Part_2.pdf...
            part_num = (i // PAGES_PER_CHUNK) + 1
            output_filename = f"Constituencies_Part_{part_num}.pdf"
            
            with open(output_filename, "wb") as out:
                writer.write(out)
            
            print(f"✅ Created: {output_filename} (Pages {i+1}-{end_page})")
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{INPUT_FILE}'. Make sure it is in the same folder.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    safe_split()