import re
import sys
from pathlib import Path
import fitz  # PyMuPDF

PDF_PATH = Path(r'C:\\Users\\ismailAfsinBaran\\Desktop\\Uzerinde_19_var.pdf')
if not PDF_PATH.is_file():
    print('PDF not found at expected location.')
    sys.exit(1)

# Open PDF and extract text page by page
full_text = ''
with fitz.open(str(PDF_PATH)) as doc:
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        txt = page.get_text("text")
        full_text += txt + '\n'

# Locate Surah Al‑Baqara heading (Arabic "سورة البقرة")
match = re.search(r'سورة\s*البقرة', full_text)
if not match:
    print('Surah Baqarah heading not found in PDF text.')
    # Show a snippet for debugging
    print('First 500 chars of extracted text:')
    print(full_text[:500])
    sys.exit(1)
start_idx = match.end()
# Find the next surah heading to define the end of Baqarah
next_match = re.search(r'سورة\s*[\u0621-\u064A]+', full_text[start_idx:])
end_idx = start_idx + next_match.start() if next_match else len(full_text)
baqarah_text = full_text[start_idx:end_idx]

# Define all Elif variants to count
elif_chars = {
    '\u0627': 'ا',   # Alef
    '\u0671': 'ٱ',   # Alef Wasla
    '\u0623': 'أ',   # Alef Hamza Above
    '\u0625': 'إ',   # Alef Hamza Below
    '\u0622': 'آ',   # Alef Madda
    '\u0670': 'ٰ',   # Superscript Alef (dagger alef)
    '\u0649': 'ى',   # Alef Maqsura
}

counts = {name: baqarah_text.count(char) for char, name in elif_chars.items()}

total = sum(counts.values())
print('Elif counts in Surah Baqarah (PDF via PyMuPDF):')
for name, cnt in counts.items():
    print(f'  {name}: {cnt}')
print('Total inclusive Elif count:', total)
