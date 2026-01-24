import re
import sys
from pathlib import Path

# Try to import PyPDF2; if not available, fallback to pdfminer
try:
    from PyPDF2 import PdfReader
except ImportError:
    print('PyPDF2 not installed. Please install it.')
    sys.exit(1)

PDF_PATH = Path(r'C:\\Users\\ismailAfsinBaran\\Desktop\\Uzerinde_19_var.pdf')
if not PDF_PATH.is_file():
    print('PDF not found at expected location.')
    sys.exit(1)

from pdfminer.high_level import extract_text

# Extract full text from PDF
full_text = extract_text(str(PDF_PATH))

# Find Surah Al-Baqara section (Arabic heading "سورة البقرة")
match = re.search(r'سورة\s*البقرة', full_text)
if not match:
    print('Surah Baqarah heading not found in PDF.')
    sys.exit(1)
start_idx = match.end()
# Assume next surah heading "سورة" marks end
next_match = re.search(r'سورة\s*[\u0621-\u064A]+', full_text[start_idx:])
end_idx = start_idx + next_match.start() if next_match else len(full_text)
baqarah_text = full_text[start_idx:end_idx]

# Define all Elif variants to count
elif_codes = {
    '\u0627': 'ا',   # Alef
    '\u0671': 'ٱ',   # Alef Wasla
    '\u0623': 'أ',   # Alef Hamza Above
    '\u0625': 'إ',   # Alef Hamza Below
    '\u0622': 'آ',   # Alef Madda
    '\u0670': 'ٰ',   # Superscript Alef
    '\u0649': 'ى',   # Alef Maqsura
}

counts = {name: baqarah_text.count(char) for char, name in elif_codes.items()}

total = sum(counts.values())
print('Elif counts in Surah Baqarah (PDF):')
for name, cnt in counts.items():
    print(f'  {name}: {cnt}')
print('Total Elif (all variants):', total)
