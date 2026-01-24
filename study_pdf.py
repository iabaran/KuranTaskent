import fitz  # PyMuPDF
from pathlib import Path

PDF_PATH = Path(r'C:\Users\ismailAfsinBaran\Desktop\Uzerinde_19_var.pdf')

def extract_intro(pdf_path, num_pages=30):
    if not pdf_path.exists():
        return "File not found."
    
    doc = fitz.open(pdf_path)
    text = ""
    for i in range(min(num_pages, len(doc))):
        page = doc.load_page(i)
        text += f"\n--- Page {i+1} ---\n"
        text += page.get_text()
    
    doc.close()
    return text

if __name__ == "__main__":
    result = extract_intro(PDF_PATH)
    with open('pdf_study.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print("Extracted first 30 pages to pdf_study.txt")
