import fitz  # PyMuPDF
from pathlib import Path

PDF_PATH = Path(r'C:\Users\ismailAfsinBaran\Desktop\Uzerinde_19_var.pdf')

def extract_pages(pdf_path, start_page, end_page):
    if not pdf_path.exists():
        return "File not found."
    
    doc = fitz.open(pdf_path)
    text = ""
    for i in range(start_page - 1, min(end_page, len(doc))):
        page = doc.load_page(i)
        text += f"\n--- Page {i+1} ---\n"
        text += page.get_text()
    
    doc.close()
    return text

if __name__ == "__main__":
    # Extracting pages 120 to 140
    result = extract_pages(PDF_PATH, 120, 140)
    with open('alm_study.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print("Extracted pages 120-140 to alm_study.txt")
