import re
import sys
from pathlib import Path

# OCR libraries
from pdf2image import convert_from_path
import pytesseract

PDF_PATH = Path(r'C:\\Users\\ismailAfsinBaran\\Desktop\\Uzerinde_19_var.pdf')
if not PDF_PATH.is_file():
    print('PDF not found at expected location.')
    sys.exit(1)

# Convert PDF pages to images (resolution 300 DPI for better OCR)
print('Converting PDF pages to images...')
pages = convert_from_path(str(PDF_PATH), dpi=300)
full_text = ''
for i, page in enumerate(pages, start=1):
    txt = pytesseract.image_to_string(page, lang='ara')  # Arabic language
    full_text += txt + '\n'
    print(f'Processed page {i}/{len(pages)}')

# Find Surah Al-Baqara heading (common phrase "سورة البقرة")
match = re.search(r'سورة\s*البقرة', full_text)
if not match:
    print('Surah Baqarah heading not found in OCR text.')
    # For debugging, show first 500 chars
    print('First 500 chars of OCR output:')
    print(full_text[:500])
    sys.exit(1)
start_idx = match.end()
# Find next surah heading ("سورة" followed by Arabic word) to mark end
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
    '\u0670': 'ٰ',   # Superscript Alef
    '\u0649': 'ى',   # Alef Maqsura
}

counts = {name: baqarah_text.count(char) for char, name in elif_chars.items()}

total = sum(counts.values())
print('Elif counts in Surah Baqarah (from PDF OCR):')
for name, cnt in counts.items():
    print(f'  {name}: {cnt}')
print('Total Elif (all variants):', total)
