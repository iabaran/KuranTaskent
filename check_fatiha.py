# -*- coding: utf-8 -*-
import json
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('quran_arabic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Function to remove all diacritics
def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670\u0617-\u061A\u06D6-\u06ED]')
    return arabic_diacritics.sub('', text)

# Check Fatiha specifically
fatiha = data[0]
print("="*60)
print("FATİHA SURESİ ANALİZİ")
print("="*60)

for i, verse in enumerate(fatiha['verses'][:4], 1):
    clean = remove_diacritics(verse['text'])
    rahman_count = clean.count('رحمن')
    rahim_count = clean.count('رحيم')
    
    print(f"\n1:{i} - {verse['text']}")
    print(f"  Rahman: {rahman_count}, Rahim: {rahim_count}")

# Now count ALL occurrences properly
print("\n" + "="*60)
print("TÜM KUR'AN ANALİZİ")
print("="*60)

rahman_in_verses = 0
rahim_in_verses = 0

for surah in data:
    for verse in surah['verses']:
        clean_text = remove_diacritics(verse['text'])
        rahman_in_verses += clean_text.count('رحمن')
        rahim_in_verses += clean_text.count('رحيم')

print(f"\nAyetlerde geçen Rahman: {rahman_in_verses}")
print(f"Ayetlerde geçen Rahim: {rahim_in_verses}")

# Basmalas: 113 surahs (excluding Tawbah)
# Each Basmala has 1 Rahman and 1 Rahim
# BUT Fatiha's Basmala is already counted in verses!
# So we need to add 112 more Basmalas (not 113)

basmala_count = 112  # All surahs except Tawbah (9) and Fatiha (1) = 114 - 2 = 112

total_rahman = rahman_in_verses + basmala_count
total_rahim = rahim_in_verses + basmala_count

print(f"\nBesmele eklenecek: {basmala_count} (Fatiha'nın Besmelesi zaten sayıldı)")
print(f"\nTOPLAM Rahman: {total_rahman} ({rahman_in_verses} ayet + {basmala_count} Besmele)")
print(f"TOPLAM Rahim: {total_rahim} ({rahim_in_verses} ayet + {basmala_count} Besmele)")
